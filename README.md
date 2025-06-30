# DaggersAhead's Wordle Game

## How to Play

1. Run:
   
   `python wordle_game.py`

2. When prompted, choose an option for which wordbank to draw words from:

   `1` - Existing wordbank.
   
   `2` - Enter a path to a custom wordbank in a `.txt` file or the wordbank provided in `wordbank.txt`.
   
   `3` - Use the debugging word ("TESTS").

4. Guess the 5-letter word in 6 tries. Colors indicate:
   - Green: Correct letter, correct placement
   - Yellow: Correct letter, wrong placement
   - Red: Letter is not in word

## Files
- `wordle_game.py` — Main game script
- `wordbank.txt` — Word list
