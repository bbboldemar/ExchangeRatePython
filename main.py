from GUI import Windows
from settings_checker import first_launch_checker

if __name__ == "__main__":  
    if not first_launch_checker():
        create_root_window()
    else:
        create_first_launch_window()