"""Exercise catalogue used by recommendation, reward, and safety agents.

The catalogue is deliberately small but structured. It gives the RL agent and
supervisor enough metadata to reason about target regions, intensity, movement
category, contraindications, and progression/regression.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Exercise:
    name: str
    display_name: str
    target_regions: List[str]
    intensity: str
    difficulty: int
    movement_type: str
    contraindicated_regions: List[str]
    instructions: List[str]
    progression: str | None = None
    regression: str | None = None


EXERCISES: Dict[str, Exercise] = {
    "breathing_reset": Exercise(
        name="breathing_reset",
        display_name="Breathing reset",
        target_regions=[],
        intensity="none",
        difficulty=0,
        movement_type="recovery",
        contraindicated_regions=[],
        instructions=[
            "Sit or lie in a comfortable position.",
            "Breathe slowly and stop the session if discomfort increases.",
        ],
        progression="seated_mobility",
    ),
    "seated_mobility": Exercise(
        name="seated_mobility",
        display_name="Seated mobility drill",
        target_regions=["lower_back", "hip"],
        intensity="low",
        difficulty=1,
        movement_type="mobility",
        contraindicated_regions=[],
        instructions=[
            "Move slowly through a pain-free range.",
            "Keep the trunk supported and avoid forcing rotation.",
        ],
        progression="standing_march",
        regression="breathing_reset",
    ),
    "light_shoulder_raise": Exercise(
        name="light_shoulder_raise",
        display_name="Light shoulder raise",
        target_regions=["shoulder"],
        intensity="low",
        difficulty=1,
        movement_type="mobility",
        contraindicated_regions=["shoulder"],
        instructions=[
            "Raise the arm only to a comfortable height.",
            "Avoid shrugging or fast movement.",
        ],
        progression="wall_push_up",
        regression="seated_mobility",
    ),
    "standing_march": Exercise(
        name="standing_march",
        display_name="Standing march",
        target_regions=["hip", "knee"],
        intensity="low",
        difficulty=2,
        movement_type="control",
        contraindicated_regions=["knee", "hip"],
        instructions=[
            "Stand near support and lift one knee at a time.",
            "Keep the movement slow and controlled.",
        ],
        progression="bodyweight_squat",
        regression="seated_mobility",
    ),
    "wall_push_up": Exercise(
        name="wall_push_up",
        display_name="Wall push-up",
        target_regions=["shoulder", "elbow"],
        intensity="low",
        difficulty=2,
        movement_type="strength",
        contraindicated_regions=["shoulder", "elbow", "wrist"],
        instructions=[
            "Place hands on a wall at chest height.",
            "Keep the movement slow and stop if shoulder or elbow discomfort rises.",
        ],
        progression=None,
        regression="light_shoulder_raise",
    ),
    "bodyweight_squat": Exercise(
        name="bodyweight_squat",
        display_name="Bodyweight squat",
        target_regions=["knee", "lower_back", "hip"],
        intensity="medium",
        difficulty=3,
        movement_type="strength",
        contraindicated_regions=["knee", "lower_back", "hip"],
        instructions=[
            "Use a shallow range and keep knees aligned with feet.",
            "Stop if knee or lower-back discomfort increases.",
        ],
        progression=None,
        regression="standing_march",
    ),
    "rest": Exercise(
        name="rest",
        display_name="Rest / stop session",
        target_regions=[],
        intensity="none",
        difficulty=0,
        movement_type="recovery",
        contraindicated_regions=[],
        instructions=["Pause the exercise session and consider professional review if pain persists."],
    ),
}


INTENSITY_RANK = {"none": 0, "low": 1, "medium": 2, "high": 3}


def available_actions() -> List[str]:
    """Return action names in a stable order."""

    return list(EXERCISES.keys())


def describe_exercise(action: str) -> dict:
    """Return serialisable metadata for an exercise action."""

    exercise = EXERCISES[action]
    return asdict(exercise)
