"""Shared Knowledge Base for OpenRehabAgent.

The Knowledge Base keeps agent outputs, audit events, and session state in one
place. It is intentionally simple so the prototype remains reproducible and easy
to inspect.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class AuditEvent:
    """A traceable event produced by one of the agents."""

    agent: str
    event: str
    payload: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class KnowledgeBase:
    """Minimal state store with audit logging for agent decisions."""

    def __init__(self) -> None:
        self._store: Dict[str, Any] = {}
        self._events: List[AuditEvent] = []

    def set(self, key: str, value: Any, agent: str = "system") -> None:
        self._store[key] = value
        self.log(agent=agent, event=f"set:{key}", payload={"value": value})

    def get(self, key: str, default: Any = None) -> Any:
        return self._store.get(key, default)

    def log(self, agent: str, event: str, payload: Dict[str, Any]) -> None:
        self._events.append(AuditEvent(agent=agent, event=event, payload=payload))

    def snapshot(self) -> Dict[str, Any]:
        return dict(self._store)

    def audit_trail(self) -> List[Dict[str, Any]]:
        return [event.__dict__ for event in self._events]
