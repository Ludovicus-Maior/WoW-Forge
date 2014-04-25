#!/bin/bash

# AWS Bootstrap script for WOW-FORGE worker nodes

# Enable verbose script execution tracing and remap STDERR to STDOUT
set -vx
exec 2>&1

# Update APT and install necessary packages
apt-get update
apt-get install -y debconf-utils python-pip python-dev ruby1.9.1 ruby1.9.1-dev build-essential wget libruby1.9.1 libxslt-dev libxml2-dev mysql-client libmysqlclient-dev git

# Lets use the new commands!
hash -r

# Automatically install all security patches
echo "unattended-upgrades	unattended-upgrades/enable_auto_updates	boolean	true" | debconf-set-selections
dpkg-reconfigure -f noninteractive unattended-upgrades
unattended-upgrade

export INSTANCE_ID=$(wget -qO- http://169.254.169.254/latest/meta-data/instance-id)
export REGION=$(wget -qO- http://169.254.169.254/latest/meta-data/placement/availability-zone | rev | cut -b 2- | rev)

# Install all required PIPs
pip install boto --upgrade
pip install mysql-python

# Install all required GEMs
gem install aws-sdk --no-rdoc --no-ri

# Set the HOSTNAME, comes after potential Elastic IP assignment
export HOSTNAME=$(wget -qO- http://169.254.169.254/latest/meta-data/public-hostname)
echo $HOSTNAME > /etc/hostname
echo $HOSTNAME > /etc/mailname
hostname $HOSTNAME

# A ruby script to get a tarball with bootstrap information
(
cat <<'EOP'
require 'aws-sdk'
AWS.config(:credential_provider => AWS::Core::CredentialProviders::EC2Provider.new)
AWS::S3.new.buckets["wow-forge-bootstrap"].objects["#{ARGV[0]}/#{ARGV[1]}/#{ARGV[2]}"].read { |chunk| print chunk }
EOP
) > /tmp/get_bootstrap_file.rb

# Initial config file overrides
cd /
ruby /tmp/get_bootstrap_file.rb $REGION worker root.tar | tar xvpo

# Initial worker user setup
addgroup worker
adduser --ingroup worker --disabled-login --gecos "Joe Worker" worker

cd ~worker
sudo -n -u worker bash -c "ruby /tmp/get_bootstrap_file.rb $REGION worker worker.tar | tar xvpo"
sudo -n -u worker bash -c "cd /home ; git clone git@github.com:Ludovicus/WoW-Forge.git worker"

reboot
