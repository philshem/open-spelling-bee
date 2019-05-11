#!/usr/bin/env python

''' play puzzles '''

import params

import sys
import json
import random

def main():
    pass

def read_puzzles():

    with open(params.PUZZLE_PATH,'r') as fp:
        puzzles = json.load(fp)

    return puzzles

def select_puzzle(puzzles, puzl_idx):

    if puzl_idx is not None:
        # get puzzle with specific index
        try:
            return [x for x in puzzles if x.get('index') == puzl_idx][0]
        except:
            puzzle_count = len(puzzles)
            print ('Invalid puzzle selection. There are',str(puzzle_count),'puzzles to choose from.')
            exit(0)
    else:
        # return a random puzzle
        return random.choice(puzzles)

def play(puzl):
    print('Type !help or !h for help')

    print('Playing puzzle index:',puzl.get('index'))

    letters = puzl.get('letters')
    print('Your letters are:',letters[0],letters[1:])

    word_list = puzl.get('word_list')
    pangram_list = puzl.get('pangrams')
    # pangram is worth 7 extra points
    total_score = puzl.get('total_score') + 7 * len(pangram_list)
    word_count = puzl.get('word_count')
    
    print ('Max score:',total_score)
    print ('Total words:', word_count)

    player_score = 0
    player_words = 0
    player_pangram = False

    #print(word_list) # no cheating!

    guess_list = []

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
            # word is found
            word_dict = word_list[word_index]

            player_score += word_dict.get('score')
            player_words += 1

            if word_dict.get('word') in pangram_list:
                # pangram found
                player_pangram = True
                # pangrams are worth +7 extra
                player_score += 7
                print (guess, word_dict.get('score')+7, player_score, '(pangram!)')
            else:
                print (guess, word_dict.get('score'), player_score)

            # add good guess to the list, so it can't be reused
            guess_list.append(guess)
        
        # all words found (somehow)
        if player_words == word_count:
            print ('Congratulations. You found them all!')

def ask_user():
    text = input("Your guess: ")
    text = text.strip().upper()

    return text

def help(msg, letters, guess_list, player_score, player_words, player_pangram, total_score, word_count):
    
    # some features for
    clean_msg = msg.replace('!','')[0].lower()

    if clean_msg == 'q':
        print('Quitting...')
        exit(0)

    help_msg = '!g : show letters\n!s : player stats\n!h : show help\n!q : quit'

    msg_dict = {
        'h' : help_msg,
        'i' : 'instructions',
        'g' : letters[0]+' '+''.join(letters[1:]),
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

    print(len(puzzles),'puzzle(s) loaded')
    
    puzl = select_puzzle(puzzles, puzzle_idx)

    play(puzl)
 