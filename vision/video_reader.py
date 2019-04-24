
import cv2
import numpy as np
import cv2
import numpy as np


# import thread for testing
import _thread

class video_reader:

	def __init__(self, video=None):

		# Active Frame variable
		self.frame = None

		# Capture object
		self.cap = None

		# Termination flag (used for multithreading)
		self.terminate = False

		# video path
		self.video = video


	def read_video(self, video):

		# Assign capture object to video
		self.cap = cv2.VideoCapture(video)

		# Check if the capture object can be opened
		if (self.cap.isOpened()== False): 

  			print("[Error] Unable to open video stream or file")
  			
  			return None

		# Check for termination flag
		while not terminate:

			# Check if the video stream ended
			while(cap.isOpened()):

			  	# Capture frame-by-frame
			  	ret, frame = self.cap.read()
			  	if ret == True:
			 
				    self.frame = frame
			 
				    if cv2.waitKey(1) & 0xFF == ord('q'):
				        break


	# calls the read video method as part of multithreading
	def __call__(self):

		self.read_video(self.video)



# ## Test Code
# test_vid = video_reader()
# thread.start_new_thread(test_vid, ('test.mp4'))

# while True:

#     cv2.imshow('frame', test_vid.frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cv2.destroyAllWindows()


