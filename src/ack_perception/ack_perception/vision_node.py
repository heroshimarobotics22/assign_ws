import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge
import cv2
import numpy as np


class VisionNode(Node):

    def __init__(self):
        super().__init__('vision_node')

        self.bridge = CvBridge()

        # Subscriber: camera image from Gazebo
        self.sub = self.create_subscription(
            Image,
            '/camera/image',
            self.image_callback,
            10
        )

        # Publisher: detected box centroid (x, y in pixels; z = area)
        self.pub = self.create_publisher(Point, '/box_centroid', 10)

        # Publisher: debug image with bounding box
        self.debug_pub = self.create_publisher(Image, '/camera/debug_image', 10)

        self.get_logger().info('VisionNode started — detecting GREEN box')

    def image_callback(self, msg):
        # Convert ROS Image → OpenCV BGR
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # Convert BGR → HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # ── GREEN HSV range ──────────────────────────────
        # Ignores red (decoy) and blue (decoy)
        lower_green = np.array([40,  80,  80])
        upper_green = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # Morphological cleanup
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

        centroid = Point()

        if contours:
            # Pick the largest contour (most likely the target box)
            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)

            if area > 50:  # filter out noise
                x, y, w, h = cv2.boundingRect(largest)
                cx = x + w // 2
                cy = y + h // 2

                centroid.x = float(cx)
                centroid.y = float(cy)
                centroid.z = float(area)  # area as confidence

                self.get_logger().info(
                    f'Box detected → centroid=({cx},{cy})  area={area:.0f}'
                )

                # Draw bounding box on debug image
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                cv2.putText(frame, f'TARGET ({cx},{cy})',
                            (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 2)
            else:
                self.get_logger().debug('Contour too small — ignored')
        else:
            self.get_logger().debug('No green object detected')

        # Always publish centroid (zeros if not detected)
        self.pub.publish(centroid)

        # Publish debug image
        debug_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        self.debug_pub.publish(debug_msg)


def main(args=None):
    rclpy.init(args=args)
    node = VisionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()