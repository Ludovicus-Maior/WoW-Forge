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


guilds = None
def IsGuildKnown(region, realm, guild):
    global guilds
    if not guilds:
        guilds = {}
    if region not in guilds:
        guilds[region] = {}
    if realm not in guilds[region]:
        guilds[region][realm] = wf.rds.GetGuilds(region, realm)
    if guild not in guilds[region][realm]:
        # Mark the guild for later processing
        guilds[region][realm][guild] = False
        return False
    return True

def FlushGuilds():
    global guilds
    if not guilds:
        return
    for region in guilds:
        for realm in guilds[region]:
            process_list = []
            for guild in guilds[region][realm]:
                if not guilds[region][realm][guild]:
                    process_list.append(guild)
                if len(process_list) > 100:
                    wf.schedule.Schedule_Guilds(region, realm, process_list)
                    process_list = []
            if len(process_list) > 0:
                wf.schedule.Schedule_Guilds(region, realm, process_list)
    return


@timeout.timeout(30)
def GetToon(url):
    return json.load(urllib.urlopen(url))

old_guilds = 0
new_guilds = 0
toons_loaded = 0
race2side = { 1:0, 5:1, 11:0, 7:0, 8:1 , 2: 1, 3:0, 4:0, 10:1, 22:0, 6:1, 24:2, 25:0, 26:1, 9:1 }

def ProcessToon(zone, realm, toon):
    global old_guilds
    global new_guilds
    global toons_loaded
    try:
        slug = wf.rds.Realm2Slug(zone, realm)
        url = "//%s.battle.net/api/wow/character/%s/%s" % (zone, slug, toon)
        url = 'http:'+urllib.quote(url.encode('utf-8'))+'?fields=guild,items,talents'
        data = GetToon(url)
        wf.util.IsLimitExceeded(data)
        if not 'items' in data:
            raise KeyError("Unable to locate toon [%s] in %s/%s" % (toon, realm, zone))
        for slot in data['items']:
            if type(data['items'][slot]) is dict:
                if "id" in data['items'][slot]:
                    data[slot+"_id"] = data['items'][slot]["id"]
                if "enchant" in data['items'][slot]["tooltipParams"]:
                    data[slot+"_enchant"] = data['items'][slot]["tooltipParams"]["enchant"]
                if "suffix" in data['items'][slot]["tooltipParams"]:
                    data[slot+"_suffix"] = data['items'][slot]["tooltipParams"]["suffix"]
                if "seed" in data['items'][slot]["tooltipParams"]:
                    data[slot+"_seed"] = data['items'][slot]["tooltipParams"]["seed"]
                if "suffix" in data['items'][slot]["tooltipParams"] and "seed" in data['items'][slot]["tooltipParams"]:
                    wf.rds.RecordRandomEnchant(data[slot+"_id"], data[slot+"_suffix"],  data[slot+"_seed"])
        if "guild" in data:
            data["guildRealm"] = data["guild"]["realm"]
            if IsGuildKnown(zone, realm, data["guild"]["name"]):
                old_guilds += 1
            else:
                now = datetime.datetime.utcnow()
                data["guild"]["lastUpdate"] = now
                data["guild"]["region"] = zone
                data["guild"]["side"] = race2side[data['race']]
                wf.rds.LoadItem2Table(data["guild"], 'realmGuilds')
                new_guilds += 1
            data["guild"] = data["guild"]["name"]
        if ("talents" in data) and (len(data["talents"]) > 0) and ("spec" in data["talents"][0]):
            data["specName"] = data["talents"][0]["spec"]["name"]
        data["region"] = zone
        now = datetime.datetime.utcnow()
        data["lastUpdate"] = now
        wf.rds.LoadItem2Table(data, 'realmCharacter')
        toons_loaded += 1
    except (timeout.TimeoutError, IOError):
        wf.logger.logger.exception("Continue after ProcessToon(url=%s)" % url)
    except KeyError, e:
        wf.logger.logger.warning(e.message)



def ProcessToons(zone, realm, toons):
    global old_guilds
    global new_guilds
    global toons_loaded
    wf.logger.logger.info("ProcessToons(%s, %s, %s)" % (zone, realm, toons))
    for toon in toons:
        ProcessToon(zone, realm, unicode(toon, encoding='utf-8'))
    wf.logger.logger.info("Toons listed:%d, loaded:%d" % (len(toons), toons_loaded))
    wf.logger.logger.info("Guilds new:%d, old:%d" % (new_guilds, old_guilds))
    wf.rds.FlushRandomEnchant()
    FlushGuilds()


# ["Process-Toons.py", "US", "Uldaman", "Drollete", "Adelphus", "Impairment", "Tupperware", "Sabina", "Arandrie", "Soconfused", "Merryjayne", "Jenkillsguys", "Dyia", "Pennyroyal"
# Process-Toons.py US Uldaman  "Drollete" "Adelphus" "Impairment" "Tupperware" "Sabina" "Arandrie" "Soconfused" "Merryjayne" "Jenkillsguys" "Nojta" "

wf.rds.AnalyzeTable('realmCharacter')
wf.rds.AnalyzeTable('realmGuilds')
try:
    zone = None
    realm = None
    toons = None
    if len(sys.argv) > 3:
        zone = sys.argv[1]
        realm = sys.argv[2]
        toons = sys.argv[3:]
        ProcessToons(zone, realm, toons)
    else:
        wf.logger.logger.error("Not enough arguments to %s" % sys.argv[0])
except wf.util.LimitExceededError:
    wf.logger.logger.error("Daily limit exceeded, exiting.")
    wf.schedule.Schedule_Toons(zone, realm, toons)
    FlushGuilds()
    wf.util.Seppuku("Limit Exceeded")
except StandardError:
    wf.logger.logger.exception("Caught exception in %s" % sys.argv[0])
    exit(1)
