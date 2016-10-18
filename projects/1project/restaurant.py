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
def extract_author_ngrams(reviews, low, high):
    ngram_counts = defaultdict(int)

    for r in reviews:
        text = ' '.join(r.paragraphs)
        tokens = word_tokenize(text)
        words = [t for t in tokens if t not in PUNCTUATION]
        for n in range(low, high + 1):
            all_ngrams = ngrams(words, n)
            for gram in all_ngrams:
                ngram_counts[gram] += 1
    return ngram_counts

def exercise4(dataset):
    n_low = 1
    n_high = 2

    LOGGER.info('Building datasets...')
    # Build Training Set
    train_author_reviews = defaultdict(list)
    for review in dataset.get_training():
        train_author_reviews[review.author].append(review)
    # Build Testing Set
    test_author_reviews = defaultdict(list)
    for review in dataset.get_testing():
        test_author_reviews[review.author].append(review)

    LOGGER.info('Building features...')
    # Build Training Features
    train_author_ngrams = []
    for author in train_author_reviews:
        counts = extract_author_ngrams(train_author_reviews[author], n_low, n_high)
        train_author_ngrams.append((counts, author))
    # Build Testing Features
    test_author_ngrams = []
    for author in test_author_reviews:
        counts = extract_author_ngrams(test_author_reviews[author], n_low, n_high)
        test_author_ngrams.append((counts, author))
    LOGGER.info('Building classifier...')
    classifier = nltk.NaiveBayesClassifier.train(train_author_ngrams)
    print("Accuracy: ", nltk.classify.accuracy(classifier, test_author_ngrams))
    return

def main():
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()
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
