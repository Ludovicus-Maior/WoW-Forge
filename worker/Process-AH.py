#!/usr/bin/env python

import json
import urllib
import time
import timeout
import sys
import os
from urlparse import urlparse
import wf.logger
import wf.rds
import wf.schedule

# {u'rand': 0, u'auc': 110488118, u'timeLeft': u'VERY_LONG', u'bid': 455000, u'item': 30282, u'seed': 65752064,
# u'ownerRealm': u'Ravencrest', u'owner': u'Skaramoush', u'buyout': 470000, u'quantity': 1}

def IsItemKnown(id):
    return True


toons = None


def IsToonKnown(region, realm, toon):
    global toons
    if not toons:
        toons = {}
    if region not in toons:
        toons[region] = {}
    if realm not in toons[region]:
        toons[region][realm] = wf.rds.GetToons(region, realm)
    if toon not in toons[region][realm]:
        # Mark the toon for later processing
        toons[region][realm][toon] = False
        return False
    return True


def FlushToons():
    global toons
    if not toons:
        return
    for region in toons:
        for realm in toons[region]:
            process_list = []
            for toon in toons[region][realm]:
                if not toons[region][realm][toon]:
                    process_list.append(toon)
                if len(process_list) > 100:
                    wf.schedule.Schedule_Toons(region, realm, process_list)
                    process_list = []
            if len(process_list) > 0:
                wf.schedule.Schedule_Toons(region, realm, process_list)
    return


siblings = None


def RecordSibling(region, realm_main, realm_aux):
    global siblings
    if not siblings:
        siblings = wf.rds.GetSiblings(region, realm_main)
    if realm_aux not in siblings:
        wf.logger.logger.info("Discovered sibling [%s] to [%s]" % (realm_aux, realm_main))
        wf.rds.AddSibling(region, realm_main, realm_aux)
        siblings.add(realm_aux)
    return


def ProcessAuctions(region, realm, faction, auctions):
    wf.logger.logger.info("Processing %s faction" % faction)
    for auction in auctions:
        ownerRealm = auction['ownerRealm']
        owner = auction['owner']
        if owner == "???" or ownerRealm == "???":
            continue
        if realm != ownerRealm:
            RecordSibling(region, realm, ownerRealm)
        IsToonKnown(region, ownerRealm, owner)

        id = auction['item']
        if not IsItemKnown(id):
            QueryItem(id)
        enchant_rand = auction['rand']
        enchant_seed = auction['seed'] & 0xffff
        if enchant_rand != 0:
            wf.rds.RecordRandomEnchant(id, enchant_rand, enchant_seed)
    FlushToons()
    wf.rds.FlushRandomEnchant()


_Progress = 0


def GetAuctionDataProgress(blocks, blocks_size, file_size):
    global _Progress
    if file_size < 0:
        return
    so_far = (blocks * blocks_size) / (1.0 * file_size)
    if (so_far > (_Progress + 0.2)):
        wf.logger.logger.info("Read %4.2f%% of the AH data" % (so_far * 100))
        _Progress = so_far


@timeout.timeout(240)
def GetAuctionData(url):
    global _Progress
    parsed_url = urlparse(url)
    guid = os.path.basename(os.path.dirname(parsed_url.path))
    tmp_name = "/tmp/%s.json" % guid
    if os.access(tmp_name, os.R_OK):
        wf.logger.logger.warning("Data already retrieved, loading.")
        tmp = open(tmp_name, "r")
        AH = json.load(tmp)
        tmp.close()
        return AH

    tmp = open(tmp_name, "w+")
    wf.logger.logger.info("Redirected to %s, saving in %s" % (url, tmp_name))

    attempts = 0
    while attempts < 3:
        _Progress = 0
        try:
            info = None
            info = urllib.urlretrieve(url, filename=tmp_name, reporthook=GetAuctionDataProgress)
        except urllib.ContentTooShortError:
            wf.logger.logger.warning("Truncating file")
            tmp.truncate(0)
        # Go to EOF
        tmp.seek(0, 2)
        if tmp.tell() > 1024:
            break
        attempts += 1
        if info:
            wf.logger.logger.error("Error status %s" % info[1].headers)
        tmp.seek(0, 0)
        wf.logger.logger.info("File contents: %s" % tmp.readlines())
        tmp.seek(0, 0)
        wf.logger.logger.warning("No data found on %d attempt.  Napping and trying again." % attempts)
        time.sleep(5.0)
    tmp.seek(0, 0)
    if attempts >= 3:
        raise ValueError("No data at %s" % url)
    wf.logger.logger.info("Data retrived, loading")
    AH = json.load(tmp)
    os.remove(tmp_name)
    return AH


def ScanAuctionHouse(zone, realm):
    then = time.time()
    wf.logger.logger.info("Checking data for %s realm [%s]" % (zone, realm))
    slug = wf.rds.Realm2Slug(zone, realm)
    data = json.load(urllib.urlopen(("http://%s.battle.net/api/wow/auction/data/%s" % (zone, slug))))
    url = data['files'][0]['url']
    AH = GetAuctionData(url)

    # Process the AH data, generating new work and updating items along the way...
    ProcessAuctions(zone, realm, 'alliance', AH['alliance']['auctions'])
    wf.schedule.Schedule_AH(zone, None)
    ProcessAuctions(zone, realm, 'horde', AH['horde']['auctions'])
    wf.schedule.Schedule_AH(zone, None)
    ProcessAuctions(zone, realm, 'neutral', AH['neutral']['auctions'])
    wf.schedule.Schedule_AH(zone, None)
    wf.rds.FinishedRealm(zone, realm)
    now = time.time()
    wf.logger.logger.info("Processed data from %s realm %s in %g seconds." % (zone, realm, now - then))


def ScanAuctionHouses(zone, realms=None):
    wf.logger.logger.info("ScanAuctionHouses(%s, %s)" % (zone, realms))
    for realm in realms:
        try:
            ScanAuctionHouse(zone, realm)
            time.sleep(1.0)
        except timeout.TimeoutError:
            wf.logger.logger.exception("Continue after TimeoutError")
            continue
        except KeyError:
            wf.logger.logger.exception("Continue after KeyError")
            continue
        except ValueError:
            wf.logger.logger.exception("Continue after ValueError")
            continue
        except EOFError:
            wf.logger.logger.exception("Break after EOFError")
            break


try:
    zone = None
    realms = None
    if len(sys.argv) > 2:
        zone = sys.argv[1]
        realms = sys.argv[2:]
        ScanAuctionHouses(zone=zone, realms=realms)
    else:
        zone = 'US'
        ScanAuctionHouses(zone)
except:
    wf.logger.logger.exception("Exception while calling ScanAuctionHouses(%s,%s)" % (zone, realms))
    exit(1)
       

    
