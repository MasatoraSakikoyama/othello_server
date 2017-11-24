# -*- coding: utf-8 -*-
from abc import ABCMeta
from collections import ChainMap

from django.db.transaction import atomic

from apps.entity.utils import bases_dict
from apps.entity.models import Game, Player, Turn
from apps.entity.caches import GameStatusCache, TurnStatusCache


def get_game_status(game_id):
    try:
        game = Game.objects.prefetch_related('player_set').get(id=game_id)
        game_status = {
            'game': game.serialized,
            'players': [p.serialized for p in game.player_set.all()],
        }
    except Game.DoesNotExist:
        game_status = {}

    return game_status


def get_turn_status(game_id):
    try:
        game = Game.objects.prefetch_related('turn_set').get(id=game_id)
        turn_status = {
            'game': game.serialized,
            'turns': [t.serialized for t in game.turn_set.all()],
        }
    except Game.DoesNotExist:
        turn_status = {}

    return turn_status


class DecolatorMeta(ABCMeta):
    def __new__(cls, name, bases, namespace):
        ns = ChainMap(namespace, *bases_dict(bases))
        namespace['multi_select'] = classmethod(ns['multi_select'])
        namespace['select'] = classmethod(ns['select'])
        namespace['insert'] = classmethod(atomic(ns['insert']))
        namespace['update'] = classmethod(atomic(ns['update']))
        namespace['delete'] = classmethod(atomic(ns['delete']))
        return super().__new__(cls, name, bases, namespace)


class BaseEntity(metaclass=DecolatorMeta):
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


class GameStatus(BaseEntity):
    def multi_select(cls, *args, **kwargs):
        where = kwargs.get('where')

        cache = GameStatusCache.get_many(where)
        if cache:
            return cache

        queryset = Game.objects.filter(**where) if where else Game.objects
        data_list = [{
                    'game': g.serialized,
                    'players': [p.serialized for p in g.player_set.all()],
                    } for g in
                    queryset
                    .prefetch_related('player_set')]

        for data in data_list:
            GameStatusCache.add(data['game']['id'], data)

        return data_list

    def select(cls, *args, **kwargs):
        game_id = kwargs['game_id']

        cache = GameStatusCache.get(game_id)
        if cache:
            return cache

        data = get_game_status(game_id)
        GameStatusCache.add(game_id, data)

        return data

    def insert(cls, *args, **kwargs):
        pass

    def update(cls, *args, **kwargs):
        pass

    def delete(cls, *args, **kwargs):
        pass


class TurnStatus(BaseEntity):
    def multi_select(cls, *args, **kwargs):
        where = kwargs.get('where')

        cache = TurnStatusCache.get_many(where)
        if cache:
            return cache

        queryset = Game.objects.filter(**where) if where else Game.objects
        data_list = [{
                    'game': g.serialized,
                    'turns': [t.serialized for t in g.turn_set.all()],
                    } for g in
                    queryset
                    .prefetch_related('turn_set')]

        for data in data_list:
            TurnStatusCache.add(data['game']['id'], data)

        return data_list

    def select(cls, *args, **kwargs):
        game_id = kwargs['game_id']

        cache = TurnStatusCache.get(game_id)
        if cache:
            return cache

        data = get_turn_status(game_id)
        TurnStatusCache.add(game_id, data)

        return data

    def insert(cls, *args, **kwargs):
        pass

    def update(cls, *args, **kwargs):
        pass

    def delete(cls, *args, **kwargs):
        pass


class Game(BaseEntity):
    def multi_select(cls, *args, **kwargs):
        pass

    def select(cls, *args, **kwargs):
        pass

    def insert(cls, *args, **kwargs):
        game_id = Game(**kwargs['data']).save().id

        game_status = get_game_status(game_id)
        GameStatusCache.add(game_id, game_status)

        turn_status = get_turn_status(game_id)
        TurnStatusCache.add(game_id, turn_status)

    def update(cls, *args, **kwargs):
        game_id = Game(**kwargs['data']).save().id

        game_status = get_game_status(game_id)
        GameStatusCache.set(game_id, game_status)

        turn_status = get_turn_status(game_id)
        TurnStatusCache.set(game_id, turn_status)

    def delete(cls, *args, **kwargs):
        game_id = kwargs['game_id']
        Game.objects.delete(id=game_id)
        GameStatusCache.delete(game_id)
        TurnStatusCache.delete(game_id)


class Player(BaseEntity):
    def multi_select(cls, *args, **kwargs):
        pass

    def select(cls, *args, **kwargs):
        pass

    def insert(cls, *args, **kwargs):
        game_id = Player(**kwargs['data']).save().game_id
        game_status = get_game_status(game_id)
        GameStatusCache.add(game_id, game_status)

    def update(cls, *args, **kwargs):
        game_id = Player(**kwargs['data']).save().game_id
        game_status = get_game_status(game_id)
        GameStatusCache.set(game_id, game_status)

    def delete(cls, *args, **kwargs):
        player_id = kwargs['player_id']
        game_id = Player.objects.get(id=player_id).game_id

        Player.objects.delete(id=player_id)

        game_status = get_game_status(game_id)
        GameStatusCache.set(game_id, game_status)

        turn_status = get_turn_status(game_id)
        TurnStatusCache.set(game_id, turn_status)


class Turn(BaseEntity):
    def multi_select(cls, *args, **kwargs):
        pass

    def select(cls, *args, **kwargs):
        pass

    def insert(cls, *args, **kwargs):
        game_id = Turn(**kwargs['data']).save().game_id
        turn_status = get_turn_status(game_id)
        TurnStatusCache.add(game_id, turn_status)

    def update(cls, *args, **kwargs):
        game_id = Turn(**kwargs['data']).save().game_id
        turn_status = get_turn_status(game_id)
        TurnStatusCache.set(game_id, turn_status)

    def delete(cls, *args, **kwargs):
        turn_id = kwargs['turn_id']
        game_id = Turn.objects.get(id=turn_id).game_id

        Turn.objects.delete(id=turn_id)

        turn_status = get_turn_status(game_id)
        TurnStatusCache.set(game_id, turn_status)
