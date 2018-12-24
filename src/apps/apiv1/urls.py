# -*- coding: utf-8 -*-
from django.conf.urls import url

from apps.apiv1.apis import init, game, turn

urlpatterns = [
    url(r'^init', init, name='init'),
    url(r'^game', game, name='game'),
    url(r'^turn', turn, name='turn'),
]
