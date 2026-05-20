"""Session request models and normalisation helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class UserProfile:
    """Non-clinical profile used to tune the prototype recommendation policy."""

    goal: str = "general_mobility"
    preferred_intensity: str = "low"
    avoid_regions: List[str] = field(default_factory=list)
    experience_level: str = "beginner"


@dataclass
class SessionInput:
    """Input accepted by the end-to-end engine for one recommendation step."""

    landmarks: Optional[List[List[float]]] = None
    self_reported_pain: Dict[str, float] = field(default_factory=dict)
    completed_previous: Optional[bool] = None
    previous_action: Optional[str] = None
    notes: str = ""
    user_profile: UserProfile = field(default_factory=UserProfile)


def normalise_pain_map(pain: Dict[str, float]) -> Dict[str, float]:
    """Clamp user-reported pain values to the [0, 1] range."""

    return {region: round(max(0.0, min(1.0, float(score))), 4) for region, score in pain.items()}
