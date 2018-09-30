import cv2
import os
import pickle
import numpy as np
from analysis.Pose import Pose

dir_path = os.path.dirname(os.path.realpath(__file__))


def main():
    # Setup

    # Load Keypoints
    with open("ref_squat.p", "rb") as file_obj:
        all_keypoints, output_image = pickle.load(file_obj)

    # Parse Poses
    poses = []
    for keypoints in all_keypoints:
        poses.append(Pose(keypoints, output_image))

    cv2.imshow("output", output_image)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
