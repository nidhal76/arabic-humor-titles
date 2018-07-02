#encoding: utf-8
import json, codecs
import random
from match_tweets_to_titles import clean_text
from alphabet_detector import AlphabetDetector


def get_rating_ids(file_path="/Users/mikahama/Downloads/title.ratings.csv", min_votes=100000):
	ids = {}
	f = open(file_path)
	f.readline()
	for line in f:
		parts = line.split("\t")
		votes = int(parts[2])
		id = parts[0]
		if votes > min_votes:
			ids[id] = votes
	json.dump(ids, open("imdb_ids_by_rating.json", "w"))

def get_titles(file_path="/Users/mikahama/Downloads/title.basics.tsv"):
	ids = json.load(codecs.open("imdb_ids_by_rating.json", "r", encoding="utf-8"))
	f = codecs.open(file_path)
	f.readline()
	titles = {}
	for line in f:
		parts = line.split("\t")
		id = parts[0]
		if id not in ids:
			continue
		title = parts[2]
		titles[title] = ids[id]
	json.dump(titles, codecs.open("imdb_titles.json", "w", encoding="utf-8"), indent=4)

def make_mt_data():
	ad = AlphabetDetector()
	source = codecs.open("data/mt/source.txt", "w", encoding="utf-8")
	target = codecs.open("data/mt/target.txt", "w", encoding="utf-8")
	source_valid = codecs.open("data/mt/source_valid.txt", "w", encoding="utf-8")
	target_valid = codecs.open("data/mt/target_valid.txt", "w", encoding="utf-8")
	mapped_titles = json.load(codecs.open("mapped_titles.json", "r", encoding="utf-8"))
	datas = list(mapped_titles.values())
	random.shuffle(datas)
	i = 0
	for data in datas:
		orig = data["tweet_clean"]
		humorous = data["matched_title"]
		if orig == humorous:
			continue
		if "ARABIC" in ad.detect_alphabet(orig):
			#skip the ones with arabic characters
			continue
		i += 1
		source.write(humorous + "\n")
		target.write(orig + "\n")
		if i % 5 == 0:
			source_valid.write(humorous + "\n")
			target_valid.write(orig + "\n")
	source.close()
	target.close()
	source_valid.close()
	target_valid.close()

def make_mt_test():
	titles = json.load(codecs.open("imdb_titles.json", "r", encoding="utf-8"))
	mt_test = codecs.open("data/mt/test.txt", "w", encoding="utf-8")
	for title in titles:
		mt_test.write(clean_text(title) + "\n")
	mt_test.close()



#get_rating_ids()
#get_titles()
make_mt_data()
#make_mt_test()