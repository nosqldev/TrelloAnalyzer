#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import glob
import utils
import burndownchart


def glob_file_name(board_name):
    iteration_snapshot_filename = sorted(glob.glob("data/iteration-snapshot-" + board_name + "-*.txt"))
    if len(iteration_snapshot_filename) > 0:
        iteration_snapshot_filename = iteration_snapshot_filename[-1]
    else:
        print("open data/iteration-snapshot-" + board_name + "-*.txt failed")
        sys.exit(-1)

    begin_date = iteration_snapshot_filename[-14:-4]
    daily_file_names = glob.glob("data/daily-" + board_name + "-*.txt")

    daily_file_names = sorted(list(filter(lambda x: x[-14:-4] > begin_date, daily_file_names)))

    if len(daily_file_names) == 0:
        print("\n There is no daily file larger than the iteration's file date, failed to generate burn down chart.")
        sys.exit(-1)

    return iteration_snapshot_filename, daily_file_names


def batch_read_cardinfo_from_json(file_names):
    daily_card_list = []

    for file_name in file_names:
        daily_card_list.append(utils.read_cardinfo_from_json(file_name))

    return daily_card_list


def do_compute_begin_day(iteration_cards):
    daily_info = {
        'working_plan_hours': 0,
        'working_actual_hours': 0,
        'done_plan_hours': 0,
        'done_actual_hours': 0,
        'new_hours': 0,
        'new_working_hours': 0,
        'total_actual_hours': 0,
        'in_daily_working_actual_hours': 0
    }

    for card_key in iteration_cards:
        daily_info['working_plan_hours'] += iteration_cards[card_key]['plan_hours']
        daily_info['working_actual_hours'] += iteration_cards[card_key]['actual_hours']

    daily_info['total_actual_hours'] = daily_info['working_actual_hours']

    return daily_info


def do_compute_daily_stat(iteration_cards_id, daily_cards):
    daily_info = {
        'working_plan_hours': 0,  # TodoList ＋ DoingList 任务计划耗时
        'working_actual_hours': 0,  # TodoList ＋ DoingList 任务实际耗时
        'done_plan_hours': 0,  # DoneList 中所有卡片的计划耗时
        'done_actual_hours': 0,  # DoneList 中所有卡片的实际耗时
        'new_hours': 0,             # TodoList + DoingList + DoneList 所有新增卡片的实际耗时
        'new_working_hours': 0,     # TodoList + DoingList 所有新增卡片的实际耗时
        'total_actual_hours': 0,     # TodoList + DoingList 所有现有卡片和新增卡片的实际耗时
        'in_daily_working_actual_hours': 0
    }

    for daily_card_key in daily_cards.keys():
        if daily_card_key in iteration_cards_id:
            if re.search("^TODO|^DOING$", daily_cards[daily_card_key]['list_name'], re.I):
                daily_info['working_plan_hours'] += daily_cards[daily_card_key]['plan_hours']
                daily_info['working_actual_hours'] += daily_cards[daily_card_key]['actual_hours']
            elif re.search("^DONE$", daily_cards[daily_card_key]['list_name'], re.I):
                daily_info['done_plan_hours'] += daily_cards[daily_card_key]['plan_hours']
                daily_info['done_actual_hours'] += daily_cards[daily_card_key]['actual_hours']

            daily_info['in_daily_working_actual_hours'] += daily_cards[daily_card_key]['actual_hours']

        else:
            daily_info['new_hours'] += daily_cards[daily_card_key]['actual_hours']

            if re.search("^TODO|^DOING$", daily_cards[daily_card_key]['list_name'], re.I):
                daily_info['new_working_hours'] += daily_cards[daily_card_key]['actual_hours']

    daily_info['total_actual_hours'] = daily_info['working_actual_hours'] + daily_info['new_hours']

    return daily_info


def compute_daily_stat(iteration_card_info, daily_card_list, daily_file_names):
    iteration_cards_id = set(iteration_card_info.keys())
    daily_stat = []
    daily_stat.append({'begin_day': do_compute_begin_day(iteration_card_info)})

    for i, daily_cards in enumerate(daily_card_list):
        daily_stat_value = do_compute_daily_stat(iteration_cards_id, daily_cards)
        daily_stat.append({daily_file_names[i][-14:-4]: daily_stat_value})

    return daily_stat


def build_burn_down_chart(board_name):
    print('\n------------> Build burn down data...')
    iteration_snapshot_filename, daily_file_names = glob_file_name(board_name)
    iteration_card_info = utils.read_cardinfo_from_json(iteration_snapshot_filename)
    daily_card_list = batch_read_cardinfo_from_json(daily_file_names)
    daily_stat = compute_daily_stat(iteration_card_info, daily_card_list, daily_file_names)
    burndownchart.draw_burn_down_chart(daily_stat)
