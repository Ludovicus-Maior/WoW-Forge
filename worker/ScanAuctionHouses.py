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

temporal_phase = []
def ClearTemporalPhase():
    global temporal_phase
    temporal_phase = []

def RecordTemporalPhase(ts):
    temporal_phase.append(ts.second)

def ComputeTemporalPhase():
    return float(sum(temporal_phase))/len(temporal_phase)

late_realms = 0
def ScanAuctionHouse(zone, realm, lastScanned):
    global late_realms
    realm_date = wf.bnet.iso_date(lastScanned)
    utc_now = datetime.datetime.utcnow()
    how_stale = (utc_now-realm_date).total_seconds()
    if how_stale < (60*60):
        # wf.logger.logger.info("ScanAuctionHouse(%s,%s): Too soon to check (%s)" % (zone, realm, lastScanned))
        return None
    if how_stale > (5*60*60):
        wf.logger.logger.error("ScanAuctionHouse(%s,%s): Realm is RANCID (%s)" % (zone, realm, lastScanned))
        late_realms +=1
    elif how_stale > (3*60*60):
        wf.logger.logger.warning("ScanAuctionHouse(%s,%s): Realm is STALE (%s)" % (zone, realm, lastScanned))
        late_realms +=1
    elif how_stale > (1.5*60*60):
        wf.logger.logger.info("ScanAuctionHouse(%s,%s): Realm is LATE (%s)" % (zone, realm, lastScanned))
        late_realms +=1
    then = time.time()
    result = wf.bnet.get_auctions(zone, realm, lastScanned)
    if result:
        # Save the data away in S3.
        wf.s3.save_ah_file(result[0], zone, realm, result[1])
    now = time.time()
    wf.logger.logger.info("Processed data from %s realm %s in %g seconds." % (zone, realm, now - then))
    return result


def ScanAuctionHouses(zone):
    global late_realms
    while True:
        then = time.time()
        realms = wf.rds.SelectRegionRealms(zone)
        wf.logger.logger.info("*"*80)
        wf.logger.logger.info("ScanAuctionHouses(%s) %d realms to scan" % (zone, len(realms)))
        ClearTemporalPhase()
        late_realms = 0
        for realm in realms:
            if not ScanAuctionHouse(zone, realm, realms[realm]):
                RecordTemporalPhase(wf.bnet.iso_date(realms[realm]))
        if len(realms) == late_realms:
            # If everyone is late, either it is maintenance or something is wrong.
            # Do a slow scan until something succeeds
            wf.logger.logger.warning("ScanAuctionHouses() %d realms LATE.  Going into slow scan mode" % late_realms)
            for realm in realms:
                if ScanAuctionHouse(zone, realm, realms[realm]):
                    break
                time.sleep(30)
        now = time.time()
        wf.logger.logger.info("ScanAuctionHouses() Scan complete in %g seconds." % (now - then))
        now = datetime.datetime.utcnow()
        tp = ComputeTemporalPhase()
        ns = (now.second + now.microsecond/1e6)
        wf.logger.logger.debug("ScanAuctionHouses() TP=%f NS=%f" % (tp, ns))
        nap_time = (tp + 4 - ns) % 60
        wf.logger.logger.info("ScanAuctionHouses() Enforced nap of %f seconds" % nap_time)
        time.sleep(nap_time)
        wf.logger.logger.info("!"*80)

try:
    ScanAuctionHouses("US")
except:
    wf.logger.logger.exception("Exception while calling ScanAuctionHouses()")
    exit(1)
       

    
