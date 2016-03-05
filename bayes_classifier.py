"""
Naive Bayes Classifier for candidate sentiment analysis
"""

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
import json, re, string


emoticons_str = r"""
    (?:
        [:=;]
        [oO\-]?
        [D\)\]\(\]/\\OpP]
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs
    r'(?:&amp;)',  # ampersands
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', '…', 'https', '&amp;', '...']


candidates = ['carson', 'clinton', 'cruz', 'kasich', 'rubio', 'sanders', 'trump']


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=True, removestop=True):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    if removestop:
        tokens = [token for token in tokens if token not in stopwords]
    return tokens


def word_feats(words):
    wordlist = preprocess(words)
    # might need to change to format [([words,in,list],sentiment),...([],)]
    return dict([(word, True) for word in wordlist if word not in stopwords])
    # return [(preprocess(wordlist), )]

for candidate in candidates:
    posfile = 'training_sets/positive/{}.json'.format(candidate)
    negfile = 'training_sets/negative/{}.json'.format(candidate)
    pos1feats = []
    neg1feats = []
    pos3feats = []
    neg3feats = []
    with open(posfile, 'r') as jsonfile:
        for line in jsonfile:
            if line not in ['\n', '\r\n']:
                tweet = json.loads(line)
                if 'text' in tweet:
                    pos1feats.append((preprocess(tweet['text']), 'pos'))
    with open(negfile, 'r') as jsonfile:
        for line in jsonfile:
            if line not in ['\n', '\r\n']:
                tweet = json.loads(line)
                if 'text' in tweet:
                    neg1feats.append((preprocess(tweet['text']), 'neg'))
    negcutoff = len(neg1feats)*3//4
    poscutoff = len(pos1feats)*3//4
    trainfeats = neg1feats[:negcutoff] + pos1feats[:poscutoff]
    testfeats = neg1feats[negcutoff:] + pos1feats[poscutoff:]
    print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))

    classifier = NaiveBayesClassifier.train(trainfeats)
    print('accuracy:', nltk.classify.util.accuracy(classifier, testfeats))
    classifier.show_most_informative_features()
