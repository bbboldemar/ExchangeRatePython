import requests

from logger import logger_wr_error, logger_wr_info, DATAFILE_data_update
from main import API_KEY1, API_KEY2, API_KEY3, API_KEY4, API_URL


def data_from_API_is_correct(data_from_API:list) -> bool:
    """ Checking for empty block of data.

    Args:
        data_from_API (list): list of dictionaries.

    Returns:
        bool: True if all data isn't empty;
        or bool: False if any data is None.
    """
    if any(block == None for block in data_from_API):
        return False
    return True


def switch_API_key(transaction_counter = [0]) -> str:
    """ Overcoming API restriction of 9 requests per minute.

    Args:
        - fake arg for switching between 4 keys.

    Returns:
        - str: API key ;
        - or str: "invalid"
        if all API 4 keys can't provide correct data.
    """
    if len(transaction_counter) == 1:
        key = API_KEY1
    if len(transaction_counter) == 2:
        key = API_KEY2
    if len(transaction_counter) == 3:
        key = API_KEY3
    if len(transaction_counter) == 4:
        key = API_KEY4
    if len(transaction_counter) == 5:
        key = None
        transaction_counter.clear()
    transaction_counter.append(1)
    print (key)
    return key


def load_data_from_API(currency:str, API_key:str = API_KEY4) -> dict:
    """ Loads data for given cryptocurrency in JSON format from 
    "api.twelvedata.com" till any given key is correct.
    
    Args:
        - currency (str): given cryptocurrency symbol;
        - API_key (str):
        default is API_KEY4, switches till all 4 keys are busted.

    Returns:
        - dict: dictionary with "str" keys and values;
        - or None if:
            - all 4 keys are busted;
            - API returns errors 500, 400, 404, 414.
    """
    if API_key == 'invalid':
            logger_wr_error('All 3 API keys are invalid')
            return None
    logger_wr_info('Updating')
    response = requests.get(API_URL.format(currency, switch_API_key()))
    if response.json()['status'] == "ok":    
        logger_wr_info('Successful update')   
        APIdata = {
            'currency_base': response.json()['meta']['currency_base'],
            'date_time': response.json()['values'][0]['datetime'],
            'cost': response.json()['values'][0]['close']
        }
        DATAFILE_data_update(APIdata)
        return APIdata
    else:
        if response.json()['code'] == 500:
            logger_wr_error('Error on the API-side. Try again later.')
            return None
        if response.json()['code'] == (400 or 414 or 404):
            logger_wr_error(response.json()['message'])
            return None
        if response.json()['code'] == (429 or 401):
            logger_wr_error(response.json()['message'])
            logger_wr_info('Switching API key')
            return load_data_from_API(currency, switch_API_key())