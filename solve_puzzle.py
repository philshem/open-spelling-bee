#!/usr/bin/env python3

''' solve (cheat) puzzles '''

import params
import utils

import os
import sys

def solve(p):

    print ('letters:', p.get('letters',None))
    print ('total_score:', p.get('total_score',''))
    print ('word_count:', p.get('word_count',''))
    print ('pangram(s):', ', '.join(p.get('pangram_list',[])))
    print ()

    # print all answers
    for x in p.get('word_list',[]):
        score = x.get('score')

        # add 7 points if word is pangram
        if x.get('word') in p.get('pangram_list',[]):
            score += + 7
        utils.print_table((x.get('word'),score), 2, 10)

    return

def main():
    
    # try to read an existing or new puzzle from command line (not required)
    try:
        puzzle_idx = sys.argv[1].strip().upper()
    except:
        print ('Please enter a puzzle. Exiting...')
        exit(0)

    if puzzle_idx is not None:
        
        # check validity of letters
        utils.check_letters(puzzle_idx)

        # choose standard sorting for all puzzle file names
        puzzle_idx = utils.sort_letters(puzzle_idx)

    # select puzzle, generate it if it doesn't exist
    puzl_path = utils.select_puzzle(puzzle_idx)

    # load json puzzle data
    puzl = utils.read_puzzle(puzl_path)

    # solve puzzle (cheat mode)
    solve(puzl)

if __name__ == "__main__":

    main()
 
