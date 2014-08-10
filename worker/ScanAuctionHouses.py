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


def ScanAuctionHouses(zone, realms=None):
    wf.logger.logger.info("ScanAuctionHouses(%s, %s)" % (zone, realms))
    if realms is None:
        realms = wf.rds.SelectStaleRealms(zone)
    for realm in realms:
        ScanAuctionHouse(zone, realm, realms[realm])
        time.sleep(1.0)



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
       

    
