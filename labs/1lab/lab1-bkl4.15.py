# Jeff McGovern
# CPE 582-01
# Lab 1: BKL Chapter 4, Exercise 15
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

TAIL_PROPORTION = 0.10
REGEX_WORDS = r'\w+'
def count_words_in_sentence(sent):
   word_counts = defaultdict(int)
   words = regexp_tokenize(sent, REGEX_WORDS)
   for word in words:
      word_counts[word.lower()] += 1
   return word_counts

SENT = "The quick brown fox jumps over the lazy dog."
def main():
   word_counts = count_words_in_sentence(SENT)
   for word in sorted(word_counts):
      print(word, ":", word_counts[word])
   return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)

