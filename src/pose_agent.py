"""Pose Agent.

This agent provides pose features for downstream pain localisation. The default
implementation uses deterministic synthetic keypoints so the research prototype
can run without a camera or clinical dataset. It also accepts external 2D/3D
landmarks from tools such as MediaPipe, OpenPose, MoveNet, or recorded JSON.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Optional

import numpy as np


JOINT_INDEX: Dict[str, int] = {
    "left_shoulder": 0,
    "right_shoulder": 1,
    "left_elbow": 2,
    "right_elbow": 3,
    "left_hip": 4,
    "right_hip": 5,
    "left_knee": 6,
    "right_knee": 7,
    "left_wrist": 8,
    "right_wrist": 9,
    "left_ankle": 10,
    "right_ankle": 11,
}


@dataclass
class PoseKeypoints:
    """Container for pose keypoints for a single frame."""

    points: np.ndarray
    confidence: float = 1.0
    source: str = "synthetic"

    def as_features(self) -> Dict[str, float]:
        """Convert keypoints into interpretable proxy movement features."""

        pts = self.points
        return {
            "shoulder_asymmetry": _vertical_delta(pts[JOINT_INDEX["left_shoulder"]], pts[JOINT_INDEX["right_shoulder"]]),
            "shoulder_width": _distance(pts[JOINT_INDEX["left_shoulder"]], pts[JOINT_INDEX["right_shoulder"]]),
            "elbow_spread": _distance(pts[JOINT_INDEX["left_elbow"]], pts[JOINT_INDEX["right_elbow"]]),
            "hip_alignment": _vertical_delta(pts[JOINT_INDEX["left_hip"]], pts[JOINT_INDEX["right_hip"]]),
            "hip_width": _distance(pts[JOINT_INDEX["left_hip"]], pts[JOINT_INDEX["right_hip"]]),
            "knee_alignment": _vertical_delta(pts[JOINT_INDEX["left_knee"]], pts[JOINT_INDEX["right_knee"]]),
            "knee_width": _distance(pts[JOINT_INDEX["left_knee"]], pts[JOINT_INDEX["right_knee"]]),
            "trunk_lean": _trunk_lean(pts),
            "arm_extension_asymmetry": _arm_extension_asymmetry(pts),
            "movement_variance": float(np.var(pts)),
            "pose_confidence": float(self.confidence),
        }


def _distance(a: Iterable[float], b: Iterable[float]) -> float:
    a_arr = np.asarray(list(a), dtype=float)[:2]
    b_arr = np.asarray(list(b), dtype=float)[:2]
    return float(np.linalg.norm(a_arr - b_arr))


def _vertical_delta(a: Iterable[float], b: Iterable[float]) -> float:
    a_arr = np.asarray(list(a), dtype=float)
    b_arr = np.asarray(list(b), dtype=float)
    return float(abs(a_arr[1] - b_arr[1]))


def _midpoint(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return (a[:2] + b[:2]) / 2.0


def _trunk_lean(points: np.ndarray) -> float:
    shoulders = _midpoint(points[JOINT_INDEX["left_shoulder"]], points[JOINT_INDEX["right_shoulder"]])
    hips = _midpoint(points[JOINT_INDEX["left_hip"]], points[JOINT_INDEX["right_hip"]])
    return float(abs(shoulders[0] - hips[0]))


def _arm_extension_asymmetry(points: np.ndarray) -> float:
    left = _distance(points[JOINT_INDEX["left_shoulder"]], points[JOINT_INDEX["left_elbow"]])
    right = _distance(points[JOINT_INDEX["right_shoulder"]], points[JOINT_INDEX["right_elbow"]])
    return float(abs(left - right))


class PoseAgent:
    """Pose provider for the OpenRehabAgent pipeline."""

    def __init__(self, num_joints: int = 12, seed: Optional[int] = 42) -> None:
        self.num_joints = num_joints
        self._rng = np.random.default_rng(seed)
        self._step = 0

    def process_frame(self) -> PoseKeypoints:
        """Return a synthetic pose array for demonstration and tests."""

        base = np.array(
            [
                [0.35, 0.25], [0.65, 0.25],
                [0.28, 0.45], [0.72, 0.45],
                [0.42, 0.65], [0.58, 0.65],
                [0.40, 0.90], [0.60, 0.90],
                [0.24, 0.63], [0.76, 0.63],
                [0.39, 1.00], [0.61, 1.00],
            ],
            dtype=float,
        )
        phase = self._step / 6.0
        noise = self._rng.normal(0, 0.012, size=base.shape)
        base[2, 1] += np.sin(phase) * 0.025
        base[3, 1] -= np.sin(phase) * 0.025
        base[6, 0] += np.cos(phase) * 0.01
        base[7, 0] -= np.cos(phase) * 0.01
        self._step += 1
        points = np.clip(base + noise, 0.0, 1.0)
        return PoseKeypoints(points=points, confidence=0.95, source="synthetic")

    def process_landmarks(self, landmarks, confidence: float = 1.0) -> PoseKeypoints:
        """Adapt external landmarks into the internal pose representation."""

        points = np.asarray(landmarks, dtype=float)
        if points.ndim != 2 or points.shape[0] < 8 or points.shape[1] < 2:
            raise ValueError("landmarks must have shape (>=8 joints, 2+) with enough joints")
        if points.shape[0] < self.num_joints:
            padding = np.repeat(points[-1:, :2], self.num_joints - points.shape[0], axis=0)
            points = np.vstack([points[:, :2], padding])
        return PoseKeypoints(points=points[: self.num_joints, :2], confidence=confidence, source="external")
