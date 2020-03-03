"""
--------------------------------------------------------
REQUEST SESSION DATA
--------------------------------------------------------
map (dictionary):
initialized in views.py
internal representation of game state
keeps track of which cells are occupied by which mark

free_cells (string json-serialized from python list):
initialized in service.py
keeps track of which cells are still empty

switch (bit):
initialized in service.py
flips to alternate player orders

first_player (dictionary):
initialized in service.py
keys: name and order
for displaying legend

second_player (dictionary):
initialized in service.py
keys: name and order
for displaying legend

current_player (dictionary):
initialized in service.py
keys: name and order
for displaying result

next_player (dictionary):
initialized in service.py
keys: name and order
for displaying whose turn it is

result (string):
initialized in service.py
stores game's terminating status ("", "win", or "draw")
"""

from collections import OrderedDict
from random import randrange
from random import shuffle
import json
import time

# -------------------------------------------------------- #
# custom modules
# -------------------------------------------------------- #
from . import config
from . models import Players


# used by views::index
def initialize_game(request):

    # initialize session data: free_cells, switch, result
    initialize_free_cells(request)
    request.session["switch"] = 0
    request.session["result"] = ""

    # randomize player order
    name = request.POST["name"]
    player_names = [config.DEFAULT_COMPUTER_NAME, name]
    shuffle(player_names)

    # initialize model: Players
    Players.objects.all().delete()
    for i, e in enumerate(player_names):
        Players.objects.create(order=i, name=e)

    # initialize session data: first_player, second_player, current_player, next_player
    first_player_order = 0
    second_player_order = 1
    first_player_name = get_name_by_order(first_player_order)
    second_player_name = get_name_by_order(second_player_order)
    first_player_mark = config.MARKS[first_player_order]
    second_player_mark = config.MARKS[second_player_order]
    request.session["first_player"] = {
        "name": first_player_name,
        "mark": first_player_mark
    }
    request.session["second_player"] = {
        "name": second_player_name,
        "mark": second_player_mark
    }
    request.session["current_player"] = request.session["first_player"]
    request.session["next_player"] = request.session["second_player"]


# used by initialize_game
def get_name_by_order(order):
    player = Players.objects.get(order=order)
    name = player.name
    return name


# used by initialize_game
def initialize_free_cells(request):
    cells = list(request.session["map"].keys())
    request.session["free_cells"] = json.dumps(cells)


# used by views::index
def initialize_map(request):
    request.session["map"] = OrderedDict()
    for i in range(config.N):
        for j in range(config.N):
            cell_id = "{}_{}".format(i, j)
            request.session["map"][cell_id] = ""


# used by views::make_move_via_ajax
def update_free_cells(request, cell_id):
    ls = json.loads(request.session["free_cells"])
    ls.remove(cell_id)
    request.session["free_cells"] = json.dumps(ls)


# used by views::make_move_via_ajax
def get_context_for_move(request, order, cell_id):
    players_model_object = get_players_model_object_by_order(order)

    # check terminating conditions
    # win
    if if_win(players_model_object, cell_id):
        request.session['result'] = "win"
        context = {
            "current_player": request.session["current_player"],
            "result": request.session["result"]
        }
    # draw
    elif not get_free_cells_as_list(request):
        request.session["result"] = "draw"
        context = {
            "current_player": request.session["current_player"],
            "result": request.session["result"]
        }
    # game in progress
    else:
        context = {
            "current_player": request.session["current_player"],
            "next_player": request.session["next_player"],
            "result": request.session["result"]
        }
        # alternate players
        request.session["switch"] ^= 1
        tmp = request.session["next_player"]
        request.session["next_player"] = request.session["current_player"]
        request.session["current_player"] = tmp

    return context


# used by get_context_for_move
def get_free_cells_as_list(request):
    ls = json.loads(request.session["free_cells"])
    return ls


# used by get_context_for_move
def get_players_model_object_by_order(order):
    player = Players.objects.get(order=order)
    return player


# used by get_context_for_move
def if_win(player, cell_id):
    [row, col] = list(map(int, cell_id.split("_")))
    player.rows[row] += 1
    player.cols[col] += 1
    if row == col:
        player.major += 1
    if row + col == config.N - 1:
        player.minor += 1
    player.save()
    tallies = {player.rows[row], player.cols[col], player.major, player.minor}
    if_win = config.N in tallies
    return if_win

