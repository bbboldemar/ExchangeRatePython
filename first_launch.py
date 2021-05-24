from tkinter import Button, Entry, Tk, Label, messagebox
from tkinter.constants import LEFT, RIGHT
from datetime import datetime
import logging
import os
import sys
logging.basicConfig(filename="logfile.log", level=logging.INFO)
global button_sub_disabled, lable_sub_disabled

def subscription_settings_window(first_launch):
    global subscription_window
    subscription_window = Tk()
    subscription_window.title("Settings")
    subscription_window.geometry('500x125')
    # subscription_window.after(1000, subscription_window.mainloop())
    if first_launch == True:
        first_launch_window.destroy()
        # subscription_window = Tk()
        # subscription_window.title("Settings")
        # subscription_window.geometry('500x125')
        disabled = Button(subscription_window, width=25, font='Arial,25', text='Destroy', command=lambda: a(True))
        disabled.pack()  
        # subscription_window.mainloop()
    else:
        # subscription_window = Tk()
        # subscription_window.title("Settings")
        # subscription_window.geometry('500x125')
        disabled = Button(subscription_window, width=25, font='Arial,25', text='Destroy', command=lambda: a(False))
        disabled.pack()  
        return False
    subscription_window.mainloop    
        


def a(first_launch):
    
    if first_launch == True:
        subscription_window.destroy()
        
    if first_launch == False:
        subscription_window.destroy()

        


def subscription_checker():
    f = open("exchanger_settings", "r")
    checker = f.readline()
    try:
        if checker == 'subscription_enabled\n':
            status = True
        else:
            status = False
    except:
        status = False               
    f.close()
    return status

def not_first_launch_check():
    try:
        subscription_checker()
    except:
        global first_launch_window
        first_launch_window = Tk()
        first_launch_window.title("First launch setup")
        first_launch_window.geometry('500x90')
        lable_sub_enabled = Label(first_launch_window, font=('Arial,25'), text='Do you want to start tracking prices via email subscription?')
        lable_sub_enabled.pack()     
        button_sub_enabled = Button(first_launch_window, width=15, font=('Arial,25'), fg='red',text='No', command=lambda: first_launch_subscription('No'))
        button_sub_enabled.pack(side = LEFT,padx = 20)
        button_sub_disabled = Button(first_launch_window, width=15, font=('Arial,25'), fg='green',text='Yes', command=lambda: first_launch_subscription('Yes'))
        button_sub_disabled.pack(side = RIGHT,padx = 20)
        f = open("exchanger_settings", "w")
        f.write('subscription_disabled\n')
        f.close()
        logging.info(datetime.today().strftime('%D - %H:%M:%S') + ' First launch, email subscription disabled')  
        first_launch_window.mainloop()        
        # print('Через пробел ведите логин и пароль от почты для подписки на email рассылку')
        # user_data = input()
        # f = open("exchanger_settings", "w")
        # f.write(user_data)
        # f.close()
        # messagebox.showinfo ("You are subscribed now", "Yor login and password are: " + user_data)
        # os.execv(sys.executable, ['python'] + sys.argv)
        
def first_launch_subscription(choise):
    global first_launch_window
    f = open("exchanger_settings", "w")
    if choise == 'Yes':
        f.write('subscription_enabled\n')
        logging.info(datetime.today().strftime('%D - %H:%M:%S') + ' Email subscription enabled')
        subscription_settings_window(True)   
    else:        
        f.write('subscription_disabled\n')
        logging.info(datetime.today().strftime('%D - %H:%M:%S') + ' Email subscription disabled')   
        messagebox.showinfo ("Email subscription disabled", "You can enable email subscription later") 
        first_launch_window.destroy()      
    f.close()
    