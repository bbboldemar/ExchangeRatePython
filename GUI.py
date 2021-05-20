from tkinter import Button, Entry, Tk, Label, messagebox
from tkinter.constants import BOTTOM
import requests



def change_email_adress(new_email):
    f = open("subscription", "w")
    f.write(new_email)
    f.close()
    messagebox.showinfo ("Success", "Email is changed to " + new_email)

 

root_window = Tk()
root_window.title("Cryptocurrency Rate")
root_window.geometry('480x110')
 



siacoin_response = requests.get('https://api.twelvedata.com/time_series?symbol=SC/USD&interval=1min&outputsize=3&format=JSON&dp=5&timezone=Europe/Moscow&apikey=f7e12a1a4dd34faca920cdff2c088e2b')
bitcoin_response = requests.get('https://api.twelvedata.com/time_series?symbol=BTC/USD&interval=1min&outputsize=3&format=JSON&dp=5&timezone=Europe/Moscow&apikey=f7e12a1a4dd34faca920cdff2c088e2b')

siacoin_datetime = siacoin_response.json()['values'][0]['datetime']
siacoin_cost = siacoin_response.json()['values'][0]['close']

bitcoin_datetime = siacoin_response.json()['values'][0]['datetime']
bitcoin_cost = bitcoin_response.json()['values'][0]['close']

siacoin_lable = Label(root_window, font=('Arial,25'), text='Siacoin value is ' + siacoin_cost + ' at ' + siacoin_datetime)
siacoin_lable.pack()#side = LEFT/RIGHT/BOTTOM/TOP

bitcoin_lable = Label(root_window, font=('Arial,25'), text='Bitcoin value is ' + bitcoin_cost + ' at ' + bitcoin_datetime)
bitcoin_lable.pack()



button = Button(width=25,text='Change email adress', command=lambda: change_email_adress(entry.get()))
button.pack(side = BOTTOM)
entry = Entry (width=25, borderwidth=1)
entry.pack(side = BOTTOM)



root_window.mainloop() 