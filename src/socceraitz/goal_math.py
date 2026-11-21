"""Exact half-goal total-market arithmetic. No probability or betting decisions.

Source: skills/unified_soccer_simulator_v4_3_skill.md, Step 1.
"""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import Enum


class Side(str, Enum):
    UNDER = "UNDER"
    OVER = "OVER"


class Status(str, Enum):
    LIVE = "LIVE"
    WON = "WON"
    LOST = "LOST"


ALLOWED_LINES = frozenset(Decimal(f"{n}.5") for n in range(9))


@dataclass(frozen=True)
class GoalMathResult:
    side: Side
    line: Decimal
    home_score: int
    away_score: int
    current_goals: int
    status: Status
    additional_goals_to_lose: int | None
    additional_goals_to_win: int | None


def evaluate_goal_math(home_score: int, away_score: int, side: Side | str,
                       line: Decimal | float | str) -> GoalMathResult:
    """Return the exact live threshold, or a settled WON/LOST status.

    Only half-goal lines 0.5 through 8.5 are supported. This function does
    not infer full-time settlement, market eligibility, or a recommendation.
    """
    if type(home_score) is not int or type(away_score) is not int:
        raise ValueError("scores must be integers (booleans are not scores)")
    if home_score < 0 or away_score < 0:
        raise ValueError("scores must be nonnegative")
    try:
        normalized_side = Side(side)
    except ValueError as exc:
        raise ValueError("side must be UNDER or OVER") from exc
    if isinstance(line, bool):
        raise ValueError("line must be a supported half-goal total")
    try:
        normalized_line = Decimal(str(line))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("line must be a supported half-goal total") from exc
    if not normalized_line.is_finite() or normalized_line not in ALLOWED_LINES:
        raise ValueError("line must be one of 0.5, 1.5, ..., 8.5")

    goals = home_score + away_score
    crossed = Decimal(goals) > normalized_line
    if crossed:
        return GoalMathResult(normalized_side, normalized_line, home_score,
                              away_score, goals,
                              Status.LOST if normalized_side is Side.UNDER else Status.WON,
                              None, None)

    needed = int(normalized_line) - goals + 1
    return GoalMathResult(normalized_side, normalized_line, home_score,
                          away_score, goals, Status.LIVE,
                          needed if normalized_side is Side.UNDER else None,
                          needed if normalized_side is Side.OVER else None)
