from django.shortcuts import render, redirect
from .get_game_pos_id import get_game_pos_id, get_local_game
from .constants import *
from .models import WaitingRoom, Game, Tournament
from .eth import get_all_tournament_games
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import GameSerializer, WaitingRoomSerializer, TournamentSerializer
from django.conf import settings
import requests
import json
from django.http import JsonResponse
from django.middleware.csrf import get_token
from .eth import store_data

# for debug purpose only
# from rest_framework.permissions import IsAuthenticated
#
# def debug_settings(request):
#     debug_info = {
#         'STATIC_URL' : settings.STATIC_URL,
#         'STATIC_ROOT': settings.STATIC_ROOT,
#         'STATICFILES_DIRS': settings.STATICFILES_DIRS,
#         'TEMPLATES_DIRS': settings.TEMPLATES
#     }
#     return JsonResponse(debug_info)
# # end of debug

""" def store_tournament_data(request): DEBUG ONLY
    # Récupérer le tournoi ou renvoyer une erreur 404 s'il n'existe pas
    try:
        tournament = 0
        store_data(tournament)
        return JsonResponse({"message": f"Data stored successfully for tournament {tournament.id}"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500) """

def start_game(request):
    if request.method == 'POST':
        player_name = request.POST.get('playerUsername')
        player_id = request.POST.get('playerId')
        game_id, player_pos = get_game_pos_id(player_name, player_id)
        return redirect('play_game', game_id=game_id, player_pos=player_pos, player_name=player_name)
    return render(request, 'game/index.html')

def start_local_game(request):
    if request.method == 'POST':
        player_id = request.POST.get('playerId')
        player_name2 = request.POST.get('playerName')
        player_name = request.POST.get('playerUsername')
        game_id = get_local_game(player_name, player_id, player_name2)
        return redirect('play_local_game', game_id=game_id, player_name=player_name)
    return render(request, 'game/index.html')

def play_local_game(request, game_id, player_name):
    context = {
        'game_id': game_id,
        'player_pos': 0,
        'window_width': WINDOW_WIDTH,
        'window_height': WINDOW_HEIGHT,
        'ball_diameter': BALL_DIAMETER,
        'bat_height': BAT_HEIGHT,
        'bat_width': BAT_WIDTH,
        'bat_speed': BAT_MOVEMENT_SPEED,
        'start_pos_y': PLAYER_START_Y,
        'player1_x' : PLAYER1_START_X,
        'player2_x' : PLAYER2_START_X,
        'player_name': player_name,
    }
    return render(request, 'game/local_play.html', context)

def play_game(request, game_id, player_pos, player_name):
    context = {
        'game_id': game_id,
        'player_pos': player_pos,
        'window_width': WINDOW_WIDTH,
        'window_height': WINDOW_HEIGHT,
        'ball_diameter': BALL_DIAMETER,
        'bat_height': BAT_HEIGHT,
        'bat_width': BAT_WIDTH,
        'bat_speed': BAT_MOVEMENT_SPEED,
        'start_pos_y': PLAYER_START_Y,
        'player1_x' : PLAYER1_START_X,
        'player2_x' : PLAYER2_START_X,
        'player_name': player_name,
    }
    return render(request, 'game/play.html', context)

def index(request):
    return render(request, 'game/index.html')

def waiting_room(request):

    if request.method == 'POST':
        player_name = request.POST.get('playerUsername')
        player_id = request.POST.get('playerId')
        waiting_room = WaitingRoom.objects.all().first()
        if waiting_room is None:
            waiting_room = WaitingRoom.objects.create()

        waiting_room.players.append(player_name)
        waiting_room.player_ids.append(player_id)
        waiting_room.save()
        return redirect('waiting_room_by_name', player_name=player_name, player_id=player_id)
    return render(request, 'game/index.html')

def waiting_room_by_name(request, player_name, player_id):
    context = {
        'player_name': player_name,
        'player_id': player_id,
    }
    return render(request, 'waiting_room.html', context)

def get_data(request):
    if request.method == 'POST':
        player_name = request.POST.get('playerName')
        return redirect('get_history', player_name=player_name)
    return render(request, 'game/index.html')

def get_history(request, player_id):
    result = get_all_tournament_games()
    if result is None or 'data' not in result:
        return JsonResponse({'error': 'Could not retrieve tournament games'}, status=500)

    tournament_history = result['data']
    formatted_history = []

    for game in tournament_history:

        if (
            game[3] == player_id or
            game[4] == player_id or
            game[5] == player_id or
            game[6] == player_id):

            formatted_game = {
                'semifinal1_start_time' : game[0],
	            'semifinal2_start_time' : game[1],
		        'final_start_time'      : game[2],
		        'semifinal1_player1_id' : game[3],
		        'semifinal1_player2_id' : game[4],
		        'semifinal2_player1_id' : game[5],
		        'semifinal2_player2_id' : game[6],
		        'semifinal1_player1'    : game[7],
		        'semifinal1_player2'    : game[8],
		        'semifinal2_player1'    : game[9],
		        'semifinal2_player2'    : game[10],        
		        'final_player1'         : game[11],         
		        'final_player2'         : game[12],
		        'semifinal1_score1'     : game[13],    
		        'semifinal1_score2'     : game[14],    
		        'semifinal2_score1'     : game[15],    
		        'semifinal2_score2'     : game[16],    
		        'final_score1'          : game[17],
		        'final_score2'          : game[18],
            }
            formatted_history.append(formatted_game)

    data = {
        'player_id' : player_id,
        'tournament_history' : formatted_history,
    }
    return JsonResponse(data)

def get_regular_history (request, player_id):
    queryset = Game.objects.filter(game_type='regular')
    if not queryset.exists():
        return JsonResponse({'error': 'Could not retrieve games'}, status=500)

    formatted_history = []

    for game in queryset:
        if str(player_id) == game.player_ids[0] or str(player_id) == game.player_ids[1]:
            formatted_game = {
                'start_time': game.start_time,
                'player_name_0': game.player_names[0] if len(game.player_names) > 0 else None,
                'player_name_1': game.player_names[1] if len(game.player_names) > 1 else None,
                'player_id_0': game.player_ids[0] if len(game.player_ids) > 0 else None,
                'player_id_1': game.player_ids[1] if len(game.player_ids) > 1 else None,
                'score_0': game.points[0] if len(game.points) > 0 else None,
                'score_1': game.points[1] if len(game.points) > 1 else None,
            }
            formatted_history.append(formatted_game)

    data = {
        'player_id': player_id,
        '1v1': formatted_history,
    }
    return JsonResponse(data)

class GameViewset(ReadOnlyModelViewSet):
 
    serializer_class = GameSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        player_id = self.kwargs['player_id']
        queryset = Game.objects.filter(game_type='regular')
        filtered_queryset = [game for game in queryset if player_id in game.player_ids]
        return filtered_queryset
    
class WaitingRoomViewset(ReadOnlyModelViewSet):
 
    serializer_class = WaitingRoomSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WaitingRoom.objects.all()
        

class TournamentViewSet(ReadOnlyModelViewSet):
    serializer_class = TournamentSerializer

    def get_queryset(self):
        return Tournament.objects.all()