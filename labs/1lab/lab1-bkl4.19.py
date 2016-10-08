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

def sort_synsets(base, others_list):
   return sorted(others_list, key=lambda x: base.shortest_path_distance(x))

def main():
   dog = wn.synset('dog.n.01')
   list = [
         wn.synset('minke_whale.n.01'),
         wn.synset('orca.n.01'),
         wn.synset('novel.n.01'),
         wn.synset('tortoise.n.01')]
   base = wn.synset('right_whale.n.01')
   pprint(list)
   print("Sorting...")
   sorted_list = sort_synsets(base, list)
   pprint(sorted_list)
   return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
