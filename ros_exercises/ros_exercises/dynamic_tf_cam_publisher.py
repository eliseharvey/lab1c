import rclpy
from rclpy.node import Node
import tf2_ros
import numpy as np
import geometry_msgs
import tf_transformations
import time

from geometry_msgs.msg import TransformStamped

from typing import Any


class DynamicTfCamPublisher(Node):

    def __init__(self):
        super().__init__('dynamic_tf_cam_publisher')

        # # set use sim time param to be true by default
        # self.set_parameters([rclpy.parameter.Parameter('use_sim_time', rclpy.Parameter.Type.BOOL, True)])

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
            tf_robot_to_world: TransformStamped = self.tfBuffer.lookup_transform('world', 'base_link_gt',
                                                                                 rclpy.time.Time())
        except tf2_ros.TransformException:
            self.get_logger().info('no transform from base_link_gt to world found')
            return

        robot_to_world: np.ndarray = self.tf_to_se3(tf_robot_to_world.transform)
        now = self.get_clock().now()

        ############################# Example from lecture/lab #############################
        # new_t = time.perf_counter()
        # time_elapsed = new_t - self.t

        # angle = 2 * np.pi * self.rotation_rate * time_elapsed

        # Z forward, X right, Y down
        
        # moon_to_robot_translation = [self.rotation_radius * np.cos(angle), 0, self.rotation_radius * np.sin(angle)]
        # moon_to_robot_translation = np.array(moon_to_robot_translation).T

        # moon_to_robot = np.eye(4)
        # moon_to_robot[:3, -1] = moon_to_robot_translation[:3]

        # now = self.get_clock().now()

        # # First way: chain with robot_to_world to produce moon_to_world
        # moon_to_world: np.ndarray = robot_to_world @ moon_to_robot
        # tf_moon_to_world = self.se3_to_tf(moon_to_world, now, parent='world', child='moon')
        # self.br.sendTransform([tf_world_to_robot, tf_moon_to_world])

        # # Easier way: no need to chain with robot_to_world

        # tf_moon_to_robot = self.se3_to_tf(moon_to_robot, now, parent='base_link_gt', child='moon')
        # self.br.sendTransform([tf_world_to_robot, tf_moon_to_robot])
        ############################# Example from lecture/lab #############################

        ## left camera (Z forward, X right, Y down)
        left_cam_to_robot_translation = [-0.05, 0, 0] # -0.05 (left) relative to base_line_gt pose
        left_cam_to_robot_translation = np.array(left_cam_to_robot_translation).T
        left_cam_to_robot = np.eye(4)
        left_cam_to_robot[:3, -1] = left_cam_to_robot_translation[:3]

        ## right camera
        right_cam_to_left_translation = [0.1, 0, 0] # 0.1 (right) relative to left pose
        right_cam_to_left_translation = np.array(right_cam_to_left_translation).T
        right_cam_to_left = np.eye(4)
        right_cam_to_left[:3, -1] = right_cam_to_left_translation[:3]

        ## left to world
        left_cam_to_world: np.ndarray = robot_to_world @ left_cam_to_robot
        tf_left_cam_to_world = self.se3_to_tf(left_cam_to_world, now, parent='base_link_gt', child='left_cam')
        self.br.sendTransform([tf_robot_to_world, tf_left_cam_to_world])

        ## right to left
        right_cam_to_left: np.ndarray = right_cam_to_left
        tf_right_cam_to_left = self.se3_to_tf(right_cam_to_left, now, parent='left_cam', child='right_cam')
        self.br.sendTransform([tf_left_cam_to_world, tf_right_cam_to_left])        

        ## log
        self.get_logger().info('Published')


def main(args=None):
    rclpy.init(args=args)

    node = DynamicTfCamPublisher()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()