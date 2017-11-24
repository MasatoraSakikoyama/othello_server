# -*- coding: utf-8 -*-
from functools import wraps
from datetime import datetime


def bases_dict(bases):
    dicts = []
    for base in bases:
        if hasattr(base, '__bases__') and hasattr(base, '__dict__'):
            dicts.append(base.__dict__)
            dicts.extend(bases_dict(base.__bases__))
    return dicts
