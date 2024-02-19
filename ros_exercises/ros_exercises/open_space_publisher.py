import rclpy
import math
from rclpy.node import Node
from std_msgs.msg import Float32
from sensor_msgs.msg import LaserScan


class ComplexSubscriber(Node):

    def __init__(self):
        super().__init__('open_space_publisher')
        self.subscription = self.create_subscription(
            LaserScan,
            'fake_scan',
            self.listener_callback,
            10)
        self.subscription
        self.distance_publisher_ = self.create_publisher(Float32, 'open_space/distance', 10)
        self.angle_publisher_ = self.create_publisher(Float32, 'open_space/angle', 10)

    def listener_callback(self, msg):
        # gather data and log 
        longest_distance = max(msg.ranges)
        longest_distance_angle = float(msg.ranges.index(longest_distance))
        self.get_logger().info(f'Longest range: {longest_distance} at angle: {longest_distance_angle}')
        # distance message
        distance_msg = Float32()
        distance_msg.data = longest_distance
        self.distance_publisher_.publish(distance_msg)
        # angle message
        angle_msg = Float32()
        angle_msg.data = longest_distance_angle
        self.distance_publisher_.publish(angle_msg)


def main(args=None):
    rclpy.init(args=args)
    open_space_publisher = ComplexSubscriber()
    rclpy.spin(open_space_publisher)
    open_space_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
