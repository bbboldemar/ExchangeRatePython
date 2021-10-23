from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from settings_checker import get_email_data
from logger import logger_wr_error, logger_wr_info

'''
Can with yandex.ru with another address and port, 
doesn't work with mail.ru.

2-step verification must be disabled, 
less secure apps must be enabled.
'''

def send_email(mail_content: str) -> int:
    """
    Sends email with given data from/to given "gmail.com" address.
    Can work with "yandex.ru" with another address and port, 
    doesn't work with "mail.ru".
    Less secure apps must be enabled,
    2-step verification must be disabled.
        Returns:
            int: 200 - message sent,
            401 - incorrect login/password,
            403 - less secure apps are disabled
            or 2-step verification enabled
            520 - dunoknowlol
    """
    if len(get_email_data()) != 0:
        your_address, your_password = get_email_data()
        message = MIMEMultipart()
        message['From'] = your_address
        message['To'] = your_address
        message['Subject'] = 'Price update from your app'
        message.attach(MIMEText(mail_content, 'plain'))
        text = message.as_string()
        try:
            session = smtplib.SMTP('smtp.gmail.com', 587, timeout = 1)
            session.starttls()
        except:
            logger_wr_error(
                'Error via sending email: less secure apps are disabled'
                'or 2-step verification enabled'
            )
            return 403
        try:
            session.login(your_address, your_password)
        except:
            logger_wr_error(
                'Error via sending email: wrong login/password'
            )
            return 401
        try:
            session.sendmail(your_address, your_address, text)
            session.quit()
            logger_wr_info(
                'Mail sent'
            )
            return 200
        except:
            logger_wr_error(
                'Error via sending email: something wrong with connection'
            )
            return 520
        
# print(send_email('OwO'))