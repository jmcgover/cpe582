# Jeff McGovern
# CPE 582-01
# Lab 2
# Monday, October 24, 2016, 11:55 PM

# System Stuff
import sys
import os
import json
from pprint import pprint

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
from pprint import pprint

# Data Structures
from collections import Counter
from collections import defaultdict

# Maths
import random

# Natural Language Processing
import nltk
from nltk import ngrams
from nltk import FreqDist
from nltk.corpus import senseval
from nltk import NaiveBayesClassifier
from nltk import word_tokenize

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

def getText():
    LOGGER.debug("Loading text...")
    text = ""
    transcripts = openJSONAsDictionary("trumpTextRaw.json")
    for t in transcripts["texts"]:
        text += " " + t["text"]
    return text

def getTokens():
    LOGGER.debug("Tokenizing...")
    return word_tokenize(getText())

def getUnigrams(tokens):
    LOGGER.debug("Unigrams...")
    return [g for g in ngrams(tokens, 1)]

def getBigrams(tokens):
    LOGGER.debug("Bigrams...")
    return [g for g in ngrams(tokens, 2)]

def main():
    LOGGER.setLevel(logging.DEBUG)
    tokens = getTokens()
    unigrams = getUnigrams(tokens)
    bigrams = getBigrams(tokens)
    numToPrint = 20
    print("Num Words: %d" % (len(tokens)))
    pprint(unigrams[:numToPrint])
    pprint(bigrams[:numToPrint])
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
