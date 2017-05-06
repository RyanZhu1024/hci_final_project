import nltk.classify.util
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews


def word_feats(words):
    return dict([(word, True) for word in words])

negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')

negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

trainfeats = negfeats + posfeats

classifier = NaiveBayesClassifier.train(trainfeats)
print('train on %d instances' % (len(trainfeats)))
classifier.show_most_informative_features()


def process():
    print('input some text')
    while True:
        line = input()
        if line.strip() is not '':
            words = word_tokenize(line)
            feats = [word_feats(words)]
            print(feats)
            print(classifier.classify_many(feats))
            for pdist in classifier.prob_classify_many(feats):
                print('pos: %.4f neg: %.4f' % (pdist.prob('pos'), pdist.prob('neg')))

process()
