#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt


def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')
        rect.set_edgecolor('white')


def draw_bar_chart(workloads):
    member_stat = workloads['member_stat']
    member_name = []
    plan_hours = []
    actual_hours = []
    new_work_hours = []
    n_groups = len(member_stat)
    label_hours = []
    labels = [value['new_work_label'] for value in member_stat.values()]
    label_names = labels[0].keys()
    bar_colors_palette = ["#61A0A8", "#91C7AE", "#749F83", "#F3F3F3", "#CA8622", "#BDA29A"]

    for label_name in label_names:
        label_hours.append([label[label_name] for label in labels])

    label_hours_tuple = list(map(tuple, label_hours))
    print(label_names)
    print(label_hours_tuple)

    for name in member_stat:
        member_name.append(name)
        plan_hours.append(member_stat[name]['plan_hours'])
        actual_hours.append(member_stat[name]['actual_hours'])
        new_work_hours.append(member_stat[name]['new_work_hours'])


    member_name = tuple(member_name)
    means_plan_hours = tuple(plan_hours)
    means_actual_hours = tuple(actual_hours)
    means_new_work_hours = tuple(new_work_hours)

    index = np.arange(n_groups)
    bar_width = 0.3

    opacity = 0.85
    #for i, label_hour in enumerate(label_hours_tuple):
    #    plt.bar(index + bar_width, label_hours_tuple[label_hour], bar_width, alpha=opacity, color=bar_colors_palette[i])
    rects_plan_hours = plt.bar(index - bar_width, means_plan_hours, bar_width, alpha=opacity, color='#4783c1', label='plan_hours')
    rects_actual_hours = plt.bar(index, means_actual_hours, bar_width, alpha=opacity, color='#c45247', label='actual_hours')

    for i in range(len(label_hours_tuple)):
        label_hours_tuple[i] = np.array(label_hours_tuple[i])
        plt.bar(index + bar_width, label_hours_tuple[i], bar_width, alpha=opacity, color=bar_colors_palette[i],
                bottom=np.sum(label_hours_tuple[0:i], axis=0))

    # plt.bar(index + bar_width, label_hours_tuple[0], bar_width, alpha=opacity, color=bar_colors_palette[3])
    # plt.bar(index + bar_width, label_hours_tuple[1], bar_width, alpha=opacity, color=bar_colors_palette[1],
    #         bottom=np.sum(label_hours_tuple[0], axis=0))
    # rects_new_hours = plt.bar(index + bar_width, label_hours_tuple[2], bar_width, alpha=opacity, color='#9bbd4f',
    #                              label='new_work_hours', bottom=np.sum(label_hours_tuple[0:2], axis=0))

    plt.xlabel('member_name')
    plt.ylabel('hours')
    plt.title('work hours by members')
    plt.xticks(np.arange(5), member_name)
    hours_max_index = actual_hours.index(max(actual_hours))
    plt.ylim(0, actual_hours[hours_max_index] + 20)
    plt.legend(loc='best', fontsize=10)

    add_labels(rects_plan_hours)
    add_labels(rects_actual_hours)
    #add_labels(rects_new_hours)

    plt.tight_layout()
    plt.savefig('img/work_hours_chart.png')
    plt.show()


# if __name__ == '__main__':
#     draw_bar_chart()
#     draw_stacked_bar_chart()

