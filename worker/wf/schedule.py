import json
import os
import wf.logger
import wf.rds
import wf.sqs


def Schedule_AH(region, realms=None):

    if not realms:
        realm = wf.rds.SelectStaleRealm(region)
        if realm:
            realms = [realm]
        else:
            wf.logger.logger.warning("Schedule_AH: There were no stale realms!")
            return
    rr = ["Process-AH.py", region]
    rr.extend(realms)
    wf.logger.logger.info("Enqueue %s" % json.dumps(rr))
    if "WF_SQS_REGION" in os.environ:
        q = wf.sqs.ConnectSQS(region=os.environ["WF_SQS_REGION"], queue=os.environ["WF_SQS_QUEUE"])
        wf.sqs.PutSeq(q, rr)

def Complete_AH(region, realm):
    return

def Schedule_Toons(region, realm, toons):

    rr = ["Process-Toons.py", region, realm, ]
    rr.extend(toons)
    wf.logger.logger.info("Enqueue %s" % json.dumps(rr))
    if "WF_SQS_REGION" in os.environ:
        q = wf.sqs.ConnectSQS(region=os.environ["WF_SQS_REGION"], queue=os.environ["WF_SQS_QUEUE"])
        wf.sqs.PutSeq(q, rr)

def Schedule_Guilds(region, realm, guilds):

    rr = ["Process-Guilds.py", region, realm, ]
    rr.extend(guilds)
    wf.logger.logger.info("Enqueue %s" % json.dumps(rr))
    if "WF_SQS_REGION" in os.environ:
        q = wf.sqs.ConnectSQS(region=os.environ["WF_SQS_REGION"], queue=os.environ["WF_SQS_QUEUE"])
        wf.sqs.PutSeq(q, rr)