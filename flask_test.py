from crypt import methods
from flask import Flask, request
import json
import requests
from werkzeug.utils import secure_filename
from db.db_test import db, User

app = Flask(__name__)
db.create_all()
app.secret_key = '0000'
@app.route("/")
def hello():
    return "<h1> Hello World!</h1>"

@app.route("/send_post", methods=['GET'])
def send_post():
    params = {
        "param1" : "test1",
        "param2" : 123,
        "param3" : "test3"
    }
    res = requests.post("http://172.30.1.21:5000/handle_post", data=json.dumps(params))
    return res.text

@app.route("/handle_post", methods=['GET', 'POST'])
def handle_post():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'

    params_str = ''
    for key in params.keys():
        params_str += 'key: {}, value: {}<br>'.format(key, params[key])
    return params_str

@app.route("/anyReq", methods=['GET', 'POST'])
def anyreq():
    # print("values: ", request.values) 
    if request.method == 'POST':
        print("post: ", request.form.get('postData'))
        admin = User(name='post', data=request.form.get('postData'))

        db.session.add(admin)
        db.session.commit()
        print(User.query.all())
        # return request.args.get('getData')
        return 'post'
    else:
        return 'get'


host_addr = "172.30.1.21"
port_num = "5000"

if __name__ == "__main__":
    app.debug = True    
    app.run(host=host_addr, port=port_num)