from django.db import models


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


class Players(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Marks(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name