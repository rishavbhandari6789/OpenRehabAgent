"""End-to-end OpenRehabAgent orchestration engine."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List

from .feedback_agent import FeedbackAgent
from .knowledge_base import KnowledgeBase
from .llm_explainer_agent import LLMExplainerAgent
from .models.exercise_catalog import available_actions, describe_exercise
from .pain_localization_agent import PainLocalizationAgent
from .pose_agent import PoseAgent
from .reward_model import RewardModel
from .rl_agent import RLAgent
from .session import SessionInput
from .state_encoder import StateEncoder
from .supervisor_agent import SupervisorAgent


class OpenRehabEngine:
    """Coordinates all agents through a shared knowledge base."""

    def __init__(self, seed: int = 42, pain_threshold: float = 0.55) -> None:
        self.pose_agent = PoseAgent(seed=seed)
        self.pain_agent = PainLocalizationAgent()
        self.actions = available_actions()
        self.rl_agent = RLAgent(actions=self.actions, seed=seed)
        self.supervisor = SupervisorAgent(pain_threshold=pain_threshold)
        self.feedback_agent = FeedbackAgent()
        self.explainer = LLMExplainerAgent()
        self.kb = KnowledgeBase()
        self.encoder = StateEncoder()
        self.reward_model = RewardModel()
        self.previous_state = "start"
        self.step = 0

    def recommend(self, session_input: SessionInput | None = None) -> Dict[str, Any]:
        session_input = session_input or SessionInput()
        self.step += 1

        pose = (
            self.pose_agent.process_landmarks(session_input.landmarks)
            if session_input.landmarks is not None
            else self.pose_agent.process_frame()
        )
        pain = self.pain_agent.estimate_pain(pose, session_input.self_reported_pain)
        self.kb.set("pose_features", pose.as_features(), agent="pose_agent")
        self.kb.set("pain_regions", pain.regions, agent="pain_localisation_agent")

        max_intensity = "low" if session_input.user_profile.experience_level == "beginner" else "medium"
        decision = self.supervisor.evaluate(
            pain.regions,
            self.actions,
            avoid_regions=session_input.user_profile.avoid_regions,
            max_intensity=max_intensity,
        )
        self.kb.set("safety_decision", asdict(decision), agent="supervisor_agent")

        state = self.encoder.encode(pain.regions, session_input.previous_action or self.previous_state)
        chosen = self.rl_agent.select_action(state, decision.allowed_actions)
        completed = self._infer_completion(chosen, pain.max_score, session_input.completed_previous)
        reward = self.reward_model.compute(
            action=chosen,
            highest_region=pain.highest_region,
            max_pain=pain.max_score,
            completed=completed,
            preferred_intensity=session_input.user_profile.preferred_intensity,
            blocked=chosen in decision.blocked_actions,
        )
        next_state = self.encoder.encode(pain.regions, chosen)
        self.rl_agent.update(state, chosen, reward, next_state)

        explanation = self.explainer.explain(chosen, pain.regions, decision.reason, decision.blocked_actions)
        self.feedback_agent.record_feedback(
            pain_score=pain.max_score,
            completed=completed,
            notes=explanation,
            recommended_action=chosen,
            region=pain.highest_region,
        )

        session = {
            "step": self.step,
            "state": state,
            "next_state": next_state,
            "pose_source": pose.source,
            "pose_confidence": pose.confidence,
            "pain_regions": pain.regions,
            "pain_explanation": pain.explanation,
            "highest_region": pain.highest_region,
            "allowed_actions": decision.allowed_actions,
            "blocked_actions": decision.blocked_actions,
            "risk_level": decision.risk_level,
            "recommended_action": chosen,
            "recommended_exercise": describe_exercise(chosen),
            "reward": reward,
            "completed": completed,
            "explanation": explanation,
        }
        self.kb.log("openrehab_engine", "session_completed", session)
        self.previous_state = next_state
        return session

    def summary(self) -> Dict[str, Any]:
        return {
            "feedback_summary": self.feedback_agent.summary(),
            "feedback_records": self.feedback_agent.records(),
            "q_table": {f"{state}|{action}": value for (state, action), value in self.rl_agent.q_table.items()},
            "audit_trail": self.kb.audit_trail(),
        }

    @staticmethod
    def _infer_completion(action: str, max_pain: float, completed_previous: bool | None) -> bool:
        if completed_previous is not None:
            return completed_previous
        if action == "rest":
            return True
        return max_pain < 0.75
