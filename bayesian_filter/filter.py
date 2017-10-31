#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bayesian_filter.word as word
import os


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


def get_interesting_words(test_dict):
    word_prob_list = {}
    pw_dict = {}
    text_prob_dict = {}
    category_words_dict = word.get_category_dict()
    category_list = list(category_words_dict.keys())

    for words in test_dict.keys():
        for category_name in category_list:
            if words in category_words_dict[category_name].keys():
                pw = category_words_dict[category_name][words]/len(category_words_dict[category_name])
                pw_dict[category_name] = pw
            else:
                pw_dict[category_name] = 0.01
        word_prob_list[words] = pw_dict.copy()

    for category_name in category_list:
        category_prob_list = []
        test_prob = 1.0

        # build a interesting words list for each category
        for words in word_prob_list.keys():
            category_prob_list.append(word_prob_list[words][category_name])

        # Sort the list of category interesting words, return top 3 elements
        category_prob_list = sorted(category_prob_list, reverse=True)[0:3]

        for i in range(len(category_prob_list)):
            test_prob *= category_prob_list[i]

        # if there is no interesting words in this category, assign the category's probability of 0
        if test_prob == 1.0:
            text_prob_dict[category_name] = 0
        else:
            text_prob_dict[category_name] = test_prob

    return text_prob_dict


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

    for i in range(len(test_dict_list)):
        text_prob_dict[test_line[i]] = get_interesting_words(test_dict_list[i])
        text_prob_category[test_line[i]] = text_filter(text_prob_dict[test_line[i]])

    print(text_prob_dict)
    print(text_prob_category)
    print(right_result)

    cal_accuracy(text_prob_category, right_result)


if __name__ == '__main__':
    predictions()
