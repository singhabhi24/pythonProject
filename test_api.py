# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
import json
from Am1Json import Am1JSON
from collections import namedtuple
from json import JSONEncoder

# from typing import List

# creating a Flask app
app = Flask(__name__)


# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        data = "hello world"
        return jsonify({'data': data})


# A simple function to calculate the square of a number
# the number to be squared is sent in the URL when we use GET
# on the terminal type: curl http://127.0.0.1:5000 / home / 10
# this returns 100 (square of 10)
@app.route('/home/<int:num>', methods=['GET'])
def disp(num):
    print(num)
    return jsonify({'data': num ** 2})


@app.route('/setData/', methods=['POST'])
def setData():
    data = request.data
    r = json.loads(data)
    jsonRes = json.dumps(r, indent=4, cls=StudentEncoder)
    # print("JSON Res")
    # print(jsonRes)
    obj = Am1JSON()
    obj.set_gpsis(r['gpsis'])
    print(obj.get_gpsis())
    success = obj.get_gpsis()
    return jsonify({' set in the backend i.e:': success})


class StudentEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


# driver function
if __name__ == '__main__':
    app.run(debug=True)
