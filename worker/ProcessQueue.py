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


def GetJsonMessage(q):
    rs = q.get_messages(num_messages=1,  wait_time_seconds=20)
    if len(rs) == 0:
        return None
    msg = rs[0].get_body()
    q.delete_message(rs[0])
    jmsg = json.loads(msg)
    return jmsg


def DoMessage(q,jmsg):
    try:
        subprocess.check_call(jmsg)
    except OSError:
        wf.logger.logger.exception("Unable to execute message: %s" % jmsg)
        raise
    except subprocess.CalledProcessError:
        wf.logger.logger.exception("Error while executing message: %s" % jmsg)
        m = boto.sqs.message.Message()
        m.set_body(json.dumps(jmsg))
        q.write(m)

if __name__ == "__main__":
    stime = time.time()
    q = wf.sqs.ConnectSQS(region=os.environ["WF_SQS_REGION"], queue=os.environ["WF_SQS_QUEUE"])
    m = GetJsonMessage(q)
    while True:
        if m:
            DoMessage(q, m)
	else:
            wf.schedule.Schedule_AH("US")
        ctime = time.time()
        # After 15 minutes, allow the driver to do maintainance
        if ( (ctime-stime) > 60*15 ):
            wf.logger.logger.info("Exiting to allow for maintainance")
            exit(0)
        m = GetJsonMessage(q)
