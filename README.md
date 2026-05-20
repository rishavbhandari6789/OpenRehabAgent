# OpenRehabAgent

OpenRehabAgent is a modular multi-agent research prototype for video-based pain localisation and adaptive exercise recommendation.

The repository implements the core software architecture described in the accompanying research outputs on SSRN and Zenodo. It now includes a complete runnable orchestration engine that combines synthetic or external pose landmarks, transparent pain-localisation heuristics, self-reported pain fusion, Q-learning style exercise recommendation, safety supervision, reward modelling, feedback tracking, audit logging, and an LLM-ready explanation layer.


## Research alignment

- SSRN paper: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5848742
- Zenodo record: https://zenodo.org/records/17765634

## Core agents

| Agent | Purpose |
|---|---|
| Pose Agent | Generates or adapts pose keypoints and interpretable pose features |
| Pain Localisation Agent | Estimates region-level discomfort from pose features |
| Exercise Recommendation Agent | Uses Q-learning style state/action/reward updates for adaptive exercise selection |
| Supervisor Agent | Applies safety rules before recommendations are returned |
| Feedback Agent | Records pain, adherence, and user response |
| LLM Explainer Agent | Produces human-readable explanations without clinical claims |
| Reward Model | Scores adherence, pain burden, intensity fit, and blocked-action penalties |
| State Encoder | Converts pain estimates into auditable RL states |
| Knowledge Base | Stores shared state and audit trail across agents |

## Architecture

```text
Video / Synthetic Pose
        |
        v
Pose Agent
        |
        v
Shared Knowledge Base
   |          |           |
   v          v           v
Pain Agent   RL Agent   Supervisor
   |          |           |
   +----------+           v
                          Safe Output
                              |
                              v
                        LLM Explainer
                              |
                              v
                           Feedback
                              |
                              v
                    Shared Knowledge Base

## Repository structure

```text
OpenRehabAgent/
├── README.md
├── LICENSE
├── CITATION.cff
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── requirements.txt
├── pyproject.toml
├── docs/
│   ├── architecture.md
│   ├── research-alignment.md
│   ├── safety-and-limitations.md
│   ├── evaluation-plan.md
│   └── development-roadmap.md
├── examples/
│   └── sample_output.json
├── src/
│   ├── main.py
│   ├── pose_agent.py
│   ├── pain_localization_agent.py
│   ├── rl_agent.py
│   ├── supervisor_agent.py
│   ├── feedback_agent.py
│   ├── llm_explainer_agent.py
│   ├── knowledge_base.py
│   ├── api/
│   │   └── app.py
│   └── models/
│       └── exercise_catalog.py
└── tests/
    └── test_agents.py
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main --steps 5 --output examples/sample_output.json
```

## Run tests

```bash
pytest
```

## Run API demo

```bash
uvicorn src.api.app:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```


## One-step recommendation API

Run the API:

```bash
uvicorn src.api.app:app --reload
```

Example request:

```bash
curl -X POST http://127.0.0.1:8000/recommend \
  -H "Content-Type: application/json" \
  -d @examples/sample_landmarks.json
```

The response includes pose features, region-level pain estimates, blocked actions, selected action, exercise instructions, reward, explanation, and audit-ready state.

## Current status

The current version demonstrates the architecture and agent interaction flow using deterministic synthetic data or external landmark arrays. It is suitable for software research, education, reproducibility, and future extension.

## Limitations

OpenRehabAgent does not use clinical data and is not intended for patient decision-making. See `docs/safety-and-limitations.md`.

## Citation

Please use the citation metadata in `CITATION.cff` and cite the associated SSRN and Zenodo research outputs.
