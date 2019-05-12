#!/usr/bin/env python

''' play puzzles based on params.py PUZZLE_PATH_READ value'''

import params
import generate_puzzles
import functions

import os
import sys
import json
import random
import glob

def main():
    pass

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
        print ('Puzzles must be ',str(params.TOTAL_LETTER_COUNT),'letters long. Please try again.')
        exit(0)

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

def play(puzl):
    print('Type !help or !h for help')

    letters = puzl.get('letters')
    print('Playing puzzle index:',letters)

#    letters = puzl.get('letters')
    print('Your letters are:',draw_letters_honeycomb(letters))

    word_list = puzl.get('word_list')
    pangram_list = puzl.get('pangram_list')
    # pangram is worth 7 extra points
    total_score = puzl.get('total_score') + 7 * int(puzl.get('pangram_count'))
    word_count = puzl.get('word_count')
    
    print ('Max score:',total_score)
    print ('Total words:', word_count)

    player_score = 0
    player_words = 0

    #print(word_list) # no cheating!

    guess_list = []
    player_pangram = False

    # loop until game ends
    while True:
        # ask user to guess a word
        guess = ask_user()

        # user need some help
        if guess.startswith('!'):
            help(guess, letters, guess_list, player_score, player_words, player_pangram, total_score, word_count)
            continue

        # already guessed that
        if guess in guess_list:
            print ('You already found:',guess)
            continue
        
        # guess less than minimum letters
        if len(guess) < params.MIN_WORD_LENGTH:
            print ('Guessed word is too short. Minimum length:',str(params.MIN_WORD_LENGTH))
            continue           

        # scenario 1: includes letter not in a list
        if any([x for x in guess if x not in letters]):
            print ('Invalid letter(s)')
            continue

        # scenario 2: doesn't include center letter but all letters valid
        if letters[0] not in guess:
            print ('Must include center letter:',letters[0])
            continue

        # find index of array for matching word, if any
        # https://stackoverflow.com/a/4391722/2327328
        word_index = next((index for (index, d) in enumerate(word_list) if d['word'] == guess), None)

        if word_index is None:
            # scenario 4: not a valid word
            print ('Sorry,',guess,'is not a valid word')
            continue
        elif guess in guess_list:
            # scenario 5: good word but already found
            print ('You already found',guess)
            continue
        else:
            # word is valid and found
            word_dict = word_list[word_index]

            player_words += 1

            word_score = word_dict.get('score')
            if word_dict.get('word') in pangram_list:
                # pangrams are worth +7 extra
                word_score += 7
                player_pangram = True
                guess += '*'

            player_score += word_score

            print_list = ['✓ '+guess, \
                'word score = '+str(word_score), \
                'words found = '+str(player_words) + '/'+str(word_count), \
                'total score = '+str(player_score) + '/'+str(total_score), \
                    ]

            # print success and running stats
            print_table(print_list, len(print_list), 22)

            # add good guess to the list, so it can't be reused
            guess_list.append(guess)
        
        # all words found (somehow this could be possible)
        if player_words == word_count:
            print ('Congratulations. You found them all!')

def print_table(data, cols, wide):
    '''Prints formatted data on columns of given width.'''
    # https://stackoverflow.com/a/50215584/2327328
    n, r = divmod(len(data), cols)
    pat = '{{:{}}}'.format(wide)
    line = '\n'.join(pat * cols for _ in range(n))
    last_line = pat * r
    print(line.format(*data))
    print(last_line.format(*data[n*cols:]))

def shuffle_letters(letters):
    # shuffles letters, excluding the center letter
    # random.shuffle() only works in place
    other_letters = list(letters[1:])
    random.shuffle(other_letters)
    return letters[0] + ''.join(other_letters)

def draw_letters_honeycomb(letters):
    
    # taken from http://ascii.co.uk/art/hexagon

    if len(letters) != 7:
        # simple one-line printing for now
        # currently not used
        return letters[0]+' '+''.join(letters[1:])

    hex_string = r'''
            _____
           /     \
          /       \
    ,----(    {2}    )----.
   /      \       /      \
  /        \_____/        \
  \   {1}    /     \    {3}   /
   \      /       \      /
    )----(    {0}'   )----(
   /      \       /      \
  /        \_____/        \
  \   {4}    /     \    {5}   /
   \      /       \      /
    `----(    {6}    )----'
          \       /
           \_____/
'''

    return hex_string.format(*letters)

def ask_user():
    text = input('Your guess: ')
    text = text.strip().upper()

    return text

def help(msg, letters, guess_list, player_score, player_words, player_pangram, total_score, word_count):
    
    # some features for
    clean_msg = msg.replace('!','')[0].lower()

    if clean_msg == 'q':
        print('Quitting...')
        exit(0)

    help_msg = '!i : instructions\n!g : show letters\n!f : shuffle letters\n!s : player stats\n!h : help\n!q : quit'
    instruction_msg = '''
    Welcome to the Open Source Spelling Bee puzzle!
    To play, build minimum ''' + str(params.MIN_WORD_LENGTH) + '''-letter words.
    Each word must include the center letter at least once.
    Letters may be used as many times as you'd like.

    Scoring: 1 point for a 4 letter word, and 1 more point for each word longer than 4 letters.
                Example:  WORD - 1 point
                          WORDS - 2 points
                          SPELLING - 5 points

    Each puzzle has ''' + str(params.COUNT_PANGRAMS) + ''' pangram(s) that uses each of the ''' + str(params.MIN_WORD_LENGTH) + ''' letters.
    The pangram is worth 7 extra points.

    Have fun!
    '''

    msg_dict = {
        'h' : help_msg,
        'i' : instruction_msg,
        'g' : draw_letters_honeycomb(letters),
        'f' : draw_letters_honeycomb(shuffle_letters(letters)),
        's' : 'guessed: '+', '.join(guess_list[::-1])+'\n'
                'player words: '+str(player_words)+' / '+str(word_count)+' ('+str(round(player_words*100.0/word_count,1))+'%)'+'\n'
                'player score: '+str(player_score)+' / '+str(total_score)+' ('+str(round(player_score*100.0/total_score,1))+'%)'+'\n'
                'pangram found: '+str(player_pangram),
    }

    print(msg_dict.get(clean_msg,'Unknown selection'))
    return

def main():
    
    # try to read an existing or new puzzle from command line (not required)
    try:
        puzzle_idx = sys.argv[1].strip().upper()
    except:
        puzzle_idx = None

    if puzzle_idx is not None:
        
        # check validity of letters
        functions.check_letters(puzzle_idx)

        # choose standard sorting for all puzzle file names
        puzzle_idx = functions.sort_letters(puzzle_idx)

    puzl_path = select_puzzle(puzzle_idx)

    puzl = read_puzzle(puzl_path)

    play(puzl)

if __name__ == "__main__":

    main()
 