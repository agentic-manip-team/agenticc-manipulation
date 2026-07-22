"""M5: Recovery ka dimagh — pure logic, ROS ke baghair (testable)."""

STRATEGIES = {
    'object_not_found': 'Re-detect from new viewpoint',
    'motion_failed':    'Try alternative planner (RRT -> STOMP)',
    'grasp_failed':     'Open gripper -> home -> re-detect -> retry',
    'place_failed':     'Re-check target location -> retry place',
    'api_failed':       'Switch to backup LLM (Gemini)',
    'timeout':          'Wait 2s -> retry step',
    'collision':        'Emergency stop -> home -> rebuild scene',
}
MAX_ATTEMPTS = 3
HUMAN_HELP = 'HUMAN_INTERVENTION_NEEDED'


class RecoveryPolicy:
    """Failure aane par faisla karta hai — kya strategy, ya insan ko bulao."""

    def __init__(self):
        self.attempts = {}  # failure_type -> count

    def on_success(self):
        # success -> sab counters saaf
        self.attempts.clear()

    def decide(self, failure_type):
        # returns: (faisla, attempt_number)
        self.attempts[failure_type] = self.attempts.get(failure_type, 0) + 1
        n = self.attempts[failure_type]
        if n > MAX_ATTEMPTS:
            return HUMAN_HELP, n
        return STRATEGIES.get(failure_type, 'Unknown -> full replan'), n