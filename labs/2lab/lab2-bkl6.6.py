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

# Maths
import random

# Natural Language Processing
import nltk
from nltk import ngrams
from nltk import FreqDist
from nltk.corpus import senseval
from nltk import NaiveBayesClassifier

def extract_features(trigram_tags):
    features = {}
    features['left_word'] = trigram_tags[0][0]
    features['left_tag'] = trigram_tags[0][1]
    features['right_word'] = trigram_tags[2][0]
    features['right_tag'] = trigram_tags[2][1]
    return features

def get_train_test(all_data, proportion = 0.50):
    train_set = []
    test_set = []
    # Shuffle
    shuffled_data = all_data[:]
    random.shuffle(shuffled_data)
    # Select
    max_test_num = int(proportion * round(len(shuffled_data)))
    test_set = shuffled_data[:max_test_num]
    train_set = shuffled_data[max_test_num:]
    return train_set, test_set

def main():
    print('Grabbing tagged Text...')
    tagged_text = nltk.corpus.brown.tagged_words()
    print('Finding contexts...')
    contexts = list(ngrams(tagged_text, 3))
    strongpowerful_contexts = []
    for left, middle, right in contexts:
        if middle[0] == 'strong' or middle[0] == 'powerful':
            strongpowerful_contexts.append((left, middle, right))
    print('Building datasets...')
    train_set, test_set = get_train_test(strongpowerful_contexts)
    print('Training...')
    classifier = NaiveBayesClassifier.train([(
        extract_features((left,middle,right)), middle[0]) for left,middle,right in train_set])
    accuracy = nltk.classify.accuracy(classifier, [(
        extract_features((left,middle,right)), middle[0]) for left,middle,right in train_set])
    print('Accuracy: %.3f' % accuracy)
    classifier.show_most_informative_features(5)
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)

