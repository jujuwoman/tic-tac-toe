from django.contrib.postgres.fields import JSONField
from django.db import models
from django.forms import ModelForm

# -------------------------------------------------------- #
# custom modules
# -------------------------------------------------------- #
from . import config


# -------------------------------------------------------- #
# helpers
# -------------------------------------------------------- #
def get_default_array():
    return [config.DEFAULT_COUNTER_VALUE] * config.N


# -------------------------------------------------------- #
# models
# -------------------------------------------------------- #
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
    moves = models.IntegerField(default=config.DEFAULT_COUNTER_VALUE)

    def __int__(self):
        return self.moves


class Players(models.Model):
    order = models.IntegerField(default=config.DEFAULT_COUNTER_VALUE)
    name = models.CharField(max_length=config.MAX_NAME_LENGTH)
    rows = JSONField(default=get_default_array)
    cols = JSONField(default=get_default_array)
    major = models.IntegerField(default=config.DEFAULT_COUNTER_VALUE)
    minor = models.IntegerField(default=config.DEFAULT_COUNTER_VALUE)

    def __str__(self):
        return self.name


class Marks(models.Model):
    name = models.CharField(max_length=config.MAX_NAME_LENGTH)

    def __str__(self):
        return self.name


# -------------------------------------------------------- #
# model forms
# -------------------------------------------------------- #
class PlayersForm(ModelForm):
    class Meta:
        model = Players
        fields = ['order', 'name']
