import os

CURRENCIES = ['SC','BTC']

API_URL = (
    'https://api.twelvedata.com/time_series?symbol={}/'
    'USD&interval=1min&outputsize=3&format=JSON&dp=5&'
    'timezone=Europe/Moscow&apikey={}'
    )

API_KEY1 = 'ab2a1285e34c4fa78173db8c5a9f6d5f'
API_KEY2 = '6d21950f1e80428391843b55ad20ae62'
API_KEY3 = 'af4ace33f1994561baeb9873123b53b4'
API_KEY4 = 'f7e12a1a4dd34faca920cdff2c088e2b'

SETTINGS = "exchanger_settings"
DATAFILE = "Price-History"
LOGFILE = "logfile.log"

ROOT_DIR = os.path.dirname(os.path.abspath('__main__'))
PATH_TO_DATAFILE = os.path.join(ROOT_DIR, 'userfiles', DATAFILE)
PATH_TO_SETTINGS = os.path.join(ROOT_DIR, 'userfiles', SETTINGS)
PATH_TO_LOGFILE = os.path.join(ROOT_DIR, 'userfiles', LOGFILE)
