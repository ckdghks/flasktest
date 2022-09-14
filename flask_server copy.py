from flask import Flask,  jsonify, request, render_template
from PIL import Image
import json
from io import BytesIO
import base64
import numpy as np
import cv2

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    with open("./static/images/test.jpg", "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())
    


    dataurl = 'data:image/jpeg;base64,' + b64_string.decode('utf-8')
    return '<body> <img src="{}"> </body>'.format(dataurl)
    # return cv2.imshow("img", img), cv2.waitKey(0)
    # image = Image.open(img)
    # image.save('/home/parallels/data/output.png', 'png')

    

if __name__ == "__main__":
    app.debug = True
    app.run(host="172.30.1.93", port=5000)
