import os

from logger import logger_wr_info
from main import PATH_TO_SETTINGS

def user_files_exist() -> bool:
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


def convert_target_price() -> list[float, float]:
    with open(PATH_TO_SETTINGS, 'r') as f:
        get_all = f.readlines()
        try: 
            return [float(get_all[3][:len(get_all[3])-1]), float(get_all[4][:len(get_all[4])-1])]
        except:
            return list()


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


def get_email_data() -> tuple:
    try:
        with open(PATH_TO_SETTINGS, 'r') as f:
            get_all = f.readlines()
            return get_all[1], get_all[2]
    except:
        return tuple()


def write_settings_data(address, password, SC_target, BC_target):
    with open(PATH_TO_SETTINGS, 'r') as f:
            get_all = f.readlines()
    with open(PATH_TO_SETTINGS, 'w') as f:
        for i,line in enumerate(get_all,1):
            if i == 2:
                f.writelines(address+ '\n')
            elif i == 3:
                f.writelines(password+ '\n')
            elif i == 4:
                f.writelines(SC_target+ '\n')
            elif i == 5:
                f.writelines(BC_target+ '\n')
            else:
                f.writelines(line)