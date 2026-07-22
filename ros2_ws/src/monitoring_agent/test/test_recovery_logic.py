"""M5 unit tests — recovery escalation logic."""
from monitoring_agent.recovery_logic import RecoveryPolicy, HUMAN_HELP


def test_known_failure_gets_strategy():
    p = RecoveryPolicy()
    decision, n = p.decide('grasp_failed')
    assert 'gripper' in decision.lower()
    assert n == 1


def test_unknown_failure_gets_replan():
    p = RecoveryPolicy()
    decision, _ = p.decide('alien_attack')
    assert 'replan' in decision.lower()


def test_attempts_count_up():
    p = RecoveryPolicy()
    p.decide('motion_failed')
    _, n = p.decide('motion_failed')
    assert n == 2


def test_human_help_after_max():
    p = RecoveryPolicy()
    for _ in range(3):
        p.decide('timeout')          # attempts 1,2,3
    decision, _ = p.decide('timeout')  # 4th
    assert decision == HUMAN_HELP


def test_success_resets_counters():
    p = RecoveryPolicy()
    p.decide('grasp_failed')
    p.decide('grasp_failed')
    p.on_success()                   # reset
    _, n = p.decide('grasp_failed')
    assert n == 1


def test_counters_independent_per_type():
    p = RecoveryPolicy()
    p.decide('grasp_failed')
    _, n = p.decide('motion_failed')  # doosri type -> apna counter
    assert n == 1