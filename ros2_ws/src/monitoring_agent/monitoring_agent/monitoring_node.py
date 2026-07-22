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

        # timeout ka pehra: har 1 sec check karo robot kab se chup hai
        self.last_msg_time = None
        self.timeout_reported = False
        self.watchdog = self.create_timer(1.0, self.check_timeout)

        self.get_logger().info('Monitoring Agent READY — watching /execution/status')

    def check_timeout(self):
        # abhi tak koi msg hi nahi aya -> intezar
        if self.last_msg_time is None:
            return
        silent_for = time.monotonic() - self.last_msg_time
        if silent_for > TIMEOUT_SEC and not self.timeout_reported:
            self.timeout_reported = True  # bar bar report na karo
            self.get_logger().error(f'ROBOT SILENT for {silent_for:.0f}s --> TIMEOUT!')
            fail_msg = String()
            fail_msg.data = 'timeout'
            self.failure_pub.publish(fail_msg)

    def status_callback(self, msg):
        # msg aya -> robot zinda hai, timer reset
        self.last_msg_time = time.monotonic()
        self.timeout_reported = False

        try:
            data = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().warn('Invalid JSON, ignoring')
            return

        action = data.get('action')
        step = data.get('step_id')

        # rule apply karo (success_criteria.py se)
        if action == 'MOVE_TO':
            success = sc.check_move_to(data.get('distance_to_target', 999.0))
        elif action == 'GRASP':
            success = sc.check_grasp(data.get('finger_gap', 999.0))
        elif action == 'PLACE':
            success = sc.check_place(data.get('object_at_target', False),
                                     data.get('stable_1_sec', False))
        elif action in ('OPEN_GRIPPER', 'CLOSE_GRIPPER', 'HOME'):
            success = sc.check_gripper(data.get('done', False))
        else:
            success = False

        # elaan + publish
        if success:
            self.get_logger().info(f'Step {step} [{action}] --> SUCCESS')
        else:
            reason = sc.failure_type_for(action)
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