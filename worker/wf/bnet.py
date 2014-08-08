#!/usr/bin/env python

import httplib
import json
import logging
import os
import tempfile
import urllib3
import urllib3.util
import urllib3.util.request
import wf.logger
import wf.rds
from urllib3 import PoolManager, Retry


http = PoolManager(10,
                   headers=urllib3.util.request.make_headers(keep_alive=True, user_agent="WoW-Forge/1.0"),
                   timeout=urllib3.util.Timeout(connect=5, read=1),
                   retries=Retry(total=50, connect=3, read=3, redirect=3, backoff_factor=1))

httplib.HTTPConnection.debuglevel = 1
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

class BNetError(StandardError):
    def __init__(self, url, response):
        self.url = url
        self.status = response.status
        self.msg = response.read()

    def __str__(self):
        return "<BNetError url=%s, status=%s, msg=%s>" % (self.url, self.status, self.msg)

def request(url, return_file=False, allow_compression=False, modified_since=None):
    headers = {}
    if modified_since:
        headers["If-Modified-Since"] = modified_since
    if allow_compression:
        headers["Accept-encoding"] = 'gzip'
    response = http.request('GET', url, headers=headers, preload_content=False)
    if modified_since and response.status == 304:
        wf.logger.logger.info("Status 304, no new data since %s" % modified_since)
        return None
    if response.status == 200:
        # Happiness
        if return_file:
            (ohandle, path) = tempfile.mkstemp()
            handle = os.fdopen(ohandle, "w")
            wf.logger.logger.info("Status 200, saving to %s" % path)
            while True:
                data = response.read(64*1024, decode_content=True)
                if data is None or data is '':
                        break
                handle.write(data)
            handle.close()
            response.release_conn()
            return path
        data = response.data
        wf.logger.logger.info("Status 200,  content [%s]" % data)
        response.release_conn()
        c_type = response.headers.get('content-type', '')
        if "json" in c_type.lower():
            data = json.loads(data)
        return data
    if response.status == 500:
        data = response.read()
        wf.util.IsLimitExceeded(data)
    raise BNetError(url, response)


def get_auctions(zone, realm, lastScanned):
    wf.logger.logger.info("Checking data for %s realm [%s]" % (zone, realm))
    slug = wf.rds.Realm2Slug(zone, realm)
    data = request("http://%s.battle.net/api/wow/auction/data/%s" % (zone, slug),  modified_since=lastScanned)
    if data is None and lastScanned:
        # No new data
        wf.logger.logger.info("No new data from %s realm %s since %s." % (zone, realm, lastScanned))
        wf.rds.FinishedRealm(zone, realm, lastScanned)
        return None
    url = data['files'][0]['url']
    lm = data['files'][0]['lastModified']
    path = request(url, return_file=True, allow_compression=True)
    wf.rds.FinishedRealm(zone, realm, lm)
    return path