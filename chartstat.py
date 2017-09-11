#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'STHeiti'


def add_labels(rects, pos):
    for i, rect in enumerate(rects):
        if rect.get_height() > 0:
            plt.text(rect.get_x() + rect.get_width() / 2, pos[i], rect.get_height(), ha='center', va='bottom')
            rect.set_edgecolor('white')


def draw_bar_chart(workloads):
    member_stat = workloads['member_stat']
    member_name = []
    plan_hours = []
    actual_hours = []
    new_work_hours = []
    n_groups = len(member_stat)
    label_hours = []
    label_names_list = []
    labels = [value['new_work_label'] for value in member_stat.values()]
    label_names = labels[0].keys()
    bar_colors_palette = ["#6E7074", "#61A0A8", "#749F83", "#BDA29A", "#91C7AE", "#91C7AE"]

    for label_name in label_names:
        label_hours.append([label[label_name] for label in labels])
        label_names_list.append(label_name)

    label_hours_tuple = list(map(tuple, label_hours))

    for name in member_stat:
        member_name.append(name)
        plan_hours.append(member_stat[name]['plan_hours'])
        actual_hours.append(member_stat[name]['actual_hours'])
        new_work_hours.append(member_stat[name]['new_work_hours'])

    member_name = tuple(member_name)
    plan_hours = tuple(plan_hours)
    actual_hours = tuple(actual_hours)
    new_work_hours = tuple(new_work_hours)

    index = np.arange(n_groups)
    bar_width = 0.3

    opacity = 0.85
    rects_plan_hours = plt.bar(index - bar_width, plan_hours, bar_width, alpha=opacity, color='#4783c1', label='plan_hours')
    rects_actual_hours = plt.bar(index, actual_hours, bar_width, alpha=opacity, color='#c45247', label='actual_hours')

    for i in range(len(label_hours_tuple)):
        label_hours_tuple[i] = np.array(label_hours_tuple[i])
        rects_new_hours = plt.bar(index + bar_width, label_hours_tuple[i], bar_width, alpha=opacity, color=bar_colors_palette[i],
                                  label=str(label_names_list[i]), bottom=np.sum(label_hours_tuple[0:i], axis=0))
        add_labels(rects_new_hours, np.sum(label_hours_tuple[0:i], axis=0) + label_hours_tuple[i]/2)

    plt.xlabel('member_name')
    plt.ylabel('hours')
    plt.title('work hours by members')
    plt.xticks(index, member_name)
    hours_max_index = actual_hours.index(max(actual_hours))
    plt.ylim(0, actual_hours[hours_max_index] + 40)
    plt.legend(loc='best', fontsize=10)

    add_labels(rects_plan_hours, plan_hours)
    add_labels(rects_actual_hours, actual_hours)

    plt.tight_layout()
    plt.savefig('img/work_hours_chart.png')
    plt.show()
