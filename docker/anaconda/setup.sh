#!/bin/bash

service cron start
crontab crontab.txt

wget "http://file.learn-x.com/simhei.ttf" -O /tmp/simhei.ttf

if [ ! -f /opt/conda/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/simhei.ttf ];
then
    cp /tmp/simhei.ttf /opt/conda/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/
fi

if [ ! -f /opt/conda/pkgs/matplotlib-2.0.2-np112py36_0/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/simhei.ttf ];
then
    ln /opt/conda/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/simhei.ttf /opt/conda/pkgs/matplotlib-2.0.2-np112py36_0/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/
fi

python3 ./check_plot.py
