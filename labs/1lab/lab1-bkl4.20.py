# Jeff McGovern
# CPE 582-01
# Lab 1: BKL Chapter 4, Exercise 19
# Friday, October 7, 2016, 11:30 PM

import os
import sys

# Write a program to sort words by length. Define a helper function cmp_len
# which uses the cmp comparison function on word lengths.

import nltk
from nltk.corpus import webtext
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.tokenize import regexp_tokenize
import random
from pprint import pprint
from collections import defaultdict
import textwrap

ARB_NUM = 50
CORPUS = webtext
RAW_TEXT = CORPUS.raw(random.choice(CORPUS.fileids()))
TEXT = word_tokenize(RAW_TEXT)
SENTS = CORPUS.sents(random.choice(CORPUS.fileids()))

def main():
    test_words = TEXT
    pprint(test_words[:17])
    word_counts = defaultdict(int)
    for word in test_words:
        word_counts[word] += 1
    sorted_words = sorted([word for word in word_counts], key=lambda x: word_counts[x], reverse = True)
    for w in sorted_words[:17]:
        print('"{}":{}'.format(w, word_counts[w]))
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)

