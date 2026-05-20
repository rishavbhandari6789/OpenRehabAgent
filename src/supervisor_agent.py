"""Supervisor Agent.

The supervisor applies transparent safety rules before a recommendation reaches
the user. It never certifies an action as clinically safe; it only blocks actions
that violate the prototype's declared constraints.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .models.exercise_catalog import EXERCISES, INTENSITY_RANK


@dataclass
class SafetyDecision:
    allowed_actions: List[str]
    blocked_actions: List[str]
    reason: str
    risk_level: str


class SupervisorAgent:
    """Rule-based supervisor that can block unsafe actions."""

    def __init__(self, pain_threshold: float = 0.55, stop_threshold: float = 0.75) -> None:
        self.pain_threshold = pain_threshold
        self.stop_threshold = stop_threshold

    def filter_actions(self, pain_estimate: Dict[str, float], candidate_actions: List[str]) -> List[str]:
        return self.evaluate(pain_estimate, candidate_actions).allowed_actions

    def evaluate(
        self,
        pain_estimate: Dict[str, float],
        candidate_actions: List[str],
        avoid_regions: List[str] | None = None,
        max_intensity: str = "medium",
    ) -> SafetyDecision:
        avoid = set(avoid_regions or [])
        severe_regions = {region for region, score in pain_estimate.items() if score >= self.stop_threshold}
        high_risk_regions = {region for region, score in pain_estimate.items() if score >= self.pain_threshold} | avoid
        max_rank = INTENSITY_RANK.get(max_intensity, 2)

        allowed: List[str] = []
        blocked: List[str] = []
        for action in candidate_actions:
            exercise = EXERCISES.get(action)
            if exercise is None:
                blocked.append(action)
                continue
            if severe_regions and action != "rest":
                blocked.append(action)
                continue
            if INTENSITY_RANK[exercise.intensity] > max_rank:
                blocked.append(action)
                continue
            if high_risk_regions.intersection(exercise.contraindicated_regions):
                blocked.append(action)
            else:
                allowed.append(action)

        if "rest" in candidate_actions and "rest" not in allowed:
            allowed.append("rest")
            if "rest" in blocked:
                blocked.remove("rest")
        if not allowed:
            allowed = ["rest"]

        if severe_regions:
            risk_level = "stop"
            reason = "Severe discomfort signal detected for " + ", ".join(sorted(severe_regions))
        elif high_risk_regions:
            risk_level = "caution"
            reason = "High or avoided region detected for " + ", ".join(sorted(high_risk_regions))
        else:
            risk_level = "normal"
            reason = "No high pain risk detected"
        return SafetyDecision(allowed_actions=allowed, blocked_actions=blocked, reason=reason, risk_level=risk_level)
