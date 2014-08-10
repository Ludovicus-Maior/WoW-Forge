#!/usr/bin/env python


import MySQLdb
import fuzzy
import os
import datetime
import string
import wf.logger
import _mysql_exceptions

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

    database = MySQLdb.connect(user=db_user, passwd=db_pass, host=db_host, db="Warcraft", charset='utf8', use_unicode=True)
    database.autocommit(auto_commit)

TableFields = {}
def AnalyzeTable(table):
    global database
    global TableFields
    if not database:
        ConnectDatabase(True)
    wf.logger.logger.info("Analyzing table %s" % table)
    TableFields[table] = {}
    c = database.cursor()
    c.execute("""SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS`
                     WHERE `TABLE_SCHEMA`='Warcraft' and `table_name` = %s ;""", (table,))
    d = c.fetchone()
    while d:
        column = d[0]
        TableFields[table][column] = True
        d = c.fetchone()
    c.close()


ItemFieldsWritten = {}
def LoadItem2Table(Item, table):
    global ItemFieldsWritten
    global TableFields
    global database
    c = database.cursor()
    cmd = "REPLACE INTO `Warcraft`.`%s` (" % table

    if not table in TableFields:
        raise KeyError("Hey!  Someone forgot to Analyze table %s" % table)

    tfs = set(TableFields[table])
    ifs = set(Item)
    tks = list(tfs & ifs)
    tks.sort()
    item = {k: Item[k] for k in tks}

    cmd = cmd + string.join(tks, ',') + " ) VALUES ("
    v = []
    for tk in tks:
        v.append('%('+tk+')s')
        ItemFieldsWritten[tk] = True

    cmd = cmd + string.join(v, ',') + ") ;"

    try:
        c.execute(cmd, item)
    except _mysql_exceptions.MySQLError:
        wf.logger.logger.exception("LoadItem2Table Exception with Table %s, Items %s" % (table, item))
        raise
    finally:
        c.close()



def SelectStaleRealm(region):
    global database
    if not database:
        ConnectDatabase(True)

    c = database.cursor()
    c.execute("""SELECT `name` FROM `realmStatus` WHERE `region` = %s AND `enqueueTime` IS NULL ORDER BY `lastAuctionScan` LIMIT 1;""" ,
              (region,))
    d = c.fetchone()
    if d is None:
        return None
    realm = d[0]
    now = datetime.datetime.utcnow()
    c.execute("""UPDATE `realmStatus` SET `enqueueTime` = %s WHERE `enqueueTime` IS NULL and `name` = %s and  `region` = %s;""",
              (now.isoformat(' '), realm, region))
    c.close()
    return realm

def SelectRegionRealms(region):
    global database
    if not database:
        ConnectDatabase(True)

    c = database.cursor()
    c.execute("""SELECT `name`, `lastAuctionScan` FROM `realmStatus` WHERE `region` = %s ORDER BY `lastAuctionScan`;""" ,
              (region,))
    d = c.fetchone()
    realms_ts = {}
    realms = list()
    while d is not None:
        realms_ts[d[0]] = d[1]
        realms.append(d[0])
        d = c.fetchone()
    c.close()
    return realms_ts


def FinishedRealm(region, realm, lastModified):
    global database
    if not database:
        ConnectDatabase(True)

    now = datetime.datetime.utcnow()
    c = database.cursor()
    rows_done = c.execute("""UPDATE `realmStatus` SET `enqueueTime` = NULL,  `lastAuctionScan` = %s WHERE `name` = %s and  `region` = %s;""",
              (lastModified, realm, region))
    if rows_done != 1:
        wf.logger.logger.warning("FinishedRealm(%s,%s): failed to update realm." % (region, realm))
    else:
        wf.logger.logger.info("FinishedRealm(%s,%s): updated realm on %s." % (region, realm, lastModified))
    c.close()
    return realm


def ResetRealms():
    global database
    if not database:
        ConnectDatabase(True)

    c = database.cursor()
    c.execute("""UPDATE `realmStatus` SET `enqueueTime` = NULL;""")
    c.close()


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
    c.close()
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
    c.close()

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
#        print "# %s - %s: %s" % (region, realm, d[0])
        d = c.fetchone()
    c.close()
    return h


def GetGuilds(region, realm):
    global database
    if not database:
        ConnectDatabase(True)

    c = database.cursor()
    c.execute('SELECT `name`, `lastUpdate` FROM `realmGuilds` WHERE `region` = %s AND `realm` = %s ;',
              (region, realm))

    d = c.fetchone()
    h = {}
    while d is not None:
        h[d[0]] = d[1]
        d = c.fetchone()
    c.close()
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
    c.close()
    return

def FlushRandomEnchant():
    RecordRandomEnchant(None, None, None)


def ToonExists(region, realm, toon):
    c = database.cursor()
    cmd = "SELECT EXISTS(SELECT 1 FROM realmCharacter WHERE `region` = '%s' and `realm` = '%s' and `name` = '%s' );" % (region, realm, toon)
    c.execute(cmd)
    d = c.fetchone()
    value = d[0]
    c.close()
    return value != 0


def LookupRegionSlugs(region):
    global database
    if not database:
        ConnectDatabase(True)

    c = database.cursor()
    c.execute("""SELECT `name`, `slug` FROM `realmStatus` WHERE `region` = %s;""" ,
              (region,))
    d = c.fetchone()
    h = {}

    while d is not None:
        h[d[0]] = d[1]
        h[fuzzy.nysiis(d[0])] = d[1]
        d = c.fetchone()
    c.close()
    return h



realm2slug={}
def Realm2Slug(region, realm):
    global realm2slug
    if not region in realm2slug:
        realm2slug[region] = LookupRegionSlugs(region)
    if not realm in realm2slug[region]:
        # Lets see if we can find an alias for it
        realm = fuzzy.nysiis(realm)
    return realm2slug[region].get(realm)
