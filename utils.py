#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import matplotlib.font_manager as fm
import matplotlib


def setup_font():
    if "STHeiti" in [f.name for f in fm.fontManager.ttflist]:
        matplotlib.rcParams['font.family'] = 'STHeiti'
    elif "SimHei" in [f.name for f in fm.fontManager.ttflist]:
        matplotlib.rcParams['font.family'] = 'SimHei'
    else:
        print("No suitable font found")
    matplotlib.rcParams['axes.unicode_minus'] = False


def read_cardinfo_from_json(file_name):
    #print('Read the file with：' + file_name)

    try:
        with open(file_name, 'r') as f:
            snapshot_cards_info = json.load(f)
    except IOError as e:
        print('read cards_info error: ' + str(e))
        sys.exit(-1)

    return snapshot_cards_info
