import indicoio
import sys
indicoio.config.api_key = "93312f019163e78e178170ed04c89a31"

# single example
fn = sys.argv[1]
with open(fn + ".out", "w") as fout:
    with open(fn, "r") as f:
        for line in f.readlines():
            if len(line) < 25:
                continue

            sent = indicoio.sentiment_hq(line)
            fout.write("{}-{}\n".format(line, sent))