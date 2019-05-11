# open-spelling-bee

Open source port of New York Times' puzzle game Spelling Bee

Requires Python 3.x and nothing but standard Python libraries.


## to play
    
    git clone https://github.com/philshem/open-spelling-bee.git
    cd open-spelling-bee

    python3 play_puzzles.py

## to generate new puzzles

Set custom parameters in the `params.py` file, then generate

    python3 generate_puzzles.py

Runtime depends on your parameters. For the default parameter settings, the code takes approximately 8 hours to generate 100 7-letter puzzles that meet the criteria (total points, total words, pangram count).

---

## game play
To play, build minimum 4-letter words using the letters provided.

Each word must include the center letter at least once.

Letters may be used as many times as you'd like.

Scoring: 1 point for a 4 letter word, and 1 more point for each word longer than 4 letters.

Each puzzle has 1 "pangram" that uses each of the 7 letters at least once. The pangram is worth 7 extra points.

Dictionary: Scrabble word list [TWL06](https://www.wordgamedictionary.com/twl06/)


## example play
(based on test game found in data/1.puzzles.json)

```
You selected a random puzzle, index: 0
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