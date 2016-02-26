"""
Tweet Corpus Builder for Final Project
author: Ross Tripi
"""

from queue import Queue
from threading import Thread
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
    filename = 'stream'

    def __init__(self, filename):
        self.filename = filename

    def on_data(self, data):
        try:
            os.makedirs(os.path.dirname('corpora/{}.json'.format(self.filename)), exist_ok=True)
            with open('corpora/{}.json'.format(self.filename), 'a') as f:
                f.write(data)
                return True
        except BaseException as ex:
            print("Error on_data: %s" % str(ex))
        return True

    def on_error(self, status):
        print(status)
        if status == 420:
            print("\tNumber of allowed connections for time window exceeded for " + self.filename)
            return False  # returning False in on_data disconnects the stream
        return True


def carson_fetch():
    carson_stream = Stream(auth, TweetListener("carson")).filter(track=['#Carson'], async=True)


def clinton_fetch():
    clinton_stream = Stream(auth, TweetListener("clinton")).filter(track=['#Clinton'], async=True)


def cruz_fetch():
    cruz_stream = Stream(auth, TweetListener("cruz")).filter(track=['#Cruz'], async=True)


def kasich_fetch():
    kasich_stream = Stream(auth, TweetListener("kasich")).filter(track=['#Kasich'], async=True)


def rubio_fetch():
    rubio_stream = Stream(auth, TweetListener("rubio")).filter(track=['#Rubio'], async=True)


def sanders_fetch():
    sanders_stream = Stream(auth, TweetListener("sanders")).filter(track=['#Sanders'], async=True)


def trump_fetch():
    trump_stream = Stream(auth, TweetListener("trump")).filter(track=['#Trump'], async=True)


carson_thread = Thread(target=carson_fetch)
clinton_thread = Thread(target=clinton_fetch)
cruz_thread = Thread(target=cruz_fetch)
kasich_thread = Thread(target=kasich_fetch)
rubio_thread = Thread(target=cruz_fetch)
sanders_thread = Thread(target=sanders_fetch)
trump_thread = Thread(target=trump_fetch)

carson_thread.start()
clinton_thread.start()
cruz_thread.start()
kasich_thread.start()
rubio_thread.start()
sanders_thread.start()
trump_thread.start()
