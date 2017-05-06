"""
Data get from http://help.sentiment140.com/for-students
"""
from nltk.corpus import stopwords
from nltk.classify import NaiveBayesClassifier
import nltk.classify.util
import pickle
from multiprocessing.dummy import Pool as ThreadPool
import csv
import re
import string

import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

negates = ['no', 'not', 'nor']
negreg = ".+n\'t"
stops = [stop for stop in set(stopwords.words('english')) if re.match(negreg, stop) is not None or stop not in negates]


def word_feats(words):
    return dict([(word, True) for word in words])


# def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
#     bigram_finder = BigramCollocationFinder.from_words(words)
#     bigrams = bigram_finder.nbest(score_fn, n)
#     return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])

negfeats = []
neufeats = []
posfeats = []

data_pairs = [('negdata-all.txt', negfeats, 'neg'), ('posdata-all.txt', posfeats, 'pos'),
              ('neudata-all.txt', neufeats, 'neu')]


def get_tokens(phrase):
    fs = [word.strip(string.punctuation) for word in phrase.split(" ")]
    return [f.lower() for f in fs if f and f.lower() not in stops and not f.startswith('@')]


def read_one_file(path):
    print('read %s' % path[0])
    with open(path[0], 'r') as data:
        lines = data.readlines()
        for idx, text in enumerate(lines):
            text = text.lower()
            tokens = get_tokens(text)
            # words = [token for token in tokens if token not in stops]
            path[1].append((word_feats(tokens), path[2]))
            # try:
            # path[1].append((word_feats(tokens), path[2]))
            # except ZeroDivisionError:
            #     pass
            print("Progress for %s %f." % (path[0], idx / len(lines)))


pool = ThreadPool(len(data_pairs))


def read_data(dp):
    pool.map(read_one_file, dp)


read_data(data_pairs)
pool.close()
pool.join()

trainfeats = negfeats + posfeats + neufeats
testfeats = []


def get_sentiment(sent):
    if sent is '0':
        return 'neg'
    elif sent is '2':
        return 'neu'
    else:
        return 'pos'

with open('test.csv', encoding='latin-1') as testFile:
    reader = csv.reader(testFile, delimiter=',')
    for row in reader:
        sentiment = row[0]
        text = row[-1]
        tokens = get_tokens(text)
        # words = [token for token in tokens if token not in stops]
        # try:
        testfeats.append((word_feats(tokens), get_sentiment(sentiment)))
        # except ZeroDivisionError:
        #     pass
def naive_bayes():
    print('Naive bayes, train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))
    classifier = NaiveBayesClassifier.train(trainfeats)
    print('accuracy: ', nltk.classify.util.accuracy(classifier, testfeats))
    classifier.show_most_informative_features()
    with open('classifier.pickle', 'wb') as f:
        print('save classifier')
        pickle.dump(classifier, f)


def max_entropy():
    print('Max entropy, train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))
    num_iterations = 2
    algorithm = nltk.classify.MaxentClassifier.ALGORITHMS[0]
    classifier = nltk.MaxentClassifier.train(trainfeats, algorithm, max_iter=num_iterations)
    print('accuracy: ', nltk.classify.util.accuracy(classifier, testfeats))
    classifier.show_most_informative_features()
    with open('classifier-entropy.pickle', 'wb') as f:
        print('save classifier')
        pickle.dump(classifier, f)

max_entropy()
