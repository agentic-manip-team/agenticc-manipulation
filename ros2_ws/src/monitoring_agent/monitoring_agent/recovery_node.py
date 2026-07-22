import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool


class RecoveryAgent(Node):
    """M5 Recovery Agent — failure sun kar strategy chunta hai."""

    # har failure type ki apni strategy
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

    def __init__(self):
        super().__init__('recovery_node')
        # input: failure ki khabar
        self.fail_sub = self.create_subscription(
            String, '/monitoring/failure_reason', self.on_failure, 10)
        # input: success par counters reset
        self.result_sub = self.create_subscription(
            Bool, '/monitoring/task_result', self.on_result, 10)
        # output: replan ka order
        self.replan_pub = self.create_publisher(Bool, '/recovery/replan_request', 10)

        self.attempts = {}  # failure_type -> kitni baar hua
        self.get_logger().info('Recovery Agent READY — watching /monitoring/failure_reason')

    def on_result(self, msg):
        if msg.data:
            self.attempts.clear()  # success aya -> hisab saaf

    def on_failure(self, msg):
        ftype = msg.data
        self.attempts[ftype] = self.attempts.get(ftype, 0) + 1
        n = self.attempts[ftype]

        # 3 se zyada -> insan ko bulao
        if n > self.MAX_ATTEMPTS:
            self.get_logger().error(
                f'{ftype}: attempts khatam -> HUMAN_INTERVENTION_NEEDED')
            return

        strategy = self.STRATEGIES.get(ftype, 'Unknown -> full replan')
        self.get_logger().warn(
            f'{ftype} (attempt {n}/{self.MAX_ATTEMPTS}) -> STRATEGY: {strategy}')

        replan = Bool()
        replan.data = True
        self.replan_pub.publish(replan)  # Planning Agent ke liye signal


def main(args=None):
    rclpy.init(args=args)
    node = RecoveryAgent()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()