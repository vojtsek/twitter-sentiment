import os.path as path
from glob import glob
import logging
from lib.twokenize import tokenize


def preprocess(f, word_limit=0):
    preprocessed_lines = []

    for line in f.readlines():
        filtered_line = []

        for token in tokenize(line):
            if token.startswith('@') or\
               token.startswith(':') or\
               token.startswith('http'):
               continue
            if token.startswith('#'):
                filtered_line.append(token[1:])
            else:
                filtered_line.append(token)

        if word_limit <= len(filtered_line):
            preprocessed_lines.append(' '.join(filtered_line))

    return preprocessed_lines


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    from main import OUT_DIR

    for f_name in glob(path.join(OUT_DIR, 'raw_1k', '*.txt')):
        with open(f_name, 'r') as f:
            print(len(preprocess(f, 10)))
