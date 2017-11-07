# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import View

from apps.apiv1.entities import GameStatus


class JSONView(View):
    http_method_names = ['get', 'post', 'put', 'delete']

    def json_response(self, data):
        return HttpResponse(data, content_type='application/json')


class Initialize(JSONView):
    http_method_names = ['post']

    def post(self, request):
        data = GameStatus.select(id=1)
        return self.json_response(data)


class Turn(JSONView):
    http_method_names = ['post']

    def post(self, request):
        data = GameStatus.select(id=1)
        return self.json_response(data)
