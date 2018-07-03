# -*- coding: utf-8 -*-
import spacy
from common import *
import random

nlp = spacy.load('en')


def main():
    # load data
    movies = read_json('./imdb_titles.json')
    arabic_words = read_json('./arabic_words_list.json')

    movie_titles = list(movies.keys())
    ar_words = list(arabic_words.keys())

    for title in movie_titles:
        doc = nlp(title)  # parse
        tokens = list(map(lambda _t: (_t.i, _t.text, _t.pos_,), doc))
        to_change_tokens = list(filter(lambda _t: _t[2] in ['NOUN', 'ADJ', 'VERB'], tokens))

        if not to_change_tokens or len(tokens) <= 1:
            continue

        for _ in range(5):
            new_title = list(map(lambda _t: _t.text, doc))
            random_idx_to_replace = random.choice(to_change_tokens)

            new_title[random_idx_to_replace[0]] = random.choice(ar_words)
            print(new_title)


if __name__ == '__main__':
    main()
