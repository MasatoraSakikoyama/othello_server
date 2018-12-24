# -*- coding: utf-8 -*-
from functools import wraps
from datetime import datetime

from django.conf import settings
from django.http import JsonResponse

SESSION_KEY = 'user_id'
SESSION_EXPIRE = 7*24*60*60

def datetime_default(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(repr(o) + " is not JSON serializable")


def set_session(response, value):
    response.set_cookie(SESSION_KEY, value, SESSION_EXPIRE)


def check_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.user.is_authenticated:
            kwargs[SESSION_KEY] = request.user.id
            return func(*args, **kwargs)
        elif request.COOKIES.get(SESSION_KEY):
            kwargs[SESSION_KEY] = request.COOKIES.get(SESSION_KEY)
            return func(*args, **kwargs)
        else:
            return JsonResponse(status=401)
    return wrapper
