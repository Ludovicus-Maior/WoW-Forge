#!/usr/bin/env python


import boto
from boto.s3.key import Key
import os
import time
import wf.logger


def save_ah_file(local_file, zone, realm, timestamp, retry=3):
    try:
        s3_conn = boto.connect_s3()
        bucket = s3_conn.get_bucket('wf-ah-data')
        key = Key(bucket)
        key.key = "%s/%s/%s.json" % (zone, realm, timestamp)
        wf.logger.logger.info("copying %s to %s" % (local_file, key.key))
        key.set_contents_from_filename(local_file)
    except Exception:
        if retry > 0:
            wf.logger.logger.exception("Error while writing file, retry up to %d times" % retry)
            time.sleep(2.0)
            return save_ah_file(local_file, zone, realm, timestamp, retry=(retry-1))
        else:
            raise
    finally:
        # Clean up.  The file may be gone if we retried.
        if os.path.isfile(local_file):
            os.unlink(local_file)

