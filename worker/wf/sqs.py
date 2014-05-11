#!/usr/bin/env python

import boto.sqs
import json
import wf.logger



def ConnectSQS(region="us-west-1", queue="WorkerQ"):
    try:
        conn = boto.sqs.connect_to_region(region)
        try:
            q = conn.get_queue(queue)
            return q
        except StandardError:
            wf.logger.logger.exception("Unable to connect to SQS queue %s" % queue)
            raise
    except StandardError:
        wf.logger.logger.exception("Unable to connect to SQS region %s" % region)
        raise
    exit(1)


def PutSeq(queue, seq):
    mesg = boto.sqs.message.Message()
    mesg.set_body(json.dumps(seq))
    queue.write(mesg)
