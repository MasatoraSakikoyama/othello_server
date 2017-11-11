# -*- coding: utf-8 -*-
from abc import ABCMeta
from collections import ChainMap
from functools import wraps

from django.core.cache import cache

from apps.entity import get_bases_dict


def cachehandler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cls = globals()[args[0].__name__]
        handler = getattr(cls, func.__name__)
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


class DecolatorMeta(ABCMeta):
    def __new__(mcls, name, bases, namespace):
        ns = ChainMap(namespace, *get_bases_dict(bases))
        namespace['multi_select'] = classmethod((ns['multi_select']))
        namespace['select'] = classmethod(cachekey(ns['select']))
        namespace['insert'] = classmethod(cachekey(ns['insert']))
        namespace['update'] = classmethod(cachekey(ns['update']))
        namespace['delete'] = classmethod(cachekey(ns['delete']))
        return super().__new__(mcls, name, bases, namespace)


class CacheModel(metaclass=DecolatorMeta):
    @classmethod
    @cachekey
    def multi_select(cls, *args, **kwargs):
        keys = cache.keys(kwargs['key'])
        return [d for d in cache.get_many(keys) if match(d, kwargs['where'])]

    @classmethod
    @cachekey
    def select(cls, *args, **kwargs):
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
