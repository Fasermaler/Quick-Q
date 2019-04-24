#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:48:22 2019

@author: Olivier
"""
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
#from Drink_class import Class


#Sets up the json
cred = credentials.Certificate("canteen-1d-firebase-adminsdk-wibfq-547f9050df.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


#Prepare the different collections and documents. There will be 5 collections.
#1. Drink price 
#2. Date - To track EACH drink sale
#3. drink_day- splits a day into 3 documents: Morning, afternoon, evening, trak drink sales with each time segment
#4. drink_week - splits a week into 6 documents: Mon-Sat, track drink sale for each day
#5. drink_month - splits a month into 12 documents: Jan-Dec, track drink sale for each month
#6. drink_year - track drink sales for each year

#Setting up collection 1. Collection: "Drink_prices" Document: drinkname Info: price of the drink
doc_ref_drink_prices = db.collection(u'Drink_prices').document(u'Drink_prices')
doc_ref_drink_prices.set({})

#Setting up collection 2. Collection: "Today" Document: sale Info: dictionary of drinks sold
doc_ref_today = db.collection(u'Today').document(u'Today')
doc_ref_today.set({})


#Setting up collection 3. Collection: "Drink_day_count" Document: time segment Info: Dict of total drinks sold
##Morning ranges 7am-11am Afternoon 11am-5pm Dinner 5pm - 7pm
time_seg = [u'Morning', u'Afternoon',u'Evening']
col_ref_day = db.collection(u'Drink_day_count')
for i in time_seg:
    doc_ref_day = col_ref_day.document(i)
    doc_ref_day.set({})

#Setting up collection 4. Collection:"Drink_week_count" DOcument: week info: Dict of total drinks sold
week_lst = [u'Monday',u'Tuesday',u'Wednesday',u'Thursday',u'Friday',u'Saturday']
col_ref_week = db.collection(u'Drink_week_count')
for i in week_lst:
    doc_ref_week = col_ref_week.document(i)
    doc_ref_week.set({})

#Setting up collection 5. Collection:"Drink_month_count" Document: Month info: Diction of total drink sold
month_lst = [u'January', u'February', u'March', u'April',
                  u'May', u'June', u'July', u'August',
                  u'September', u'October', u'Novemeber', u'December']
col_ref_month = db.collection(u'Drink_month_count')
for i in month_lst:
    doc_ref_week = col_ref_month.document(i)
    doc_ref_week.set({})

#Setting up collection 6. Collection:"Drink_year_count" Document: Year info: Dictonary of total drinks sold

year_lst = [u'2019',u'2018']
col_ref_year = db.collection(u'Drinks_year_count')
for i in year_lst:
    doc_ref_year = col_ref_year.document(i)
    doc_ref_year.set({})

lst_main = [col_ref_day , col_ref_week, col_ref_month, col_ref_year]

def important_details():
    return db, cred,doc_ref_drink_prices,doc_ref_today,col_ref_day,col_ref_week,col_ref_month,col_ref_year

def important_lsts():
    return time_seg,week_lst,month_lst,year_lst,lst_main

#print(new_drink.time)
#new_drink2.add_price(1.20)
print("you are re-running this code")
#new_drink.add_price(1.00)
#new_drink.add_counter(lst_time,1.00)
