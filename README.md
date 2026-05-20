# OpenRehabAgent

OpenRehabAgent is a modular multi-agent research prototype for video-based pain localisation and adaptive exercise recommendation.

The repository implements the core software architecture described in the accompanying research outputs on SSRN and Zenodo. It includes a runnable orchestration engine that combines synthetic or external pose landmarks, transparent pain-localisation heuristics, self-reported pain fusion, reinforcement-learning style exercise recommendation, safety supervision, reward modelling, feedback tracking, audit logging, and an LLM-ready explanation layer.


---

# Research Alignment

- SSRN paper: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5848742
- Zenodo record: https://zenodo.org/records/17765634

---

# Core Agents

| Agent | Purpose |
|---|---|
| Pose Agent | Generates or adapts pose keypoints and interpretable pose features |
| Pain Localisation Agent | Estimates region-level discomfort from pose features |
| RL Recommendation Agent | Uses reinforcement-learning style updates for adaptive exercise selection |
| Supervisor Agent | Applies safety rules before recommendations are returned |
| Feedback Agent | Records pain, adherence, and user response |
| LLM Explainer Agent | Produces human-readable explanations without clinical claims |
| Reward Model | Scores adherence, pain burden, intensity fit, and blocked-action penalties |
| State Encoder | Converts pain estimates into auditable RL states |
| Knowledge Base | Stores shared state and audit trail across agents |

---

# Architecture

```text
Video / Synthetic Pose Input
            │
            ▼
      Pose Agent
            │
            ▼
   Shared Knowledge Base
      ├─────────────────────────────┐
      │                             │
      ▼                             ▼
Pain Localisation Agent     RL Recommendation Agent
      │                             │
      └──────────────┬──────────────┘
                     ▼
             Supervisor Agent
                     │
                     ▼
           Safe Recommendation
                     │
                     ▼
            LLM Explainer Agent
                     │
                     ▼
               Feedback Agent
                     │
                     └──────────────► Shared Knowledge Base
```

---

# Repository Structure

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
│   ├── sample_landmarks.json
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
│   ├── reward_model.py
│   ├── state_encoder.py
│   ├── rehab_engine.py
│   ├── session.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── app.py
│   └── models/
│       └── exercise_catalog.py
└── tests/
    └── test_agents.py
```

---

# Quick Start

## Create virtual environment

```bash
python -m venv .venv
```

## Activate environment

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run orchestration demo

```bash
python -m src.main --steps 5 --output examples/sample_output.json
```

---

# Run Tests

```bash
pytest
```

---

# Run API Demo

```bash
uvicorn src.api.app:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

# One-Step Recommendation API

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

The response includes:

- Pose features
- Region-level pain estimates
- Blocked actions
- Selected exercise
- Exercise instructions
- Reward signal
- LLM explanation
- Audit-ready state information

---

# Current Status

The current version demonstrates the architecture and agent interaction flow using deterministic synthetic data or externally provided landmark arrays.

The repository is suitable for:

- Software architecture research
- Reinforcement learning experimentation
- Explainable AI prototypes
- Human-AI interaction studies
- Educational demonstrations
- Reproducibility research

---

# Safety and Limitations

OpenRehabAgent does not use clinical datasets and is not intended for patient diagnosis or treatment decisions.

See:

```text
docs/safety-and-limitations.md
```

---

# Citation

Please use the citation metadata provided in:

```text
CITATION.cff
```

and cite the associated SSRN and Zenodo research outputs when referencing this repository.

---

# License

This project is released under the MIT License.