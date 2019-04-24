# Quick Q (QuQ)

Quick Q (also known as QuQ) is a self-checkout solution for pre-packaged drinks in the SUTD Canteen. The project was done as part of the module: 10.009 Digital World. A demo video: `demo_video.mp4` can be found in this directory demonstrating the product functioning.

This work was done with the combined work of the following team:

- [Fasermaler](https://github.com/fasermaler)

- [oliviergoals](https://github.com/oliviergoals)
- [Etzernal](https://github.com/Etzernal)
- Emily
- Nigel

## Introduction

Quick Q was designed as a response to the inefficiency of the SUTD drinks canteen vendor. It was noticed that 30% of drinks store patrons are often turned away by the frequent long queues. 

Quick Q is a self-checkout solution for pre-packaged drinks using the following libraries:

- OpenCV Aruco Marker detection
- Kivy for front-end GUI
- Firebase-admin for database

Quick Q significantly reduces queue times as it requires no manpower and is able to scan multiple drinks simultaneously to allow for fast check-outs. Each sale is also recorded into an online Database, providing drinks store vendors with Data analytics needed to make smart business decisions.

Do note that the project's original name was cutQ - thus the references within the code base.

## How to Run

### To Run the Raspberry pi Code:

Assuming the appropriate dependencies are installed, simply VNC/SSH into the Raspberry Pi of your choice and navigate to the Quick Q directory. Then type `python3 main.py` to run the script. 

If using SSH, remember to run the command `export DISPLAY=:0` to ensure that the Kivy GUI will be displayed on the Raspberry Pi.

## Convenience Scripts

Under the `convenience scripts folder` there exists `updater.sh` and `setup.sh`. `setup.sh` will help in installing Quick-Q and all it's dependencies while `updater.sh` will update existing Quick-Q installs.

## Code Overview

The following is a brief overview of the code used in the project. QuQ runs on python3 though some modifications can be made if the user desires to run it in python 2.7.

### Raspberry Pi Code

The following is code that runs on the Raspberry Pi 3B+ (the main end-user experience)

### Dependencies

- OpenCV 3.3.0
- Picamera
- Firebase-admin SDK
- _thread (or thread library python 2.7)
- Kivy for python 3.7

#### Main

`main.py` is the main script that runs the entire code. It contains most of the Kivy screen classes and imports the `cutQ_vision_class` and `update` class (for firebase updating).

It also includes a `DEBUG` flag that can be set to `True` to allow for debug prints during code execution. 

**Firebase Update and OpenCV Vision Object Initialization**

```python
# Initialize firebase update and CV vision objects
update = update(cred, db)
vision = cutQ_vision_class(update.pull_drinkp())
```

This code initializes the updater object `update` with the credentials file `cred` and the database reference `db`. It also initializes the vision object `vision` with argument `update.pull_drinkp()` which is a subroutine under `update` that pulls the latest drinks price list from the firebase. 

**Credentials and Database reference Initialization**

`cred` and `db` are provided in the following lines of code:

```python
# firebase app initialization requirements
cred = credentials.Certificate("./credentials/canteen-1d-firebase-adminsdk-wibfq-547f9050df.json")
try:
    firebase_admin.delete_app(firebase_admin.get_app())
except:
    pass
firebase_admin.initialize_app(cred)
db = firestore.client()
```

- `cred` is the credentials certificate to access the firebase
- `try...except` loop is used to delete any prior instances of firebase admin applications
  - It works by passing the results of the`get_app` method to the `delete_app` method
- `initialize_app` is used to initialize a firebase app instance using the corresponding credentials
- `db` is the firebase database reference

**Threading of vision loop**

The following code starts the vision loop within a thread (so that is is able to run concurrently with the GUI):

```PYTHON
# Start the vision thread
_thread.start_new_thread(vision.start, ())
```

**get_drinks_dict function**

```python
def get_drinks_dict():

    drinksdict = vision.drink_dict # gets the drink dict from the vision class

```

This function is a wrapper for the `drink_dict` attribute (containing the active list of detected drinks from the `vision` object) that is called by the Kivy App when required.

#### Kivy Screens

The following are the various Kivy Screens as used by the GUI, they also include code logic within.

##### Start Screen

Start screen is the first screen, it uses the `startscreen.png` file under the `assets` folder. Start screen has the `change_to_confirm` function that updates the screen manager to change the active screen to the `confirm` screen

```python
# Kivy Start Screen Code
class StartScreen(Screen):

    def __init__(self, **kwargs):

        Screen.__init__(self, **kwargs)

        # Sets the layout
        self.layout = BoxLayout(orientation ='vertical')
        
        # Canopy Coffee Image
        i1 = Image(source = './assets/startscreen.PNG', size_hint= (1, 0.8))
        self.layout.add_widget(i1)
        
        # START Button
        b1 = Button(text ='START', font_size = 25, bold = True, size_hint = (1, 0.2), background_color = (0,0,1,1))
        b1.bind(on_press = self.change_to_confirm)
        self.layout.add_widget(b1)
        
        self.add_widget(self.layout)
    
    # Change to confirmation Screen after 'START' button pressed
    def change_to_confirm(self, value):
        
        self.manager.current = 'confirm'
```

##### Confirm Screen

Confirm screen is the confirmation screen that checks with the user is all their drinks have been placed into the scanning area. It includes the function `change_to_orders` which changes the screen to `orders` and sets the transition animation to a swipe `left`.

```python
# Class for the screen asking for user confirmation that they have placed all items
class ConfirmScreen(Screen):

    def __init__(self, **kwargs):

        Screen.__init__(self, **kwargs)

        # Layout
        self.layout = BoxLayout(orientation = 'vertical')
        
        # Ask if all orders have been placed Label
        l1 = Label(text = 'All orders placed?', font_size = 25, color = (0,0,0,1), size_hint = (1, 0.8), bold = True)
        self.layout.add_widget(l1)
        
        # Confirmation Button
        b1 = Button(text = 'Confirm', font_size = 25, size_hint = (1, 0.2), background_color = (0,0,1,1), bold = True)
        b1.bind(on_press = self.change_to_orders)
        self.layout.add_widget(b1)
        
        self.add_widget(self.layout)


    # Change to screen to display orders    
    def change_to_orders(self, value):

        self.manager.transition.direction = 'left'
        self.manager.current = 'orders'
```

##### Order Screen

Order screen is the most complex of the screens, it will display all the orders as detected by the `vision` class and asks the user to confirm the order.

```python
class OrderScreen(Screen):

    def __init__(self, **kwargs):

        Screen.__init__(self, **kwargs)
        self.layout = GridLayout(cols = 1)
        
        # Create a heading layout
        self.headinglayout = GridLayout(cols = 3, size_hint = (1, 0.1))


        # Headings (drink, qty, unit price)
        l1 = Label(text = 'Drink', font_size = 25, color = (1,0,0,1), bold = True)
        self.headinglayout.add_widget(l1)
        l2 = Label(text = 'Qty', font_size = 25, color = (1,0,0,1), bold = True)
        self.headinglayout.add_widget(l2)
        l3 = Label(text = 'Unit Price', font_size = 25, color = (1,0,0,1), bold = True)
        self.headinglayout.add_widget(l3)


        self.layout.add_widget(self.headinglayout)

        # Create an orderlayout
        self.orderlayout = GridLayout(cols=3, size_hint = (1, 0.4))
        
        # Add orderlayout to root layout
        self.layout.add_widget(self.orderlayout)
        
        # Create layout for total price
        self.pricelayout = GridLayout(cols= 2, size_hint = (1, 0.2))
        
        # Total price
        total_price = 0
        p1 = Label(text = 'Total:', font_size = 25, color =(0,0,0,1))
        self.pricelayout.add_widget(p1)
        self.p2 = Label(text = '${:.2f}'.format(total_price), font_size = 25, color = (0,0,0,1))
        self.pricelayout.add_widget(self.p2)
        
        # Add pricelayout to root layout
        self.layout.add_widget(self.pricelayout)
        
        # Ask if the order is correct Label
        l2 = Label(text = 'Is your order correct?', font_size = 25, color = (0,0,0,1), size_hint = (1, 0.1), bold = True)
        self.layout.add_widget(l2)
        
        # BUTTONS
        self.buttonlayout = GridLayout(cols = 2, size_hint = (1, 0.2))
        
        # YES button
        b1 = Button(text = 'Yes', font_size = 25, background_color = (0,1,0,1), bold = True)
        b1.bind(on_press = self.change_to_payment)
        self.buttonlayout.add_widget(b1)
        
        # NO button
        b2 = Button(text = 'No', font_size = 25, background_color = (1,0,0,1), bold = True)
        b2.bind(on_press = self.change_to_confirm)
        self.buttonlayout.add_widget(b2)
        self.layout.add_widget(self.buttonlayout)
        self.add_widget(self.layout)
```

Order screen has 3 functions:

- `change_to_payment` advances to the payment screen if the user confirms the order

- `change_to_confirm` returns to the confirmation screen if the user does not agree with the order tally

- `on_enter` on_enter is the function that starts every time the order screen is entered. Firstly, it will erase all prior drinks related widgets.

  ```python
  # Clears any previous price lists
  self.orderlayout.clear_widgets()
  ```

  It will attempt to call `get_drinks_dict` to obtain the drinks dictionary and create a list of drinks and their prices on screen via widget creation.

  ```python
  # gets the drinks dictionary from the vision class
          d = get_drinks_dict()
  
          for key in d:
              drink = Label(text = key, font_size = 25, color = (0,0,0,1))
              self.orderlayout.add_widget(drink)
              qty = Label (text = str(d[key][0]), font_size = 25, color = (0,0,0,1))
              self.orderlayout.add_widget(qty)
              price = Label (text = '${:.2f}'.format(d[key][1]), font_size = 25, color = (0,0,0,1))
              self.orderlayout.add_widget(price)
              total_price += d[key][0]*d[key][1]
  ```

  Finally, it will update the `total_price` displayed on screen.

  ```python
  #self.p2.text = '${:.2f}'.format(total_price)
  self.p2.text = '${:.2f}'.format(total_price)
  ```

  The `on_screen` Kivy method has a noticeable delay but this has not been resolved despite github issues raised.

##### Payment Screen

Finally, the payment screen is the screen that displays the payment QR code required for electronic payment. At the moment this is a static QR code from the image `emily_qrcode` under the `assets` folder. (Feel free to make a donation to this QR code :D )

The payment screen includes two buttons, `PAID` and `Quit`. `PAID` will call `change_to_start`.

`Quit` will quit the application. At any point, pressing `Esc` on a keyboard connected to the Rpi will also result in an exit.

```python
# Class for the payment screen
class PaymentScreen(Screen):

    def __init__(self, **kwargs):

        Screen.__init__(self, **kwargs)
        self.layout = BoxLayout(orientation = 'vertical')
        
        # default payment status
        self.payment = False
        
        # Scan to pay Label
        l1 = Label(text = 'Scan QR code to pay', font_size = 25, color = (0,0,0,1), size_hint = (1, 0.2), valign = 'bottom')
        self.layout.add_widget(l1)
        
        # QR code shown 
        self.qrlayout = BoxLayout(padding = [60, 0, 60, 80], size_hint = (1, 0.6))
        i1 = Image(source = './assets/emily_qrcode.jpg', allow_stretch = True)
        self.qrlayout.add_widget(i1)
        self.layout.add_widget(self.qrlayout)
        
        self.buttonlayout = BoxLayout(size_hint = (1, 0.2))
        
        # Press 'PAID' button after payment has been made
        b1 = Button(text = 'PAID', font_size = 25, bold = True, background_color = (0,0,1,1), size_hint = (0.7, 1))
        b1.bind(on_press = self.change_to_start)
        self.buttonlayout.add_widget(b1)
        
        # Quit App Button
        b2 = Button(text = 'Quit', font_size = 25, size_hint = (0.3, 1))
        b2.bind(on_press = self.quit_app)
        self.buttonlayout.add_widget(b2)
        
        self.layout.add_widget(self.buttonlayout)
        
        self.add_widget(self.layout)
```

The payment screen class includes `change_to_start` which changes the the screen to the start screen. It also result in the sale to be sent to the firebase `update` class and calls the `update_values` method. This will result in the database being updated with the sale.

```python
    # Goes back to start screen after payment has been made    
    def change_to_start(self, value):

        global drinks
        global DEBUG

        self.manager.current = 'start'
        self.payment = True # change payment status


        # Try Except encapsulation to ensure the program does not crash during internet outtage
        try:
            c_time = time.localtime()

            update.update_values(drinks, time.localtime(), True)
        except:
            print("Unable to upload to firebase")

        # Resets the drinks list
        drinks = []

        if DEBUG:
            print("drinks is")
            print(drinks)

        return self.payment

```

#### DrinksApp Class

The `DrinksApp` class builds all the screens into a singular app as per the Kivy Library.

```python
# Drinks App class from Kivy
class DrinksApp(App):

    # Build method build all widgets and screens

    def build(self):
        Window.clearcolor = (1,1,1,1) # changes background color to white

        # create Screen Manager
        sm = ScreenManager()
        
        # Initialise different screens
        ss = StartScreen(name = 'start')
        os = OrderScreen(name = 'orders')
        cs = ConfirmScreen(name='confirm')
        ps = PaymentScreen(name = 'payment')
        sm.add_widget(ss)
        sm.add_widget(cs)
        sm.add_widget(os)
        sm.add_widget(ps)
        
        return sm
```

#### Main Check

Finally, the following code runs if `main.py` is run as main:

```python
# Runs if main is run as main
if __name__ == '__main__':

    DrinksApp().run()
```

#### Vision Class

The vision class can be found in the `vision` folder. It contains many classes and the full documentation can be found in the markdown file `Vision Documentation.md`.

#### Firebase

##### Database Format

The Firebase database format is as follows:

Database is in the format below: 

- Collection
  - Document
    - Data Entry in the form of a dictionary

- Drink_day_count
  - Morning
    - drink name : count of drink purchased
  - Afternoon
    - drink name : count of drink purchased
  - Evening
    - drink name : count of drink purchased
- Drink_month_count
  - January
    - drink name : count of drink purchased
  - February 
    - drink name : count of drink purchased
  - March
    - drink name : count of drink purchased
  - April
    - drink name : count of drink purchased
  - May
    - drink name : count of drink purchased
  - June
    - drink name : count of drink purchased
  - July
    - drink name : count of drink purchased
  - August
    - drink name : count of drink purchased
  - September
    - drink name : count of drink purchased
  - October
    - drink name : count of drink purchased
  - November
    - drink name : count of drink purchased
  - December
    - drink name : count of drink purchased
- Drink_week_count
  - Monday
    - drink name : count of drink purchased
  - Tuesday
    - drink name : count of drink purchased
  - Wednesday
    - drink name : count of drink purchased
  - Thursday
    - drink name : count of drink purchased
  - Friday
    - drink name : count of drink purchased
  - Saturday
    - drink name : count of drink purchased
- Drink_year_count
  - 2018
    - drink name : count of drink purchased
  - 2019
    - drink name : count of drink purchased
- Today
  - Today
    - sale number for day : [list of drinks purchased for this sale]
- Drink_prices
  - Drink_prices
    - aruco marker number: [drink name, unit price of drink]

The firebase folder contains the following files:

- `firebase_grabber.py`: A firebase script that grabs the drinks prices. This script's functionality has now been superseded by the more complete `firestore_update_and_pull.py`
- `firestore_initialise.py`: This is to be run once when setting up a fresh database as it will create the collections and documents.
- `firestore_initial_drink.py`: This is demo code used to initialize the list of drinks.  It can also be modified to initialize the drinks list of the user's choice
- `firestore_update_and_pull.py`: Actual runtime firebase code that is being accessed. It's contents will be discussed in the next section

#### Firestore Update and Pull

`firestore_update_and_pull.py` contains only the `update` class and contains the runtime firebase code.

**init**

`__init__` is the initialization for `update`. It takes in `cred` and `db` which are the firebase credentials and database references respectively.

First it attempts to delete any prior firebase app instance.

```python
try:
    firebase_admin.delete_app(firebase_admin.get_app())
except:
    pass
```

Next it sets all the relevant internal DOCREFs

```python
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
        
```

**Update Main**

`update_main` takes in the following arguments:

- `cv_drink_lst`: list of drinks from the vision class
- `time_factor`: time (in hours) of the sale
- `index` firebase index

It is not directly called by `main.py`, instead it is the subroutine used by `update_values` when attempting to update the various firebase attributes.

It references the relevant document and appends the drinks count accordingly.

```python
def update_main(self,cv_drink_lst,time_factor,index):
        doc = self.col_ref_lst[index].document(time_factor).get()
        for drink,count in doc.to_dict().items():
            previous_count = count
            for k in cv_drink_lst:
                if drink == k:
                    previous_count += 1
                    self.col_ref_lst[index].document(time_factor).update({drink:previous_count})
    
```

**Update values**

`update_values` takes in the following arguments:

- `cv_drink_lst`: list of drinks from the vision class
- `current_time`:current time of sale
- `payment` : boolean value indicative of a successful sale

First, the subroutine checks if `payment` is `True`:

```python
if payment == True:
```

Next it only gets the hour of the day from the provided time. This allows it to categorize if the sale took place in the Morning, Afternoon or Evening and update the relevant firebase fields. It does this by calling the `update_main` subroutine.

```python
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
```

Next, the firebase will append the quantity of each drink sold to the cumulative totals of day, month and year accordingly (for backend data analytics).

```python
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

```

Finally, it updates the single sales for the day using `doc_today` as reference.

```python
#to record single sales
doc_today = self.doc_ref_today.get()
count = str(len(doc_today.to_dict()) + 1)
self.doc_ref_today.update({count:cv_drink_lst})
```

**Pull Drinkp**

`pull_drinkp` is the function called at the start of `main` and fed into the `vision` object initialization. It pulls the pre-defined drinks list in the following format: `{aruco ID: ('drink_name', price)}`.

```python
def pull_drinkp(self):
    self.doc = self.doc_ref_drink_prices.get()
    return self.doc.to_dict(
```

**Restart**

Restart allows the `day` database to be reset by setting it to be an empty dictionary.

```python
def restart(self):
    self.doc_ref_today.set({})
```



