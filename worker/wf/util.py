#!/usr/bin/env python

import wf.logger

import boto
import boto.ec2
import requests
import subprocess
import time

from boto.s3.key import Key

class LimitExceededError(StandardError):
    pass


def IsLimitExceeded(data):
    if 'status' in data and data['status'] == "nok":
        if 'reason' in data and data['reason'] == "Daily limit exceeded":
            raise LimitExceededError(data['reason'])


def Seppuku(why):
    # Get the instance ID
    r = requests.get("http://169.254.169.254/latest/meta-data/instance-id")
    if r.status_code != 200:
        wf.logger.logger.error("Seppuku() unable to get instance ID")
        exit(3)
    instance_id = r.text

    # Declare our intent
    wf.logger.logger.error("Seppuku(%s): Instance is stopping because [%s]" % (instance_id, why))

    # Save a copy of the latest syslog to S3
    s3_conn = boto.connect_s3()
    bucket = s3_conn.get_bucket('wf-instance-logs')
    key = Key(bucket)
    key.key = "%s.txt" % instance_id
    wf.logger.logger.error("Seppuku(%s): copying log to %s" % (instance_id, key.generate_url(0)))
    key.set_contents_from_filename('/var/log/syslog')


    # Now commit Seppuku
    ec2_conn = boto.ec2.connect_to_region("us-west-1")
    # this can throw an exception.  Protect later.
    ec2_conn.terminate_instances(instance_ids=[instance_id])
    time.sleep(60*5)

    # What!  No sleep?  Then halt
    subprocess.check_call(["sudo", "halt"])
    time.sleep(60*5)
    exit(9)

