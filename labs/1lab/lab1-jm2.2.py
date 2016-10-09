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

def response(input):
    response = None
    print('User : {}'.format(input))
    input = re.sub(r"\b([Ii]'{0,1}[Mm])|([Ii] [Aa][Mm])\b", "YOU ARE", input)
    input = re.sub(r"\bmy\b", "YOUR", input, re.IGNORECASE)
    input = re.sub(r"\bme\b", "YOU", input, re.IGNORECASE)
    input = re.sub(r"\b(I|me)\b", "YOU", input, re.IGNORECASE)

    response1 = re.sub(r".*\byour (father|mother)\b.*", 
            "IT'S NOT TRUE. THAT'S IMPOSSIBLE", input, re.IGNORECASE)
    response2 = re.sub(r".*\b[jJ]oin YOU\b.*",
            "I'LL NEVER JOIN YOU",input, re.IGNORECASE)
    response3 = re.sub(r".*\b(always|never|all|every\w*|impossible)\b.*",
            "ONLY A SITH DEALS IN ABSOLUTES",input, re.IGNORECASE)
    response2 = re.sub(r".*\b(fear|afraid|scared|frightened)\b.*",
            "\g<1> IS THE PATH TO THE DARK SIDE",input, re.IGNORECASE)
    response3 = re.sub(r".*\b(fear|afraid|scared|frightened)\b.*",
            "\g<1> LEADS TO HATE. HATE LEADS TO ANGER. ANGER LEADS TO SUFFERING.",input)
    response4 = re.sub(r".*\b(hate|hatred|hated|despise|detest)\b.*",
            "\g<1> LEADS TO ANGER. ANGER LEADS TO SUFFERING.",input)
    response5 = re.sub(r".*\b(anger|angry|angery|angered|mad)\W.*",
            "\g<1> LEADS TO SUFFERING.",input)

    responses = [r for r in (response1, response2, response3, response4, response5) if r != input]
    if len(responses):
        response = random.choice(responses).upper()
    else:
        response = input.upper()
    print('LUKE: {}'.format(response))
    return response

def eliza_response(input):
    response = None
    print('User : {}'.format(input))
    input = re.sub(r"\b[Ii]'{0,1}[Mm]\b", "YOU ARE", input)
    input = re.sub(r"\bmy\b", "YOUR", input, re.IGNORECASE)
    input = re.sub(r"\bme\b", "YOU", input, re.IGNORECASE)

    response1 = re.sub(r".* YOU ARE (depressed|sad) .*","I AM SORRY TO HEAR YOU ARE \1",input)
    response2 = re.sub(r".* YOU ARE (depressed|sad) .*","WHY DO YOU THINK YOU ARE \1",input)
    response3 = re.sub(r".* all .*","IN WHAT WAY",input)
    response4 = re.sub(r".* always .*","CAN YOU THINK OF A SPECIFIC EXAMPLE",input)

    responses = [r for r in (response1, response2, response3, response4) if r != input]
    if len(responses):
        response = random.choice(responses).upper()
    else:
        response = input.upper()
    print('ELIZA: {}'.format(response))
    return response

def main():
    print('THIS IS ELIZA')
    eliza_response("Men are all alike.")
    eliza_response("They're always bugging us about something or the other.")
    eliza_response("Well, my boyfriend made me come here.")
    eliza_response("He says I'm depressed much of the time.")
    print('SAY HELLO TO LUKE')
    response('Join me.')
    response('I am your father.')
    response('I am a jedi.')
    response('I am a sith.')
    response('I am angry.')
    response('I hated it.')
    response('It scared me.')
    response('I fear death.')
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)




