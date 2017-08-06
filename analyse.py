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
# 3. Provide flexible pattern to match titles such as: "Refactor the data access object(1h) (3h)"
# 4. Handle more task type, e.g: 新增/new/临时
# 5. Snap todo list
# 6. Be compatible with Python 2.x and Python 3.x
# 7. Draw burn down chart
# 8. Write test code for this project

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


def fetch_card_name_by_pattern(card_name, pattern):
    return re.compile(pattern, re.S | re.U).findall(card_name)


def fetch_list_id_by_board(list_pattern):
    url = 'https://api.trello.com/1/boards/_BOARDID_/lists?key=_APP_KEY_&token=_TOKEN_'
    url = basic_replace(url)
    url = url.replace("_BOARDID_", g_board_id)
    body = do_request(url)
    list_info = []

    for item in body:
        if re.search(list_pattern, item['name'], re.I) is not None:
            list_info.append({'id': item['id'], 'name': item['name']})

    return list_info


def fetch_members_by_board():
    url = 'https://api.trello.com/1/boards/_BOARDID_/members?key=_APP_KEY_&token=_TOKEN_'
    url = basic_replace(url)
    url = url.replace("_BOARDID_", g_board_id)
    body = do_request(url)
    all_members_info = {}

    for item in body:
        all_members_info[item['id']] = item['fullName']

    return all_members_info


def fetch_cards_info(list_id):
    url = 'https://api.trello.com/1/lists/_LISTID_/cards?key=_APP_KEY_&token=_TOKEN_'
    url = basic_replace(url)
    url = url.replace("_LISTID_", list_id)
    body = do_request(url)
    available_cards_info = []
    board_members = fetch_members_by_board() #todo

    for item in body:
        member_id = None

        if len(item['idMembers']) > 0 and item['idMembers'][0] is not None:
            full_name = board_members[item['idMembers'][0]]
            member_id = item['idMembers'][0]
        else:
            full_name = 'null'
            member_id = ''

        card_hours = fetch_card_name_by_pattern(item['name'], workload_pattern)
        plan_hours = float(card_hours[0]) if len(card_hours) > 0 else 0
        work_hours = float(card_hours[1]) if len(card_hours) > 1 else plan_hours

        available_cards_info.append({
            'id': item['id'],
            'member_id': member_id,
            'card_name': item['name'],
            'full_name': full_name,
            'card_hours': card_hours,
            'plan_hours': plan_hours,
            'work_hours': work_hours
        })

    return available_cards_info


def groupby_task(card_statistics, card_name, hours):
    task = fetch_card_name_by_pattern(card_name, task_pattern)

    if len(task) > 0:
        task[0].replace(' ', '')
        if task[0] == '新增':
            card_statistics['new'] += hours
        elif task[0] == '紧急':
            card_statistics['urgent'] += hours


def groupby_author(members_info, card_info):
    member_id = card_info['member_id']

    if member_id in members_info:
        members_info[member_id]['plan_hours'] += card_info['plan_hours']
        members_info[member_id]['work_hours'] += card_info['work_hours']
    else:
        members_info[member_id] = {
            'full_name': card_info['full_name'],
            'plan_hours': card_info['plan_hours'],
            'work_hours': card_info['work_hours']
        }


def sum_workloads(all_cards_info):
    card_statistics = {'total': 0, 'none': 0, 'new': 0, 'urgent': 0}
    member_statistics = []
    members_info = {}

    for card_info in all_cards_info:
        card_hours = card_info['card_hours']
        if len(card_hours) > 0:
            hours = float(card_hours[0])
            card_statistics['total'] += hours
            groupby_task(card_statistics, card_info['card_name'], hours)
        else:
            card_statistics['none'] += 1

        groupby_author(members_info, card_info)

    members_info_keys = members_info.keys()

    for member_id in members_info_keys:
        member_statistics.append(members_info[member_id])

    return {'card_statistics': card_statistics, 'member_statistics': member_statistics}


def show(list_type, card_statistics, member_statistics):
    print(colors.fg.red, "LIST IS: [", list_type, "]")
    print(colors.fg.cyan, card_statistics, colors.reset)
    print(colors.fg.cyan, member_statistics, colors.reset)


def compute_list(list_pattern):
    all_cards_info = []

    for list in fetch_list_id_by_board(list_pattern):
        all_cards_info = fetch_cards_info(list['id'])

    workloads = sum_workloads(all_cards_info)
    show(list_pattern, workloads['card_statistics'], workloads['member_statistics'])


def main():
    read_config("./config.json")
    listname = "DONE"

    if len(sys.argv) == 2:
        listname = sys.argv[1]

    compute_list(listname)

if __name__ == '__main__':
    main()

# vim: set expandtab tabstop=4 shiftwidth=4 foldmethod=marker:

