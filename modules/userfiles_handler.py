import os

from modules.logger import logger_wr_info, logger_wr_error
from constants import PATH_TO_SETTINGS, PATH_TO_KEYS


def exchanger_settings_exist() -> bool:
    return os.path.exists(PATH_TO_SETTINGS)


def create_exchanger_settings_file() -> None:
    with open(PATH_TO_SETTINGS, "w") as f:
        f.write('subscription_disabled\n')


def check_exchanger_settings_subscription() -> bool:
    with open(PATH_TO_SETTINGS, 'r') as f:
        if f.readline() == 'subscription_enabled\n':
            return True


def disable_exchanger_settings_subscription():
    with open(PATH_TO_SETTINGS, 'w+') as f:
        f.writelines('subscription_disabled\n')
        logger_wr_info('Email subscription disabled')


def convert_exchanger_settings_target_rate() -> list[float, float]:
    """ Reads users target rates "exchanger_settings" file
    and converts them to float.

    Returns:
        - list[float, float]: converted rates:
        - or None if users target rates are incorrect.
    """
    with open(PATH_TO_SETTINGS, 'r') as f:
        try:
            get_all = f.readlines()
            return [
                float(get_all[3][:len(get_all[3])-1]), 
                float(get_all[4][:len(get_all[4])-1])
            ]
        except:
            logger_wr_error('Incorrect tagret price format')
            return None


def read_exchanger_settings_log_pass() -> tuple:
    """ Reads users email login and password
    thru "exchanger_settings" file.

    Returns:
        - tuple: (users login, users password);
        - or ('error', 'error') if users data doesn't exist.
    """
    try:
        with open(PATH_TO_SETTINGS, 'r') as f:
            get_all = f.readlines()
            return (
                get_all[1][:len(get_all[1])-1], 
                get_all[2][:len(get_all[1])-1]
            )
    except:
        logger_wr_error("Can't read login/password thru file")
        return ('error', 'error')


def write_exchanger_settings_data(address, password, SC_target, BC_target):
    """ Writes users input into "exchanger_settings" file
    and enables email subscription.

    Args:
        - address (str): users email address
        - password (str): users password address
        - SC_target (str): users target rate for SC
        - BC_target (str): users target rate BTC
    """
    with open(PATH_TO_SETTINGS, 'w') as f:
        f.writelines('subscription_enabled\n')
        f.writelines(address + '\n')
        f.writelines(password + '\n')
        f.writelines(SC_target + '\n')
        f.writelines(BC_target + '\n')
    logger_wr_info('Email subscription enabled')


def keys_read_API_key() -> str:
    with open(PATH_TO_KEYS, "r") as f:
        get_key = f.readline()
        return get_key[:len(get_key)-1]


def keys_switch_API_key() -> str:
    """ Overcoming API restriction of 8 requests per minute.

    Returns:
        - str: new API key.
    """
    with open(PATH_TO_KEYS, "r") as f:
        get_all = f.readlines()
    with open(PATH_TO_KEYS, "w+") as f:
        f.writelines(get_all[3])
        f.writelines(get_all[0])
        f.writelines(get_all[1])
        f.writelines(get_all[2])
        return f.readline()
