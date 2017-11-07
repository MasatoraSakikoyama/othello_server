# -*- coding: utf-8 -*-
from abc import ABCMeta
from collections import ChainMap

from apps.apiv1.utils import require
from apps.apiv1.entities.caches import cachehandler
from apps.apiv1.entities.models import Game


def get_bases_dict(bases):
    dicts = []
    for base in bases:
        if hasattr(base, '__bases__') and hasattr(base, '__dict__'):
            dicts.append(base.__dict__)
            dicts.extend(get_bases_dict(base.__bases__))
    return dicts


class DecolatorMeta(ABCMeta):
    def __new__(mcls, name, bases, namespace):
        ns = ChainMap(namespace, *get_bases_dict(bases))
        namespace['multi_select'] = classmethod(
            cachehandler(ns['multi_select']),
        )
        namespace['select'] = classmethod(
            require(cachehandler(ns['select']), require_kwargs=['id']),
        )
        namespace['insert'] = classmethod(
            require(cachehandler(ns['insert']), require_kwargs=['id', 'data']),
        )
        namespace['update'] = classmethod(
            require(cachehandler(ns['update']), require_kwargs=['id', 'data']),
        )
        namespace['delete'] = classmethod(
            require(cachehandler(ns['delete']), require_kwargs=['id']),
        )
        return super().__new__(mcls, name, bases, namespace)


class BaseModel(metaclass=DecolatorMeta):
    def multi_select(cls, *args, **kwargs):
        raise NotImplementedError

    def select(cls, *args, **kwargs):
        raise NotImplementedError

    def insert(cls, *args, **kwargs):
        raise NotImplementedError

    def update(cls, *args, **kwargs):
        raise NotImplementedError

    def delete(cls, *args, **kwargs):
        raise NotImplementedError


class GameStatus(BaseModel):
    def multi_select(cls, *args, **kwargs):
        where = kwargs['where']
        cache = kwargs['cache_handler'](where=where)

        if cache:
            return cache
        else:
            if where:
                return [d.serialized for d in Game.objects.filter(**where).get()]
            else:
                return [d.serialized for d in Game.objects.all()]

    def select(cls, *args, **kwargs):
        id = kwargs['id']
        cache = kwargs['cache_handler'](id=id)

        if cache:
            return cache
        else:
            return Game.objects.get(id=id).serialized

    def insert(cls, *args, **kwargs):
        id = kwargs['id']
        data = kwargs['data']
        cache = kwargs['cache_handler'](id=id, data=data)

        if cache:
            return cache
        else:
            game = Game(id=id, **data)
            return game.save()

    def update(cls, *args, **kwargs):
        id = kwargs['id']
        data = kwargs['data']
        cache = kwargs['cache_handler'](id=id, data=data)

        if cache:
            return cache
        else:
            game = Game(id=id, **data)
            return game.save()

    def delete(cls, *args, **kwargs):
        id = kwargs['id']
        cache = kwargs['cache_handler'](id=id)

        if cache:
            return cache
        else:
            return Game.objects.delete(id=id)
