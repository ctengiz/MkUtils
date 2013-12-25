# -*- coding: utf-8 -*-

"""
Helper functions for sqlalchemy

__author__ : Çağatay Tengiz
__date__   : 25.12.2013
"""

import json
import datetime
from mkutils.mkhelpers import format_date


def sa_to_json(obj):
    """Converts an sqlalchemy query result set to json.
    Example usage ::
        q = session.query(Amodel).all()
        json_result = sa_to_json(q)

    :param obj: Source result set
    :return: :rtype: Result json string
    """
    return json.dumps(sa_to_dict(obj))


def sa_to_dict(obj):
    """Converts an sqlalchemy query result set array of dicts.
    This functions tries

    Example usage ::
        q = session.query(Amodel).all()
        json_result = sa_to_json(q)

    :param obj: Sqlalchemy result set
    :return: :array:
    """
    source_array = []
    result_array = []

    if isinstance(obj, list):
        source_array = obj[:]
    else:
        source_array.append(obj)

    for row in source_array:
        row_dict = {}
        for item in row.__dict__.items():
            if item[0][0] is '_':
                continue
            if item[0] is 'session':
                continue
            if (
                    isinstance(item[1], datetime.date)
                    or isinstance(item[1], datetime.time)
                    or isinstance(item[1], datetime.datetime)
            ):
                row_dict[item[0]] = format_date(item[1], type(item[1]))
            elif isinstance(item[1], list):
                continue
                #row_dict[item[0]] = sa_to_dict(item[1])
            else:
                #print item[0], item[1]
                if item[1]:
                    row_dict[item[0]] = item[1]
                else:
                    row_dict[item[0]] = ''
        result_array.append(row_dict)

    if result_array.__len__() == 1:
        return result_array[0]
    else:
        return result_array






