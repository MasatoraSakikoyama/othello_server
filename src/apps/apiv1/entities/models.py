# -*- coding: utf-8 -*-
import json

from django.db import models
from django.forms.models import model_to_dict

from apps.apiv1.utils import datetime_default


class BaseModel(models.Model):
    @property
    def serialized(self):
        data = model_to_dict(self)
        return json.dumps(data, default=datetime_default)

    class Meta:
        abstract = True


class Game(BaseModel):
    id = models.AutoField(primary_key=True)
    test = models.DateTimeField()

    class Meta:
        db_table = 'game'
