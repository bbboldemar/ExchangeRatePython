from tkinter import Button, Entry, Tk, Label, messagebox
from tkinter.constants import BOTTOM
import requests
from datetime import datetime
from mail_sender import send_email

labels = []
cycles = 0
symbols = ['SC','BTC']
prices = [0.02, 39000]
api_twelvedata = 'https://api.twelvedata.com/time_series?symbol={}/USD&interval=1min&outputsize=3&format=JSON&dp=5&timezone=Europe/Moscow&apikey=f7e12a1a4dd34faca920cdff2c088e2b'

def update_prices():
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
    print ('updated at ' + datetime.today().strftime('%H:%M:%S'))
    root_window.after(60000, update_prices)
    
def create_lables(symbols):
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

def change_email_adress(new_email):
    f = open("exchanger_setting", "w")
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

root_window.after(10000, update_prices)
root_window.mainloop() 