"""Deterministic offline contract tests for the first implemented component."""

import unittest
from decimal import Decimal

from socceraitz.goal_math import Side, Status, evaluate_goal_math


class GoalMathTests(unittest.TestCase):
    def test_exhaustive_live_and_crossed_thresholds(self):
        # 9 lines x 12 current goal totals x 2 sides = 216 assertions sets.
        for half_line in range(9):
            line = Decimal(f"{half_line}.5")
            for goals in range(12):
                for side in (Side.UNDER, Side.OVER):
                    with self.subTest(line=line, goals=goals, side=side):
                        result = evaluate_goal_math(goals, 0, side, line)
                        self.assertEqual(result.current_goals, goals)
                        self.assertEqual(result.line, line)
                        if goals > line:
                            self.assertEqual(result.status,
                                             Status.LOST if side is Side.UNDER else Status.WON)
                            self.assertIsNone(result.additional_goals_to_lose)
                            self.assertIsNone(result.additional_goals_to_win)
                        else:
                            self.assertEqual(result.status, Status.LIVE)
                            expected = half_line - goals + 1
                            self.assertEqual(
                                result.additional_goals_to_lose if side is Side.UNDER
                                else result.additional_goals_to_win, expected)
                            self.assertIsNone(
                                result.additional_goals_to_win if side is Side.UNDER
                                else result.additional_goals_to_lose)

    def test_canonical_examples(self):
        for home, away, side, line, remaining in (
            (0, 0, "UNDER", 2.5, 3),
            (1, 0, "UNDER", 2.5, 2),
            (2, 0, "UNDER", 2.5, 1),
            (3, 0, "UNDER", 4.5, 2),
            (3, 1, "UNDER", 4.5, 1),
            (1, 0, "OVER", 2.5, 2),
            (2, 1, "OVER", 3.5, 1),
        ):
            with self.subTest(home=home, away=away, side=side, line=line):
                actual = evaluate_goal_math(home, away, side, line)
                self.assertEqual(actual.status, Status.LIVE)
                self.assertEqual(actual.additional_goals_to_lose if side == "UNDER"
                                 else actual.additional_goals_to_win, remaining)
        self.assertEqual(evaluate_goal_math(3, 2, "UNDER", 4.5).status, Status.LOST)
        self.assertEqual(evaluate_goal_math(3, 2, "OVER", 4.5).status, Status.WON)

    def test_split_score_is_preserved(self):
        actual = evaluate_goal_math(2, 1, "UNDER", "4.50")
        self.assertEqual((actual.home_score, actual.away_score, actual.current_goals), (2, 1, 3))
        self.assertEqual(actual.additional_goals_to_lose, 2)

    def test_reject_unsupported_lines(self):
        for line in (-0.5, 0, 1, 2.25, 9.5, "NaN", "Infinity", True, "bad"):
            with self.subTest(line=line), self.assertRaises(ValueError):
                evaluate_goal_math(0, 0, Side.UNDER, line)

    def test_reject_invalid_scores(self):
        for home, away in ((-1, 0), (0, -1), (1.0, 0), (True, 0), (0, None)):
            with self.subTest(home=home, away=away), self.assertRaises(ValueError):
                evaluate_goal_math(home, away, Side.UNDER, 2.5)

    def test_reject_invalid_side(self):
        with self.assertRaises(ValueError):
            evaluate_goal_math(0, 0, "BOTH", 2.5)


if __name__ == "__main__":
    unittest.main()
