# -*- coding: utf-8 -*-
import json

from django.db import models
from django.forms.models import model_to_dict
from django.contrib.auth.models import User

from apps.entity.utils import datetime_default


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, null=False, blank=False)

    @property
    def serialized(self):
        data = model_to_dict(self)
        return json.dumps(data, default=datetime_default)

    class Meta:
        abstract = True


class UserProfile(BaseModel):
    user = models.OneToOneField(User)
    image = models.ImageField()

    class Meta:
        db_table = 'user_profile'


class Game(BaseModel):
    winner = models.ForeignKey(Player, on_delete=models.DO_NOTHING, related_query_name='game')
    first = models.ForeignKey(Player, on_delete=models.DO_NOTHING, related_query_name='game')
    second = models.ForeignKey(Player, on_delete=models.DO_NOTHING, related_query_name='game')

    class Meta:
        db_table = 'game'


class Turn(BaseModel):
    X_AXIS = (
        ('a', 'a'),
        ('b', 'b'),
        ('c', 'c'),
        ('d', 'd'),
        ('e', 'e'),
        ('f', 'f'),
        ('d', 'd'),
        ('h', 'h'),
    )
    Y_AXIS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
    )

    count = models.IntegerField(null=False, blank=False)
    x_axis = models.CharField(choices=X_AXIS, null=False, blank=False)
    y_axis = models.CharField(choices=Y_AXIS, null=False, blank=False)
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, related_query_name='turn')
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING, related_query_name='turn')

    class Meta:
        db_table = 'turn'
