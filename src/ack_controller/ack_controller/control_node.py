import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Point


class ControlNode(Node):

    def __init__(self):
        super().__init__('control_node')
        self.sub = self.create_subscription(Point, '/box_centroid', self.centroid_callback, 10)
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.image_cx     = 320.0
        self.kp_angular   = 0.004
        self.linear_speed = 0.4
        self.search_speed = 0.15   # creep forward when box not in view
        self.stop_area    = 6000.0
        self.min_area     = 50.0

        self.get_logger().info('ControlNode started — visual servoing active')

    def centroid_callback(self, msg: Point):
        twist = Twist()
        area = msg.z

        # Box not detected — creep forward to search
        if msg.x == 0.0 and msg.y == 0.0 and area == 0.0:
            twist.linear.x = self.search_speed
            self.get_logger().warn('Box not detected — searching forward')
            self.pub.publish(twist)
            return

        # Ignore tiny noise detections
        if area < self.min_area:
            twist.linear.x = self.search_speed
            self.pub.publish(twist)
            return

        # Stop if close enough
        if area >= self.stop_area:
            self.get_logger().info(f'Reached box! area={area:.0f} — stopping')
            self.pub.publish(twist)  # zero twist
            return

        # Visual servoing — drive + steer toward centroid
        error_x = self.image_cx - msg.x
        twist.linear.x  = self.linear_speed
        twist.angular.z = self.kp_angular * error_x

        self.get_logger().info(
            f'Driving → linear={twist.linear.x:.2f}  '
            f'angular={twist.angular.z:.3f}  '
            f'error={error_x:.1f}  area={area:.0f}'
        )
        self.pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = ControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()