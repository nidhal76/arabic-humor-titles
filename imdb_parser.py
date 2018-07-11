#encoding: utf-8
import json, codecs
import random
from match_tweets_to_titles import clean_text
from alphabet_detector import AlphabetDetector
from nltk import bigrams
import glob
from bs4 import BeautifulSoup

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
	json.dump(ids, open("data/imdb_ids_by_rating.json", "w"))

def get_titles(file_path="/Users/mikahama/Downloads/title.basics.tsv"):
	ids = json.load(codecs.open("data/imdb_ids_by_rating.json", "r", encoding="utf-8"))
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
	json.dump(titles, codecs.open("data/imdb_titles.json", "w", encoding="utf-8"), indent=4)

def __make_bigram_lists(title1, title2):
	t1 = title1.split(" ")
	t2 = title2.split(" ")
	add_to = None
	t3 = None
	if len(t1) < len(t2):
		t3 = t2[len(t1):]
		t2 = t2[:len(t1)]
		add_to = "t2"
	elif len(t2) < len(t1):
		t3 = t1[len(t2):]
		t1 = t1[:len(t2)]
		add_to = "t1"	
	if len(t1) == 1:
		b1 = [t1]
	else:
		b1 = list(bigrams(t1))
	if len(t2) == 1:
		b2 = [t2]
	else:
		b2 = list(bigrams(t2))
	if add_to is None:
		return b1, b2
	if add_to == "t2":
		last = b2.pop()
		a = list(last)
		a.extend(t3)
		b2.append(a)
	if add_to == "t1":
		last = b1.pop()
		a = list(last)
		a.extend(t3)
		b1.append(a)

	return b1, b2

def make_mt_data(bigrams=False):
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
		if not bigrams:
			source.write(humorous + "\n")
			target.write(orig + "\n")
			if i % 5 == 0:
				source_valid.write(humorous + "\n")
				target_valid.write(orig + "\n")
		if bigrams:
			source_grams, target_grams = __make_bigram_lists(humorous, orig)
			for x in range(len(source_grams)):
				source_gram = " ".join(source_grams[x])
				target_gram = " ".join(target_grams[x])
				source.write(source_gram + "\n")
				target.write(target_gram + "\n")
				if i % 5 == 0:
					source_valid.write(source_gram + "\n")
					target_valid.write(target_gram + "\n")
	source.close()
	target.close()
	source_valid.close()
	target_valid.close()

def make_mt_data_from_master(bigrams=False):
	ad = AlphabetDetector()
	source = codecs.open("data/mt/source.txt", "w", encoding="utf-8")
	target = codecs.open("data/mt/target.txt", "w", encoding="utf-8")
	source_valid = codecs.open("data/mt/source_valid.txt", "w", encoding="utf-8")
	target_valid = codecs.open("data/mt/target_valid.txt", "w", encoding="utf-8")
	mapped_titles = json.load(codecs.open("data/master-generated-titles-filtered.json", "r", encoding="utf-8"))
	keys = list(mapped_titles.keys())
	random.shuffle(keys)
	i = 0
	for key in keys:
		orig = clean_text(key.replace(".",""))
		humorous_ones = mapped_titles[key]
		if "output" not in humorous_ones:
			continue
		for humorous in humorous_ones["output"]:
			i += 1
			if "ARABIC" in ad.detect_alphabet(humorous):
				#skip the ones with arabic characters
				continue
			humorous = clean_text(humorous.replace(" .", ""))
			if not bigrams:
				target.write(humorous + "\n")
				source.write(orig + "\n")
				if i % 10 == 0:
					target_valid.write(humorous + "\n")
					source_valid.write(orig + "\n")
			if bigrams:
				source_grams, target_grams = __make_bigram_lists(humorous, orig)
				for x in range(len(source_grams)):
					source_gram = " ".join(source_grams[x])
					target_gram = " ".join(target_grams[x])
					source.write(source_gram + "\n")
					target.write(target_gram + "\n")
					if i % 10 == 0:
						source_valid.write(source_gram + "\n")
						target_valid.write(target_gram + "\n")
	source.close()
	target.close()
	source_valid.close()
	target_valid.close()

def make_url_list():
	d = json.load(codecs.open("data/imdb_titles_ids.json", "r", encoding="utf-8"))
	f = codecs.open("data/imdb_keyword_urls.txt", "w", encoding="utf-8")
	for id in d.values():
		f.write("https://www.imdb.com/title/"+id+"/keywords\n")
	f.close()

def make_keywords_json():
	files = glob.glob("data/imdb_keywords/*")
	results = {}
	for file in files:
		id, keywords = __parse_keywords(file)
		results[id] = keywords
	movie_titles = json.load(codecs.open("data/imdb_titles_ids.json", "r", encoding="utf-8"))
	res = {}
	for title, title_id in movie_titles.iteritems():
		res[title] = results[title_id]
	json.dump(res, codecs.open("data/imdb_titles_keywords.json", "w", encoding="utf-8"), indent=4)

def __parse_keywords(file):
	html = codecs.open(file, "r", encoding="utf-8").read()
	soup = BeautifulSoup(html, 'html.parser')
	id =""
	for link in soup.find_all('link', {"rel": "canonical"}):
		url_parts = link.get("href").split("/")
		id = url_parts[len(url_parts)-2]
		break
	keywords = []
	for keyword in soup.find_all("div", {"class":"sodatext"}):
		keywords.append(keyword.text.replace("\n",""))
	return id, keywords



def make_mt_test(bigrams=False):
	titles = json.load(codecs.open("data/imdb_titles.json", "r", encoding="utf-8"))
	mt_test = codecs.open("data/mt/test.txt", "w", encoding="utf-8")
	for title in titles:
		t = clean_text(title)
		if bigrams:
			b1, b2 = __make_bigram_lists(t, t)
			for bigram in b1:
				mt_test.write(" ".join(bigram) + "\n")
		else:
			mt_test.write(t + "\n")
	mt_test.close()

#print __parse_keywords("data/imdb_keywords/keywords")
#make_keywords_json()
#make_mt_data_from_master()
make_mt_test()
#print __make_bigram_lists("taxi driver and me", "hijaabi driver and sheik and great")
#get_rating_ids()
#get_titles()
#make_url_list()
#make_mt_data(True)
#make_mt_test(True)