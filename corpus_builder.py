"""
Tweet Corpus Builder for Final Project
author: Ross Tripi
"""

import tweepy
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


class TweetListener(StreamListener):
    """Class to pull tweets as they appear"""

    def on_data(self, data):
        try:
            os.makedirs(os.path.dirname('corpora/all_candidates.json'), exist_ok=True)
            with open('corpora/all_candidates.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as ex:
            print("Error on_data: %s" % str(ex))
        return True

    def on_error(self, status):
        print(status)
        if status == 420:
            print("\tNumber of allowed connections for time window exceeded")
            return False  # returning False in on_data disconnects the stream
        return True


candidates_stream = Stream(auth, TweetListener()).filter(track=['#Carson', 'Carson', '#BenCarson', 'Ben Carson',
                                                                        '#Clinton', 'Clinton', '#Hillary', 'Hillary', '#HillaryClinton', 'Hillary Clinton',
                                                                        '#Cruz', 'Cruz', '#TedCruz', 'Ted Cruz',
                                                                        '#Kasich', 'Kasich', '#JohnKasich', 'John Kasich',
                                                                        '#Rubio', 'Rubio', '#Marco', 'Marco', '#MarcoRubio', 'Marco Rubio',
                                                                        '#Sanders', 'Sanders', '#Bernie', 'Bernie', '#BernieSanders', 'Bernie Sanders',
                                                                        '#Trump', 'Trump', '#Donald', 'Donald', '#DonaldTrump', 'Donald Trump'])

