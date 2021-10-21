from tkinter import Label, Button, Tk, Entry, messagebox
from tkinter.constants import BOTTOM, LEFT, RIGHT
from datetime import datetime
import webbrowser
import logging

import requests

from API import api_twelvedata, load_data_from_API
from mail_sender import send_email
from settings_checker import (
    subscription_checker,
    subscription_switcher, 
    settings_data_changer, 
    target_price_checker, 
    price_history_update
)

labels = []
symbols = ['SC','BTC']
logging.basicConfig(
    filename="logfile.log", level=logging.INFO
)


def create_lables(symbols):
    
    try:
        data_from_API = load_data_from_API()
        for symbol in symbols:
            currency_base = data_from_API[0]
            date_time = data_from_API[1]
            cost = data_from_API[2]
            price_history_update(currency_base, date_time, cost)
            lable = Label(
                root_window, 
                font=('Arial,25'), 
                text=currency_base + f' ({symbol})' ' value is ' 
                + cost + ' at ' + date_time
            )
            lable.pack()
            labels.append(lable)
    except:
        logging.error(
            datetime.today().strftime('%D - %H:%M:%S') 
            + ' Error: cant reach remote API'
        )
        messagebox.showinfo (
            "Error", "Can't reach remote server"
        )
        create_lables(symbols)


def not_first_launch_check():
    try:
        subscription_checker()
        return True
    except:
        global first_launch_window
        first_launch_window = Tk()
        first_launch_window.title("First launch setup")
        first_launch_window.geometry('500x90')
        lable_sub_enabled = Label(
            first_launch_window, 
            font=('Arial,25'), 
            text='Start tracking prices via email subscription?'
        )
        lable_sub_enabled.pack()     
        button_sub_enabled = Button(
            first_launch_window, 
            width=15, font=('Arial,25'), 
            fg='red',text='No', 
            command=lambda: first_launch_window_answer('No')
        )
        button_sub_enabled.pack(side = LEFT,padx = 20)
        button_sub_disabled = Button(
            first_launch_window, 
            width=15, 
            font=('Arial,25'), 
            fg='green',
            text='Yes', 
            command=lambda: first_launch_window_answer('Yes')
        )
        button_sub_disabled.pack(side = RIGHT,padx = 20)
        f = open("exchanger_settings", "w")
        f.write('subscription_disabled\nNone\nNone\nNone\nNone\n')
        f.close()
        f = open("price_history", "w")
        f.close()
        logging.info(
            datetime.today().strftime('%D - %H:%M:%S') 
            + ' First launch'
        )  
        first_launch_window.mainloop()


def first_launch_window_answer(choise):
    if choise == 'Yes':
        first_launch_window.destroy()
        subscription_settings_window()          
    else:        
        logging.info(
            datetime.today().strftime('%D - %H:%M:%S') 
            + ' Email subscription disabled'
        )   
        messagebox.showinfo (
            "Email subscription disabled", 
            "You can enable email subscription later"
        ) 
        first_launch_window.destroy()       


def update_prices():
    success = True
    subrscription_status = subscription_checker()
    logging.info(
        datetime.today().strftime('%D - %H:%M:%S') + ' Updating...'
    )
    if subrscription_status == True:
        try:
            prices = target_price_checker()
        except:
            logging.error(
                datetime.today().strftime('%D - %H:%M:%S') 
                + ' Invalid target price format'
            )
            button_sub_enabled.destroy(), lable_sub_enabled.destroy()
            subscribsion_settings_opener('enable')
            messagebox.showinfo (
                "Subscription Error", "Invalid target price format"
            ) 
            subrscription_status = False

    try:
        counter = 0
        for symbol in symbols:
            response = requests.get(api_twelvedata.format(symbol))
            currency_base = response.json()['meta']['currency_base']
            date_time = response.json()['values'][0]['datetime']
            cost = response.json()['values'][0]['close']
            price_history_update(currency_base, date_time, cost)
            if subrscription_status == True and float(cost) > prices[counter]:
                success = send_email(
                    currency_base + ' cost is ' 
                    + cost + ' at ' + date_time 
                    + ' (more than ' + f'{prices[counter]}' + ')'
                )
            labels[counter].configure(text=currency_base 
            + f' ({symbol})' ' value is ' + cost + ' at ' + date_time
            )
            counter += 1
        if success == False:
            logging.error(
                datetime.today().strftime('%D - %H:%M:%S') 
                + ' Invalid email address or password'
            )
            button_sub_enabled.destroy(), lable_sub_enabled.destroy()
            subscribsion_settings_opener('enable')            
            messagebox.showinfo (
                "Subscription Error", "Invalid email address or password"
            )
        logging.info(
            datetime.today().strftime('%D - %H:%M:%S') + ' Successful update!'
        )
    except:
        logging.error(
            datetime.today().strftime('%D - %H:%M:%S') 
            + ' Error: cant reach remote API'
        )
        messagebox.showinfo (
            "Error", "Can't reach remote API to update prices"
        )
    root_window.after(60000, update_prices)


def sub_button(choise):
    global root_window
    global button_sub_disabled, lable_sub_disabled
    global button_sub_enabled, lable_sub_enabled
    if choise == True:
        button_sub_enabled = Button(
            root_window, 
            width=25, 
            font='Arial,25', 
            text='Disable Subscription', 
            command=lambda: subscribsion_settings_opener('disable')
        )
        button_sub_enabled.pack(side = BOTTOM)
        lable_sub_enabled = Label(  
            root_window, 
            font=('Arial,20'), 
            fg='green', 
            text='email subcribtion enabled'
        )
        lable_sub_enabled.pack(side = BOTTOM)
        try:
            button_sub_disabled.destroy(), lable_sub_disabled.destroy()
        except Exception: 
            pass
    else:
        button_sub_disabled = Button(   
            root_window, 
            width=25, 
            font='Arial,25', 
            text='Enable Subscription', 
            command=lambda: subscribsion_settings_opener('enable')
        )
        button_sub_disabled.pack(side = BOTTOM)
        lable_sub_disabled= Label(  
            root_window, 
            font=('Arial,20'), 
            fg='red', 
            text='email subcribtion disabled'
        )
        lable_sub_disabled.pack(side = BOTTOM)
        try:
            button_sub_enabled.destroy(), lable_sub_enabled.destroy()   
        except Exception: 
            pass  


def subscribsion_settings_opener(choise):
    subscription_switcher('disable')
    
    if choise == 'disable':
        logging.info(
            datetime.today().strftime('%D - %H:%M:%S') 
            + ' Email subscription disabled'
        )
        sub_button(False)
    else:         
        root_window.withdraw()
        subscription_settings_window()


def subscription_settings_window():
    global root_window, subscription_window
    global entry_address, entry_password, entry_SC_min, entry_BC_min
    subscription_window = Tk()
    subscription_window.title("Settings")
    subscription_window.geometry('560x180')

    discard_button = Button(
        subscription_window, 
        width=18, fg='red', 
        font='Arial,25', 
        text='Disable Subscription', 
        command=lambda: discard_changes()
    )
    discard_button.place(relx=0.02, rely=0.8)
    
    apply_changes_button = Button(  
        subscription_window, 
        width=18, 
        fg='green', 
        font='Arial,25', 
        text='Apply Changes', 
        command=lambda: apply_changes(
            entry_address.get(), 
            entry_password.get(), 
            entry_SC_min.get(), 
            entry_BC_min.get()
        )
    )
    apply_changes_button.place(relx=0.6, rely=0.8)

    lable_address = Label(  
        subscription_window, 
        font=('Arial,18'), 
        text='Your email address: '
    )
    lable_address.place(relx=0.01, rely=0.05)    
    entry_address = Entry(
        subscription_window, width=30, borderwidth=1
    )
    entry_address.place(relx=0.5, rely=0.05)

    lable_password = Label( 
        subscription_window, 
        font=('Arial,18'), 
        text='Your email password: '
    )
    lable_password.place(relx=0.01, rely=0.2)
    entry_password = Entry(
        subscription_window, width=30, borderwidth=1, show='*'
    )
    entry_password.place(relx=0.5, rely=0.2)  

    try:
        response = requests.get(api_twelvedata.format('SC'))
        currency_base = response.json()['meta']['currency_base']
        date_time = response.json()['values'][0]['datetime']
        cost = response.json()['values'][0]['close']
        price_history_update(currency_base, date_time, cost)
    except: 
        cost = 'N/A'

    lable_SC_minmax = Label(
        subscription_window, 
        font=('Arial,18'), 
        text='Minimum tracked price for Siacoin: '
    )
    lable_SC_minmax.place(relx=0.01, rely=0.35)
    entry_SC_min = Entry(
        subscription_window, width=15
    )
    entry_SC_min.place(relx=0.5, rely=0.35)
    lable_BC_current = Label(
        subscription_window,
        font=('Arial, 10'), 
        text='Current: '+ cost
    )
    lable_BC_current.place(relx=0.73, rely=0.35)        

    try:
        response = requests.get(api_twelvedata.format('BTC'))
        currency_base = response.json()['meta']['currency_base']
        date_time = response.json()['values'][0]['datetime']
        cost = response.json()['values'][0]['close']
        price_history_update(currency_base, date_time, cost)
    except: 
        cost = 'N/A'

    lable_BC_minmax = Label(
        subscription_window, font=('Arial,18'), 
        text='Minimum tracked price  for Bitcoin: '
    )
    lable_BC_minmax.place(relx=0.01, rely=0.5)
    entry_BC_min = Entry(
        subscription_window, width=15
    )
    entry_BC_min.place(relx=0.5, rely=0.5) 
    lable_BC_current = Label(
        subscription_window, 
        font=('Arial, 10'), 
        text='Current: '+ cost
    )
    lable_BC_current.place(relx=0.73, rely=0.5)     

    subscription_window.mainloop


def discard_changes():
    subscription_window.destroy()

    try:
        button_sub_disabled.destroy(), lable_sub_disabled.destroy()
        sub_button(False)
        root_window.deiconify()
    except Exception: 
        pass


def apply_changes(address, password, SC_target, BC_target):
    subscription_window.destroy()
    settings_data_changer(address, password, SC_target, BC_target)
    subscription_switcher('enable')

    try:
        sub_button(True)
        root_window.deiconify()
    except Exception: 
        pass   

    logging.info(   
        datetime.today().strftime('%D - %H:%M:%S') 
        + ' Email subscription enabled'
    )

def create_history_button():
    button_sub_enabled = Button(
        root_window, 
        width=10, 
        text='Price History', 
        command=lambda: webbrowser.open('price_history')
    )
    button_sub_enabled.pack(side = RIGHT)

if __name__ == "__main__":  
    not_first_launch_check()

    root_window = Tk()
    root_window.title("Cryptocurrency to USD")
    root_window.geometry('500x140')  

    create_lables(symbols)
    sub_button(subscription_checker())
    create_history_button()

    root_window.after(60000, update_prices)
    logging.info(
        datetime.today().strftime('%D - %H:%M:%S') + ' Start'
    )
    root_window.mainloop()
    
def create_root_window():
    pass
    
def create_first_launch_window():
    pass