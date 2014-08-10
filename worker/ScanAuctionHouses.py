#!/usr/bin/env python

import time
import sys
import wf.bnet
import wf.logger
import wf.rds
import wf.schedule
import wf.s3
import wf.util



def ScanAuctionHouse(zone, realm, lastScanned):
    then = time.time()
    result = wf.bnet.get_auctions(zone, realm, lastScanned)
    if result:
        # Save the data away in S3.
        wf.s3.save_ah_file(result[0], zone, realm, result[1])
    now = time.time()
    wf.logger.logger.info("Processed data from %s realm %s in %g seconds." % (zone, realm, now - then))
    return result


def ScanAuctionHouses(zone, realms=None):
    while True:
        wf.logger.logger.info("ScanAuctionHouses(%s, %s)" % (zone, realms))
        if realms is None:
            realms = wf.rds.SelectRegionRealms(zone)
        realms_notupdated = len(realms)
        for realm in realms:
            if not ScanAuctionHouse(zone, realm, realms[realm]):
                realms_notupdated -= 1
            time.sleep(1.0)
        wf.logger.logger.info("ScanAuctionHouses() Scan complete. %d realms not updated. Napping till the next run" % realms_notupdated)
        time.sleep(1.0 * realms_notupdated)



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
       

    
