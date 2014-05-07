#!/usr/bin/env python

import json
from pprint import pprint
from types import *
import MySQLdb
import string
import exceptions
import urllib
import time
import random
import timeout
import sys
import os
import tempfile
import traceback
from urlparse import urlparse

import xml.dom.minidom 

# {u'rand': 0, u'auc': 110488118, u'timeLeft': u'VERY_LONG', u'bid': 455000, u'item': 30282, u'seed': 65752064, u'ownerRealm': u'Ravencrest', u'owner': u'Skaramoush', u'buyout': 470000, u'quantity': 1}

def IsItemKnown(id):
    return True

def RecordRandomEnchant(id,enchant_rand,enchant_seed):
    return


def IsToonKnown(realm,toon):
    return False

def QueryToon(realm,toon):
    return
    
def RecordSibling(realm_a,realm_b):
    return
    

def ScheduleNextAH():
    """Out of the AH which have not been scanned within the past 24 hours,
       select the oldest to process next and queue a query for it.
    """
    return

def FlushCachedData():
    """Write any remaining queries or database updates. """
    return
    
def ProcessAuctions(realm,faction,auctions):
    print "#Processing %s faction" % faction
    for auction in auctions:
        ownerRealm = auction['ownerRealm']
        owner = auction['owner']
        if realm != ownerRealm:
            RecordSibling(realm, ownerRealm)
        if not IsToonKnown(ownerRealm, owner):
            QueryToon(ownerRealm, owner)
        id = auction['item']
        if not IsItemKnown(id):
            QueryItem(id)
        enchant_rand = auction['rand']
        enchant_seed = auction['seed'] & 0xffff
        if enchant_rand != 0:
            RecordRandomEnchant(id,enchant_rand,enchant_seed)

_Progress=0
def GetAuctionDataProgress(blocks, blocks_size, file_size):
    global _Progress
    if file_size < 0:
        return
    so_far = (blocks * blocks_size) / (1.0 * file_size)
    if (so_far > (_Progress+0.2)):
        print "# Read %4.2f%% of the AH data" % (so_far * 100)
        _Progress = so_far

@timeout.timeout(240)
def GetAuctionData(url):
    global _Progress
    parsed_url = urlparse(url)
    guid = os.path.basename(os.path.dirname(parsed_url.path))
    tmp_name = "/tmp/%s.json" % guid
    if os.access(tmp_name,os.R_OK):
        print "# Data already retrived, loading."
        tmp = open(tmp_name, "r")
        AH = json.load(tmp)
        tmp.close()
        return AH
            
    tmp = open(tmp_name, "w+")
    print "# Redirected to %s, saving in %s" % (url,tmp_name)

    attempts = 0
    while attempts < 3:
        _Progress = 0
        try:
            info = None
            info=urllib.urlretrieve(url, filename=tmp_name, reporthook=GetAuctionDataProgress)
        except urllib.ContentTooShortError:
            print "# Truncating file"
            tmp.truncate(0)
        # Go to EOF
        tmp.seek(0,2) 
        if tmp.tell() > 1024:
            break
        attempts += 1
        if info:
            print "# Error status %s" % info[1].headers  
        tmp.seek(0,0)
        print "# File contents: %s" % tmp.readlines()
        tmp.seek(0,0)
        print "# No data found on %d attempt.  Napping and trying again." % attempts
        time.sleep(5.0)
    tmp.seek(0,0)
    if attempts >= 3:
        raise ValueError("No data at %s" % url)
    print "# Data retrived, loading"
    AH = json.load(tmp)
    return AH
     
def ScanAuctionHouse(zone,realm):   
    then = time.time()
    print "# Checking data for %s realm [%s]" % (zone,realm)
    data = json.load(urllib.urlopen(("http://%s.battle.net/api/wow/auction/data/" % zone) + realm))
    url = data['files'][0]['url']
    AH = GetAuctionData(url)

    # Process the AH data, generating new work and uopdating items along the way...
    ProcessAuctions(realm,'alliance',AH['alliance']['auctions'])
    ScheduleNextAH()
    ProcessAuctions(realm,'horde',AH['horde']['auctions'])
    ScheduleNextAH()
    ProcessAuctions(realm,'neutral',AH['neutral']['auctions'])
    ScheduleNextAH()
    FlushCachedData()

    now = time.time()
    print "# Processed data from %s realm %s in %g seconds." % (zone,realm, now-then)
        
def ScanAuctionHouses(zone,realms=None):
    global accessAH
    
    for realm in realms:
        try:
            ScanAuctionHouse(zone,realm)
            time.sleep(1.0)
        except timeout.TimeoutError:
            traceback.print_exc()
            print "# Continue after TimeoutError"
            continue
        except KeyError:
            traceback.print_exc()
            print "# Continue after KeyError"
            continue    
        except ValueError:
            traceback.print_exc()
            print "# Continue after ValueError"
            continue
        except EOFError:
            traceback.print_exc()
            print "# Break after EOFError"
            break
    
try:
    if len(sys.argv) > 2:
        ScanAuctionHouses(zone=sys.argv[1],realms=sys.argv[2:])
    else:
        ScanAuctionHouses('US')
except:
    traceback.print_exc()
    pass
       

    
