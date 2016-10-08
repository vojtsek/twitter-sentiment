import tweepy
from tweepy import Stream
import logging
import json
import os
import os.path as path
from collections import OrderedDict

import twitter_config
from tweet_writer_listener import TweetWriterListener


CITIES = ['San Francisco', 'New York', 'Boston', 'Los Angeles', 'Dallas', 'Miami']
OUT_DIR = 'out'
LIMIT = 10


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


def mkdir_if_not_exists(dir_name):
    try:
        os.makedirs(dir_name)
    except OSError:
        pass


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.getLogger("tweetpy").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    mkdir_if_not_exists(OUT_DIR)

    logging.info('API authentization')
    auth = tweepy.OAuthHandler(twitter_config.CONSUMER_KEY, twitter_config.CONSUMER_SECRET)
    auth.set_access_token(twitter_config.ACCESS_TOKEN, twitter_config.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # for country in countries:
    BBOX_FILE = path.join(OUT_DIR, 'bboxes.json')
    if path.isfile(BBOX_FILE):
        logging.info('Using the cached bounding boxes from file %s', BBOX_FILE)
        bboxes = json.load(open(BBOX_FILE, 'r'))
    else:
        logging.info('Caching the bounding boxes into file %s', BBOX_FILE)
        bboxes = OrderedDict()
        for city in CITIES:
            try:
                place_bb = place2coords(city)
                bboxes[city] = place_bb
            except:
                print('Coords error')
        json.dump(bboxes, open(BBOX_FILE, 'w'))

    logging.info('Creating stream')

    for city, locations in bboxes.items():
        logging.info('Getting tweets from %s (%s)', city, locations)
        with open(path.join(OUT_DIR, "{}_tweets.txt".format(city.replace(' ', ''))), 'a') as f_out:
            stream = Stream(auth, TweetWriterListener(f_out, LIMIT))
            stream.filter(locations=locations, languages=["en"], async=False)
