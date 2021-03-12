# -*- coding: utf-8 -*-

def field_exists(dict, fields):
    if dict is None:
        return False

    for field in fields:
        if field not in dict or dict[field] is None:
            return False

    return True

