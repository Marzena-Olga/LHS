#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script prepare tickets on Jira from Prometheus metrics.
# Author: Marzena Kupniewska
# Maintainer: Marzena Kupniewska

import requests
import json
import base64
import urllib3
import sys
import argparse
from datetime import datetime, timedelta, timezone

def get_silences():
    tok = 'admin' + ':' + 'admin'
    encoded_tok = base64.b64encode(tok.encode()).decode()
    url = 'https://l-prdmon-p02.discover.lhgroup.de:8443/alertmanager/api/v2/silences'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Basic %s' % encoded_tok}
    proxy = {'http': '', 'https': ''}
    r = requests.get(url, headers=headers, proxies=proxy, verify=False)
    print(r.status_code)
    print(r)
    z = (r.json())
    print(json.dumps(z, indent=4))

def set_silences(url, login, password, minutes):
    tok = login + ':' + password
    encoded_tok = base64.b64encode(tok.encode()).decode()
    #url = 'https://l-prdmon-p02.discover.lhgroup.de:8443/alertmanager/api/v2/silences'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Basic %s' % encoded_tok}
    proxy = {'http': '', 'https': ''}
    now = datetime.now(timezone.utc)
    startsat = now.strftime('%Y-%m-%dT%H:%M:%S')
    end = now + timedelta(minutes=minutes)
    endsat = end.strftime('%Y-%m-%dT%H:%M:%S')
    print(startsat, ' ', endsat)
    silence_json = json.dumps({
        "comment": "silenced by pipelie",
        "createdBy": "pipeline",
        "matchers": [
            {
                "name": "environment",
                "value": "PRD",
                "isRegex": False
            }
        ],
        "startsAt": startsat,
        "endsAt": endsat,
        "status": {"state": "active"}
    })
    r = requests.request("POST", url, verify=False, proxies=proxy, data=silence_json, headers=headers)
    z = (r.json())
    print(json.dumps(z, indent=4))
    return r.status_code

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Script required params eq: --url=https://l-prdmon-p02.discover.lhgroup.de:8443/alertmanager/api/v2/silences --login=admin --password=adminpassword --time=120"
    )
    parser.add_argument("--url", required=True, type=str)
    parser.add_argument("--login", required=True, type=str)
    parser.add_argument("--password", required=True, type=str)
    parser.add_argument("--time", required=True, type=str)
    args = parser.parse_args()

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    #get_silences()

    if args.time == '5m':
        stime = 5
    if args.time == '15m':
        stime = 15
    if args.time == '30m':
        stime = 30
    if args.time == '1h':
        stime = 60
    if args.time == '2h':
        stime = 120
    if args.time == '3h':
        stime = 180
    if args.time == '1d':
        stime = 1440

    ret = set_silences(args.url, args.login, args.password, stime)
    print(ret)
    if ret != 200:
        sys.exit(-1)

