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
from collections import defaultdict

def str_to_int(x):
    assert isinstance(x, str)
    return int(round(float(x)))
def parse_rating(x):
    assert isinstance(x, str)
    return str_to_int(re.findall('\d+\.{0,1}\d*',x)[0])

# The meat of it all: Parses all the review files
def get_paragraphs(soup, parent_dir):
    # EXTRACT PARAGRAPHS
    paras = []

    # Replace br's
    LOGGER.debug('Replacing br\'s...')
    for br in soup.find_all('br'):
        br.replace_with('\n')

    LOGGER.debug('Getting body...')
    body = soup.find('body')

    # Split by either <p> or <span>
    parent_dir = parent_dir
    raw_paragraphs = []
    LOGGER.debug('Getting paragraphs...')
    if any((
                all(x in parent_dir for x in ('Gavin Scott', 'Review1')),
                all(x in parent_dir for x in ('Daniel Kauffman', 'Review2')),
                all(x in parent_dir for x in ('Daniel Kauffman', 'Review3'))
                )):
        LOGGER.debug('Using <span> on {}...'.format(parent_dir))
        soup_paras = body.find_all('span')
    else:
        LOGGER.debug('Using <p> to parse paragraphs...')
        soup_paras = body.find_all('p')

    if all(x in parent_dir for x in ('Alanna Buss', 'Review2')):
        LOGGER.debug('')
        body_string = str(body)
        LOGGER.debug('BEFORE:{}'.format(body_string))
        for i,p in enumerate(soup_paras):
            LOGGER.debug('PTAG:{}:{}'.format(i,str(p)))
            body_string = body_string.replace(str(p), '')
        body_string = body_string.replace('<body>','<p>')
        body_string = body_string.replace('</body>','</p>')
        LOGGER.debug('AFTER:{}'.format(body_string))
        soup_paras[10] = BeautifulSoup(body_string, 'lxml')

    # Gather text
    if all(x in parent_dir for x in ('Jonathan Sleep', 'Review3')):
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

    # Build list of paragraphs
    LOGGER.debug('RAW_PARAGRAPHS:%s', raw_paragraphs)
    paragraphs = []
    for p in raw_paragraphs:
        if re.findall('WRITTEN REVIEW:[^\n]+\w+',p):
            LOGGER.debug('FOUND:%s', re.findall('WRITTEN REVIEW:[^\n]+\w+',p))
            paragraphs.extend(('WRITTEN REVIEW:', p.replace('WRITTEN REVIEW:', '').strip()))
        else:
            LOGGER.debug('APPENDING RAW:%s', p)
            paragraphs.append(p)
    if any((
                all(x in parent_dir for x in ('Jon Doughty',)),
                all(x in parent_dir for x in ('Joseph Wilson', 'Review1'))
                )):
        LOGGER.debug('Collapsing {}...'.format(parent_dir))
        paras = collapse_paragraphs(paragraphs)
    elif 'Ryan Smith' in parent_dir and 'Review2' in parent_dir:
        LOGGER.debug('Collapsing Ryan\'s Review2 paragraphs, joining without space...')
        paras = collapse_paragraphs(paragraphs, '')
    elif 'Christian Durst' in parent_dir and ('Review3' in parent_dir or 'Review1' in parent_dir):
        LOGGER.debug('Collapsing ALL of Skylar\'s Review3 paragraphs...')
        paras = collapse_paragraphs(paragraphs, all=True)
        if 'Review1' in parent_dir:
            paras = paras[0:8]\
                    + ['WRITTEN REVIEW:']\
                    + [paras[8].replace('WRITTEN REVIEW:','').strip()]\
                    + paras[9:]
    else:
        paras = [p for p in paragraphs if p]

    if all( x in parent_dir for x in ('Justin Postigo', 'Review3')):
        LOGGER.debug('Appending empty paragraph to Justin\'s Review3...')
        paras.append('')
    if all( x in parent_dir for x in ('Jeffrey McGovern',)):
        paras = paras[0:3] \
            + [paras[3].replace(', CA','').replace(', WA','')]\
            + paras[4:]
    if all( x in parent_dir for x in ('Samuel Lakes', 'Review1')):
        paras = paras[0:2] \
            + [paras[2].replace(', San Luis Obispo, CA 93401','')]\
            + paras[3:]
    if all( x in parent_dir for x in ('Samuel Lakes', 'Review2')):
        LOGGER.debug('Fixing CITY in Sam\'s Review2...')
        paras = paras[0:2] \
            + [paras[2].replace(', San Luis Obispo, CA 93405','')]\
            + ['CITY: San Luis Obispo'] \
            + paras[3:]
    if all( x in parent_dir for x in ('Ivan Pachev', 'Review2')):
        LOGGER.debug('Combining some paragraphs of Ivan\'s Review2...')
        paras[11] = ' '.join(paras[11:13])
        paras[12] = ' '.join(paras[14:])
        del paras[13:]
    if 'Christian Durst' in parent_dir:
        paras[0] = 'REVIEWER: Christian Durst'
    if 'Foaad Khosmood' in paras[0]:
        paras[0] = 'REVIEWER: Aditya Budhwar'
    return paras

# Collapses paragraphs with blank lines inside the array
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


# Checks the directory for existence
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


# Builds a list of reviews from a list of filenames
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

# Retrieves the lowest filenames in given directory's directory tree
def get_lowest_filenames(dir):
    lowest_files = []
    for root, dirs, filenames in os.walk(str(dir)):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            lowest_files.append(full_path)
    return lowest_files

# Constants relevant to this project
TEST_DIR = 'test'
TRAIN_DIR = 'training'
REVIEW_DIR = 'Review[123]';
REVIEW_DIR_REGEX = re.compile(REVIEW_DIR)
DIR_REGEX = re.compile('{}|{}|{}'.format(TEST_DIR, TRAIN_DIR, REVIEW_DIR))

# Extracts the directories relevant to this project
def extract_dirs(path):
    """
        Validate the directory exitence and structure

        :param path_string: string path to the directory containin the data
        :type path_string: string

        :return: Path object representing the path of the directory
        :rtype: pathlib.Path
    """

    # Validate Directory
    check_dir(path, True)

    # Check Structure
    discovered_dirs = {}
    for filename in os.listdir(path):
        LOGGER.debug(filename)
        subdir_path = os.path.join(path, filename)
        if DIR_REGEX.match(filename) and os.path.isdir(subdir_path):
            discovered_dirs[filename] = subdir_path

    test_train_dirs = [discovered_dirs[dir] 
          for dir in (TEST_DIR, TRAIN_DIR) if dir in discovered_dirs]
    review_dirs = [discovered_dirs[dir] 
          for dir in discovered_dirs if REVIEW_DIR_REGEX.match(dir)]
    LOGGER.debug('Test and Training Directories:{}'.format(test_train_dirs))
    LOGGER.debug('Review Directories:{}'.format(review_dirs))
    if all([dir in discovered_dirs for dir in (TEST_DIR, TRAIN_DIR)]):
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

# Sanitizes various strings in the reviews
def sanitize_reviews(reviews):
    for review in reviews:
        review.city = review.city.replace(', CA','').replace(', WA','').title()
        review.restaurant = review.restaurant.replace('é','e')
        if review.restaurant == 'chili peppers':
            review.restaurant = 'chillie peppers restaurant'
        if review.restaurant == 'central coasters':
            review.restaurant = 'central coaster'
        if review.restaurant == 'oki momo':
            review.restaurant = 'okimomo asian grill'
        if review.restaurant == 'fatoush':
            review.restaurant = 'fattoush'
        if review.restaurant == 'slo brew':
            review.restaurant = 'slo brewing company'
    return

# Constants relevant to the Review data structure
FOOD_STR    = 'FOOD'
VENUE_STR   = 'VENUE'
SERVICE_STR = 'SERVICE'
OVERALL_STR = 'OVERALL'
RATING_STR  = 'RATING'
FOOD_NDX    = 0
VENUE_NDX   = 1
SERVICE_NDX = 2
OVERALL_NDX = 3
ALL_RATING_STR = (FOOD_STR, VENUE_STR, SERVICE_STR, OVERALL_STR)
class Review(object):
    def __init__(self, path):
        self.path = path

        # Open and BeautifulSoup
        soup = None
        LOGGER.debug("Opening %s...", path)
        with open(path, 'r') as file:
            LOGGER.debug("BeautifulSouping...")
            soup = BeautifulSoup(file, 'lxml')
        self.raw = soup.prettify()

        # Get parent directory to handle specific cases
        self.parent_dir = os.path.dirname(path)

        # Extract Paragraphs
        self.all_paras = get_paragraphs(soup, self.parent_dir)
        self.fill_properties()
        return
    def __str__(self):
        return self.raw
    def fill_properties(self):
        [LOGGER.debug('PARAGRAPH:%d:%s', i, p) for i,p in enumerate(self.all_paras)]
        if len(self.all_paras) != 13:
            LOGGER.error('Parsed %d paragraphs for %s',len(self.all_paras),self.path)
            [LOGGER.error('PARAGRAPH:%d:%s', i, p) for i,p in enumerate(self.all_paras)]
        else:
            LOGGER.debug('Parsed %d paragraphs for %s',len(self.all_paras),self.path)
        assert len(self.all_paras) == 13, 'Received {} paragraphs, need 13'.format(len(self.all_paras))
        self.author = None
        self.restaurant = None
        self.address = None
        self.city = None
        self.paragraphs = self.all_paras[-4:]
        self.ratings = [None] * 4
        LOGGER.debug(self.parent_dir)
        for i,p in enumerate(self.all_paras[:-4]):
            if 'reviewer' in p.lower():
                author = p.replace('REVIEWER','').replace(':','').strip()
                LOGGER.debug('Author: %s', author)
                self.author = author
            if 'name' in p.lower():
                restaurant = p.lower().replace('name','').replace(':','').strip()
                LOGGER.debug('Restaurant: %s', restaurant)
                self.restaurant = restaurant
            if 'address' in p.lower():
                address = p.lower().replace('address','').replace(':','').strip()
                LOGGER.debug('Address: %s', address)
                self.address = address
            if 'city' in p.lower():
                city = p.lower().replace('city','').replace(':','').strip()
                LOGGER.debug('City: %s', self.city)
                self.city = city
            if FOOD_STR in p:
                rating = parse_rating(p)
                LOGGER.debug('Food Rating:%d', rating)
                self.ratings[FOOD_NDX] = rating
            if VENUE_STR in p:
                rating = parse_rating(p)
                LOGGER.debug('Venue Rating:%d', rating)
                self.ratings[VENUE_NDX] = rating
            if SERVICE_STR in p:
                rating = parse_rating(p)
                LOGGER.debug('Service Rating:%d', rating)
                self.ratings[SERVICE_NDX] = rating
            if any(x in p for x in (OVERALL_STR, RATING_STR)):
                rating = parse_rating(p)
                LOGGER.debug('Overall Rating:%d', rating)
                self.ratings[OVERALL_NDX] = rating
        assert self.author, 'No author for %s' % self.path
        assert self.city, 'No city for %s:%s' % (self.path, self.city)
        assert self.address, 'No address for %s:%s' % (self.path, self.address)
        assert self.restaurant, 'No restaurant for %s:%s' % (self.path, self.restaurant)
        for ndx, r in enumerate(self.ratings):
            assert r != None, 'Failed to parse %s rating' % ALL_RATING_STR[ndx]
        return

class ReviewDataset(object):
    def __init__(self, dir_path):
        self.test = None
        self.train = None

        # Validate and extract dirs
        folders = extract_dirs(dir_path)
        LOGGER.debug('DISCOVERED FOLDERS:{}'.format(folders))

        # Extract all filenames
        filenames = {}
        for folder in folders:
            filenames[folder] = get_lowest_filenames(folder)
        LOGGER.debug('DISCOVERED FILES:{}'.format(pformat(filenames)))

        # Build Reviews
        self.all_reviews = []
        self.reviews = {}
        for folder in filenames:
            new_reviews = build_reviews(filenames[folder])
            self.all_reviews.extend(new_reviews)
            self.reviews[folder] = new_reviews

        # Build Test and Training Sets
        if all(x in self.reviews for x in (TEST_DIR, TRAIN_DIR)):
            self.predetermined = True
            self.test = self.reviews[TEST_DIR]
            self.train = self.reviews[TRAIN_DIR]
        else:
            self.test = None
            self.train = None

        # Sanitize Reviews
        sanitize_reviews(self.all_reviews)
        return

    def make_test_train(self, train_portion):
        test = None
        train = None
        shuffled_reviews = self.all_reviews[:]
        random.shuffle(shuffled_reviews)
        test  = shuffled_reviews[:int(train_portion*len(shuffled_reviews))]
        train = shuffled_reviews[int(train_portion*len(shuffled_reviews)):]
        return test, train
