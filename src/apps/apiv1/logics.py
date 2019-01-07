# -*- coding: utf-8 -*-
from itertools import groupby

from django.db.models import Prefetch

from apps.entity.models import GameModel, PlayerModel, TurnModel


def game_list(user_id, limit=10):
    def _serialize(game, playeres):
        g = game.serialized
        g.playeres = [p.serialized for p in playeres]
        return g

    prefetch = Prefetch('player_set', queryset=PlayerModel.objects.filter(player_id=user_id))
    games = GameModel.objects.prefetch_related(prefetch).all()[limit]
    playeres = PlayerModel.objects.filter(game__in=games)
    return [_serialize(k, v) for k, v in groupby(playeres, key=lambda x: x.game)]

def game(game_id):
    game = GameModel.objects.prefetch_related('player_set', 'turn_set').get(game_id=game_id)
    g = game.serialized
    g.playeres = [p.serialized for p in game.player_set.all()]
    g.turns = [t.serialized for t in game.turn_set.all()]
    return g
