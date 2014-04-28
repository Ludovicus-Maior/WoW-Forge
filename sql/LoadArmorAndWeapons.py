#!/usr/bin/env python

from boto.s3.connection import S3Connection
import exceptions
import json
from pprint import pprint
from types import *
import MySQLdb
import os
import string
import sys


#   {"id":21846,"disenchantingSkillRank":300,"description":"","name":"Spellfire Belt","icon":"inv_belt_04","stackable":1,"itemBind":2,
#        "bonusStats":[{"stat":5,"amount":35,"reforged":false},{"stat":32,"amount":18,"reforged":false},{"stat":7,"amount":27,"reforged":false}],
#        "itemSpells":[],"buyPrice":108162,"itemClass":4,"itemSubClass":1,"containerSlots":0,"inventoryType":6,"equippable":true,
#        "itemLevel":105,
#        "itemSet":{"id":552,"name":"Wrath of Spellfire",
#                   "setBonuses":[{"description":"Increases spell power by 7% of your total Intellect.","threshold":3}],
#                   "items":[21848,21847,21846]},
#        "maxCount":0,"maxDurability":60,"minFactionId":0,"minReputation":0,"quality":4,
#        "sellPrice":21632,"requiredSkill":0,"requiredLevel":70,"requiredSkillRank":0,
#        "socketInfo":{"sockets":[{"type":"YELLOW"},{"type":"BLUE"}],
#                      "socketBonus":"+4 Stamina"},
#        "itemSource":{"sourceId":26752,"sourceType":"CREATED_BY_SPELL"},
#        "baseArmor":233,"hasSockets":true,"isAuctionable":true,"armor":233,"displayInfoId":43295,"nameDescription":"","nameDescriptionColor":"000000"},
#   {"id":24461,"disenchantingSkillRank":225,"description":"","name":"Hatebringer","icon":"inv_mace_21","stackable":1,"itemBind":1,
#        "bonusStats":[{"stat":4,"amount":25,"reforged":false},{"stat":32,"amount":22,"reforged":false},{"stat":7,"amount":21,"reforged":false}],
#        "itemSpells":[],"buyPrice":452373,"itemClass":2,"itemSubClass":5,"containerSlots":0,
#        "weaponInfo":{"damage":{"min":240,"max":360},"weaponSpeed":3.6,"dps":83.333336},
#        "inventoryType":17,"equippable":true,"itemLevel":94,"maxCount":0,"maxDurability":100,"minFactionId":0,"minReputation":0,"quality":3,
#        "sellPrice":90474,"requiredSkill":0,"requiredLevel":63,"requiredSkillRank":0,
#        "socketInfo":{"sockets":[{"type":"RED"},{"type":"YELLOW"},{"type":"BLUE"}],"socketBonus":"+4 Strength"},
#        "itemSource":{"sourceId":18105,"sourceType":"CREATURE_DROP"},"baseArmor":0,"hasSockets":true,"isAuctionable":false,
#        "armor":0,"displayInfoId":43200,"nameDescription":"","nameDescriptionColor":"000000"},


def ReadItemData():
    conn = S3Connection()
    bucket = conn.get_bucket("wow-forge-bootstrap")
    key  = bucket.get_key("database/itemdata_5.0.json")
    key.get_contents_to_filename("/tmp/itemdata_5.0.json")
    json_file=open('/tmp/itemdata_5.0.json')
    json_data = json.load(json_file)
    json_file.close()
    return json_data
    
def ConnectDatabase():
    global database
    try:
        db_host=os.environ['WF_RDS_HOST']
        db_user=os.environ['WF_RDS_USER']
        db_pass=os.environ['WF_RDS_PASSWORD']
    except:
        print "Missing environment variable setup for WF_RDS_*"
        pass

    database=MySQLdb.connect(host=db_host,user=db_user,passwd=db_pass,db="Warcraft")
    database.autocommit(True)

TableFields = {}
    
def AnalyzeTable(table):
    global database
    print "# Analyzing table %s" % table
    TableFields[table] = {}
    c=database.cursor()
    c.execute("""SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS`
                     WHERE `TABLE_SCHEMA`='Warcraft' and `table_name` = %s ;""" , (table,) )
    d=c.fetchone()
    while d :
        column = d[0]
#        print column
        TableFields[table][column] = True
        d=c.fetchone()
    c.close()

def AnalyzeSchema():
    AnalyzeTable('item')
    AnalyzeTable('item_name')
    AnalyzeTable('equippable')

ItemFieldsWritten = {}
              
def LoadItem2Table(Item,table):
    global ItemFieldsWritten
    c=database.cursor()
    cmd = "REPLACE INTO `Warcraft`.`%s` (" % table

    if not table in TableFields:
        raise KeyError("Hey!  Someone forgot to Analyze table %s" % table)

    tfs = set(TableFields[table])
    ifs = set(Item)
    tks = list(tfs & ifs)
    tks.sort()
    
    cmd = cmd + string.join(tks,',') + " ) VALUES ("
    v=[]
    for tk in tks:
        v.append('%('+tk+')s')
        ItemFieldsWritten[tk] = True
        
    cmd = cmd + string.join(v,',') + ") ;"
#    print "# %s" % (cmd,)
    try:
        c.execute(cmd,Item)
    except:
        print "# Exception with command %s" % c._last_executed
        raise
    finally:
        c.close()
#        print "# %s" % (c._last_executed,)

def ValidateItem(Item):
    global ItemFieldsWritten
    unwrittenFields = list(set(Item) - set(ItemFieldsWritten))
    if len(unwrittenFields) == 0:
        return
    validated = True
    for unwritten in unwrittenFields:
        if (Item[unwritten] != 0) and (Item[unwritten] != []):
            print "!! Field %s with value %s in item %d [%s] unwritten." % (unwritten,Item[unwritten],Item['id'],Item['name'])
            validated = False
    if not validated:
         raise KeyError("Validation failure")
            
        
unpackBonus = { 3: 'statAgility', 4:'statStrength', 5:'statIntellect', 6:'statSpirit', 7:'statStamina', 32:'statCritical',
                36:'statHaste', 49:'statMastery', 35:'statResilience', 31:'statHit', 13:'statDodge', 14:'statParry', 45:'statSpellPower',
                57:'statPVPPower', 37:'statExpertise' }
unPackedBonuses= {}

def ReportData():
    print "# Ignored bonusStats ..."
    pprint(unPackedBonuses)

def UnpackItem(Item):
    if Item['bonusStats'] == [] and  Item['itemSpells'] == [] and Item['itemLevel'] > 1 :
        # No stats, thats suspicicous!
        Item['randomEnchant'] = True
        
    # "bonusStats":[{"stat":5,"amount":35,"reforged":false},{"stat":32,"amount":18,"reforged":false},{"stat":7,"amount":27,"reforged":false}],
    global unPackedBonuses
    for bonus in Item['bonusStats']:
        if bonus['stat'] in unpackBonus:
            Item[unpackBonus[bonus['stat']]] = bonus['amount']
        else:
            if bonus['stat'] in unPackedBonuses:
                unPackedBonuses[bonus['stat']] += 1
            else:
                unPackedBonuses[bonus['stat']] = 1
    del(Item['bonusStats'])
            
    # "socketInfo":{"sockets":[{"type":"YELLOW"},{"type":"BLUE"}],"socketBonus":"+4 Stamina"},
    if 'socketInfo' in Item:
        Item['sockets'] = ''
        for socket in Item['socketInfo']['sockets']:
            Item['sockets'] += socket['type'][0]
        if 'socketBonus' in Item['socketInfo']:
            Item['socketBonus'] = Item['socketInfo']['socketBonus']
        del(Item['socketInfo'])
    
    # "weaponInfo":{"damage":{"min":240,"max":360},"weaponSpeed":3.6,"dps":83.333336},
    if 'weaponInfo' in Item:
        Item['damageMin'] = Item['weaponInfo']['damage']['min']
        Item['damageMax'] = Item['weaponInfo']['damage']['max']
        Item['weaponSpeed'] = Item['weaponInfo']['weaponSpeed']
        Item['dps'] = Item['weaponInfo']['dps']
        del(Item['weaponInfo'])
        
    # allowableClasses = [2 ,3 4]
    if 'allowableClasses' in Item:
        Item['allowableClasses'] = string.join(map(str,Item['allowableClasses']),",")

    # allowableRaces =  [6, 9]
    if 'allowableRaces' in Item:
        Item['allowableRaces'] = string.join(map(str,Item['allowableRaces']),",")
                
    # "itemSource":{"sourceId":26752,"sourceType":"CREATED_BY_SPELL"},
    if 'itemSource' in Item:
        Item['itemSource'] = "%s:%s" % (Item['itemSource']['sourceType'], Item['itemSource']['sourceId'])
        if Item['itemSource'] == "NONE:0":
            del(Item['itemSource'])
        
    # "requiredAbility":{u'spellId': 20222, u'name': u'Goblin Engineer', u'description': u'Allows an engineer to make lethal goblin devices.'}
    if 'requiredAbility' in Item:
        Item['requiredAbility'] = Item['requiredAbility']['spellId']
 
    # "boundZone": {u'id': 2017, u'name': u'Stratholme'} 
    if 'boundZone' in Item:
        Item['boundZone'] = Item['boundZone']['id']
        
        
     # "itemSet":{u'items': [10412, 10411, 10413, 10410, 6473], u'setBonuses': [{u'threshold': 2, u'description': u'Increases Intellect by 5.'}, {u'threshold': 3, u'description': u'Increases expertise by 4.'}, {u'threshold': 4, u'description': u'Increases Intellect by 5.'}, {u'threshold': 5, u'description': u'Increases Intellect by 10.'}], u'id': 162, u'name': u'Embrace of the Viper'}
    if 'itemSet' in Item:
        # TODO
        del(Item['itemSet'])
       
    # "itemSpells":{u'nCharges': 0, u'spellId': 17152, u'spell': {u'castTime': u'Instant', u'description': u'Increases Strength by 200 for 10 sec.', u'icon': u'spell_nature_strength', u'id': 17152, u'name': u'Destiny'}, u'trigger': u'ON_PROC', u'consumable': False, u'categoryId': 0}]
    if 'itemSpells' in Item:
        # TODO
        del(Item['itemSpells'])
        
            
def LoadItem(Item):
    global ItemFieldsWritten
    if (Item['itemClass'] != 4) and (Item['itemClass'] != 2) :
        return
    UnpackItem(Item)
    ItemFieldsWritten = {}
    LoadItem2Table(Item,'item')
    LoadItem2Table(Item,'item_name')
    LoadItem2Table(Item,'equippable')
    ValidateItem(Item)
    

def LoadData(Data):
    count = 0
    for item in Data['items']:
        LoadItem(item)
        count = count + 1
        if (count % 1000) == 0 :
            print "# Processed %d records" % count


print "Reading Data"
jd=ReadItemData()
print "Read %d items" % len(jd['items'])
print "analyzing"
ConnectDatabase()
AnalyzeSchema()
LoadData(jd)
ReportData()

    
