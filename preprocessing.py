"""
Tweet Pre-Processing Script for Final Project
author: Ross Tripi
"""

import json, re, os, operator, string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import bigrams
from collections import Counter, defaultdict

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

cooccurrence_matrix = defaultdict(lambda: defaultdict(int))


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


for filename in os.listdir('corpora'):
    print("Processing file: {}".format(filename))
    with open('corpora/' + filename, 'r') as jsonfile:
        count_singletons = Counter()
        count_bigrams = Counter()
        #print("Tweets for " + filename + ":")
        for line in jsonfile:
            if line not in ['\n', '\r\n']:
                #print("Tokenizing the line: \n{}".format(line))
                tweet = json.loads(line)
                if 'text' in tweet:
                    # create list of single terms
                    terms_all = [term.lower() for term in preprocess(tweet['text']) if term.lower() not in stop]
                    # create list of bigrams
                    bigrams_all = bigrams([term.lower() for term in preprocess(tweet['text'])])
                    # update frequency distributions for singletons and bigrams
                    count_singletons.update(terms_all)
                    count_bigrams.update(bigrams_all)
                    # update co-occurrence matrix
                    for i in range(len(terms_all)-1):
                        for j in range(i+1, len(terms_all)):
                            word1, word2 = sorted([terms_all[i], terms_all[j]])
                            if word1 != word2:
                                cooccurrence_matrix[word1][word2] += 1

                    # tokens = preprocess(tweet['text'])
                    # print(tokens)
        # print most common singletons, bigrams, and co-occurrences
        print(count_singletons.most_common(25))
        print(count_bigrams.most_common(25))
        com_max = []
        for term1 in cooccurrence_matrix:
            term1_max_terms = max(cooccurrence_matrix[term1].items(), key=operator.itemgetter(1))[:5]
            for term2 in term1_max_terms:
                com_max.append(((term1, term2), cooccurrence_matrix[term1][term2]))
        terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
        print(terms_max[:5])

