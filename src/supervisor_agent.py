"""Supervisor Agent.

Applies simple safety rules on top of the RL agent's recommendations.
"""

from typing import Dict, List


class SupervisorAgent:
    """Rule-based supervisor that can block unsafe actions."""

    def __init__(self, pain_threshold: float = 0.7) -> None:
        self.pain_threshold = pain_threshold

    def filter_actions(self, pain_estimate: Dict[str, float], candidate_actions: List[str]) -> List[str]:
        """Filter actions when any region's pain exceeds a threshold.

        In this simple version, if pain is high we allow only the 'rest' action
        (if present). Otherwise, we leave the list unchanged.
        """
        max_pain = max(pain_estimate.values()) if pain_estimate else 0.0
        if max_pain >= self.pain_threshold and "rest" in candidate_actions:
            return ["rest"]
        return candidate_actions
