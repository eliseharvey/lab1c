from geometry_msgs.msg import TransformStamped
import rclpy
from rclpy.node import Node
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster


class StaticTfCamPublisher(Node):
    """
    Broadcast transforms that never change. This publishes the left_cam and right_cam 
    relatic to base_link_gt. The transforms are only published once at startup, and are constant for all
    time.
    """

    def __init__(self):
        super().__init__('static_tf_cam_publisher')
        self.tf_static_broadcaster = StaticTransformBroadcaster(self)
        # publish static transforms once at startup
        self.make_transforms()

    def make_transforms(self):
        # left cam
        left_cam = TransformStamped()
        left_cam.header.stamp = self.get_clock().now().to_msg()
        left_cam.header.frame_id = 'base_link_gt'
        left_cam.child_frame_id = 'left_cam'
        left_cam.transform.translation.x = -0.05
        left_cam.transform.translation.y = 0.0
        left_cam.transform.translation.z = 0.0
        # right cam
        right_cam = TransformStamped()
        right_cam.header.stamp = self.get_clock().now().to_msg()
        right_cam.header.frame_id = 'base_link_gt'
        right_cam.child_frame_id = 'right_cam'
        right_cam.transform.translation.x = 0.05
        right_cam.transform.translation.y = 0.0
        right_cam.transform.translation.z = 0.0
        # publish both - can only broadcase once so put mutliple into br
        self.tf_static_broadcaster.sendTransform([left_cam, right_cam])
        self.get_logger().info('Published both')


def main():
    rclpy.init()
    node = StaticTfCamPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()