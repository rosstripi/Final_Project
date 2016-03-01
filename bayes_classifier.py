"""
Naive Bayes Classifier for candidate sentiment analysis
"""

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
import json

candidates = ['carson', 'clinton', 'cruz', 'kasich', 'rubio', 'sanders', 'trump']


def word_feats(words):
    # need to add feature extractor here because you can't iterate on a string
    return dict([(word, True) for word in words])

for candidate in candidates:
    posfile = 'training_sets/positive/{}.json'.format(candidate)
    negfile = 'training_sets/negative/{}.json'.format(candidate)
    posfeats = []
    negfeats = []
    with open(posfile, 'r') as jsonfile:
        for line in jsonfile:
            if line not in ['\n', '\r\n']:
                tweet = json.loads(line)
                if 'text' in tweet:
                    posfeats.append((word_feats(tweet['text']), 'pos'))
    with open(negfile, 'r') as jsonfile:
        for line in jsonfile:
            if line not in ['\n', '\r\n']:
                tweet = json.loads(line)
                if 'text' in tweet:
                    posfeats.append((word_feats(tweet['text']), 'neg'))
    negcutoff = len(negfeats)*3//4
    poscutoff = len(posfeats)*3//4
    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
    print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))

    classifier = NaiveBayesClassifier.train(trainfeats)
    print('accuracy:', nltk.classify.util.accuracy(classifier, testfeats))
    classifier.show_most_informative_features()
