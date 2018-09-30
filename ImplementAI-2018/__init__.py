import cv2
import numpy as np
from flask import Flask, render_template, Response, jsonify, request
from flask.json import jsonify
from .camera import VideoCamera
from waitress import serve


app = Flask(__name__)

video_camera = None
global_frame = None

@app.route("/")
def serve_frontend():
	return render_template("home.html")

@app.route("/process", methods=['POST'])
def process():
	if (request.method =='POST'):
		file_bytes = request.files['file'].read()
		nparr = np.fromstring(file_bytes, np.uint8)
		img_np = cv2.imdecode(nparr,0)

		# Work with openpose here

		return "received"

@app.route("/record_status", methods=["POST"])
def record_status():
	global video_camera
	if video_camera == None:
		video_camera = VideoCamera()

	json = request.get_json()

	status = json['status']

	if status == "true":
		video_camera.start_record()
		return jsonify(result="started")
	else:
		video_camera.stop_record()
		status = 'false'
		return jsonify(result="stopped")


@app.route("/video_stream")
def video_stream():
	global video_camera
	global global_frame

	if video_camera == None:
		video_camera = VideoCamera()

	while True:
		frame = video_camera.get_frame()

		if frame != None:
			global_frame = frame
			yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
		else:
			yield (b'--frame\r\n'
				   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')


@app.route("/video_viewer")
def video_viewer():
	return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
	serve(app)