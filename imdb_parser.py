#encoding: utf-8
import json, codecs

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


#get_rating_ids()
get_titles()