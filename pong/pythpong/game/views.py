from django.shortcuts import render, redirect
from .get_game_pos_id import get_game_pos_id, get_local_game
from .constants import *
from .models import WaitingRoom, Game
from .eth import get_all_tournament_games
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import GameSerializer, WaitingRoomSerializer, TournamentSerializer
from django.conf import settings
import requests
import json
from django.http import JsonResponse
from django.middleware.csrf import get_token

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

def start_game(request):
    if request.method == 'POST':
        player_name = request.POST.get('playerName')
        player_id = request.POST.get('playerId')
        game_id, player_pos = get_game_pos_id(player_name, player_id)
        return redirect('play_game', game_id=game_id, player_pos=player_pos, player_name=player_name)
    return render(request, 'game/index.html')

def start_local_game(request):
    if request.method == 'POST':
        player_id = request.POST.get('playerId')
        player_name = request.POST.get('playerName')
        game_id = get_local_game(player_name, player_id)
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
        player_name = request.POST.get('playerName')
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

def get_history(request, player_name):
    tournament_history = get_all_tournament_games()
    context = {
        'player_name' : player_name,
        'tournament_history' : tournament_history,
    }
    return render(request, 'game/history.html', context)


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