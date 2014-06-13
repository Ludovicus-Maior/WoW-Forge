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
