# Jeff McGovern
# CPE 582-01
# Lab 1: BKL Chapter 4, Exercise 10
# Friday, October 7, 2016, 11:30 PM

import os
import sys

# Write a program to sort words by length. Define a helper function cmp_len
# which uses the cmp comparison function on word lengths.

import nltk
from nltk.corpus import webtext
from nltk.tokenize import word_tokenize
from nltk.tokenize import regexp_tokenize
import random
from pprint import pprint
from collections import defaultdict

ARB_NUM = 50
CORPUS = webtext
TEXT = word_tokenize(CORPUS.raw(random.choice(CORPUS.fileids())))
SENTS = CORPUS.sents(random.choice(CORPUS.fileids()))

def cmp_len(a, b):
    # There is no cmp function in Python3:
    # https://docs.python.org/3.0/whatsnew/3.0.html 
    # Here is the idiom suggested: (If you really need the cmp() functionality,
    # you could use the expression (a > b) - (a < b) as the equivalent for
    # cmp(a, b).)
    return (len(a) > len(b)) - (len(a) < len(b))

def main():
    assert(cmp_len('one', 'two') == 0)
    assert(cmp_len('one', 'three') < 0)
    assert(cmp_len('nine', 'ten') > 0)
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
