#!/usr/bin/env python

''' generate puzzles based on criteria in params.py '''

import params
import functions

import os
import sys
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

def make_puzzles(word_list, letters=None):
	
	if letters is not None:
		manual_puzzle = True
	else:
		manual_puzzle = False
		letters = get_letters()
		#letters = 'WAHORTY' # debug

	results = []
	if params.THREADS > 1:
		pool = ThreadPool(params.THREADS) 
		results = pool.starmap(check_words, zip(itertools.repeat(letters), word_list))
	else:
		for word in word_list:
			results.append(check_words(letters, word))

	# remove None from list
	results = list(filter(None.__ne__, results))

	# get total score of all words
	total_score = sum([x.get('score') for x in results])

	# generate list of pangrams
	pangram_list = list(filter(lambda x: x.get('pangram'), results))

	# check if generated answers are valid, based on params
	if not manual_puzzle and ((len(pangram_list) != params.COUNT_PANGRAMS) \
		or (total_score < params.MIN_TOTAL_SCORE or total_score > params.MAX_TOTAL_SCORE) \
		or (len(results) < params.MIN_WORD_COUNT or len(results) > params.MAX_WORD_COUNT)):
		# not valid! go to next letters (except when manual puzzle)
		# incorrect number of pangrams
		# OR total_score falls out of bounds
		# OR total number of words falls out of bounds
		print ('\t'.join((letters, str(len(results)), str(total_score), str(len(pangram_list)), str(0))))
		return 0

	print ('\t'.join((letters, str(len(results)), str(total_score), str(len(pangram_list)), str(1))))

	# if you made it this far, you have a valid word list
	# and the game will be recorded

	# WARNING! if puzzle already exists, it will be overwritten

	pangram_list = [x.get('word') for x in pangram_list ]

	generation_info = {
		'path' : params.WORD_LIST_PATH,
		'min_word_length' : params.MIN_WORD_LENGTH,
		'total_letter_count' : params.TOTAL_LETTER_COUNT,
		'min_word_count' : params.MIN_WORD_COUNT,
		'max_word_count' : params.MAX_WORD_COUNT,
		'min_total_score' : params.MIN_TOTAL_SCORE,
		'max_total_score' : params.MAX_TOTAL_SCORE,
		'count_pangrams' : params.COUNT_PANGRAMS,
		'manual_puzzle' : manual_puzzle,
	}

	tmp = {
			'letters' : letters, # key letter is always first in list
			'generation_info' : generation_info,
			'total_score' : total_score,
			'word_count' : len(results),
			'pangram_count' : len(pangram_list),
			'pangram_list' : pangram_list,
			'word_list' : results,
		}

	file_path = params.PUZZLE_DATA_PATH + os.sep + letters + '.json'
	with open(file_path, 'w') as json_file:
		json.dump(tmp, json_file, indent=4)

	return 1

def main(puzzle_input=None):

	words = get_words(params.WORD_LIST_PATH)
	#words = words[0:10000] #debug

	# header for csv output
	print ('\t'.join(('index', 'letters', 'word_count', 'total_score', 'pangram_count', 'is_valid')))

	if len(sys.argv) > 1:
		puzzle_input = sys.argv[1].strip().upper()
	else:
		puzzle_input = None

	# user has requested a specific puzzle be created		
	if puzzle_input is not None:		
		# check validity of letters
		functions.check_letters(puzzle_input)

		# manually request one puzzle by defining letters  on command line
		# alphabetize the non-center letters (all but first in array)
		puzzle_input = functions.sort_letters(puzzle_input)
		
		make_puzzles(words, puzzle_input)

	# user/code has no specific puzzle to create, generating many
	else:
		idx_valid = 0

		# generating N puzzles based on params
		for i in range(params.MAX_PUZZLE_TRIES):
			idx_valid += make_puzzles(words, None)

			# reached target count of puzzles, exiting loop
			if idx_valid >= params.PUZZLE_COUNT:
				exit(0)

	return puzzle_input

if __name__ == "__main__":
	main()
