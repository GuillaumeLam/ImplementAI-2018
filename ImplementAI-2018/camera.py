# From Github: yushulx/web-camera-recorder link: https://github.com/yushulx/web-camera-recorder.git

import cv2
import threading
import sys
import os
from sys import platform
from openpose import get_openpose
from analysis.Pose import Pose, get_pose_keypoint_errors
import pickle
import matplotlib.pyplot as plt
import numpy as np

class RecordingThread(threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('./static/video.avi', fourcc, 20.0, (640, 480))


    def run(self):
        while self.isRunning:
            ret, frame = self.cap.read()
            if ret:
                self.out.write(frame)

        self.out.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()


class VideoCamera(object):
    def __init__(self):
        # Open a camera
        self.cap = cv2.VideoCapture(0)

        # Initialize video recording environment
        self.is_record = False
        self.out = None

        # Thread for recording
        self.recordingThread = None
        self.plot_test = []
        self.count = 0

        self.params = dict()
        self.params['logging_level'] = 3
        self.params["output_resolution"] = "-1x-1"
        self.params["net_resolution"] = "-1x368"
        self.params["model_pose"] = "BODY_25"
        self.params["alpha_pose"] = 0.6
        self.params["scale_gap"] = 0.3
        self.params["scale_number"] = 1
        self.params["render_threshold"] = 0.05
        self.params["num_gpu_start"] = 0
        self.params["disable_blending"] = False
        self.openpose = get_openpose(self.params)

        with open('./analysis/ref_squat.p', "rb") as file_obj:
            ref_squat_keypoints, ref_squat_img = pickle.load(file_obj)
        self.ref_squat_pose = Pose(ref_squat_keypoints[0], ref_squat_img)

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        ret, frame = self.cap.read()

        keypoints, output_image = self.openpose.forward(frame, True)
        pose = Pose(keypoints[0], output_image)
        error_dict = get_pose_keypoint_errors(pose, self.ref_squat_pose)
        error = 0
        for v in error_dict.values():
            error += v
        print(error)
        self.plot_test.append(error)


        if ret:
            ret, jpeg = cv2.imencode('.jpg', output_image)
            
            # Record video
            # if self.is_record:
            #     if self.out == None:
            #         fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            #         self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))

            #     ret, frame = self.cap.read()
            #     if ret:
            #         self.out.write(frame)
            # else:
            #     if self.out != None:
            #         self.out.release()
            #         self.out = None

            return jpeg.tobytes()

        else:
            return None

    def start_record(self):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False
        plt.plot(self.plot_test)
        plt.show()
        if self.recordingThread != None:
            self.recordingThread.stop()
