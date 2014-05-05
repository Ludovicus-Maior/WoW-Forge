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
import tempfile
import rotate
import traceback

import xml.dom.minidom 


#  wget http://www.wowhead.com/item=51964&xml
# <?xml version="1.0" encoding="UTF-8"?><wowhead>
#  <item id="51964"><name><![CDATA[Vigorous Belt]]></name><level>25</level><quality id="3">Rare</quality>
#  <class id="4"><![CDATA[Armor]]></class><subclass id="2"><![CDATA[Leather Armor]]></subclass><icon displayId="49925">INV_Belt_03</icon>
#  <inventorySlot id="6">Waist</inventorySlot>
#  <randomEnchantments>
#   <randomEnchantment id="71"><![CDATA[of the Bandit]]></randomEnchantment>
#   <randomEnchantment id="78"><![CDATA[of the Monkey]]></randomEnchantment>
#   <randomEnchantment id="79"><![CDATA[of the Moon]]></randomEnchantment>
#   <randomEnchantment id="80"><![CDATA[of the Wild]]></randomEnchantment>
#   <randomEnchantment id="82"><![CDATA[of the Vision]]></randomEnchantment>
#  </randomEnchantments>
#  <htmlTooltip><![CDATA[<table><tr><td><b class="q3">Vigorous Belt</b><span style="color: #ffd100"><br />Item Level 25</span><br /><!--bo-->Binds when picked up<table width="100%"><tr><td>Waist</td><th>Leather</th></tr></table><!--rf--><span>65 Armor</span><br /><!--re--><span class="q2">&lt;Random enchantment&gt;</span><!--rs--><!--e--><!--ps--><br />Durability 40 / 40</td></tr></table><table><tr><td><!--rr--><div class="whtt-sellprice">Sell Price: <span class="moneysilver">8</span> <span class="moneycopper">46</span></div></td></tr></table>]]></htmlTooltip><json><![CDATA["armor":65,"classs":4,"displayid":49925,"id":51964,"level":25,"name":"4Vigorous Belt","slot":6,"slotbak":6,"source":[2],"sourcemore":[{"icon":"inv_misc_bag_15","n":"Satchel of Helpful Goods","q":3,"t":3,"ti":51999}],"subclass":2]]></json><jsonEquip><![CDATA["armor":65,"displayid":49925,"dura":40,"sellprice":846,"slotbak":6]]></jsonEquip><link>http://www.wowhead.com/item=51964</link></item></wowhead>

randomEnchantItems = {}

def LoadCache(file):
    print "Reading Data from: "+file
    json_file=open(file,"r")
    data = json.load(json_file)
    json_file.close()
    return data

def SaveCache(data,file):
    print "Writing Data to: "+file
    rotate.rotate(file)
    json_file=open(file,"w+")
    json.dump(data,json_file,indent=1,sort_keys=True)
    json_file.close()    
  
@timeout.timeout(8)
def GetToon(url):
    return json.load(urllib.urlopen(url))
    
def ProcessToon(realm,toon):
    global realmInfo
    
    try:
        url = '//us.battle.net/api/wow/character/'+realm+'/'+toon
        url = 'http:'+urllib.quote(url.encode('utf-8'))+'?fields=guild'
        data = GetToon(url)
        # check for lone rangers
        if not ('guild' in data):
            return
        gname = data['guild']['name']
        if not (gname in realmInfo['guilds']):
            realmInfo['guilds'][gname] = 0
    except (timeout.TimeoutError, IOError):
        traceback.print_exc()
        print "# Continue after ProcessToon(url=%s)" % url
        pass
    
def ProcessAuctions(realm,faction,auctions):
    global randomEnchantItems
    global realmInfo
    print "#Processing %s faction" % faction
    added = 0
    new = 0
    toons = 0 
    for auction in auctions:
        if not (auction['owner'] in realmInfo['toons']):
            ProcessToon(realm, auction['owner'])
            realmInfo['toons'][auction['owner']] = 0
            toons += 1
        if auction['rand'] != 0:
            # We have a RE item
            id = str(auction['item'])
            RAND = str(auction['rand'])
            seed = str(auction['seed'] & 0xffff)
            if not id in randomEnchantItems:
                randomEnchantItems[id] = {}
                randomEnchantItems[id]['seed'] = {}
                new += 1   
            if RAND in randomEnchantItems[id]:
                randomEnchantItems[id][RAND] += 1
            else:
                randomEnchantItems[id][RAND] = 1
                added +=1 
            if seed in randomEnchantItems[id]['seed']:
                randomEnchantItems[id]['seed'][seed] += 1
            else:
                randomEnchantItems[id]['seed'][seed] = 1
#                pprint(auction)
                added += 1
#            print "# Item %s rand %s seed %s" % (id, RAND, seed)
    print "# New items %d, augmented %d, toons %d" %(new, added, toons)

_Progress=0
def GetAuctionDataProgress(blocks, blocks_size, file_size):
    global _Progress
    if file_size < 0:
        return
    so_far = (blocks * blocks_size) / (1.0 * file_size)
    if (so_far > (_Progress+0.2)):
        print "# Read %4.2f of the AH data" % (so_far * 100)
        _Progress = so_far

@timeout.timeout(240)
def GetAuctionData(url):
    global _Progress
    tmp=tempfile.NamedTemporaryFile(suffix='.json', prefix='auctions',dir='/tmp')
    print "# Redirected to %s, saving in %s" % (url,tmp.name)

    attempts = 0
    while attempts < 3:
        _Progress = 0
        try:
            info = None
            info=urllib.urlretrieve(url, filename=tmp.name, reporthook=GetAuctionDataProgress)
        except urllib.ContentTooShortError:
            print "# Truncating file"
            tmp.truncate(0)
        tmp.seek(0,2) # Go to EOF
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
        ScanAuctionHouses(zone=sys.argv[1],realms=sys.argv[1:])
    else:
        ScanAuctionHouses('US')
except:
    traceback.print_exc()
    pass
       

    
