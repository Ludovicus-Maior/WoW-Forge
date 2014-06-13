#!/usr/bin/env python

import json
import sys
import timeout
import urllib
import wf.logger
import wf.rds
import wf.schedule


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


@timeout.timeout(16)
def GetToon(url):
    return json.load(urllib.urlopen(url))


def ProcessToon(zone, realm, toon):
    try:
        slug = wf.rds.Realm2Slug(zone, realm)
        url = "//%s.battle.net/api/wow/character/%s/%s" % (zone, slug, toon)
        url = 'http:'+urllib.quote(url.encode('utf-8'))+'?fields=guild,items,talents'
        data = GetToon(url)
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
            data["guild"] = data["guild"]["name"]
            IsGuildKnown(zone, realm, data["guild"])
        if ("talents" in data) and (len(data["talents"]) > 0) and ("spec" in data["talents"][0]):
            data["specName"] = data["talents"][0]["spec"]["name"]
        data["region"] = zone
        wf.rds.LoadItem2Table(data, 'realmCharacter')
    except (timeout.TimeoutError, IOError):
        wf.logger.logger.exception("Continue after ProcessToon(url=%s)" % url)
    except KeyError, e:
        wf.logger.logger.warning(e.message)



def ProcessToons(zone, realm, toons):
    wf.logger.logger.info("ProcessToons(%s, %s, %s)" % (zone, realm, toons))
    for toon in toons:
        ProcessToon(zone, realm, unicode(toon, encoding='utf-8'))
    wf.rds.FlushRandomEnchant()
    FlushGuilds()


# ["Process-Toons.py", "US", "Uldaman", "Drollete", "Adelphus", "Impairment", "Tupperware", "Sabina", "Arandrie", "Soconfused", "Merryjayne", "Jenkillsguys", "Dyia", "Pennyroyal"
# Process-Toons.py US Uldaman  "Drollete" "Adelphus" "Impairment" "Tupperware" "Sabina" "Arandrie" "Soconfused" "Merryjayne" "Jenkillsguys" "Nojta" "

wf.rds.AnalyzeTable('realmCharacter')
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
except StandardError:
    wf.logger.logger.exception("Caught exception in %s" % sys.argv[0])
    exit(1)