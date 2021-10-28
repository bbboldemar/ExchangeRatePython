from tkinter import Label, Button, Tk, Entry, messagebox
from tkinter.constants import BOTTOM, LEFT, RIGHT

from API import load_data_from_API, data_from_API_is_correct
from logger import DATAFILE_open, LOGFILE_open
from mail_sender import format_email_data
from settings_checker import (
    check_user_is_subscribed,
    switch_subscription, 
    write_settings_data,
    convert_target_rate,
    create_default_user_files,
    user_files_exist
)
from main import CURRENCIES


def create_lables_CCrate(CURRENCIES):
    global root_window_labels
    root_window_labels = []
    data_from_API = [load_data_from_API(currency) for currency in CURRENCIES]
    print(data_from_API)
    if data_from_API_is_correct(data_from_API):
        for currency in range(len(CURRENCIES)):
            lable = Label(
                root_window, 
                font = ('Arial,25'), 
                text = 
                    data_from_API[currency]['currency_base'] + 
                    ' value is ' +
                    data_from_API[currency]['cost'] + ' at ' + 
                    data_from_API[currency]['date_time']
            )
            lable.pack()
            root_window_labels.append(lable)
    else:
        messagebox.showinfo(
            "Error", "API connection error. Opening log file."
        )
        LOGFILE_open()
        print ('API error. Exit')
        raise exit()
                    

def update_lables_CCrate(CURRENCIES):
    # counter = 0
    data_from_API = [load_data_from_API(currency) for currency in CURRENCIES]
    print (data_from_API)
    if data_from_API_is_correct(data_from_API):
        for currency in range(len(CURRENCIES)):
            print (currency)
            # root_window_labels[currency].configure(
            #     text = 
            #         data_from_API[currency]['currency_base'] + 
            #         ' value is ' +
            #         data_from_API[currency]['cost'] + ' at ' + 
            #         data_from_API[currency]['date_time']
            # )
            # if check_user_is_subscribed():
            #     email_parser(data_from_API, counter)
            # counter += 1
    else:
        messagebox.showinfo(
            "Error", "API connection error. Opening log file."
        )
        LOGFILE_open()
        print ('API error. Exit')
        raise exit()
    # root_window.after(60000, func = update_lables_CCrate(CURRENCIES))


def email_parser(data_from_API:dict, counter:int):
    target_rate = convert_target_rate()
    if target_rate != None:
        rate_reached_target = float(data_from_API['cost']) > target_rate[counter]
        if rate_reached_target:
            email_status = format_email_data(data_from_API, target_rate[counter])
            if email_status != 200:
                subscribsion_settings_opener('enable')
                # button_sub_enabled.destroy(), lable_sub_enabled.destroy()
                if email_status == 401:
                    messagebox.showinfo (
                        "Subscription Disabled", "Invalid email address or password."
                    )
                if email_status == 403:
                    messagebox.showinfo (
                        "Subscription Disabled", 
                        "Less secure apps must be enabled, " 
                        "2-step verification must be disabled."
                    )
                if email_status == 520:
                    messagebox.showinfo (
                        "Subscription Disabled", 
                        "Unknown problem via sending email. "
                        "Contact developer via github"
                    )
                      
    else:
        button_sub_enabled.destroy(), lable_sub_enabled.destroy()
        messagebox.showinfo (
            "Subscription Disabled", "Invalid target price format"
        )
        subscribsion_settings_opener('enable')


def create_history_button():
    button_sub_enabled = Button(
        root_window, 
        width=10, 
        text='Price History', 
        command=lambda: DATAFILE_open()
    )
    button_sub_enabled.pack(side = RIGHT)

def subscribsion_settings_opener(choise):
    switch_subscription(False)
    
    if choise == 'disable':
        sub_button(False)
    else:         
        root_window.withdraw()
        create_subscription_settings_window()


      





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
        write_settings_data(address, password, SC_target, BC_target)
    sub_button(status)
    root_window.deiconify()

def create_subscription_settings_window():
    'Nice'
    global subscription_window
    subscription_window = Tk()
    subscription_window.title("Settings. Please, fill all entry fields")
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
           
           
           
    lable_BTC_min_trackin_price = Label(
        subscription_window, font=('Arial,18'), 
        text='Minimum tracked price for Bitcoin: '
    )
    lable_SC_min_trackin_price = Label(
        subscription_window, 
        font=('Arial,18'), 
        text='Minimum tracked price for Siacoin: '
    )
    data_from_API = [load_data_from_API(currency) for currency in CURRENCIES]
    if data_from_API_is_correct(data_from_API):
        lable_SC_current = Label(
            subscription_window,
            font=('Arial, 10'), 
            text='Current: '+ data_from_API[0]['cost']
        )
        lable_BTC_current = Label(
            subscription_window, 
            font=('Arial, 10'), 
            text='Current: '+ data_from_API[1]['cost']
            )
    else: 
        lable_SC_current = Label(
            subscription_window,
            font=('Arial, 10'), 
            text='Current: N/A'
        )
        lable_BTC_current = Label(
            subscription_window, 
            font=('Arial, 10'), 
            text='Current: N/A'
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





def create_first_launch_window():
    def user_need_subscription(confirmation):
        first_launch_window.destroy()
        if confirmation:
            create_subscription_settings_window()   
            # root_window.deiconify()
            
    global first_launch_window
    first_launch_window = Tk()
    first_launch_window.title("First launch setup")
    first_launch_window.geometry('500x90')
    
    lable_enable_sub_first_launch_window = Label(
        first_launch_window, 
        font=('Arial,25'), 
        text='Start tracking target rate via email subscription?'
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


def create_root_window():
    global root_window
    root_window = Tk()
    root_window.title("Cryptocurrency to USD")
    root_window.geometry('500x140')  
    create_lables_CCrate(CURRENCIES)
    

    sub_button(check_user_is_subscribed())
    create_history_button()
    
    root_window.mainloop()
    # root_window.after(3000, update_lables_CCrate(CURRENCIES))

if __name__ == "__main__":
    if not user_files_exist():
        create_default_user_files()
        create_first_launch_window()
    create_root_window()
    
    

"""
class Person:
 
    # конструктор
    def __init__(self, name):
        self.name = name  # устанавливаем имя
 
    def display_info(self):
        print("Привет, меня зовут", self.name)
 
# person1 = Person("Tom")
# person1.display_info()         # Привет, меня зовут Tom 

class Windows:
    def root_window():
        pass
        
        
    def first_launch_window():
        pass
    
class Labeles:
    def __init__(self, name):
        self.name = name  # устанавливаем имя
 
    def display_info(self):
        print("Привет, меня зовут", self.name)
"""

