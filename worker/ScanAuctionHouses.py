#!/usr/bin/env python

import datetime
import time
import sys
import wf.bnet
import wf.logger
import wf.rds
import wf.schedule
import wf.s3
import wf.util

NO_UPDATE_NAP = 20

def ScanAuctionHouse(zone, realm, lastScanned):
    realm_date = wf.bnet.iso_date(lastScanned)
    utc_now = datetime.datetime.utcnow()
    if (utc_now-realm_date).total_seconds() < (58*60):
        wf.logger.logger.info("ScanAuctionHouse(%s,%s): Too soon to check (%s)" % (zone, realm, lastScanned))
        return None
    then = time.time()
    result = wf.bnet.get_auctions(zone, realm, lastScanned)
    if result:
        # Save the data away in S3.
        wf.s3.save_ah_file(result[0], zone, realm, result[1])
    now = time.time()
    wf.logger.logger.info("Processed data from %s realm %s in %g seconds." % (zone, realm, now - then))
    return result


def ScanAuctionHouses(zone):
    global NO_UPDATE_NAP
    while True:
        then = time.time()
        realms = wf.rds.SelectRegionRealms(zone)
        wf.logger.logger.info("!"*80)
        wf.logger.logger.info("ScanAuctionHouses(%s) %d realms to scan" % (zone, len(realms)))
        oldest_realm_date = None
        someone_updated = False
        for realm in realms:
            if not ScanAuctionHouse(zone, realm, realms[realm]):
                realm_date = wf.bnet.iso_date(realms[realm])
                if oldest_realm_date is None or realm_date < oldest_realm_date:
                    oldest_realm_date = realm_date
            else:
                someone_updated = True
        now = time.time()
        wf.logger.logger.info("ScanAuctionHouses() Scan complete in %g seconds." % (now - then))
        if not someone_updated:
            wf.logger.logger.info("ScanAuctionHouses() No updates occurred.  Enforced nap of %d seconds" % NO_UPDATE_NAP)
            time.sleep(NO_UPDATE_NAP)
        utc_now = datetime.datetime.utcnow()
        # Let us poll starting at 2 minutes till the hour
        oldest_realm_date = oldest_realm_date + datetime.timedelta(minutes=59)
        nap_delta = (oldest_realm_date - utc_now).total_seconds()
        if nap_delta > 0:
            wf.logger.logger.info("ScanAuctionHouses() Napping till %s" % oldest_realm_date)
            time.sleep(nap_delta)
        else:
            wf.logger.logger.info("ScanAuctionHouses() No rest for the wicked.  %s is too close." % oldest_realm_date)
        wf.logger.logger.info("!"*80)

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
except:
    wf.logger.logger.exception("Exception while calling ScanAuctionHouses(%s,%s)" % (zone, realms))
    exit(1)
       

    
