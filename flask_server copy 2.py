from email import header
from email.policy import strict
from pickletools import uint8
from cv2 import waitKey
from flask import Flask,  jsonify, request, render_template, send_file
from PIL import Image
import json
from io import BytesIO
import base64
import numpy as np
import cv2
import requests

app = Flask(__name__)

def on_json_loading_failed_return_dict(e):
    return {}

@app.route("/", methods=["GET", "POST"])
def index():
    
    ## header
    header = request.headers
    contentType = header.get('content-type')
    print(contentType) # application/json
   
    if not request.json or 'img' not in request.json:
        print('400')
    
    im_b64 = request.json['img']

    img_bytes = base64.b64decode(im_b64.encode('utf-8'))

    img = Image.open(BytesIO(img_bytes))

    img_arr =  np.asarray(img)
    print('img shape', img_arr.shape)

    return str(img_arr)


if __name__ == "__main__":
    app.debug = True
    app.run(host="172.30.1.21", port=5000)
    # app.run(host="172.20.10.5", port=5000)
