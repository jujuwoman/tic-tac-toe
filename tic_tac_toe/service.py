from random import randrange
from random import shuffle

# -------------------------------------------------------- #
# custom modules
# -------------------------------------------------------- #
from . import config
from . models import Players


CELL = "\t<div onclick=\"{}\" style=\"{}\" id=\"{}\"></div>"
HTML = "<div class='grid' id=\"cells\">\n{}\n</div>"
PATH = "templates/tic_tac_toe/grid.html"


def make_index_grid():
    cells = "\n".join([CELL for _ in range(config.N ** config.DIMENSIONS)])
    html = HTML.format(cells)
    with open(PATH, "w") as file:
        file.write(html)


def make_game_session_grid():
    arr = []
    for i in range(config.N):
        for j in range(config.N):
            java_script = "makeAjaxCall(this.id);"
            cursor = "cursor:pointer"
            cell_id = "{}_{}".format(i, j)
            arr.append(CELL.format(java_script, cursor, cell_id))
    cells = "\n".join(arr)
    html = HTML.format(cells)
    with open(PATH, "w") as file:
        file.write(html)


def make_cell_ids():
    cell_ids = ["{}_{}".format(i, j) for i in range(config.N) for j in range(config.N)]
    return cell_ids


def initialize_game(request):
    name = request.POST['name']
    player_names = [config.DEFAULT_OPPONENT_NAME, name]
    shuffle(player_names)

    request.session['moves'] = config.DEFAULT_COUNTER_VALUE
    request.session['game_result'] = ""
    # request.session['seed'] = randrange(config.NUMBER_OF_PLAYERS)
    Players.objects.all().delete()

    for i, e in enumerate(player_names):
        Players.objects.create(order=i, name=e)

    first_player_order = 0
    second_player_order = 1

    first_player_name = get_name_by_order(first_player_order)
    second_player_name = get_name_by_order(second_player_order)

    first_player_mark = config.MARKS[first_player_order]
    second_player_mark = config.MARKS[second_player_order]

    request.session["first_player"] = {
        "order": first_player_order,
        "name": first_player_name,
        "mark": first_player_mark
    }
    request.session["second_player"] = {
        "order": second_player_order,
        "name": second_player_name,
        "mark": second_player_mark
    }


def get_player_by_order(order):
    player = Players.objects.get(order=order)
    return player


def get_name_by_order(order):
    player = Players.objects.get(order=order)
    name = player.name
    return name


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


def if_grid_filled(moves):
    return moves == config.N ** config.DIMENSIONS
