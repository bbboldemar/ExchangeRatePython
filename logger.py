import logging
from datetime import datetime

logging.basicConfig(
    filename = "logfile.log", 
    level = logging.DEBUG
)

def logger_wr_info(message: str) -> None:
    logging.info(datetime.today().strftime('%D - %H:%M:%S') + message)


def logger_wr_error(message: str) -> None:
    logging.error(datetime.today().strftime('%D - %H:%M:%S') + message)


def price_history_update(currency_base, date_time, cost):
    with open("price_history",'a') as f:
        f.write('at ' + date_time + ' ' + currency_base + ' value is ' + cost + '\n')