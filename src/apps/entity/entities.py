# -*- coding: utf-8 -*-
from abc import ABCMeta
from collections import ChainMap

from django.db.transaction import commit_on_success

from apps.entity.utils import bases_dict
from apps.entity.caches import cachehandler
from apps.entity.models import Game, Player, Turn


class DecolatorMeta(ABCMeta):
    def __new__(cls, name, bases, namespace):
        ns = ChainMap(namespace, *bases_dict(bases))
        namespace['multi_select'] = classmethod(
            cachehandler(ns['multi_select']),
        )
        namespace['select'] = classmethod(
            cachehandler(ns['select']),
        )
        namespace['insert'] = classmethod(
            commit_on_success(
                cachehandler(ns['insert']),
            ),
        )
        namespace['update'] = classmethod(
            commit_on_success(
                cachehandler(ns['update']),
            ),
        )
        namespace['delete'] = classmethod(
            commit_on_success(
                cachehandler(ns['delete']),
            ),
        )
        return super().__new__(cls, name, bases, namespace)


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
    @classmethod
    def _save(cls, *args, **kwargs):
        game = Game(**kwargs['game']).save().sirealized
        players = [Player(**p).save().sirealized for p in kwargs['palyers']]
        kwargs['cache_handler'](data={
            'game': game,
            'players': players,
        })

    def multi_select(cls, *args, **kwargs):
        where = kwargs['where']
        cache = kwargs['cache_handler'](where=where)

        if cache:
            return cache
        elif where:
            return [g.serialized for g in
                    Game
                    .objects
                    .filter(**where)
                    .select_related('player__user')]
        else:
            return [g.serialized for g in
                    Game
                    .objects
                    .select_related('player__user')]

    def select(cls, *args, **kwargs):
        game_id = kwargs['game_id']
        cache = kwargs['cache_handler'](id=game_id)

        if cache:
            return cache
        else:
            return (Game
                    .objects
                    .filter(id=game_id)
                    .select_related('player__user')
                    .serialized)

    def insert(cls, *args, **kwargs):
        cls._save(*args, **kwargs)

    def update(cls, *args, **kwargs):
        cls._save(*args, **kwargs)

    def delete(cls, *args, **kwargs):
        game_id = kwargs['game_id']
        Game.objects.delete(id=game_id)
        kwargs['cache_handler'](id=game_id)


class TurnStatus(BaseModel):
    @classmethod
    def _save(cls, *args, **kwargs):
        game = Game(**kwargs['game']).save().sirealized
        players = [Player(**p).save().sirealized for p in kwargs['palyers']]
        kwargs['cache_handler'](game_id=game['id'], data={
            'game': game,
            'players': players,
        })

    def multi_select(cls, *args, **kwargs):
        where = kwargs['where']
        cache = kwargs['cache_handler'](game_id=None, where=where)

        if cache:
            return cache
        elif where:
            return [t.serialized for t in
                    Turn
                    .objects
                    .filter(**where)
                    .select_related('player__user')]
        else:
            return [t.serialized for t in
                    Turn
                    .objects
                    .select_related('player__user')]

    def select(cls, *args, **kwargs):
        game_id = kwargs['game_id']
        cache = kwargs['cache_handler'](id=game_id)

        if cache:
            return cache
        else:
            game = Game.objects.get(id=game_id)
            turns = [t.serialized for t in
                     Turn
                     .objects
                     .filter(game__id=game_id)
                     .select_related('player__user')]
            return {
                'game': game,
                'turns': turns,
            }

    def insert(cls, *args, **kwargs):
        cls._save(*args, **kwargs)

    def update(cls, *args, **kwargs):
        cls._save(*args, **kwargs)

    def delete(cls, *args, **kwargs):
        game_id = kwargs['game_id']
        Turn.objects.filter(game__id=game_id).delete()
        kwargs['cache_handler'](id=game_id)
