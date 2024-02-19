import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from custom_msgs.msg import OpenSpace


class ComplexSubscriber(Node):

    def __init__(self):
        super().__init__('open_space_publisher')
        # ROS parameters - with defaults set
        self.declare_parameters(
            namespace='',
            parameters = [
                ('subscriber_topic', 'open_space'), 
                ('publisher_topic', 'fake_scan')
            ]
        )
        # get ROS parameters
        subscriber_topic, publisher_topic= self.get_parameters(
            ['subscriber_topic', 'publisher_topic']
        )
        # set up
        self.subscription = self.create_subscription(
            LaserScan,
            publisher_topic.value,
            self.listener_callback,
            10)
        self.subscription
        self.open_space_publisher_ = self.create_publisher(OpenSpace, subscriber_topic.value, 10)


    def listener_callback(self, msg):
        # gather data and log 
        longest_distance = max(msg.ranges)
        longest_distance_angle = float(msg.ranges.index(longest_distance))
        self.get_logger().info(f'Longest range: {longest_distance} at angle: {longest_distance_angle}')
        # OpenSpace message
        open_space_msg = OpenSpace()
        open_space_msg.distance = longest_distance
        open_space_msg.angle = longest_distance_angle
        self.open_space_publisher_.publish(open_space_msg)


def main(args=None):
    rclpy.init(args=args)
    open_space_publisher = ComplexSubscriber()
    rclpy.spin(open_space_publisher)
    open_space_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
