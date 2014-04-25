#!/usr/bin/env python

import boto.sqs
import json
import os
import subprocess
import time
import traceback


def Connect(region="us-west-2", queue="WorkerQ"):
    try:
        conn = boto.sqs.connect_to_region(region)
	try:
            q = conn.get_queue(queue)
	    return q
	except:
            print "Unable to connect to SQS queue %s" % queue
            print (traceback.format_exc())
    except:
        print "Unable to connect to SQS region %s" % region
        print (traceback.format_exc())
    exit(1)


def GetJsonMessage(q):
    while True:
        rs = q.get_messages(num_messages=1,  wait_time_seconds=60*5)
        if len(rs) > 0:
            break
    msg = rs[0].get_body()
    q.delete_message(msg)
    jmsg = json.loads(msg)
    return jmsg


def DoMessage(q,jmsg):
    try:
        subprocess.check_call(jmsg)
    except OSError:
        print "Unable to execute message: %s" % jmsg
        print (traceback.format_exc())
    except subprocess.CalledProcessError:
        print "Error while executing message: %s" % jmsg
        m = boto.sqs.message.Message()
        m.set_body(json.dumps(jmsg))
        q.write(m)

if __name__ == "__main__":
    stime = time.time()
    q = Connect(region=os.environ["WF_SQS_REGION"], queue=os.environ["WF_SQS_QUEUE"])
    m = GetJsonMessage(q)
    while m:
        DoMessage(q, m)
	ctime = time.time()
	# After 15 minutes, allow the driver to do maintainance
	if ( (ctime-stime) > 60*15 ):
	    exit(0)
        m = GetJsonMessage(q)
