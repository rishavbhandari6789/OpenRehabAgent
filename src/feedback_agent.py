"""Feedback Agent.

Stores user feedback such as self-reported pain, adherence, and subjective
response to a recommendation.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass
class SessionFeedback:
    pain_score: float
    completed: bool
    notes: str = ""
    recommended_action: str = ""
    region: str = ""


class FeedbackAgent:
    """In-memory store for feedback records."""

    def __init__(self) -> None:
        self.history: List[SessionFeedback] = []

    def record_feedback(
        self,
        pain_score: float,
        completed: bool,
        notes: str = "",
        recommended_action: str = "",
        region: str = "",
    ) -> None:
        self.history.append(
            SessionFeedback(
                pain_score=pain_score,
                completed=completed,
                notes=notes,
                recommended_action=recommended_action,
                region=region,
            )
        )

    def summary(self) -> Dict[str, float | int]:
        if not self.history:
            return {"sessions": 0, "avg_pain": 0.0, "completion_rate": 0.0}
        avg_pain = sum(f.pain_score for f in self.history) / len(self.history)
        completion_rate = sum(1 for f in self.history if f.completed) / len(self.history)
        return {
            "sessions": len(self.history),
            "avg_pain": round(avg_pain, 4),
            "completion_rate": round(completion_rate, 4),
        }

    def records(self) -> List[Dict[str, object]]:
        return [asdict(item) for item in self.history]
