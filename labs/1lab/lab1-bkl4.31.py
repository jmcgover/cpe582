# Jeff McGovern
# CPE 582-01
# Lab 1: BKL Chapter 4, Exercise 31
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

LENGTH = 300
START = random.randint(0, len(RAW_TEXT) - LENGTH - 1)

def just_wrap_text(text, width):
    just_text = None
    # Wrap words using textwrap
    wrapped = textwrap.fill(text, width)
    lines = wrapped.split('\n')
    just_wrapped_lines = []

    # Justify
    for i, line in enumerate(lines):
        # Clean up outer spaces and split lines into words
        line = line.strip()
        words = line.split()

        # Relevant paddign amounts
        num_chars = sum([len(w) for w in words])
        necessary_padding = width - num_chars
        spaces_between = necessary_padding // (len(words) - 1) if len(words) > 1 else 0
        remaining_spaces = necessary_padding - spaces_between * (len(words) - 1) + 1

        # Insert Paddings
        padded_words = []
        for j,word in enumerate(words):
            if j != 0:
                padded_words.append(' ' * (spaces_between + (1 if remaining_spaces else 0)))
            padded_words.append(word)
            if remaining_spaces:
                remaining_spaces -= 1
        just_wrapped_lines.append(padded_words)

    # Validate
    for line in just_wrapped_lines:
        assert(len(''.join(line)) == width)
    return '\n'.join([''.join(line) for line in just_wrapped_lines])

def main():
    test_string = RAW_TEXT[START:(START + LENGTH)]
    print('UNWRAPPED\n{}'.format(test_string))
    just_wrapped = just_wrap_text(test_string, 40)
    print('WRAPPED\n{}'.format(just_wrapped))
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)

