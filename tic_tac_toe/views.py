from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from random import randrange


# -------------------------------------------------------- #
# custom modules
# -------------------------------------------------------- #
from . import config
from . import service
# from .forms import InputForm
from . models import Players


# -------------------------------------------------------- #
# views
# -------------------------------------------------------- #

# initialize game
def index(request):

    starter = randrange(config.NUMBER_OF_PLAYERS)

    Players.objects.all().delete()
    Players.objects.create(name=0)
    Players.objects.create(name=1)

    # player0 = Players.objects.create(name=0)
    # player1 = Players.objects.create(name=1)

    # rows = []
    # cols = []
    # major = []
    # minor = []
    # for i in range(config.N):
    #     rows.append(0)
    #     cols.append(0)
    #     major.append(0)
    #     minor.append(0)

    # rows = {}
    # cols = {}
    # major = {}
    # minor = {}
    # for i in range(config.N):
    #     rows[i] = 0
    #     cols[i] = 0
    #     major[i] = 0eieecchtccijlgjjgkevgcgltutcjrgkdkttenhnfiuh

    #     minor[i] = 0
    # player0 = Players.objects.create(name=0, rows=rows, cols=cols)
    # player1 = Players.objects.create(name=1, rows=rows, cols=cols)
    # player0 = Players.objects.create(name=0, rows=rows, cols=cols, major=major, minor=minor)
    # player1 = Players.objects.create(name=1, rows=rows, cols=cols, major=major, minor=minor)

        # player0.rows.append(0)
        # player0.rows.append(0)
        # player0.minor.append(0)
        # player0.major.append(0)

    # player1 = Players.objects.create(name=1, rows=rows, cols=cols, major=major, minor=minor)
    # for i in range(config.N):
    #     player1.rows.append(0)
    #     player1.rows.append(0)
    #     player1.minor.append(0)
    #     player1.major.append(0)


    # starter = 0
    # request.session['map'] = [[-1] * 3] * 3
    # request.session['markedRows'] = set()
    # request.session['markedCols'] = set()
    request.session['player1'] = []
    request.session['player2'] = []
    request.session['currentPlayer'] = starter
    request.session['testAjax'] = starter
    request.session['moves'] = 0
    return HttpResponseRedirect('session')

    # if request.method == 'POST':
    #     return HttpResponseRedirect('progress')
    #
    # starter = 0
    # request.session['player1'] = []
    # request.session['player2'] = []
    # request.session['currentPlayer'] = starter
    # request.session['testAjax'] = starter
    # request.session['moves'] = 0
    #
    # return render(request, 'tic_tac_toe/index.html',
    #               {
    #                   'starter': starter,
    #                   'currentPlayer': starter
    #               })

# # in-session game behavior
# # fetch current player
# def progress2(request):
#     response = request.session['moves'] % 2
#     request.session['moves'] += 1
#     return HttpResponse(response)

def getCurrentPlayer(request):
    currentPlayer = request.session['moves'] % config.NUMBER_OF_PLAYERS
    request.session['moves'] += 1
    nextPlayer = request.session['moves'] % config.NUMBER_OF_PLAYERS
    response = {
        "currentPlayer": currentPlayer,
        "nextPlayer": nextPlayer
    }
    return JsonResponse(response)

def getNextPlayer(request):
    request.session['moves'] += 1
    response = request.session['moves'] % config.NUMBER_OF_PLAYERS
    return HttpResponse(response)

def getCellIds(request):
    response = []
    for i in range(config.ROWS):
        for j in range(config.COLUMNS):
            cell = "{}_{}".format(i, j)
            html = "<div onclick=\"processCellAjax(\'{0}\'); makeAjaxCall(\'{0}\');\" id=\"{0}\"></div>".format(cell)
            response.append(html)
    return JsonResponse(response, safe=False)

def getCellId(request):
    # if request.session['currentPlayer'] == 0:
    #     request.session['currentPlayer'] = 1
    # else:
    #     request.session['currentPlayer'] = 0
    name = request.session['currentPlayer']
    player = Players.objects.get(name=name)
    cellId = request.POST['cellId']
    response = [cellId]
    if service.ifWin(player, cellId):
        return HttpResponseRedirect('gg')
    else:
        return JsonResponse(response, safe=False)

# # in-session game behavior
# def progress2(request):
#     # return render(request, 'tic_tac_toe/progress2.html')
#     if request.session['currentPlayer'] == 0:
#         request.session['currentPlayer'] = 1
#     else:
#         request.session['currentPlayer'] = 0
#     reponse = request.session['currentPlayer']
#     return HttpResponse(reponse)

# # in-session game behavior
# def progress2(request):
#     # return render(request, 'tic_tac_toe/progress2.html')
#
#     reponse = request.session['currentPlayer']
#     return HttpResponse(reponse)

def showModels(request):
    response = Players.objects.all()
    return HttpResponse(response)


def makeMark(request):
    response = '<div id=circle></div>'
    return HttpResponse(response)

def session(request):
    # if request.method == 'POST':
    #     form = InputForm(request.POST)
    #     if form.is_valid():
    #         service.process_player_input(request)
    #         if request.session['result']:
    #             return HttpResponseRedirect('/game_over')

    if request.session['currentPlayer'] == 0:
        request.session['currentPlayer'] = 1
    else:
        request.session['currentPlayer'] = 0

    # return render(request, 'tic_tac_toe/progress2.html')


    return render(request, 'tic_tac_toe/session.html',
                  {
                      'starter': 0,
                      'testAjax': request.POST,
                      # 'testAjax': request.is_ajax(),
                      # 'testAjax': request.POST.get('currentPlayer'),
                      # 'currentPlayer': request.POST.get('currentPlayer')
                      'currentPlayer': request.session['currentPlayer']
                  })

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
#     return render(request, 'tic_tac_toe/session.html',
#                   {
#                       'word': '',
#                       'progress': request.session['progress'],
#                       'form': InputForm(),
#                       'incorrect_guesses': request.session['incorrect_guesses'],
#                       'free_guesses_remaining': request.session['free_guesses_remaining']
#                   })
#
# display appropriate game over message
def gg(request):
    # result = request.session['result']
    # if result == 1:
    #     message = config.WINNING_MESSAGE
    # else:
    #     message = config.LOSING_MESSAGE

    return render(request, 'tic_tac_toe/gg.html',
                  {
                      # 'word': request.session['word'],
                      # 'progress': request.session['progress'],
                      # 'result': result,
                      # 'message': message,
                      # 'incorrect_guesses': request.session['incorrect_guesses'],
                      # 'free_guesses_remaining': request.session['free_guesses_remaining']
                  })
