#!/usr/bin/env python

import httplib
import json
import urllib2
import time
import timeout
import sys
import os
from urlparse import urlparse
import wf.logger
import wf.rds
import wf.schedule
import wf.util

# {u'rand': 0, u'auc': 110488118, u'timeLeft': u'VERY_LONG', u'bid': 455000, u'item': 30282, u'seed': 65752064,
# u'ownerRealm': u'Ravencrest', u'owner': u'Skaramoush', u'buyout': 470000, u'quantity': 1}

httplib.HTTPConnection.debuglevel = 1

class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):
    def http_error_default(self, req, fp, code, msg, headers):
        result = urllib2.HTTPError(
            req.get_full_url(), code, msg, headers, fp)
        result.status = code
        return result

def ProcessAuctions(region, slug, auctions_file):
    # copy to S3 bucket


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
    return tmp_name


def ScanAuctionHouse(zone, realm, lastScanned):
    then = time.time()
    wf.logger.logger.info("Checking data for %s realm [%s]" % (zone, realm))
    slug = wf.rds.Realm2Slug(zone, realm)
    request = urllib2.request("http://%s.battle.net/api/wow/auction/data/%s" % (zone, slug))
    request.add_header("User-Agent", "WoW-Forge/1.0")
    request.add_header('Accept-encoding', 'gzip')
    if lastScanned:
        request.add_header("If-Modified-Since", lastScanned)
    opener = urllib2.build_opener(DefaultErrorHandler())
    data_stream = opener.open(request)
    if data_stream.status == 304:
        # No new data
        wf.logger.logger.info("No new data from %s realm %s since %s." % (zone, realm, lastScanned))
        wf.rds.FinishedRealm(zone, realm, lastScanned)

    if data_stream.status == 500:
        data = json.load(data_stream)
        wf.util.IsLimitExceeded(data)
        return

    if data_stream.status != 200:
        raise data_stream.result

    data = json.load(data_stream)
    url = data['files'][0]['url']
    lm = data['files'][0]['lastModified']
    ah_file = GetAuctionData(url)

    # Save the data away in S3.
    ProcessAuctionFile(zone, slug, ah_file, lm)
    wf.rds.FinishedRealm(zone, realm, lm)
    now = time.time()
    wf.logger.logger.info("Processed data from %s realm %s in %g seconds." % (zone, realm, now - then))


def ScanAuctionHouses(zone, realms=None):
    wf.logger.logger.info("ScanAuctionHouses(%s, %s)" % (zone, realms))
    if realms is None:
        realms = wf.rds.SelectStaleRealms(zone)
    for realm in realms:
        try:
            ScanAuctionHouse(zone, realm, realms[realm])
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
        realms = {}
        for realm in sys.argv[2:]:
            realms[realm] = 0
        ScanAuctionHouses(zone=zone, realms=realms)
    else:
        zone = 'US'
        ScanAuctionHouses(zone)
except wf.util.LimitExceededError:
    wf.logger.logger.error("Daily limit exceeded, exiting.")
    wf.schedule.Schedule_AH(zone, realms)
    wf.util.Seppuku("Limit Exceeded")
except:
    wf.logger.logger.exception("Exception while calling ScanAuctionHouses(%s,%s)" % (zone, realms))
    exit(1)
       

    
