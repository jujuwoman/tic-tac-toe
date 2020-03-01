import requests
from django.db import models
from random import randrange
from random import shuffle

# -------------------------------------------------------- #
# custom modules
# -------------------------------------------------------- #
from . import config
from . models import Players


def initialize_game(request):
    name = request.POST['name']
    player_names = [config.DEFAULT_OPPONENT_NAME, name]
    shuffle(player_names)

    request.session['moves'] = 0
    Players.objects.all().delete()

    for i, e in enumerate(player_names):
        Players.objects.create(order=i, name=e)


def if_win(player, cell_id):
    [row, col] = list(map(int, cell_id.split('_')))
    player.rows[row] += 1
    player.cols[col] += 1
    if row == col:
        player.major += 1
    if row + col == config.N - 1:
        player.minor += 1
    player.save()
    return config.N in {player.rows[row], player.cols[col], player.major, player.minor}


def if_draw(moves):
    return moves == config.N ** config.DIMENSIONS
