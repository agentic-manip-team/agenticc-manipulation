"""M5: Har step type ke success rules — pure logic, ROS ke baghair (testable)."""

# thresholds
POSITION_TOLERANCE = 0.02    # 2cm
GRASP_GAP_THRESHOLD = 0.06   # 6cm


def check_move_to(distance_to_target):
    # target ke 2cm andar pohncha?
    return distance_to_target <= POSITION_TOLERANCE


def check_grasp(finger_gap):
    # fingers ke beech object hai?
    return finger_gap <= GRASP_GAP_THRESHOLD


def check_place(object_at_target, stable_1_sec):
    # object sahi jagah + 1 sec stable?
    return bool(object_at_target and stable_1_sec)


def check_gripper(done):
    # open/close/home mukammal hua?
    return bool(done)


def failure_type_for(action):
    # action -> failure ka naam
    mapping = {
        'MOVE_TO': 'motion_failed',
        'GRASP': 'grasp_failed',
        'PLACE': 'place_failed',
        'OPEN_GRIPPER': 'motion_failed',
        'CLOSE_GRIPPER': 'motion_failed',
        'HOME': 'motion_failed',
    }
    return mapping.get(action, 'unknown_action')