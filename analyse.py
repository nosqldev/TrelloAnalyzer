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
# 9. Switch between multiple boards

# Get your app-key from: https://trello.com/app-key
# Get token from: https://trello.com/1/authorize?expiration=never&scope=read&response_type=token&name=Server%20Token&key={APP-KEY}

import urllib.request
import re
import sys
import codecs
import sendemail
import chartstat
import json
from datetime import datetime
import glob

# {{{ global config
g_app_key = None
g_token = None
g_board_id = None
g_user_id = None
g_sender = None
g_receiver = None
g_username = None
g_password = None
# }}}
# {{{ pattern config
workload_pattern = u'[(（]\s*(\d+(?:\.\d+)?)\s*[hH]\s*[)）]'
requirement_pattern = u'[\[【［]\s*(.*)\s*[】］\]]\s*'
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
    global g_user_id
    global g_board_id
    global g_sender
    global g_receiver
    global g_username
    global g_password

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
    g_user_id = config['user_id']
    g_board_id = config['board_id']
    g_sender = config['sender']
    g_receiver = config['receiver']
    g_username = config['username']
    g_password = config['password']


def basic_replace(url):
    url = url.replace("_APP_KEY_", g_app_key)
    url = url.replace("_TOKEN_", g_token)
    return url


def do_request(url):
    request = urllib.request.Request(url)
    content = None
    flag = False

    for i in range(3):  # retry when network access failed
        try:
            response = urllib.request.urlopen(request)
            content = response.read().decode()
            flag = True
            break
        except urllib.request.HTTPError as e:
            print("http error: " + str(e))
        except Exception as e:
            print("error: " + str(e))

    if not flag:
        sys.exit(-1)

    if content is None:
        return []
    else:
        return json.loads(content)


def get_card_name_by_pattern(card_name, pattern):
    return re.findall(pattern, card_name, re.S | re.U)


def fetch_board_by_user():
    url = 'https://api.trello.com/1/members/_USERID_/boards?key=_APP_KEY_&token=_TOKEN_'
    url = basic_replace(url)
    url = url.replace("_USERID_", g_user_id)
    body = do_request(url)
    board_info = {}

    for item in body:
        board_info[item['shortLink']] = item['name']

    return board_info


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


def fetch_cards_by_list_id(list_id):
    url = 'https://api.trello.com/1/lists/_LISTID_/cards?key=_APP_KEY_&token=_TOKEN_'
    url = basic_replace(url)
    url = url.replace("_LISTID_", list_id)
    body = do_request(url)

    return body


def get_cards_info(list_id, board_members):
    available_cards_info = []

    all_cards_info = fetch_cards_by_list_id(list_id)

    for item in all_cards_info:
        card_info = {
            'id': item['id'],
            'card_name': item['name'],
            'member_id': None,
            'member_name': None,
            'label_id': None,
            'label_name': None,
            'plan_hours': 0,
            'actual_hours': 0
        }

        idMembers = item['idMembers']
        if len(idMembers) > 0 and idMembers[0] is not None:
            member_id = idMembers[0]
            card_info['member_id'] = member_id
            card_info['member_name'] = board_members[member_id]

        labels = item['labels']
        if len(labels) > 0 and labels[0] is not None:
            label = labels[0]
            card_info['label_id'] = label['id']
            card_info['label_name'] = label['name']

        card_hours = get_card_name_by_pattern(item['name'], workload_pattern)
        card_info['plan_hours'] = float(card_hours[0]) if len(card_hours) > 0 else 0
        card_info['actual_hours'] = float(card_hours[1]) if len(card_hours) > 1 else card_info['plan_hours']

        available_cards_info.append(card_info)

    return available_cards_info


def groupby_label(label_stat, card_info):
    label_name = card_info['label_name']
    actual_hours = card_info['actual_hours']

    if label_name is not None and label_name != 'null':
        label_name.replace(' ', '')
        if label_name in label_stat:
            label_stat[label_name] += actual_hours
        else:
            label_stat[label_name] = actual_hours


def groupby_requirement(requirement_stat, card_name, hours):
    requirement_name = get_card_name_by_pattern(card_name, requirement_pattern)

    if len(requirement_name) > 0:
        if requirement_name[0] in requirement_stat:
            requirement_stat[requirement_name[0]] += hours
        else:
            requirement_stat[requirement_name[0]] = hours


def groupby_author(members_info, card_info):
    member_id = card_info['member_id']
    label_name = card_info['label_name']

    if member_id in members_info:
        if label_name == '新增' or label_name == '紧急':
            members_info[member_id]['new_work_hours'] += card_info['actual_hours']
        else:
            members_info[member_id]['plan_hours'] += card_info['plan_hours']
            members_info[member_id]['actual_hours'] += card_info['actual_hours']
    else:
        if label_name == '新增' or label_name == '紧急':
            members_info[member_id] = {
                'member_name': card_info['member_name'],
                'plan_hours': 0,
                'actual_hours': 0,
                'new_work_hours': card_info['actual_hours']
            }
        else:
            members_info[member_id] = {
                'member_name': card_info['member_name'],
                'plan_hours': card_info['plan_hours'],
                'actual_hours': card_info['actual_hours'],
                'new_work_hours': 0
            }


def build_members_stat(members_info):
    member_stat = {}
    members_info_keys = members_info.keys()

    for member_id in members_info_keys:
        member_name = members_info[member_id]['member_name']
        member_stat[member_name] = members_info[member_id]
        del(member_stat[member_name]['member_name'])

    return member_stat


def sum_workloads(all_cards_info, action, board_name):
    workloads = {
        'card_stat': {'总预估工时': 0, '无预估工时卡片数': 0},
        'label_stat': {},
        'member_stat': {},
        'requirement_stat': {}
    }
    members_info = {}

    for card_id in all_cards_info.keys():
        plan_hours = all_cards_info[card_id]['plan_hours']
        if plan_hours > 0:
            hours = float(plan_hours)
            workloads['card_stat']['总预估工时'] += hours
            groupby_label(workloads['label_stat'], all_cards_info[card_id])
            groupby_requirement(workloads['requirement_stat'], all_cards_info[card_id]['card_name'], hours)
        else:
            workloads['card_stat']['无预估工时卡片数'] += 1

        groupby_author(members_info, all_cards_info[card_id])

    if action == "new_card_stat":
        members_info = build_new_card_stat(all_cards_info, board_name)

    workloads['member_stat'] = build_members_stat(members_info)

    if len(workloads['requirement_stat']) == 0:
        workloads['equirement_stat'] = {'requirement': 0}

    return workloads


def show(board_name, list_name, workloads):
    origin = sys.stdout
    file = codecs.open('data/task_stat.txt', 'w', encoding='utf-8')
    sys.stdout = file

    print("[", board_name + "：" + list_name, "]")
    print("总计：", workloads['card_stat'])
    print("标签：", workloads['label_stat'])
    print("成员：", workloads['member_stat'])
    print("需求：", workloads['requirement_stat'])

    sys.stdout = origin
    file.close()


def cardinfo_turn_to_dict(all_cards_info):
    cards_info = {}

    for card_info in all_cards_info:
        card_id = card_info['id']
        cards_info[card_id] = card_info
        del (cards_info[card_id]['id'])

    return cards_info


def save_cardinfo_to_json(cards_dict, board_name, action):
    if action == "new_iteration":
        cards_info = {card_id: cards_dict[card_id] for card_id in cards_dict if
                           re.search("^DOING|^TODO", cards_dict[card_id]['list_name'])}
        file_name = "data/iteration-snapshot-"
    elif action == "daily_cards":
        cards_info = {card_id: cards_dict[card_id] for card_id in cards_dict if
                                re.search("^DOING|^TODO|^DONE$", cards_dict[card_id]['list_name'])}
        file_name = "data/daily-"

    try:
        with open(file_name + board_name + '-' + datetime.now().date().isoformat() + '.txt', 'w', encoding='utf-8') as f:
            json.dump(cards_info, f)
        print('save cards success')
    except IOError as e:
        print('write cards_info error: ' + str(e))
        sys.exit(-1)


def generate_member_stat_from_cards_info(cards_info):
    member_stat = {}

    all_labels = list(set([value['label_name'] for value in cards_info.values()]))

    for card_id in cards_info:
        member_stat[cards_info[card_id]['member_id']] = {
                                                            'member_name': cards_info[card_id]['member_name'],
                                                            'plan_hours': 0,
                                                            'actual_hours': 0,
                                                            'new_work_hours': 0,
                                                            'new_work_label': {label: 0 for label in all_labels}
                                                         }

    return member_stat


def build_new_card_stat(cards_info, board_name):
    cards_info_keys = cards_info.keys()
    new_cards_info = {}

    member_stat = generate_member_stat_from_cards_info(cards_info)

    # file_name = sorted(glob.glob("data/iteration-snapshot-" + board_name + "-*.txt"))[-1]
    file_name = sorted(glob.glob("data/daily-" + board_name + "-*.txt"))[-1]
    print('compare the file with：' + file_name)

    try:
        with open(file_name, 'r') as f:
            snapshot_cards_info = json.load(f)
    except IOError as e:
        print('read cards_info error: ' + str(e))
        sys.exit(-1)

    for card_id in cards_info_keys:
        member_id = cards_info[card_id]['member_id']
        card_info = cards_info[card_id]

        if card_id not in snapshot_cards_info.keys():
            member_stat[member_id]['new_work_hours'] += card_info['actual_hours']

            if u'新增' in str(card_info['label_name']):
                member_stat[member_id]['new_work_label'][card_info['label_name']] += card_info['actual_hours']
        else:
            member_stat[member_id]['plan_hours'] += card_info['plan_hours']
            member_stat[member_id]['actual_hours'] += card_info['actual_hours']

    return member_stat


def compute_list(board_name, list_name, action):
    cards_list = []
    lists_name = []
    board_members = fetch_members_by_board()

    card_id_list = fetch_list_id_by_board(list_name)

    for i, card_list in enumerate(card_id_list):
        print("\rfetching card info %d/%d" % (i+1, len(card_id_list)), end='', flush=True)
        cards_info = get_cards_info(card_list['id'], board_members)
        [h.update({'list_name': card_list['name']}) for h in cards_info]
        cards_list.extend(cards_info)
        lists_name.append(card_list['name'])

    print("")
    list_name = " & ".join(lists_name)

    if len(cards_list):
        cards_dict = cardinfo_turn_to_dict(cards_list)

        if action == "new_iteration" or action == "daily_cards":
            save_cardinfo_to_json(cards_dict, board_name, action)
        else:
            workloads = sum_workloads(cards_dict, action, board_name)
            show(board_name, list_name, workloads)
            chartstat.draw_bar_chart(workloads)
            # sendemail.send_email(board_name, g_sender, g_receiver, g_username, g_password)
    else:
        print('The list is empty！')


def set_board_info():
    global g_board_id
    action = ""
    list_name = "^TODO|^DOING$|^DONE$"
    board_info = fetch_board_by_user()

    if len(sys.argv) == 2:
        print(board_info)
        g_board_id = input("please input a board_id：")

        if sys.argv[1] == 'board':
            list_name = input("please input a list name：").upper()
        elif sys.argv[1] == 'new_iteration':
            list_name = "^TODO|^DOING$"
            action = "new_iteration"
        elif sys.argv[1] == 'daily_cards':
            list_name = "^TODO|^DOING$"
            action = "daily_cards"
        elif sys.argv[1] == 'new_card_stat':
            list_name = "^TODO|^DOING$|^DONE$"
            action = "new_card_stat"

    board_name = board_info[g_board_id]
    compute_list(board_name, list_name, action)


def main():
    read_config("./config.json")
    set_board_info()

if __name__ == '__main__':
    main()

# vim: set expandtab tabstop=4 shiftwidth=4 foldmethod=marker:

