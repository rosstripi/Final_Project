"""
Tweet Pre-Processing Script for Final Project
author: Ross Tripi
"""

import json, re, os, operator, string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

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

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', '…', 'https']


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


for filename in os.listdir('corpora'):
    with open('corpora/' + filename, 'r') as jsonfile:
        count_all = Counter()
        print("Tweets for " + filename + ":")
        for line in jsonfile:
            if line not in ['\n', '\r\n']:
                tweet = json.loads(line)
                terms_all = [term for term in preprocess(tweet['text']) if term.lower() not in stop]
                count_all.update(terms_all)
                # tokens = preprocess(tweet['text'])
                # print(tokens)
        print(count_all.most_common(5))

