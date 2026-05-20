"""Reward model for adaptive exercise selection."""

from __future__ import annotations

from .models.exercise_catalog import EXERCISES, INTENSITY_RANK


class RewardModel:
    """Calculate a reproducible reward from safety, pain, adherence, and fit."""

    def compute(
        self,
        action: str,
        highest_region: str,
        max_pain: float,
        completed: bool,
        preferred_intensity: str = "low",
        blocked: bool = False,
    ) -> float:
        if blocked:
            return -1.0
        exercise = EXERCISES.get(action)
        if exercise is None:
            return -1.0
        if action == "rest":
            return round(0.35 if max_pain >= 0.55 else -0.05, 4)

        adherence = 0.35 if completed else -0.35
        pain_penalty = max_pain * 0.75
        region_fit = 0.20 if highest_region not in exercise.contraindicated_regions else -0.50
        preference_penalty = abs(INTENSITY_RANK[exercise.intensity] - INTENSITY_RANK.get(preferred_intensity, 1)) * 0.08
        reward = 0.55 + adherence + region_fit - pain_penalty - preference_penalty
        return round(max(-1.0, min(1.0, reward)), 4)
