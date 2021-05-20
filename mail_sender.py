import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# email_address = 'your_address@gmail.com'
# email_password = 'your_password'
# 2-step verification must be disabled, less secure apps must be enabled

def send_email(mail_content):
    message = MIMEMultipart()
    message['From'] = email_address
    message['To'] = email_address
    message['Subject'] = 'Price update from your app'
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587) 
    # must works with yandex.ru with another address and port
    # doesn't work with mail.ru at all
    session.starttls()
    session.login(email_address, email_password)
    text = message.as_string()
    session.sendmail(email_address, email_address, text)
    session.quit()
    print('Mail sent')

# send_email('OwO')