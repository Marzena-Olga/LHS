#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script manage monitoring silences in alertmanager.
# Author: Marzena Kupniewska
# Maintainer: Marzena Kupniewska

import urllib3
import requests
import base64
import os
import json
import datetime
import time
import socket
import sys

#https://petstore.swagger.io/?url=https://raw.githubusercontent.com/prometheus/alertmanager/main/api/v2/openapi.yaml#/

def get_silences(show=0):
    tok = login + ':' + password
    encoded_tok = base64.b64encode(tok.encode()).decode()
    headers = {'Content-Type': 'application/json', 'Authorization': 'Basic %s' % encoded_tok}
    proxy = {'http': '', 'https': ''}
    url = 'https://l-pdtmon-t02.discover-test.lhgroup.de:8443/alertmanager/api/v2/silences'
    r = requests.get(url, headers=headers, proxies=proxy, verify=False)
    print(r.status_code)
    try:
        z = (r.json())
    except:
        sys.exit('No json return')
    if show == 1:
        print('List silences:')
        id = 0
        for i in z:
            if i['status']['state'] == 'active':
                print(id,'-', i['id'], i['status']['state'], i['createdBy'], i['comment'], i['endsAt'], i['matchers'])
            id = id + 1
    return z

def set_silent(name='',value='',silent_time=''):
    print('Set silence')
    tok = login + ':' + password
    encoded_tok = base64.b64encode(tok.encode()).decode()
    headers = {'Content-Type': 'application/json', 'Authorization': 'Basic %s' % encoded_tok}
    proxy = {'http': '', 'https': ''}
    url = 'https://l-pdtmon-t02.discover-test.lhgroup.de:8443/alertmanager/api/v2/silences'
    data = json.dumps({
        "matchers": [{"name": "envinronment", "value": "UAT", "isRegex": False, "isEqual": True}, ],
        "startsAt": datetime.datetime.utcfromtimestamp(time.time()).isoformat(),
        "endsAt": datetime.datetime.utcfromtimestamp(time.time() + 4*3600).isoformat(),
        "createdBy": "MK",
        "comment": "Testowy Silence"})
    data = json.loads(data)
    print(json.dumps(data, indent=4))
    r = requests.post(url, json=data,  headers=headers, proxies=proxy, verify=False)
    print(r.status_code)
    print(r.content)

def remove_silence(silence):
    tok = login + ':' + password
    encoded_tok = base64.b64encode(tok.encode()).decode()
    headers = {'Content-Type': 'application/json', 'Authorization': 'Basic %s' % encoded_tok}
    proxy = {'http': '', 'https': ''}
    url = 'https://l-pdtmon-t02.discover-test.lhgroup.de:8443/alertmanager/api/v2/silence'
    url = url + '/' + silence
    r = requests.delete(url, headers=headers, proxies=proxy, verify=False)
    print(r.status_code)

def choose_silence():
    ret = ''
    while ret == '':
        silence_list = get_silences(1)
        id = input("Write silence number or q to quit the script: ")
        id = int(id)
        #silence = silence_list[id]['id']
        silence = silence_list[id]['id']
        #print(id, silence)
        for i in silence_list:
            if silence == i['id']:
                print(silence)
                #remove_silence(silence)
            if (silence == 'q' or silence == 'Q'):
                ret = silence
                sys.exit()

if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    login = 'admin'
    password = sys.argv[1]
    print('#########################################################################')
    #set_silent()
    choose_silence()
    get_silences(1)


