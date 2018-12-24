# -*- coding: utf-8 -*-
from django.http import JsonResponse

from apps.apiv1.entities import GameStatus
from apps.session.utils import check_session


@check_session
def init(request, user_id):
    if request.method == 'GET':
        return JsonResponse(GameStatus.multi_select(), status=200)
    else:
        return JsonResponse(status=405)


@check_session
def game(request, user_id):
    if request.method == 'GET':
        return JsonResponse(GameStatus.select(game_id=1), status=200)

    elif request.method == 'POST':
        return JsonResponse(GameStatus.select(game_id=1), status=200)
    else:
        return JsonResponse(status=405)


@check_session
def turn(request, user_id):
    if request.method == 'GET':
        return JsonResponse(GameStatus.select(game_id=1), status=200)
    else:
        return JsonResponse(status=405)
