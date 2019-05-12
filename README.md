# Open Spelling Bee (OSB)

Open source port of New York Times' puzzle game Spelling Bee for the command line.

Requires Python 3.x and nothing but standard Python libraries.

## to play

To download the game:

    git clone https://github.com/philshem/open-spelling-bee.git
    cd open-spelling-bee

To play a random game:

    python3 play_puzzles.py

To play a non-random game:

    python3 play_puzzles.py AGFEDCB

where A is the center letter. If the puzzle `AGFEDCB` does not exist, it will be created and saved to `data/ABCDEFG.json` (the file names are the first letter and the alphabetically sorted remaining letters).

## to generate new puzzles

Set custom parameters in the `params.py` file, for example how many puzzles you want to create. Then generate by running:

    python3 generate_puzzles.py

Runtime depends on your parameters. For the default parameter settings, the code takes approximately 8 hours to generate 100 7-letter puzzles that meet the criteria (total points, total words, pangram count).

To generate a certain letter combination, use:

    python3 generate_puzzles.py AGFEDCB

which will then be saved to `data/ABCDEFG.json`.

For a list of the previous NY Times letter selections, see [William Shunn's page](https://www.shunn.net/bee/?past=1).

---

# Game Play
To play, build words with a minimum of 4 letters, using the letters provided.

Each word must include the center letter at least once.

Letters may be used as many times as you'd like.

Scoring: 1 point for a 4 letter word, and 1 more point for each additional letter.

Each puzzle has 1 "pangram" that uses each of the 7 letters at least once. The pangram is worth 7 extra points.

Dictionary: Scrabble word list [TWL06](https://www.wordgamedictionary.com/twl06/)


## example play

(based on game found in `data/RDGHNOU.json`)

```
Type !help or !h for help
Playing puzzle index: 1
Your letters are: 
            _____
           /     \
          /       \
    ,----(    N    )----.
   /      \       /      \
  /        \_____/        \
  \   H    /     \    U   /
   \      /       \      /
    )----(    R'   )----(
   /      \       /      \
  /        \_____/        \
  \   G    /     \    D   /
   \      /       \      /
    `----(    O    )----'
          \       /
           \_____/

Max score: 88
Total words: 37
Your guess: GROUND
✓ GROUND              word score = 3        words found = 1/37    total score = 3/88    

Your guess: GURU     
✓ GURU                word score = 1        words found = 2/37    total score = 4/88    

Your guess: GROUNDHOG
✓ GROUNDHOG*          word score = 13       words found = 3/37    total score = 17/88   
```

Use the following commands for more details:
```
!i : instructions
!g : show letters
!f : shuffle letters
!s : player stats
!h : help
!q : quit
```