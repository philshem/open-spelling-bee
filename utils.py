#!/usr/bin/env python3

''' helper functions that are used between different parts of the code '''

import params
import generate_puzzles

import os
import random
import json
import glob
import sys

# check validity of provided letters
def check_letters(pzl):

	if len(pzl) != len(list(set(pzl))):
		print('Invalid count of letters requested.', file=sys.stderr)
		print('Exiting...', file=sys.stderr)
		exit(1)

	elif len(pzl) != params.TOTAL_LETTER_COUNT:
		print('Invalid count of letters requested.', file=sys.stderr)
		print('Exiting...', file=sys.stderr)
		exit(1)
	else:
		return

# smart sorting of letters, keeping first letter first
def sort_letters(pzl):
	return pzl[0] + ''.join(sorted(pzl[1:]))


def select_puzzle(puzl_idx=None):

    puzzles = glob.glob(params.PUZZLE_DATA_PATH + os.sep + '*.json')
    puzl_idx_list = [x.split(os.sep)[-1].split('.')[0] for x in puzzles]

    # scenario 1: no selection made, so return a random puzzle
    if puzl_idx is None:
        # return a random puzzle
        puzl_path = random.choice(puzzles)
        print ('You selected a random puzzle:',puzl_path)
        return puzl_path

    if len(puzl_idx) != params.TOTAL_LETTER_COUNT:
        print ('Puzzles must be ',str(params.TOTAL_LETTER_COUNT),'letters long. Please try again.', file=sys.stderr)
        exit(1)

    # scenario 2: specific puzzle requested but not already available
    if puzl_idx in puzl_idx_list:
        print('Existing puzzle will be played:',puzl_idx)
        puzl_path = params.PUZZLE_DATA_PATH + os.sep + puzl_idx + '.json'
    # scenario 3: create a new puzzle because an existing one was not found
    else:
        puzl_idx = generate_puzzles.main(puzl_idx)
        print ('You created a new puzzle:',puzl_idx)
        puzl_path = params.PUZZLE_DATA_PATH + os.sep + puzl_idx + '.json'
    
    return puzl_path

def read_puzzle(puzl_path):

    with open(puzl_path,'r') as fp:
        puzzles = json.load(fp)

    #print(len(puzzles.get('letters'),'total puzzle(s) were loaded')

    return puzzles

def print_table(data, cols, wide):
    '''Prints formatted data on columns of given width.'''
    # https://stackoverflow.com/a/50215584/2327328
    n, r = divmod(len(data), cols)
    pat = '{{:{}}}'.format(wide)
    line = '\n'.join(pat * cols for _ in range(n))
    sys.stdout.reconfigure(encoding="utf-8")
    print(line.format(*data))
    #last_line = pat * r
    #print(last_line.format(*data[n*cols:]))
