# Geo Tweet Sentiment Analysis
Tiny project that analyses the sentiment of the tweets corresponding to various locations.

## Pipeline
- In `main.py` locations of cities are obtained from the Twitter API. Then the bounding boxes are computed and stored in `out/raw_1k/bboxes.json`.
- Afterwards a thousand of tweets from a particular location are downloaded and stored in the respective file.
- In the next step the minor preprocessing and filtering are applied.
- Then, the sentiment of each tweet is estimated using `sentiment.py` (via [indico.io](https://indico.io/) API). The sentiment itself is expressed as a number between 0 and 1.
- Finally, `visualize.py` plots the distribution of sentiment for each city. The sentiment is divided into 5 categories - strongly negative, mildly negative, neutral, midly positive and strongly positive. Each city is represented by a pie chart demonstrating the distribution of the sentiment.

## Example Output
![USA Tweet Sentiment](https://raw.githubusercontent.com/vojtsek/twitter-sentiment/master/awesome_result2.jpg "USA Tweet Sentiment")

## Discussion
According to [indico.io](https://indico.io/) sentiment analysis, the sentiment dstribution of tweets around USA is pretty similar, however, one may find minor differences when taking a closer look.

## Authors
- [Vojtěch Hudeček](https://github.com/vojtsek)
- [Petr Bělohlávek](https://github.com/petrbel)

Thanks to developers of `twokenize` and others.
