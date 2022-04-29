#!/usr/bin/env python3

''' parameter file for generate_puzzles.py '''

import os

# how many games to generate, and max number of attempts to try
PUZZLE_COUNT = 1000
MAX_PUZZLE_TRIES = 100000

# file paths
WORD_LIST_PATH = 'word_lists' + os.sep + 'scowl.txt'
PUZZLE_DATA_PATH = 'data'

# multithreading if more than 1
THREADS = 1

# set minimum word length and total letters used
MIN_WORD_LENGTH = 4
TOTAL_LETTER_COUNT = 7

VOWEL_LIST = ('A', 'E', 'I', 'O', 'U')

# set count of pangrams (suggested = 1)
COUNT_PANGRAMS = 1

# word count limits
MIN_WORD_COUNT = 25
MAX_WORD_COUNT = 50

# Reject games with too many plural pairs (-S)
CAP_PLURALS = True
MAX_PLURALS = 3


# Reject games with too many gerund pairs (-ING)
CAP_GERUNDS = True
MAX_GERUNDS = 5

# total score limits
MIN_TOTAL_SCORE = 60
MAX_TOTAL_SCORE = 240

# Show rejected games as well as valid ones.
# True, False, or "dots", or "why".
PRINT_INVALID = "dots"        # "dots" simply prints a dot per invalid game.
PRINT_INVALID = "why"         # "why" prints % stats for invalid games.
