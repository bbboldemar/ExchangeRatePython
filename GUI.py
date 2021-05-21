from tkinter import Button, Tk, Label, messagebox
from tkinter.constants import BOTTOM
import requests
from datetime import datetime
from mail_sender import send_email
from status_check import subscription_checker, not_first_launch_check
import logging
import os
import sys
logging.basicConfig(filename="logfile.log", level=logging.INFO)


labels = []
cycles = 0
symbols = ['SC','BTC']
prices = [0.02, 36000]
api_twelvedata = 'https://api.twelvedata.com/time_series?symbol={}/USD&interval=1min&outputsize=3&format=JSON&dp=5&timezone=Europe/Moscow&apikey=f7e12a1a4dd34faca920cdff2c088e2b'

    
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
        create_lables(symbols)
        # os._exit(os.EX_OK)

def sub_button():
    global button_sub_enabled, lable_sub_enabled, button_sub_disabled, lable_sub_disabled, root_window
    if subscription_checker() == 1:
        button_sub_enabled = Button(root_window, width=25, font=('Arial,25'),text='Disable Subscription', command=lambda: subscription_control('disable'))
        button_sub_enabled.pack(side = BOTTOM)
        lable_sub_enabled = Label(root_window, font=('Arial,20'), fg='green', text='email subcribtion enabled')
        lable_sub_enabled.pack(side = BOTTOM)

    else:
        button_sub_disabled = Button(root_window, width=25, font=('Arial,25'),text='Enable Subscription', command=lambda: subscription_control('enable'))
        button_sub_disabled.pack(side = BOTTOM)
        lable_sub_disabled= Label(root_window, font=('Arial,20'), fg='red', text='email subcribtion disabled')
        lable_sub_disabled.pack(side = BOTTOM)

def subscription_control(choise):
    global button_sub_disabled
    global lable_sub_disabled
    global lable_sub_enabled
    global button_sub_enabled
    if choise == 'enable':
        with open("exchanger_settings",'r') as f:
            get_all = f.readlines()
        with open("exchanger_settings",'w') as f:
            for i,line in enumerate(get_all,1):
                if i == 1:
                    f.writelines('subscription_enabled\n')
                else:
                    f.writelines(line)
        button_sub_disabled.destroy()
        lable_sub_disabled.destroy()
        sub_button()
    elif choise == 'disable':
        with open("exchanger_settings",'r') as f:
            get_all = f.readlines()
        with open("exchanger_settings",'w') as f:
            for i,line in enumerate(get_all,1):
                if i == 1:
                    f.writelines('subscription_disabled\n')
                else:
                    f.writelines(line)   
        button_sub_enabled.destroy()
        lable_sub_enabled.destroy()
        sub_button() 

def update_prices():
    try:
        global cycles
        counter = 0
        for symbol in symbols:
            response = requests.get(api_twelvedata.format(symbol))
            date_time = response.json()['values'][0]['datetime']
            cost = response.json()['values'][0]['close']
            if symbol == 'SC':
                CCoin = 'Siacoin'
            else:
                CCoin = 'Bitcoin'
            if float(cost) > prices[counter] and subscription_checker() == 1:
                send_email(CCoin + ' cost is ' + cost + ' at ' + date_time + ' (more than ' + f'{prices[counter]}' + ')')
                # messagebox.showinfo ("Price reached your limit!", CCoin + ' cost is ' + cost + ' at ' + date_time + ' (more than ' + f'{prices[counter]}' + ')')
            labels[counter].configure(text=CCoin + f' ({symbol})' ' value is ' + cost + ' at ' + date_time)
            counter +=1
        logging.info(datetime.today().strftime('%D - %H:%M:%S') + ' Update')
        root_window.after(60000, update_prices)
    except:
        logging.error(datetime.today().strftime('%D - %H:%M:%S') + ' Error: cant reach remote API')
        messagebox.showinfo ("Error", "Can't reach remote API to update prices")
        root_window.after(5000, update_prices)        


global root_window
not_first_launch_check()
root_window = Tk()
root_window.title("Cryptocurrency to USD")
root_window.geometry('500x125')  
create_lables(symbols)
sub_button()

root_window.after(5000, update_prices)
logging.info(datetime.today().strftime('%D - %H:%M:%S') + ' Start')
root_window.mainloop()
