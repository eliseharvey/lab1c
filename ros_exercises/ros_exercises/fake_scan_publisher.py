import rclpy
import random
import math
from rclpy.node import Node

from sensor_msgs.msg import LaserScan


class FakeScanPublisher(Node):

    def __init__(self):
        super().__init__('fake_scan_publisher')
        self.publisher_ = self.create_publisher(LaserScan, 'fake_scan', 10) # type, topic, queue
        timer_period = 0.05  # Seconds; Hz = cycles per second, 20 Hz = 0.05 cycles per seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        """
        Details for LaserScan message:
            Timestamp: Current ros time
            Frame_id: “base_link”
            Angle_min: (-2/3)pi
            Angle_max: (2/3)pi
            Angle_increment: (1/300)pi
            Time_increment: Leave it unset if you wish
            Scan_time: The time difference in seconds between consecutive scans.

            Range_min: 1.0
            Range_max: 10.0
            Ranges: One dimensional array with elements of random floats between range_min and range_max, Use angle_min, angle_max, and angle_increment to determine the length. Be careful of an off-by-1 error! There should be an element at angle_min and angle_max.
            Intensities: Leave it unset if you wish
        """
        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.angle_min = -(2/3)*math.pi
        msg.angle_max = (2/3)*math.pi
        msg.angle_increment = (1/300)*math.pi
        # msg.time_increment = can leave unset
        msg.scan_time = 0.1 
        msg.range_min = 1.0
        msg.range_max = 10.0
        ranges = []
        for i in range(int(((msg.angle_max - msg.angle_min) / msg.angle_increment) + 1)):
            ranges.append(random.uniform(1.0, 10.0))
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
