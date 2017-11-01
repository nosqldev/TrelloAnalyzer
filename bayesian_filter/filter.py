#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bayesian_filter.word as word
import os


def show():
    category_words_dict = word.get_category_dict()
    category_list = list(category_words_dict.keys())

    print('训练集中分词总数：')
    for category_name in category_list:
        print(category_name, len(list(category_words_dict[category_name])))
    print('-' * 10)


def get_test_words():
    test_words_list = []
    test_dict_list = []
    test_line = []
    right_result = {}
    root_path = "../filter_data/test/"
    file_list = os.listdir(root_path)

    for file_name in file_list:
        test_file = os.path.join(root_path, file_name)
        file = open(test_file, 'r', encoding='utf-8')

        while 1:
            line = file.readline()
            if not line:
                break
            test_line.append(line)
            right_result[line] = file_name[0:-4]
            word_processed = word.file_word_process(line)
            test_words_list.append(word_processed)

    for i in range(len(test_words_list)):
        test_dict_list.append(word.add_to_dict(test_words_list[i]))

    return test_dict_list, test_line, right_result


def get_interesting_words(test_dict, category_words_dict, count):
    word_frequency_list = {}
    pw_time = {}
    text_prob_dict = {}
    category_list = list(category_words_dict.keys())

    for words in test_dict.keys():
        word_frequency = 0
        for category_name in category_list:
            if words in category_words_dict[category_name].keys():
                word_frequency += category_words_dict[category_name][words]
                pw_time[category_name] = word_frequency
            else:
                pw_time[category_name] = 0
        word_frequency_list[words] = pw_time.copy()

    for category_name in category_list:
        text_frequency = 0
        for words in word_frequency_list.keys():
            if word_frequency_list[words][category_name] is not None:
                text_frequency += word_frequency_list[words][category_name]
        if text_frequency != 0:
            text_prob_dict[category_name] = text_frequency / len(category_words_dict[category_name])
            # text_prob_dict[category_name] = text_frequency / count[category_name]
        else:
            text_prob_dict[category_name] = 0

    return text_prob_dict


def cal_bayes(text_prob_dict):
    ps_category = 0
    text_prob = {}

    for category_name in text_prob_dict.keys():
        ps_category += text_prob_dict[category_name]

    for category_name in text_prob_dict.keys():
        if ps_category != 0:
            text_prob[category_name] = text_prob_dict[category_name] / ps_category
        else:
            text_prob[category_name] = 0

    return text_prob


def text_filter(text_prob_dict):
    text_prob_category_name = ''
    text_prob_value = sorted((text_prob_dict[category_name] for category_name in text_prob_dict.keys()), reverse=True)[0]

    for category_name in text_prob_dict.keys():
        if text_prob_value == text_prob_dict[category_name]:
            text_prob_category_name = category_name

    return text_prob_category_name


def cal_accuracy(text_prob_category, right_result):
    right_count = 0
    error_count = 0

    for name in text_prob_category.keys():
        if text_prob_category[name] == right_result[name]:
            right_count += 1
        else:
            error_count += 1

    print('rightCount:', right_count)
    print('errorCount:', error_count)
    print('Prediction accuracy:', right_count/(right_count+error_count))

    return right_count/(right_count+error_count)


def predictions():
    test_dict_list, test_line, right_result = get_test_words()
    text_prob_dict = {}
    text_prob_category = {}
    category_words_dict = word.get_category_dict()
    count = {}

    for category_name in category_words_dict.keys():
        n = 0
        for words in category_words_dict[category_name]:
            n += category_words_dict[category_name][words]
        count[category_name] = n

    for i in range(len(test_dict_list)):
        text_prob_dict[test_line[i]] = cal_bayes(get_interesting_words(test_dict_list[i], category_words_dict, count))
        text_prob_category[test_line[i]] = text_filter(text_prob_dict[test_line[i]])

    print('分类概率：')
    print(text_prob_dict)
    print('预测分类：')
    print(text_prob_category)
    print('正确分类：')
    print(right_result)

    cal_accuracy(text_prob_category, right_result)


if __name__ == '__main__':
    show()
    predictions()

