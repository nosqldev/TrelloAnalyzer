#!/usr/bin/env python3

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

if 'SimHei' in [f.name for f in fm.fontManager.ttflist]:
    print("SimHei.ttf is available")
else:
    print("SimHei.ttf is NOT installed")
