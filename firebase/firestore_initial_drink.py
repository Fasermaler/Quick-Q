#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 14:14:40 2019

@author: Olivier
"""
#this class will be used to initialise the drink price and list of drinks into firebase accordingly to each collection and doc
# a methods that will curated are as follows: 

from firebase1D_initialise import important_details
from firebase1D_initialise import important_lsts

# All of the details were taken from the initialising file. 

#In important details, the following were returned (1) db (2) creds (3) doc_ref for prices and today and (4) column referneces for the day,week,month,year  
db, creds, doc_ref_drink_prices,doc_ref_today,col_ref_day,col_ref_week,col_ref_month,col_ref_year = important_details()

# In important lsts, the different lists were return. eg week_lst would be like ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
time_seg,week_lst,month_lst,year_lst,lst_main = important_lsts()

class Drink:
    #(1)
    # Input drink_dict is a dict in the following format ({"drink_name":price float}). 
    # The input drink_dict in this case should be the pre-disposed/standard menu of prepackaged drinks offered by the drink store
    def __init__(self,drink_dict):
        # Drink_price_dict attribute is initialised as this dict will be used for the drink_price document in the firebase
        self.drink_price_dict = drink_dict
        # Drink_dict is a new attribute that is initialised to get the output ({"drink_name":0})
        # This is for all the documents within the column references for day, week, month, year
        # The value of dictionary is the count of the drinks that have been bought
        self.drink_dict = {}
        for i in drink_dict.keys():
            self.drink_dict.update({i:0})
        
    #(2)
    # col_ref_lst is a list the list that includes all column references that should be updated
    # In most cases, the col_ref_lst will consist of col_ref_day, col_ref_week, col_ref_month and col_ref_year
    # This class is to add self.drink_dict to each of the documents for all of the columns in the col_ref_lst 
    def add_drink(self,col_ref_lst):
         for i in range(len(col_ref_lst)): #to make sure all collections are updates
            for doc in col_ref_lst[i].get(): #retrieve doc.id and update the data in the doc for each respective collection
                col_ref_lst[i].document(doc.id).set(self.drink_dict)
    #(3)
    # This is to store the values in the price document in the format of {index:[drink_name,price]}
    # the index will be assigned to the aruco marker.
    def set_price(self):
        x = 0
        for drink, price in self.drink_price_dict.items():    
            x += 1
            doc_ref_drink_prices.update({str(x):[drink,price]})
            
        


newdrink = Drink({"longan":1.3,
                  "water_chestnut":1.3,
                  "bandung":1.3,"lime_juice":1.3,
                  "pineapple_juice":1.3,
                  
                 "red_bean":1.3,"sour_plum":1.3,"green_bean":1.3,
                 "chrysanthemum":1.3, "barley":1.3,"can_drink": 1.5,
                 "coconut_water":2.6, "bottle_cheap":1.8,"bottle_ex":1.9,
                 "milk":2.6,"soy_milk":1.5})
newdrink.add_drink(lst_main)
newdrink.set_price()







    