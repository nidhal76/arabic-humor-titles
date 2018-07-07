#encoding: utf-8
import codecs, json, os, fnmatch, glob
import xml.etree.cElementTree as ET
import urllib2, urllib
import justext, nltk
from match_tweets_to_titles import clean_text

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

def extract_arabic_words(oed_path="/Users/mikahama/neologismi/oed"):
	result = {}
	for file in find_files(oed_path+ "/dictionary.json/", "words.json"):
		data = json.load(codecs.open(file, "r", encoding="utf-8"))
		for item in data:
			lemma = item["lemma"]
			if "etymology" in item:
				etymon = item["etymology"] 
				if "etymon_language" in etymon:
					lang_lists = etymon["etymon_language"]
					for lang_list in lang_lists:
						if "Arabic" in lang_list:
							result[lemma] = item["parts_of_speech"]
							break
	json.dump(result, codecs.open("arabic_words_list.json", "w", encoding="utf-8"), indent=4)

def bnc_frequencies(bnc_path="/Users/mikahama/neologismi/bnc/Texts/"):
	files = glob.glob(bnc_path+"*/*/*.xml")
	freqs = {}
	for file in files:
		tree = ET.parse(file)
		root = tree.getroot()
		texts = root.findall("wtext")
		for text in texts:
			sentences = text.getiterator("s")
			for sentence in sentences:
				words = sentence.getiterator("w")
				for word in words:
					w = word.text
					if w is not None:
						if w not in freqs:
							freqs[w] = 0
						freqs[w] += 1
	json.dump(freqs, codecs.open("data/bnc_frequencies.json", "w", encoding="utf-8"), indent=4)

def find_wikipedia_pages():
	words = json.load(codecs.open("arabic_words_list.json", "r", encoding="utf-8"))
	wiki_results = codecs.open("data/wikipages.xml", "w", encoding="utf-8")
	wiki_results.write("<root>")
	for word in words:
		url = "https://en.wikipedia.org/w/api.php?action=opensearch&search="+urllib.quote(word.encode('utf8'))+"&format=xml"
		try:
			response = urllib2.urlopen(url)
			data = response.read()
			wiki_results.write(data.decode('utf-8'))
		except:
			print word
	wiki_results.write("</root>")
	wiki_results.close()

def list_wiki_urls():
	text = codecs.open("data/wikipages.xml", "r", encoding="utf-8").read()
	i = text.find("<Url")
	while i != -1:
		text = text[i:]
		a = text.find(">")
		text = text[a+1:]
		a = text.find("<")
		url = text[:a]
		print url
		i = text.find("<Url")

def __get_keywords(file, bnc_frequencies, keyword_dict={}, ignore_capitalized=False):
	f = codecs.open(file, "r", encoding="utf-8").read()
	paragraphs = justext.justext(f, justext.get_stoplist("English"))
	freqs = {}
	text_freqs = {}
	for paragraph in paragraphs:
		if not paragraph.is_boilerplate:
			tokens = nltk.word_tokenize(clean_text(paragraph.text, not ignore_capitalized))
			for token in tokens:
				if ignore_capitalized and token != token.lower():
					continue
				if token not in text_freqs:
					text_freqs[token] = 0
				if token in freqs:
					text_freqs[token] += 1
					continue
				elif token in bnc_frequencies:
					freqs[token] = bnc_frequencies[token]
					text_freqs[token] += 1
				else:
					freqs[token] = 0
					text_freqs[token] += 1
	for f_key, f_value in text_freqs.iteritems():
		if f_value < 2:
			del freqs[f_key]
	x = len(freqs.keys())/10
	for i in range(x):
		min_word = min(freqs, key=freqs.get)
		if min_word not in keyword_dict:
			keyword_dict[min_word] = 0
		keyword_dict[min_word] += text_freqs[min_word]
		del freqs[min_word]


def get_extended_arabic_words():
	bnc = json.load(codecs.open("data/bnc_frequencies.json", "r", encoding="utf-8"))
	files = glob.glob("data/arabic_wikipedia/*")
	keyword_dict = {}
	for file in files:
		__get_keywords(file, bnc,keyword_dict)
	json.dump(keyword_dict, codecs.open("data/more_arabic.json", "w", encoding="utf-8"), indent=4)

def get_keywords_for_file(file):
	bnc = json.load(codecs.open("data/bnc_frequencies.json", "r", encoding="utf-8"))
	kw = {}
	__get_keywords(file, bnc, kw, True)
	return kw

print get_keywords_for_file("data/sex_and_the_city_plot.txt")
#get_extended_arabic_words()
#extract_arabic_words()
#bnc_frequencies()
#find_wikipedia_pages()
#list_wiki_urls()



