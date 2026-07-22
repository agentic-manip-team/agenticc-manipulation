"""M5 integration tests — monitoring rules + recovery policy MIL KAR sahi chalte hain."""
from monitoring_agent import success_criteria as sc
from monitoring_agent.recovery_logic import RecoveryPolicy, HUMAN_HELP


def test_failed_grasp_flows_to_recovery():
    # robot ka kharab grasp -> monitoring pakre -> recovery sahi strategy de
    success, reason = sc.evaluate_step({'action': 'GRASP', 'finger_gap': 0.09})
    assert not success and reason == 'grasp_failed'
    decision, n = RecoveryPolicy().decide(reason)
    assert 'gripper' in decision.lower() and n == 1


def test_good_step_needs_no_recovery():
    success, reason = sc.evaluate_step({'action': 'MOVE_TO', 'distance_to_target': 0.01})
    assert success and reason == ''


def test_repeated_failure_ends_in_human_help():
    # ek hi step 4 baar fail -> akhir mein insan ko bulao
    p = RecoveryPolicy()
    bad_step = {'action': 'MOVE_TO', 'distance_to_target': 0.20}
    final = None
    for _ in range(4):
        ok, reason = sc.evaluate_step(bad_step)
        assert not ok
        final, _n = p.decide(reason)
    assert final == HUMAN_HELP


def test_recovery_then_success_resets():
    # fail -> recover -> success -> counters saaf
    p = RecoveryPolicy()
    _, reason = sc.evaluate_step({'action': 'GRASP', 'finger_gap': 0.09})
    p.decide(reason)
    ok, _ = sc.evaluate_step({'action': 'GRASP', 'finger_gap': 0.04})
    assert ok
    p.on_success()
    _, n = p.decide('grasp_failed')
    assert n == 1