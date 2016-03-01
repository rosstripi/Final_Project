"""
Training Set Builder for Final Project
author: Ross Tripi
"""

import tweepy, json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import os

consumer_key        = "3cbQ7BUWxktCbCte32GlShgbl"
consumer_secret     = "BWjrIMQ9r5JuFRlm0W33CRXs9a8tNqCxO2om75izNE7T8LklrG"
# note: access tokens may have to be occasionally updated
access_token        = "351203594-B4esbGhxDgDvjimeywxWgKgAvPbssrtEkPscWOBW"
access_token_secret = "cBrDXuSXws7QL1Bh1zDFwxE8ny32pwa7dEgtrj43XMK7t"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# terms for each candidate
carson_terms = ['#carson', 'carson', '#bencarson', 'ben carson']
clinton_terms = ['#clinton', 'clinton', '#hillary', 'hillary', '#hillaryclinton', 'hillary clinton']
cruz_terms = ['#cruz', 'cruz', '#tedcruz', 'ted cruz']
kasich_terms = ['#kasich', 'kasich', '#johnkasich', 'john kasich']
rubio_terms = ['#rubio', 'rubio', '#marco', 'marco', '#marcorubio', 'marco rubio']
sanders_terms = ['#sanders', 'sanders', '#bernie', 'bernie', '#berniesanders', 'bernie sanders']
trump_terms = ['#trump', 'trump', '#donald', 'donald', '#donaldtrump', 'donald trump']


class TweetListener(StreamListener):
    """Class to pull tweets as they appear"""

    def write_to_json(self, candidate, data):
        os.makedirs(os.path.dirname('training_sets/{}.json').format(candidate), exist_ok=True)
        with open('training_sets/{}.json'.format(candidate), 'a') as f:
            f.write(data)
            return True

    def on_data(self, data):
        try:
            jtweet = json.loads(data)
            if 'text' in jtweet:
                tweet_text = jtweet['text']
                tweet_text = tweet_text.lower()
                # if any(term in tweet_text for term in carson_terms):
                #     self.write_to_json('carson', data)
                # if any(term in tweet_text for term in clinton_terms):
                #     self.write_to_json('clinton', data)
                # if any(term in tweet_text for term in cruz_terms):
                #     self.write_to_json('cruz', data)
                if any(term in tweet_text for term in kasich_terms):
                    self.write_to_json('kasich', data)
                # if any(term in tweet_text for term in rubio_terms):
                #     self.write_to_json('rubio', data)
                # if any(term in tweet_text for term in sanders_terms):
                #     self.write_to_json('sanders', data)
                # if any(term in tweet_text for term in trump_terms):
                #     self.write_to_json('trump', data)
        except BaseException as ex:
            print("Error on_data: %s" % str(ex))
        return True

    def on_error(self, status):
        print(status)
        if status == 420:
            print("\tNumber of allowed connections for time window exceeded")
            return False  # returning False in on_data disconnects the stream
        return True


candidates_stream = Stream(auth, TweetListener()).filter(track=[
                                                                        #'#Carson', 'Carson', '#BenCarson', 'Ben Carson',
                                                                        #'#Clinton', 'Clinton', '#Hillary', 'Hillary', '#HillaryClinton', 'Hillary Clinton',
                                                                        #'#Cruz', 'Cruz', '#TedCruz', 'Ted Cruz',
                                                                        '#Kasich', 'Kasich', '#JohnKasich', 'John Kasich',
                                                                        #'#Rubio', 'Rubio', '#Marco', 'Marco', '#MarcoRubio', 'Marco Rubio',
                                                                        #'#Sanders', 'Sanders', '#Bernie', 'Bernie', '#BernieSanders', 'Bernie Sanders',
                                                                        #'#Trump', 'Trump', '#Donald', 'Donald', '#DonaldTrump', 'Donald Trump'
                                                                ])
