#!/usr/bin/env python

import json
import sys
import timeout
import urllib
import wf.logger




@timeout.timeout(8)
def GetToon(url):
    return json.load(urllib.urlopen(url))



def ProcessToon(zone, realm, toon):
    try:
        url = "//%s.battle.net/api/wow/character/%s/%s" % (zone, realm, toon)
        url = 'http:'+urllib.quote(url.encode('utf-8'))+'?fields=guild'
        data = GetToon(url)
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
        if "guild" in data:
            data["guildRealm"] = data["guild"]["realm"]
            data["guild"] = data["guild"]["name"]
        if ("talents" in data) and (len(data["talents"]) > 0) and ("spec" in data["talents"][0]):
            data["specName"] = data["talents"][0]["spec"]["name"]
        LoadItem2Table(data,'realmCharacter')
    except (timeout.TimeoutError, IOError):
        traceback.print_exc()
        wf.logger.logger.exception("Continue after ProcessToon(url=%s)" % url)






def ProcessToons(zone, realm, toons):
    for toon in toons:
        ProcessToon(zone, realm, toon)



# ["Process-Toons.py", "US", "Uldaman", "Drollete", "Chewrider", ...

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
        wf.logger.logger.error("Not enough arguments to %s", sys.argv[0])
