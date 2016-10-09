# Jeff McGovern
# CPE 582-01
# Lab 1: BKL Chapter 4, Exercise 14
# Friday, October 7, 2016, 11:30 PM

import os
import sys

# Write a program to sort words by length. Define a helper function cmp_len
# which uses the cmp comparison function on word lengths.

import nltk
from nltk.corpus import webtext
from nltk.tokenize import word_tokenize
import random
from pprint import pprint

ARB_NUM = 50
CORPUS = webtext
TEXT = word_tokenize(CORPUS.raw(random.choice(CORPUS.fileids())))
SENTS = CORPUS.sents(random.choice(CORPUS.fileids()))

TAIL_PROPORTION = 0.10
def novel10(text):
   word_list = word_tokenize(text)
   first90 = set()
   last10 = set()
   for position, word in enumerate(word_list):
      if position < (len(word_list) - TAIL_PROPORTION * len(word_list)):
         first90.add(word)
      else:
         last10.add(word)

   novel_words = last10.difference(first90)
   print("Unique 10% tail:")
   for novel_word in novel_words:
      assert(novel_word not in first90)
      print(novel_word)
   return novel_words

def main():
   fileid = random.choice(CORPUS.fileids())
   print('USING {} FROM {}'.format(fileid, 'webtext'))
   novel10(CORPUS.raw(fileid))
   return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
