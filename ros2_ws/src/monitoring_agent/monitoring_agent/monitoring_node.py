import json
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool

# rules alag file se (testable design)
from monitoring_agent import success_criteria as sc

TIMEOUT_SEC = 6.0  # itni der robot chup rahe to timeout


class MonitoringAgent(Node):
    """M5 Monitoring Agent — har step check + robot ki khamoshi ka pehra."""

    def __init__(self):
        super().__init__('monitoring_node')
        # input: robot ke steps
        self.status_sub = self.create_subscription(
            String, '/execution/status', self.status_callback, 10)
        # outputs: result + failure reason
        self.result_pub = self.create_publisher(Bool, '/monitoring/task_result', 10)
        self.failure_pub = self.create_publisher(String, '/monitoring/failure_reason', 10)

        # timeout ka pehra
        self.last_msg_time = None
        self.timeout_reported = False
        self.watchdog = self.create_timer(1.0, self.check_timeout)

        self.get_logger().info('Monitoring Agent READY — watching /execution/status')

    def check_timeout(self):
        if self.last_msg_time is None:
            return
        silent_for = time.monotonic() - self.last_msg_time
        if silent_for > TIMEOUT_SEC and not self.timeout_reported:
            self.timeout_reported = True
            self.get_logger().error(f'ROBOT SILENT for {silent_for:.0f}s --> TIMEOUT!')
            fail_msg = String()
            fail_msg.data = 'timeout'
            self.failure_pub.publish(fail_msg)

    def status_callback(self, msg):
        # msg aya -> robot zinda, timer reset
        self.last_msg_time = time.monotonic()
        self.timeout_reported = False

        try:
            data = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().warn('Invalid JSON, ignoring')
            return

        # ek hi call mein poora faisla
        success, reason = sc.evaluate_step(data)
        step, action = data.get('step_id'), data.get('action')

        if success:
            self.get_logger().info(f'Step {step} [{action}] --> SUCCESS')
        else:
            self.get_logger().error(f'Step {step} [{action}] --> FAILED ({reason})')
            fail_msg = String()
            fail_msg.data = reason
            self.failure_pub.publish(fail_msg)

        result = Bool()
        result.data = bool(success)
        self.result_pub.publish(result)


def main(args=None):
    rclpy.init(args=args)
    node = MonitoringAgent()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()