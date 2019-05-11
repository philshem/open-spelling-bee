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