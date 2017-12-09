#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import bayesian_filter.word as word
from sklearn.grid_search import GridSearchCV


def get_best_params(x_train, y_train):
    tuned_parameters = [{'alpha': [0.01, 0.1, 1]}]
    scores = ['r2']

    for score in scores:
        clf = GridSearchCV(MultinomialNB(), tuned_parameters, cv=5, scoring=score)
        clf.fit(x_train, y_train)
        print(clf.best_estimator_)

        for params, mean_score, scores in clf.grid_scores_:
            print("%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() / 2, params))

    return clf.best_estimator_


def text_filter_for_sklearn(train_line, train_labels, test_line, test_labels):
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

    clf = get_best_params(x_train, y_train)
    clf.fit(x_train, y_train)
    predict = clf.predict(x_test)
    # print(test_line)
    # print(predict)

    score = accuracy_score(y_test, predict)
    print('\nprecision_score:' + str(score))


if __name__ == '__main__':
    train_line, train_labels = word.word_process("../filter_data/train/")
    test_line, test_labels = word.word_process("../filter_data/test/")

    text_filter_for_sklearn(train_line, train_labels, test_line, test_labels)
