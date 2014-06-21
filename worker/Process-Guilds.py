#!/usr/bin/env python

import datetime
import json
import sys
import timeout
import urllib
import wf.logger
import wf.rds
import wf.schedule
import wf.util


toons = None
def IsToonKnown(region, realm, toon):
    global toons
    if not toons:
        toons = {}
    if region not in toons:
        toons[region] = {}
    if realm not in toons[region]:
#        print "! %s - %s: GetToons" % (region, realm)
        toons[region][realm] = wf.rds.GetToons(region, realm)
    if toon not in toons[region][realm]:
        # Mark the toon for later processing
#        print "! %s - %s: %s" % (region, realm, toon)
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
                    toons[region][realm][toon] = True
                if len(process_list) > 100:
                    wf.schedule.Schedule_Toons(region, realm, process_list)
                    process_list = []
            if len(process_list) > 0:
                wf.schedule.Schedule_Toons(region, realm, process_list)
    return


@timeout.timeout(30)
def GetGuild(url):
    return json.load(urllib.urlopen(url))


def ProcessGuild(zone, realm, guild):
    toons={}
    toons['new'] = 0
    toons['underage'] = 0
    toons['old'] = 0
    try:
        slug = wf.rds.Realm2Slug(zone, realm)
        url = "//%s.battle.net/api/wow/guild/%s/%s" % (zone, slug, guild)
        url = 'http:'+urllib.quote(url.encode('utf-8'))+'?fields=members'
        data = json.load(urllib.urlopen(url))
        if wf.util.IsLimitExceeded(data):
            wf.logger.logger.error("Daily limit exceeded, exiting.")
            exit(2)
        for member in data['members']:
            if member['character']['level'] < 11:
                toons['underage'] += 1
                continue
            gtoon = member['character']['name']
            trealm = member['character']['realm']
            if IsToonKnown(zone, trealm, gtoon):
                toons['old'] += 1
            else:
                toons['new'] += 1
        data["region"] = zone
        now = datetime.datetime.utcnow()
        data["lastUpdate"] = now
        wf.rds.LoadItem2Table(data, 'realmGuilds')
    except (timeout.TimeoutError, IOError):
        wf.logger.logger.exception("Continue after ProcessGuild(url=%s)" % url)
    except KeyError, e:
        wf.logger.logger.error(e.message)
    finally:
         wf.logger.logger.info("Processed guild %s|%s, New=%d, Underage=%d, Old=%d" % (guild, realm, toons['new'], toons['underage'], toons['old']))


def ProcessGuilds(zone, realm, guilds):
    wf.logger.logger.info("ProcessGuilds(%s, %s, %s)" % (zone, realm, guilds))
    for guild in guilds:
        ProcessGuild(zone, realm, unicode(guild, encoding='utf-8'))
        FlushToons()


# ["Process-Guilds.py", "US", "Uldaman", "Two Percent", "THREE D"]
# "./Process-Guilds.py" "US" "Uldaman" "Two Percent" "THREE D"

wf.rds.AnalyzeTable('realmGuilds')
try:
    zone = None
    realm = None
    guilds = None
    if len(sys.argv) > 3:
        zone = sys.argv[1]
        realm = sys.argv[2]
        guilds = sys.argv[3:]
        ProcessGuilds(zone, realm, guilds)
    else:
        wf.logger.logger.error("Not enough arguments to %s" % sys.argv[0])
except wf.util.LimitExceededError:
    wf.logger.logger.error("Daily limit exceeded, exiting.")
    wf.schedule.Schedule_Guilds(zone, realm, guilds)
    FlushToons()
    wf.util.Seppuku("Limit Exceeded")
except StandardError:
    wf.logger.logger.exception("Caught exception in %s" % sys.argv[0])
    exit(1)
