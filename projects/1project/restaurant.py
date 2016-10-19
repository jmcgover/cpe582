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

# Logging
import logging
LOGGER = logging.getLogger(__name__)
HANDLER = logging.StreamHandler()
HANDLER.setFormatter(logging.Formatter('%(levelname)s:%(message)s'))
LOGGER.addHandler(HANDLER)
LOGGER.setLevel(logging.WARNING)

# Natual Language Processing
import nltk
from nltk.tokenize import word_tokenize
from nltk import ngrams
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
def extract_ngrams(reviews, low, high, lowercase = False):
    ngram_counts = defaultdict(int)

    for review in reviews:
        text = ' '.join(review.paragraphs)
        tokens = None
        if lowercase:
            tokens = word_tokenize(text.lower())
        else:
            tokens = word_tokenize(text)
        words = [t for t in tokens if t not in PUNCTUATION]
        for n in range(low, high + 1):
            all_ngrams = ngrams(words, n)
            for gram in all_ngrams:
                ngram_counts[gram] += 1
    return ngram_counts

def build_ngram_features(all_author_reviews, smooth = False, normalize = False, lowercase = False):
    features = []
    n_low = 1
    n_high = 3
    # Extract N Grams
    for author in all_author_reviews:
        counts = extract_ngrams(all_author_reviews[author], n_low, n_high)
        features.append((counts,author))
    # Simple Laplace Smoothing
    if smooth:
        vocab = set()
        for counts, author in features:
            vocab.add(word for word in counts)
        for counts, author in features:
            for word in vocab:
                if word not in counts:
                    counts[word] = 1
    # Make each count a proportion of all the words of the author
    if normalize:
        for counts, author in features:
            total_words = sum(count for word, count in counts.items())
            for word in vocab:
                counts[word] = counts[word] / total_words
    return features

def build_author_classes(reviews):
    auth_dict = defaultdict(list)
    for r in reviews:
        auth_dict[r.author].append(r)
    return auth_dict

def exercise4(dataset, runs = 5):

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
            test_reviews, train_reviews = dataset.make_test_train(0.25)
            predetermined = False
        if not predetermined:
            LOGGER.setLevel(logging.INFO)
            LOGGER.info('Run %d of %d', n + 1, runs)

        # Build Classes
        test_classes  = build_author_classes(test_reviews)
        train_classes = build_author_classes(train_reviews)

        LOGGER.info('Building features...')

        # Build Features
        test_features = build_ngram_features(test_classes, smooth = True, normalize = True, lowercase = True)
        train_features = build_ngram_features(train_classes, smooth = True, normalize = True, lowercase = True)

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
        # Print Everything
        HEADER = ('ACTUAL', 'CLASSIFIED')
        classifications.sort()
        col_width = max(len(a) for a,c in (classifications + [HEADER]))
        for a,c in ([HEADER] + classifications):
            print("Exercise 4: %s %s" % (a.ljust(col_width), c))
        accuracy = nltk.classify.accuracy(classifier, test_features)
        print("Exercise 4:", accuracy)
        if predetermined:
            return
        else:
            accuracies.append(accuracy)
    print("Exercise 4: Runs: %d Average: %.3f Max: %.3f Min: %.3f" %
            (runs, sum(accuracies) / len(accuracies), max(accuracies), min(accuracies)))
    return

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
        exercise4(dataset)
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
