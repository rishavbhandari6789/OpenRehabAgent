# Changelog

## [0.3.0] - 2026-05-20

### Added

- End-to-end `OpenRehabEngine` that coordinates Pose, Pain Localisation, Exercise Recommendation, Supervisor, Feedback, Explainer, and Knowledge Base agents.
- Structured `SessionInput` and `UserProfile` objects for landmark input, self-reported pain, avoided regions, preferred intensity, and experience level.
- Expanded pose feature extraction, including trunk lean, hip/knee alignment, arm-extension asymmetry, pose confidence, and external landmark support.
- Pain localisation that combines transparent pose heuristics with optional self-reported pain.
- State encoder for converting region-level pain signals into auditable Q-learning states.
- Reward model for adherence, discomfort, intensity fit, and safety-aware action feedback.
- Expanded exercise catalogue with display names, instructions, target regions, difficulty, progression, regression, and contraindications.
- `/recommend` FastAPI endpoint for one-step adaptive recommendations.
- Sample external landmark payload in `examples/sample_landmarks.json`.
- Additional unit tests for external landmarks, self-report integration, state encoding, engine output, and supervisor stop logic.

### Changed

- CLI simulation now uses the full orchestration engine instead of wiring all agents directly in `main.py`.
- API version updated to `0.3.0`.
- Sample output regenerated from the full engine.


## [0.2.0] - 2026-05-17

### Added

- Research alignment documentation.
- Mermaid architecture diagrams.
- Safety and limitations documentation.
- Evaluation plan.
- Development roadmap.
- LLM-ready explanation agent.
- FastAPI simulation endpoint.
- Deterministic synthetic pose generation.
- Region-level transparent pain localisation.
- Exercise catalogue.
- Agent audit trail.
- Unit tests.
- GitHub Actions workflow.
- Citation metadata.

## [0.1.0] - 2025-11-30

### Added

- Initial research prototype.
- Pose Agent.
- Pain Localisation Agent.
- Exercise Recommendation Agent.
- Feedback Agent.
- Supervisor Agent.
- Shared Knowledge Base.
