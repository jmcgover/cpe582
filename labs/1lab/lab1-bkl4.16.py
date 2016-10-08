# Jeff McGovern
# CPE 582-01
# Lab 1: BKL Chapter 4, Exercise 16
# Friday, October 7, 2016, 11:30 PM

import os
import sys

# Write a program to sort words by length. Define a helper function cmp_len
# which uses the cmp comparison function on word lengths.

import nltk
from nltk.corpus import state_union
from nltk.tokenize import word_tokenize
from nltk.tokenize import regexp_tokenize
import random
from pprint import pprint
from collections import defaultdict

ARB_NUM = 50
CORPUS = state_union
TEXT = word_tokenize(CORPUS.raw(random.choice(CORPUS.fileids())))
SENTS = CORPUS.sents(random.choice(CORPUS.fileids()))

LETTER_VALS = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':80, 'g':3, 'h':8,
'i':10, 'j':10, 'k':20, 'l':30, 'm':40, 'n':50, 'o':70, 'p':80, 'q':100,
'r':200, 's':300, 't':400, 'u':6, 'v':6, 'w':800, 'x':60, 'y':10, 'z':7}
def gematria(word):
   return sum(LETTER_VALS[letter.lower()] for letter in word if letter in LETTER_VALS)

def build_gematria_counts(text):
   gematria_counts = defaultdict(set)
   for word in word_tokenize(text):
      if len([c for c in word if c in LETTER_VALS]):
         gematria_counts[gematria(word)].add(word)
   return gematria_counts

def build_corpus_gematria(corpus):
   doc_gem_counts = {}
   for fileid in corpus.fileids():
      print("PROCESSING", fileid, file=sys.stderr)
      doc_gem_counts[fileid] = build_gematria_counts(corpus.raw(fileid))
   return doc_gem_counts

def build_whole_corpus_gematris(per_file_gems):
   whole_gem = defaultdict(set)
   for fileid, gem_counts in per_file_gems.items():
      print('COALESCING', fileid)
      for gem, words in gem_counts.items():
         whole_gem[gem] = whole_gem[gem].union(words)
   return whole_gem

def get_gematris_synonym(word, synonyms):
   gematria_score = gematria(word)
   if gematria_score in synonyms:
      word_singleton = set()
      word_singleton.add(word)
      return random.sample(synonyms[gematria_score].union(word_singleton), 1)[0]
   return word

def decode(text, gematris_synonyms):
   word_list = word_tokenize(text)
   new_word_list = word_list[:]
   for position, word in enumerate(word_list):
      new_word_list[position] = get_gematris_synonym(word, gematris_synonyms)
   return ' '.join(new_word_list)

def main():
   # Word Gematria
   test_string = 'banana'
   print('Gematria for "{}": {}'.format(test_string, gematria(test_string)))

   # Sentence Gematria
   test_sentence = 'The quick brown fox jumped over the lazy dog.'
   print('Gematria for "{}": '.format(test_sentence))
   pprint(build_gematria_counts(test_sentence))

   # Looking for 666
   desired_length = 666
   each_gematria = build_corpus_gematria(CORPUS)
   for fileid, file_gem in each_gematria.items():
      if desired_length in file_gem:
         print('(gem {}){}: {}'.format(desired_length, fileid, file_gem[desired_length]))

   # Train Gematris Synonbyms
   corpus_gems = build_whole_corpus_gematris(each_gematria)
   for gem, words in corpus_gems.items():
      print('ALL:{}:{}'.format(gem, words))

   # Randomly Replace Words
   test_sentence_long = 'The quick brown fox jumped over the lazy dog, and then ran to the tree, ate a banana, and sang a song that wasn\'t that bad.'
   decoded = decode(test_sentence_long, corpus_gems)
   print('DECODED\n{}\n{}'.format(test_sentence_long, decoded))
   return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
