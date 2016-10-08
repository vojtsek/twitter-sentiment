import json
import logging

from tweepy.streaming import StreamListener
from tweepy.error import TweepError, RateLimitError


class TweetWriterListener(StreamListener):
    def __init__(self, f_out, limit, progress_frequency=10):
        StreamListener.__init__(self)
        self.f_out = f_out
        self.limit = limit
        self.counter = 0
        self.progress_frequency = progress_frequency

    def __del__(self):
        logging.info('Stream finished after %d/%d tweets saved', self.counter, self.limit)

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            tweet_text = tweet['text'].replace('\n', ' ')
            logging.debug('Got: \t%s', tweet_text)
            self.f_out.write('{}\n'.format(tweet_text))
            self.f_out.flush()
            self.counter += 1
            if self.counter % self.progress_frequency == 0:
                logging.info('Tweet {}/{}', self.counter, self.limit)
        except RateLimitError:
            logging.warning('RateLimitError, sleeping for 15min')
        except TweepError as e:
            logging.error('TweepError - reason: %s; response: %s; api_code: %s', e.reason, e.response, e.api_code)
        except UnicodeEncodeError:
            logging.warning('Couldn\'t parse accepted tweet {}/{}, ignoring', self.counter, self.limit)
        except RuntimeError as e:
            logging.error('Unexpected error: %s', e)

        return self.counter < self.limit

    def on_error(self, status):
        logging.error('Stream error: %d', status)
