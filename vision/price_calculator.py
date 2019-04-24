'''
This class calculates the total price of the drinks

Author: Fasermaler 
March 2019
'''

class price_calculator:

	# initialize with the price list
	def __init__(self, price_list):

		self.set_price_list(price_list)
		self.drinks_list = []
		self.total_price = 0.0
		self.old_ids = None

	# subroutine to set the price list
	def set_price_list(self, price_list):

		self.price_list = price_list
		self.pure_prices = {}

		for i in price_list.values():
			self.pure_prices[i[0]] = i[1]

		print(self.pure_prices)


	# calculates the total price and return a list of drinks in id order
	# returns a list of drinks and the total price
	def calculate_price(self, ids):

		# reset the drinks list and total price
		self.drinks_list = []
		self.total_price = 0.0
		self.old_ids = ids
		#print(ids)

		for i in range(len(ids)):
			# get the ID
			id_1 = ids[i][0]
			#print(id_1)
			try:
				drink = self.price_list[str(id_1)][0]
				self.total_price += self.price_list[str(id_1)][1]
				self.drinks_list.append(drink)
			except:
				self.drinks_list.append(None)

		# round the price
		self.total_price = round(self.total_price, 2)

	# adds more items to the drinks list and total price 
	# also returns the new id list with the new ids added
	def add_item(self, ids):

		for i in range(len(ids)):
			# get the ID
			id_1 = ids[i]
			drink = self.price_list[str(id_1)][0]
			self.total_price += self.price_list[str(id_1)][1]
			self.drinks_list.append(drink)

		# round the price
		self.total_price = round(self.total_price, 2)
		# Extend the ID list
		self.old_ids.extend(ids)

	# reset the prices, drinks list and ids
	def reset_all(self):

		self.drinks_list = []
		self.total_price = 0.0
		self.old_ids = None	

## test code ##
# Define the price list
# prices = price_calculator({'66': ('bandung', 4.4), '69': ('lemon tea', 5.5)})
# prices.calculate_price([66,66,69,69,69,66])
# print("Drinks list: " + str(prices.drinks_list))
# print("Total Price: " + str(prices.total_price))

# # Add some drinks
# print("Adding some items")
# prices.add_item([66,69])
# print("Drinks list: " + str(prices.drinks_list))
# print("Total Price: " + str(prices.total_price))
# print("Total IDS: " + str(prices.old_ids))

# # Reset all
# print("Resetting All")
# prices.reset_all()
# print("Drinks list: " + str(prices.drinks_list))
# print("Total Price: " + str(prices.total_price))
# print("Total IDS: " + str(prices.old_ids))