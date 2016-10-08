from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.error import TweepError, RateLimitError
import json
import sys
import twitter_config
import logging


class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            logging.info('\t%s', tweet['text'])
        except RateLimitError as e:
            print('except', e)
        except TweepError as e:
            print('except', e.reason, e.response, e.api_code)
        return True

    def on_error(self, status):
        print('err', status)
