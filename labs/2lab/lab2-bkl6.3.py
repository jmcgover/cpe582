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
from nltk.corpus import senseval
from nltk import NaiveBayesClassifier

def main():
    instances = senseval.instances('interest.pos')
    size = int(len(instances) * 0.1)
    train_set, test_set = instances[size:], instances[:size]
    print('Training...')
    classifier = NaiveBayesClassifier.train(
            [({"context" : tuple(instance.context)}, instance.senses)
            for instance in train_set])
    print('Testing...')
    accuracy = nltk.classify.accuracy(classifier, [({"context" : tuple(instance.context)}, instance.senses)
            for instance in test_set])
    print('Accuracy: %.3f' % accuracy)
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)

