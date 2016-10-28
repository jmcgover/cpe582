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
    nouns = [word for word, tag in tagged_words if tag == 'NN']
    noun_counts = Counter(nouns)
    mostly_plural = {}
    for noun, count in noun_counts.items():
        if noun + 's' in noun_counts and noun_counts[noun + 's'] > noun_counts[noun]:
            mostly_plural[(noun, noun + 's')] = (noun_counts[noun], noun_counts[noun + 's'])
    return mostly_plural

def q2(tagged_text):
    word_tags = defaultdict(set)
    [word_tags[word].add(tag) for word, tag in tagged_text]
    return sorted([(word, tags) for word, tags in word_tags.items()], key = lambda x: len(x[1]), reverse = True)[0]

def q3(tagged_text):
    tag_counts = Counter(tag for word, tag in tagged_text)
    return sorted([(tag, count) for tag, count in tag_counts.items()], key = lambda x: x[1], reverse = True)

def q3(tagged_text):
    tag_counts = Counter(tag for word, tag in tagged_text)
    return sorted([(tag, count) for tag, count in tag_counts.items()], key = lambda x: x[1], reverse = True)

def q4(tagged_text):
    tag_bigrams = ngrams(tagged_text, 2)
    noun_bigrams = []
    for first, second in tag_bigrams:
        if 'NN' in second[1]:
            noun_bigrams.append((first, second))
    tag_bigram_words = defaultdict(list)
    [tag_bigram_words[(first[1], second[1])].append((first[0], second[0])) for first, second in noun_bigrams]
    tagbigram_examples = []
    for bigram in tag_bigram_words:
        tagbigram_examples.append((bigram, FreqDist(tag_bigram_words[bigram])))
    return sorted(tagbigram_examples, key = lambda x: len(x[1]), reverse = True)

def main():
    print('Grabbing tagged Text...')
    tagged_text = nltk.corpus.brown.tagged_words()
    print('1. Finding mostly plural nouns...')
    mostly_plural = q1(tagged_text)
    pprint(mostly_plural)
    print('2. Finding word with most distinct tags...')
    most_distinct = q2(tagged_text)
    pprint(most_distinct)
    print('3. Listing most common tags...')
    tag_counts = q3(tagged_text)
    pprint(tag_counts[:20])
    print('4. Finding noun collocations...')
    tagbigram_examples = q4(tagged_text)
    for bigram, examples in tagbigram_examples[:20]:
        print(len(examples), bigram, examples.most_common(5))
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)

