from http.client import responses
from urllib import response
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import cv2
import requests
import json
import torch
from io import BytesIO
import base64
from PIL import Image
import numpy as np

client_id = "z4vt1p0gu1"
client_secret = "zEKZLR3LXbngOH6e789YjCFMoGHJqAfQXr950Ba3"
url = "https://naveropenapi.apigw.ntruss.com/vision-obj/v1/detect"
headers = {'X-NCP-APIGW-API-KEY-ID': client_id, 'X-NCP-APIGW-API-KEY': client_secret}

model = torch.hub.load('ultralytics/yolov5', 'yolov5m6', force_reload=True)

class ImageSub(Node):

    def __init__(self):
        super().__init__('image_subscriber')

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

    def test(self, data):
        frame = self.listener_callback(data)
        cv2.imwrite('./images/test.jpg', frame)

        # files = {'image': frame.tobytes()}
        files = {'image': open('./images/test.jpg', 'rb')}
        response = requests.post(url, files=files, headers=headers)
        rescode = response.status_code
        if(rescode == 200):
            # print(response.text)
            naver_objectDetection(response.text, frame)
        else:
            print("Error Code: " + str(rescode))


    def yolo(self, data):
        frame = self.listener_callback(data)
        results = model(frame)
        
        results.ims     #imgs -> ims changes
        results.render()

        for im in results.ims:
            nparr1 = np.array(im)
            cv2.imshow("yolov5", nparr1)
            cv2.waitKey(1)



def naver_objectDetection(results, frame):
    height, width, _ = frame.shape
    # print(type(results))
    # print(type(json.loads(results)))
    dict1 = json.loads(results)
    # print(dict1["predictions"])
    obj_index = dict1["predictions"][0]['num_dectetions']
    print(obj_index)
    ret_name = dict1["predictions"][0]['detection_names']
    ret_scores = dict1["predictions"][0]['detection_scores']
    ret_boxes = dict1["predictions"][0]['detection_boxes']
    # print(type(ret_boxes[1][0]))
    cv2.rectangle(frame, (int(ret_boxes[1][0] * width), int(ret_boxes[1][1]) * height), (int(ret_boxes[1][2] * width), int(ret_boxes[1][3]* height)), (255, 0, 0), 3)
    
    cv2.imshow("camera", frame)
    cv2.waitKey(1)

'''
[
    {
        'num_detections' : 3,
        'detection_classes': [27.0, 62.0, 62.0],
        'detection_names': ['backpack', 'chair', 'chair'],
        'detection_scores': [0.933899, 0.929769, 0.525905],
        'detection_boxes': [
                            [0.763873, 0.309685, 0.983145, 0.598012], 
                            [0.796134, 0.890211, 0.986239, 1.0], 
                            [0.884725, 0.0995454, 0.997397, 0.32092]
                           ]
    }
]
'''




def main(args=None):
    rclpy.init(args=args)

    image_subscriber = ImageSub()

    rclpy.spin(image_subscriber)

    image_subscriber.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()
