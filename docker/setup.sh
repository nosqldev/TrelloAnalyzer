#!/bin/sh

if [ ! -f $ANACONDAPATH/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/simhei.ttf ];
then
    cp /tmp/simhei.ttf $ANACONDAPATH/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/
fi

if [ ! -f $ANACONDAPATH/pkgs/matplotlib-2.0.2-np112py36_0/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/simhei.ttf ];
then
    ln $ANACONDAPATH/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/simhei.ttf $ANACONDAPATH/pkgs/matplotlib-2.0.2-np112py36_0/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/
fi

python3 ./check_plot.py
