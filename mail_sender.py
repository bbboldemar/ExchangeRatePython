from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from settings_checker import read_user_log_pass
from logger import logger_wr_error, logger_wr_info

def send_email(mail_content:str) -> int:
    """ Sends email content with given data from/to given "gmail.com" 
    address and returns response code.
    Can work with "yandex.ru" with another address and port, 
    doesn't work with "mail.ru".
    For google account less secure apps must be enabled,
    2-step verification must be disabled.

    Args:
        - mail_content (str): any given string.

    Returns:
        - int: response code:
        
            - 200: Message sent;
            - 401: Incorrect login/password;
            - 403: Less secure apps are disabled or 2-step verification enabled;
            - 520: Unknown error.
    """
    your_address, your_password = read_user_log_pass()
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
      
  
def format_email_data(data_from_API:dict, target_price:float) -> int:
    """ Formats messages text.

    Args:
        - data_from_API (dict): reached price;
        - target_price (float): target price;

    Returns:
        - int: response code:
            - 200: Message sent;
            - 401: Incorrect login/password;
            - 403: Less secure apps are disabled or 2-step verification enabled;
            - 520: Unknown error.
    """
    email_status = send_email(
        data_from_API['currency_base'] + ' cost is ' 
        + data_from_API['cost'] + ' at ' + data_from_API['date_time'] 
        + ' (more than ' + f'{target_price}' + ')'
    )
    return email_status

# print(send_email('OwO'))