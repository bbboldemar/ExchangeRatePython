import requests

api_twelvedata = (
    'https://api.twelvedata.com/time_series?'
    'symbol={}/USD'
    '&interval=1min&'
    'outputsize=3&'
    'format=JSON&'
    'dp=5&'
    'timezone=Europe/Moscow&'
    'apikey=ab2a1285e34c4fa78173db8c5a9f6d5f'
    )
    # 'apikey=f7e12a1a4dd34faca920cdff2c088e2b'
    # )


def load_data_from_API(currency: str) -> tuple[str, str, str]:
    response = requests.get(api_twelvedata.format(currency))
    currency_base = response.json()['meta']['currency_base']
    date_time = response.json()['values'][0]['datetime']
    cost = response.json()['values'][0]['close']
    return (currency_base, date_time, cost)