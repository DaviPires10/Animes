from threading import Thread

import requests

class Settings:
    """ AnimeFire global app configuration """    
    
    APP_NAME = "AnimeFire"
    APP_ICON = "/images/app.ico"
    VERSION = "1.0"
    AUTHOR = "1.0"
    YEAR = "2024"
    
    WIDTH = 580  # window size when starting the app
    HEIGHT = 700

def run_in_thread(func):
    def wrapper(*args, **kwargs):           
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
    return wrapper

