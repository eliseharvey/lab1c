import rclpy
import random
import math
from rclpy.node import Node

from sensor_msgs.msg import LaserScan


class FakeScanPublisher(Node):

    def __init__(self):
        super().__init__('fake_scan_publisher')
        # ROS parameters - with defaults set
        self.declare_parameters( 
            namespace='',
            parameters = [
                ('publish_topic', 'fake_scan'), 
                ('publish_rate', 0.05), # Seconds; Hz = cycles per second, 20 Hz = 0.05 cycles per seconds
                ('angle_min', -(2/3)*math.pi),
                ('angle_max', (2/3)*math.pi),
                ('range_min', 1.0),
                ('range_max', 10.0),
                ('angle_increment', (1/300)*math.pi),
            ]
        )
        # get ROS parameters
        publish_topic, publish_rate = self.get_parameters(
            ['publish_topic', 'publish_rate']
        )
        # set up
        self.publisher_ = self.create_publisher(LaserScan, publish_topic.value, 10) # type, topic, queue
        timer_period = publish_rate.value  
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        angle_min, angle_max, range_min, range_max, angle_increment = self.get_parameters(
            ['angle_min', 'angle_max', 'range_min', 'range_max', 'angle_increment']
        )
        msg = LaserScan() 
        msg.header.stamp = self.get_clock().now().to_msg() # not included in ROS parameter update
        msg.header.frame_id = 'base_link'                  # not included in ROS parameter update
        msg.angle_min = angle_min.value
        msg.angle_max = angle_max.value
        msg.angle_increment = angle_increment.value
        # msg.time_increment = can leave unset
        msg.scan_time = 0.1                                # not included in ROS parameter update
        msg.range_min = range_min.value
        msg.range_max = range_max.value
        ranges = []
        for i in range(int(((msg.angle_max - msg.angle_min) / msg.angle_increment) + 1)):
            ranges.append(random.uniform(msg.range_min, msg.range_max))
        msg.ranges = ranges
        # msg.intensities = can leave unset
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing Fake Laser Scan')


def main(args=None):
    rclpy.init(args=args)
    fake_scan_publisher = FakeScanPublisher()
    rclpy.spin(fake_scan_publisher)
    fake_scan_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
