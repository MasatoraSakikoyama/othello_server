# -*- coding: utf-8 -*-
from django.conf.urls import url

from apps.apiv1.apiv1s import games, game, turn

urlpatterns = [
    url(r'^/games', games, name='games'),
    url(r'^/game', game, name='game'),
]
