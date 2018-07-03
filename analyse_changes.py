# -*- coding: utf-8 -*-
from collections import defaultdict
import spacy
from common import *

nlp = spacy.load('en')


def main():
    stats = defaultdict(lambda: defaultdict(int))
    titles = read_json('./data/mapped_titles.json')
    for tweet_id, data in titles.items():
        original_title = data['matched_title']
        tweet = data['tweet_clean']

        # add a full stop at the end of the sentence to indicate that it is a complete sentence
        # improves parsing text
        original_title = original_title + '.'
        tweet = tweet + '.'

        # parse
        doc_o = nlp(original_title)
        doc_t = nlp(tweet)

        tokens_o = list(map(lambda _t: _t.text, doc_o))

        # find changed tokens
        for token in doc_t:

            # ignore tokens that exist in original title
            if token.text in tokens_o:
                continue

            stats['POS'][token.pos_] += 1

    print(stats)
    ''' Results:
    {'NOUN': 1537, 'ADJ': 303, 'ADP': 73, 'NUM': 66, 'VERB': 225, 'ADV': 54, 'PRON': 15, 'PART': 13,
              'PROPN': 18, 'X': 13, 'DET': 32, 'INTJ': 7, 'CCONJ': 16, 'PUNCT': 5}
    '''

    if __name__ == '__main__':
        main()
