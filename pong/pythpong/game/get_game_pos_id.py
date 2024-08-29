from .models import Game, Tournament
from django.db.models import Count
from django.conf import settings
import random
import time
import requests

#   this method is called when a new connection is accepted to start game and needs the game id and player id.
#   It provides the available game id and the player id for the new player.
#   If there is any game where one player is waiting for another player, that game id and a player id is given.
#   If there is no existing game with one available slot, it creates a new game and returns the ids.

def get_game_pos_id(player_name, player_id):

    player_pos = 0
    existing_games = Game.objects.all()

    for existing_game in existing_games:
        if len(existing_game.player_pos) == 1:
            #add the new player
            player_pos = list({0, 1} - set(existing_game.player_pos))[0]
            existing_game.player_names.append(player_name)
            existing_game.player_pos.append(player_pos)
            existing_game.player_ids.append(player_id)
            existing_game.start_play = True
            existing_game.start_time = int(time.time())
            existing_game.save()
            return existing_game.game_id, player_pos

    # if no game with 1 player, create a new game
    new_game = Game.objects.create_game(player_name, player_id, 'regular')
    return new_game.game_id, player_pos

def get_local_game(player_name, player_id, player_name2):

    new_game = Game.objects.create_game(player_name, player_id, 'local')
    new_game.player_pos = [0, 1]
    new_game.player_ids = [0, 0]
    new_game.player_names.append(player_name2)
    new_game.start_play = True
    new_game.start_time = int(time.time())
    new_game.save()
    return new_game.game_id