from datetime import datetime
import logging
logging.basicConfig(filename="logfile.log", level=logging.INFO)
      
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


    