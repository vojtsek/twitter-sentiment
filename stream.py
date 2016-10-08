from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import sys

class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            print (tweet["text"])
        except Exception:
            pass
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    # auth = OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    auth = OAuthHandler("mXGTwaLOFqU4T28nUywSnpc1o", "GUFlX9a26MQqREaffhqU9KDPZnoZmlqgZ8XDYrGVH6GvN4EhS6")
    auth.set_access_token("880950271-aBZRRjHXgK9h6WAnBXWDVnsw8hlR6Yzsepv0uRx2",
                          "aiEEYYH6gHxZ4cLZOQZrOYvWFTW9cJ5OG6wXVKQ9P1FEV")
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=[sys.argv[1]], languages=["en"])
