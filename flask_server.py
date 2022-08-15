from email import header
from cv2 import waitKey
from flask import Flask,  jsonify, request, render_template
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
    header = request.headers
    contentType = header.get('content-type')
    print(contentType)
    # request.on_json_loading_failed = on_json_loading_failed_return_dict
    dict_data = request.get_json()
    return jsonify(dict_data)
    # print(request.get_json(force=True))
    # print(dict_data)

    img = dict_data['img']
    
    # test static images
    # dataurl = "images/output.png"
    # return render_template('image.html', image_data=dataurl)

    # dataurl = 'data:image/png;base64,' + base64.b64encode(img.getvalue()).decode('UTF-8')
    dataurl = 'data:image/png;base64,' + img
    return render_template('image.html', image_data=dataurl)
    
    return "{}".format(jsonify(dict_data))

if __name__ == "__main__":
    app.debug = True
    app.run(host="172.30.1.50", port=5000)
