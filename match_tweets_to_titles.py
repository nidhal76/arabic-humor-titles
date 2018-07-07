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


def get_imdb_movies(file_path='./data/title.basics.tsv'):
    return read_csv(file_path, delimiter='\t')


def clean_text(text, lowercase=True):
    # remove hashtags
    if lowercase:
        text = text.lower()
    text = re.sub(r'#([a-zA-Z0-9\_]+)?', '', text)
    text = re.sub(r'@([a-zA-Z0-9\_]+)?', '', text)
    text = re.sub(r"http\S+", '', text)
    text = re.sub(r'[^\w\s]', '', text)  # remove special characters

    words = text.split()

    # remove twittercom ... urls when they are spaced
    words = filter(lambda _w: 'twittercom' not in _w, words)
    words = filter(lambda _w: 'rt' != _w, words)  # remove RT
    words = filter(lambda _w: not re.search('(\d){18}', _w), words)

    text = ' '.join(words)

    return text


def main():
    start = time.time()
    tweets = list(get_tweets())  # get tweets

    movies = json.load(codecs.open('./data/imdb_titles.json', 'r', encoding='utf-8'))  # get movie titles
    movie_titles = list(movies.keys())

    # comment out to use entire IMDB
    # movies = list(get_imdb_movies())
    # movie_titles = list(map(lambda _m: _m['originalTitle'], movies))

    # movie title without episode
    movie_titles_without_eps = filter(lambda _title: '-' in _title, movie_titles)
    movie_titles_without_eps = map(lambda _title: _title.split('-')[0].strip(), movie_titles_without_eps)
    movie_titles_without_eps = list(movie_titles_without_eps)

    # short title
    short_movie_titles = filter(lambda _title: ':' in _title, movie_titles)
    short_movie_titles = map(lambda _title: _title.split(':')[0].strip(), short_movie_titles)
    short_movie_titles = list(short_movie_titles)

    movies = list(set(movie_titles + movie_titles_without_eps + short_movie_titles))

    result = {}

    # for each tweet, find closest movie title
    for tweet in tweets:
        tweet_clean_text = clean_text(tweet['text'])

        if not tweet_clean_text.strip():
            continue

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

        # at most 3 words difference and diff must be less than # of words in the tweet
        if closest_dist_word <= 3 and closest_dist_word < len(tweet_clean_text.split(' ')):
            print(tweet_clean_text, '\t', closest, '\t', closest_dist)
            result[tweet['id']] = {
                'tweet': tweet['text'],
                'tweet_clean': tweet_clean_text,
                'matched_title': closest,
                'dist_char': closest_dist,
                'dist_word': closest_dist_word
            }

    end = time.time()

    json.dump(result, codecs.open("./data/mapped_titles.json", "w", encoding="utf-8"), indent=4)

    print(end - start)
    # find closest title to tweet


if __name__ == '__main__':
    main()
