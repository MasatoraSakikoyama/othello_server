# -*- coding: utf-8 -*-
import json

from django.db import models
from django.db.models.signals import post_save
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
    # FixMe
    image = models.ImageField()

    class Meta:
        db_table = 'user_profile'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)


class Game(BaseModel):
    last_count = models.IntegerField(null=False, blank=False)
    last_record = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'game'


class Player(BaseModel):
    CHOICES = (
        ('w', 'white'),
        ('b', 'black'),
    )

    color = models.CharField(max_length=1, choices=CHOICES)
    is_fierst = models.BooleanField(null=False, blank=False)
    is_winner = models.BooleanField(null=False, blank=False)

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        db_table = 'player'


class Turn(BaseModel):
    X_AXIS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    Y_AXIS = ['1', '2', '3', '4', '5', '6', '7', '8']
    CHOICES = tuple([('{}{}'.format(x, y), '{}{}'.format(x, y)) for x in X_AXIS
                    for y in Y_AXIS]) + (('path', 'path'),)

    count = models.IntegerField(null=False, blank=False)
    axis = models.CharField(max_length=4, choices=CHOICES)
    record = models.TextField(null=False, blank=False)

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        db_table = 'turn'
