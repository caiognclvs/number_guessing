import io
import unittest
from unittest.mock import patch

import number_guessing


class FixedRng:
    def __init__(self, number):
        self.number = number

    def randint(self, _lower, _upper):
        return self.number


class NumberGuessingGameTests(unittest.TestCase):
    def play(self, answers, number=42, times=None):
        output = io.StringIO()
        inputs = iter(answers)
        clock = iter(times or [10.0, 11.0, 12.0, 13.0])
        won = number_guessing.play_round(
            input_fn=lambda _prompt: next(inputs),
            output=output,
            rng=FixedRng(number),
            clock=lambda: next(clock),
            high_scores={},
        )
        return won, output.getvalue()

    def test_correct_guess_reports_attempts_and_updates_score(self):
        won, output = self.play(["2", "10", "42"])
        self.assertTrue(won)
        self.assertIn("correct number in 2 attempts", output)
        self.assertIn("Best Medium score: 2 attempts", output)

    def test_invalid_input_does_not_use_a_chance(self):
        won, output = self.play(["1", "not a number", "0", "42"])
        self.assertTrue(won)
        self.assertIn("whole number", output)
        self.assertIn("between 1 and 100", output)
        self.assertIn("correct number in 1 attempt", output)

    def test_hint_and_loss_message(self):
        won, output = self.play(["3", "10", "20", "30"], number=42)
        self.assertFalse(won)
        self.assertIn("Hint: the number is even", output)
        self.assertIn("Out of chances! The number was 42", output)

    def test_main_supports_replay(self):
        answers = iter(["1", "42", "n"])
        with patch("builtins.input", side_effect=lambda _prompt: next(answers)):
            with patch("number_guessing.random.randint", return_value=42):
                with patch("builtins.print") as print_mock:
                    number_guessing.main()
        printed = "\n".join(call.args[0] for call in print_mock.call_args_list)
        self.assertIn("Welcome to the Number Guessing Game!", printed)
        self.assertIn("Thanks for playing!", printed)


if __name__ == "__main__":
    unittest.main()
