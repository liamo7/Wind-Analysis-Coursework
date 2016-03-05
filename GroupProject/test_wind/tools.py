__author__ = 'Brian'
import inspect


def debug(message):
    func = inspect.currentframe().f_back.f_code
    # # print(func.co_filename + ' - ' + func.co_name + ': ' + message)


def ifnull(var,val):
    if var is None:
        return val
    else:
        return var