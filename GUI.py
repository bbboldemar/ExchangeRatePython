from tkinter import Label, Button, Tk, Entry, messagebox
from tkinter.constants import BOTTOM, LEFT, RIGHT
import webbrowser

from logger import logger_wr_error, logger_wr_info, price_history_update
from API import load_data_from_API
from mail_sender import send_email
from settings_checker import (
    user_is_subscribed_checker,
    subscription_switcher, 
    settings_data_changer, 
    target_price_checker, 
    create_user_files,
    user_files_exist
)

labels = []
currencies = ['SC','BTC']

def create_lables(currencies):
    try:
        for currency in currencies:
            data_from_API = load_data_from_API(currency)
            currency_base = data_from_API[0]
            date_time = data_from_API[1]
            cost = data_from_API[2]
            price_history_update(currency_base, date_time, cost)
            lable = Label(
                root_window, 
                font = ('Arial,25'), 
                text = currency_base + f' ({currency})' ' value is ' 
                    + cost + ' at ' + date_time
            )
            lable.pack()
            labels.append(lable)
    except:
        logger_wr_error(
            ' Error: cant reach remote API'
        )
        messagebox.showinfo (
            "Error", "Can't reach remote server"
        )
        create_lables(currencies)


def create_history_button():
    button_sub_enabled = Button(
        root_window, 
        width=10, 
        text='Price History', 
        command=lambda: webbrowser.open('price_history')
    )
    button_sub_enabled.pack(side = RIGHT)


def subscribsion_settings_opener(choise):
    subscription_switcher('disable')
    
    if choise == 'disable':
        logger_wr_info(
            ' Email subscription disabled'
        )
        sub_button(False)
    else:         
        root_window.withdraw()
        create_subscription_settings_window()


def update_prices():
    email_is_send = True
    user_is_subscribed = user_is_subscribed_checker()
    logger_wr_info(
        ' Updating...'
    )
    if user_is_subscribed:
        try:
            prices = target_price_checker()
        except:
            button_sub_enabled.destroy(), lable_sub_enabled.destroy()
            logger_wr_error(
                ' Invalid target price format, subscription disabled'
            )
            messagebox.showinfo (
                "Subscription Disabled", "Invalid target price format"
            )
            subscribsion_settings_opener('enable')
            user_is_subscribed = False

    try:
        counter = 0
        for currency in currencies:
            data_from_API = load_data_from_API(currency)
            currency_base = data_from_API[0]
            date_time = data_from_API[1]
            cost = data_from_API[2]
            price_history_update(currency_base, date_time, cost)
            if user_is_subscribed and float(cost) > prices[counter]:
                email_is_send = send_email(
                    currency_base + ' cost is ' 
                    + cost + ' at ' + date_time 
                    + ' (more than ' + f'{prices[counter]}' + ')'
                )
            labels[counter].configure(text=currency_base 
            + f' ({currency})' ' value is ' + cost + ' at ' + date_time
            )
            counter += 1
        if not email_is_send:
            root_window.withdraw()
            button_sub_enabled.destroy(), lable_sub_enabled.destroy()
            logger_wr_error(
                ' Invalid email address or password, subscription disabled'
            )
            messagebox.showinfo (
                "Subscription Disabled", "Invalid email address or password"
            )
            subscribsion_settings_opener('enable')            
        logger_wr_info(
            ' Successful update!'
        )
    except:
        logger_wr_error(
            ' Error: cant reach remote API'
        )
        messagebox.showinfo (
            "Error", "Can't reach remote API to update prices"
        )
    root_window.after(60000, update_prices)


def sub_button(choise):
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


def apply_subscription_changes(address, password, SC_target, BC_target, status):
    subscription_window.destroy()
    
    if not status:
        button_sub_disabled.destroy(), lable_sub_disabled.destroy()
    else:
        settings_data_changer(address, password, SC_target, BC_target)
        subscription_switcher('enable')
        logger_wr_info(   
            ' Email subscription enabled'
        )
    sub_button(status)
    root_window.deiconify()

def create_subscription_settings_window():
    # global entry_address, entry_password, entry_SC_min, entry_BC_min, root_window
    global subscription_window
    subscription_window = Tk()
    subscription_window.title("Settings")
    subscription_window.geometry('560x180')
    
    discard_button = Button(
        subscription_window, 
        width=18, 
        fg='red', 
        font='Arial,25', 
        text='Disable Subscription', 
        command=lambda: apply_subscription_changes(
            'None', 
            'None', 
            'None', 
            'None',
            False
        )
    )
    apply_changes_button = Button(  
        subscription_window, 
        width=18, 
        fg='green', 
        font='Arial,25', 
        text='Apply Changes', 
        command=lambda: apply_subscription_changes(
            entry_address.get(), 
            entry_password.get(), 
            entry_SC_min.get(), 
            entry_BTC_min.get(),
            True
        )
    )
        
        
        
    try:
        data_from_API = load_data_from_API('SC')
        currency_base = data_from_API[0]
        date_time = data_from_API[1]
        cost = data_from_API[2]
        price_history_update(currency_base, date_time, cost)
    except: 
        cost = 'N/A'
    try:
        data_from_API = load_data_from_API('BTC')
        currency_base = data_from_API[0]
        date_time = data_from_API[1]
        cost = data_from_API[2]
        price_history_update(currency_base, date_time, cost)
    except: 
        cost = 'N/A'
           
           
           
    lable_BTC_min_trackin_price = Label(
        subscription_window, font=('Arial,18'), 
        text='Minimum tracked price for Bitcoin: '
    )
    lable_SC_min_trackin_price = Label(
        subscription_window, 
        font=('Arial,18'), 
        text='Minimum tracked price for Siacoin: '
    )
    lable_SC_current = Label(
        subscription_window,
        font=('Arial, 10'), 
        text='Current: '+ cost
    )
    lable_BTC_current = Label(
        subscription_window, 
        font=('Arial, 10'), 
        text='Current: '+ cost
    )
    lable_address = Label(  
        subscription_window, 
        font=('Arial,18'), 
        text='Your email address: '
    )
    lable_password = Label( 
        subscription_window, 
        font=('Arial,18'), 
        text='Your email password: '
    )
    entry_address = Entry(
        subscription_window, width=30, borderwidth=1
    )
    entry_password = Entry(
        subscription_window, width=30, borderwidth=1, show='*'
    )
    entry_SC_min = Entry(
        subscription_window, width=15
    )
    entry_BTC_min = Entry(
        subscription_window, width=15
    )
    
    discard_button.place(relx=0.02, rely=0.8)
    apply_changes_button.place(relx=0.6, rely=0.8)

    lable_SC_min_trackin_price.place(relx=0.01, rely=0.35)
    lable_BTC_min_trackin_price.place(relx=0.01, rely=0.5)
    lable_address.place(relx=0.01, rely=0.05)
    lable_password.place(relx=0.01, rely=0.2)
    lable_SC_current.place(relx=0.73, rely=0.35)
    lable_BTC_current.place(relx=0.73, rely=0.5)

    entry_address.place(relx=0.5, rely=0.05)
    entry_password.place(relx=0.5, rely=0.2)
    entry_SC_min.place(relx=0.5, rely=0.35)
    entry_BTC_min.place(relx=0.5, rely=0.5) 

    subscription_window.mainloop



def user_need_subscription(Yes):
    first_launch_window.withdraw()
    if Yes:
        create_subscription_settings_window()          
    else:        
        logger_wr_info(
            ' Email subscription disabled'
        )
        messagebox.showinfo (
            "Email subscription disabled", 
            "You can enable email subscription later"
        )  
    first_launch_window.destroy()


def create_first_launch_window():
    global first_launch_window
    first_launch_window = Tk()
    first_launch_window.title("First launch setup")
    first_launch_window.geometry('500x90')
    
    lable_enable_sub_first_launch_window = Label(
        first_launch_window, 
        font=('Arial,25'), 
        text='Start tracking prices via email subscription?'
    )
         
    button_enable_sub_first_launch_window = Button(
        first_launch_window, 
        width=15, 
        font=('Arial,25'), 
        fg='red',
        text='No', 
        command=lambda: user_need_subscription(False)
    )
    
    button_disable_sub_first_launch_window = Button(
        first_launch_window, 
        width=15, 
        font=('Arial,25'), 
        fg='green',
        text='Yes', 
        command=lambda: user_need_subscription(True)
    )
    
    lable_enable_sub_first_launch_window.pack()
    button_enable_sub_first_launch_window.pack(side = LEFT,padx = 20)
    button_disable_sub_first_launch_window.pack(side = RIGHT,padx = 20)
    first_launch_window.mainloop()


def create_main_window():
    global root_window
    root_window = Tk()
    root_window.title("Cryptocurrency to USD")
    root_window.geometry('500x140')  

    create_lables(currencies)
    sub_button(user_is_subscribed_checker())
    create_history_button()
    
    logger_wr_info(
        ' Start'
    )

if __name__ == "__main__":  
    if not user_files_exist():
        create_user_files()
        logger_wr_info(
            ' First launch'
        )
        create_first_launch_window()
    create_main_window()
    root_window.after(15000, update_prices)
    root_window.mainloop()
    
    


# class Person:
 
#     # конструктор
#     def __init__(self, name):
#         self.name = name  # устанавливаем имя
 
#     def display_info(self):
#         print("Привет, меня зовут", self.name)
 
# # person1 = Person("Tom")
# # person1.display_info()         # Привет, меня зовут Tom 

# class Windows:
#     def root_window():
#         pass
        
        
#     def first_launch_window():
#         pass
    
# class Labeles:
#     def __init__(self, name):
#         self.name = name  # устанавливаем имя
 
#     def display_info(self):
#         print("Привет, меня зовут", self.name)
