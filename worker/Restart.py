#!/usr/bin/env python


import os
import wf.logger
import wf.rds
import wf.schedule
import wf.sqs


if __name__ == "__main__":
    wf.logger.logger.info("Draining SQS queue")
    q = wf.sqs.ConnectSQS(region=os.environ["WF_SQS_REGION"], queue=os.environ["WF_SQS_QUEUE"])
    count = wf.sqs.Drain(q)
    wf.logger.logger.info("Removed %d messages" % count)

    wf.logger.logger.info("Resetting AH queue times.")
    wf.rds.ResetRealms()

