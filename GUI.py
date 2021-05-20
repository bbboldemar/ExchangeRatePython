from tkinter import Button, Entry, Tk, Label, messagebox
from tkinter.constants import BOTTOM
import requests
from datetime import datetime
from mail_sender import send_email
import logging
logging.basicConfig(filename="logfile.log", level=logging.INFO)
import os

labels = []
cycles = 0
symbols = ['SC','BTC']
prices = [0.02, 39000]
api_twelvedata = 'https://api.twelvedata.com/time_series?symbol={}/USD&interval=1min&outputsize=3&format=JSON&dp=5&timezone=Europe/Moscow&apikey=f7e12a1a4dd34faca920cdff2c088e2b'

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
            if float(cost) > prices[counter]:
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


def change_email_adress(new_email):
    f = open("exchanger_settings", "w")
    f.write(new_email)
    f.close()
    messagebox.showinfo ("Success", "Email is changed to " + new_email)

root_window = Tk()
root_window.title("Cryptocurrency to USD")
root_window.geometry('500x125')

create_lables(symbols)

button = Button(width=25,text='Change email adress', command=lambda: change_email_adress(entry.get()))
button.pack(side = BOTTOM)
entry = Entry(width=25, borderwidth=1)
entry.pack(side = BOTTOM)

root_window.after(5000, update_prices)
logging.info(datetime.today().strftime('%D - %H:%M:%S') + ' Start')
root_window.mainloop()
