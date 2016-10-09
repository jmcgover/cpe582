# Jeff McGovern
# CPE 582-01
# Lab 1: JM Chapter 2, Exercise 2.1
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

import re

ARB_NUM = 50
CORPUS = state_union
RAW_TEXT = CORPUS.raw(random.choice(CORPUS.fileids()))
TEXT = word_tokenize(RAW_TEXT)
SENTS = CORPUS.sents(random.choice(CORPUS.fileids()))

LENGTH = 300
START = random.randint(0, len(RAW_TEXT) - LENGTH - 1)

CONSOLE_WIDTH = 80

def apply_regex(pattern, string):
    print('REGEX :{}'.format(pattern))
    print('STRING:{}'.format(string))
    result = re.match(pattern, string)
    print('RESULT:{}'.format(result.string if result else None))
    print('*' * (CONSOLE_WIDTH // 2))
    return

gettys1 = 'Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal.'

gettys2 = 'Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this.'

bees = 'mad gab bleb blab BLEB BLAB MAD GABBB FUB fub'
alpha_not_quite = 'adsfyqweoiruyqwoeiruyzlsdkmnvbzxc,mvnb'
alpha_only = 'adsfyqweoiruyqwoeiruyzlsdkmnvbzxcmvnb'

repeat1 = 'banana banana'
repeat2 = 'Humbert Humbert'
repeat3 = 'Humbert banana'
repeat4 = 'banana banana '
repeat5 = 'Humbert banana '

aba1 = 'aba'
aba2 = 'bab'
aba3 = 'bbbbbbbabbbbbbbb'
aba4 = 'babbabbabbabbabbabbabbabbabbabbabbabbabbabbab'

line1 = """1 banana
"""
line2 = """1 banana"""
line3 = """
1 banana
"""
line4 = """1 banana
1 apple"""
line5 = """1 banana
1 apple
"""
line6 = """1 banana
five apple
"""
line7 = """one banana
five apple
"""

def prob1():
    print('-' * CONSOLE_WIDTH)
    print('1. the set of all alphabetic strings')
    regex = r'^[a-zA-Z]+$'
    apply_regex(regex, bees)
    apply_regex(regex, alpha_only)
    apply_regex(regex, alpha_not_quite)
    return

def prob2():
    print('-' * CONSOLE_WIDTH)
    print('2. the set of all lower case alphabetic strings ending in \'b\'')
    regex = r'^[a-zA-Z]*b$'
    apply_regex(regex, gettys1)
    apply_regex(regex, alpha_only)
    apply_regex(regex, alpha_not_quite)
    return

def prob3():
    print('-' * CONSOLE_WIDTH)
    print(textwrap.fill('3. the set of all strings with two consecutive repeated words (e.g. "Humbert Humbert" and "the the" but not "the bug" or "the big bug")', width = CONSOLE_WIDTH))
    regex = r'(\w+)\W\1'
    apply_regex(regex, gettys1)
    apply_regex(regex, repeat1)
    apply_regex(regex, repeat2)
    apply_regex(regex, repeat3)
    apply_regex(regex, repeat4)
    apply_regex(regex, repeat5)
    return

def prob4():
    print('-' * CONSOLE_WIDTH)
    print(textwrap.fill('4. the set of all strings from the alphabet a,b such that each a is immediately preceded by and immediately followed by a b', width = CONSOLE_WIDTH))
    regex = r'(bab)+'
    apply_regex(regex, bees)
    apply_regex(regex, alpha_only)
    apply_regex(regex, aba1)
    apply_regex(regex, aba2)
    apply_regex(regex, aba3)
    apply_regex(regex, aba4)
    return

def prob5():
    print('-' * CONSOLE_WIDTH)
    print(textwrap.fill('5. all strings that start at the beginning of the line with an integer and that end at the end of the line with a word', width = CONSOLE_WIDTH))
    regex = r'(^[0-9]+.*\w+$)|(^[0-9]+.*\w+\n([0-9]+.*\w+\n)*[0-9]+.*\w+$)'
    apply_regex(regex, line1)
    apply_regex(regex, line2)
    apply_regex(regex, line3)
    apply_regex(regex, line4)
    apply_regex(regex, line5)
    apply_regex(regex, line6)
    apply_regex(regex, line7)
    return

grra1 = 'grotto raven'
grra2 = 'grottos ravens'
grra3 = 'sgrottos sravens'
grra4 = 'raven grotto'
grra5 = 'ravens grottos'
grra6 = 'sravens sgrottos'
grra7 = 'fuckass'
def prob6():
    print('-' * CONSOLE_WIDTH)
    print(textwrap.fill('6. all strings that have both the word grotto and the word raven in them (but not, e.g. words like grottos that merely contain the word grotto', width = CONSOLE_WIDTH))
    regex = r'.*\b(grotto\b.*raven\b)|(raven\b.*grotto).*'
    apply_regex(regex, grra1)
    apply_regex(regex, grra2)
    apply_regex(regex, grra3)
    apply_regex(regex, grra4)
    apply_regex(regex, grra5)
    apply_regex(regex, grra6)
    apply_regex(regex, grra7)
    return

register1 = 'The cat eats. The cat meows.'
register2 = 'The cat eats banana pancakes'
register3 = 'Shouldn\'t the cat eats? Shouldn\'t the cat meows?'
register4 = '11567 cat eats. 11567 cat meows.'

def prob7():
    print('-' * CONSOLE_WIDTH)
    print(textwrap.fill('7. write a pattern that places the first word of an English sentence in a register. Deal with punctuation.', width = CONSOLE_WIDTH))
    regex = r"([A-Z]\w+'{0,1}\w{0,1}).*\1"
    apply_regex(regex, register1)
    apply_regex(regex, register2)
    apply_regex(regex, register3)
    apply_regex(regex, register4)
    return

def main():
    prob1()
    prob2()
    prob3()
    prob4()
    prob5()
    prob6()
    prob7()
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)



