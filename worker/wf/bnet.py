#!/usr/bin/env python

import datetime
import httplib
import json
import logging
import os
import tempfile
import time
import types
import urllib3
import urllib3.util
import urllib3.util.request
import wf.logger
import wf.rds
import wf.util
from urllib3 import PoolManager, Retry


http = PoolManager(10,
                   headers=urllib3.util.request.make_headers(keep_alive=True, user_agent="WoW-Forge/1.0"),
                   timeout=urllib3.util.Timeout(connect=5, read=1),
                   retries=Retry(total=50, connect=3, read=3, redirect=3, backoff_factor=1))

# httplib.HTTPConnection.debuglevel = 1
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

class BNetError(StandardError):
    def __init__(self, url, response):
        self.url = url
        self.status = response.status
        self.msg = response.read()

    def __str__(self):
        return "<BNetError url=%s, status=%s, msg=%s>" % (self.url, self.status, self.msg)

def iso_date(in_date):
    if isinstance(in_date, types.StringTypes):
        return datetime.datetime.strptime(in_date, "%Y-%m-%d %H:%M:%S")
    return in_date

# Sat, 09 Aug 2014 17:06:27 GMT
def http_date(in_date):
    if isinstance(in_date, types.StringTypes):
        in_date = datetime.datetime.strptime(in_date, "%Y-%m-%d %H:%M:%S")
    return in_date.strftime("%a, %d %b %Y %H:%M:%S GMT")


def request(url, return_file=False, allow_compression=False, modified_since=None, retry404=None):
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
            (temp_handle, path) = tempfile.mkstemp()
            handle = os.fdopen(temp_handle, "w")
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
    if response.status == 404 and retry404 and retry404 > 0:
        wf.logger.logger.info("URL %s not found, retry up to %d times" % (url, retry404))
        time.sleep(1.0)
        return request(url, return_file, allow_compression, modified_since, retry404 - 1)
    raise BNetError(url, response)


def get_auctions(zone, realm, lastScanned):
    wf.logger.logger.info("Checking AH data for %s realm [%s] last checked %s" % (zone, realm, lastScanned))
    slug = wf.rds.Realm2Slug(zone, realm)
    if lastScanned:
        modified_since = http_date(lastScanned)
    else:
        modified_since = None
    data = request("http://%s.battle.net/api/wow/auction/data/%s" % (zone, slug),  modified_since=modified_since)
    if data is None and lastScanned:
        # No new data
        wf.logger.logger.info("No new data from %s realm %s since %s." % (zone, realm, lastScanned))
        return None
    url = data['files'][0]['url']
    lm = data['files'][0]['lastModified']
    try:
        path = request(url, return_file=True, allow_compression=True, retry404=4)
    except BNetError:
        wf.logger.logger.exception("get_auctions()")
        wf.rds.FinishedRealm(zone, realm, lastScanned)
        return None
    wf.rds.FinishedRealm(zone, realm, datetime.datetime.utcfromtimestamp(lm/1000).isoformat(" "))
    return (path, (lm/1000))