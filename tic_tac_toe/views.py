from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from .forms import NameForm

# -------------------------------------------------------- #
# custom modules
# -------------------------------------------------------- #
from . import config
from . import service
from . models import Players


# -------------------------------------------------------- #
# pages
# -------------------------------------------------------- #
def index(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            service.initialize_game(request)
            return HttpResponseRedirect('game_session')
    else:
        form = NameForm()
    context = {'form': form}
    return render(request, 'tic_tac_toe/index.html', context)


def game_session(request):
    # if request.method == 'POST':
    #     form = InputForm(request.POST)
    #     if form.is_valid():
    #         service.process_player_input(request)

    if request.session['currentPlayer'] == 0:
        request.session['currentPlayer'] = 1
    else:
        request.session['currentPlayer'] = 0
    # order = request.session['currentPlayer']
    # player = Players.objects.get(order=order)
    # cell_id = request.POST['cellId']
    # if service.if_win(player, cell_id):
    #     context = {'message': }
    context = {'currentPlayer': request.session['currentPlayer']}
    return render(request, 'tic_tac_toe/game_session.html', context)


def game_over(request):
    # result = request.session['result']
    # if result == 1:
    #     message = config.WINNING_MESSAGE
    # else:
    #     message = config.LOSING_MESSAGE
    prompt = "game over"
    context = {'prompt': prompt}
    return render(request, 'tic_tac_toe/game_over.html', context)


# -------------------------------------------------------- #
# subpages
# -------------------------------------------------------- #
# def get_name(request):
#     if request.method == 'POST':
#         form = NameForm(request.POST)
#         if form.is_valid():
#             return HttpResponseRedirect('session')
def make_grid(request):
    response = []
    for i in range(config.N):
        for j in range(config.N):
            cell = "{}_{}".format(i, j)
            html = "<div onclick=\"makeAjaxCall(\'{0}\');\" id=\"{0}\"></div>".format(cell)
            response.append(html)
    return JsonResponse(response, safe=False)


def make_move(request):

    # get current player, mebbe save this info to model and call from service
    cur_order = request.session['moves'] % config.NUMBER_OF_PLAYERS
    request.session['moves'] += 1
    nxt_order = request.session['moves'] % config.NUMBER_OF_PLAYERS

    player = Players.objects.get(order=cur_order)
    cell_id = request.POST['cell_id']
    moves = request.session['moves']

    if service.if_win(player, cell_id):
        message = "{} wins.".format(cur_order)
        context = {'message': message}
        return render(request, 'tic_tac_toe/game_over.html', context)

    elif service.if_draw(moves):
        message = "Draw"
        context = {'message': message}
        return render(request, 'tic_tac_toe/game_over.html', context)

    response = {
        "currentPlayer": cur_order,
        "nextPlayer": nxt_order
    }
    return JsonResponse(response)


def makeMark(request):
    response = '<div id=circle></div>'
    return HttpResponse(response)


# def index(request):
#     # initialize form
#     if request.method == 'POST':
#         form = InputForm(request.POST)
#         if form.is_valid():
#             # update data in response to player input
#             service.process_player_input(request)
#             # redirect player to appropriate page
#             if request.session['result']:
#                 return HttpResponseRedirect('game_over')
#             return HttpResponseRedirect('session')
#
#     # initialize data
#     word = service.select_word()
#     progress = len(word) * '*'
#     result = 0
#     incorrect_guesses = ''
#     free_guesses_remaining = config.FREE_GUESSES
#
#     # record initialized data
#     request.session['word'] = word
#     request.session['progress'] = progress
#     request.session['result'] = result
#     request.session['incorrect_guesses'] = incorrect_guesses
#     request.session['free_guesses_remaining'] = free_guesses_remaining
#
#     return render(request, 'tic_tac_toe/index.html',
#                   {
#                       'word': '',
#                       'progress': progress,
#                       'form': InputForm(),
#                       'incorrect_guesses': incorrect_guesses,
#                       'free_guesses_remaining': free_guesses_remaining
#                   })

# # in-session game behavior
# def session(request):
#     if request.method == 'POST':
#         form = InputForm(request.POST)
#         if form.is_valid():
#             service.process_player_input(request)
#             if request.session['result']:
#                 return HttpResponseRedirect('/game_over')
#
#     return render(request, 'tic_tac_toe/game_session.html',
#                   {
#                       'word': '',
#                       'progress': request.session['progress'],
#                       'form': InputForm(),
#                       'incorrect_guesses': request.session['incorrect_guesses'],
#                       'free_guesses_remaining': request.session['free_guesses_remaining']
#                   })
#
# display appropriate game over message

# # in-session game behavior
# # fetch current player
# def progress2(request):
#     response = request.session['moves'] % 2
#     request.session['moves'] += 1
#     return HttpResponse(response)


# def getCellId(request):
#     # if request.session['currentPlayer'] == 0:
#     #     request.session['currentPlayer'] = 1
#     # else:
#     #     request.session['currentPlayer'] = 0
#     name = request.session['currentPlayer']
#     player = Players.objects.get(name=name)
#     cellId = request.POST['cellId']
#     response = [cellId]
#     if service.if_win(player, cellId):
#         return HttpResponseRedirect('gg')
#     else:
#         return JsonResponse(response, safe=False)

# def getNextPlayer(request):
#     request.session['moves'] += 1
#     response = request.session['moves'] % config.NUMBER_OF_PLAYERS
#     return HttpResponse(response)

# 'testAjax': request.is_ajax(),
# 'currentPlayer': request.POST.get('currentPlayer')

    # starter = randrange(config.NUMBER_OF_PLAYERS)

# html = "<div onclick=\"processCellAjax(\'{0}\'); makeAjaxCall(\'{0}\');\" id=\"{0}\"></div>".format(cell)
