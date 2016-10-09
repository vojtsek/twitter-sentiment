# Geo tweet sentiment analysis
Tiny project that analyses how sentiment of tweets corresponds to location.

In *main.py* locations of cities is obtained from twitter API
and bounding boxes are computed and stored in *out/raw_1k/bboxes.json*.
Afterwards tweets from particular location are downloaded and stored in respective file.

Then sentiment of each tweet is estimated using *sentiment.py*.
Sentiment is expressed as number between 0 and 1.

Finally *visualize.py* plots the distribution of sentiment for each city.
