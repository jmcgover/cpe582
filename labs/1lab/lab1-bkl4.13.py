# Jeff McGovern
# CPE 582-01
# Lab 1: BKL Chapter 4, Exercise 13
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

VOWELS = "aeiou"

def build_empty_set_table(m, n):
   table = []
   for i in range(m):
      table.append([])
      for j in range(n):
         table[i].append(set())
   return table

def do_the_thing(word_list):
   vowel_lens = [len([letter for letter in w if letter.lower() in VOWELS]) for w in word_list]
   word_lens = [len(w) for w in word_list]

   word_table = build_empty_set_table(max(word_lens) + 1, max(vowel_lens) + 1)
   for word, length, vowels in zip(word_list, word_lens, vowel_lens):
      word_table[length][vowels].add(word)
   return word_table

def main():
   word_table = do_the_thing(random.sample(TEXT, ARB_NUM))
   for length, words in enumerate(word_table):
      for vowels, words in enumerate(word_table[length]):
         print(length, vowels, words)
   return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
