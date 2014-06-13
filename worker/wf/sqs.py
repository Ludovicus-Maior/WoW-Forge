#!/usr/bin/env python

import boto.sqs
import json
import wf.logger
from boto.sqs.message import RawMessage



def ConnectSQS(region="us-west-1", queue="WorkerQ"):
    try:
        conn = boto.sqs.connect_to_region(region)
        try:
            q = conn.get_queue(queue)
            q.set_message_class(RawMessage)
            return q
        except StandardError:
            wf.logger.logger.exception("Unable to connect to SQS queue %s" % queue)
            raise
    except StandardError:
        wf.logger.logger.exception("Unable to connect to SQS region %s" % region)
        raise
    exit(1)


def PutSeq(queue, seq):
    mesg = boto.sqs.message.RawMessage()
    mesg.set_body(json.dumps(seq, ensure_ascii=True))
    queue.write(mesg)


def GetJsonMessage(q):
    rs = q.get_messages(num_messages=1,  wait_time_seconds=20)
    if len(rs) == 0:
        return None
    msg = rs[0].get_body()
    q.delete_message(rs[0])
    jmsg = json.loads(msg)
    return jmsg

def Drain(queue):
    rs = queue.get_messages(num_messages=1,  wait_time_seconds=1)
    count = 0
    while len(rs) > 0:
        queue.delete_message(rs[0])
        count += 1
        rs = queue.get_messages(num_messages=1,  wait_time_seconds=1)
    return count

