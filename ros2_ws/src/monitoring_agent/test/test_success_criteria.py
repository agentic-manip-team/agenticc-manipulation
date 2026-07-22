"""M5 unit tests — success criteria rules."""
from monitoring_agent import success_criteria as sc


# MOVE_TO: 2cm rule
def test_move_to_pass():
    assert sc.check_move_to(0.01)        # 1cm -> pass

def test_move_to_fail():
    assert not sc.check_move_to(0.15)    # 15cm -> fail

def test_move_to_boundary():
    assert sc.check_move_to(0.02)        # exactly 2cm -> pass


# GRASP: finger gap rule
def test_grasp_pass():
    assert sc.check_grasp(0.046)

def test_grasp_fail():
    assert not sc.check_grasp(0.09)      # gap bara -> object nahi pakra


# PLACE: dono conditions zaroori
def test_place_pass():
    assert sc.check_place(True, True)

def test_place_fail_not_stable():
    assert not sc.check_place(True, False)

def test_place_fail_wrong_spot():
    assert not sc.check_place(False, True)


# failure classification
def test_failure_types():
    assert sc.failure_type_for('GRASP') == 'grasp_failed'
    assert sc.failure_type_for('MOVE_TO') == 'motion_failed'
    assert sc.failure_type_for('XYZ') == 'unknown_action'