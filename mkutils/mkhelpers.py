# -*- coding: utf-8 -*-

"""
Generic Helper Functions
"""

import datetime
import configparser
import base64


def is_numeric(aval):
    """Checks via type() if aval is numeric or not.

    :param aval:
    :return: :boolean:
    """
    atyp = type(aval)
    if (atyp == datetime.datetime
        or atyp == datetime.time
        or atyp == datetime.date
        or atyp == int
        or atyp == float
        or atyp == complex
    ):
        return True
    else:
        return False


def is_string_numeric(aval, ignore_empty_string=True):
    """Checks if a string contains a numeric value

    :param aval:
    :param ignore_empty_string: If `True`, empt string will be tretaed as if it contains 0
    :return: :rtype:
    """
    if aval == '' or aval == '' and ignore_empty_string:
        return True
    try:
        float(aval)
        return True
    except ValueError:
        return False


def datetime_to_str(dt):
    """Converts a date/time value to string.

    :param dt:
    :return: :rtype:
    """

    _typ = type(dt)

    #todo: get format from locale settings
    if _typ == datetime.date:
        return dt.strftime('%d.%m.%Y')

    elif _typ == datetime.datetime:
        return dt.strftime('%d.%m.%Y %H:%M')

    elif _typ == datetime.time:
        return dt.strftime('%H:%M')

    else:
        return None


def current_year():
    return datetime.datetime.today().year


def current_month():
    return datetime.datetime.today().month


def current_date_as_str():
    dt = datetime.date.today()
    return dt.strftime('%d.%m.%Y')

def read_config_file(path):
    aconfig = configparser.ConfigParser()
    with open('%s/config.ini' % path, 'r', encoding='utf-8') as f:
        aconfig.read_file(f)

    return aconfig


def decode_config_base64(decoded_string):
    return base64.b64decode(decoded_string.encode("ascii")[2:-1]).decode("utf-8")


