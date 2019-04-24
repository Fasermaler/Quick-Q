'''
This is the csv class that allows for csv reading functionality
The main function of this class is to read the csv file that contain
the prices of the drinks. By default the csv file should be prices.csv

The formatting of the csv should be:
id,name,price
WITHOUT SPACES AFTER THE COMMA

The output of this class will be a dictionary in the format:
{id: (name, price)}

'''


import csv



class csv_reader:

	def __init__(self):
		
		# Initialize price dict
		self.prices_ls = {}

		# Initialize config dict
		self.config_ls = {}

		csv.register_dialect('prices',
							delimiter = ',',
							skipinitialspace=False)

		csv.register_dialect('config',
							delimiter = ' ',
							skipinitialspace=False)

	
	# Gets the prices from the price csv
	def get_prices(self, file='prices.csv'):
		
		with open(file, mode='r') as csv_file:
			
			reader = csv.DictReader(csv_file, dialect='prices')
			line_count = 0
			
			for row in reader:

				if line_count == 0:
					
					line_count += 1
				
				self.prices_ls[row["id"]] = (row["name"],float(row["price"]))

	


	def print_prices(self):
		
		print(self.prices_ls)


	# Gets the configuration params from the config csv
	def get_config(self, file='config'):

		with open(file, mode='r') as cfg_file:
			
			reader = csv.DictReader(filter(lambda row: row[0]!='#', cfg_file), dialect='config')
			line_count = 0

			for row in reader:

				if line_count == 0:
					line_count += 1
				self.config_ls[row["param"]] = (row["value"])

		# load the config params into variables
		self.pi_height = int(self.config_ls["pi_cam_height"])
		self.pi_width = int(self.config_ls["pi_cam_width"])
		self.pi_fps = int(self.config_ls["pi_cam_fps"])
				
			


# ### TEST CODE ###
# print('getting price values')
# csv_read = csv_reader()

# csv_read.get_prices('prices.csv')

# csv_read.print_prices()


# print('getting config values')
# csv_read.get_config()

# print(csv_read.config_ls)
# print(csv_read.pi_height)
