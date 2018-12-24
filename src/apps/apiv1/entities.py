# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

from apps.apiv1.models import Game, Player, Turn


class BaseEntity(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def multi_select(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def select(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def insert(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def update(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def delete(cls, *args, **kwargs):
        raise NotImplementedError


class GameStatus(BaseEntity):
    @classmethod
    def multi_select(cls, *args, **kwargs):
        where = kwargs.get('where')

        queryset = Game.objects.filter(**where) if where else Game.objects
        data_list = [{
                    'game': g.serialized,
                    'players': [p.serialized for p in g.player_set.all()],
                    } for g in
                    queryset
                    .prefetch_related('player_set')]

        return data_list

    @classmethod
    def select(cls, *args, **kwargs):
        game_id = kwargs['game_id']
        try:
            game = Game.objects.prefetch_related('player_set').get(id=game_id)
            data = {
                'game': game.serialized,
                'players': [p.serialized for p in game.player_set.all()],
            }
        except Game.DoesNotExist:
            data = {}

        return data

    @classmethod
    def insert(cls, *args, **kwargs):
        pass

    @classmethod
    def update(cls, *args, **kwargs):
        pass

    @classmethod
    def delete(cls, *args, **kwargs):
        pass


class TurnStatus(BaseEntity):
    @classmethod
    def multi_select(cls, *args, **kwargs):
        where = kwargs.get('where')

        queryset = Game.objects.filter(**where) if where else Game.objects
        data_list = [{
                    'game': g.serialized,
                    'turns': [t.serialized for t in g.turn_set.all()],
                    } for g in
                    queryset
                    .prefetch_related('turn_set')]

        return data_list

    @classmethod
    def select(cls, *args, **kwargs):
        game_id = kwargs['game_id']
        try:
            game = Game.objects.prefetch_related('turn_set').get(id=game_id)
            data = {
                'game': game.serialized,
                'turns': [t.serialized for t in game.turn_set.all()],
            }
        except Game.DoesNotExist:
            data = {}

        return data

    @classmethod
    def insert(cls, *args, **kwargs):
        pass

    @classmethod
    def update(cls, *args, **kwargs):
        pass

    @classmethod
    def delete(cls, *args, **kwargs):
        pass
