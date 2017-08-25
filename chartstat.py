#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt


def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')
        rect.set_edgecolor('white')


def column_graphs(workloads):
    member_name = []
    plan_hours = []
    actual_hours = []
    new_work_hours = []
    n_groups = len(workloads['member_stat'])

    for member_stat in workloads['member_stat']:
        member_name.append(member_stat['member_name'])
        plan_hours.append(member_stat['plan_hours'])
        actual_hours.append(member_stat['actual_hours'])
        new_work_hours.append(member_stat['new_work_hours'])

    member_name = tuple(member_name)
    means_plan_hours = tuple(plan_hours)
    means_actual_hours = tuple(actual_hours)
    means_new_work_hours = tuple(new_work_hours)

    index = np.arange(n_groups)
    bar_width = 0.3

    opacity = 0.85
    rects_plan_hours = plt.bar(index, means_plan_hours, bar_width, alpha=opacity, color='#4783c1', label='plan_hours')
    rects_actual_hours = plt.bar(index + bar_width, means_actual_hours, bar_width, alpha=opacity, color='#c45247', label='actual_hours')
    rects_new_hours = plt.bar(index + 2*bar_width, means_new_work_hours, bar_width, alpha=opacity, color='#9bbd4f',
                                 label='new_work_hours')

    plt.xlabel('member_name')
    plt.ylabel('hours')
    plt.title('work hours by members')
    plt.xticks(index + bar_width, member_name)
    plt.ylim(0, 40)
    plt.legend()

    add_labels(rects_plan_hours)
    add_labels(rects_actual_hours)
    add_labels(rects_new_hours)

    plt.tight_layout()
    # plt.savefig('work_hours_chart.png')
    plt.show()
