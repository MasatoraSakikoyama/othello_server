# -*- coding: utf-8 -*-
from functools import wraps
from datetime import datetime

import jwt
from django.conf import settings
from django.http import HttpResponse


def datetime_default(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(repr(o) + " is not JSON serializable")


def create_jwt(user_id, expire=3600):
    now = datetime.utcnow()
    payload = {
        'nbf': now,
        'exp': now + timedelta(seconds=expire),
        'user_id': user_id,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def check_jwt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            user_id = jwt.decode(
                args[0].META['HTTP_AUTHORIZATION'],
                settings.SECRET_KEY,
                algorithms=['HS256']
            ).get('user_id')

            if user_id:
                args[1] = user_id
            else:
                raise
        except:
            return HttpResponse(status=401)
        return func(*args, **kwargs)
    return wrapper
