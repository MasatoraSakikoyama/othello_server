# -*- coding: utf-8 -*-
from functools import wraps
from datetime import datetime


def datetime_default(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(repr(o) + " is not JSON serializable")


def require(func, require_args=None, require_kwargs=None):
    """
    Usage:
        >>> @require(require_args=[0, 1], require_kwargs=['c', 'd', 'e'])
        ... def test(a, b, c=None, d=4, e=None):
        ...     pass
        ...
        >>> test(1, 2, c=3)
        TypeError: require kwargs['e']
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if require_args and type(require_args) == list:
            for i in require_args:
                try:
                    if not args[i]:
                        raise TypeError
                except (IndexError, TypeError):
                    raise TypeError('require args[{}]'.format(i))
        else:
            TypeError('require is invalid argument')

        if require_kwargs and type(require_kwargs) == list:
            for k in require_kwargs:
                try:
                    if not kwargs[k]:
                        raise TypeError
                except (KeyError, TypeError):
                    raise TypeError("require kwargs['{}']".format(k))
        else:
            TypeError('require is invalid argument')

        return func(*args, **kwargs)
    return wrapper
