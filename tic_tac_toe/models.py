from django.contrib.postgres.fields import JSONField
from django.db import models

# -------------------------------------------------------- #
# custom modules
# -------------------------------------------------------- #
from . import config


# -------------------------------------------------------- #
# models
# -------------------------------------------------------- #
def get_default_array():
    return [config.DEFAULT_COUNTER_VALUE] * config.N


# -------------------------------------------------------- #
# models
# -------------------------------------------------------- #
# class History(models.Model):
#     name = models.CharField(max_length=config.MAX_NAME_LENGTH)
#     wins = models.IntegerField(default=config.DEFAULT_COUNTER_VALUE)
#     draws = models.IntegerField(default=config.DEFAULT_COUNTER_VALUE)
#     losses = models.IntegerField(default=config.DEFAULT_COUNTER_VALUE)
#     last_played = models.DateTimeField()
#
#     def __int__(self):
#         return self.name


class History(models.Model):
    human_player_name = models.CharField(max_length=config.MAX_NAME_LENGTH)
    moves = models.IntegerField(default=config.DEFAULT_COUNTER_VALUE)
    result = models.CharField(max_length=5, default="-")
    last_played = models.DateTimeField()

    def __int__(self):
        return self.human_player_name


class Players(models.Model):
    order = models.IntegerField(default=config.DEFAULT_COUNTER_VALUE)
    name = models.CharField(max_length=config.MAX_NAME_LENGTH)
    rows = JSONField(default=get_default_array)
    cols = JSONField(default=get_default_array)
    major = models.IntegerField(default=config.DEFAULT_COUNTER_VALUE)
    minor = models.IntegerField(default=config.DEFAULT_COUNTER_VALUE)

    def __str__(self):
        return self.name
