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

def main():
    print('Grabbing tagged Text...')
    tagged_text = nltk.corpus.brown.tagged_words()
    contexts = list(ngrams(tagged_text, 3))
    categories = defaultdict(list)
    print('Categorizing...')
    for left, middle, right in contexts:
        if middle[0].lower() == 'must':
            categories[right[1]].append((left, middle, right))
    for tag, contexts in categories.items():
        print('%s:{' % tag)
        for left, middle, right in contexts:
            print('\t%s : %s' % (' '.join([left[0], middle[0], right[0]]),
                ' '.join([left[1], middle[1], right[1]]),))
        print('}')
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
