import datetime


def tprint(*args, **kwargs):
    formatted_args = [f"{int(arg)}" if isinstance(
        arg, (float, int)) else arg for arg in args]
    print(datetime.datetime.now().strftime(
        "%H:%M:%S"), *formatted_args, **kwargs)


class Items():
    OVEN = "oven"
    SUPER_OVEN = "super_oven"
    PLATE_TABLE = "plate_table"
    BACON = "bacon"
    ASSISTANT = "assistant"
