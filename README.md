# Open Spelling Bee (OSB)

# 🐝

Open source port of New York Times' puzzle game Spelling Bee for the command line.

Requires Python 3.x and nothing but standard Python libraries.

## to play

To download the game:

    git clone https://github.com/philshem/open-spelling-bee.git
    cd open-spelling-bee

To play a random game:

    python3 play_puzzle.py

To play a non-random game:

    python3 play_puzzle.py RDGHNOU

where `R` is the center letter that must be used at least once in each word. If the puzzle `RDGHNOU` does not exist, it will be created and saved to `data/RDGHNOU.json` (the file names are the first letter and the alphabetically sorted remaining letters).

The word list used is from [SCOWL](http://wordlist.aspell.net/). The default setting contains 40,000 words, which seems comparable to the New York Times dictionary. (See below on changing the size parameter to include more erudite words.)

To reach "genius" level, you'll need to solve 50% of the words.

To solve a game (aka cheat-mode):

    python3 solve_puzzles.py RDGHNOU

If the game does not exist, it will be created and saved to the `data/` folder. 

For a list of the previous NY Times letter selections, see [William Shunn's page](https://www.shunn.net/bee/?past=1).

## to generate new puzzles

Set custom parameters in the `params.py` file, for example how many puzzles you want to create. Then generate by running:

    python3 generate_puzzles.py

Or to save the word stats:

    python3 generate_puzzles.py > stats.csv

Runtime depends on your parameters. For the default parameter settings, the code takes approximately 8 hours to generate 100 7-letter puzzles that meet the criteria (total points, total words, pangram count).

To generate a certain letter combination, use:

    python3 generate_puzzles.py AGFEDCB

which will then be saved to `data/ABCDEFG.json`.

## to change the size of the wordlist

If you find the game overly facile or wish your recondite words were accepted, you can change the wordlist size. Change `size=35` to a larger number in [word_lists/mkscowl](word_lists/mkscowl) and then run `mkscowl` to create a new wordlist. You must run `generate_puzzles.py` (as detailed above) whenever the wordlist changes.

|Description|Scowl size|Num words|Sample word|
|-|-|-|-|
|Small|`size=35`|40,198|abacus|
|Medium|`size=50`|63,375|abeyance|
|Large|`size=70`|115,332|abecedarian|
|Huge|`size=80`|251,064|abapical|
|Insane|`size=95`|435,726|abigailship|

---

# Game Play

To play, build words with a minimum of 4 letters, using the letters provided.

Each word must include the center letter at least once.

Letters may be used as many times as you'd like.

Scoring: 1 point for a 4 letter word, and 1 more point for each additional letter.

Each puzzle has 1 "pangram" that uses each of the 7 letters at least once. The pangram is worth 7 extra points.



## example play

(based on game found by playing `python3 play_puzzle.py RDGHNOU`)

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

---

## interesting puzzles

+ `Q` as center letter: `QAHILSU`, `QBEISTU`

+ `X` as center letter: `XACESTV`, `XEFIOST`, `XAENSTU`, `XADEIRS`, `XAEINOT`, `XCENOST`, `XEFIPRS`, `XAERSTY`, `XDELOPS`, `XBELOST`, `XCDELSU`

+ `Z` as center letter: `ZORIBTE`, `ZRBEOSU`, `ZCEILST`,`ZAEMNST`,`ZADELRS`, `ZADENRS`, `ZAEIKLS`, `ZACENOS`, `ZGILNOS`, `ZABDELR`, `ZBEGINO`, `ZABGINS`, `ZEILNOR`, `ZABDELS`, `ZAELOST`
