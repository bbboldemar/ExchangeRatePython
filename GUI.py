from tkinter import Label, Button, Tk, Entry, messagebox
from tkinter.constants import BOTTOM, LEFT, RIGHT

from API import load_data_from_API, keys_read_API_key
from logger import DATAFILE_open, LOGFILE_open
from mail_sender import format_email_data
from settings_checker import (
    switch_exchanger_settings_subscription,
    convert_exchanger_settings_target_rate,
    check_exchanger_settings_subscription,
    create_exchanger_settings_file,
    write_exchanger_settings_data,
    exchanger_settings_exist
)

def raise_exit_incorrect_data():
    messagebox.showinfo(
            "Error", "API connection error. Opening log file."
        )
    LOGFILE_open()
    print ('API error. Exit')
    raise exit()


def raise_error_email_subscription(email_status):
    root_window.withdraw()
    subscribsion_settings_opener('enable')
    if email_status == 401:
        message = (
            "Invalid email address/password OR "
            "less secure apps are disabled OR "
            "2-step verification enabled."
        )
    elif email_status == 403:
        message = ("Can not connect to smtp.gmail.com on port 587")
    elif email_status == 412:
        message = ("Invalid target price format.")
    else:
        message = (
            "Unknown problem via sending email. "
            "Contact developer via github"
            )
    messagebox.showinfo ("Subscription Disabled", message)


def form_email(data_from_API:dict, counter:int):
    target_rate = convert_exchanger_settings_target_rate()
    if target_rate != None:
        rate_reached_target = float(data_from_API['cost']) > target_rate[counter]
        if rate_reached_target:
            email_status = format_email_data(data_from_API, target_rate[counter])
            if email_status != 200:
                raise_error_email_subscription(email_status)        
    else:
        raise_error_email_subscription(412)
                

def update_lables_CCrate():
    CURRENCIES = ['SC','BTC']####
    print ('update')
    first_call_key = keys_read_API_key()
    data_from_API = [
        load_data_from_API(
            currency, 
            first_call_key, 
            keys_read_API_key()
        ) for currency in CURRENCIES]
    if None not in data_from_API:
        for block, currency in enumerate(CURRENCIES):
            root_window_labels[block].configure(
                text = 
                    data_from_API[block]['currency_base'] + 
                    ' value is ' +
                    data_from_API[block]['cost'] + ' at ' + 
                    data_from_API[block]['date_time']
            )
            if check_exchanger_settings_subscription():
                form_email(data_from_API[block], block)
        root_window.after(60000, update_lables_CCrate)
    else:
        raise_exit_incorrect_data()


def create_lables_CCrate():
    CURRENCIES = ['SC','BTC']####
    print ('create')
    global root_window_labels
    first_call_key = keys_read_API_key()
    data_from_API = [
        load_data_from_API(
            currency, 
            first_call_key, 
            keys_read_API_key()
        ) for currency in CURRENCIES]
    if None not in data_from_API:
        root_window_labels = []
        for block, currency in enumerate(CURRENCIES):
            lable = Label(
                root_window, 
                font = ('Arial,25'), 
                text = 
                    data_from_API[block]['currency_base'] + 
                    ' value is ' +
                    data_from_API[block]['cost'] + ' at ' + 
                    data_from_API[block]['date_time']
            )
            lable.pack()
            root_window_labels.append(lable)
    else:
        raise_exit_incorrect_data()


def create_history_button():
    button_sub_enabled = Button(
        root_window, 
        width=10, 
        text='Price History', 
        command=lambda: DATAFILE_open()
    )
    button_sub_enabled.pack(side = RIGHT)
#
#
#
#
def subscribsion_settings_opener(choise):
    switch_exchanger_settings_subscription('disable')
    
    if choise == 'disable':
        sub_button(False)
    else:         
        root_window.withdraw()
        create_subscription_settings_window()


def apply_subscription_changes(address, password, SC_target, BC_target, status):
    subscription_window.destroy()
    
    if not status:
        try:
            button_sub_disabled.destroy(), lable_sub_disabled.destroy()
        except Exception: 
            print ('not a bug')
    else:
        write_exchanger_settings_data(address, password, SC_target, BC_target)
    sub_button(status)
    root_window.deiconify()


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
            print ('not a bug')
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
            print ('not a bug')


def create_subscription_settings_window():
    CURRENCIES = ['SC','BTC']####
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
    first_call_key = keys_read_API_key()
    # change to reading from Price-History BUT it isn't exist on firt launch
    data_from_API = [
        load_data_from_API(
            currency, 
            first_call_key, 
            keys_read_API_key()
        ) for currency in CURRENCIES]
    # if data_from_API_is_correct(data_from_API):
    if None not in data_from_API:
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
#
#
#
#
def create_first_launch_window():
    def user_need_subscription(confirmation):
        first_launch_window.destroy()
        if confirmation:
            create_subscription_settings_window()   
            
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
    
    create_lables_CCrate()
    root_window.after(60000, update_lables_CCrate)
    sub_button(check_exchanger_settings_subscription())
    create_history_button()
    root_window.mainloop()
    

if __name__ == "__main__":
    if not exchanger_settings_exist():
        create_exchanger_settings_file()
        create_first_launch_window()
    create_root_window()
    

