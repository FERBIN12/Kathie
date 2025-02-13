#!/usr/bin/env python3

import rclpy 
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped

class TwistRelay(Node):
    def __init__(self):
        super().__init__("twist relay")

        self.controller_sub_ = self.create_subscription(
            Twist,
            "/nina_controller/cmd_vel_unstamped",
            self.controller_twist_cb,
            10
            )
        self.controller_pub_ = self.create_publisher(
            TwistStamped,
            "/nina_controller/cmd_vel",
            10
    
        )

        self.key_sub_ = self.create_subscription(
            TwistStamped,
            "/input_vel/cmd_vel_stamped",
            self.key_sub_cb,
            10
        )

        self.key_pub_ = self.create_publisher(
            Twist,
            "/input_vel/cmd_vel",
            10
        )

    def controller_twist_cb(self, msg):
        twist_stamped = TwistStamped()
        twist_stamped.header.stamp = self.get_clock().now()
        twist_stamped.twist = msg
        self.controller_pub_.publish(twist_stamped)

    def key_sub_cb(self, msg):
        twist = Twist()
        twist = msg.twist
        self.key_pub_.publish(twist)


def main():
    rclpy.init()
    node = TwistRelay()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    

if __name__ == '__main__':
    main()