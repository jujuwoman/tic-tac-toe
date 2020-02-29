from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField

from django.db import models

# -------------------------------------------------------- #
# custom modules
# -------------------------------------------------------- #
from . import config


class Roster(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Stats(models.Model):
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE)
    wins = models.IntegerField()
    losses = models.IntegerField()
    draws = models.IntegerField()

    def __int__(self):
        return [self.wins, self.losses, self.draws]


class GameState(models.Model):
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE)
    turn = models.BooleanField()

    def __bool__(self):
        return self.turn


def get_default_array():
    return [config.BASE_COUNTER_VALUE] * config.N


class Players(models.Model):
    name = models.CharField(max_length=255)
    rows = JSONField(default=get_default_array)
    cols = JSONField(default=get_default_array)
    major = models.IntegerField(default=config.BASE_COUNTER_VALUE)
    minor = models.IntegerField(default=config.BASE_COUNTER_VALUE)

    def __str__(self):
        return self.name


class Marks(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
