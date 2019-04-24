# -*- coding: utf-8 -*-
'''
  firestore_device_class
  Initialise a device that captures an image and sends it to a random request
  queue shard at a user-defined interval, with additional parameters.
  Copyright 2018 Fasermaler, methylDragon
  All rights reserved.
'''

from google.cloud import firestore
from google.auth.transport.requests import AuthorizedSession

try:
    from methyl_auth_utils.google import CloudPasswordLogin
except:
    from lib.methyl_auth_utils.google import CloudPasswordLogin

import cv2 as cv, cv2
import json
import configparser
import random
import numpy as np
import time
import socket

# Initializes the device class
class PeopleCounterDevice:
    def __init__(self, config_file_path=None):
        self.parse_config_file(config_file_path)
        self.populate_config_parameters()

        self.first_request = True

        # Init client credentials
        self.client_credentials = CloudPasswordLogin(self.login_email, self.login_password, self.api_key)

        self.init_opencv()

        self.ret = None
        self.frame = None
        self.frame_gray = None
        self.prev_frame = np.zeros((self.camera_height, self.camera_width), np.uint8)
        self.prev_frame_gray = np.zeros((self.camera_height, self.camera_width), np.uint8)
        self.movement_detected = False

        for i in range(self.times_to_rotate_by_90_degrees):
            self.prev_frame = np.rot90(self.prev_frame)
            self.prev_frame_gray = np.rot90(self.prev_frame_gray)

        self.latest_image = np.zeros((self.camera_height, self.camera_width), np.uint8)

        # Init URLs
        self.url_base = 'https://firebasestorage.googleapis.com/v0/b/'

        # inference_image_api_url: REST API endpoint for inference image
        # inference_image_url: Binary image content for inference image
        self.inference_image_api_url = (self.url_base
                                       + self.database_id
                                       + ".appspot.com/o/"
                                       + str(self.client_credentials.uid)
                                       + "%2Finference_"
                                       + self.device_id
                                       + ".jpg")

        self.inference_image_url = self.inference_image_api_url + "?alt=media"

        # recorded_image_api_url: REST API for recorded latest image
        # recorded_image_url: Binary image content for recorded latest image
        self.recorded_image_api_url = (self.url_base
                                      + self.database_id
                                      + ".appspot.com/o/"
                                      + str(self.client_credentials.uid)
                                      + "%2Frecorded_"
                                      + self.device_id
                                      + ".jpg")

        self.recorded_image_url = self.recorded_image_api_url + "?alt=media"

        # Init database and storage clients
        # For Cloud Firestore
        self.db = firestore.Client(project=self.database_id, credentials=self.client_credentials)
        self.device_doc = self.db.collection('DEVICES').document(self.device_id)

        # For Cloud Storage
        self.authed_session = AuthorizedSession(self.client_credentials)

        # Get Request Queue IDs
        self.request_queues = None
        self.request_queues_list = []

        self.fetch_request_queues()

        # Initialise the device on Firestore
        try: # Tries to update the device
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
            except:
                ip = None

            self.device_doc.update({'device_name': self.device_name,
                                    'recorded_image_url': self.recorded_image_url,
                                    'inference_image_url': self.inference_image_url,
                                    'client_name': self.client_name,
                                    'device_ip': ip})

            s.close()

        except: # If the device document does not exist then create the device document
            try:
                self.device_doc.set({'device_name': self.device_name,
                                     'last_count_date': None,
                                     'last_count_utc_time': None,
                                     'last_count_unix_time': None,
                                     'people_count': None,
                                     'recorded_image_url': self.recorded_image_url,
                                     'inference_image_url': self.inference_image_url,
                                     'client_name': self.client_name})
            except:
                print("UNABLE TO INITIALISE DEVICE ON DATABASE")

    def parse_config_file(self, config_file_path): # Subroutine that parses the config file
        self.user_config = configparser.ConfigParser()
        self.user_config.read(config_file_path)

    def populate_config_parameters(self): # Subroutine that calls the config file
        # Get Device Info
        self.client_name = self.user_config['DEVICE_INFO']['CLIENT_NAME']
        self.device_name = self.user_config['DEVICE_INFO']['DEVICE_NAME'] # Physical Location of device

        # Get Login Info
        self.login_email = self.user_config['LOGIN_INFO']['LOGIN_EMAIL']
        self.login_password = self.user_config['LOGIN_INFO']['LOGIN_PASSWORD']

        self.api_key = self.user_config['LOGIN_INFO']['API_KEY']
        self.database_id = self.user_config['LOGIN_INFO']['DATABASE_ID']
        self.device_id = self.user_config['LOGIN_INFO']['DEVICE_ID']

        # Create mutable variables
        self.record_latest_image = []
        self.point_threshold = []
        self.scaling_percentage = []
        self.request_frequency = []
        self.motion_sensitivity_threshold = []
        self.camera_height = []
        self.camera_width = []
        self.camera_number = []
        self.times_to_rotate_by_90_degrees = []
        self.bypass_motion_detection = []

        # Define parameter constraints
        parameter_dict_list = [{'parameter': self.record_latest_image, 'id': 'RECORD_LATEST_IMAGE',
                                'lower_limit': None, 'upper_limit': None, 'default': False},

                               {'parameter': self.point_threshold, 'id': 'POINT_THRESHOLD',
                                'lower_limit': 1, 'upper_limit': 10, 'default': 5},

                               {'parameter': self.scaling_percentage, 'id': 'SCALING_PERCENTAGE',
                                'lower_limit': 5, 'upper_limit': 150, 'default': 100},

                               {'parameter': self.request_frequency, 'id': 'REQUEST_FREQUENCY',
                                'lower_limit': 30, 'upper_limit': 84600, 'default': 300},

                               {'parameter': self.motion_sensitivity_threshold, 'id': 'MOTION_SENSITIVITY_THRESHOLD',
                                'lower_limit': 0.001, 'upper_limit': 0.8, 'default': 0.0025},

                               {'parameter': self.camera_height, 'id': 'CAMERA_HEIGHT',
                                'lower_limit': 1, 'upper_limit': 1080, 'default': 540},

                               {'parameter': self.camera_width, 'id': 'CAMERA_WIDTH',
                                'lower_limit': 1, 'upper_limit': 1920, 'default': 960},

                               {'parameter': self.camera_number, 'id': 'CAMERA_NUMBER',
                                'lower_limit': 0, 'upper_limit': None, 'default': 0},

                               {'parameter': self.times_to_rotate_by_90_degrees, 'id': 'TIMES_TO_ROTATE_BY_90_DEGREES',
                                'lower_limit': 0, 'upper_limit': 3, 'default': 0},

                               {'parameter': self.bypass_motion_detection, 'id': 'BYPASS_MOTION_DETECTION',
                                'lower_limit': None, 'upper_limit': None, 'default': False}]

        # Populate mutable variables and apply constraints
        for parameter_dict in parameter_dict_list:
            try:
                identifier = parameter_dict['id']
                lower_limit = parameter_dict['lower_limit']
                upper_limit = parameter_dict['upper_limit']
                default = parameter_dict['default']

                user_input = self.user_config['PARAMETERS'][identifier]

                if type(default) == int:
                    try:
                        user_input = int(user_input)
                    except:
                        pass

                if type(default) == float:
                    try:
                        user_input = float(user_input)
                    except:
                        pass

                if type(default) == bool:
                    if user_input in ['TRUE', 'True', 'true', True]:
                        user_input = True
                    else:
                        user_input = False
                    continue

                elif type(user_input) != type(default):
                    print("[WARN]:", identifier, "is of the wrong type. Please check config. Defaulting to", default)
                    user_input = default
                    continue
                else:
                    if not lower_limit is None:
                        if user_input < lower_limit:
                            user_input = lower_limit
                            print("[WARN]:", identifier, "is too low. Please check config. Limiting to", lower_limit)

                    if not upper_limit is None:
                        if user_input > upper_limit:
                            user_input = upper_limit
                            print("[WARN]:", identifier, "is too high. Please check config. Limiting to", upper_limit)

            except:
                print("[WARN]:", identifier, "is invalid. Please check config. Defaulting to", default)
                user_input = default

            finally:
                parameter_dict['parameter'].append(user_input)

        # Bake in mutable variables
        self.record_latest_image = self.record_latest_image[0]
        self.point_threshold = int(self.point_threshold[0])
        self.scaling_percentage = int(self.scaling_percentage[0])
        self.request_frequency = int(self.request_frequency[0])
        self.motion_sensitivity_threshold = self.motion_sensitivity_threshold[0]
        self.camera_height = int(self.camera_height[0])
        self.camera_width = int(self.camera_width[0])
        self.camera_number = int(self.camera_number[0])
        self.times_to_rotate_by_90_degrees = int(self.times_to_rotate_by_90_degrees[0])
        self.bypass_motion_detection = self.bypass_motion_detection[0]

    def fetch_request_queues(self):
        '''Gets the request_queues IDs'''
        self.request_queues_list = []
        self.request_queues = self.db.collection('REQUEST_QUEUES').get()

        for queue in self.request_queues:
            if queue.id.startswith('REQUEST_QUEUE'): #Filters for only REQUEST_SHARD collections
                self.request_queues_list.append(queue.id)

    # Method to capture and save a frame from the camera
    def cap_and_save_frame(self):
        if self.camera_avail:

            for _ in range(4):
                self.ret, self.frame = self.cap.read()

            self.ret, self.frame = self.cap.read()

            for i in range(self.times_to_rotate_by_90_degrees):
                self.frame = np.rot90(self.frame)

            self.frame_gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)

            if self.ret:
                self.movement_detected = self.detect_movement(self.prev_frame_gray, self.frame_gray, self.motion_sensitivity_threshold)

                if self.movement_detected or self.bypass_motion_detection:
                    self.prev_frame = self.frame
                    self.prev_frame_gray = self.frame_gray

                    if self.record_latest_image or self.first_request:
                        self.latest_image = self.frame
                    else:
                        self.latest_image = self.frame_gray

                    return True

            else:
                self.camera_avail = False
                self.movement_detected = False

                try:
                    self.init_opencv()
                except:
                    pass

                print('[WARN]: Unable to get image from camera')

        else:
            try:
                self.init_opencv()
            except:
                pass

        return False

    def detect_movement(self, prev_frame, frame, motion_sensitivity_threshold):
        frame_delta = cv.absdiff(prev_frame, frame)
        thresh = cv.threshold(frame_delta, 25, 255, cv.THRESH_BINARY)[1]
        thresh = cv.erode(thresh, None, iterations = 2)
        thresh = cv.dilate(thresh, None, iterations = 10)

        contour_thresh = frame_delta.size * motion_sensitivity_threshold

        #print("THRESHOLD IS", contour_thresh, "OF", frame_delta.size)
        cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[1]

        for c in cnts:
            # Save the coordinates of all found contours
            (x, y, w, h) = cv.boundingRect(c)

            # If the contour is too small, ignore it, otherwise, there's movement
            if cv.contourArea(c) > contour_thresh:
                print("MOTION DETECTED")
                return True

        print("NO MOTION DETECTED")
        return False

    def send_request(self, time):
        """Send a request to a random request queue shard."""
        if self.movement_detected or self.bypass_motion_detection:
            for i in range(2): # Just try twice
                try:
                    target_request_queue = random.choice(self.request_queues_list)
                    print("\nTARGET:", target_request_queue)

                    request_header = str(int(time))

                    if self.first_request:
                        request_string = (str(self.client_credentials.uid) + "^^"
                                          + str(self.device_id) + "^^"
                                          + str("True") + "^^"
                                          + str(self.point_threshold) + "^^"
                                          + str(self.scaling_percentage))

                        self.first_request = False

                    else:
                        request_string = (str(self.client_credentials.uid) + "^^"
                                          + str(self.device_id) + "^^"
                                          + str(self.record_latest_image) + "^^"
                                          + str(self.point_threshold) + "^^"
                                          + str(self.scaling_percentage))


                    request_dict = {request_header: request_string, 'latest_request_device_id': self.device_id}

                    print(request_dict)

                    self.db.collection('REQUEST_QUEUES').document(target_request_queue).update(request_dict)

                    print('\n[INFO] Sent request to', target_request_queue)

                    self.movement_detected = False

                    break

                except Exception as e:
                    try:
                        print("\n[ERROR] Unable to send request to", str(target_request_queue))
                    except:
                        print("\n[ERROR] Unable to send request! Could not assign target request queue.")
                    print("Error:", e)
                    print("Aborting")
                    self.fetch_request_queues()
                    time.sleep(600)
        else:
            print('[WARN]: Request was not sent')

    def init_opencv(self):
        try:
            try:
                cv.VideoCapture(self.camera_number).release()
            except:
                pass

            self.cap = cv.VideoCapture(self.camera_number) # creates the capture object

            if self.cap.read()[0] == False:
                for i in range(-1, 10):
                    self.cap = cv.VideoCapture(i)

                    if self.cap.read()[0]:
                        print("CAMERA ACTIVATED, INDEX:", i)
                        break
            else:
                print("CAMERA ACTIVATED, INDEX:", 0)

            self.cap.set(3, self.camera_width)
            self.cap.set(4, self.camera_height)

            # Just in case the camera can't be set to the desired resolution
            self.camera_width = int(self.cap.get(3))
            self.camera_height = int(self.cap.get(4))

            self.cap.set(3, self.camera_width)
            self.cap.set(4, self.camera_height)

            if self.cap.isOpened():
                print("CAMERA READY")
                self.camera_avail = True # Sets the availability of the camera to True

                self.ret, self.frame = self.cap.read() # Reads from the capture object

                for i in range(self.times_to_rotate_by_90_degrees):
                    self.frame = np.rot90(self.frame)

                if self.ret:
                    self.frame_gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
                else:
                    self.camera_avail = False

            else:
                self.camera_avail = False

        except Exception as e:
            print('[ERROR]: Unable to detect a camera')
            print(e)

            self.camera_avail = False #  Sets the availability of the camera to False

        cv.destroyAllWindows() # Destroy CV windows if any

    def upload_file_and_send_request(self):
        try:
            capture_time = int(time.time())
            capture_bytes = cv2.imencode('.jpg', self.latest_image)[1]

            try:
                response = self.authed_session.post(self.inference_image_api_url, data=bytes(capture_bytes))
            except Exception as e:
                print(e)
                pass

            print(response.json())

            self.send_request(capture_time)
            print("\nIMAGE UPLOADED. REQUEST SENT:", capture_time)

        except Exception as e:
            print('\n[ERROR]: Image capture Failed. Request aborted.')
            print("Error:", e)

if __name__ == "__main__":
    while True:
        try:
            try:
                device = PeopleCounterDevice('/boot/config.ini')
            except:
                device = PeopleCounterDevice('config.ini')

            last_send_time = 0

            while True:
                if (int(time.time() - last_send_time) > int(device.request_frequency)):
                    last_send_time = int(time.time())

                    saved_frame_status = device.cap_and_save_frame()

                    if device.movement_detected and saved_frame_status:
                        device.upload_file_and_send_request()
                    else:
                        pass

        except Exception as e:
            print("\n[ERROR]: Restarting Script")
            device.cap.release()
            print("Error:", e)
            time.sleep(1)

            #break

    device.cap.release()