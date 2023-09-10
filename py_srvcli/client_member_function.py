import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, PointCloud2
from nav_msgs.msg import Path
from cv_bridge import CvBridge
import cv2
from ultralytics import YOLO
import requests
import json


class ImageAndLidarListener(Node):

    def __init__(self):
        super().__init__('image_and_lidar_listener')
        self.image_subscription = self.create_subscription(
            Image,
            '/OAK_D_back/color/preview/image',  # Modify to the correct image topic
            self.image_callback,
            10  # QoS profile depth
        )
        self.lidar_subscription = self.create_subscription(
            PointCloud2,
            '/points',  # Modify to the correct lidar topic
            self.lidar_callback,
            10  # QoS profile depth
        )
        self.path_subscription = self.create_subscription(
            Path,
            '/lio_sam/mapping/path',
            self.path_callback,
            10  # QoS
        )
        self.cv_bridge = CvBridge()
        self.pothole_detector = YOLO('yolov8s-pothole-detector.pt')

    def image_callback(self, msg):
        try:
            # Convert the ROS Image message to an OpenCV image
            cv_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            results = self.pothole_detector(cv_image)
            annotated_frame = results[0].plot()

            cv2.imshow('Annotated frame', annotated_frame)
            cv2.waitKey(1)  # Update the image window
        except Exception as e:
            self.get_logger().error(f"Error processing image: {str(e)}")

    def lidar_callback(self, msg):
        try:
            # Process the PointCloud2 data and visualize it
            # Example: Print the number of points in the cloud
            num_points = msg.width * msg.height
            # self.get_logger().info(f"Received PointCloud2 with {num_points} points")

        except Exception as e:
            self.get_logger().error(f"Error processing lidar data: {str(e)}")

    def path_callback(self, msg):
        try:
            path = msg

            payload = []
            for pose_stamped in path.poses:
                x = pose_stamped.pose.position.x
                y = pose_stamped.pose.position.y
                z = pose_stamped.pose.position.z
                payload.append((float(x), float(y), float(z)))
            self.get_logger().info(f"PATH {payload}")

            payload = json.dumps(payload)

            headers = {'Content-Type': 'application/json'}
            response = requests.post("http://127.0.0.1:5000/store_path", data=payload, headers=headers)

            if response.status_code != 200:
                self.get_logger().info("Something went wrong: couldn't send my path\n\n")
        except Exception as e:
            self.get_logger().error(f"Error processing pose data: {str(e)}")




def main(args=None):
    rclpy.init(args=args)
    node = ImageAndLidarListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

