#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 01:32:02 2019

@author: Olivier
"""

# To avoid re-initialising, firebase_admin is reimported and reinitialised

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time

# cred = credentials.Certificate("canteen-1d-firebase-adminsdk-wibfq-547f9050df.json")
# firebase_admin.initialize_app(cred)


# db = firestore.client()

# This class will be used to update the values of the firebase according to the list that is outputed from the CV class

class update:
    
    # This is to initialise firebase & ensure no other code is running on the firebase 
    def __init__(self,cred,db):
        
        try:
            firebase_admin.delete_app(firebase_admin.get_app())
        except:
            pass
        
        
        # All the of the attributes of the firebased are initialised accordingly
        # detials such as time_seg, week_lst , month_lst and year_list is also inputed
        
        self.cred = cred
        firebase_admin.initialize_app(self.cred)
        self.db = db
        self.doc_ref_drink_prices = self.db.collection(u'Drink_prices').document(u'Drink_prices')
        self.doc_ref_today = self.db.collection(u'Today').document(u'Today')
        self.col_ref_day = self.db.collection(u'Drink_day_count')
        self.col_ref_day = self.db.collection(u'Drink_day_count')
        self.col_ref_week = self.db.collection(u'Drink_week_count')
        self.col_ref_month = self.db.collection(u'Drink_month_count')
        self.col_ref_year = self.db.collection(u'Drink_year_count')
        self.time_seg = [u'Morning', u'Afternoon',u'Evening']
        self.week_lst = [u'Monday',u'Tuesday',u'Wednesday',u'Thursday',u'Friday',u'Saturday']
        self.month_lst = [u'January', u'February', u'March', u'April',
                  u'May', u'June', u'July', u'August',
                  u'September', u'October', u'Novemeber', u'December']
        self.year_lst = [u'2019',u'2018']
        self.col_ref_lst = [self.col_ref_day , self.col_ref_week, self.col_ref_month, self.col_ref_year]
        
        
    '''
    This function is to update the doc of the different column references namely self.col_ref_lst according to the index
    this function wil be called within the below functions 
    This can be done for the col_ref_lst as they have similar formatting
    Index argument refers to which col_ref to be called 
    Time factor argument refers to which document ie for col_ref_week, time factor could be "Wednesday"
    '''
    def update_main(self,cv_drink_lst,time_factor,index):
        doc = self.col_ref_lst[index].document(time_factor).get()
        for drink,count in doc.to_dict().items():
            previous_count = count
            for k in cv_drink_lst:
                if drink == k:
                    previous_count += 1
                    self.col_ref_lst[index].document(time_factor).update({drink:previous_count})
    
    
    # This function is to update the columns for entries in the cv_drink_lst 
    # Payment arugment is just to see if payment has been done, if payment is not done the cv_drink_lst output would not be updated on the firebase
    def update_values(self,cv_drink_lst,current_time, payment):
        if payment == True:
            
            #for time seg which is col_ref_lst[0]
            hour = int(time.strftime('%H',current_time)) 
            if hour >= 7 and hour <= 11:
                self.update_main(cv_drink_lst,u'Morning',0)
            elif hour > 11 and hour <= 16:
                self.update_main(cv_drink_lst,u'Afternoon',0)
            elif hour > 16 and hour <= 20:
                self.update_main(cv_drink_lst,u'Evening',0)
            else:
                pass
                                
            #for week which is col_ref_lst[1]
            day = time.strftime('%A',current_time)
            for i in self.week_lst:
                if i == day:
                    self.update_main(cv_drink_lst,i,1)

            #for month which is col_ref_lst[2]
            month = time.strftime('%B',current_time)
            for k in self.month_lst:
                if k == month:
                    self.update_main(cv_drink_lst,k,2)
                        
            # for year which is col_ref_lst[3]
            year = time.strftime('%Y',current_time)
            for j in self.year_lst:
                if j == year:
                    self.update_main(cv_drink_lst,j,3)

            
            #to record single sales
            doc_today = self.doc_ref_today.get()
            count = str(len(doc_today.to_dict()) + 1)
            self.doc_ref_today.update({count:cv_drink_lst})
        
            
        cv_drink_lst = []
        return True   
        
    def pull_drinkp(self):
        self.doc = self.doc_ref_drink_prices.get()
        return self.doc.to_dict()     
        
    #at the end of everyday, the today doc reference should restart
    def restart(self):
        self.doc_ref_today.set({})
    
    
# THE FOLLOWING CODE WAS USED AS REFERENCE FOR THE CLIENT INTERFACE TO ADD NEW DRINK AND UPDATE PRICES IN THE FIREBASE
# =============================================================================
#     def price(self, drink_name, new_price):
#         doc = self.doc_ref_drink_prices.get()
#         
#         for num, lst in doc.to_dict().items():
#             if drink_name in lst:
#                 self.doc_ref_drink_prices.update({num:[drink_name,new_price]})
# 
# #        else:
# #            print("there is no such drink")
#     
#     def new_drink(self, drink_name, new_price):
#         if drink_name not in self.col_ref_day.document(u'Morning').get().to_dict():
#             for i in range(len(self.col_ref_lst)): #to make sure all collections are updates
#                 for doc in self.col_ref_lst[i].get(): #retrieve doc.id and update the data in the doc for each respective collection
#                     self.col_ref_lst[i].document(doc.id).update({drink_name:0})
#         
#             doc = self.doc_ref_drink_prices.get()
#             lst = doc.to_dict().values()
#             marker_num = str(len(lst) + 1)
#             self.doc_ref_drink_prices.update({marker_num:[drink_name,new_price]})
#         else:
#             print("You already have a drink")
# =============================================================================
            

### DEFUNCT CODE
   
# class Pull: 
#     def __init__(self,cred,db):
#         try:
#             firebase_admin.delete_app(firebase_admin.get_app())
#         except:
#             pass
        
#         self.cred = cred
#         firebase_admin.initialize_app(self.cred)
#         self.db = db
#         self.doc_ref_drink_prices = self.db.collection(u'Drink_prices').document(u'Drink_prices')
#         self.doc_ref_today = self.db.collection(u'Today').document(u'Today')
#         self.col_ref_day = self.db.collection(u'Drink_day_count')
#         self.col_ref_day = self.db.collection(u'Drink_day_count')
#         self.col_ref_week = self.db.collection(u'Drink_week_count')
#         self.col_ref_month = self.db.collection(u'Drink_month_count')
#         self.col_ref_year = self.db.collection(u'Drinks_year_count')
#         self.time_seg = [u'Morning', u'Afternoon',u'Evening']
#         self.week_lst = [u'Monday',u'Tuesday',u'Wednesday',u'Thursday',u'Friday',u'Saturday']
#         self.month_lst = [u'January', u'February', u'March', u'April',
#                   u'May', u'June', u'July', u'August',
#                   u'September', u'October', u'Novemeber', u'December']
#         self.year_lst = [u'2019',u'2018']
#         self.col_ref_lst = [self.col_ref_day , self.col_ref_week, self.col_ref_month, self.col_ref_year]
        
    
#     def pull_drinkp(self):
#         final_dic = {}
#         doc = self.doc_ref_drink_prices.get()
#         for key, value in doc.to_dict().items():
#             final_dic.update({key:(value[0],value[1])})
#         return final_dic
        

#current_time = time.localtime()
#cv_drink_lst = ['bandung','luo_han_guo','bandung','ice_lemon_tea']
#payment = True
#transaction = Update(cred,db)
#transaction.update_values(cv_drink_lst, current_time,payment)
#transaction.restart()
#cv_drink_lst = ['bandung','milk','sour_plum','soy_milk']
#transaction.update_values(cv_drink_lst, current_time,payment)
#cv_drink_lst = ['pineapple_juice','milk','sour_plum','soy_milk']
#transaction.update_values(cv_drink_lst, current_time,payment)
#transaction.new_drink("check", 0.1)









