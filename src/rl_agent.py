"""Reinforcement-learning based exercise recommendation agent.

This file defines a small Q-learning style agent that can be used in the
OpenRehabAgent simulation.
"""

from typing import Any, Dict, List, Tuple
import random


class RLAgent:
    """Minimal Q-learning style agent."""

    def __init__(self, actions: List[str], gamma: float = 0.9, alpha: float = 0.1, epsilon: float = 0.1) -> None:
        self.actions = actions
        self.gamma = gamma
        self.alpha = alpha
        self.epsilon = epsilon
        self.q_table: Dict[Tuple[Any, str], float] = {}

    def _q(self, state: Any, action: str) -> float:
        return self.q_table.get((state, action), 0.0)

    def select_action(self, state: Any) -> str:
        """Epsilon-greedy action selection."""
        if not self.actions:
            return ""
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        # Exploit
        q_values = [(a, self._q(state, a)) for a in self.actions]
        q_values.sort(key=lambda x: x[1], reverse=True)
        return q_values[0][0]

    def update(self, state: Any, action: str, reward: float, next_state: Any) -> None:
        """Tabular Q-learning update."""
        best_next = max((self._q(next_state, a) for a in self.actions), default=0.0)
        old_value = self._q(state, action)
        new_value = old_value + self.alpha * (reward + self.gamma * best_next - old_value)
        self.q_table[(state, action)] = new_value
