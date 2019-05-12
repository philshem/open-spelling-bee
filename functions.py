#!/usr/bin/env python

''' helper functions that are used between different parts of the code '''

import params

# check validity of provided letters
def check_letters(pzl):

	if len(pzl) != len(list(set(pzl))):
		print('Invalid count of letters requested.')
		print('Exiting...')
		exit(0)

	elif len(pzl) != params.TOTAL_LETTER_COUNT:
		print('Invalid count of letters requested.')
		print('Exiting...')
		exit(0)
	else:
		return

# smart sorting of letters, keeping first letter first
def sort_letters(pzl):
	return pzl[0] + ''.join(sorted(pzl[1:]))