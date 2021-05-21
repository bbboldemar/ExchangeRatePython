from tkinter import Button, Entry, Tk, Label, messagebox
from tkinter.constants import LEFT, RIGHT
from datetime import datetime
import logging
logging.basicConfig(filename="logfile.log", level=logging.INFO)

def subscription_checker():
    f = open("exchanger_settings", "r")
    checker = f.readline()
    try:
        if checker == 'subscription_enabled\n':
            status = 1
        else:
            status = 0
    except:
        status = 0                
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
        button_sub_enabled = Button(first_launch_window, width=22, font=('Arial,25'), fg='red',text='No', command=lambda: first_launch_subscription('No'))
        button_sub_enabled.pack(side = LEFT)
        button_sub_disabled = Button(first_launch_window, width=22, font=('Arial,25'), fg='green',text='Yes', command=lambda: first_launch_subscription('Yes'))
        button_sub_disabled.pack(side = RIGHT)
        f = open("exchanger_settings", "w")
        f.write('subscription_disabled\n')
        f.close()  
        first_launch_window.mainloop()        
        # print('Через пробел ведите логин и пароль от почты для подписки на email рассылку')
        # user_data = input()
        # f = open("exchanger_settings", "w")
        # f.write(user_data)
        # f.close()
        # messagebox.showinfo ("You are subscribed now", "Yor login and password are: " + user_data)
        # os.execv(sys.executable, ['python'] + sys.argv)
        
def first_launch_subscription(choise):
    if choise == 'Yes':
        f = open("exchanger_settings", "w")
        f.write('subscription_enabled\n')
        f.close()
        messagebox.showinfo ("Email subscription enabled", "Start tracking target prices")          
    else:        
        f = open("exchanger_settings", "w")
        f.write('subscription_disabled\n')
        f.close()   
        messagebox.showinfo ("Email subscription disabled", "You can enable email subscription later")       
    first_launch_window.destroy()