# -*- coding: utf-8 -*-
from functools import wraps

from django.core.cache import cache


def cachehandler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        handler = globals()[args[0].__name__].dispatch(func.__name__)
        kwargs['cache_handler'] = handler
        return func(*args, **kwargs)
    return wrapper


def cachekey(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        id = kwargs.get('id')
        key = '{class_name}_{id}'.format(
            class_name=args[0].__name__,
            id=id if id else '*',
        )
        kwargs['key'] = key
        return func(*args, **kwargs)
    return wrapper


def match(data, where):
    return all([data.get(k) == v for k, v in where.items()]) if where else True


class CacheModel:
    @classmethod
    def dispatch(cls, method=None):
        return getattr(cls, method)

    @classmethod
    @cachekey
    def multi_select(cls, *args, **kwargs):
        keys = cache.keys(kwargs['key'])
        return [d for d in cache.get_many(keys) if match(d, kwargs['where'])]

    @classmethod
    @cachekey
    def select(cls, *args, **kwargs):
        import socket
        return cache.get(kwargs['key'])

    @classmethod
    @cachekey
    def insert(cls, *args, **kwargs):
        return cache.add(kwargs['key'], kwargs['data'])

    @classmethod
    @cachekey
    def update(cls, *args, **kwargs):
        return cache.set(kwargs['key'], kwargs['data'])

    @classmethod
    @cachekey
    def delete(cls, *args, **kwargs):
        return cache.delete(kwargs['key'])


class GameStatus(CacheModel):
    pass
