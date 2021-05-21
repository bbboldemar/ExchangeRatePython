import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import messagebox
from datetime import datetime
import logging
logging.basicConfig(filename="logfile.log", level=logging.INFO)

# def get_email_data():
    # f = open("exchanger_settings", "r")
    # contents = f.read().split()
    # f.close()
    # return contents

def send_email(mail_content):
    try:
        # your_address, your_password = get_email_data()
        your_address = '******@gmail.com'
        your_password = "******"
        exchanger_setting_exists = True
    except:
        logging.error(datetime.today().strftime('%D - %H:%M:%S') + ' Error via sending email: cant reach exchanger_settings')
        exchanger_setting_exists = False
        # messagebox.showinfo ("Error", "Can't reach Subscription Setting ")
    if  exchanger_setting_exists == True:
        try:
            message = MIMEMultipart()
            message['From'] = your_address
            message['To'] = your_address
            message['Subject'] = 'Price update from your app'
            message.attach(MIMEText(mail_content, 'plain'))
            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.starttls()
            session.login(your_address, your_password)
            text = message.as_string()
            session.sendmail(your_address, your_address, text)
            session.quit()
            logging.info(datetime.today().strftime('%D - %H:%M:%S') + ' Mail sent')
            return True
        except:
            logging.error(datetime.today().strftime('%D - %H:%M:%S') + ' Error via sending email: invalid SMTP parameters')
            messagebox.showinfo ("Subscription Error", "Invalid address or password")
            return False
        

# send_email('OwO')

# must works with yandex.ru with another address and port
# doesn't work with mail.ru at all
# your_address = 'your_address@gmail.com'
# your_password = 'your_password'
# 2-step verification must be disabled, less secure apps must be enabled