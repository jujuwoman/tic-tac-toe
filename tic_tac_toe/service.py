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

moves (integer):
initialized in service.py
total number of moves made in a game

random_cell_id (string):
initialized in service.py
stores computer's randomly chosen move
"""

import json
from collections import OrderedDict
from datetime import datetime
from random import randrange
from random import shuffle

# -------------------------------------------------------- #
# custom modules
# -------------------------------------------------------- #
from . import config
from .models import History
from .models import Players


# used by views::index
def initialize_game(request):
    # initialize session data: free_cells, switch, result
    initialize_free_cells(request)
    request.session["switch"] = 0
    request.session["result"] = ""
    request.session["moves"] = 0

    # randomize player order
    # player name will be case-insensitive
    name = request.POST["name"].lower()
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

    # initialize session data: random_cell_id
    if first_player_name == config.DEFAULT_COMPUTER_NAME:
        request.session['random_cell_id'] = get_random_free_cell(request)
    else:
        request.session['random_cell_id'] = ""


# used by views::make_move_via_ajax
def get_context_for_move(request, order, cell_id):
    players_model_object = get_players_model_object_by_order(order)

    # check terminating conditions
    # win
    if is_win(players_model_object, cell_id):
        request.session['result'] = "win"
        add_history_entry(request)
        context = {
            "current_player": request.session["current_player"],
            "result": request.session["result"]
        }
    # draw
    elif not get_free_cells_as_list(request):
        request.session["result"] = "draw"
        add_history_entry(request)
        context = {
            "current_player": request.session["current_player"],
            "result": request.session["result"]
        }
    # game in progress
    else:
        # assign random move if computer is next player
        update_random_cell_id(request, order)

        context = {
            "current_player": request.session["current_player"],
            "next_player": request.session["next_player"],
            "result": request.session["result"],
            "random_cell_id": request.session["random_cell_id"]
        }
        # alternate players
        request.session["switch"] ^= 1
        tmp = request.session["next_player"]
        request.session["next_player"] = request.session["current_player"]
        request.session["current_player"] = tmp

    return context


def initialize_map(request):
    request.session["map"] = OrderedDict()
    for i in range(config.N):
        for j in range(config.N):
            cell_id = "{}_{}".format(i, j)
            request.session["map"][cell_id] = ""


def initialize_free_cells(request):
    ls = list(request.session["map"].keys())
    request.session["free_cells"] = json.dumps(ls)


def update_random_cell_id(request, order):
    current_player_name = get_name_by_order(order)
    next_player_name = get_name_by_order(order ^ 1)
    if current_player_name == config.DEFAULT_COMPUTER_NAME:
        if next_player_name == config.DEFAULT_COMPUTER_NAME:
            # allows computer to play against computer
            request.session["random_cell_id"] = get_random_free_cell(request)
        else:
            # allows next human player to make move by choice
            request.session["random_cell_id"] = ""
    else:
        request.session["random_cell_id"] = get_random_free_cell(request)


def get_random_free_cell(request):
    ls = get_free_cells_as_list(request)
    cell_id = ls[randrange(len(ls))]
    return cell_id


def remove_free_cell(request, cell_id):
    ls = get_free_cells_as_list(request)
    ls.remove(cell_id)
    request.session["free_cells"] = json.dumps(ls)


def get_free_cells_as_list(request):
    ls = json.loads(request.session["free_cells"])
    return ls


def get_name_by_order(order):
    player = Players.objects.get(order=order)
    name = player.name
    return name


def get_players_model_object_by_order(order):
    player = Players.objects.get(order=order)
    return player


def is_win(player, cell_id):
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


def add_history_entry(request):
    History.objects.create(human_player_name=request.session["current_player"]["name"],
                           moves=request.session["moves"],
                           result=request.session["result"],
                           last_played=datetime.now())


def history():
    return {i: {"name": e.human_player_name,
                "moves": e.moves,
                "result": e.result,
                "last_played": e.last_played}
            for i, e in enumerate(History.objects.all())}
