# Architecture

OpenRehabAgent follows a modular multi-agent architecture for video-based pain localisation and adaptive exercise recommendation.

## High-level architecture

```mermaid
flowchart TD
    A[Video or Synthetic Pose Input] --> B[Pose Agent]
    B --> C[Shared Knowledge Base]
    C --> D[Pain Localisation Agent]
    D --> C
    C --> E[Exercise Recommendation Agent]
    E --> C
    C --> F[Supervisor Agent]
    F --> G[Safe Recommendation]
    G --> H[LLM Explainer Agent]
    H --> I[User-facing Explanation]
    I --> J[Feedback Agent]
    J --> C
```

## Sequence flow

```mermaid
sequenceDiagram
    participant User
    participant Pose as Pose Agent
    participant KB as Knowledge Base
    participant Pain as Pain Localisation Agent
    participant RL as Recommendation Agent
    participant Safety as Supervisor Agent
    participant Explain as LLM Explainer
    participant Feedback as Feedback Agent

    User->>Pose: Video frame or synthetic pose
    Pose->>KB: Pose features
    KB->>Pain: Pose features
    Pain->>KB: Region pain scores
    KB->>Safety: Pain scores and candidate actions
    Safety->>RL: Allowed actions
    RL->>Explain: Selected action
    Explain->>User: Explanation and disclaimer
    User->>Feedback: Pain and adherence feedback
    Feedback->>KB: Feedback history
```

## Safety governance

```mermaid
flowchart LR
    A[Candidate Exercise] --> B{High pain in contraindicated region?}
    B -->|Yes| C[Block or downgrade action]
    B -->|No| D[Allow action]
    C --> E[Audit decision]
    D --> E
    E --> F[Knowledge Base]
```

## Design principles

1. Modular agent boundaries
2. Transparent heuristics before complex models
3. Safety-aware recommendation
4. Feedback-based adaptation
5. Auditability and reproducibility
6. Clear non-clinical limitations
