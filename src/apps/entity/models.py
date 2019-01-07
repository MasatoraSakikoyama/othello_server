# -*- coding: utf-8 -*-
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from django.db import models
from django.forms.models import model_to_dict


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=128, unique=True, validators=[UnicodeUsernameValidator()])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def serialized(self):
        return model_to_dict(self)

    class Meta:
        abstract = True


class GameModel(BaseModel):
    game_id = models.CharField(max_length=128, null=False, blanke=True)

    class Meta:
        db_table = 'game'


class PlayerModel(BaseModel):
    player_id = models.CharField(max_length=128, null=False, blanke=True)
    is_first = models.BooleanField(null=False, blank=False)
    is_winner = models.BooleanField(null=True, blank=True)
    game = models.ForeignKey(GameModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'player'


class TurnModel(BaseModel):
    turn_id = models.CharField(max_length=128, null=False, blanke=True)
    count = models.IntegerField(null=False, blank=False)
    axis = models.CharField(max_length=4, choices=settings.AXIS_CHOICES)
    game = models.ForeignKey(GameModel, on_delete=models.CASCADE)
    player = models.ForeignKey(PlayerModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'turn'
