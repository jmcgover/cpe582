# Jeff McGovern
# CPE 582-01
# Lab 2
# Monday, October 24, 2016, 11:55 PM

import sys
import os

import nltk
from pprint import pprint

def main():
    print('Grabbing tagged Text...')
    tagged_text = nltk.corpus.brown.tagged_words()
    tag_set = set()
    print('Finding unique tags...')
    [tag_set.add(tag) for word, tag in tagged_text]
    print('Printing %d tags...' % (len(tag_set),))
    pprint(sorted([t for t in tag_set]))
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
