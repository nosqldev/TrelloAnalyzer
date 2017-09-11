#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

