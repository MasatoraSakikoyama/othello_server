# -*- coding: utf-8 -*-
from apps.session.apis import JSONView
from apps.session.utils import check_jwt
from apps.entity.entities import GameStatus


class Initialize(JSONView):
    http_method_names = ['post']

    @check_jwt
    def post(self, request, user_id):
        return self.json_response(200, GameStatus.multi_select())


class Turn(JSONView):
    http_method_names = ['post']

    @check_jwt
    def post(self, request, user_id):
        return self.json_response(200, GameStatus.select(game_id=1))
