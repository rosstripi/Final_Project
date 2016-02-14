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

consumer_key        = "3cbQ7BUWxktCbCte32GlShgbl"
consumer_secret     = "BWjrIMQ9r5JuFRlm0W33CRXs9a8tNqCxO2om75izNE7T8LklrG"
# note: access tokens may have to be occasionally updated
access_token        = "351203594-B4esbGhxDgDvjimeywxWgKgAvPbssrtEkPscWOBW"
access_token_secret = "cBrDXuSXws7QL1Bh1zDFwxE8ny32pwa7dEgtrj43XMK7t"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            directory, link = self.queue.get()
            download_link(directory, link)
            self.queue.task_done()



class TweetListener(StreamListener):
    """Class to pull tweets as they appear"""
    filename = 'stream'

    def __init__(self, filename):
        self.filename = filename

    def on_data(self, data):
        try:
            with open('corpora/{}.json'.format(self.filename), 'a') as f:
                f.write(data)
                return True
        except BaseException as ex:
            print("Error on_data: %s" % str(ex))
        return True

    def on_error(self, status):
        print(status)
        return True


trump_stream = Stream(auth, TweetListener("trump")).filter(track=['#Trump'])
clinton_stream = Stream(auth, TweetListener("clinton")).filter(track=['#Clinton'])
cruz_stream = Stream(auth, TweetListener("cruz")).filter(track=['#Cruz'])
bush_stream = Stream(auth, TweetListener("bush")).filter(track=['#Bush'])
rubio_stream = Stream(auth, TweetListener("rubio")).filter(track=['#Rubio'])
kasich_stream = Stream(auth, TweetListener("kasich")).filter(track=['#Kasich'])
sanders_stream = Stream(auth, TweetListener("sanders")).filter(track=['#Sanders'])
