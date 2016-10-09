# Jeff McGovern
# CPE 582-01
# Project 1: Restaurant Reviews
# Monday, October 7, 2016, 11:30 PM

# File System
import os
import stat
from pathlib import Path

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
from bs4 import BeautifulSoup
from pprint import pprint

# Maths
import random

DESCRIPTION = """Machine learning algorithms to predict paragraph rating and topic, overall rating, and authorship of restaurant reviews written by students in CPE 582 Fall 2016. Written by Jeff McGovern (jmcgover@calpoly.edu)."""
def get_arg_parser():
    parser = ArgumentParser(prog=sys.argv[0], description=DESCRIPTION)
    parser.add_argument('data_dir',
            metavar='DATA_DIR', 
            help='path (absolute or relative) to the data directory')
    parser.add_argument('-d', '--debug',
            action='store_true', default=False,
            help='enters debug logging mode, adding details to the log message')
    return parser

def enter_debug_mode():
    verbose_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s:%(funcName)s:%(levelname)s:%(message)s')
    verbose_handler.setFormatter(formatter)
    LOGGER.removeHandler(HANDLER)
    LOGGER.addHandler(verbose_handler)
    LOGGER.setLevel(logging.DEBUG)

TEST_DIR = 'test'
TRAIN_DIR = 'training'
EXPECTED_DIRS_TEST_TRAIN = (TEST_DIR, TRAIN_DIR)
EXPECTED_DIRS_REVIEW = ('Review1', 'Review2', 'Review3')
def extract_dirs(path_string):
    """
        Validate the directory exitence and structure

        :param path_string: string path to the directory containin the data
        :type path_string: string

        :return: Path object representing the path of the directory
        :rtype: pathlib.Path
    """

    # Python3's OO way of using paths
    path = Path(path_string)

    # Validate Directory
    check_dir(path, True)

    # Check Structure
    test_train_dirs = {}
    review_dirs = {}
    for file in path.iterdir():
        if file.name in EXPECTED_DIRS_TEST_TRAIN and file.is_dir():
            test_train_dirs[file.name] = file
        if file.name in EXPECTED_DIRS_REVIEW and file.is_dir():
            review_dirs[file.name] = file

    if all([dir in test_train_dirs for dir in EXPECTED_DIRS_TEST_TRAIN]):
        # Test Train
        LOGGER.debug('test and training folder exist')
        return [v for k,v in test_train_dirs.items()]
    elif all([dir in review_dirs for dir in EXPECTED_DIRS_REVIEW]):
        # Reviews
        LOGGER.debug('all review folders exist')
        return [v for k,v in review_dirs.items()]
    else:
        # Nothing is correct
        [check_dir(path / name, False) for name in EXPECTED_DIRS_TEST_TRAIN]
        [check_dir(path / name, False) for name in EXPECTED_DIRS_REVIEW]
        sys.exit(errno.ENOTDIR)
    return None

def check_dir(path, exit_program):
    if not path.exists():
        LOGGER.error("Directory '%s' does not exist", path)
        if exit_program:
            sys.exit(errno.ENOENT)
        else:
            return False
    if not path.is_dir():
        LOGGER.error("Directory '%s' is not a directory", path)
        if exit_program:
            sys.exit(errno.ENOTDIR)
        else:
            return False
    return True

def get_lowest_files(dir):
    lowest_files = []
    for root, dirs, files in os.walk(str(dir)):
        for file in files:
            full_path = os.path.join(root, file)
            lowest_files.append(Path(full_path))
    return lowest_files

def build_datasets(path_string):
    # Validate and extract dirs
    folders = extract_dirs(path_string)
    files = {}
    for folder in folders:
        files[folder.name] = get_lowest_files(folder)
    pprint(folders)
    all_files = []
    for folder in files:
        all_files.extend(files[folder])
    pprint(all_files)
    for filepath in all_files:
        if 'McGovern' in str(filepath):
            soup = None
            with filepath.open() as file:
                soup = BeautifulSoup(file, 'lxml')
            print(soup.prettify())
            print(soup.text)
    soup = None
    with random.choice(all_files).open() as file:
        soup = BeautifulSoup(file, 'lxml')
    print(soup.prettify())
    print('*' * 40)
    print(soup.text)
    return


def main():
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()
    if args.debug == True:
        enter_debug_mode()
    data_dir = args.data_dir
    result = build_datasets(data_dir)
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
