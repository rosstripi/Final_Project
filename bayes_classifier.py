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


candidates = ['carson', 'clinton', 'cruz',
              'kasich', 'rubio', 'sanders',
              'trump']
already_classified_bigrams = []
bigram_features = None  # contains "set" of bigrams found in tweets


def tokenize(s):
    """
    Takes a string and returns all terms, hastags, and other relevant features in a list.

    :param s: string to tokenize
    :return: list of terms, hastags, and other features from the string, in order they appear
    """
    return tokens_re.findall(s)


def preprocess(s, lowercase=True, removestop=True):
    """
    Process string and turn into list of tokens, emoticons, and relevant features.

    :param s: string to process
    :param lowercase: force string to lowercase; default TRUE
    :param removestop: remove stopwords and extraneous words from string; default TRUE
    :return: list of tokens in order they appear
    """
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    if removestop:
        tokens = [token for token in tokens if token not in stopwords]
    return tokens


def bigram_preprocess(s):
    """
    Gets list of bigrams from a given string.

    :param s:  A string to have bigrams taken from
    :return: A list of bigrams in the form of tuples
    """
    bigram_feature_vector = []
    for item in nltk.bigrams(preprocess(s, removestop=False)):
        bigram_feature_vector.append(item)
    return bigram_feature_vector


def word_feats(words):
    wordlist = preprocess(words)
    # might need to change to format [([words,in,list],sentiment),...([],)]
    return dict([(word, True) for word in wordlist if word not in stopwords])
    # return [(preprocess(wordlist), )]


def get_bigrams_in_tweets(tweets):
    """
    Takes list formatted as [((bi,gram),sentiment),...] and returns list of all bigrams

    :param tweets: list formatted as [((bi,gram),sentiment),...] containing bigrams in tweet, tweet sentiment
    :return: list of all bigrams in all tweets
    """
    all_bigrams = []
    for (bigrams, sentiment) in tweets:
      all_bigrams.extend(bigrams)
    return all_bigrams


def get_bigram_features(bigramlist):
    """
    Takes list of bigrams and returns "set" of bigrams (no repeated bigrams; not actually a set)

    :param bigramlist: list of bigrams formatted as [(bi,gram),...]
    :return: "set" of bigrams (no repeated bigrams; not actually a set)
    """
    bigramlist = nltk.FreqDist(bigramlist)
    bigram_feats = bigramlist.keys()
    return bigram_feats


def extract_bigram_features(document_bigrams):
    document_bigrams = set(document_bigrams)
    features = {}
    for bigram in bigram_features:
        features['contains(%s)' % str(bigram)] = (bigram in document_bigrams)
    return features


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
                    # pos1feats.append((preprocess(tweet['text']), 'pos'))
                    already_classified_bigrams.append((bigram_preprocess(tweet['text']), 'pos'))
    with open(negfile, 'r') as jsonfile:
        for line in jsonfile:
            if line not in ['\n', '\r\n']:
                tweet = json.loads(line)
                if 'text' in tweet:
                    # neg1feats.append((preprocess(tweet['text']), 'neg'))
                    already_classified_bigrams.append((bigram_preprocess(tweet['text']), 'neg'))
    global bigram_features
    bigram_features = get_bigram_features(get_bigrams_in_tweets(already_classified_bigrams))
    training_set = nltk.classify.apply_features(extract_bigram_features, already_classified_bigrams)
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    print("Results for {}: \n".format(candidate))
    print(classifier.show_most_informative_features())
    # reset both global containers of bigrams and features
    bigram_features = None
    already_classified_bigrams = []
    # negcutoff = len(neg1feats)*3//4
    # poscutoff = len(pos1feats)*3//4
    # trainfeats = neg1feats[:negcutoff] + pos1feats[:poscutoff]
    # testfeats = neg1feats[negcutoff:] + pos1feats[poscutoff:]
    # print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))

    # classifier = NaiveBayesClassifier.train(trainfeats)
    # print('accuracy:', nltk.classify.util.accuracy(classifier, testfeats))
    # classifier.show_most_informative_features()




