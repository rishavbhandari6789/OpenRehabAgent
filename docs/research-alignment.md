# Research Alignment

OpenRehabAgent is aligned with the research paper:

**OpenRehabAgent: A Modular Multi-Agent Architecture for Video-Based Pain Localisation and Adaptive Exercise Recommendation**

The SSRN abstract describes five cooperating agents: Pose Agent, Pain Localisation Agent, Exercise Recommendation Agent, Feedback Agent, Supervisor Agent, and a shared Knowledge Base. The current repository implements that structure in Python as a reproducible research prototype.

## Research-to-code mapping

| Research concept | Repository implementation |
|---|---|
| Pose Agent | `src/pose_agent.py` |
| Pain Localisation Agent | `src/pain_localization_agent.py` |
| Exercise Recommendation Agent | `src/rl_agent.py` |
| Feedback Agent | `src/feedback_agent.py` |
| Supervisor Agent | `src/supervisor_agent.py` |
| Shared Knowledge Base | `src/knowledge_base.py` |
| Explanation layer | `src/llm_explainer_agent.py` |
| End-to-end simulation | `src/main.py` |
| API demonstration | `src/api/app.py` |

## Current prototype scope

The current implementation uses deterministic synthetic pose signals and transparent heuristics. It demonstrates the architecture, agent interaction, safety filtering, recommendation loop, and feedback recording.

## Research limitation

This repository is not a medical device. It does not diagnose, treat, or provide physiotherapy advice. It is a software research prototype for architecture exploration and responsible AI experimentation.

## Evidence alignment

The repository supports the public research outputs hosted on SSRN and Zenodo by providing executable code, documentation, tests, diagrams, and versioned release notes.
