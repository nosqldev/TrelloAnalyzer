#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import utils


def draw_burn_down_chart(daily_stat):
    utils.setup_font()
    print(daily_stat)
    iteration_date = [str(daily_stat[i].keys())[12:-3] for i in range(len(daily_stat))]
    print(iteration_date)
    total_actual_hours = []
    working_actual_hours = []
    working_plan_hours = []
    new_hours = []
    new_working_hours = []

    for i in range(len(daily_stat)):
        total_actual_hours.append(daily_stat[i][iteration_date[i]]['total_actual_hours'])
        working_actual_hours.append(daily_stat[i][iteration_date[i]]['working_actual_hours'])
        working_plan_hours.append(daily_stat[i][iteration_date[i]]['working_plan_hours'])
        new_hours.append(-daily_stat[i][iteration_date[i]]['new_hours'])
        new_working_hours.append(daily_stat[i][iteration_date[i]]['new_working_hours'])
    print(total_actual_hours)
    print(working_actual_hours)
    print(working_plan_hours)
    print(new_working_hours)
    print(new_hours)

    x_date = range(len(iteration_date))
    plt.plot(x_date, total_actual_hours, marker='.', label='total_actual_hours')
    plt.plot(x_date, working_plan_hours, marker='.', label='working_plan_hours')
    plt.plot(x_date, working_actual_hours, marker='.', label='working_actual_hours')

    plt.bar(x_date, new_working_hours, 0.3, alpha=0.85, color='#4783c1', label='new_working_hours')
    plt.bar(x_date, new_hours, 0.3, alpha=0.85, color='#c45247', label='new_hours')

    plt.xlabel('date')
    plt.ylabel('hours')
    plt.title('燃尽图')
    # plt.margins(0)
    plt.subplots_adjust(bottom=0)
    plt.xticks(x_date, iteration_date, rotation=40)
    hours_max_index = working_plan_hours.index(max(working_plan_hours))
    hours_min_index = new_hours.index(min(new_hours))
    plt.ylim(new_hours[hours_min_index], working_plan_hours[hours_max_index] + 100)
    plt.legend(loc='best', fontsize=10)

    plt.grid(ls='dashed', dash_joinstyle='round', color='#cccccc')
    plt.tight_layout()
    plt.savefig('img/burn_down_chart.png')
    plt.show()
