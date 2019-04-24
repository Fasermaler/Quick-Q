
import argparse
'''
Custom argument parsing wrapper

the defaults can be defined upon initialization

Else the defaults are:

video path: None
Imshow: True
price csv path: 'prices.csv'
'''


class arg_parser:

	def __init__(self, default_video=None, default_imshow=True, default_prices='prices.csv'):

		# starts the parser object
		self.parser = argparse.ArgumentParser(description='Detect drinks in video stream')
		# Argument for video path
		self.parser.add_argument("-v", "--video", default =default_video, required=False,
								help="path to input video file")
		# Argument for showing video feed
		self.parser.add_argument("-i", "--imshow", default=default_imshow, required=False,
								help="enables imshow mode")
		# Argument for location of price csv file
		self.parser.add_argument("-p", "--prices", default=default_prices, required=False,
								help="path to price file")

		# Initialize variables
		self.video_path = None
		self.imshow = None
		self.price_path = None

	# parse the arguments accordingly
	def parse_arguments(self):

		args = vars(self.parser.parse_args())

		# assigns the arguments to the attributes
		self.video_path = args["video"]
		self.imshow = args["imshow"]
		self.price_path = args["prices"]


	# Th call magic subroutine is to parse arguments
	def __call__(self):

		self.parse_arguments()


## Test Code ##

args = arg_parser()
args.parse_arguments()

print("video path: " + str(args.video_path))
print("imshow: " + str(args.imshow))
print("price path: " + str(args.price_path))

