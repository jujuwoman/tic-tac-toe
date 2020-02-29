import requests
from django.db import models

# -------------------------------------------------------- #
# custom modules
# -------------------------------------------------------- #
from . import config
from . models import Players



def ifWin(player, cellId):

    [row, col] = list(map(int, cellId.split('_')))

    player.rows[row] += 1
    player.cols[col] += 1
    if row == col:
        player.major += 1
    if row + col == config.N - 1:
        player.minor += 1
    player.save()

    return config.N in {player.rows[row], player.cols[col], player.major, player.minor}

def ifDraw(request):
    return request.sessionp['moves'] == config.N ** config.DIMENSIONS