# Jeff McGovern
# CPE 582-01
# Lab 2
# Monday, October 24, 2016, 11:55 PM

# System Stuff
import sys
import os
import json
from pprint import pprint
from pprint import pformat

# Logging
import logging
from logging import handlers
LOGGER = logging.getLogger(__name__)
SH = logging.StreamHandler()
FH = logging.handlers.RotatingFileHandler("extract.log", maxBytes=5 * 1000000, backupCount = 5)
SH.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(message)s"))
FH.setFormatter(logging.Formatter("%(asctime)s:%(lineno)s:%(funcName)s:%(levelname)s:%(message)s"))
LOGGER.setLevel(logging.CRITICAL)
LOGGER.addHandler(SH)
LOGGER.addHandler(FH)
LOGGER.info("Beginning Session")

# Data Structures
from collections import Counter
from collections import defaultdict

# Maths
import random

# Natural Language Processing
import nltk
from nltk import ngrams
from nltk import everygrams
from nltk import FreqDist
from nltk.corpus import senseval
from nltk import NaiveBayesClassifier
from nltk import word_tokenize
import string

def saveDictionaryAsJSON(dictionary, filename, check = False):
    LOGGER.debug("Saving dictionary as JSON to '%s'", filename)
    if check and os.path.isfile(filename):
        LOGGER.warning("File already exists!")
        return False
    with open(filename, 'w') as file:
        json.dump(dictionary, file)
    return True

def openJSONAsDictionary(filename, check = False):
    LOGGER.debug("Loading JSON as dictionary:'%s'", filename)
    if check and not os.path.isfile(filename):
        LOGGER.error("File doesn't exist!")
        return None
    with open(filename, 'r') as file:
        return json.load(file)

def getTrumpText():
    LOGGER.debug("Loading text...")
    text = ""
    transcripts = openJSONAsDictionary("trumpTextRaw.json")
    for t in transcripts["texts"]:
        text += " " + t["text"]
    return text

PUNCTUATION = set(string.punctuation)
def getAustenTokens():
    austen = nltk.corpus.gutenberg.words('austen-emma.txt')
    return austen

def getTokens(text):
    LOGGER.debug("Tokenizing...")
    return word_tokenize(text)

def getUnigrams(tokens):
    LOGGER.debug("Unigrams...")
    return [g for g in ngrams(tokens, 1)]

def getBigrams(tokens):
    LOGGER.debug("Bigrams...")
    return [g for g in ngrams(tokens, 2)]

def getEveryGram(tokens, l, h):
    return [g for g in everygrams(tokens, l, h)]

def main():
    bigrams = getBigrams(getAustenTokens())
    sentence = []
    # Begin
    start = None
    while start is None:
        possible = random.choice(bigrams)
        if possible[0] in set([".", "!", "?"]):
            start = possible[1]
        if possible[0][0].isupper():
            start = possible[0]
    # Rest
    sentence.append(start)
    while sentence[-1] not in set([".", "!", "?"]):
        possible = random.choice(bigrams)
        if possible[0] == sentence[-1]:
            sentence.append(possible[1])
    cleanSentence = []
    for index in range(1,len(sentence)):
        if sentence[index] in PUNCTUATION:
            cleanSentence.append(sentence[index-1]+sentence[index])
        elif sentence[index-1] in PUNCTUATION:
            pass
        else:
            cleanSentence.append(sentence[index-1])
    print(' '.join(cleanSentence))
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)

