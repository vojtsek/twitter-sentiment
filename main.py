import tweepy
import pickle as pck
import logging
import sys
import json

countries = [
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
    latitudes = list(map(lambda x: x[0], coords))
    longitudes = list(map(lambda x: x[1], coords))
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

    logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(__name__)
#
    auth = tweepy.OAuthHandler("mXGTwaLOFqU4T28nUywSnpc1o", "GUFlX9a26MQqREaffhqU9KDPZnoZmlqgZ8XDYrGVH6GvN4EhS6")
    auth.set_access_token("880950271-aBZRRjHXgK9h6WAnBXWDVnsw8hlR6Yzsepv0uRx2", "aiEEYYH6gHxZ4cLZOQZrOYvWFTW9cJ5OG6wXVKQ9P1FEV")
#
    api = tweepy.API(auth)

    for country in countries:
        try:
            place_bb = place2coords(country[0])
            with open("bboxes.out", "a") as f:
                f.write("{},{}\n".format(country[0], place_bb))
        except:
            pass

