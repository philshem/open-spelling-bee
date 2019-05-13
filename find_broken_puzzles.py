

import params
import utils
import glob
import os


puzzles = glob.glob(params.PUZZLE_DATA_PATH + os.sep + '*.json')
for p in puzzles:
    tmp = p.split(os.sep)[-1].split('.')[0]
    print (tmp)
    k = tmp[0]
    if tmp[1:] != utils.sort_letters(tmp[1:]):
        # gotta rename the puzzle, non-alphabetical order 
        #os.rename(p, p.replace(tmp, utils.sort_letters(tmp)))
        os.rename(p, p.replace(tmp, utils.sort_letters(tmp)))

