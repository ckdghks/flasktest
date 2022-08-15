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
    json_data = request.get_json(force=True)
    json_str = json.dumps(json_data)
    dict_data = json.loads(json_str)

    img = dict_data['img']
    img = base64.b64decode(img)
    img = BytesIO(img)
    
    # img = np.array(Image.open(BytesIO(img)))
    # image.save(img, 'PNG')
    dataurl = 'data:image/png;base64,' + base64.b64encode(img.getvalue()).decode('ascii')
    return render_template('image.html', image_data=dataurl)
    # return cv2.imshow("img", img), cv2.waitKey(0)
    # image = Image.open(img)
    # image.save('/home/parallels/data/output.png', 'png')

    

if __name__ == "__main__":
    app.debug = True
    app.run(host="172.30.1.50", port=5000)
