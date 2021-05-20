import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import messagebox

def get_address():
    # f = open("exchanger_setting", "r")
    # contents = f.read()
    # f.close()
    # return contents
    return '******@gmail.com'

def get_password():
    return '******'

# your_address = 'your_address@gmail.com'
# your_password = 'your_password'
# 2-step verification must be disabled, less secure apps must be enabled
def send_email(mail_content):
    try:
        your_address = get_address()
    except:
        messagebox.showinfo ("Error", "Please input valid email adress")
        os._exit(os.EX_OK)
        # quit()
        # exit()
        # sys.exit('Error via sending email: address')
    try:
        your_password = get_password()
    except:
        messagebox.showinfo ("Error", "Please input valid password")
        os._exit(os.EX_OK)
        # sys.exit('Error via sending email: password')    
    try:
        message = MIMEMultipart()
        message['From'] = your_address
        message['To'] = your_address
        message['Subject'] = 'Price update from your app'
        message.attach(MIMEText(mail_content, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587)
        # must works with yandex.ru with another address and port
        # doesn't work with mail.ru at all
        session.starttls()
        session.login(your_address, your_password)
        text = message.as_string()
        session.sendmail(your_address, your_address, text)
        session.quit()
        print('Mail sent')
    except:
        messagebox.showinfo ("Error", "Invalid email address or password")
        print('Error via sending email: invalid SMTP parameters')


# send_email('OwO')