# -*- coding: utf-8 -*-
from django.http import JsonResponse

from apps.apiv1.forms import GameForm, PlayerForm, TurnForm
from apps.apiv1.logics import game_list
from apps.session.utils import check_session


@check_session
def games(request, user_id):
    if request.method == 'GET':
        try:
            return JsonResponse(game_list(user_id), status=200)
        except Exception as e:
            return JsonResponse(status=404)
    else:
        return JsonResponse(status=405)

@check_session
def game(request, user_id):
    if request.method == 'GET':
        game_id = request.GET.get('gid')
        if game_id is None:
            return JsonResponse(status=404)
        try:
            return JsonResponse(game(game_id), status=200)
        except Exception as e:
            return JsonResponse(status=404)
    elif request.method == 'POST':
        game_form = GameForm(request.POST.get('game'))
        game_model = game_form.save()
        
        return JsonResponse(game_model.serialized, status=200)
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
    else:
        return JsonResponse(status=405)
