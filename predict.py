import string
import pickle
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

tokenizer = RegexpTokenizer(r'\w+')
stops = set(stopwords.words('english'))


def get_tokens(phrase):
    fs = [word.strip(string.punctuation) for word in phrase.split(" ")]
    return [f.lower() for f in fs if f and f.lower() not in stops and not f.startswith('@')]


def word_feats(words):
    return dict([(word, True) for word in words])

f = open('classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()

while True:
    print('give some text')
    line = input()
    if line.strip() is not '':
        tokens = get_tokens(line)
        feats = [word_feats(tokens)]
        print(feats)
        print(classifier.classify_many(feats))
        for pdist in classifier.prob_classify_many(feats):
            print('pos: %.4f neg: %.4f' % (pdist.prob('pos'), pdist.prob('neg')))