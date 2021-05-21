from tkinter import *
from tkinter.constants import BOTTOM, LEFT, RIGHT
import requests
from datetime import datetime
from mail_sender import send_email
import logging
import os
logging.basicConfig(filename="logfile.log", level=logging.INFO)

subscribed = 1
labels = []
cycles = 0
symbols = ['SC','BTC']
prices = [0.02, 42000]
api_twelvedata = 'https://api.twelvedata.com/time_series?symbol={}/USD&interval=1min&outputsize=3&format=JSON&dp=5&timezone=Europe/Moscow&apikey=f7e12a1a4dd34faca920cdff2c088e2b'

def sub_button():
    global button_sub_enabled, lable_sub_enabled, button_sub_disabled, lable_sub_disabled
    if subscribed == 1:
        button_sub_enabled = Button(width=25, font=('Arial,25'), fg='red',text='Disable Subscription', command=lambda: disable_subscription())
        button_sub_enabled.pack(side = BOTTOM)
        lable_sub_enabled = Label(root_window, font=('Arial,20'), text='email subcribtion enabled')
        lable_sub_enabled.pack(side = BOTTOM)

    else:
        button_sub_disabled = Button(width=25, font=('Arial,25'), fg='green',text='Enable Subscription', command=lambda: enable_subscription())
        button_sub_disabled.pack(side = BOTTOM)
        lable_sub_disabled= Label(root_window, font=('Arial,20'), text='email subcribtion disabled')
        lable_sub_disabled.pack(side = BOTTOM)

def enable_subscription():
    global subscribed
    button_sub_disabled.destroy()
    lable_sub_disabled.destroy()
    subscribed = 1
    sub_button()

def disable_subscription():
    global subscribed
    button_sub_enabled.destroy()
    lable_sub_enabled.destroy()
    subscribed = 0
    sub_button()

def update_prices():
    try:
        global cycles
        counter = 0
        correct_SMMTP = True
        for symbol in symbols:
            response = requests.get(api_twelvedata.format(symbol))
            date_time = response.json()['values'][0]['datetime']
            cost = response.json()['values'][0]['close']
            if symbol == 'SC':
                CCoin = 'Siacoin'
            else:
                CCoin = 'Bitcoin'
            if float(cost) > prices[counter] and correct_SMMTP == True:
                correct_SMMTP = send_email(CCoin + ' cost is ' + cost + ' at ' + date_time + ' (more than ' + f'{prices[counter]}' + ')')
                # messagebox.showinfo ("Price reached your limit!", CCoin + ' cost is ' + cost + ' at ' + date_time + ' (more than ' + f'{prices[counter]}' + ')')
            labels[counter].configure(text=CCoin + f' ({symbol})' ' value is ' + cost + ' at ' + date_time)
            counter +=1
        logging.info(datetime.today().strftime('%D - %H:%M:%S') + ' Update')
        root_window.after(60000, update_prices)
    except:
        logging.error(datetime.today().strftime('%D - %H:%M:%S') + ' Error: cant reach remote API')
        messagebox.showinfo ("Error", "Can't reach remote API to update prices")
        root_window.after(5000, update_prices)        
    
def create_lables(symbols):
    try:
        for symbol in symbols:
            response = requests.get(api_twelvedata.format(symbol))
            date_time = response.json()['values'][0]['datetime']
            cost = response.json()['values'][0]['close']
            if symbol == 'SC':
                CCoin = 'Siacoin'
            else:
                CCoin = 'Bitcoin'
            lable = Label(root_window, font=('Arial,25'), text=CCoin + f' ({symbol})' ' value is ' + cost + ' at ' + date_time)
            lable.pack()
            labels.append(lable)
    except:
        logging.error(datetime.today().strftime('%D - %H:%M:%S') + ' Error: cant reach remote API')
        messagebox.showinfo ("Error", "Can't reach remote server")
        os._exit(os.EX_OK)

root_window = Tk()
root_window.title("Cryptocurrency to USD")
root_window.geometry('500x125')

create_lables(symbols)
sub_button()

root_window.after(5000, update_prices)
logging.info(datetime.today().strftime('%D - %H:%M:%S') + ' Start')
root_window.mainloop()
