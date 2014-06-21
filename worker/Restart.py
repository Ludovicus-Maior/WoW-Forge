#!/usr/bin/env python

import os
import sys
import wf.logger
import wf.rds
import wf.schedule
import wf.sqs

from optparse import OptionParser


if __name__ == "__main__":
    wf.logger.logger.info("Draining SQS queue")
    q = wf.sqs.ConnectSQS(region=os.environ["WF_SQS_REGION"], queue=os.environ["WF_SQS_QUEUE"])
    count = wf.sqs.Drain(q)
    wf.logger.logger.info("Removed %d messages" % count)

    wf.logger.logger.info("Resetting AH queue times.")
    wf.rds.ResetRealms()

    if len(sys.argv) > 1:
        wf.logger.logger.info("Scheduling Bootstrap jobs.")
        wf.schedule.Schedule_Guilds("US", "Uldaman", ["Aviary of Radagast", "Suomen Pankki", "Two Percent"])
        wf.schedule.Schedule_Guilds("US", "Dawnbringer", ["Mixed Nutz", "ShadowGrove"])
        wf.schedule.Schedule_Guilds("US", "Cenarion Circle", ["MoonBough", "Fuel the Fire"])
        wf.schedule.Schedule_AH("US", ["Uldaman"])
        wf.schedule.Schedule_AH("US", ["Cenarion Circle"])
        wf.schedule.Schedule_AH("US", ["Dawnbringer"])