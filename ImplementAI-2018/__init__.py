import cv2
import numpy as np
from flask import Flask, render_template, Response, jsonify, request
from flask.json import jsonify
from flask_cors import CORS, cross_origin
from .camera import VideoCamera
from waitress import serve


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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



@app.route("/improv_json", methods=["GET"])
@cross_origin()
def improv_json():
	# temp = video_camera.current_info
	# format some stuff
	temp = {"foo": "bar"}

	temp = {
    "pose": "Squat",
    "comment": {
        "comment1": "Back is off by 10 degrees",
        "comment2": "Arm angle should be 180 degrees",
        "comment3": "Knees are too slanted at 30 degrees"
    },
    "tip": {
        "tip1": "Straighten your back more",
        "tip2": "Arms need to be straight",
        "tip3": "Knees can't be more forward than your toes"
    }
}

	if video_camera and video_camera.temp_info.get('error'):
		temp["pose"] = "Squat Error [{}]".format(video_camera.temp_info['error'])
	response = jsonify(temp)
	# response.headers.add('Access-Control-Allow-Origin', '*')
	return response



if __name__ == "__main__":
	serve(app)
