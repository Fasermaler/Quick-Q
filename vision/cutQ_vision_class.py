'''
This script identifies drinks marked with aruco markers and calculates their total cost

User variables are to be set in the 'config' file, not within the program

Author: Fasermaler 
March 2019
'''

import cv2
import numpy as np

import cv2.aruco as aruco

import csv

# Fire base imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Time import
import time

# import thread to do multithreading
import _thread

# import argparse to take in system arguments
import argparse

# Custom imports
from aruco_detector import aruco_detector
from picam_class import pi_cam
from video_reader import video_reader
from arg_parser import arg_parser
from price_calculator import price_calculator
from csv_reader import csv_reader
from pull_prices import pull_prices


class cutQ_vision_class:

	def __init__(self, drinkp):
		# Parses the console arguments
		self.args = arg_parser()#default_imshow=False)
		self.args.parse_arguments()

		# start the csv reader 
		self.csv_read = csv_reader()

		# Get the config file parameters
		self.config_read = csv_reader()
		print(self.config_read.get_config())

		# If no video path was specified, use the pi camera as live feed
		if self.args.video_path == None:

			self.stream = pi_cam(self.config_read.pi_height, self.config_read.pi_width, self.config_read.pi_fps)

		else:
			self.stream = video_reader(str(self.args.video_path))

		# Start the aruco detector
		self.aruco_detector = aruco_detector()

		# Start the price calculator
		print(drinkp)
		self.prices = price_calculator(drinkp)


		self.drinks = None
		self.price = None
		self.drink_dict = {}
		

				# Starts the thread to get frames
		_thread.start_new_thread(self.stream.get_frame_continuous, ())

	def start(self):

		reset_count = 0
		
		# encapsulate the whole program in a try except in case of termination
		# try:
		while True:
			try:
				# get the frame from the stream
				frame = self.stream.frame
				#self.drink_dict = {}




				# get the coordinates and ids of the aruco markers
				#try:

				corners, ids = self.aruco_detector.return_aruco_ids(frame)
				
				if ids != None:
					self.drink_dict = {}

					# calculate the prices
					
					self.prices.calculate_price(ids)
					


					# If the user opts to show the cv2 screen

					if self.args.imshow:
						print(self.prices.drinks_list)
						self.aruco_detector.draw_markers(frame, corners, ids, text=self.prices.drinks_list, text_flag=True)
						
						

					print(self.prices.total_price)
					for i in range(len(self.drinks)):
						if self.drinks[i] not in self.drink_dict.keys():
							if self.drinks[i] != None:
								self.drink_dict[self.drinks[i]] = (1, self.prices.pure_prices[self.drinks[i]])
						else:
							self.drink_dict[self.drinks[i]] = (self.drink_dict[self.drinks[i]][0] + 1 , self.prices.pure_prices[self.drinks[i]])
					print(self.drink_dict)
					#reset_count = 0
				else:
					if reset_count == 10:
						self.drink_dict = {}
						reset_count = 0
					else:
						reset_count += 1
				cv2.imshow('Stream', frame)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break

				# updates the main class attributes
				self.price = self.prices.total_price
				self.drinks = self.prices.drinks_list



					
				# except:
				# 	#print("skipped a frame")
				# 	pass
			except Exception as e: print(e)

		# except:

		# 	# terminate the stream
		# 	self.stream.terminate = True

		cv2.destroyAllWindows()

## Test Code ##

#vision = cutQ_vision_class()

# Do note that this has no termination condition at the moment
#vision.start()




