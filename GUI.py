from tkinter import Button, Entry, Tk, Label, messagebox
import requests
def change_email_adress(new_email):
    f = open("subscription", "w")
    f.write(new_email)
    f.close()
    messagebox.showinfo ("Success", "Email is changed to " + new_email)

#def create_labels(symbols):
#    for symbol in symbols:
#        response = 


root_window = Tk()
root_window.title("Nani")
root_window.geometry('480x480')

google_response = requests.get('https://api.twelvedata.com/time_series?symbol=GOOGL&interval=1min&type=stock&outputsize=1&format=JSON&dp=4&timezone=Europe/Moscow&apikey=f7e12a1a4dd34faca920cdff2c088e2b'   )

siacoin_response = requests.get('https://api.twelvedata.com/time_series?symbol=SC/BNB&interval=1min&outputsize=1&format=JSON&dp=4&apikey=f7e12a1a4dd34faca920cdff2c088e2b'    )

#print (google_response)
#print (google_response.json())
print (google_response.json()['values'][0]['datetime'])
print (google_response.json()['values'][0]['close'])
google_datetime = google_response.json()['values'][0]['datetime']
google_cost = google_response.json()['values'][0]['close']


entry = Entry (width=10, borderwidth=1)
entry.pack()

google_lable = Label(root_window, font=('Arial,25'), text='GOOGL ' + google_datetime + ' ' + google_cost)
google_lable.pack()#side = LEFT/RIGHT/BOTTOM/TOP

apple_lable = Label(root_window, text='SC')
apple_lable.pack()

button = Button(text='Change email adress', command=lambda: change_email_adress(entry.get()))
button.pack()

root_window.mainloop() 