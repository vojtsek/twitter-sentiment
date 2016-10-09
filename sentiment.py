import indicoio
from glob import glob
from os import path
from preprocess import preprocess

indicoio.config.api_key = "93312f019163e78e178170ed04c89a31"

# single example


if __name__ == '__main__':
    for f_name in glob(path.join('out', 'raw_1k', '*.txt')):
        with open(f_name, 'r') as f:
            preprocessed = preprocess(f, 5)
            with open("{}.sentiment".format(f_name), 'w') as ff:
                for i, tweet in enumerate(preprocessed):
                    sentiment = indicoio.sentiment_hq(tweet)
                    ff.write(tweet)
                    ff.write('\n')
                    ff.write(str(sentiment))
                    ff.write('\n')
                    print i
