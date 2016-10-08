# Jeff McGovern
# CPE 582-01
# Lab 1: BKL Chapter 4, Exercise 32
# Friday, October 7, 2016, 11:30 PM

import os
import sys

# Write a program to sort words by length. Define a helper function cmp_len
# which uses the cmp comparison function on word lengths.

import nltk
from nltk import edit_distance
from nltk.corpus import state_union
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.tokenize import regexp_tokenize
import random
from pprint import pprint
from collections import defaultdict
import textwrap
from nltk import FreqDist
import string

ARB_NUM = 50
CORPUS = state_union
RAW_TEXT = CORPUS.raw(random.choice(CORPUS.fileids()))
TEXT = word_tokenize(RAW_TEXT)
SENTS = CORPUS.sents(random.choice(CORPUS.fileids()))

LENGTH = 300
START = random.randint(0, len(RAW_TEXT) - LENGTH - 1)

CONSOLE_WIDTH = 80
def summarize_corpus(corpus, n):
    for fileid in sorted(corpus.fileids()):
        print(textwrap.fill('PROCESSING:{}'.format(fileid), width = CONSOLE_WIDTH))
        words = corpus.words(fileid)
        sents = corpus.sents(fileid)
        word_dist = FreqDist(words)
        sent_scores = []
        for sent in sents:
            sent_scores.append((sum([word_dist[word] for word in sent]), sent))
        sent_scores = sorted(sent_scores, reverse = True)
        for score, sent in sent_scores[:n]:
            print(textwrap.fill('{}:{}'.format(score, ''.join(
                [' ' + token if not token.startswith('\'') 
                    and token not in string.punctuation else token
                    for token in sent]).strip()), width=CONSOLE_WIDTH))
            print()
        print('-' * CONSOLE_WIDTH)
    return

def main():
    summarize_corpus(CORPUS, 2)
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)


