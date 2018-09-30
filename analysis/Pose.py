import numpy as np

# Mapping for OpenPose Body25 index -> keypoint name
index_to_joint_map = {
        0: "Nose",
        1: "Neck",
        2: "RShoulder",
        3: "RElbow",
        4: "RWrist",
        5: "LShoulder",
        6: "LElbow",
        7: "LWrist",
        8: "MidHip",
        9: "RHip",
        10: "RKnee",
        11: "RAnkle",
        12: "LHip",
        13: "LKnee",
        14: "LAnkle",
        15: "REye",
        16: "LEye",
        17: "REar",
        18: "LEar",
        19: "LBigToe",
        20: "LSmallToe",
        21: "LHeel",
        22: "RBigToe",
        23: "RSmallToe",
        24: "RHeel",
    }


class Pose:

    def __init__(self, keypoints, image):
        # Keypoints
        self.image = image
        self.keypoints = keypoints
        if self.keypoints.shape != (25, 3):
            raise ValueError("Wrong size for keypoints. Expected (25, 3), got: [{}]".format(keypoints.shape))
        self.confidence = keypoints[:,2]

        x_mean = np.mean(keypoints[:,0][np.where(keypoints[:,2]>0.2)])
        y_mean = np.mean(keypoints[:,1][np.where(keypoints[:,2]>0.2)])
        self.keypoints[np.where(keypoints[:,2]<0.2)] = x_mean
        self.keypoints[np.where(keypoints[:,2]<0.2)] = y_mean

        self.keypoints = keypoints[:, :2]

        # Map Keypoints so their co-ordinates can be accessed by their joint names.
        self.keypoint_dict = self._get_keypoint_dict(self.keypoints)

        # Compute the vectors between joints in Cartesian co-ordinates where mid-hip is (0, 0).
        self.cartesian_keypoints = self._get_cartesian_keypoints()
        self.cartesian_keypoint_dict = self._get_keypoint_dict(self.cartesian_keypoints)

        # Compute the inner angles between significant joints.
        self.cartesian_joint_angles = self._get_cartesian_joint_angles()

        # Transform the cartesian co-ordinates to [0,1] in x and y.
        self.normalized_keypoints = self._get_normalized_keypoints()
        self.normalized_keypoints_dict = self._get_keypoint_dict(self.normalized_keypoints)
        self.mirrored_keypoints = self._get_mirrored_keypoints()

        #from matplotlib import pyplot as plt
        #x, y = self.normalized_keypoints.T

        #print(self.normalized_keypoints)

        #plt.scatter(x, y)
        #plt.show()

    @staticmethod
    def _get_keypoint_dict(keypoints):
        """
        Returns a dictionary where the joint name maps to it's co-ordinates.
        """
        keypoint_dict = {}

        for i, key in enumerate(index_to_joint_map.values()):
            keypoint_dict[key] = keypoints[i, :]
        return keypoint_dict

    def _get_mirrored_keypoints(self):

        mirrored_keypoint_dict = {}

        for i,key in enumerate(index_to_joint_map.values()):
            x,y = self.normalized_keypoints_dict[key]
            delta = abs(x-0.5)
            if(x<0.5):
                mirrored_keypoint_dict[key] = x + 2*delta, y
            elif(x>0.5):
                mirrored_keypoint_dict[key] = x-2*delta,y
            else:
                mirrored_keypoint_dict[key] = x,y

        return mirrored_keypoint_dict


    def _get_cartesian_keypoints(self):
        """
        Transforms the keypoints to the cartesian co-ordinates centered on the MidHip.
        Returns a (25, 2) numpy-array.
        """
        midhip_x, midhip_y = self.keypoint_dict['MidHip']

        transformed_coords = np.zeros((25, 2), dtype=float)
        # print('===================================================')
        # print('Cartesian Transformation')
        for i, joint_coord in enumerate(self.keypoints):
            # print(i)
            # print(index_to_joint_map[i], joint_coord)
            joint_x, joint_y = joint_coord
            new_x, new_y = (joint_x - midhip_x), -1 * (joint_y - midhip_y)

            transformed_coords[i] = (new_x, new_y)
        #     print(index_to_joint_map[i], transformed_coords[i])
        #
        # print('===================================================')
        return transformed_coords

    def _get_cartesian_joint_angles(self):
        """
        Calculates the relative joint angles between certain joints.
        Returns a dictionary which maps the joint-pair to the the angle of the vectors.
        """
        lookup = self.cartesian_keypoint_dict

        # Center
        neck_nose = self._get_relative_vector_angle(lookup['Neck'], lookup['Nose'])
        hip_neck = self._get_relative_vector_angle(lookup['MidHip'], lookup['Neck'])

        # Right Arm
        r_shoulder_elbow = self._get_relative_vector_angle(lookup['RShoulder'], lookup['RElbow'])
        r_elbow_wrist = self._get_relative_vector_angle(lookup['RElbow'], lookup['RWrist'])

        # Left Arm
        l_shoulder_elbow = self._get_relative_vector_angle(lookup['LShoulder'], lookup['LElbow'])
        l_elbow_wrist = self._get_relative_vector_angle(lookup['LElbow'], lookup['LWrist'])

        # Right Leg
        r_hip_knee = self._get_relative_vector_angle(lookup['RHip'], lookup['RKnee'])
        r_knee_ankle = self._get_relative_vector_angle(lookup['RKnee'], lookup['RAnkle'])

        # Left Leg
        l_hip_knee = self._get_relative_vector_angle(lookup['LHip'], lookup['LKnee'])
        l_knee_ankle = self._get_relative_vector_angle(lookup['LKnee'], lookup['LAnkle'])

        angles = {"NeckNose": neck_nose, "HipNeck": hip_neck,
                  "RShoulderElbow": r_shoulder_elbow, "RElbowWrist": r_elbow_wrist,
                  "LShoulderElbow": l_shoulder_elbow, "LElbowWrist": l_elbow_wrist,
                  "RHipKnee": r_hip_knee, "RKneeAnkle": r_knee_ankle,
                  "LHipKnee": l_hip_knee, "LKneeAnkle": l_knee_ankle
                  }

        return angles

    @staticmethod
    def _get_vector_angle(u, v):
        """"
        Gets the angle between the vector 'u' and the vector 'v', i.e. the absolute angle for which 'u' needs to rotate
        about the origin to align with 'v'.
        Returns the result in degrees in the range [0, 180].
        """
        cos_theta = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
        theta = np.arccos(np.clip(cos_theta, -1.0, 1.0))
        theta_deg = np.rad2deg(theta)

        return theta_deg

    @staticmethod
    def _get_relative_vector_angle(u, v):
        """
        Gets the angle between the vector 'u' and the vector 'v' with respect to the +x axis.
        Returns the result in degrees in the range [-180, 180].
        """
        difference = (v-u)
        difference /= np.linalg.norm(difference)

        x, y = np.clip(difference, -1.0, 1.0)[:2]
        theta = np.arctan2(y, x)
        theta_deg = np.rad2deg(theta)

        return theta_deg

    def _get_normalized_keypoints(self):

        normalized_keypoints = self.cartesian_keypoints.copy()
        normalized_keypoints[:, 0] -= min(normalized_keypoints[:, 0])
        normalized_keypoints[:, 0] /= (max(normalized_keypoints[:, 0]) - min(normalized_keypoints[:, 0]))

        normalized_keypoints[:, 1] -= min(normalized_keypoints[:, 1])
        normalized_keypoints[:, 1] /= (max(normalized_keypoints[:, 1]) - min(normalized_keypoints[:, 1]))

        return normalized_keypoints

        # Debug Stuff
        # from matplotlib import pyplot as plt
        # x, y = normalized_keypoints.T
        # plt.scatter(x, y)
        # plt.show()

        # box_width = max(self.cartesian_keypoints[:, 0]) - min(self.cartesian_keypoints[:, 0])
        # box_height = max(self.cartesian_keypoints[:, 1]) - min(self.cartesian_keypoints[:, 1])

        # tlx, tly = int(min(self.keypoints[:, 0])), int(min(self.keypoints[:, 1]) + box_height)
        # brx, bry = int(min(self.keypoints[:, 0]) + box_width), int(min(self.keypoints[:, 1]))
        #
        # import cv2
        # cv2.rectangle(self.image, (tlx, tly), (brx, bry), (255, 0, 0), 2)
        # cv2.imshow('', self.image)
        # cv2.waitKey()
        # pass


def get_pose_keypoint_errors(pose1, pose2, error_func=lambda x: x**2):
    """
    Calculates the error between the normalized keypoint locations between two poses.
    The error by default is the squared L2 distance.

    The result is returned in keypoint dictionary format.
    """

    pose1_coords_dict = pose1.cartesian_keypoint_dict
    pose2_coords_dict = pose2.cartesian_keypoint_dict

    if pose1_coords_dict.keys() != pose2_coords_dict.keys():
        raise ValueError("The two poses don't have the same keypoints.")

    error_dictionary = {}
    for (k1, v1), (k2, v2) in zip(pose1_coords_dict.items(), pose2_coords_dict.items()):
        if k1 != k2:
            raise ValueError("The two poses have mis-matched keypoint names.")

        l2_distance = np.linalg.norm(v1 - v2)
        error_dictionary[k1] = error_func(l2_distance)

    return error_dictionary
