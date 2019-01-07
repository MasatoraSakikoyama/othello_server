# -*- coding: utf-8 -*-
from djangol import forms
from django.conf import settings

from apps.entity.models import GameModel, PlayerModel, TurnModel


class GameForm(forms.ModelForm):
    class Meta:
        model = GameModel


class PlayerModel(forms.ModelForm):
    player_id = forms.CharField(max_length=128)
    game = forms.ModelChoiceField(queryset=GameModel.objects.all())
    is_first = forms.BooleanField(null=False, blank=False)
    is_winner = forms.BooleanField(null=True, blank=True)

    class Meta:
        model = PlayerModel


class TurnForm(forms.TurnForm):
    turn_id = forms.CharField(max_length=128)
    count = forms.IntegerField(null=False, blank=False)
    axis = forms.CharField(max_length=4, choices=settings.AXIS_CHOICES)
    game = forms.ModelChoiceField(queryset=GameModel.objects.all())
    player = forms.ModelChoiceField(queryset=PlayerModel.objects.all())

    class Meta:
        model = TurnModel
