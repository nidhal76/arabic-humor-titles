# -*- coding: utf-8 -*-
import json
import codecs
import os
from gensim.models.word2vec import Word2Vec as w
from gensim.models.keyedvectors import KeyedVectors


def abs_path(fn):
    return os.path.join(os.path.dirname(__file__), './' + fn)


def read_json(file_path):
    return json.load(codecs.open(abs_path(file_path), 'r', encoding='utf-8'))


def load_w2v_model(model_path, binary=True):
    try:
        model = KeyedVectors.load_word2vec_format(model_path, binary=binary)
    except:
        model = w.load(model_path)
    return model

    # sim = model.similarity('dog', 'cat')
    #
    # res = model.most_similar_cosmul(positive=pos, negative=neg, topn=t)  # most similar
    # res_2 = model.most_similar(positive=pos, negative=neg, topn=t)
    # not_sim = model.doesnt_match(['word', 'word', 'word'])  # not match
    # sim = model.similarity('word', 'word')  # word similarity
    # n_sim = model.n_similarity('word', 'word')
