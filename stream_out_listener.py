from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.error import TweepError, RateLimitError
import json
import sys
import twitter_config
import logging


class StdOutListener(StreamListener):


    def __init__(self, filename, limit):
        StreamListener.__init__(self)
        self.f = open(filename, "a")
        self.limit = limit
        self.name = filename
        self.counter = 0


    def __del__(self):
        logging.info("'%s' is done.", self.name)
        self.f.close()


    def on_data(self, data):
        try:
            tweet = json.loads(data)
            logging.info('Got: \t%s', tweet['text'])
            self.f.write("{}\n".format(tweet['text']))
            self.counter += 1
        except RateLimitError as e:
            print('except', e)
        except TweepError as e:
            print('except', e.reason, e.response, e.api_code)
        if self.counter >= self.limit:
            return False
        return True


    def on_error(self, status):
        print('err', status)
