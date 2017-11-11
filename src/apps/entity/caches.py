# -*- coding: utf-8 -*-
from abc import ABCMeta
from collections import ChainMap
from functools import wraps

from django.core.cache import cache

from apps.entity.utils import bases_dict


def cachehandler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cls = globals()[args[0].__name__]
        handler = getattr(cls, func.__name__)
        kwargs['cache_handler'] = handler
        return func(*args, **kwargs)
    return wrapper


class DecolatorMeta(ABCMeta):
    def __new__(mcls, name, bases, namespace):
        ns = ChainMap(namespace, *bases_dict(bases))
        namespace['_match'] = classmethod(ns['_match'])
        namespace['_key'] = classmethod(ns['_key'])
        namespace['multi_select'] = classmethod(ns['multi_select'])
        namespace['select'] = classmethod(ns['select'])
        namespace['insert'] = classmethod(ns['insert'])
        namespace['update'] = classmethod(ns['update'])
        namespace['delete'] = classmethod(ns['delete'])
        return super().__new__(mcls, name, bases, namespace)


class CacheModel(metaclass=DecolatorMeta):
    def _match(data, where):
        if where:
            return all([data.get(k) == v for k, v in where.items()])
        else:
            return True

    def _key(cls, *args, **kwargs):
        game_id = kwargs['game_id']
        return '{cls_name}_{id}'.format(
            cls_name=cls.__name__.lower(),
            id=game_id if game_id else '*',
        )

    def multi_select(cls, *args, **kwargs):
        keys = cache.keys(cls._key(*args, **kwargs))
        return [d for d in cache.get_many(keys)
                if cls._match(d, kwargs['where'])]

    def select(cls, *args, **kwargs):
        return cache.get(cls._key(*args, **kwargs))

    def insert(cls, *args, **kwargs):
        cache.add(cls._key(*args, **kwargs), kwargs['data'])

    def update(cls, *args, **kwargs):
        cache.set(cls._key(*args, **kwargs), kwargs['data'])

    def delete(cls, *args, **kwargs):
        cache.delete(cls._key(*args, **kwargs))


class GameStatus(CacheModel):
    pass


class TurnStatus(CacheModel):
    pass
