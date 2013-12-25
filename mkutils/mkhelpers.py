# -*- coding: utf-8 -*-

"""
Generic Helper Functions

__author__ : Çağatay Tengiz
__date__   : 25.12.2013
"""

import datetime


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


def format_date(dt, _typ):
    """
    Bu metod json için tarih'i string'e çevirir.
    TODO : Localization'a göre formatı ayarla
    """
    if (_typ == datetime.date) and (dt):
        return dt.strftime('%d.%m.%Y')
    elif _typ == datetime.datetime:
        return dt.strftime('%d.%m.%Y %H:%M')
    elif _typ == datetime.time:
        return dt.strftime('%H:%M')
    else:
        return None

