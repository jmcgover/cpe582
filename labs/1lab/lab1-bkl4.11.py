# Jeff McGovern
# CPE 582-01
# Lab 1: BKL Chapter 4, Exercise 10
# Friday, October 7, 2016, 11:30 PM

import os
import sys

# Write a program to sort words by length. Define a helper function cmp_len
# which uses the cmp comparison function on word lengths.

import nltk
from nltk.corpus import webtext
from nltk.tokenize import word_tokenize
import random

ARB_NUM = 10
CORPUS = webtext
TEXT = word_tokenize(CORPUS.raw(random.choice(CORPUS.fileids())))
SENTS = CORPUS.sents(random.choice(CORPUS.fileids()))

def problem_0():
    print("Beginning Problem 4.11 Part 0")
    # Create a list of words and store it in a variable sent1.
    # Now assign sent2 = sent1.
    # Modify one of the items in sent1 and verify that sent2 has changed.
    sent1 = random.sample(TEXT, ARB_NUM)
    sent2 = sent1

    # Show Before
    print('Before')
    assert(compare_two_lists(sent1, sent2) == True)

    # Modify Random Element
    sent1[random.randint(0, len(sent1))] = "PROBLEM 0: VERY OBVIOUS REPLACEMENT"

    # Show After
    print('After')
    assert(compare_two_lists(sent1, sent2) == True)
    return

def problem_1():
    # Now try the same exercise but instead assign sent2 = sent1[:].
    # Modify sent1 again and see what happens to sent2.
    # Explain.
    print("Beginning Problem 4.11 Part 1")
    sent1 = random.sample(TEXT, ARB_NUM)
    sent2 = sent1[:]

    # Show Before
    print('Before')
    assert(compare_two_lists(sent1, sent2) == True)

    # Modify Random Element
    sent1[random.randint(0, len(sent1) - 1)] = "PROBLEM 1: VERY OBVIOUS REPLACEMENT"

    # Show After
    print('After')
    assert(compare_two_lists(sent1, sent2) == False)

    return

def problem_2():
    # Now try the same exercise but instead assign sent2 = sent1[:].
    # Modify sent1 again and see what happens to sent2.
    # Explain.
    print("Beginning Problem 4.11 Part 2")
    text1 = random.sample(TEXT, ARB_NUM)
    text2 = text1[:]

    # Show Before
    print('Before')
    assert(compare_two_lists(text1, text2) == True)

    # Modify Random Element
    text1[random.randint(0, len(text1) - 1)][1] = "PROBLEM 2: VERY OBVIOUS REPLACEMENT"

    # Show After
    print('After')
    assert(compare_two_lists(text1, text2) == False)
    return

def compare_two_lists(a, b, verbose = True):
    is_identical = True
    for x,y in zip(a,b):
        is_identical = is_identical and x == y
        if verbose:
            print('{}:"{}" == "{}"'.format(x == y, x, y))
    if verbose:
        print("Lists are identical" if is_identical else "Lists are not identical")
    return is_identical

def main():
    problem_0()
    print()
    problem_1()
    print()
    problem_2()
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
