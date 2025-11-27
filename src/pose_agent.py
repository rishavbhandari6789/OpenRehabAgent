"""Pose Agent.

Responsible for providing pose keypoints for each frame.
Here we simulate pose keypoints with simple numeric arrays.
"""

from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass
class PoseKeypoints:
    """Container for pose keypoints for a single frame."""
    points: np.ndarray


class PoseAgent:
    """Simple pose agent that generates synthetic keypoints."""

    def __init__(self, num_joints: int = 8) -> None:
        self.num_joints = num_joints

    def process_frame(self) -> PoseKeypoints:
        """Return a synthetic pose array for demonstration purposes."""
        points = np.random.rand(self.num_joints, 2)
        return PoseKeypoints(points=points)
