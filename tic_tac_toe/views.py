from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render

# -------------------------------------------------------- #
# custom modules
# -------------------------------------------------------- #
from . import config
from . import service
from .forms import NameForm


# -------------------------------------------------------- #
# pages
# -------------------------------------------------------- #
def index(request):

    # clear cache
    request.session.flush()
    # initialize session data: map
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
        return render(request, "tic_tac_toe/index.html", context)


def game_session(request):
    context = {
        "map": request.session["map"],
        "first_player": request.session["first_player"],
        "second_player": request.session["second_player"],
        "current_player": request.session["current_player"],
        "random_cell_id": request.session["random_cell_id"]
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
def make_move_via_ajax(request):
    current_player_order = request.session["switch"]
    cell_id = request.POST["cell_id"]

    # update game state
    request.session["map"][cell_id] = config.MARKS[current_player_order]
    service.remove_free_cell(request, cell_id)

    context = service.get_context_for_move(request, current_player_order, cell_id)
    return JsonResponse(context)
