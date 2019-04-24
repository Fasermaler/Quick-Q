# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 01:31:32 2019

@author: Em
"""
import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button 
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.app import App
from kivy.core.window import Window


# this is just a function that wraps the drinksdict information so that it can be called by kivy
def get_drinks_dict():
    drinksdict = vision.drink_dict # gets the drink dict from the vision class
    print("drinksdict got: ")
    print(drinksdict)
    return drinksdict
# dictionary returned
# key is drink name, value is a tuple of qty and unit price

class StartScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = BoxLayout(orientation ='vertical')
        
        # Canopy Coffee Image
        i1 = Image(source = 'startscreen.PNG', size_hint= (1, 0.8))
        self.layout.add_widget(i1)
        
        # START Button
        b1 = Button(text ='START', font_size = 25, bold = True, size_hint = (1, 0.2), background_color = (0,0,1,1))
        b1.bind(on_press = self.change_to_confirm)
        self.layout.add_widget(b1)
        
        self.add_widget(self.layout)
    
    # Change to confirmation Screen after 'START' button pressed
    def change_to_confirm(self, value):
        self.manager.current = 'confirm'

class ConfirmScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = BoxLayout(orientation = 'vertical')
        
        # Ask if all orders have been placed Label
        l1 = Label(text = 'All orders placed?', font_size = 25, color = (0,0,0,1), size_hint = (1, 0.8), bold = True)
        self.layout.add_widget(l1)
        
        # Confirmation Button
        b1 = Button(text = 'Confirm', font_size = 25, size_hint = (1, 0.2), background_color = (0,0,1,1), bold = True)
        b1.bind(on_press = self.change_to_orders(order_screen=os))
        self.layout.add_widget(b1)
        
        self.add_widget(self.layout)
     
    # After 'Confirm' button pressed, starts scanning drinks
    # Change to screen to display orders    
    def change_to_orders(self, value, order_screen=None):
        self.manager.transition.direction = 'left'
        self.manager.current = 'orders'

        # Drinks ordered
        total_price = 0
        drinksdict = vision.drink_dict
        for key in drinksdict:
            drink = Label(text = key, font_size = 25, color = (0,0,0,1))
            order_screen.orderlayout.add_widget(drink)
            qty = Label (text = str(d[key][0]), font_size = 25, color = (0,0,0,1))
            order_screen.orderlayout.add_widget(qty)
            price = Label (text = '${:.2f}'.format(d[key][1]), font_size = 25, color = (0,0,0,1))
            order_screen.orderlayout.add_widget(price)
            total_price += d[key][0]*d[key][1]

        p2= Label(text = '${:.2f}'.format("HAHA GAY"), font_size = 25, color = (0,0,0,1))
        order_screen.pricelayout.add_widget(p2)
        
        
class OrderScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = GridLayout(cols = 1)
        
        # Create an orderlayout
        self.orderlayout = GridLayout(cols=3, size_hint = (1, 0.5))
        
        # Headings (drink, qty, unit price)
        l1 = Label(text = 'Drink', font_size = 25, color = (1,0,0,1), bold = True)
        self.orderlayout.add_widget(l1)
        l2 = Label(text = 'Qty', font_size = 25, color = (1,0,0,1), bold = True)
        self.orderlayout.add_widget(l2)
        l3 = Label(text = 'Unit Price', font_size = 25, color = (1,0,0,1), bold = True)
        self.orderlayout.add_widget(l3)
        

        
        
        # Add orderlayout to root layout
        self.layout.add_widget(self.orderlayout)
        
        # Create layout for total price
        self.pricelayout = GridLayout(cols= 2, size_hint = (1, 0.2))
        
        # Total price
        p1 = Label(text = 'Total:', font_size = 25, color =(0,0,0,1))
        self.pricelayout.add_widget(p1)
        p2= Label(text = '${:.2f}'.format(total_price), font_size = 25, color = (0,0,0,1))
        self.pricelayout.add_widget(p2)
        
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
    
    # Change to payment screen if 'YES' button pressed
    def change_to_payment(self, value):
        self.manager.current = 'payment'
    
    # Goes back to confirmation screen and rescans drinks if 'NO' button pressed    
    def change_to_confirm(self, value):
        self.manager.transition.direction = 'right'
        self.manager.current = 'confirm'

        
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
        i1 = Image(source = 'emily_qrcode.jpg', allow_stretch = True)
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
        

    
    # Goes back to start screen after payment has been made    
    def change_to_start(self, value):
        global paid
        self.manager.current = 'start'
        self.payment = True # change payment status
        paid = True
        return self.payment
    
    # Quits the app
    def quit_app(self, value):
        App.get_running_app().stop()
        
        

class DrinksApp(App):

    def build(self):
        Window.clearcolor = (1,1,1,1) # changes background color to white

        # create Screen Manager
        sm = ScreenManager()
        
        # Initialise different screens
        ss = StartScreen(name = 'start')
        os = OrderScreen(name = 'orders')
        cs = ConfirmScreen(name='confirm', order_screen=os)
        ps = PaymentScreen(name = 'payment')
        sm.add_widget(ss)
        sm.add_widget(cs)
        sm.add_widget(os)
        sm.add_widget(ps)
        
        return sm


if __name__ == '__main__':
    DrinksApp().run()