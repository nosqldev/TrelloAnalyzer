#!/usr/bin/python
# -*- coding: utf-8 -*-

# © Copyright 2017 jingmi. All Rights Reserved.
#
# -----------------------------------------------------------------------
# analyzing any list in trello
# Author: jingmi@gmail.com
# Created: 2017-08-01 14:44
# -----------------------------------------------------------------------

# Get your app-key from: https://trello.com/app-key
# Get token from: https://trello.com/1/authorize?expiration=never&scope=read&response_type=token&name=Server%20Token&key={APP-KEY}

import json
import urllib2 
import re

# {{{ global config
g_app_key = None
g_token = None
g_board_id = None
# }}}
# {{{ pattern config
workload_pattern = u'[(（]\s*(\d+)\s*pt[)）]'
# }}}
# {{{ class colors
class colors:
    '''Colors class:
    reset all colors with colors.reset
    two subclasses fg for foreground and bg for background.
    use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.green
    also, the generic bold, disable, underline, reverse, strikethrough,
    and invisible work with the main class
    i.e. colors.bold'''

    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class fg:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        lightwhite='\033[1;37;40m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'

# }}}

def read_config(filepath):
    global g_app_key
    global g_token
    global g_board_id

    f = open(filepath, "r")
    config = json.load(f)
    f.close()

    g_app_key = config['app_key']
    g_token = config['token']
    g_board_id = config['board_id']

def basic_replace(url):
    url = url.replace("_APP_KEY_", g_app_key)
    url = url.replace("_TOKEN_", g_token)
    return url

def do_request(url):
    request = urllib2.Request(url)
    content = None

    try:
        response = urllib2.urlopen(request)
        content = response.read()
    except urllib2.HTTPError as e:
        print "http error: " + str(e)
    except Exception as e:
        print "error: " + str(e)

    if content is None:
        return []
    else:
        return json.loads(content)

def fetch_list_id(list_pattern):
    url = 'https://api.trello.com/1/boards/_BOARDID_/lists?key=_APP_KEY_&token=_TOKEN_'
    url = basic_replace(url)
    url = url.replace("_BOARDID_", g_board_id)
    body = do_request(url)
    list_ids = []

    for item in body:
        if re.search(list_pattern, item['name'], re.I) is not None:
            list_ids.append((item['name'], item['id']))

    return list_ids

def fetch_cards(list_id):
    url = 'https://api.trello.com/1/lists/_LIST_ID_/cards?key=_APP_KEY_&token=_TOKEN_'
    url = basic_replace(url)
    url = url.replace("_LIST_ID_", list_id)
    body = do_request(url)
    cards_info = [(item['id'], item['name']) for item in body]

    return cards_info

def sum_workloads(cards_info):
    compiled_pattern = re.compile(workload_pattern, re.S | re.U)

    counter = {'total':0, 'none':0}

    for card_info in cards_info:
        result = compiled_pattern.findall(card_info[1])
        #print card_info[1], result
        if len(result) > 0:
            counter['total'] += int(result[0])
        else:
            counter['none'] += 1

    return counter

def groupby_author():
    pass

def groupby_task():
    pass

def show(list_pattern, stat_result):
    print colors.fg.red, "LIST IS: [", list_pattern, "]" 
    print colors.fg.lightcyan, stat_result, colors.reset

def compute_list(list_pattern):
    all_cards_info = []

    for list_id in fetch_list_id(list_pattern):
        for card_info in fetch_cards(list_id[1]):
            all_cards_info.append(card_info)

    show(list_pattern, sum_workloads(all_cards_info))

def main():
    read_config("./trello.json")
    compute_list("^Done$")

if __name__ == '__main__':
    main()

# vim: set expandtab tabstop=4 shiftwidth=4 foldmethod=marker:

