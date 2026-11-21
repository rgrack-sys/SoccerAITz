"""SoccerAITz: provider-independent soccer decision-support components."""

from .goal_math import GoalMathResult, Side, Status, evaluate_goal_math

__all__ = ["GoalMathResult", "Side", "Status", "evaluate_goal_math"]
