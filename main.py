import tweepy
from tweepy import Stream
import logging
import json
import os.path as path
from collections import OrderedDict

import twitter_config
from stream_out_listener import StdOutListener

cities = ['San Francisco', 'New York', 'Boston', 'Los Angeles', 'Dallas', 'Miami']

countries = [
    ('San Francisco',),
    ("Tirana", "Albania"),
    ("Vienna", "Austria"),
    ("Brussels", "Belgium"),
    ("Sofia", "Bulgaria"),
    ("Prague", "Czech Republic"),
    ("Tallinn", "Estonia"),
    ("Helsinki", "Finland"),
    ("Berlin", "Germany"),
    ("Athens", "Greek"),
    ("Budapest", "Hungary"),
    ("Dublin", "Rome"),
    ("Rome", "Italy"),
    ("Vaduz", "Liechenstein"),
    ("Luxembourg", "Luxembourg"),
    ("Amsterdam", "Netherlands"),
    ("Warsaw", "Poland"),
    ("Bratislava", "Slovakia"),
    ("Madrid", "Spain"),
    ("London", "United Kingdom"),
    ("Berne", "Switzerland"),
]


class CountryTweets:

    def __init__(self, country, capital, cid, tweets=None):
        self.country = country
        self.capital = capital
        self.cid = cid
        if tweets is None:
            self.tweets = []
        else:
            self.tweets = tweets

    def append_tweets(self, tweets):
        self.tweets.extend(tweets)


def poly2bb(coords):
    longitudes = list(map(lambda x: x[0], coords))
    latitudes= list(map(lambda x: x[1], coords))
    sw_lat = min(latitudes)
    sw_long = min(longitudes)
    ne_lat = max(latitudes)
    ne_long = max(longitudes)
    return [sw_long, sw_lat, ne_long, ne_lat]


def place2coords(place, gran="city"):
    places = api.geo_search(query=place, granularity=gran)
    coords = places[0].bounding_box.coordinates
    return poly2bb(coords[0])


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.getLogger("tweetpy").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    logging.info('API authentization')
    auth = tweepy.OAuthHandler(twitter_config.CONSUMER_KEY, twitter_config.CONSUMER_SECRET)
    auth.set_access_token(twitter_config.ACCESS_TOKEN, twitter_config.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # for country in countries:
    BBOX_FILE = 'bboxes.json'
    if path.isfile(BBOX_FILE):
        logging.info('Using the cached bounding boxes from file %s', BBOX_FILE)
        bboxes = json.load(open(BBOX_FILE, 'r'))
    else:
        logging.info('Caching the bounding boxes into file %s', BBOX_FILE)
        bboxes = OrderedDict()
        for city in cities:
            try:
                place_bb = place2coords(city)
                bboxes[city] = place_bb
            except:
                print('err')
        json.dump(bboxes, open(BBOX_FILE, 'w'))

    logging.info('Creating stream')

    for city, locations in bboxes.items():
        logging.info('Getting tweets from %s (%s)', city, locations)
        stream = Stream(auth, StdOutListener("{}-tweets.out".format(city.split(" ")[0]), 5))
        stream.filter(locations=locations, languages=["en"], async=False)
