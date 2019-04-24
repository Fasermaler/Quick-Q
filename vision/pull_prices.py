import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time

# cred = credentials.Certificate("canteen-1d-firebase-adminsdk-wibfq-547f9050df.json")
# firebase_admin.initialize_app(cred)

class pull_prices: 

    def __init__(self,cred,db):
        try:
            firebase_admin.delete_app(firebase_admin.get_app())
        except:
            pass
        
        self.cred = cred
        firebase_admin.initialize_app(self.cred)
        self.db = db
        self.doc_ref_drink_prices = self.db.collection(u'Drink_prices').document(u'Drink_prices')
        self.doc_ref_today = self.db.collection(u'Today').document(u'Today')
        self.col_ref_day = self.db.collection(u'Drink_day_count')
        self.col_ref_day = self.db.collection(u'Drink_day_count')
        self.col_ref_week = self.db.collection(u'Drink_week_count')
        self.col_ref_month = self.db.collection(u'Drink_month_count')
        self.col_ref_year = self.db.collection(u'Drinks_year_count')
        self.time_seg = [u'Morning', u'Afternoon',u'Evening']
        self.week_lst = [u'Monday',u'Tuesday',u'Wednesday',u'Thursday',u'Friday',u'Saturday']
        self.month_lst = [u'January', u'February', u'March', u'April',
                  u'May', u'June', u'July', u'August',
                  u'September', u'October', u'Novemeber', u'December']
        self.year_lst = [u'2019',u'2018']
        self.col_ref_lst = [self.col_ref_day , self.col_ref_week, self.col_ref_month, self.col_ref_year]
        
    
    def pull_drinkp(self):
        final_dic = {}
        doc = self.doc_ref_drink_prices.get()
        for key, value in doc.to_dict().items():
            final_dic.update({key:(value[0],value[1])})
        return final_dic




# ## TEST CODE ##
# cred = credentials.Certificate("canteen-1d-firebase-adminsdk-wibfq-547f9050df.json")
# db = firestore.client()
# pull = pull_prices(cred, db)
# print(pull.pull_drinkp())