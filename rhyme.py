#encoding: utf-8
from espeakng import ESpeakNG

stops = ["a", "the", "and", "or", "of", "an"]
esng = ESpeakNG()
esng.voice = 'en-gb-x-rp'


def allitieration(title):
	tokens = title.lower().split(" ")
	tokens_to_test = []  
	for token in tokens:
		if token not in stops:
			tokens_to_test.append(token)
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
		

#print allitieration("Beauty and the Beast OK OK")
