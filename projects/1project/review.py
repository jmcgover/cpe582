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

        # Open and BeautifulSoup
        soup = None
        LOGGER.debug("Opening %s...", filename)
        with open(filename, 'r') as file:
            LOGGER.debug("BeautifulSouping...")
            soup = BeautifulSoup(file, 'lxml')

        # EXTRACT PARAGRAPHS
        LOGGER.debug('Replacing br\'s...')
        for br in soup.find_all('br'):
            br.replace_with('\n')

        LOGGER.debug('Getting body...')
        body = soup.find('body')

        raw_paragraphs = []
        LOGGER.debug('Getting paragraphs...')
        if 'Gavin Scott' in self.path and 'Review1' in self.path:
            LOGGER.debug('Using <span> on Gavin\'s Review1...')
            soup_paras = body.find_all('span')
        elif 'Daniel Kauffman' in self.path and 'Review2' in self.path:
            LOGGER.debug('Using <span> on Daniel\'s Review2...')
            soup_paras = body.find_all('span')
        elif 'Daniel Kauffman' in self.path and 'Review3' in self.path:
            LOGGER.debug('Using <span> on Daniel\'s Review3...')
            soup_paras = body.find_all('span')
        else:
            LOGGER.debug('Using <p> to parse paragraphs...')
            soup_paras = body.find_all('p')
        if 'Jonathan Sleep' in self.path and 'Review3' in self.path:
            for p in soup_paras:
                LOGGER.debug('Found a paragraph...')
                raw_paragraphs.append(p.get_text())
        else:
            if soup_paras:
                for p in soup_paras:
                    LOGGER.debug('Found a paragraph...')
                    raw_paragraphs.extend(p.get_text().split('\n'))
            else:
                LOGGER.debug('Could not find paragraphs...')
                raw_paragraphs.extend(body.get_text().split('\n'))
        LOGGER.debug('RAW_PARAGRAPHS:%s', raw_paragraphs)
        paragraphs = []
        for p in raw_paragraphs:
            if re.findall('WRITTEN REVIEW:[^\n]+\w+',p):
                LOGGER.debug('FOUND:%s', re.findall('WRITTEN REVIEW:[^\n]+\w+',p))
                paragraphs.extend(('WRITTEN REVIEW:', p.replace('WRITTEN REVIEW:', '').strip()))
            else:
                LOGGER.debug('APPENDING RAW:%s', p)
                paragraphs.append(p)
        if 'Jon Doughty' in self.path:
            LOGGER.debug('Collapsing Jon\'s paragraphs...')
            self.paras = Review.collapse_paragraphs(paragraphs)
        elif 'Christian Durst' in self.path and 'Review1' in self.path:
            LOGGER.debug('Collapsing Skylar\'s Review1 paragraphs...')
            self.paras = Review.collapse_paragraphs(paragraphs)
        elif 'Joseph Wilson' in self.path and 'Review1' in self.path:
            LOGGER.debug('Collapsing Joey\'s Review1 paragraphs...')
            self.paras = Review.collapse_paragraphs(paragraphs)
        elif 'Ryan Smith' in self.path and 'Review2' in self.path:
            LOGGER.debug('Collapsing Ryan\'s Review2 paragraphs...')
            self.paras = Review.collapse_paragraphs(paragraphs, '')
        elif 'Christian Durst' in self.path and 'Review3' in self.path:
            LOGGER.debug('Collapsing Skylar\'s Review3 paragraphs...')
            self.paras = Review.collapse_paragraphs(paragraphs, all=True)
        else:
            self.paras = [p for p in paragraphs if p]

        if 'Justin Postigo' in self.path and 'Review3' in self.path:
            LOGGER.debug('Appending empty paragraph to Justin\'s Review3...')
            self.paras.append('')
        if 'Samuel Lakes' in self.path and 'Review2' in self.path:
            LOGGER.debug('Fixing CITY in Sam\'s Review2...')
            self.paras = self.paras[0:2] \
                + [self.paras[2].replace(', San Luis Obispo, CA 93405','')]\
                + ['CITY: San Luis Obispo'] \
                + self.paras[3:]
        if 'Ivan Pachev' in self.path and 'Review2' in self.path:
            LOGGER.debug('Combining some paragraphs of Ivan\'s Review2...')
            self.paras[11] = ' '.join(self.paras[11:13])
            self.paras[12] = ' '.join(self.paras[14:])
            del self.paras[13:]


        LOGGER.debug('Prettifying...')
        self.raw = soup.prettify()
        LOGGER.debug('PRETTY:%s', self.raw)
        [LOGGER.debug('PARAGRAPH:%d:%s', i, p) for i,p in enumerate(self.paras)]
        if len(self.paras) != 13:
            LOGGER.error('Parsed %d paragraphs for %s',len(self.paras),self.path)
            [LOGGER.error('PARAGRAPH:%d:%s', i, p) for i,p in enumerate(self.paras)]
        else:
            LOGGER.debug('Parsed %d paragraphs for %s',len(self.paras),self.path)
        assert(len(self.paras) == 13)
        return
    def __str__(self):
        return self.raw
    @staticmethod
    def collapse_paragraphs(paragraphs, text_delimiter = ' ', all=False):
        collapsed_paras = []
        if all:
            LOGGER.debug('Collapsing all...')
            review_para = ''
            for j in range(len(paragraphs)):
                LOGGER.debug('INSPECTING:%d:%s',j,paragraphs[j])
                if paragraphs[j]:
                    review_para += paragraphs[j] + text_delimiter
                elif review_para:
                    LOGGER.debug('ADDING:%s', review_para)
                    collapsed_paras.append(review_para)
                    review_para = ''
                else:
                    LOGGER.debug('SKIPPING:%s', paragraphs[j])
            if review_para:
                collapsed_paras.append(review_para)
        else:
            for i,p in enumerate(paragraphs):
                LOGGER.debug('%d:%s',i,p)
                if 'WRITTEN REVIEW' in p:
                    collapsed_paras.append(p)
                    review_para = ''
                    for j in range(i + 1, len(paragraphs)):
                        LOGGER.debug('INSPECTING:%d:%s',j,paragraphs[j])
                        if paragraphs[j]:
                            review_para += paragraphs[j] + text_delimiter
                        elif review_para:
                            LOGGER.debug('ADDING:%s', review_para)
                            collapsed_paras.append(review_para)
                            review_para = ''
                        else:
                            LOGGER.debug('SKIPPING:%s', paragraphs[j])
                    if review_para:
                        collapsed_paras.append(review_para)
                    break
                elif p:
                    collapsed_paras.append(p)
        if len(collapsed_paras) > 13:
            collapsed_paras[12] = ''.join(collapsed_paras[12:])
            del collapsed_paras[13:]
        return collapsed_paras

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
        for review in sorted(all_reviews, reverse=True, key=lambda x: len(x.paras)):
            LOGGER.debug('%s PARAGRAPHS: %d', review.path, len(review.paras))
            [LOGGER.debug('%d:%s', i, para) for i,para in enumerate(review.paras)]
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


