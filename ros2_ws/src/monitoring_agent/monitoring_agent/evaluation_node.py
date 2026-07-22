import csv
import os
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool

# CSV yahan banega (team structure: data/evaluation/)
CSV_PATH = os.path.expanduser('~/ros2_ws/data/evaluation/results.csv')


class EvaluationAgent(Node):
    """M5 Evaluation — har result CSV mein save + live success rate."""

    def __init__(self):
        super().__init__('evaluation_node')
        # inputs: monitoring ke results
        self.result_sub = self.create_subscription(
            Bool, '/monitoring/task_result', self.on_result, 10)
        self.fail_sub = self.create_subscription(
            String, '/monitoring/failure_reason', self.on_failure, 10)

        self.total = 0
        self.passed = 0
        self.last_failure = ''

        # CSV file tayar karo (header ke sath, agar nayi hai)
        os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
        if not os.path.exists(CSV_PATH):
            with open(CSV_PATH, 'w', newline='') as f:
                csv.writer(f).writerow(['timestamp', 'result', 'failure_reason'])

        self.get_logger().info(f'Evaluation Agent READY — logging to {CSV_PATH}')

    def on_failure(self, msg):
        self.last_failure = msg.data  # agle FAILED ki wajah yaad rakho

    def on_result(self, msg):
        self.total += 1
        if msg.data:
            self.passed += 1
            reason = ''
        else:
            reason = self.last_failure

        # CSV mein ek row likho
        with open(CSV_PATH, 'a', newline='') as f:
            csv.writer(f).writerow([
                time.strftime('%Y-%m-%d %H:%M:%S'),
                'SUCCESS' if msg.data else 'FAILED',
                reason,
            ])

        # live stats
        rate = 100.0 * self.passed / self.total
        self.get_logger().info(
            f'Logged #{self.total} | success rate: {rate:.1f}%')


def main(args=None):
    rclpy.init(args=args)
    node = EvaluationAgent()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()