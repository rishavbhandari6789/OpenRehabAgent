# OpenRehabAgent

OpenRehabAgent is a modular multi-agent framework for video-based pain localisation and adaptive exercise recommendation.
The code in this repository reflects the core components described in the accompanying research paper and includes a small
simulation script to demonstrate how the agents interact.

The system is organised around five main agents:

- Pose Agent – extracts skeletal keypoints from user video (represented here by simple synthetic poses).
- Pain Localisation Agent – estimates region-level discomfort or strain from pose sequences.
- Exercise Recommendation Agent – uses a simple Q-learning style update to suggest exercises.
- Feedback Agent – records user-reported pain and adherence.
- Supervisor Agent – enforces safety rules and can filter unsafe actions.

A lightweight in-memory Knowledge Base is used to share state between agents.

## Repository structure

```text
OpenRehabAgent/
├── README.md
├── LICENSE
├── docs/
│   └── architecture diagram
├── src/
│   ├── main.py
│   ├── pose_agent.py
│   ├── pain_localization_agent.py
│   ├── rl_agent.py
│   ├── supervisor_agent.py
│   ├── feedback_agent.py
│   └── knowledge_base.py
└── requirements.txt
```

The `main.py` script runs a simple end-to-end simulation over a few steps to illustrate how the agents could be wired together.

## Getting started

1. (Optional) Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the simulation:

   ```bash
   python -m src.main
   ```

   This will simulate a short sequence of "sessions" where the RL agent selects exercises, the pain agent produces dummy estimates,
   the supervisor filters actions, and the feedback agent stores simple records.

You can extend or replace the components with real models, camera input, or richer logic as you continue development.

## Code status

The current code is a compact research prototype intended to demonstrate the overall structure and data flow of OpenRehabAgent.
It does not connect to real cameras or production pose estimation models yet, but the interfaces are designed to be adapted.

## License

This project is released under the MIT License (see `LICENSE` for details).
