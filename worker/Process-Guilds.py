#!/usr/bin/env python

import json
import sys
import timeout
import urllib
import wf.logger
import wf.rds
import wf.schedule


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
                if len(process_list) > 100:
                    wf.schedule.Schedule_Toons(region, realm, process_list)
                    process_list = []
            if len(process_list) > 0:
                wf.schedule.Schedule_Toons(region, realm, process_list)
    return


@timeout.timeout(24)
def GetGuild(url):
    return json.load(urllib.urlopen(url))


def ProcessGuild(zone, realm, guild):
    try:
        slug = wf.rds.Realm2Slug(zone, realm)
        url = "//%s.battle.net/api/wow/guild/%s/%s" % (zone, slug, guild)
        url = 'http:'+urllib.quote(url.encode('utf-8'))+'?fields=members'
        data = json.load(urllib.urlopen(url))
        for member in data['members']:
            if member['character']['level'] < 11:
                continue
            gtoon = member['character']['name']
            trealm = member['character']['realm']
            IsToonKnown(zone, trealm, gtoon)
        data["region"] = zone
        wf.rds.LoadItem2Table(data, 'realmGuilds')
    except (timeout.TimeoutError, IOError):
        wf.logger.logger.exception("Continue after ProcessGuild(url=%s)" % url)
    except KeyError, e:
        wf.logger.logger.warning(e.message)



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
except StandardError:
    wf.logger.logger.exception("Caught exception in %s" % sys.argv[0])
    exit(1)