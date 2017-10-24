#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bayesian_filter.word as word
import os


def get_test_words():
    test_words_list = []
    test_dict_list = []
    root_path = "../filter_data/test/"
    file_list = os.listdir(root_path)
    test_file = os.path.join(root_path, file_list[0])
    file = open(test_file)

    while 1:
        line = file.readline()
        if not line:
            break
        word_processed = word.file_word_process(line)
        test_words_list.append(word_processed)

    for i in range(len(test_words_list)):
        test_dict_list.append(word.add_to_dict(test_words_list[i]))

    return test_dict_list


def get_interesting_words(test_dict):
    word_prob_list = {}
    pw_dict = {}
    category_words_dict = word.get_category_dict()
    category_list = list(category_words_dict.keys())

    for words in test_dict.keys():
        pw_dict = {'depend_third': 0.01, 'online_prob': 0.01, 'requirement': 0.01, 'tech': 0.01}
        for category_name in category_list:
            if words in category_words_dict[category_name].keys():
                pw = category_words_dict[category_name][words]/len(category_words_dict[category_name])
                pw_dict[category_name] = pw
        word_prob_list[words] = pw_dict.copy()

    print(word_prob_list)


def main():
    test_dict_list = get_test_words()

    # for i in range(len(test_dict_list)):
    get_interesting_words(test_dict_list[1])


if __name__ == '__main__':
    main()
