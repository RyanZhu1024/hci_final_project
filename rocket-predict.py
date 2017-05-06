import json
import pickle
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import string
import csv


tokenizer = RegexpTokenizer(r'\w+')
stops = set(stopwords.words('english'))
stops.add(('RT', 'rt'))


def word_feats(words):
    return dict([(word, True) for word in words])

f = open('classifier-entropy.pickle', 'rb')
classifier = pickle.load(f)
f.close()

result = {'pos': 0, 'neg': 0}

with open('test-data.json') as f:
    lines = f.readlines()
    for line in lines:
        data = json.loads(line)
        text = data['text']
        tokens = tokenizer.tokenize(text)
        words = [token for token in tokens if token not in stops]
        feats = word_feats(words)
        print(feats)
        label = classifier.classify(feats)
        print(label)
        result[label] += 1

print(result)


testfeats = []


def get_sentiment(sent):
    if sent is '0':
        return 'neg'
    elif sent is '2':
        return 'neu'
    else:
        return 'pos'


def get_tokens(phrase):
    fs = [word.strip(string.punctuation) for word in phrase.split(" ")]
    return [f.lower() for f in fs if f and f.lower() not in stops and not f.startswith('@')]

with open('test.csv', encoding='latin-1') as testFile:
    reader = csv.reader(testFile, delimiter=',')
    for row in reader:
        sentiment = row[0]
        text = row[-1]
        tokens = get_tokens(text)
        testfeats.append((word_feats(tokens), get_sentiment(sentiment)))
print('accuracy: ', nltk.classify.util.accuracy(classifier, testfeats))
