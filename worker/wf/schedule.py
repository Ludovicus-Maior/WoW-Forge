import json
import os
import wf.logger
import wf.rds
import wf.sqs


def Schedule_AH(region, realm=None):

    if not realm:
        realm = wf.rds.SelectStaleRealm(region)
    rr = ["Process-Realm.py", region, realm]
    wf.logger.logger.info(json.dumps(rr))
    if "WF_SQS_REGION" in os.environ:
        q = wf.sqs.ConnectSQS(region=os.environ["WF_SQS_REGION"], queue=os.environ["WF_SQS_QUEUE"])
        wf.sqs.PutSeq(q, rr)

def Complete_AH(region, realm):
    return

def Schedule_Toons(region, realm, toons):

    rr = ["Process-Toons.py", region, realm, ]
    rr.extend(toons)
    wf.logger.logger.info(json.dumps(rr))
    if "WF_SQS_REGION" in os.environ:
        q = wf.sqs.ConnectSQS(region=os.environ["WF_SQS_REGION"], queue=os.environ["WF_SQS_QUEUE"])
        wf.sqs.PutSeq(q, rr)

def Schedule_Guilds(region, realm, guilds):

    rr = ["Process-Guilds.py", region, realm, ]
    rr.extend(guilds)
    wf.logger.logger.info(json.dumps(rr))
    if "WF_SQS_REGION" in os.environ:
        q = wf.sqs.ConnectSQS(region=os.environ["WF_SQS_REGION"], queue=os.environ["WF_SQS_QUEUE"])
        wf.sqs.PutSeq(q, rr)