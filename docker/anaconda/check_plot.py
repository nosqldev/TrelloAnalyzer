#!/usr/bin/env python3

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

if 'SimHei' in [f.name for f in fm.fontManager.ttflist]:
    print("SimHei.ttf is available")
else:
    print("SimHei.ttf is NOT installed")

mpl.rcParams['font.family'] = 'SimHei'
print(mpl.rcParams['font.family'])
print(mpl.rcParams['font.sans-serif'])

plt.title(u'标题')
plt.text(1, 1, u'这是一段注释')
plt.ylabel(u'Y轴')
plt.plot([1, 2, 3, 4])
plt.savefig("/tmp/plot.jpg")
