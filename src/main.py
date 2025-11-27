"""End-to-end simulation for OpenRehabAgent.

This script wires together the agents and simulates a small number of steps.
It is not connected to real video input but demonstrates the intended data flow.
"""

from .pose_agent import PoseAgent
from .pain_localization_agent import PainLocalizationAgent
from .rl_agent import RLAgent
from .supervisor_agent import SupervisorAgent
from .feedback_agent import FeedbackAgent
from .knowledge_base import KnowledgeBase


def run_simulation(steps: int = 5) -> None:
    pose_agent = PoseAgent()
    pain_agent = PainLocalizationAgent()
    actions = ["light_shoulder_raise", "bodyweight_squat", "rest"]
    rl_agent = RLAgent(actions=actions)
    supervisor = SupervisorAgent(pain_threshold=0.6)
    feedback_agent = FeedbackAgent()
    kb = KnowledgeBase()

    state = "start"

    for t in range(steps):
        pose = pose_agent.process_frame()
        pain = pain_agent.estimate_pain(pose)
        kb.set("pain", pain.regions)

        allowed_actions = supervisor.filter_actions(pain.regions, actions)
        if not allowed_actions:
            chosen = "rest"
        else:
            chosen = rl_agent.select_action(state)

        # Simple reward: prefer lower pain and completion of non-rest actions.
        max_pain = max(pain.regions.values()) if pain.regions else 0.0
        reward = -max_pain
        completed = chosen != "rest"
        feedback_agent.record_feedback(pain_score=max_pain, completed=completed, notes=f"Action: {chosen}")

        next_state = "after_" + chosen
        rl_agent.update(state, chosen, reward, next_state)
        state = next_state

    print("Simulation finished.")
    print(feedback_agent.summary())


if __name__ == "__main__":
    run_simulation()
