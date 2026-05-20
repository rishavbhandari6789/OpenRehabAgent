"""Exercise Recommendation Agent.

A compact Q-learning style agent used to demonstrate adaptive recommendation.
It is intentionally simple and deterministic-friendly so the research prototype
can be reproduced without clinical data.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple
import random


class RLAgent:
    """Minimal Q-learning style recommendation agent."""

    def __init__(
        self,
        actions: List[str],
        gamma: float = 0.9,
        alpha: float = 0.1,
        epsilon: float = 0.1,
        seed: int = 42,
    ) -> None:
        self.actions = actions
        self.gamma = gamma
        self.alpha = alpha
        self.epsilon = epsilon
        self.q_table: Dict[Tuple[Any, str], float] = {}
        self._random = random.Random(seed)

    def _q(self, state: Any, action: str) -> float:
        return self.q_table.get((state, action), 0.0)

    def select_action(self, state: Any, allowed_actions: List[str] | None = None) -> str:
        """Epsilon-greedy action selection over allowed actions."""

        candidates = allowed_actions or self.actions
        if not candidates:
            return "rest"
        if self._random.random() < self.epsilon:
            return self._random.choice(candidates)
        q_values = [(a, self._q(state, a)) for a in candidates]
        q_values.sort(key=lambda x: (x[1], x[0]), reverse=True)
        return q_values[0][0]

    def update(self, state: Any, action: str, reward: float, next_state: Any) -> None:
        """Tabular Q-learning update."""

        best_next = max((self._q(next_state, a) for a in self.actions), default=0.0)
        old_value = self._q(state, action)
        new_value = old_value + self.alpha * (reward + self.gamma * best_next - old_value)
        self.q_table[(state, action)] = round(new_value, 6)

    def explain_action(self, state: Any, action: str) -> str:
        return f"Selected {action} for state {state} with Q-value {self._q(state, action):.4f}"
