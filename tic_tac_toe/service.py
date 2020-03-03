from collections import OrderedDict
from random import shuffle

# -------------------------------------------------------- #
# custom modules
# -------------------------------------------------------- #
from . import config
from . models import Players


# used by views::index
def initialize_game(request):

    # initialize following session data:
    # free_cells

    # initialize following session data:
    # moves, switch, result
    request.session["moves"] = config.DEFAULT_COUNTER_VALUE # mebbe deprecate
    request.session["switch"] = 0
    request.session["result"] = ""

    # randomize players
    name = request.POST["name"]
    player_names = [config.DEFAULT_OPPONENT_NAME, name]
    shuffle(player_names)

    # initialize following model:
    # Players
    Players.objects.all().delete()
    for i, e in enumerate(player_names):
        Players.objects.create(order=i, name=e)

    # initialize following session data:
    # first_player, second_player, current_player, next_player
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
    request.session["free_cells"] = request.session["map"].keys()


# used by views::index
def initialize_map(request):
    # map serves as internal representation of game state
    request.session["map"] = OrderedDict()
    for i in range(config.N):
        for j in range(config.N):
            cell_id = "{}_{}".format(i, j)
            request.session["map"][cell_id] = ""


# used by views::make_move
def get_player_object_by_order(order):
    player = Players.objects.get(order=order)
    return player


# used by views::make_move
def if_win(player, cell_id):
    [row, col] = list(map(int, cell_id.split('_')))
    player.rows[row] += 1
    player.cols[col] += 1
    if row == col:
        player.major += 1
    if row + col == config.N - 1:
        player.minor += 1
    player.save()
    tallies = {player.rows[row], player.cols[col], player.major, player.minor}
    return config.N in tallies


# used by views::make_move
def if_grid_filled(moves):
    return moves == config.N ** config.DIMENSIONS
