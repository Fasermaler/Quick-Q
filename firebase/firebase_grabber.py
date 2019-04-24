import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time


		
class pull_prices: 

    def __init__(self, cred):
		# Kill any prior firebase app instance
        try:
            firebase_admin.delete_app(firebase_admin.get_app())
        except:
            pass

		# Get credentials and initialize new firebase app instance
        self.cred = cred
        firebase_admin.initialize_app(self.cred)

        self.db = firestore.client()
        self.doc_ref_drink_prices = self.db.collection(u'Drink_prices').document(u'Drink_prices')
        self.doc_ref_today = self.db.collection(u'Today').document(u'Today')
        self.col_ref_day = self.db.collection(u'Drink_day_count')
        self.col_ref_week = self.db.collection(u'Drink_week_count')
        self.col_ref_month = self.db.collection(u'Drink_month_count')
        self.col_ref_year = self.db.collection(u'Drinks_year_count')

        self.col_ref_lst = [self.col_ref_day , self.col_ref_week, self.col_ref_month, self.col_ref_year]

        self.time_seg = [u'Morning', u'Afternoon',u'Evening']
        self.week_lst = [u'Monday',u'Tuesday',u'Wednesday',u'Thursday',u'Friday',u'Saturday']
        self.month_lst = [u'January', u'February', u'March', u'April',
                  u'May', u'June', u'July', u'August',
                  u'September', u'October', u'Novemeber', u'December']

        self.year_lst = [u'2019',u'2018']

    def pull_drinkp(self):
        self.doc = self.doc_ref_drink_prices.get()
        return self.doc.to_dict()


#### TEST CODE ####
cred = credentials.Certificate("canteen-1d-firebase-adminsdk-wibfq-547f9050df.json")

test = pull_prices(cred)
print(test.pull_drinkp())