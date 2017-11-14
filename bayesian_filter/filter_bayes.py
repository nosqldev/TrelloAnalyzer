#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import bayesian_filter.word as word
import os
import re
import jieba


def file_word_process(train_path):
    word_line = []
    word_label = []
    stop_list = word.get_stop_words()
    file_list = os.listdir(train_path)
    for i, file_name in enumerate(file_list):
        train_file = os.path.join(train_path, file_name)
        file = open(train_file, 'r', encoding='utf-8')

        while 1:
            line = file.readline()

            if not line:
                break
            line = re.sub(r'[^\u4e00-\u9fa5]', '', line)
            line_fenci = jieba.cut(line)
            line_fenci_stop = []
            for seg in line_fenci:
                if seg not in stop_list:
                    if seg != ' ':
                        line_fenci_stop.append(seg)
            line_fenci_str = str(list(line_fenci_stop))[1:-1]
            word_line.append(line_fenci_str)
            word_label.append(i)
    return word_line, word_label


def text_filter_for_sklearn():
    train_line, train_labels = file_word_process("../filter_data/train/")
    test_line, test_labels = file_word_process("../filter_data/test/")
    count_v0 = CountVectorizer()
    count_v0.fit_transform(train_line)
    count_v1 = CountVectorizer(vocabulary=count_v0.vocabulary_)
    counts_train = count_v1.fit_transform(train_line)
    print('the shape of train is ' + repr(counts_train.shape))

    count_v2 = CountVectorizer(vocabulary=count_v0.vocabulary_)
    counts_test = count_v2.fit_transform(test_line)
    print('the shape of test is ' + repr(counts_test.shape))

    tfidftransformer = TfidfTransformer()
    train_data = tfidftransformer.fit(counts_train).transform(counts_train)
    test_data = tfidftransformer.fit(counts_test).transform(counts_test)

    x_train = train_data
    y_train = train_labels
    x_test = test_data
    y_test = test_labels

    clf = MultinomialNB(alpha=0.1)
    clf.fit(x_train, y_train)
    preds = clf.predict(x_test)
    # print(preds)

    return preds, y_test


def predictions():
    preds, y_test = text_filter_for_sklearn()
    num = 0

    for i, pred in enumerate(preds.tolist()):
        if int(pred) == int(y_test[i]):
            num += 1
    print('precision_score:' + str(float(num) / len(preds)))


if __name__ == '__main__':
    predictions()
