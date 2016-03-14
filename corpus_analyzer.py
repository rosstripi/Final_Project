"""
Script that uses Bayes classifiers to iterate through candidate corpora and determine percentage of
positive vs. negative sentiment tweets for each candidate.

Writes these results to a csv file. (not yet implemented)
"""

import bayes_classifier, json, os
from collections import defaultdict

candidates = ['carson', 'clinton', 'cruz',
              'kasich', 'rubio', 'sanders',
              'trump']
total_tweets_per_candidate = defaultdict(int)
total_tweets = 0
sentiment_counts_per_candidate = defaultdict(lambda: defaultdict(int))

# terms for each candidate
carson_terms = ['#carson', 'carson', '#bencarson', 'ben carson']
clinton_terms = ['#clinton', 'clinton', '#hillary', 'hillary', '#hillaryclinton', 'hillary clinton']
cruz_terms = ['#cruz', 'cruz', '#tedcruz', 'ted cruz']
kasich_terms = ['#kasich', 'kasich', '#johnkasich', 'john kasich']
rubio_terms = ['#rubio', 'rubio', '#marco', 'marco', '#marcorubio', 'marco rubio']
sanders_terms = ['#sanders', 'sanders', '#bernie', 'bernie', '#berniesanders', 'bernie sanders']
trump_terms = ['#trump', 'trump', '#donald', 'donald', '#donaldtrump', 'donald trump']


bigram_classifiers = {}


for candidate in candidates:
    bigram_classifiers[candidate] = bayes_classifier.build_bigram_classifier_for_candidate(candidate)


for filename in os.listdir('corpora'):  # uncomment this when finished gathering tweets
#for lap_number in range(1):  # comment out this line when finished gathering tweets
    #filename = "all_candidates_20160227.json"  # comment out this line when finished gathering tweets
    print("Processing file: {}".format(filename))
    with open('corpora/' + filename, 'r') as jsonfile:
        #print("Tweets for " + filename + ":")
        for line in jsonfile:
            if line not in ['\n', '\r\n']:
                #print("Tokenizing the line: \n{}".format(line))
                tweet = json.loads(line)
                if 'text' in tweet:
                    total_tweets += 1
                    #update_all_counters(tweet['text'])
                    terms_all = bayes_classifier.preprocess(tweet['text'], removestop=False)
                    if any(term in terms_all for term in carson_terms):
                        total_tweets_per_candidate["carson"] += 1
                        sentiment_counts_per_candidate["carson"][bayes_classifier.classify_string(bigram_classifiers["carson"],tweet['text'])] += 1
                    if any(term in terms_all for term in clinton_terms):
                        total_tweets_per_candidate["clinton"] += 1
                        sentiment_counts_per_candidate["clinton"][bayes_classifier.classify_string(bigram_classifiers["clinton"],tweet['text'])] += 1
                    if any(term in terms_all for term in cruz_terms):
                        total_tweets_per_candidate["cruz"] += 1
                        sentiment_counts_per_candidate["cruz"][bayes_classifier.classify_string(bigram_classifiers["cruz"],tweet['text'])] += 1
                    if any(term in terms_all for term in kasich_terms):
                        total_tweets_per_candidate["kasich"] += 1
                        sentiment_counts_per_candidate["kasich"][bayes_classifier.classify_string(bigram_classifiers["kasich"],tweet['text'])] += 1
                    if any(term in terms_all for term in rubio_terms):
                        total_tweets_per_candidate["rubio"] += 1
                        sentiment_counts_per_candidate["rubio"][bayes_classifier.classify_string(bigram_classifiers["rubio"],tweet['text'])] += 1
                    if any(term in terms_all for term in sanders_terms):
                        total_tweets_per_candidate["sanders"] += 1
                        sentiment_counts_per_candidate["sanders"][bayes_classifier.classify_string(bigram_classifiers["sanders"],tweet['text'])] += 1
                    if any(term in terms_all for term in trump_terms):
                        total_tweets_per_candidate["trump"] += 1
                        sentiment_counts_per_candidate["trump"][bayes_classifier.classify_string(bigram_classifiers["trump"],tweet['text'])] += 1


for candidate in candidates:
    print("Stats for {}: \n".format(candidate))
    print("Total tweets from corpus: {}\n".format(total_tweets_per_candidate[candidate]))
    print("Ratio of Pos:Neg : {}:{}\n".format(sentiment_counts_per_candidate[candidate]['pos'],sentiment_counts_per_candidate[candidate]['neg']))
    print("\n ------------------------------------------------------------------------------------------------------\n")
    print("Total tweets examined: {}\n".format(total_tweets))
