import os

from logger import logger_wr_info
from main import PATH_TO_SETTINGS

def user_files_exist() -> bool:
    logger_wr_info('Start')
    print (os.path.exists(PATH_TO_SETTINGS))
    return os.path.exists(PATH_TO_SETTINGS)

def create_default_user_files() -> None:
    f = open(PATH_TO_SETTINGS, "w")
    f.write('subscription_disabled\nNone\nNone\nNone\nNone\n')
    f.close()
    logger_wr_info('First launch')


def check_user_is_subscribed() -> bool:
    try:
        with open(PATH_TO_SETTINGS, 'r') as f:
            checker = f.readline()
            if checker == 'subscription_enabled\n':
                return True
            else:
                return False
    except:
        return None


def convert_target_rate() -> list[float, float]:
    """ Reads users target rates "exchanger_settings" file
    and converts them to float.

    Returns:
        - list[float, float]: converted rates:
        - or None if users target rates are incorrect.
    """
    with open(PATH_TO_SETTINGS, 'r') as f:
        try :
            get_all = f.readlines()
            return [float(get_all[3][:len(get_all[3])-1]), float(get_all[4][:len(get_all[4])-1])]           
        except:
            return None


def switch_subscription(status: bool):
    with open(PATH_TO_SETTINGS, 'r') as f:
            get_all = f.readlines()
    with open(PATH_TO_SETTINGS, 'w') as f:
        for i,line in enumerate(get_all,1):
            if i == 1:
                if status:
                    f.writelines('subscription_enabled\n')
                    logger_wr_info('Email subscription enabled')
                else:
                    f.writelines('subscription_disabled\n')
                    logger_wr_info('Email subscription disabled')
            else:
                f.writelines(line)


def read_user_log_pass() -> tuple:
    """ Reads users email login and password
    thru "exchanger_settings" file.

    Returns:
        - tuple: (users login, users password);
        - or tuple: ('', '') if users data doesn't exist.
    """
    try:
        with open(PATH_TO_SETTINGS, 'r') as f:
            get_all = f.readlines()
            return get_all[1], get_all[2]
    except:
        return ('', '')


def write_settings_data(address, password, SC_target, BC_target):
    """ Writes users input into "exchanger_settings" file
    and enables email subscription.

    Args:
        - address (str): users email address
        - password (str): users password address
        - SC_target (str): users target rate for SC
        - BC_target (str): users target rate BTC
    """
    with open(PATH_TO_SETTINGS, 'w') as f:
        logger_wr_info('Email subscription enabled')
        f.writelines('subscription_enabled\n')
        f.writelines(address+ '\n')
        f.writelines(password+ '\n')
        f.writelines(SC_target+ '\n')
        f.writelines(BC_target+ '\n')