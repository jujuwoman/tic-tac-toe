import requests
from django.db import models

def player_input(request):
    coordinates = request.POST['coordinates']
    return

def ifWin(request):

    # player = request.POST.get('player')
    # [row, col] = request.POST...split('_')

    player.rows[row] += 1
    player.cols[col] += 1
    if row == col:
        player.minor[row] += 1
    if row + col == config.N:
        player.major[row] += 1
    return config.N in {player.rows[row], player.cols[col], player.minor[row], player.major[row]}

def ifDraw(request):
    return request.sessionp['moves'] == config.N ** config.DIMENSIONS