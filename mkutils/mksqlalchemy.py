# -*- coding: utf-8 -*-

"""
Helper functions for sqlalchemy

__author__ : Çağatay Tengiz
__date__   : 25.12.2013
"""

import json
import datetime
from mkutils.mkhelpers import datetime_to_str
from sqlalchemy.types import String, Text
import sqlalchemy


def sa_to_json(obj):
    """
    Converts an sqlalchemy query result set to json.

    Example usage ::
        q = session.query(Amodel).all()
        json_result = sa_to_json(q)

    :param obj: Source result set
    :return: :str: Result json string
    """
    return json.dumps(sa_to_dict(obj))


def sa_row_to_dict(row, convert_to_str=False):
    row_dict = {}

    for fld in dir(row):
        if fld[:2] != '__' and fld[:4] != '_sa_' and fld != "_decl_class_registry":
            _attr = getattr(row, fld)

            if (isinstance(_attr, str) or
                    isinstance(_attr, bool)):
                row_dict[fld] = _attr

            elif (isinstance(_attr, datetime.date) or
                      isinstance(_attr, datetime.time) or
                      isinstance(_attr  , datetime.datetime)):
                row_dict[fld] = datetime_to_str(_attr)

            elif isinstance(_attr, type(None)):
                row_dict[fld] = None

            elif (isinstance(_attr, int) or isinstance(_attr, float)):
                if convert_to_str:
                    row_dict[fld] = str(_attr)
                else:
                    row_dict[fld] = str(_attr)

    return row_dict



def sa_to_dict(obj, convert_to_str=False, return_in_array=True):
    """
    Converts an sqlalchemy query result set array of dicts.

    Example usage ::
        q = session.query(Amodel).all()
        json_result = sa_to_json(q)

    :param obj: Sqlalchemy result set
    :return: :array: Array of dicts.
    """
    source_array = []
    result_array = []

    if isinstance(obj, list):
        source_array = obj[:]
    else:
        source_array.append(obj)

    for row in source_array:
        row_dict = sa_row_to_dict(row, convert_to_str)

        result_array.append(row_dict)

    if result_array.__len__() == 1 and not return_in_array:
        return result_array[0]
    else:
        return result_array


def formdata_to_sa(data, atbl, arec):
    """
    Maps contents of a html request data (get / post) to fields (members) of a SqlAlchemy mapping class.
    Posted html controls' names should be the same with the class' members.

    :param data: Form data from bottle.request or compatible dict object
    :param atbl: Mapping SqlAlchemy class
    :param arec: Result record
    """
    if not arec:
        arec = atbl()

    for fld in data:
        if data[fld] == '':
            data[fld] = None
        if fld in atbl.__mapper__.columns:
            atype = atbl.__mapper__.columns[fld].type
            if isinstance(atype, String) \
                    and not isinstance(atype, Text)\
                    and data[fld]:
                data[fld] = data[fld][:atbl.__mapper__.columns[fld].type.length]
            setattr(arec, fld, data[fld])


def print_sql():
    """
    Print
    """
    pass

