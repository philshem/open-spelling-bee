#!/usr/bin/env python

''' generate puzzles based on criteria in params.py '''

import params

import os
import string
import random
from multiprocessing import Pool as ThreadPool
import itertools
from collections import defaultdict
import json

def get_words(word_file):

	# https://github.com/jmlewis/valett/
	# https://raw.githubusercontent.com/jmlewis/valett/master/scrabble/sowpods.txt

	# http://scrabutility.com/TWL06.txt

	with open(params.WORD_LIST_PATH,'r') as wp:
		words = wp.readlines()

	# trim whitespace and remove short words
	words = [w.strip() for w in words if len(w.strip()) >= params.MIN_WORD_LENGTH]

	return words

def get_letters():

	alphabet_list = list(string.ascii_uppercase)

	while True:
		# generate sample of alphabet (can inlcude each letter only once)
		random_list = random.sample(alphabet_list, params.TOTAL_LETTER_COUNT)

		# make sure each letter list includes at least one vowel
		if [i for i in random_list if i in params.VOWEL_LIST]:
			return ''.join(random_list)

def check_words(letters, word):

	letters = list(letters)

	# filter logic: must include any letter from list, as well as the first item 
	if all(x in set(letters) for x in word) and letters[0] in word:

		# calculate the score of the word
		score = get_score(word)

		# check if word is pangram of letters
		if all(x in set(word) for x in letters):
			#print ('pangram:', word, letters)
			return {'word' : word , 'score' : score, 'pangram' : True}
		else:
			return {'word' : word , 'score' : score, 'pangram' : False}
	else:
		# no matching words found
		return None

def get_score(word):

	# simple scoring algorithm, for now
	return len(word) - params.MIN_WORD_LENGTH + 1

def make_games():
	pass

if __name__ == "__main__":

	words = get_words(params.WORD_LIST_PATH)
	
	#words = words[0:10000] #debug
	#words = ['AAHED']
	#print (words)

	puzl = []

	idx = 0
	for i in range(params.MAX_PUZZLE_TRIES):

		letters = get_letters()
		#letters = 'WAHORTY' # debug

		if params.THREADS > 1:
			pool = ThreadPool(params.THREADS) 
			results = pool.starmap(check_words, zip(itertools.repeat(letters), words))
		else:
			results = []
			for word in words:
				results.append(check_words(letters, word))

		# remove None from list
		results = list(filter(None.__ne__, results))

		# get total score of all words
		total_score = sum([x.get('score') for x in results])

		# generate list of pangrams
		pangram_list = list(filter(lambda x: x.get('pangram'), results))

		print (i, letters, len(results), total_score, len(pangram_list))

		# check if pangram count is allowed (default = 1)
		if len(pangram_list) > params.MAX_PANGRAMS or len(pangram_list) < params.MIN_PANGRAMS:
			# go to next letter group, incorrect number of pangrams
			continue

		elif total_score < params.MIN_TOTAL_SCORE or total_score > params.MAX_TOTAL_SCORE:
			# go to next letter group, total_score falls out of bounds
			continue

		elif len(results) < params.MIN_WORD_COUNT or len(results) > params.MAX_WORD_COUNT:
			# go to next letter group, total number of words falls out of bounds
			continue

		# if you made it this far, you have a valid word list
		# and the game will be recorded
		idx += 1
		
		pangram_list = [x.get('word') for x in pangram_list ]

		puzl.append({
				'index' : idx,
			    'letters' : letters,
				'total_score' : total_score,
				'word_count' : len(results),
				'pangram_list' : pangram_list,
				'pangram_count' : len(pangram_list),
				'word_list' : results,
			})

		if len(puzl) >= params.PUZZLE_COUNT:
			# reached target count of puzzles, exiting loop
			break

	if len(puzl) > 0:
		with open(params.PUZZLE_PATH, 'w') as json_file:
			json.dump(puzl, json_file, indent=4)
	
	#print (puzl)
