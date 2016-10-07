#! /usr/bin/env python3

# CPE 582 Fall 2016
# Jeff McGovern - jmcgover@calpoly.edu

# SYSTEM
import errno
import os
import sys

# LOGGING
import logging
LOGGER = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

# AGGREGATE TYPES
import collections
from collections import defaultdict

# HTML PARSING


def main():
    return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
