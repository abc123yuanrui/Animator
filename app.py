from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
import os
import cv2
import sys
import io
import numpy as np
from PIL import Image
from werkzeug import secure_filename
sys.path.append('./Cartoon')
from cartoonizer import cartoonize


app = Flask(__name__)
CORS(app)
@app.route('/')
def index():
    return 'come on!'

@app.route("/ImgProcess", methods=['GET', 'POST'])
@cross_origin()
def sage_img():
    imgFile = request.files["myImage"]
    if "myImage" not in request.files:
        return jsonify({'error': 'No data provided.'}), 400
    nparr = np.frombuffer(imgFile.read(), dtype=np.uint8)
    imgInBGR = cv2.imdecode(nparr, flags=1)
    imgIn = cv2.cvtColor(imgInBGR , cv2.COLOR_BGR2RGB)
    imgOut =cartoonize(imgIn)
    im = Image.fromarray(imgOut)
    # create file-object in memory
    file_object = io.BytesIO()
    # write PNG in file-object
    im.save(file_object,"PNG")
    # move to beginning of file so `send_file()` it will read from start  
    file_object.seek(0)
    # send file directly:
    return send_file(file_object,
                     attachment_filename='processedImg.PNG',
                     mimetype='image/PNG')
    # send base64 string (cost high resources):
    # res={}
    # base64Out = base64.b64encode(imgOut)
    # res['processedImg']=[str(base64Out)]
    # print(jsonify(res))
    # return jsonify(res)

if __name__== "__main__":
    app.run()