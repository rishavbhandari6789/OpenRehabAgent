"""LLM Explainer Agent.

This optional agent produces human-readable explanations for recommendations.
It is implemented with a safe local template by default so the repository is
fully runnable without API keys or external services.
"""

from __future__ import annotations

from typing import Dict, List

from .models.exercise_catalog import EXERCISES


class LLMExplainerAgent:
    """Template-based explanation agent with an LLM-ready interface."""

    def explain(
        self,
        action: str,
        pain_regions: Dict[str, float],
        safety_reason: str,
        blocked_actions: List[str] | None = None,
        clinical_disclaimer: bool = True,
    ) -> str:
        highest_region = max(pain_regions, key=pain_regions.get) if pain_regions else "none"
        highest_score = pain_regions.get(highest_region, 0.0)
        exercise = EXERCISES.get(action)
        display = exercise.display_name if exercise else action
        blocked = f" Blocked actions: {', '.join(blocked_actions)}." if blocked_actions else ""
        instruction = " ".join(exercise.instructions[:2]) if exercise else "Follow the prototype safety note."
        explanation = (
            f"Recommended action: {display}. The highest estimated discomfort region is "
            f"{highest_region} with score {highest_score:.2f}. Supervisor decision: {safety_reason}.{blocked} "
            f"Suggested use: {instruction}"
        )
        if clinical_disclaimer:
            explanation += " Research prototype only; not medical advice."
        return explanation
