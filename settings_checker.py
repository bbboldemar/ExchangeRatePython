      
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

def settings_changer():
    with open("exchanger_settings",'r') as f:
            get_all = f.readlines()
    with open("exchanger_settings",'w') as f:
        for i,line in enumerate(get_all,1):
            if i == 1:
                f.writelines('subscription_enabled\n')
            else:
                f.writelines(line)

# print('Через пробел ведите логин и пароль от почты для подписки на email рассылку')
# user_data = input()
# f = open("exchanger_settings", "w")
# f.write(user_data)
# f.close()
# messagebox.showinfo ("You are subscribed now", "Yor login and password are: " + user_data)
# os.execv(sys.executable, ['python'] + sys.argv)