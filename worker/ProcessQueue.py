#!/usr/bin/env python

import boto.sqs
import json
import os
import subprocess
import sys
import time
import traceback
import wf.logger
import wf.schedule
import wf.sqs

def DoMessage(q,jmsg):
    try:
        subprocess.check_call(jmsg)
    except OSError:
        wf.logger.logger.exception("Unable to execute message: %s" % jmsg)
        raise
    except subprocess.CalledProcessError:
        wf.logger.logger.exception("Error while executing message: %s" % jmsg)
        wf.sqs.PutSeq(q, jmsg)


if __name__ == "__main__":
    start_time = time.time()
    q = wf.sqs.ConnectSQS(region=os.environ["WF_SQS_REGION"], queue=os.environ["WF_SQS_QUEUE"])
    m = wf.sqs.GetJsonMessage(q)
    while True:
        if m:
            DoMessage(q, m)
        else:
            wf.schedule.Schedule_AH("US")
        current_time = time.time()
        # After 15 minutes, allow the driver to do maintenance
        if (current_time-start_time) > 60*15:
            wf.logger.logger.info("Exiting to allow for maintenance")
            exit(0)
        m = wf.sqs.GetJsonMessage(q)
