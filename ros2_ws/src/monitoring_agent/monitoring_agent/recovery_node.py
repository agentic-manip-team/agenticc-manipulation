import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool

# faisla-saazi alag file se (testable design)
from monitoring_agent.recovery_logic import RecoveryPolicy, HUMAN_HELP, MAX_ATTEMPTS


class RecoveryAgent(Node):
    """M5 Recovery Agent — failure sun kar strategy chunta hai."""

    def __init__(self):
        super().__init__('recovery_node')
        # inputs
        self.fail_sub = self.create_subscription(
            String, '/monitoring/failure_reason', self.on_failure, 10)
        self.result_sub = self.create_subscription(
            Bool, '/monitoring/task_result', self.on_result, 10)
        # output
        self.replan_pub = self.create_publisher(Bool, '/recovery/replan_request', 10)

        self.policy = RecoveryPolicy()  # dimagh
        self.get_logger().info('Recovery Agent READY — watching /monitoring/failure_reason')

    def on_result(self, msg):
        if msg.data:
            self.policy.on_success()

    def on_failure(self, msg):
        decision, n = self.policy.decide(msg.data)

        if decision == HUMAN_HELP:
            self.get_logger().error(f'{msg.data}: attempts khatam -> {HUMAN_HELP}')
            return

        self.get_logger().warn(
            f'{msg.data} (attempt {n}/{MAX_ATTEMPTS}) -> STRATEGY: {decision}')
        replan = Bool()
        replan.data = True
        self.replan_pub.publish(replan)


def main(args=None):
    rclpy.init(args=args)
    node = RecoveryAgent()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()