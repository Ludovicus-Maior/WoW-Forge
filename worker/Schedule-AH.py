#!/usr/bin/env python

import boto.sqs
import json
import MySQLdb
import os
import time
import random

def ConnectDatabase(auto_commit):
    global database
    try:
        db_user=os.environ['WOWFORGE_DB_USER']
        db_pass=os.environ['WOWFORGE_DB_PASSWORD']
    except:
        print "Missing environment variable setup for WOWFORGE_DB_*"
        pass

    database=MySQLdb.connect(user=db_user,passwd=db_pass,db="Warcraft")
    database.autocommit(auto_commit)
    
def ConnectSQS(region="us-west-2", queue="WorkerQ"):
    try:
        conn = boto.sqs.connect_to_region(region)
	try:
            q = conn.get_queue(queue)
	except:
	    q = conn.create_queue(queue,...)
        return q
    except:
        print "Unable to connect to SQS region %s" % region
        print (traceback.format_exc())
    exit(1)

def SelectStaleRealm(region):
    global database
    c=database.cursor()
    c.execute("""SELECT `name` FROM `realmStatus` WHERE `region` = %s and `enqueueTime` = 0 ORDER BY `lastModified` LIMIT 1;""" ,(region,))
    d=c.fetchone()
    realm=d[0]
    c.execute("""UPDATE `realmStatus` SET `enqueueTime` = %s WHERE `enqueueTime` = 0 and `name` = %s and  `region` = %s;""" , (time.time(),realm,region))
    return [region,realm]
    
if __name__ == "__main__":
    region = "US"
    
    ConnectDatabase(True)
    rr=SelectStaleRealm("US")
    rr.insert(0,"Process-Realm.py")
    print json.dumps(rr)
    q = ConnectSQS()
    m = boto.sqs.message.Message()
    m.set_body(json.dumps(rr))
    q.write(m)


    
