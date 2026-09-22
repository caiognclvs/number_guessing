# Number Guessing Game

A dependency-free CLI number guessing game written in Python.

## Run

```bash
python3 number_guessing.py
```

Choose a difficulty, then guess the number from 1 to 100 before your chances run out. Invalid guesses do not consume a chance. After two incorrect guesses, the game gives an even/odd hint. Best scores are tracked for each difficulty while the program is running.

## Test

```bash
python3 -m unittest -v
```
