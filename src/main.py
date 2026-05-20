"""Command-line simulation for OpenRehabAgent."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from .rehab_engine import OpenRehabEngine
from .session import SessionInput, UserProfile


def run_simulation(steps: int = 5, output_path: str | None = None) -> Dict[str, Any]:
    engine = OpenRehabEngine(seed=42, pain_threshold=0.55)
    sessions: List[Dict[str, Any]] = []

    for step in range(steps):
        synthetic_report = {}
        if step >= max(2, steps // 2):
            synthetic_report = {"shoulder": 0.35 + min(0.25, step * 0.02)}
        session = engine.recommend(
            SessionInput(
                self_reported_pain=synthetic_report,
                user_profile=UserProfile(preferred_intensity="low", experience_level="beginner"),
            )
        )
        sessions.append(session)

    result: Dict[str, Any] = {
        "project": "OpenRehabAgent",
        "version": "0.3.0",
        "steps": steps,
        "sessions": sessions,
        **engine.summary(),
        "disclaimer": "Research prototype only. Not a medical device or clinical decision system.",
    }

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run OpenRehabAgent simulation")
    parser.add_argument("--steps", type=int, default=5)
    parser.add_argument("--output", type=str, default="")
    args = parser.parse_args()

    result = run_simulation(steps=args.steps, output_path=args.output or None)
    print(json.dumps({"feedback_summary": result["feedback_summary"], "disclaimer": result["disclaimer"]}, indent=2))


if __name__ == "__main__":
    main()
