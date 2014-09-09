#!/usr/bin/env python

import datetime
import json
import sys
import wf.logger


def Load_AH_State(file):
    print "Reading Data from: "+file
    json_file = open(file, "r")
    data = json.load(json_file)
    json_file.close()
    return data

def DictEqual(a, b):
    shared_keys = set(a.keys()) & set(b.keys())
    if not (len(shared_keys) == len(a.keys()) and len(shared_keys) == len(b.keys())):
        return False
    for key in a:
        if a[key] != b[key]:
            return False
    return True


def CompareDicts(pre, post, keys):
    diff = set()
    for key in keys:
        if not DictEqual(pre[key], post[key]):
            diff.add(key)
    return diff


def AH_List2Map(into):
    output = {}
    for auc in into:
        output[auc["auc"]] = auc
    return output

def AH_Diff(pre, post):
    pre = AH_List2Map(pre)
    post = AH_List2Map(post)
    pre_set = set(pre.keys())
    post_set = set(post.keys())
    missing = pre_set - post_set
    new = post_set - pre_set
    mutated = CompareDicts(pre, post, pre_set & post_set)

    print "*"*40
    print "Missing"
    for key in missing:
        print pre[key]
    print "*"*40
    # print "New"
    # for key in new:
    #     print key
    # print "*"*40
    # print "Changed"
    # for key in mutated:
    #     print key

def Realm_diff(before, after):
    pre = Load_AH_State(before)
    post = Load_AH_State(after)
    print "A"*80
    AH_Diff(pre['alliance']['auctions'], post['alliance']['auctions'])
    print "H"*80
    AH_Diff(pre['horde']['auctions'], post['horde']['auctions'])
    print "N"*80
    AH_Diff(pre['neutral']['auctions'], post['neutral']['auctions'])


try:
    Realm_diff(sys.argv[1], sys.argv[2])
except:
    import pdb
    pdb.post_mortem()
    wf.logger.logger.exception("Exception while calling ScanAuctionHouses()")
    exit(1)
       

    
