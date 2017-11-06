# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.views.generic import View


class JSONView(View):
    http_method_names = ['get', 'post', 'put', 'delete']

    def json_response(self, data_to_dump):
        # Todo: datetime type is not compatible
        data = json.dumps(data_to_dump)
        return HttpResponse(data, content_type='application/json')


class Initialize(JSONView):
    http_method_names = ['post']

    def post(self, request):
        return self.json_response({'test': 'test'})


class Turn(JSONView):
    http_method_names = ['post']

    def post(self, request):
        return self.json_response({'test': 'test'})
