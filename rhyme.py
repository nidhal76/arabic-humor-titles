#encoding: utf-8
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
		pronOUnciation =  esng.g2p(token, ipa=2)
		start_sounds.append(pronOUnciation[0])
	print start_sounds

	n_of_alliterating = 0
	n_of_non_alliterating = 0
	for sound in start_sounds:
		n = start_sounds.count(sound)
		if n == 1:
			n_of_non_alliterating += 1
		else:
			n_of_alliterating +=1
	return n_of_alliterating / float(n_of_non_alliterating +n_of_alliterating)

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

		pronOUnciation =  esng.g2p(token, ipa=2)
		pronunciations.append(pronOUnciation.replace(u"ˈ", ""))
	n_of_rhyming = 0
	n_of_non_rhyming = 0
	for sound in pronunciations:
		n = len(__get_similar(sound, pronunciations))
		if n == 1:
			n_of_non_rhyming += 1
		else:
			n_of_rhyming +=1
	return n_of_rhyming / float(len(tokens))


#print rhyme("No go hoe")
