# -*- coding: utf-8 -*-
import sys, codecs
import csv
import time
import re
import json
import editdistance


def read_csv(file_path, delimiter=','):
    with codecs.open(file_path, "r", "utf-8") as tweets_file:
        reader = csv.DictReader(tweets_file, delimiter=delimiter)
        for line in reader:
            yield line


def get_tweets(file_path='./data/saudimovietitles-tweets.csv'):
    return read_csv(file_path, delimiter=';')


def clean_text(text):
    # remove hashtags
    text = text.lower()
    text = re.sub(r'#([a-zA-Z0-9\_]+)?', '', text)
    text = re.sub(r'@([a-zA-Z0-9\_]+)?', '', text)
    text = re.sub(r"http\S+", '', text)
    text = re.sub(r'[^\w\s]', '', text)

    words = text.split()

    # remove twittercom ... urls when they are spaced
    words = filter(lambda _w: 'twittercom' not in _w, words)
    words = filter(lambda _w: not re.search('(\d){18}', _w), words)

    text = ' '.join(words)

    return text


def main():
    start = time.time()
    tweets = list(get_tweets())  # get tweets

    movies = json.load(codecs.open('./imdb_titles.json', 'r', encoding='utf-8'))  # get movie titles
    movie_titles = list(movies.keys())

    # movie title without episode
    movie_titles_without_eps = filter(lambda _title: '-' in _title, movie_titles)
    movie_titles_without_eps = map(lambda _title: _title.split('-')[0].strip(), movie_titles_without_eps)
    movie_titles_without_eps = list(movie_titles_without_eps)

    # short title
    short_movie_titles = filter(lambda _title: ':' in _title, movie_titles)
    short_movie_titles = map(lambda _title: _title.split(':')[0].strip(), short_movie_titles)
    short_movie_titles = list(short_movie_titles)

    movies = list(set(movie_titles + movie_titles_without_eps + short_movie_titles))

    # for each tweet, find closest movie title
    for tweet in tweets:
        tweet_clean_text = clean_text(tweet['text'])
        closest = tweet_clean_text
        closest_dist = sys.maxsize
        closest_dist_word = sys.maxsize

        for movie in movies:
            movie_title = clean_text(movie)

            # calculate edit distance

            dist = editdistance.eval(tweet_clean_text, movie_title)
            # split(' ') to measure edit distance using words instead of characters
            dist_word = editdistance.eval(tweet_clean_text.split(' '), movie_title.split(' '))

            if dist_word < closest_dist_word:
                closest_dist = dist
                closest_dist_word = dist_word
                closest = movie_title
            elif dist_word == closest_dist_word and dist < closest_dist:
                closest_dist = dist
                closest_dist_word = dist_word
                closest = movie_title
        if closest_dist_word <= 3 and closest_dist_word < len(tweet_clean_text.split(' ')):
            print(tweet_clean_text, '\t', closest, '\t', closest_dist)
    end = time.time()

    print(end - start)
    # find closest title to tweet


if __name__ == '__main__':
    main()
