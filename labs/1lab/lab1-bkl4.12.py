# Jeff McGovern
# CPE 582-01
# Lab 1: BKL Chapter 4, Exercise 12
# Friday, October 7, 2016, 11:30 PM

import os
import sys

import nltk
from nltk.corpus import brown
from nltk.tokenize import word_tokenize
import random
from pprint import pprint

ARB_NUM = 10
CORPUS = brown
TEXT = word_tokenize(CORPUS.raw(random.choice(CORPUS.fileids())))
SENTS = CORPUS.sents(random.choice(CORPUS.fileids()))

def do_the_thing(n, m):
   assert(n > 1)
   assert(m > 2)
   print()
   print('Building empty word table: word_table = [[''] * n] * m')
   word_table = [[''] * n] * m
   pprint(word_table)

   print('Assigning to hopefully one spot: word_table[1][2] = \'hello\'')
   word_table[1][2] = 'hello'
   pprint(word_table)
   print('It looks like there\'s only one n-dimensional vector that\'s being referenced m-many times.')
   return

def do_the_right_thing(n, m):
   assert(n > 1)
   assert(m > 2)
   word_table = []

   print('Building empty word table using range() for enumeration and append()')
   for i in range(m):
      word_table.append([''] * n)
   pprint(word_table)

   print('Assigning to hopefully one spot: word_table[1][2] = \'hello\'')
   word_table[1][2] = 'hello'
   pprint(word_table)
   return

def main():
   do_the_thing(7, 11)
   do_the_right_thing(7, 11)
   return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)

