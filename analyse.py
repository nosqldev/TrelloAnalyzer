#!/usr/bin/python3
# -*- coding: utf-8 -*-

# © Copyright 2017 jingmi. All Rights Reserved.
#
# -----------------------------------------------------------------------
# analyzing any list in trello
# Author: jingmi@gmail.com
# Created: 2017-08-01 14:44
# -----------------------------------------------------------------------

# TODO
# 1. Support parameters so we can run script as follows: ./analyse.py todo
# 2. Fill the blank function: groupby_author(), groupby_task()
# 3. Handle more task type, e.g: 新增/new/临时
# 4. Be compatible with Python 2.x and Python 3.x
# 5. Write test code for this project
# 6. Provide flexible pattern to match titles such as: "Refactor the data access object(1h) (3h)"
# 7. Draw burn down chart
# 8. Snap todo list

# Get your app-key from: https://trello.com/app-key
# Get token from: https://trello.com/1/authorize?expiration=never&scope=read&response_type=token&name=Server%20Token&key={APP-KEY}

import json
import urllib.request
import re
import sys

# {{{ global config
g_app_key = None
g_token = None
g_board_id = None
# }}}
# {{{ pattern config
workload_pattern = u'[(（]\s*(\d+(?:\.\d+)?)\s*h\s*[)）]'
task_pattern = u'[\[【［]\s*(新\s*增|紧\s*急)\s*[】］\]]\s*'
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

    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        lightwhite = '\033[1;37;40m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'
    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'

# }}}

def read_config(filepath):
    global g_app_key
    global g_token
    global g_board_id

    f = None
    try:
        f = open(filepath, "r")
    except IOError as e:
        print("OOPS: " + str(e))
        print('''Perhaps you need:
    1. cp trello.json config.json
    2. fill config.json''')
        sys.exit(-1)

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
    request = urllib.request.Request(url)
    content = None

    try:
        response = urllib.request.urlopen(request)
        content = response.read().decode()
    except urllib.request.HTTPError as e:
        print("http error: " + str(e))
    except Exception as e:
        print("error: " + str(e))

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
    cards_info = [(item['id'], item['name'], item['idMembers'][0]) for item in body]

    return cards_info

def fetch_board_members():
    url = 'https://api.trello.com/1/boards/_BOARDID_/members?key=_APP_KEY_&token=_TOKEN_'
    url = basic_replace(url)
    url = url.replace("_BOARDID_", g_board_id)
    body = do_request(url)
    member_info = {}

    for item in body:
        member_info[item['id']] = item['fullName']

    return member_info

def fetch_card_members(card_members, memberId, man_hour):
    if len(card_members) > 0:
        isMemberExist = False

        for member in card_members:
            if member['id'] == str(memberId):
                member['man_hour'] += man_hour
                isMemberExist = True
                break
        if isMemberExist is False:
            card_members.append({'id': memberId, 'man_hour': man_hour})
    else:
        card_members.append({'id': memberId, 'man_hour': man_hour})

    return card_members

def groupby_author(board_members, card_members, memberId, man_hour):
    members_counter = []
    fetch_card_members(card_members, memberId, man_hour)

    for card_member in card_members:
        members_counter.append({'fullName': board_members[card_member['id']], 'time': card_member['man_hour']})

    return members_counter

def sum_workloads(cards_info):
    compiled_workload_pattern = re.compile(workload_pattern, re.S | re.U)
    counter = {'total': 0, 'none': 0, 'new': 0, 'urgent': 0}
    card_members = []
    board_members = fetch_board_members()

    for card_info in cards_info:
        man_hour = compiled_workload_pattern.findall(card_info[1])
        memberId = card_info[2]

        if len(man_hour) > 0:
            man_hour = float(man_hour[0])
            counter['total'] += man_hour
            members_counter = groupby_author(board_members, card_members, memberId, man_hour)
            groupby_task(card_info[1], man_hour, counter)

        else:
            counter['none'] += 1

    return {'counter': counter, 'members_counter': members_counter}

def groupby_task(title, man_hour, counter):
    compiled_task_pattern = re.compile(task_pattern, re.S | re.U)
    task = compiled_task_pattern.findall(title)

    if len(task) > 0:
        task[0].replace(' ', '')
        if task[0] == '新增':
            counter['new'] += man_hour
        elif task[0] == '紧急':
            counter['urgent'] += man_hour


def show(list_pattern, stat_man_hour, members_counter):
    print(colors.fg.red, "LIST IS: [", list_pattern, "]")
    print(colors.fg.cyan, stat_man_hour, colors.reset)
    print(colors.fg.cyan, members_counter, colors.reset)

def compute_list(list_pattern):
    all_cards_info = []

    for list_id in fetch_list_id(list_pattern):
        for card_info in fetch_cards(list_id[1]):
            all_cards_info.append(card_info)

    workloads_statistic = sum_workloads(all_cards_info)
    show(list_pattern, workloads_statistic['counter'], workloads_statistic['members_counter'])

def main():
    read_config("./config.json")
    compute_list("^Done$")

    #print("list's name:")
    #listname = sys.argv[1]
    #compute_list(listname)

if __name__ == '__main__':
    main()

# vim: set expandtab tabstop=4 shiftwidth=4 foldmethod=marker:

