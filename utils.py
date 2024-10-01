#print with timestamp
import datetime

def tprint(*args, **kwargs):
    print(datetime.datetime.now().strftime("%H:%M:%S"), *args, **kwargs)