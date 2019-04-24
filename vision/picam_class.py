from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image
import cv2

import time

# importing thread for multithreading testing
import _thread

class pi_cam:

    # sets the initialization variables for rpi cam
    def __init__(self, h=240, w=432, fps=32):

        self.camera = PiCamera()

        # the pi camera library will automatically change any unallowable resolutioj
        self.camera.resolution = (w, h)
        
        # checks to ensure that the user sets a reasonable fps count
        if fps < 14:

            fps = 14

        elif fps > 60:

            fps = 60

        self.camera.framerate = fps
        self.rawCapture = PiRGBArray(self.camera, size=(w,h))

        # current active frame
        self.frame = None

        # Termination flag
        self.terminate = False

        time.sleep(0.1)


    def get_single_frame(self):

        for cap in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):

            self.frame = cap.array

            self.rawCapture.truncate(0)

            break


    # Flushes the frame buffer before calling the actual frame
    # Take note that excessive flush_count will adversely affect framerate
    def flush_buffer_single(self, flush_count=5):

        for cap in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):

            # ensures a reasonable flush_count has been set

            if flush_count < 1:

                flush_count = 1

            elif flush_count > 10:

                flush_count = 10

            for i in range(flush_count):
                self.frame = cap.array

            self.rawCapture.truncate(0)

            break


    # For multithreading
    # Flushing buffer option is available, set 1 to not flush at all
    def get_frame_continuous(self, flush_count=5):
        
        # ensures a reasonable flush_count has been set

        if flush_count < 1:

            flush_count = 1

        elif flush_count > 10:

            flush_count = 10
        
        # checks for the termination flag, important for multithreading
        while not self.terminate:
            for cap in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
                for i in range(flush_count):
                    self.frame = cap.array
                #print("I have a frame")

                    

                #cv2.imshow('frame', self.frame)

                self.rawCapture.truncate(0)
                #self.rawCapture.seek(0)
                #key = cv2.waitKey(10) & 0xFF

    # the call magic method only calls the get frame continuous as part of multithreading
    def __call__(self, flush_count=5):

        self.get_frame_continuous(flush_count)


# ## Test Code ##

# test_cam = pi_cam()
# thread.start_new_thread(test_cam.get_frame_continuous, ())

# while True:
#     try:
#         cv2.imshow('frame', test_cam.frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     except:
#         pass

# cv2.destroyAllWindows()

# test_cam = pi_cam()
# test_cam()


