from modules.logger import logger_wr_error, logger_wr_info
from modules.gui import create_root_window
from modules import install_and_import
from modules.userfiles_handler import (
    exchanger_settings_exist,
    create_exchanger_settings_file
)


def requests_installed_check():
    try:
        import requests
    except:
        install = input(
            'Install Requests — 3-rd party library for Python (Y/N)?')
        if install in ["y", "Y", ""]:
            install_and_import('requests')
            logger_wr_info('Installed "requests" library')
        else:
            print('Exit')
            raise quit()


if __name__ == "__main__":
    logger_wr_info('Start')
    requests_installed_check()
    if not exchanger_settings_exist():
        logger_wr_info('First launch')
        create_exchanger_settings_file()
        create_root_window(True)
    else:
        logger_wr_info('Welcome back')
        create_root_window(False)
