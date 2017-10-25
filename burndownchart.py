#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import utils


def draw_burn_down_chart(daily_stat):
    utils.setup_font()
    # print(daily_stat)
    iteration_date = [str(daily_stat[i].keys())[12:-3] for i in range(len(daily_stat))]
    total_actual_hours = []
    working_actual_hours = []
    working_plan_hours = []
    new_hours = []
    new_working_hours = []
    in_daily_working_actual_hours = []

    for i in range(len(daily_stat)):
        total_actual_hours.append(daily_stat[i][iteration_date[i]]['total_actual_hours'])
        working_actual_hours.append(daily_stat[i][iteration_date[i]]['working_actual_hours'])
        working_plan_hours.append(daily_stat[i][iteration_date[i]]['working_plan_hours'])
        new_hours.append(-daily_stat[i][iteration_date[i]]['new_hours'])
        new_working_hours.append(daily_stat[i][iteration_date[i]]['new_working_hours'])
        in_daily_working_actual_hours.append(daily_stat[0][iteration_date[0]]['working_actual_hours'] -
                                            daily_stat[i][iteration_date[i]]['in_daily_working_actual_hours'])

    in_daily_working_actual_hours[0] = 0

    print('\n------------> Show the work hours list:')
    print(' 总实际+新增工作时长：' + str(total_actual_hours))
    print(' 未完成实际工作时长： ' + str(working_actual_hours))
    print(' 未完成计划工作时长： ' + str(working_plan_hours))
    print(' 新增未完成工作时长： ' + str(new_working_hours))
    print(' 总新增工作时长：     ' + str(new_hours))
    print(' !new实际工时偏离度： ' + str(in_daily_working_actual_hours))

    x_date = np.arange(len(iteration_date))
    plt.plot(x_date, total_actual_hours, marker='.', label='总实际+新增工作时长')
    plt.plot(x_date, working_plan_hours, marker='.', label='未完成计划工作时长')
    plt.plot(x_date, working_actual_hours, marker='.', label='未完成实际工作时长')

    plt.bar(x_date + 0.15, new_working_hours, 0.3, alpha=0.85, color='#4783c1', label='新增未完成工作时长')
    plt.bar(x_date + 0.15, new_hours, 0.3, alpha=0.85, color='#c45247', label='总新增工作时长')
    plt.bar(x_date - 0.15, in_daily_working_actual_hours, 0.3, alpha=0.85, color='#61A0A8', label='非新增实际工时偏离度')

    plt.xlabel('date')
    plt.ylabel('hours')
    plt.title('燃尽图')
    plt.subplots_adjust(bottom=0)
    # plt.xticks(x_date, iteration_date, rotation=40)
    hours_max_index = total_actual_hours.index(max(total_actual_hours))
    hours_min_index = new_hours.index(min(new_hours))
    plt.ylim(new_hours[hours_min_index], total_actual_hours[hours_max_index] + total_actual_hours[hours_max_index]*0.8)
    plt.legend(loc='best', fontsize=8)

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 0))
    ax.set_xticks(x_date)
    ax.set_xticklabels(iteration_date, rotation=35)

    plt.grid(ls='dashed', dash_joinstyle='round', color='#cccccc')
    plt.tight_layout()
    plt.savefig('img/burn_down_chart.png')
    print('\n------------> Save the burn down chart successfully.')
    # plt.show()
