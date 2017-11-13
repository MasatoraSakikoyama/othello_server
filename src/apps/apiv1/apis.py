# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.views.generic import View

from apps.apiv1.entities import GameStatus
from apps.apiv1.utils import datetime_default


class JSONView(View):
    http_method_names = ['get', 'post', 'put', 'delete']

    def json_response(self, data):
        return HttpResponse(
            json.dumps(data, default=datetime_default),
            content_type='application/json',
        )


class Initialize(JSONView):
    http_method_names = ['post']

    def post(self, request):
        data = GameStatus.multi_select()
        return self.json_response(data)


class Turn(JSONView):
    http_method_names = ['post']

    def post(self, request):
        data = GameStatus.select(game_id=1)
        return self.json_response(data)
