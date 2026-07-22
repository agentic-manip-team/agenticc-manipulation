import json
import random
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MockRobot(Node):
    """Fake robot — asli Execution Agent ki naqal, testing/demo ke liye."""

    def __init__(self):
        super().__init__('mock_robot')
        self.pub = self.create_publisher(String, '/execution/status', 10)
        self.timer = self.create_timer(2.0, self.send_step)  # har 2 second

        # Pick-and-place ke 5 steps (sab sahi values ke saath)
        self.steps = [
            {'step_id': 1, 'action': 'OPEN_GRIPPER', 'done': True},
            {'step_id': 2, 'action': 'MOVE_TO', 'distance_to_target': 0.01},
            {'step_id': 3, 'action': 'GRASP', 'finger_gap': 0.046},
            {'step_id': 4, 'action': 'MOVE_TO', 'distance_to_target': 0.015},
            {'step_id': 5, 'action': 'PLACE', 'object_at_target': True, 'stable_1_sec': True},
        ]
        self.i = 0
        self.get_logger().info('Mock Robot started — sending fake steps')

    def send_step(self):
        step = dict(self.steps[self.i % len(self.steps)])

        # 30% chance: jaan boojh kar ghalti dalo (failure simulate karne ke liye)
        if random.random() < 0.3:
            if step['action'] == 'MOVE_TO':
                step['distance_to_target'] = 0.15   # 15cm door reh gaya = fail
            elif step['action'] == 'GRASP':
                step['finger_gap'] = 0.09           # gap bara = object nahi pakra
            elif step['action'] == 'PLACE':
                step['object_at_target'] = False    # object jagah par nahi

        msg = String()
        msg.data = json.dumps(step)
        self.pub.publish(msg)
        self.get_logger().info(f"Sent: {step['action']} (step {step['step_id']})")
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    node = MockRobot()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()