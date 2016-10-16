# Jeff McGovern
# CPE 582-01
# Project 1: Restaurant Reviews
# Monday, October 7, 2016, 11:30 PM

# File System
import os
import stat

# System
import sys
import errno
from argparse import ArgumentParser

# Logging
import logging
LOGGER = logging.getLogger('__main__')

# Natual Language Processing
import nltk
from bs4 import BeautifulSoup
from pprint import pformat
import re

# Maths
import random

class Review(object):
    FOOD_STR    = 'FOOD'
    VENUE_STR   = 'VENUE'
    SERVICE_STR = 'SERVICE'
    OVERALL_STR = 'OVERALL'
    FOOD_NDX    = 0
    VENUE_NDX   = 1
    SERVICE_NDX = 2
    OVERALL_NDX = 3

    def __init__(self, filename):
        self.path = filename
        self.author = None
        self.restaurant = None
        self.address = None
        self.city = None
        self.paragraphs = []
        self.ratings = []
        self.raw = None

        # Open and Parse
        soup = None
        LOGGER.debug("Opening %s...", filename)
        with open(filename, 'r') as file:
            LOGGER.debug("BeautifulSouping...")
            soup = BeautifulSoup(file, 'lxml')
        LOGGER.debug('Prettifying...')
        self.raw = soup.prettify()
        LOGGER.debug('Getting paragraphs...')
        self.paras = soup.find_all('p')
        self.newlines = soup.find_all('br')
        return
    def __str__(self):
        return self.raw

class ReviewDataset(object):
    TEST_DIR = 'test'
    TRAIN_DIR = 'training'
    REVIEW_DIR = 'Review[123]';
    REVIEW_DIR_REGEX = re.compile(REVIEW_DIR)
    DIR_REGEX = re.compile('{}|{}|{}'.format(TEST_DIR, TRAIN_DIR, REVIEW_DIR))

    def __init__(self, dir_path, training_portion = 0.30):
        self.test = set()
        self.train = set()
        # Validate and extract dirs
        folders = ReviewDataset.extract_dirs(dir_path)
        LOGGER.debug('DISCOVERED FOLDERS:{}'.format(folders))
        filenames = {}
        for folder in folders:
            filenames[folder] = ReviewDataset.get_lowest_filenames(folder)
        LOGGER.debug('DISCOVERED FILES:{}'.format(pformat(filenames)))
        all_reviews = []
        reviews = {}
        for folder in filenames:
            new_reviews = ReviewDataset.build_reviews(filenames[folder])
            all_reviews.extend(new_reviews)
            reviews[folder] = new_reviews
        for review in sorted(all_reviews, key=lambda x: len(x.paras), reverse = True):
            paragraphs = review.paras
            LOGGER.debug('%2d: %s', len(paragraphs), review.path)
            for i, p in enumerate(paragraphs):
                LOGGER.debug('%d:%s', i, p.raw)
        LOGGER.debug('Count: %d', len(all_reviews))

    @staticmethod
    def extract_dirs(path):
        """
            Validate the directory exitence and structure

            :param path_string: string path to the directory containin the data
            :type path_string: string

            :return: Path object representing the path of the directory
            :rtype: pathlib.Path
        """

        # Validate Directory
        ReviewDataset.check_dir(path, True)

        # Check Structure
        discovered_dirs = {}
        for filename in os.listdir(path):
            LOGGER.debug(filename)
            subdir_path = os.path.join(path, filename)
            if ReviewDataset.DIR_REGEX.match(filename) and os.path.isdir(subdir_path):
                discovered_dirs[filename] = subdir_path

        test_train_dirs = [discovered_dirs[dir] 
              for dir in (ReviewDataset.TEST_DIR, ReviewDataset.TRAIN_DIR) if dir in discovered_dirs]
        review_dirs = [discovered_dirs[dir] 
              for dir in discovered_dirs if ReviewDataset.REVIEW_DIR_REGEX.match(dir)]
        LOGGER.debug('Test and Training Directories:{}'.format(test_train_dirs))
        LOGGER.debug('Review Directories:{}'.format(review_dirs))
        if all([dir in discovered_dirs for dir in (ReviewDataset.TEST_DIR, ReviewDataset.TRAIN_DIR)]):
            # Test Train
            LOGGER.debug('test and training folder exist')
            return test_train_dirs
        elif len(review_dirs):
            # Reviews
            LOGGER.debug('review folders exist: {}'.format(review_dirs))
            return review_dirs
        else:
            # Nothing is correct
            [check_dir(os.path.join(path, name), False) for name in (TEST_DIR, TRAIN_DIR)]
            LOGGER.error('Could not find any directory of the style \'{}\''.format(REVIEW_DIR))
            sys.exit(errno.ENOTDIR)
        return None

    @staticmethod
    def check_dir(path, exit_program):
        if not os.path.exists(path):
            LOGGER.error("Directory '%s' does not exist", path)
            if exit_program:
                sys.exit(errno.ENOENT)
            else:
                return False
        if not os.path.isdir(path):
            LOGGER.error("Directory '%s' is not a directory", path)
            if exit_program:
                sys.exit(errno.ENOTDIR)
            else:
                return False
        return True

    @staticmethod
    def get_lowest_filenames(dir):
        lowest_files = []
        for root, dirs, filenames in os.walk(str(dir)):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                lowest_files.append(full_path)
        return lowest_files

    @staticmethod
    def build_reviews(filenames):
        reviews = []
        for filename in filenames:
            LOGGER.debug('PARSING:%s', filename)
            try:
                new_review = Review(filename)
                reviews.append(new_review)
            except Exception as e:
                LOGGER.warning('Failed to parse "%s": %s', filename, e)
        return reviews

