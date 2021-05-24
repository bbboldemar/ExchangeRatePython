from tkinter import messagebox, Label, Button, DISABLED, Tk
from tkinter.constants import BOTTOM, LEFT, RIGHT
import requests
from datetime import datetime
from mail_sender import send_email
from settings_checker import subscription_checker
import logging
logging.basicConfig(filename="logfile.log", level=logging.INFO)

labels = []
symbols = ['SC','BTC']
prices = [0.02, 36000]
api_twelvedata = 'https://api.twelvedata.com/time_series?symbol={}/USD&interval=1min&outputsize=3&format=JSON&dp=5&timezone=Europe/Moscow&apikey=f7e12a1a4dd34faca920cdff2c088e2b'

def not_first_launch_check():
    try:
        subscription_checker()
        return True
    except:
        global first_launch_window
        first_launch_window = Tk()
        first_launch_window.title("First launch setup")
        first_launch_window.geometry('500x90')
        lable_sub_enabled = Label(first_launch_window, font=('Arial,25'), text='Do you want to start tracking prices via email subscription?')
        lable_sub_enabled.pack()     
        button_sub_enabled = Button(first_launch_window, width=15, font=('Arial,25'), fg='red',text='No', command=lambda: first_launch_window_answer('No'))
        button_sub_enabled.pack(side = LEFT,padx = 20)
        button_sub_disabled = Button(first_launch_window, width=15, font=('Arial,25'), fg='green',text='Yes', command=lambda: first_launch_window_answer('Yes'))
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

def first_launch_window_answer(choise):
    f = open("exchanger_settings", "w")
    if choise == 'Yes':
        f.write('subscription_enabled\n')
        logging.info(datetime.today().strftime('%D - %H:%M:%S') + ' Email subscription enabled')
        subscription_settings_window()   
    else:        
        f.write('subscription_disabled\n')
        logging.info(datetime.today().strftime('%D - %H:%M:%S') + ' Email subscription disabled')   
        messagebox.showinfo ("Email subscription disabled", "You can enable email subscription later") 
        first_launch_window.destroy()      
    f.close()
         
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

def update_prices(state):
    if state == True:
        try:
            counter = 0
            for symbol in symbols:
                response = requests.get(api_twelvedata.format(symbol))
                date_time = response.json()['values'][0]['datetime']
                cost = response.json()['values'][0]['close']
                if symbol == 'SC':
                    CCoin = 'Siacoin'
                else:
                    CCoin = 'Bitcoin'
                if float(cost) > prices[counter] and subscription_checker() == True:
                    send_email(CCoin + ' cost is ' + cost + ' at ' + date_time + ' (more than ' + f'{prices[counter]}' + ')')
                    # messagebox.showinfo ("Price reached your limit!", CCoin + ' cost is ' + cost + ' at ' + date_time + ' (more than ' + f'{prices[counter]}' + ')')
                labels[counter].configure(text=CCoin + f' ({symbol})' ' value is ' + cost + ' at ' + date_time)
                counter +=1
            logging.info(datetime.today().strftime('%D - %H:%M:%S') + ' Update')
            root_window.after(60000, update_prices, False)  #Need to change to True   
        except:
            logging.error(datetime.today().strftime('%D - %H:%M:%S') + ' Error: cant reach remote API')
            messagebox.showinfo ("Error", "Can't reach remote API to update prices")
            root_window.after(5000, update_prices, False)   #Need to change to True    

def sub_button(choise):
    global button_sub_enabled, lable_sub_enabled, button_sub_disabled, lable_sub_disabled, root_window
    if choise == True:
        button_sub_enabled = Button(root_window, width=25, font='Arial,25', text='Disable Subscription', command=lambda: subscribsion_settings_opener('disable'))
        button_sub_enabled.pack(side = BOTTOM)
        lable_sub_enabled = Label(root_window, font=('Arial,20'), fg='green', text='email subcribtion enabled')
        lable_sub_enabled.pack(side = BOTTOM)
        try:
            button_sub_disabled.destroy(), lable_sub_disabled.destroy()
        except Exception: 
            pass
        update_prices(False)      
    else:
        button_sub_disabled = Button(root_window, width=25, font='Arial,25', text='Enable Subscription', command=lambda: subscribsion_settings_opener('enable'))
        button_sub_disabled.pack(side = BOTTOM)
        lable_sub_disabled= Label(root_window, font=('Arial,20'), fg='red', text='email subcribtion disabled')
        lable_sub_disabled.pack(side = BOTTOM)
        try:
            button_sub_enabled.destroy(), lable_sub_enabled.destroy()   
        except Exception: 
            pass  
        update_prices(False)   #Need to change to True 
               
def subscribsion_settings_opener(choise):
    with open("exchanger_settings",'r') as f:
        get_all = f.readlines()
    with open("exchanger_settings",'w') as f:
        for i,line in enumerate(get_all,1):
            if i == 1:
                if choise == 'enable':
                    choise = True
                    f.writelines('subscription_enabled\n')
                else:
                    choise = False
                    f.writelines('subscription_disabled\n')
                    logging.info(datetime.today().strftime('%D - %H:%M:%S') + ' Email subscription disabled')
            else:
                f.writelines(line)        
    if choise == True:
        root_window.withdraw()
        subscription_settings_window()                     
    sub_button(choise)

def subscription_settings_window():
    global root_window
    global subscription_window
    subscription_window = Tk()
    subscription_window.title("Settings")
    subscription_window.geometry('500x125')
    try:
        first_launch_window.destroy()
    except Exception: 
        pass
    apply_changes_button = Button(subscription_window, width=25, font='Arial,25', text='Apply changes ', command=lambda: apply_changes())
    apply_changes_button.pack(side = BOTTOM)  
    subscription_window.mainloop

def apply_changes():
    try:
        root_window.deiconify()
    except Exception: 
        pass
    subscription_window.destroy()
    logging.info(datetime.today().strftime('%D - %H:%M:%S') + ' Email subscription enabled')

not_first_launch_check()
root_window = Tk()
root_window.title("Cryptocurrency to USD")
root_window.geometry('500x125')  
logging.info(datetime.today().strftime('%D - %H:%M:%S') + ' Start')

create_lables(symbols)
sub_button(subscription_checker())
root_window.mainloop()




