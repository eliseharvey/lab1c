import rclpy
from rclpy.node import Node
import tf2_ros
import numpy as np
import geometry_msgs
import tf_transformations
import time

from geometry_msgs.msg import TransformStamped

from typing import Any


class BaseLinkTfPub(Node):

    def __init__(self):
        super().__init__('dynamic_tf_cam_publisher')

        # instantiate buffer that the listener will write to
        self.tfBuffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tfBuffer, self)

        # broadcaster that will publish the transform
        self.br = tf2_ros.TransformBroadcaster(self)

        timer_period = 1.0 / 20  # hz
        self.timer = self.create_timer(timer_period, self.node_callback)

        self.t = time.perf_counter()
        self.rotation_rate = 1  # Hz
        self.rotation_radius = 2.0  # meters

    def tf_to_se3(self, transform: TransformStamped.transform) -> np.ndarray:
        """
        Convert a TransformStamped message to a 4x4 SE3 matrix 
        """
        q = transform.rotation
        q = [q.x, q.y, q.z, q.w]
        t = transform.translation
        mat = tf_transformations.quaternion_matrix(q)
        mat[0, 3] = t.x
        mat[1, 3] = t.y
        mat[2, 3] = t.z
        return mat

    def se3_to_tf(self, mat: np.ndarray, time: Any, parent: str, child: str) -> TransformStamped:
        """
        Convert a 4x4 SE3 matrix to a TransformStamped message
        """
        obj = geometry_msgs.msg.TransformStamped()

        # current time
        obj.header.stamp = time.to_msg()

        # frame names
        obj.header.frame_id = parent
        obj.child_frame_id = child

        # translation component
        obj.transform.translation.x = mat[0, 3]
        obj.transform.translation.y = mat[1, 3]
        obj.transform.translation.z = mat[2, 3]

        # rotation (quaternion)
        q = tf_transformations.quaternion_from_matrix(mat)
        obj.transform.rotation.x = q[0]
        obj.transform.rotation.y = q[1]
        obj.transform.rotation.z = q[2]
        obj.transform.rotation.w = q[3]

        return obj

    def node_callback(self):
        """
        syntax note: lookup_transform args are (parent, child)
        additional note: rclpy.time.Time() gives you time zero (not the current time).
                         However, when you are looking up transforms, passing in time 
                         zero tells ROS to give you the most recent transform.
        """
        ## set up
        try:
            tf_left_cam_to_world: TransformStamped = self.tfBuffer.lookup_transform('world', 'left_cam',
                                                                                 rclpy.time.Time())
        except tf2_ros.TransformException:
            self.get_logger().info('No transform from left_cam to world found')
            return
        left_cam_to_world: np.ndarray = self.tf_to_se3(tf_left_cam_to_world.transform)
        now = self.get_clock().now()
        ## compute world to baselink (note: baselink is the robot!) by (LC to world)^-1 * (LC to robot)
        robot_to_left_cam_translation = np.array([0.05, 0, 0]).T # -1*-0.05
        robot_to_left_cam = np.eye(4)
        robot_to_left_cam[:3, -1] = robot_to_left_cam_translation[:3]
        ## compute world to robot (what we are broadcasting)
        world_to_robot = np.linalg.inv(left_cam_to_world) @ robot_to_left_cam
        ## broadcasst
        tf_world_to_robot = self.se3_to_tf(world_to_robot, now, parent='world', child='base_link_gt_2')
        self.br.sendTransform([tf_world_to_robot])  
        ## log
        self.get_logger().info('Published')


def main(args=None):
    rclpy.init(args=args)

    node = BaseLinkTfPub()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()