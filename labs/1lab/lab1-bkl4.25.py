# Jeff McGovern
# CPE 582-01
# Lab 1: BKL Chapter 4, Exercise 25
# Friday, October 7, 2016, 11:30 PM

import os
import sys

# Write a program to sort words by length. Define a helper function cmp_len
# which uses the cmp comparison function on word lengths.

import nltk
from nltk import edit_distance
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

def print_edit_distance(a, b, file = sys.stdout):
    print('DISTANCE:{}:{}: {}'.format(a, b, edit_distance(a,b)))
    return

ANSWER = 'Dynamic programming is built off the notion of finding optimal subproblems, where some of these subproblems overlap with each other or the current problem, in order to find the most optimal solution to the current problem. In the case of edit distance, how we edit ealier in the word may affect what the most optimal solution is at the curetn stage of the solution. In the case of Levenshtein distance, it is a bottom up approach for some algorithms, because a decision is made on what to calculate next.'
def main():
    for a,b in zip(random.sample(TEXT, 17), random.sample(TEXT, 17)):
        print_edit_distance(a,b)
    pprint(ANSWER, width = 40)
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
