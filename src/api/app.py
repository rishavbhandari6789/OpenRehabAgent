"""FastAPI demo endpoint for OpenRehabAgent."""

from __future__ import annotations

from typing import Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.main import run_simulation
from src.rehab_engine import OpenRehabEngine
from src.session import SessionInput, UserProfile


app = FastAPI(
    title="OpenRehabAgent API",
    description="Research prototype API for multi-agent rehabilitation recommendation simulation.",
    version="0.3.0",
)


class SimulationRequest(BaseModel):
    steps: int = Field(default=5, ge=1, le=50)


class RecommendationRequest(BaseModel):
    landmarks: Optional[List[List[float]]] = None
    self_reported_pain: Dict[str, float] = Field(default_factory=dict)
    completed_previous: Optional[bool] = None
    previous_action: Optional[str] = None
    avoid_regions: List[str] = Field(default_factory=list)
    preferred_intensity: str = "low"
    experience_level: str = "beginner"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "project": "OpenRehabAgent"}


@app.post("/simulate")
def simulate(request: SimulationRequest) -> dict:
    return run_simulation(steps=request.steps)


@app.post("/recommend")
def recommend(request: RecommendationRequest) -> dict:
    engine = OpenRehabEngine(seed=42)
    return engine.recommend(
        SessionInput(
            landmarks=request.landmarks,
            self_reported_pain=request.self_reported_pain,
            completed_previous=request.completed_previous,
            previous_action=request.previous_action,
            user_profile=UserProfile(
                avoid_regions=request.avoid_regions,
                preferred_intensity=request.preferred_intensity,
                experience_level=request.experience_level,
            ),
        )
    )
