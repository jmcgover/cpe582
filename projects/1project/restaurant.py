# Jeff McGovern
# CPE 582-01
# Project 1: Restaurant Reviews
# Monday, October 7, 2016, 11:30 PM

# File System
import os
import stat

# Custom Classes
from review import *

# System
import sys
import errno
from argparse import ArgumentParser

# Standard
import math

# Logging
import logging
LOGGER = logging.getLogger(__name__)
HANDLER = logging.StreamHandler()
HANDLER.setFormatter(logging.Formatter('%(levelname)s:%(message)s'))
LOGGER.addHandler(HANDLER)
LOGGER.setLevel(logging.CRITICAL)
logging.captureWarnings(True)

# Natual Language Processing
import nltk
from nltk.tokenize import word_tokenize
from nltk import ngrams
from nltk import FreqDist
from nltk import ConfusionMatrix
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
from pprint import pformat
import re

# Maths
import random
from collections import defaultdict
import string

DESCRIPTION = """Machine learning algorithms to predict paragraph rating and topic, overall rating, and authorship of restaurant reviews written by students in CPE 582 Fall 2016. Written by Jeff McGovern (jmcgover@calpoly.edu)."""
def get_arg_parser():
    parser = ArgumentParser(prog=sys.argv[0], description=DESCRIPTION)
    parser.add_argument('data_dir',
            metavar='DATA_DIR', 
            help='path (absolute or relative) to the data directory')
    parser.add_argument('-d', '--debug',
            action='store_true', default=False,
            help='enters debug logging mode, adding details to the log message')
    parser.add_argument('-i', '--info',
            action='store_true', default=False,
            help='enters info logging mode')
    parser.add_argument('-q', '--quiet',
            action='store_true', default=False,
            help='quiets output for Review* tests')
    parser.add_argument('-c', '--confusion',
            action='store_true', default=False,
            help='outputs the confusion matrix')
    parser.add_argument('-t', '--test',
            nargs = '?',
            help='test the review parsing of a single file')
    return parser

def enter_debug_mode():
    verbose_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s:%(funcName)s:%(lineno)s:%(levelname)s:%(message)s')
    verbose_handler.setFormatter(formatter)
    LOGGER.removeHandler(HANDLER)
    LOGGER.addHandler(verbose_handler)
    LOGGER.setLevel(logging.DEBUG)

PUNCTUATION = set(string.punctuation)
def extract_ngrams(text,
        low = 1, high = 2,
        lowercase = False,
        filter_punctuation = True,
        binary = False,
        least_common = None,
        most_common = None,
        normalize = False,
        sample = False):
    #text = ' '.join(review.paragraphs)
    tokens = None

    # Make lowercase
    if lowercase:
        tokens = word_tokenize(text.lower())
    else:
        tokens = word_tokenize(text)

    # Remove Punctuation
    if filter_punctuation:
        words = [t for t in tokens if t not in PUNCTUATION]
    else:
        words = [t for t in tokens]

    # Do the N Gram Thing
    ngram_counts = {}
    assert not (sample and binary), "Please don't make sample and binary True. One or the other or neither pls"
    for n in range(low, high + 1):
        ngram_freqdist = FreqDist(ngrams(words, n))
        grams_to_consider = ngram_freqdist
        if least_common:
            assert least_common > 0.0 and least_common <= 1.0, \
                    'Least common must be a proportion, not %.3f' % least_common
            num_least_common = int(least_common * ngram_freqdist.N())
            grams_to_consider = []
            for bleh in ngram_freqdist.most_common()[-1 * num_least_common:]:
                gram, count = bleh
                grams_to_consider.append(gram)
        for gram in grams_to_consider:
            if sample:
                ngram_counts[gram] = ngram_freqdist.freq(gram)
            elif binary:
                ngram_counts[gram] = True
            else:
                ngram_counts[gram] = ngram_freqdist[gram]
    if normalize:
        total_counts = sum(count for ngram, count in ngram_counts.items())
        for gram, count in ngram_counts.items():
            ngram_counts[gram] = count / total_counts
    return ngram_counts

sia = SentimentIntensityAnalyzer()
def extract_sentiment(text):
    return sia.polarity_scores(text)

def extract_pos(text):

    return

def extract_features1(paragraph):
    features = {}

    # SENTIMENT
    sentiments = extract_sentiment(paragraph)
    for type, sentiment in sentiments.items():
        features['sentiment' + type] = sentiment
    return features

    # NGRAM
    ngram_features = extract_ngrams(paragraph, 
            low=1, high=5,
            lowercase = False)
    for key in ngram_features:
        features[key] = ngram_features[key]
    return features

def extract_features2(review):
    features = {}

    # SENTIMENT
    sentiments = extract_sentiment(' '.join(review.paragraphs))
    for type, sentiment in sentiments.items():
        features['sentiment' + type] = sentiment
    return features

    # NGRAM
    ngram_features = extract_ngrams(' '.join(review.paragraphs),
            low=1, high=5,
            lowercase = True, binary = False, normalize = False)
    for key in ngram_features:
        features[key] = ngram_features[key]
    return features

    # SENTIMENT PER PARAGRAPH
    para_sentiments = []
    for p in review.paragraphs:
        para_sentiments.append(extract_sentiment(p))
    for i, para_sent in enumerate(para_sentiments):
        for type, sentiment in para_sent.items():
            features['paragraph_' + str(i) + '_sentiment_' + type] = sentiment
    return features


def extract_features3(review):
    features = {}

    # OTHER RATINGS
    for type, rating in zip(ALL_RATING_STR[:OVERALL_NDX], review.ratings[:OVERALL_NDX]):
        features[type] = rating
    return features

    # NGRAMS
    ngram_features = extract_ngrams(' '.join(review.paragraphs), lowercase = False)
    for key in ngram_features:
        features[key] = ngram_features[key]
    return features

    # SENTIMENT
    sentiments = extract_sentiment(' '.join(review.paragraphs))
    for type, sentiment in sentiments.items():
        features['sentiment' + type] = sentiment
    return features

def extract_features4(review):
    features = {}
    # NGRAMS
    ngram_features = extract_ngrams(' '.join(review.paragraphs), lowercase = False, least_common = 0.50)
    for key in ngram_features:
        features[key] = ngram_features[key]
    return features

# EXERCISE 1
def exercise1(dataset, runs = 5, test_portion = 0.50):

    LOGGER.info('Building datasets...')
    # Build Test and Training Review Sets
    test_reviews = None
    train_reviews = None
    predetermined = None
    accuracies = []
    for n in range(runs):
        if dataset.test and dataset.train:
            test_reviews = dataset.test
            train_reviews = dataset.train
            predetermined = True
        else:
            test_reviews, train_reviews = dataset.make_test_train(test_portion)
            predetermined = False
        if not predetermined:
            LOGGER.info('Run %d of %d', n + 1, runs)

        LOGGER.info('Building paragraphs...')
        test_paras = []
        for r in test_reviews:
            test_paras.extend((para, rating) for para, rating in zip(r.paragraphs, r.ratings))
        train_paras = []
        for r in train_reviews:
            train_paras.extend((para, rating) for para, rating in zip(r.paragraphs, r.ratings))

        LOGGER.info('Building features...')
        # Build Features
        test_features  = [(extract_features1(para), "GOOD" if rating >= 4 else "BAD")
                for para, rating in test_paras]
        train_features = [(extract_features1(para), "GOOD" if rating >= 4 else "BAD")
                for para, rating in train_paras]

        LOGGER.info('Building classifier...')
        # Build Classifier
        LOGGER.info('Training Examples: %d', len(train_reviews))
        LOGGER.info('Training Features: %d', len(train_features))
        classifier = nltk.NaiveBayesClassifier.train(train_features)
        #classifier = nltk.DecisionTreeClassifier.train(train_features)

        LOGGER.info('Checking accuracy...')
        # Perform Classification
        classifications = []
        for t in test_features:
            classifications.append((t[1], classifier.classify(t[0])))

        LOGGER.info('Printing results...')
        classifications.sort()
        if not predetermined:
            # Print Everything
            HEADER = ('ACTUAL', 'CLASSIFIED')
            col_width = max(len(a) for a,c in (classifications + [HEADER]))
            for a,c in ([HEADER] + classifications):
                print("Exercise 1: %s %s" % (a.ljust(col_width), c))
        accuracy = nltk.classify.accuracy(classifier, test_features)
        print("Exercise 1: %.3f" % (accuracy,))
        if predetermined:
            return accuracy
        else:
            LOGGER.info('Predetermined:%s',predetermined)
            accuracies.append(accuracy)
    print("Exercise 1: Runs: %d Average: %.3f Max: %.3f Min: %.3f" %
            (runs, sum(accuracies) / len(accuracies), max(accuracies), min(accuracies)))
    return accuracies

# EXERCISE 2
def exercise2(dataset, runs = 5, test_portion = 0.50):

    LOGGER.info('Building datasets...')
    # Build Test and Training Review Sets
    test_reviews = None
    train_reviews = None
    predetermined = None
    accuracies = []
    for n in range(runs):
        if dataset.test and dataset.train:
            test_reviews = dataset.test
            train_reviews = dataset.train
            predetermined = True
        else:
            test_reviews, train_reviews = dataset.make_author_test_train(test_portion)
            predetermined = False
        if not predetermined:
            LOGGER.info('Run %d of %d', n + 1, runs)

        LOGGER.info('Building features...')
        # Build Features
        test_features  = [(extract_features2(r), "GOOD" if r.ratings[OVERALL_NDX] >= 4 else "BAD")
                for r in test_reviews]
        train_features = [(extract_features2(r), "GOOD" if r.ratings[OVERALL_NDX] >= 4 else "BAD")
                for r in train_reviews]

        LOGGER.info('Building classifier...')
        # Build Classifier
        LOGGER.info('Training Examples: %d', len(train_reviews))
        LOGGER.info('Training Features: %d', len(train_features))
        classifier = nltk.NaiveBayesClassifier.train(train_features)
        #classifier = nltk.DecisionTreeClassifier.train(train_features)

        LOGGER.info('Checking accuracy...')
        # Perform Classification
        classifications = []
        for t in test_features:
            classifications.append((t[1], classifier.classify(t[0])))

        LOGGER.info('Printing results...')
        classifications.sort()
        if not predetermined:
            # Print Everything
            HEADER = ('ACTUAL', 'CLASSIFIED')
            col_width = max(len(a) for a,c in (classifications + [HEADER]))
            for a,c in ([HEADER] + classifications):
                print("Exercise 2: %s %s" % (a.ljust(col_width), c))
        accuracy = nltk.classify.accuracy(classifier, test_features)
        print("Exercise 2: %.3f" % (accuracy,))
        if predetermined:
            return accuracy
        else:
            LOGGER.info('Predetermined:%s',predetermined)
            accuracies.append(accuracy)
    print("Exercise 2: Runs: %d Average: %.3f Max: %.3f Min: %.3f" %
            (runs, sum(accuracies) / len(accuracies), max(accuracies), min(accuracies)))
    return accuracies

# EXERCISE 3
def exercise3(dataset, runs = 5, test_portion = 0.50):

    LOGGER.info('Building datasets...')
    # Build Test and Training Review Sets
    test_reviews = None
    train_reviews = None
    predetermined = None
    accuracies = []
    for n in range(runs):
        if dataset.test and dataset.train:
            test_reviews = dataset.test
            train_reviews = dataset.train
            predetermined = True
        else:
            test_reviews, train_reviews = dataset.make_test_train(test_portion)
            predetermined = False
        if not predetermined:
            LOGGER.info('Run %d of %d', n + 1, runs)

        LOGGER.info('Building features...')
        # Build Features
        test_features  = [(extract_features3(r), str(r.ratings[OVERALL_NDX]))
                for r in test_reviews]
        train_features = [(extract_features3(r), str(r.ratings[OVERALL_NDX]))
                for r in train_reviews]

        LOGGER.info('Building classifier...')
        # Build Classifier
        LOGGER.info('Training Examples: %d', len(train_reviews))
        LOGGER.info('Training Features: %d', len(train_features))
        classifier = nltk.NaiveBayesClassifier.train(train_features)
        #classifier = nltk.DecisionTreeClassifier.train(train_features)

        LOGGER.info('Checking accuracy...')
        # Perform Classification
        classifications = []
        for t in test_features:
            classifications.append((t[1], classifier.classify(t[0])))

        LOGGER.info('Printing results...')
        classifications.sort()
        if not predetermined:
            # Print Everything
            HEADER = ('ACTUAL', 'CLASSIFIED')
            col_width = max(len(a) for a,c in (classifications + [HEADER]))
            for a,c in ([HEADER] + classifications):
                print("Exercise 3: %s %s" % (a.ljust(col_width), c))
        accuracy = math.sqrt(sum((y - y_t) * (y - y_t)
                for y, y_t in [(int(a), int(c)) for a,c in classifications]) / len(classifications))
        print("Exercise 3: %.3f" % (accuracy,))
        if predetermined:
            return accuracy
        else:
            LOGGER.info('Predetermined:%s',predetermined)
            accuracies.append(accuracy)
    print("Exercise 3: Runs: %d Average Accuracy: %.3f Max: %.3f Min: %.3f" %
            (runs, sum(accuracies) / len(accuracies), max(accuracies), min(accuracies)))
    return accuracies

# EXERCISE 4
def exercise4(dataset, runs = 5, test_portion = 0.50):

    LOGGER.info('Building datasets...')
    # Build Test and Training Review Sets
    test_reviews = None
    train_reviews = None
    predetermined = None
    overall_classifications = []
    accuracies = []
    rmses = []
    for n in range(runs):
        if dataset.test and dataset.train:
            test_reviews = dataset.test
            train_reviews = dataset.train
            predetermined = True
        else:
            test_reviews, train_reviews = dataset.make_author_test_train(test_portion)
            predetermined = False
        if not predetermined:
            LOGGER.info('Run %d of %d', n + 1, runs)

        LOGGER.info('Building features...')
        # Build Features
        test_features  = [(extract_features4(r), r.author)
                for r in test_reviews]
        train_features = [(extract_features4(r), r.author)
                for r in train_reviews]

        LOGGER.info('Building classifier...')
        # Build Classifier
        LOGGER.info('Training Examples: %d', len(train_reviews))
        LOGGER.info('Training Features: %d', len(train_features))
        classifier = nltk.NaiveBayesClassifier.train(train_features)
        #classifier = nltk.DecisionTreeClassifier.train(train_features)

        LOGGER.info('Checking accuracy...')
        # Perform Classification
        classifications = []
        for t in test_features:
            classifications.append((t[1], classifier.classify(t[0])))

        LOGGER.info('Printing results...')
        classifications.sort()
        accuracy = nltk.classify.accuracy(classifier, test_features)
        rmse = math.sqrt(sum(1 for a,c in classifications if a != c) / len(classifications))
        confusion = ConfusionMatrix(
                [ref for ref, test in classifications],
                [test for ref, test in classifications])
        overall_classifications.extend(classifications)
        if not predetermined:
            HEADER = ('ACTUAL', 'CLASSIFIED')
            col_width = max(len(a) for a,c in (classifications + [HEADER]))
            for a,c in ([HEADER] + classifications):
                print("Exercise 4: %s %s" % (a.ljust(col_width), c))
        print("Exercise 4: %.3f" % (accuracy,))
        print("Exercise 4: Average RMSE Error: %.3f" % (rmse,))

        if predetermined:
            return accuracy
        print('Exercise 4: Confusion Matrix:\n%s' % (
            confusion.pretty_format(show_percents = False, values_in_chart = True),))
        accuracies.append(accuracy)
        rmses.append(rmse)
    overall_confusion = ConfusionMatrix(
            [ref for ref, test in overall_classifications],
            [test for ref, test in overall_classifications])
    print('Exercise 4: Overall Confusion Matrix:\n%s' % (
        overall_confusion.pretty_format(show_percents = False, values_in_chart = True),))
    print("Exercise 4: Runs: %d Average     : %.3f Max: %.3f Min: %.3f" %
            (runs, sum(accuracies) / len(accuracies), max(accuracies), min(accuracies)))
    print("Exercise 4: Runs: %d Average RMSE: %.3f Max: %.3f Min: %.3f" %
            (runs, sum(rmses) / len(rmses), max(rmses), min(rmses)))
    return accuracies

def main():
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()
    LOGGER.setLevel(logging.CRITICAL)
    if args.info == True:
        LOGGER.setLevel(logging.INFO)
    if args.debug == True:
        enter_debug_mode()
    data_dir = args.data_dir
    if args.test:
        LOGGER.info('Looking for paths containing %s in %s', args.test, data_dir)
        filenames = ReviewDataset.get_lowest_filenames(data_dir)
        relevant = [name for name in filenames if args.test.lower() in name.lower()]
        LOGGER.info('Found:%s', pformat(relevant))
        reviews = [Review(name) for name in relevant]
        for r in reviews:
            [LOGGER.info('%s:%d:%s',r.path,i,p) for i,p in enumerate(r.all_paras)]
    else:
        dataset = ReviewDataset(data_dir)
        exercise1(dataset)
        exercise2(dataset)
        exercise3(dataset, runs = 10)
        exercise4(dataset)
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
