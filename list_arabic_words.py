#encoding: utf-8
import codecs, json, os, fnmatch

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

def extract_arabic_words(oed_path="/Users/mikahama/neologismi/oed"):
	result =[]
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
							result.append(lemma)
							break
	json.dump(result, codecs.open("arabic_words_list.json", "w", encoding="utf-8"), indent=4)

extract_arabic_words()
