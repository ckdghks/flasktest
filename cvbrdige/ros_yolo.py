from http.client import responses
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import cv2
import torch
import numpy as np


model = torch.hub.load('ultralytics/yolov5', 'yolov5m6', force_reload=True)

class ImageSub(Node):

    def __init__(self):
        super().__init__('yolov5')

        self.subscription = self.create_subscription(
            CompressedImage,
            'image_raw/compressed',
            self.yolo,
            10
        )
        self.subscription

        self.br = CvBridge()

    def listener_callback(self, data):
        self.get_logger().info('Receving video frame')

        current_frame = self.br.compressed_imgmsg_to_cv2(data)
        # cv2.imshow("camera", current_frame)
        # cv2.waitKey(1)
        return current_frame

    def yolo(self, data):
        frame = self.listener_callback(data)
        results = model(frame)
        
        results.ims     #imgs -> ims changes
        results.render()

        for im in results.ims:
            nparr1 = np.array(im)
            cv2.imshow("yolov5", nparr1)
            cv2.waitKey(1)



def main(args=None):
    rclpy.init(args=args)

    image_subscriber = ImageSub()

    rclpy.spin(image_subscriber)

    image_subscriber.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()
