# Jeff McGovern
# CPE 582-01
# Lab 2
# Monday, October 24, 2016, 11:55 PM

# System Stuff
import sys
import os
from pprint import pprint

# Data Structures
from collections import Counter
from collections import defaultdict

# Natural Language Processing
import nltk
from nltk import ngrams
from nltk import FreqDist

def q1(tagged_words):
    word_taglist = defaultdict(list)
    [word_taglist[word].append(tag) for word, tag in tagged_words]
    singly_tagged_words = sorted([(word, taglist)for word, taglist in word_taglist.items() if len(taglist) == 1])
    return len(singly_tagged_words) / len(word_taglist.keys())

def q2(tagged_words):
    word_taglist = defaultdict(list)
    [word_taglist[word].append(tag) for word, tag in tagged_words]
    ambiguous_words = defaultdict(Counter)
    [ambiguous_words[word].update(taglist) for word, taglist in word_taglist.items() if len(taglist) > 1]
    return ambiguous_words

def q3(tagged_words, ambiguous_words):
    return len([token for token, tag in tagged_words if token in ambiguous_words]) / len(tagged_words)

def main():
    print('Grabbing tagged Text...')
    tagged_text = nltk.corpus.brown.tagged_words(tagset='universal')
    print('1. Finding proportion of word types(?) always tagged same...')
    frac_singly_tagged = q1(tagged_text)
    print("Proportion Unambiguous: %.3f" % (frac_singly_tagged))
    print('2. Finding ambiguous words...')
    ambig_words = q2(tagged_text)
    print('Number Ambiguous: %d' % len(ambig_words.keys()))
    print('3. Calculating percentage of ambiguous tokens...')
    percent_ambiguous_tokens = q3(tagged_text, ambig_words)
    print("Proportion Ambiguous Tokens: %.3f" % percent_ambiguous_tokens)
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)

