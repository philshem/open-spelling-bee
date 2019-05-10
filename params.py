#!/usr/bin/env python

''' parameter file for generate_puzzles.py '''

import os

THREADS = 1

# how many games to generate, and max number of attempts to try
PUZZLE_COUNT = 100
MAX_PUZZLE_TRIES = 100000

# file paths
WORD_LIST_PATH = 'data' + os.sep + 'TWL06.txt'
PUZZLE_PATH = 'data'+os.sep+'puzzles.json'

# set minimum word length and total letters used
MIN_WORD_LENGTH = 4
TOTAL_LETTER_COUNT = 7

VOWEL_LIST = ('A', 'E', 'I', 'O', 'U')

# set min and max for count of pangrams (suggested = 1)
MIN_PANGRAMS = 1
MAX_PANGRAMS = 1

# word count limits
MIN_WORD_COUNT = 30
MAX_WORD_COUNT = 50

# total score limits
MIN_TOTAL_SCORE = 80
MAX_TOTAL_SCORE = 120
