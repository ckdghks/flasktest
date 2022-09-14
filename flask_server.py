from email import header
from email.policy import strict
from pickletools import uint8
import queue
from re import template
from cv2 import waitKey
from flask import Flask,  jsonify, request, render_template, send_file, make_response
from PIL import Image
import json
from io import BytesIO
import base64
import numpy as np
import cv2
import requests
from ast import Bytes, literal_eval

from queue import Queue


class StreamWriter(object):
    def __init__(self) -> None:
        self.queue = Queue()
    
    def write(self, str):
        self.queue.put(str)
    
    def read(self):
        str = self.queue.get()
        self.queue.task_done()
        return str

app = Flask(__name__)

def on_json_loading_failed_return_dict(e):
    return {}

def is_json(obj):
    try:
        json.loads(obj)

    except ValueError as e:
        return False
    return True

@app.route("/", methods=["GET", "POST"])
def index():
    
    ## header
    header = request.headers
    contentType = header.get('content-type')
    print(contentType) # application/json


    # data = request.data
    # str = request.data.decode('utf-8')
    # print(str)  #   "{\"img\": \"(data)\"}"    class<type> == str
    # str2 = literal_eval(str)
    # print(str2) #   {"img": "(data)"}   class<type> == str   
    # dict = literal_eval(str2)
    # print(dict) # {'img': '(data)'} class<type> == str
    # img = dict['img']
    # print(img)  # (data)    class<type> == str
    
    # ## decoded images to numpy
    # jpg_arr = np.frombuffer(img, dtype=np.uint8)
    # img = cv2.imdecode(jpg_arr, cv2.IMREAD_COLOR)   # numpy array

    # ## save np to jpg
    # cv2.imwrite('./static/images/test.jpg', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    if request.method == 'POST':
        data = request.form.get('img')
        ## convert color
        imgdata = base64.b64decode(data)
        dataBytesIO = BytesIO(imgdata)
        image = Image.open(dataBytesIO)
        img_RGB = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_RGB)
        buff = BytesIO()
        pil_img.save(buff, format="JPEG")
        new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
        
        f = open('./templates/test.html', 'w')

        f.write(render_template('image.html', img=new_image_string))
        f.close
    else:
        return render_template('test.html')

    
    
    return 'testing'
    return render_template('image.html', img=data)
    # resp = make_response(render_template('image.html', image_file='images/test.jpg'))
    # # resp = make_response(dict_data)
    # resp.headers['content-type'] = 'application/json'
    # return resp



if __name__ == "__main__":
    app.debug = True
    app.run(host="172.30.1.63", port=5000)
    # app.run(host="172.20.10.5", port=5000)
    # app.run(host="172.30.1.21", port=5000)    # home 

