"""Feedback Agent.

Stores user feedback such as self-reported pain and adherence.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class SessionFeedback:
    pain_score: float
    completed: bool
    notes: str = ""


class FeedbackAgent:
    """In-memory store for simple feedback records."""

    def __init__(self) -> None:
        self.history: List[SessionFeedback] = []

    def record_feedback(self, pain_score: float, completed: bool, notes: str = "") -> None:
        self.history.append(SessionFeedback(pain_score=pain_score, completed=completed, notes=notes))

    def summary(self) -> str:
        if not self.history:
            return "No feedback recorded."
        avg_pain = sum(f.pain_score for f in self.history) / len(self.history)
        completion_rate = sum(1 for f in self.history if f.completed) / len(self.history)
        return f"Sessions: {len(self.history)}, Avg pain: {avg_pain:.2f}, Completion rate: {completion_rate:.2f}"
