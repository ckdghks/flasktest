import base64
from http import client
from io import BytesIO
import logging
import time
from typing import Any
from flask import Flask, jsonify

import roslibpy

import cv2
import numpy as np
import sys

import torch
from PIL import Image
from io import BytesIO

import requests
import json
# import paramiko

# try:
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
#     ssh.connect("172.30.1.25", username="ubuntu", password="turtlebot")
#     print('ssh connected')

#     ssh.exec_command("ros2 run v4l2_camera v4l2_camera_node")
#     ssh.exec_command("ros2 launch rosbridge_server rosbridge_websocket_launch.xml")
#     time.sleep(10)

# except Exception as err:
#     print(err)

# Configure logging
fmt = '%(asctime)s %(levelname)8s: %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO)
log = logging.getLogger(__name__)

client = roslibpy.Ros(host='172.30.1.25', port=9090)
model = torch.hub.load('ultralytics/yolov5', 'yolov5n')

def receive_image(msg):
    log.info('Received image stamp=%d', msg['header']['stamp']['sec'])
    base64_bytes = msg['data'].encode('ascii')
    image_bytes = base64.b64decode(base64_bytes)
    # print(image_bytes)
    decoded = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
    return decoded
    # route = 'C:/Users/ccww2/OneDrive/바탕 화면/22-1학기/DIP-20220404T112251Z-001/newsrc/data2/received-image-{}.{}.jpg'.format(msg['header']['stamp']['sec'], msg['format'])
    # with open(route , 'wb') as image_file:
    #     image_file.write(image_bytes)

def yolo(decoded):

    result = model(decoded)

    result.imgs
    result.render()
    for im in result.imgs:
        bufferd = BytesIO()
        im_base64 = Image.fromarray(im)
        im_base64.save(bufferd, format="JPEG")
        return base64.b64encode(bufferd.getvalue()).decode()

def M(msg):
    decoded = receive_image(msg)
    result = yolo(decoded)
    files = {'img': result}
    files = json.dumps(files)
    post_image(files)


def post_image(files):
    headers = {'Content-Type': "application/json", 'charset':'utf-8'}

    r = requests.post("http://172.30.1.50:5000", data=files, headers=headers)
    # print(r.status_code)
    header = r.headers
    contentType = header.get('content-type')
    print(contentType)

subscriber = roslibpy.Topic(client, '/image_raw/compressed', 'sensor_msgs/msg/CompressedImage')
subscriber.subscribe(M)

client.run_forever()
