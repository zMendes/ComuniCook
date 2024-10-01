# print with timestamp
import datetime


def tprint(*args, **kwargs):
    print(datetime.datetime.now().strftime("%H:%M:%S"), *args, **kwargs)


class Items():
    OVEN = "oven"
    SUPER_OVEN = "super_oven"
    PLATE_TABLE = "plate_table"
    BACON = "bacon"
