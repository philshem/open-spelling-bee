#!/usr/bin/env python

''' play puzzles based on params.py PUZZLE_PATH_READ value'''

import params

import sys
import json
import random

def main():
    pass

def read_puzzles():

    with open(params.PUZZLE_PATH_READ,'r') as fp:
        puzzles = json.load(fp)

    print(len(puzzles),'total puzzle(s) were loaded')

    return puzzles

def select_puzzle(puzzles, puzl_idx=None):

    if puzl_idx is None:
        # return a random puzzle
        puzl = random.choice(puzzles)
        print ('You selected a random puzzle, index:',str(puzzles.index(puzl)))

    elif puzl_idx <= len(puzzles) and puzl_idx > 0:
        # get puzzle with specific index
        #puzl_idx = [x for x in puzzles if x.get('index') == puzl_idx]
        puzl = puzzles[puzl_idx-1]
        print ('You selected puzzle index:',str(puzl_idx))
    else:
        print ('Invalid puzzle selection. There are',str(len(puzzles)),'puzzles to choose from.')
        exit(0)
    
    return puzl

def play(puzl):
    print('Type !help or !h for help')

    print('Playing puzzle index:',puzl.get('index'))

    letters = puzl.get('letters')
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
            print ('You already guessed:',guess)
            continue
        
        # guess less than minimum letters
        if len(guess) < params.MIN_WORD_LENGTH:
            print ('Guessed word is too short. Minimum length:',str(params.MIN_WORD_LENGTH))
            continue           

        # scenario 1: includes letter not in a list
        if any([x for x in guess if x not in letters]):
            print ('Invalid letter(s)')
            continue

        # scenario 2: doesn't include key letter but all letters valid
        if letters[0] not in guess:
            print ('Must include key letter:',letters[0])
            continue

        # find index of array for matching word, if any
        # https://stackoverflow.com/a/4391722/2327328
        word_index = next((index for (index, d) in enumerate(word_list) if d['word'] == guess), None)

        if word_index is None:
            # scenario 4: not a valid word
            print ('Sorry,',guess,'is not a valid word.')
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

def draw_letters_basic(letters):

    # simple one-line printing for now
    return letters[0]+' '+''.join(letters[1:])

def shuffle_letters(letters):
    # shuffles letters, excluding the center letter
    # random.shuffle() only works in place
    other_letters = list(letters[1:])
    random.shuffle(other_letters)
    return letters[0] + ''.join(other_letters)

def draw_letters_honeycomb(letters):
    hex_string = r'''
            _____
           /     \
          /       \
    ,----(    {}    )----.
   /      \       /      \
  /        \_____/        \
  \   {}    /     \    {}   /
   \      /       \      /
    )----(    {}'   )----(
   /      \       /      \
  /        \_____/        \
  \   {}    /     \    {}   /
   \      /       \      /
    `----(    {}    )----'
          \       /
           \_____/
'''

    return hex_string.format(letters[3], letters[1], letters[2], letters[0], letters[4], letters[5], letters[6])

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
                'player words: '+str(player_words)+' ('+str(round(player_words*100.0/word_count,1))+'%)'+'\n'
                'player score: '+str(player_score)+' ('+str(round(player_score*100.0/total_score,1))+'%)'+'\n'
                'pangram found: '+str(player_pangram),
    }

    print(msg_dict.get(clean_msg,'Unknown selection'))
    return

if __name__ == "__main__":

    # read user input to select specific puzzle (not required)
    if len(sys.argv) > 1:
        try:
            int(sys.argv[1])
        except:
            print ('Puzzle index must be an integer. Exiting...')
            exit(0)
 
    try:
        puzzle_idx = int(sys.argv[1])
    except:
        puzzle_idx = None

    puzzles = read_puzzles()

    puzl = select_puzzle(puzzles, puzzle_idx)

    play(puzl)
 