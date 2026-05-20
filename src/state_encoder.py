"""State encoding for the reinforcement-learning recommendation agent."""

from __future__ import annotations

from typing import Dict


class StateEncoder:
    """Convert continuous pain estimates into compact, auditable RL states."""

    def encode(self, pain_regions: Dict[str, float], previous_action: str | None = None) -> str:
        if not pain_regions:
            return "no_signal"
        highest_region = max(pain_regions, key=pain_regions.get)
        max_score = pain_regions[highest_region]
        band = self._band(max_score)
        previous = previous_action or "none"
        return f"region={highest_region}|pain={band}|prev={previous}"

    @staticmethod
    def _band(score: float) -> str:
        if score >= 0.75:
            return "severe"
        if score >= 0.55:
            return "high"
        if score >= 0.30:
            return "moderate"
        return "low"
