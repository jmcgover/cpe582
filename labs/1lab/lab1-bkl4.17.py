# Jeff McGovern
# CPE 582-01
# Lab 1: BKL Chapter 4, Exercise 17
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

def shorten(word_list, n):

   # Count Words
   word_counts = defaultdict(int)
   for word in word_list:
      word_counts[word] += 1
   sorted_counts = sorted([w for w in word_counts], key=lambda x: word_counts[x])

   # Find Most Frequent
   n_most_freq = set(sorted_counts[-n:])
   assert(len(n_most_freq))
   print('OMITTING {} MOST FREQUENT:'.format(n))
   for bleh in sorted_counts[-n:]:
      print('FREQUENT:{}:{}'.format(word_counts[bleh], bleh))

   # Delete the words
   shortened_text = []
   for w in word_list:
      if w not in n_most_freq:
         shortened_text.append(w)
   return shortened_text

def main():
   num_to_use = 200
   print(textwrap.fill(' '.join(TEXT[:num_to_use])))
   print("Shortening text....")
   shortened = shorten(TEXT[:num_to_use], 50)
   print(textwrap.fill(' '.join(shortened)))
   return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
