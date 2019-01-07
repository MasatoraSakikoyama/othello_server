# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

from django_redis import get_redis_connection

from apps.reversi.models import GameModel, PlayerModel, TurnModel


class BaseEntity(metaclass=ABCMeta):
    model = lambda x: x

    def __init__(self, data=None):
        self.data = {} if data is None else data

    @abstractmethod
    def multi_key(self):
        raise NotImplementedError

    @abstractmethod
    def key(self):
        raise NotImplementedError

    @abstractmethod
    def multi_select(self):
        raise NotImplementedError

    @abstractmethod
    def select(self):
        raise NotImplementedError

    @abstractmethod
    def insert(self):
        raise NotImplementedError

    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        raise NotImplementedError


class RDBEntity(BaseEntity, metaclass=ABCMeta):
    def multi_select(self):
        return [m.seriarized for m in self.model.objects.select_related().filter(**self.multi_key)]

    def select(self):
        return self.model.objects.select_related().get(self.key).serialized

    def insert(self):
        f = self.form(self.data)
        if not f.is_valid():
            raise Exception(f.errors)
        return f.save().serialized

    def update(self):
        m = self.model.objects.get(self.key)
        f = self.form(**self.data, instance=m)
        if not f.is_valid():
            raise Exception(f.errors)
        return f.save().serialized

    def delete(self, *args, **kwargs):
        self.model.objects.delete(self.key)


class CatchEntity(BaseEntity, metaclass=ABCMeta):
    def __init__(self, data=None):
        super().__init__(data=self.data)
        self.timeout = 60*60*7
        self.conn = get_redis_connection('storage')

    def multi_select(self):
        return self.conn.mget(self.multi_key)

    def select(self):
        return self.conn.get(self.key)

    def insert(self):
        f = self.form(self.data)
        if not f.is_valid():
            raise Exception(f.errors)
        m = f.save(commit=False).serialized

        if not self.conn.set(self.key, m, nx=True, timeout=self.timeout):
            raise Exception
        return m

    def update(self):
        f = self.form(self.data)
        if not f.is_valid():
            raise Exception(f.errors)
        _m = f.save(commit=False).serialized

        m = self.conn.get(self.key)
        m.update(_m)
        self.conn.set(self.key, m, timeout=self.timeout)
        return m

    def delete(self):
        self.conn.delete(self.key)


class GameEntity(CatchEntity):
    model = GameModel

    def multi_key(self):
        pass

    def key(self):
        pass
