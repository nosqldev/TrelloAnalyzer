#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import jieba


def get_stop_words():
    stop_list = []
    for line in open('../filter_data/stopwords.txt', 'r', encoding='utf-8'):
        stop_list.append(line[:len(line)-1])

    return stop_list


def file_word_process(contents):
    words_list = []
    stop_list = get_stop_words()
    contents = re.sub(r'\s+', '', contents)
    contents = re.sub(r'\n+', '', contents)
    contents = re.sub(r'\t+', '', contents)
    contents = re.sub(r'(\d+(?:\.\d+)?)\s*[hHdD]', '', contents)

    for seg in jieba.cut(contents):
        if seg not in stop_list:
            if seg != ' ':
                words_list.append(seg)

    return words_list


def get_category_data():
    words_list = []
    category_list = []
    root_path = "../filter_data/train/"
    category = os.listdir(root_path)

    for category_name in category:
        category_file = os.path.join(root_path, category_name)
        contents = open(category_file, encoding='utf-8').read()
        word_processed = file_word_process(contents)
        words_list.append(word_processed)
        category_list.append(category_name[:-4])

    return category_list, words_list


def add_to_dict(words_list):
    words_dict = {}

    for item in words_list:
        if item in words_dict.keys():
            words_dict[item] += 1
        else:
            words_dict.setdefault(item, 1)

    return words_dict


def get_category_dict():
    category_words_dict = {}
    category_list, words_list = get_category_data()

    for i, category_name in enumerate(category_list):
        words_dict = add_to_dict(words_list[i])
        category_words_dict[category_name] = words_dict.copy()
        words_dict.clear()

    return category_words_dict
