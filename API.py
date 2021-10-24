import requests

from logger import logger_wr_error, logger_wr_info, DATAFILE_data_update
from main import API_KEY1, API_KEY2, API_KEY3, API_URL, CURRENCIES

def all_data_from_API_is_correct(data_from_API:list) -> bool:
    for block in data_from_API:
        if len (block.values()) != 0:
            return True
        return False


def switch_API_key(counter = []) -> str:
    """
    Fake arg for switching between 2 keys
    if API limit of 9 request/minute is reached.
    """
    if len(counter) %2 == 0:
        new_key = API_KEY2
    else:
        new_key = API_KEY1
    counter.append(1)
    if len(counter) %2 == 0:
        counter.clear()
    return new_key


def load_data_from_API(currency: str, API_key:str = API_KEY3) -> dict:
    '''
    Load data in JSON format from "api.twelvedata.com"
    and return dictionary with "str" values.
    '''
    response = requests.get(API_URL.format(currency, API_key))
    if response.json()['status'] == "ok":    
        logger_wr_info('Successful update')   
        APIdata = {
            'currency_base': response.json()['meta']['currency_base'],
            'date_time': response.json()['values'][0]['datetime'],
            'cost': response.json()['values'][0]['close']
        }
        DATAFILE_data_update(APIdata)
        return (APIdata)
    else:
        if response.json()['code'] == 400:
            logger_wr_error('Requested type of currency N/A')
            return dict()
        if response.json()['code'] == 429:
            logger_wr_error('API key limit')
            return dict()

# if __name__ == '__main__':
#     def test_errors():
#         'API test launch'
        
#         print ("API test")
#         print('logfile line: 1 INFO, DATAFILE line: 1', 
#             load_data_from_API('BTC')
#         )
#         print('logfile line: 2 INFO, DATAFILE line: 2', 
#             load_data_from_API('SC')
#         )
#         API_call_limit = (x for x in range(3, 10))
#         for x in API_call_limit:
#             load_data_from_API('TESTFAIL')
#             if x != 9:
#                 print('logfile line:', x, 'ERROR wrong currency')
#             else:
#                 print('logfile line:', x, 'ERROR API limit')
#   test_errors()
