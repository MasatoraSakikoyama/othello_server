# -*- coding: utf-8 -*-
from abc import ABCMeta
from collections import ChainMap

from django.core.cache import cache

from apps.apiv1.utils import bases_dict


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


class BaseCache(metaclass=DecolatorMeta):
    def _match(data, where):
        if where:
            return all([data.get(k) == v for k, v in where.items()])
        else:
            return True

    def _key(cls, game_id):
        return '{cls_name}_{id}'.format(
            cls_name=cls.__name__.lower(),
            id=game_id if game_id else '*',
        )

    def get_many(cls, where):
        keys = cache.keys(cls._key())
        return [d for d in cache.get_many(keys)
                if cls._match(d, where)]

    def get(cls, game_id):
        return cache.get(cls._key(game_id))

    def add(cls, game_id, data):
        cache.add(cls._key(game_id), data)

    def set(cls, game_id, data):
        cache.set(cls._key(game_id), data)

    def delete(cls, game_id):
        cache.delete(cls._key(game_id))


class GameStatusCache(BaseCache):
    pass


class TurnStatusCache(BaseCache):
    pass
