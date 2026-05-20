"""Pain Localisation Agent.

The agent estimates region-level discomfort from pose features plus optional
self-reported pain. It is transparent and heuristic by design: the goal is to
show the modular architecture from the paper, not to claim clinical validity.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .session import normalise_pain_map


@dataclass
class PainEstimate:
    """Per-region pain scores in the range [0, 1]."""

    regions: Dict[str, float]
    explanation: Dict[str, str]
    source_weights: Dict[str, float]

    @property
    def max_score(self) -> float:
        return max(self.regions.values()) if self.regions else 0.0

    @property
    def highest_region(self) -> str:
        return max(self.regions, key=self.regions.get) if self.regions else "none"


class PainLocalizationAgent:
    """Transparent heuristic pain-localisation agent."""

    def __init__(self, pose_weight: float = 0.65, self_report_weight: float = 0.35) -> None:
        self.pose_weight = pose_weight
        self.self_report_weight = self_report_weight

    def estimate_pain(self, pose, self_reported_pain: Dict[str, float] | None = None) -> PainEstimate:
        features = pose.as_features()
        reported = normalise_pain_map(self_reported_pain or {})

        pose_regions = {
            "shoulder": _clip(
                0.55 * features["shoulder_asymmetry"]
                + 0.25 * features["arm_extension_asymmetry"]
                + 0.15 * features["elbow_spread"]
            ),
            "elbow": _clip(0.45 * features["elbow_spread"] + 0.25 * features["arm_extension_asymmetry"]),
            "knee": _clip(0.60 * features["knee_alignment"] + 0.15 * features["knee_width"]),
            "lower_back": _clip(0.55 * features["trunk_lean"] + 0.20 * features["hip_alignment"] + 0.20 * features["movement_variance"]),
            "hip": _clip(0.45 * features["hip_alignment"] + 0.20 * features["hip_width"]),
        }

        regions: Dict[str, float] = {}
        for region, pose_score in pose_regions.items():
            if region in reported:
                regions[region] = _clip(self.pose_weight * pose_score + self.self_report_weight * reported[region])
            else:
                regions[region] = pose_score

        for region, score in reported.items():
            regions.setdefault(region, score)

        explanation = {
            "shoulder": "pose shoulder asymmetry, arm extension asymmetry, elbow spread, and optional self-report",
            "elbow": "elbow spread, arm extension asymmetry, and optional self-report",
            "knee": "knee alignment, stance width, and optional self-report",
            "lower_back": "trunk lean, hip alignment, movement variance, and optional self-report",
            "hip": "hip alignment, hip width, and optional self-report",
        }
        return PainEstimate(
            regions=regions,
            explanation=explanation,
            source_weights={"pose": self.pose_weight, "self_report": self.self_report_weight},
        )


def _clip(value: float) -> float:
    return round(max(0.0, min(1.0, float(value))), 4)
