from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from settings_checker import get_email_data
from logger import logger_wr_error, logger_wr_info

'''
Must work with yandex.ru with another address and port, 
doesn't work with mail.ru.

2-step verification must be disabled, 
less secure apps must be enabled.
'''

def send_email(mail_content: str) -> bool:
    exchanger_settings_exists = False
    try:
        your_address, your_password = get_email_data()
        exchanger_settings_exists = True
    except:
        logger_wr_error(
            ' Error via sending email: cant reach exchanger_settings'
        )

    if  exchanger_settings_exists:        
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
            logger_wr_info(
                ' Mail sent'
            )
            return True
        except:
            logger_wr_error(
                ' Error via sending email: invalid SMTP parameters'
            )            
    return False
        
# print(send_email('OwO'))