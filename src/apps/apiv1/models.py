# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.forms.models import model_to_dict
from django.contrib.auth.models import User

from django.conf import settings


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, null=False, blank=False)

    @property
    def serialized(self):
        return model_to_dict(self)

    class Meta:
        abstract = True


class Game(BaseModel):
    class Meta:
        db_table = 'game'


class Player(BaseModel):
    login_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    anonimous_user = models.CharField(max_length=128, null=True, blank=True)
    color = models.CharField(max_length=1, choices=(('w', 'white'), ('b', 'black')))
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    is_first = models.BooleanField(null=False, blank=False)
    is_winner = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = 'player'


class Turn(BaseModel):
    CHOICES = tuple([('{}{}'.format(x, y), '{}{}'.format(x, y))
                    for x in settings.X_AXIS
                    for y in settings.Y_AXIS]) + (('path', 'path'),)

    count = models.IntegerField(null=False, blank=False)
    axis = models.CharField(max_length=4, choices=CHOICES)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        db_table = 'turn'
