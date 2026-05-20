from src.feedback_agent import FeedbackAgent
from src.main import run_simulation
from src.models.exercise_catalog import available_actions
from src.pain_localization_agent import PainLocalizationAgent
from src.pose_agent import PoseAgent
from src.rehab_engine import OpenRehabEngine
from src.rl_agent import RLAgent
from src.session import SessionInput, UserProfile
from src.state_encoder import StateEncoder
from src.supervisor_agent import SupervisorAgent


def test_pose_agent_generates_features():
    pose = PoseAgent(seed=1).process_frame()
    features = pose.as_features()
    assert "movement_variance" in features
    assert "trunk_lean" in features
    assert 0 <= features["movement_variance"] <= 1


def test_pose_agent_accepts_external_landmarks():
    landmarks = [[0.1, 0.1], [0.2, 0.1], [0.1, 0.2], [0.2, 0.2], [0.1, 0.3], [0.2, 0.3], [0.1, 0.4], [0.2, 0.4]]
    pose = PoseAgent(seed=1).process_landmarks(landmarks)
    assert pose.source == "external"
    assert pose.points.shape[0] == 12


def test_pain_agent_outputs_regions_and_merges_self_report():
    pose = PoseAgent(seed=1).process_frame()
    pain = PainLocalizationAgent().estimate_pain(pose, {"shoulder": 0.9})
    assert {"shoulder", "elbow", "knee", "lower_back", "hip"}.issubset(set(pain.regions))
    assert 0 <= pain.max_score <= 1
    assert pain.regions["shoulder"] > 0.3


def test_supervisor_blocks_high_risk_actions():
    supervisor = SupervisorAgent(pain_threshold=0.5)
    decision = supervisor.evaluate({"knee": 0.8, "shoulder": 0.1}, available_actions())
    assert "bodyweight_squat" in decision.blocked_actions
    assert decision.allowed_actions == ["rest"]
    assert decision.risk_level == "stop"


def test_rl_agent_selects_allowed_action():
    agent = RLAgent(actions=available_actions(), seed=1)
    action = agent.select_action("start", allowed_actions=["rest"])
    assert action == "rest"


def test_state_encoder_bands_pain():
    state = StateEncoder().encode({"knee": 0.62, "shoulder": 0.1}, previous_action="standing_march")
    assert state == "region=knee|pain=high|prev=standing_march"


def test_feedback_summary():
    feedback = FeedbackAgent()
    feedback.record_feedback(0.2, True, recommended_action="seated_mobility", region="lower_back")
    summary = feedback.summary()
    assert summary["sessions"] == 1
    assert summary["completion_rate"] == 1.0


def test_engine_generates_complete_recommendation():
    engine = OpenRehabEngine(seed=1)
    result = engine.recommend(SessionInput(self_reported_pain={"knee": 0.7}, user_profile=UserProfile(avoid_regions=["shoulder"])))
    assert "recommended_exercise" in result
    assert "explanation" in result
    assert "bodyweight_squat" in result["blocked_actions"]
    assert result["recommended_action"] in result["allowed_actions"]


def test_end_to_end_simulation():
    result = run_simulation(steps=3)
    assert result["steps"] == 3
    assert len(result["sessions"]) == 3
    assert "audit_trail" in result
    assert result["feedback_summary"]["sessions"] == 3
    assert result["version"] == "0.3.0"
