"""A command-line number guessing game."""

from __future__ import annotations

import random
import time
from typing import Callable, TextIO


DIFFICULTIES = {
    "1": ("Easy", 10),
    "2": ("Medium", 5),
    "3": ("Hard", 3),
}


def choose_difficulty(input_fn: Callable[[str], str], output: TextIO) -> tuple[str, int]:
    """Prompt until the player chooses a valid difficulty."""
    while True:
        output.write("Please select the difficulty level:\n")
        output.write("1. Easy (10 chances)\n")
        output.write("2. Medium (5 chances)\n")
        output.write("3. Hard (3 chances)\n")
        choice = input_fn("Enter your choice: ").strip()
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        output.write("Please choose 1, 2, or 3.\n")


def play_round(
    input_fn: Callable[[str], str] | None = None,
    output: TextIO | None = None,
    *,
    rng: random.Random | None = None,
    clock: Callable[[], float] = time.monotonic,
    high_scores: dict[str, int] | None = None,
) -> bool:
    """Play one round and return whether the player won."""
    if output is None:
        import sys

        output = sys.stdout
    if input_fn is None:
        input_fn = input
    if rng is None:
        rng = random
    if high_scores is None:
        high_scores = {}

    difficulty, max_attempts = choose_difficulty(input_fn, output)
    secret_number = rng.randint(1, 100)
    output.write(f"Great! You have selected the {difficulty} difficulty level.\n")
    output.write("Let's start the game!\n")

    attempts = 0
    start_time = clock()
    while attempts < max_attempts:
        try:
            raw_guess = input_fn("Enter your guess: ").strip()
        except EOFError:
            output.write("\nGame ended. Thanks for playing!\n")
            return False

        try:
            guess = int(raw_guess)
        except ValueError:
            output.write("Please enter a whole number between 1 and 100.\n")
            continue
        if not 1 <= guess <= 100:
            output.write("Your guess must be between 1 and 100. Try again.\n")
            continue

        attempts += 1
        if guess == secret_number:
            elapsed = clock() - start_time
            best = high_scores.get(difficulty)
            if best is None or attempts < best:
                high_scores[difficulty] = attempts
                score_message = " New high score!"
            else:
                score_message = ""
            output.write(
                f"Congratulations! You guessed the correct number in {attempts} "
                f"attempt{'s' if attempts != 1 else ''}.\n"
            )
            output.write(f"Time taken: {elapsed:.1f} seconds.{score_message}\n")
            output.write(f"Best {difficulty} score: {high_scores[difficulty]} attempts.\n")
            return True

        direction = "greater" if secret_number > guess else "less"
        output.write(f"Incorrect! The number is {direction} than {guess}.\n")
        if attempts == 2:
            parity = "even" if secret_number % 2 == 0 else "odd"
            output.write(f"Hint: the number is {parity}.\n")

    output.write(f"Out of chances! The number was {secret_number}.\n")
    output.write(f"Time taken: {clock() - start_time:.1f} seconds.\n")
    return False


def main() -> None:
    """Run rounds until the player chooses to stop."""
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    print("Guess the number before your chances run out.")
    high_scores: dict[str, int] = {}

    while True:
        try:
            play_round(high_scores=high_scores)
            answer = input("Would you like to play again? (y/n): ").strip().lower()
        except EOFError:
            print("\nThanks for playing!")
            break
        if answer not in {"y", "yes"}:
            print("Thanks for playing!")
            break
        print("\nI'm thinking of a new number between 1 and 100.\n")


if __name__ == "__main__":
    main()
