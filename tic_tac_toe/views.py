from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from .forms import NameForm

# -------------------------------------------------------- #
# custom modules
# -------------------------------------------------------- #
from . import config
from . import service


# -------------------------------------------------------- #
# pages
# -------------------------------------------------------- #
def index(request):
    # clear cache
    request.session.flush()

    # initialize following session data:
    # map
    service.initialize_map(request)

    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            service.initialize_game(request)
            return redirect("game_session")
    else:
        form = NameForm()
        context = {
            "map": request.session["map"],
            "form": form
        }
        return render(request, 'tic_tac_toe/index.html', context)


def game_session(request):
    context = {
        "map": request.session["map"],
        "first_player": request.session["first_player"],
        "second_player": request.session["second_player"],
        "current_player": request.session["current_player"]
    }
    return render(request, "tic_tac_toe/game_session.html", context)


def game_over(request):
    context = {
        "map": request.session["map"],
        "first_player": request.session["first_player"],
        "second_player": request.session["second_player"],
        "current_player": request.session["current_player"],
        "result": request.session["result"]
    }
    return render(request, "tic_tac_toe/game_over.html", context)


# -------------------------------------------------------- #
# subpages
# -------------------------------------------------------- #
# used by game_session.html
def make_move(request):

    request.session["moves"] += 1 # change to free_cells later

    current_player_order = request.session["switch"]
    current_player_object = service.get_player_object_by_order(current_player_order)
    cell_id = request.POST["cell_id"]
    moves = request.session["moves"] # change to free_cells later

    # mark map
    request.session["map"][cell_id] = config.MARKS[current_player_order]

    # check game's terminating conditions
    # when there's a winner
    if service.if_win(current_player_object, cell_id):
        request.session['result'] = "win"
        context = {
            "current_player": request.session["current_player"],
            "result": request.session["result"]
        }
    # when there's a draw
    elif service.if_grid_filled(moves):
        request.session["result"] = "draw"
        context = {
            "current_player": request.session["current_player"],
            "result": request.session["result"]
        }
    # when the game is still in progress
    else:
        context = {
            "current_player": request.session["current_player"],
            "next_player": request.session["next_player"],
            "result": request.session["result"]
        }
        # switch turns for players
        request.session["switch"] ^= 1
        tmp = request.session["next_player"]
        request.session["next_player"] = request.session["current_player"]
        request.session["current_player"] = tmp

    return JsonResponse(context)
