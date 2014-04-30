#!/bin/bash

# AWS Bootstrap script for WOW-FORGE worker nodes

# Enable verbose script execution tracing and remap STDERR to STDOUT
set -vx
exec 2>&1

# Update APT and install necessary packages
apt-get update
apt-get install -y debconf-utils python-pip python-dev build-essential wget mysql-client libmysqlclient-dev git

# Lets use the new commands!
hash -r

# Automatically install all security patches
echo "unattended-upgrades	unattended-upgrades/enable_auto_updates	boolean	true" | debconf-set-selections
dpkg-reconfigure -f noninteractive unattended-upgrades
unattended-upgrade

export INSTANCE_ID=$(wget -qO- http://169.254.169.254/latest/meta-data/instance-id)
export REGION=$(wget -qO- http://169.254.169.254/latest/meta-data/placement/availability-zone | rev | cut -b 2- | rev)
export ITYPE=$(wget -qO- http://169.254.169.254/latest/meta-data/instance-type)

# Initialize swap for small or micro instances
case $ITYPE in
*.micro|*.small)
    dd if=/dev/zero of=/swap bs=1M count=1024
    mkswap /swap
    chown root:root /swap
    chmod 600 /swap
    echo "/swap swap swap defaults 0 0" >> /etc/fstab
    swapon /swap
    ;;
*)
    echo "No special actions for $ITYPE"
    ;;
esac

# Install all required PIPs
pip install boto --upgrade
pip install mysql-python

# Set the HOSTNAME
export HOSTNAME=$(wget -qO- http://169.254.169.254/latest/meta-data/public-hostname)
echo $HOSTNAME > /etc/hostname
echo $HOSTNAME > /etc/mailname
hostname $HOSTNAME

cat > /bin/get_bootstrap_file.py <<EOF
from boto.s3.connection import S3Connection
import sys

conn = S3Connection()
bucket = conn.get_bucket("wow-forge-bootstrap")
key  = bucket.get_key("%s/%s/%s" % (sys.argv[1], sys.argv[2], sys.argv[3]) )
key.get_contents_to_file(sys.stdout)
EOF

# Initial config file overrides
cd /
python /bin/get_bootstrap_file.py $REGION worker root.tar | tar xvpo

# Initial worker user setup
addgroup worker
adduser --ingroup worker --disabled-login --gecos "Joe Worker" worker

sudo -n -u worker bash -c "cd ~worker ; python /bin/get_bootstrap_file.py $REGION worker worker.tar | tar xvpo"
sudo -n -u worker bash -c "cd ~worker ; git init . ; git remote add -t \* -f origin git@github.com:Ludovicus/WoW-Forge.git ; git checkout master"

reboot
