import os

CURRENCIES = ['SC','BTC']

API_URL = (
    'https://api.twelvedata.com/time_series?symbol={}/'
    'USD&interval=1min&outputsize=3&format=JSON&dp=5&'
    'timezone=Europe/Moscow&apikey={}'
    )

SETTINGS = "exchanger_settings"
DATAFILE = "Price-History"
LOGFILE = "logfile.log"
KEYS = 'keys'

ROOT_DIR = os.path.dirname(os.path.abspath('__main__'))
PATH_TO_DATAFILE = os.path.join(ROOT_DIR, 'userfiles', DATAFILE)
PATH_TO_SETTINGS = os.path.join(ROOT_DIR, 'userfiles', SETTINGS)
PATH_TO_LOGFILE = os.path.join(ROOT_DIR, 'userfiles', LOGFILE)
PATH_TO_KEYS = os.path.join(ROOT_DIR, 'userfiles', KEYS)
