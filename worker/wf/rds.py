#!/usr/bin/env python


import MySQLdb
import os
import datetime
import traceback
import wf.logger

database = None


def ConnectDatabase(auto_commit):
    global database
    try:
        db_user = os.environ['WF_RDS_USER']
        db_pass = os.environ['WF_RDS_PASSWORD']
        db_host = os.environ['WF_RDS_HOST']
    except:
        wf.logger.logger.exception("Missing environment variable setup for WF_RDS_*")
        raise

    database = MySQLdb.connect(user=db_user, passwd=db_pass, host=db_host, db="Warcraft")
    database.autocommit(auto_commit)


def SelectStaleRealm(region):
    global database
    if not database:
        ConnectDatabase(True)

    c = database.cursor()
    c.execute("""SELECT `name` FROM `realmStatus` WHERE `region` = %s AND `enqueueTime` IS NULL ORDER BY `lastAuctionScan` LIMIT 1;""" ,
              (region,))
    d = c.fetchone()
    realm = d[0]
    now = datetime.datetime.utcnow()
    c.execute("""UPDATE `realmStatus` SET `enqueueTime` = %s WHERE `enqueueTime` IS NULL and `name` = %s and  `region` = %s;""",
              (now.isoformat(' '), realm, region))
    return realm


def GetSiblings(region, realm):
    global database
    if not database:
        ConnectDatabase(True)

    c = database.cursor()
    c.execute("""SELECT `realm`, `sibling` FROM `realmSibling` WHERE `region` = %s AND ( `realm` = %s OR `sibling` = %s) ;""",
              (region, realm, realm))

    d = c.fetchone()
    s = set()
    while d is not None:
        s.add(d[0])
        s.add(d[1])
        d = c.fetchone()
    return s

def AddSibling(region, realm_main, realm_aux):
    global database
    if not database:
        ConnectDatabase(True)

    c = database.cursor()

    if realm_main > realm_aux:
        realm_main, realm_aux = realm_aux, realm_main

    c.execute("""INSERT INTO `realmSibling` (`realm`, `region`, `sibling`) VALUES (%s, %s, %s) ;""",
              (realm_main, region, realm_aux))


def GetToons(region, realm):
    global database
    if not database:
        ConnectDatabase(True)

    c = database.cursor()
    c.execute("""SELECT `name`, `lastUpdate` FROM `realmCharacter` WHERE `region` = %s AND `realm` = %s ;""",
              (region, realm))

    d = c.fetchone()
    h = {}
    while d is not None:
        h[d[0]] = d[1]
        d = c.fetchone()
    return h


itemRandoms = None
itemSeeds = None
def RecordRandomEnchant(id, enchant_rand, enchant_seed):
    global itemRandoms
    global itemSeeds

    if not itemRandoms:
        itemRandoms = []
    if not itemSeeds:
        itemSeeds = []

    if id:
        itemRandoms.append((id, enchant_rand))
        itemSeeds.append((id, enchant_seed))

    if id and len(itemRandoms) < 100:
        return

    global database
    if not database:
        ConnectDatabase(True)

    c = database.cursor()
    c.executemany("""INSERT INTO `itemRandomEnchants` (`id`,`randomEnchant`,`count`) VALUES (%s,%s,1) ON DUPLICATE KEY UPDATE count=count+1;""",
              itemRandoms)
    itemRandoms = []
    c.executemany("""INSERT INTO `itemSeeds` (`id`,`seed`,`count`) VALUES (%s,%s,1) ON DUPLICATE KEY UPDATE count=count+1;""",
              itemSeeds)
    itemSeeds = []

    return

def FlushRandomEnchant():
    RecordRandomEnchant(None, None, None)