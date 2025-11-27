"""Pain Localisation Agent.

Takes pose information and produces region-level pain or strain scores.
This implementation uses a simple heuristic on synthetic poses.
"""

from dataclasses import dataclass
from typing import Dict
import numpy as np


@dataclass
class PainEstimate:
    """Per-region pain scores in the range [0, 1]."""
    regions: Dict[str, float]


class PainLocalizationAgent:
    """Simple heuristic pain-localisation agent."""

    def __init__(self) -> None:
        self.regions = ["shoulder", "elbow", "knee", "lower_back"]

    def estimate_pain(self, pose) -> PainEstimate:
        """Produce a dummy pain estimate based on pose variance.

        This is a toy heuristic to make the simulation more concrete.
        """
        scores = {}
        # Use the variance of the pose points as a crude signal.
        if pose.points.size > 0:
            v = float(np.var(pose.points))
        else:
            v = 0.0
        base = min(1.0, max(0.0, v))
        for name in self.regions:
            scores[name] = base
        return PainEstimate(regions=scores)
