# encoding: utf-8
from espeakng import ESpeakNG

stops = ["a", "the", "and", "or", "of", "an"]
esng = ESpeakNG()
esng.voice = 'en-gb-x-rp'


def __get_tokens(title):
    tokens = title.lower().split(" ")
    tokens_to_test = []
    for token in tokens:
        if token not in stops:
            tokens_to_test.append(token)
    return tokens_to_test


def allitieration(title):
    tokens_to_test = __get_tokens(title)
    start_sounds = []
    for token in tokens_to_test:
        pronOUnciation = esng.g2p(token, ipa=2)
        start_sounds.append(pronOUnciation[0])
    print
    start_sounds

    n_of_alliterating = 0
    n_of_non_alliterating = 0
    for sound in start_sounds:
        n = start_sounds.count(sound)
        if n == 1:
            n_of_non_alliterating += 1
        else:
            n_of_alliterating += 1
    return n_of_alliterating / float(n_of_non_alliterating + n_of_alliterating)


def __get_similar(word, words):
    sims = []
    for w in words:
        if word == w:
            sims.append(w)
        elif len(word) > len(w) and word[-len(w):] == w:
            sims.append(w)
        elif len(word) < len(w) and w[-len(word):] == word:
            sims.append(w)
    return sims


def rhyme(title):
    consonants = "mnbvcxzlkjhgfdsptrwq"
    tokens = __get_tokens(title)
    unique_tokens = list(set(tokens))
    pronunciations = []
    for token in unique_tokens:
        if token[0] == "y":
            token = token[1:]
        while True:
            if token[0] in consonants:
                token = token[1:]
            else:
                break

        pronOUnciation = esng.g2p(token, ipa=2)
        pronunciations.append(pronOUnciation.replace(u"ˈ", ""))
    n_of_rhyming = 0
    n_of_non_rhyming = 0
    for sound in pronunciations:
        n = len(__get_similar(sound, pronunciations))
        if n == 1:
            n_of_non_rhyming += 1
        else:
            n_of_rhyming += 1
    return n_of_rhyming / float(len(tokens))


def assonance(ind):
    '''
    matching vowels.
    Returns:
    '''

    ARPABET_VOWELS = [u"ɑ", u"aɪ", u"aʊ", u"eɪ", u"i", u"oʊ", u"u", u"æ", u"ɔɪ", u"ɔ",u"ə", u"ɚ", u"ɛ", u"ɝ", u"ɨ", u"ɪ", u"ʉ", u"ʊ", u"ʌ"]

    _phones = phones(ind)
    _phones = list(map(lambda p: tuple([
        p[0],
        ' '.join(p[1])
    ]), _phones.items()))

    counts = defaultdict(int)
    for v in ARPABET_VOWELS:
        for w, p in _phones:
            if v in p:
                counts[v] += p.count(v)
    counts = list(filter(lambda d: d[1] >= 3, counts.items()))
    return counts

def espeak_ipa(word):
    ipa = esng.g2p(word, ipa=2).replace(u"ˈ", "").replace(u"ː", "")
    return [" ".join(ipa)]

def consonance(ind):
    '''
    matching vowels.
    Returns:
    '''

    ARPABET_VOWELS = [u"ɑ", u"aɪ", u"aʊ", u"eɪ", u"i", u"oʊ", u"u", u"æ", u"ɔɪ", u"ɔ",u"ə", u"ɚ", u"ɛ", u"ɝ", u"ɨ", u"ɪ", u"ʉ", u"ʊ", u"ʌ"]

    _phones = phones(ind)
    counts = defaultdict(int)
    for w, p in _phones.items():
        for _p in p:
            if _p not in ARPABET_VOWELS:  # phone isn't a vowel
                counts[_p] += 1
    counts = list(filter(lambda d: d[1] >= 3, counts.items()))
    return counts


#import pronouncing
import re
from nltk.corpus import stopwords
import operator
from functools import reduce
from collections import defaultdict

# stop words
stopwords = set(stopwords.words('english'))
# add punctuations
stopwords.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])


def ind_without_stop(ind):
    return list(filter(
        lambda _i: _i.lower() not in stopwords and not re.match('[\.,"\'\?!:;\(\)\[\]{}]+',
                                                                _i.lower()),
        ind))


def phones(ind, stress=False):
    '''
    Get the phones of every word in the slogan

    Returns: a dictionary mapping words in the slogan into their phones {word :  phones, ... }
    '''
    ind = ind_without_stop(ind)
    phones = list(map(lambda w: tuple([w, espeak_ipa(w)]), ind))
    phones = list(filter(lambda p: p[1], phones))
    phones = list(map(lambda p: tuple([p[0], p[1][0]]), phones))
    if not stress:
        phones = list(map(lambda p: tuple([p[0], unicode(filter(lambda _p: not _p.isdigit(), p[1]))]), phones))
    phones = list(map(lambda p: tuple([p[0], p[1].split()]), phones))
    return dict(phones)


def assonance_fn(ind):
    try:
        return sum(list(map(lambda x: x[1], assonance(ind)))) / float(
            len(set(reduce(operator.add, phones(ind).values()))))
    except:
        return 0.0


def consonance_fn(ind):
    try:
        return sum(list(map(lambda x: x[1], consonance(ind)))) / float(
            len(set(reduce(operator.add, phones(ind).values()))))
    except:
        return 0.0
# print rhyme("No go hoe")


