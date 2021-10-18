def subscription_checker():
    f = open("exchanger_settings", "r")
    checker = f.readline()
    try:
        if checker == 'subscription_enabled\n':
            status = True
        else:
            status = False
    except:
        status = False               
    f.close()
    return status

def target_price_checker():
    with open("exchanger_settings",'r') as f:
        get_all = f.readlines()
        return [float(get_all[3][:len(get_all[3])-1]), float(get_all[4][:len(get_all[4])-1])]

def subscription_switcher(status):
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

def price_history_update(currency_base, date_time, cost):
    with open("price_history",'a') as f:
        f.write('at ' + date_time + ' ' + currency_base + ' value is ' + cost + '\n')


# print(target_price_checker())