from flask import Flask
from flask import request
from flask.json import jsonify
import numpy as np
import cv2
import pickle
import requests

app = Flask(__name__)

@app.route("/process", methods=['POST'])
def process():
	if (request.method =='POST'):
		file_bytes = request.files['file'].read()
		nparr = np.fromstring(file_bytes, np.uint8)
		img_np = cv2.imdecode(nparr,0)

		# Work with openpose here

		return "recieved"