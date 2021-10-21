def user_files_exist() -> bool:
    try:
        with open("exchanger_settings", 'r') as f:
            f.readlines()
            return True
    except:
        return False


def create_user_files() -> None:
    f = open("exchanger_settings", "w")
    f.write('subscription_disabled\nNone\nNone\nNone\nNone\n')
    f.close()
    f = open("price_history", "w")
    f.close()
    
    
def user_is_subscribed_checker() -> bool:
    with open("exchanger_settings",'r') as f:
        checker = f.readline()
        if checker == 'subscription_enabled\n':
            return True
        else:
            return False


def target_price_checker() -> list[float, float]:
    with open("exchanger_settings",'r') as f:
        get_all = f.readlines()
        return [float(get_all[3][:len(get_all[3])-1]), float(get_all[4][:len(get_all[4])-1])]


def subscription_switcher(status: str):
    with open("exchanger_settings",'r') as f:
            get_all = f.readlines()
    with open("exchanger_settings",'w') as f:
        for i,line in enumerate(get_all,1):
            if i == 1:
                if status == "enable":
                    f.writelines('subscription_enabled\n')
                else:
                    f.writelines('subscription_disabled\n')
            else:
                f.writelines(line)


def get_email_data():
    with open("exchanger_settings",'r') as f:
        get_all = f.readlines()
        return get_all[1], get_all[2]


def settings_data_changer(address, password, SC_target, BC_target):
    with open("exchanger_settings",'r') as f:
            get_all = f.readlines()
    with open("exchanger_settings",'w') as f:
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


