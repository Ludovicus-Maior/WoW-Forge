#!/usr/bin/env python


import boto
from boto.s3.key import Key
import os
import wf.logger

def save_ah_file(local_file, zone, realm, timestamp):
    s3_conn = boto.connect_s3()
    bucket = s3_conn.get_bucket('wf-ah-data')
    key = Key(bucket)
    key.key = "%s/%s/%s.json" % (zone, realm, timestamp)
    wf.logger.logger.info("copying %s to %s" % (local_file, key.generate_url(0)))
    key.set_contents_from_filename(local_file)
    os.unlink(local_file)

