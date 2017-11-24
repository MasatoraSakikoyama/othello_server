# -*- coding: utf-8 -*-
import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import View

from apps.session.utils import datetime_default, create_jwt, check_jwt


class JSONView(View):
    http_method_names = ['get', 'post', 'put', 'delete']

    def json_response(self, status, data):
        return HttpResponse(
            status=status,
            content=json.dumps(data, default=datetime_default),
            content_type='application/json',
        )


class Account(JSONView):
    http_method_names = ['post', 'put']

    def post(self, request):
        data = request.POST
        user = User.objects.create_user(
            data['user_id'],
            data['email'],
            data['password'],
        )
        user.save()
        return self.json_response(200, {'message': 'success'})

    @check_jwt
    def put(self, request, user_id):
        data = request.POST
        user = authenticate(
            user_id=data.get('user_id'),
            password=data.get('password'),
        )
        if user:
            username = data.get('username')
            new_password = data.get('new_password')
            if username:
                user.username = username
            if new_password:
                user.set_password(new_password)
            user.save()
            return self.json_response(200, {'message': 'success'})
        else:
            return self.json_response(400, {'message': 'Invalid param'})


class Authenticate(JSONView):
    http_method_names = ['post']

    def post(self, request):
        data = request.POST
        user = authenticate(
            user_id=data.get('user_id'),
            password=data.get('password'),
        )
        if user:
            token = create_jwt(data['user_id'])
            return self.json_response(200, {'token': token.decode('ascii')})
        else:
            return self.json_response(400, {'message': 'Invalid param'})


class Unauthenticate(JSONView):
    http_method_names = ['post']

    @check_jwt
    def post(self, request, user_id):
        token = create_jwt(user_id, expire=-1)
        return self.json_response(200, {'token': token.decode('ascii')})
