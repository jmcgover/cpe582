# Jeff McGovern
# CPE 582-01
# Lab 1: BKL Chapter 4, Exercise 18
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
import textwrap

ARB_NUM = 50
CORPUS = webtext
RAW_TEXT = CORPUS.raw(random.choice(CORPUS.fileids()))
TEXT = word_tokenize(RAW_TEXT)
SENTS = CORPUS.sents(random.choice(CORPUS.fileids()))

def insert(trie, key, value):
    if key:
        first, rest = key[0], key[1:]
        if first not in trie:
            trie[first] = {}
        insert(trie[first], rest, value)
    else:
        trie['value'] = value

def main():
   trie = {}
   insert(trie, 'chat', 'cat')
   insert(trie, 'chien', 'dog')
   insert(trie, 'chair', 'flesh')
   insert(trie, 'chic', 'stylish')
   pprint(trie, width=40)
   return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)

