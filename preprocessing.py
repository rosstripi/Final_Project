"""
Tweet Pre-Processing Script for Final Project
author: Ross Tripi
"""

import json, re, os, operator, string, vincent, math
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

# global counters for singletons, bigrams, and co-occurrences
count_singletons = Counter()
count_bigrams = Counter()
cooccurrence_matrix = defaultdict(lambda: defaultdict(int))  # convert to numpy array for memory optimization
total_tweet_count = 0

singleton_probabilities = {}  # convert to numpy array for memory optimization
singleton_prob_com = defaultdict(lambda: defaultdict(int))  # convert to numpy array for memory optimization

# terms for each candidate
carson_terms = ['#Carson', 'Carson', '#BenCarson', 'Ben Carson']
clinton_terms = ['#Clinton', 'Clinton', '#Hillary', 'Hillary', '#HillaryClinton', 'Hillary Clinton']
cruz_terms = ['#Cruz', 'Cruz', '#TedCruz', 'Ted Cruz']
kasich_terms = ['#Kasich', 'Kasich', '#JohnKasich', 'John Kasich']
rubio_terms = ['#Rubio', 'Rubio', '#Marco', 'Marco', '#MarcoRubio', 'Marco Rubio']
sanders_terms = ['#Sanders', 'Sanders', '#Bernie', 'Bernie', '#BernieSanders', 'Bernie Sanders']
trump_terms = ['#Trump', 'Trump', '#Donald', 'Donald', '#DonaldTrump', 'Donald Trump']

positive_vocab = [
    'good', 'nice', 'great', 'awesome', 'outstanding',
    'fantastic', 'terrific', ':)', ':-)', 'like', 'love',
    'triumph', 'triumphal', 'triumphant', 'victory'
]
negative_vocab = [
    'bad', 'terrible', 'crap', 'useless', 'hate', ':(', ':-(',
    'defeat'
]

# global counters for candidate-specific singletons, bigrams, trigrams, and co-occurrences
carson_singletons = Counter()
carson_bigrams = Counter()
carson_trigrams = Counter()
carson_com = defaultdict(lambda: defaultdict(int))  # convert to numpy array for memory optimization
carson_tweet_count = 0

clinton_singletons = Counter()
clinton_bigrams = Counter()
clinton_trigrams = Counter()
clinton_com = defaultdict(lambda: defaultdict(int))  # convert to numpy array for memory optimization
clinton_tweet_count = 0

cruz_singletons = Counter()
cruz_bigrams = Counter()
cruz_trigrams = Counter()
cruz_com = defaultdict(lambda: defaultdict(int))  # convert to numpy array for memory optimization
cruz_tweet_count = 0

kasich_singletons = Counter()
kasich_bigrams = Counter()
kasich_trigrams = Counter()
kasich_com = defaultdict(lambda: defaultdict(int))  # convert to numpy array for memory optimization
kasich_tweet_count = 0

rubio_singletons = Counter()
rubio_bigrams = Counter()
rubio_trigrams = Counter()
rubio_com = defaultdict(lambda: defaultdict(int))  # convert to numpy array for memory optimization
rubio_tweet_count = 0

sanders_singletons = Counter()
sanders_bigrams = Counter()
sanders_trigrams = Counter()
sanders_com = defaultdict(lambda: defaultdict(int))  # convert to numpy array for memory optimization
sanders_tweet_count = 0

trump_singletons = Counter()
trump_bigrams = Counter()
trump_trigrams = Counter()
trump_com = defaultdict(lambda: defaultdict(int))  # convert to numpy array for memory optimization
trump_tweet_count = 0


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


def update_singletons(counter, tweet_text):
    terms_all = [term.lower() for term in preprocess(tweet_text) if term.lower() not in stop]
    counter.update(terms_all)


def update_bigrams(counter, tweet_text):
    bigrams_all = bigrams([term.lower() for term in preprocess(tweet_text)])
    counter.update(bigrams_all)


def update_trigrams(counter, tweet_text):
    return


def update_com(ddict, tweet_text):
    terms_all = [term.lower() for term in preprocess(tweet_text) if term.lower() not in stop]
    for i in range(len(terms_all)-1):
        for j in range(i+1, len(terms_all)):
            word1, word2 = sorted([terms_all[i], terms_all[j]])
            if word1 != word2:
                ddict[word1][word2] += 1


def calculate_probabilities():
    for term, n in count_singletons.items():
        singleton_probabilities[term] = n / total_tweet_count
        for term2 in cooccurrence_matrix[term]:
            singleton_prob_com[term][term2] = cooccurrence_matrix[term][term2] / total_tweet_count


# updates for individual candidates (maybe refactor this by including switch statement in above functions)
def update_carson(tweet_text):
    update_singletons(carson_singletons, tweet_text)
    update_bigrams(carson_bigrams, tweet_text)
    update_trigrams(carson_trigrams, tweet_text)
    update_com(carson_com, tweet_text)
    global carson_tweet_count
    carson_tweet_count += 1


def update_clinton(tweet_text):
    update_singletons(clinton_singletons, tweet_text)
    update_bigrams(clinton_bigrams, tweet_text)
    update_trigrams(clinton_trigrams, tweet_text)
    update_com(clinton_com, tweet_text)
    global clinton_tweet_count
    clinton_tweet_count += 1


def update_cruz(tweet_text):
    update_singletons(cruz_singletons, tweet_text)
    update_bigrams(cruz_bigrams, tweet_text)
    update_trigrams(cruz_trigrams, tweet_text)
    update_com(cruz_com, tweet_text)
    global cruz_tweet_count
    cruz_tweet_count += 1


def update_kasich(tweet_text):
    update_singletons(kasich_singletons, tweet_text)
    update_bigrams(kasich_bigrams, tweet_text)
    update_trigrams(kasich_trigrams, tweet_text)
    update_com(kasich_com, tweet_text)
    global kasich_tweet_count
    kasich_tweet_count += 1


def update_rubio(tweet_text):
    update_singletons(rubio_singletons, tweet_text)
    update_bigrams(rubio_bigrams, tweet_text)
    update_trigrams(rubio_trigrams, tweet_text)
    update_com(rubio_com, tweet_text)
    global rubio_tweet_count
    rubio_tweet_count += 1


def update_sanders(tweet_text):
    update_singletons(sanders_singletons, tweet_text)
    update_bigrams(sanders_bigrams, tweet_text)
    update_trigrams(sanders_trigrams, tweet_text)
    update_com(sanders_com, tweet_text)
    global sanders_tweet_count
    sanders_tweet_count += 1


def update_trump(tweet_text):
    update_singletons(trump_singletons, tweet_text)
    update_bigrams(trump_bigrams, tweet_text)
    update_trigrams(trump_trigrams, tweet_text)
    update_com(trump_com, tweet_text)
    global trump_tweet_count
    trump_tweet_count += 1

#for filename in os.listdir('corpora'):  # uncomment this when finished gathering tweets
for lap_number in range(1):  # comment out this line when finished gathering tweets
    filename = "all_candidates_20160227.json"  # comment out this line when finished gathering tweets
    print("Processing file: {}".format(filename))
    with open('corpora/' + filename, 'r') as jsonfile:
        #print("Tweets for " + filename + ":")
        for line in jsonfile:
            if line not in ['\n', '\r\n']:
                #print("Tokenizing the line: \n{}".format(line))
                tweet = json.loads(line)
                if 'text' in tweet:
                    update_singletons(count_singletons, tweet['text'])
                    update_bigrams(count_bigrams, tweet['text'])
                    update_com(cooccurrence_matrix, tweet['text'])
                    total_tweet_count += 1
                    if any(term in tweet['text'] for term in carson_terms):
                        update_carson(tweet['text'])
                    if any(term in tweet['text'] for term in clinton_terms):
                        update_clinton(tweet['text'])
                    if any(term in tweet['text'] for term in cruz_terms):
                        update_cruz(tweet['text'])
                    if any(term in tweet['text'] for term in kasich_terms):
                        update_kasich(tweet['text'])
                    if any(term in tweet['text'] for term in rubio_terms):
                        update_rubio(tweet['text'])
                    if any(term in tweet['text'] for term in sanders_terms):
                        update_sanders(tweet['text'])
                    if any(term in tweet['text'] for term in trump_terms):
                        update_trump(tweet['text'])
                    # create list of single terms
                    #terms_all = [term.lower() for term in preprocess(tweet['text']) if term.lower() not in stop]
                    # create list of bigrams
                    #bigrams_all = bigrams([term.lower() for term in preprocess(tweet['text'])])
                    # update frequency distributions for singletons and bigrams
                    #count_singletons.update(terms_all)
                    #count_bigrams.update(bigrams_all)
                    # update co-occurrence matrix
                    #for i in range(len(terms_all)-1):
                        #for j in range(i+1, len(terms_all)):
                            #word1, word2 = sorted([terms_all[i], terms_all[j]])
                            #if word1 != word2:
                                #cooccurrence_matrix[word1][word2] += 1

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
        print(carson_singletons.most_common(25))

word_freq = count_singletons.most_common(20)
labels, freq = zip(*word_freq)
data = {'data': freq, 'x': labels}
bar = vincent.Bar(data, iter_idx='x')
bar.to_json('term_freq.json')

calculate_probabilities()

pmi = defaultdict(lambda: defaultdict(int))  # convert to numpy array for memory optimization
for t1 in singleton_probabilities:
    for t2 in cooccurrence_matrix[t1]:
        if t2 in singleton_probabilities:
            denom = singleton_probabilities[t1] * singleton_probabilities[t2]
            pmi[t1][t2] = math.log2(singleton_prob_com[t1][t2] / denom)

semantic_orientation = {}  # convert to numpy array for memory optimization
for term, n in singleton_probabilities.items():
    positive_assoc = sum(pmi[term][tx] for tx in positive_vocab)
    negative_assoc = sum(pmi[term][tx] for tx in negative_vocab)
    semantic_orientation[term] = positive_assoc - negative_assoc

semantic_sorted = sorted(semantic_orientation.items(),
                         key=operator.itemgetter(1),
                         reverse=True)
top_pos = semantic_sorted[:10]
top_neg = semantic_sorted[-10:]

print(top_pos)
print(top_neg)
