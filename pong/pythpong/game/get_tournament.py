from .models import Tournament, Game
from asgiref.sync import sync_to_async
from .models import GameManager
from channels.db import database_sync_to_async
import time

@sync_to_async
def create_tournament(players, player_ids):

    tournament = Tournament.objects.create()
    tournament.semifinal1 = Game.objects.create_tournament_game('semi_final1', tournament.id)
    tournament.semifinal2 = Game.objects.create_tournament_game('semi_final2', tournament.id)

    tournament.semifinal1.player_names = [players[0], players[1]]
    tournament.semifinal1.player_pos = [0, 1]
    tournament.semifinal1.player_ids = [player_ids[0], player_ids[1]]
    tournament.semifinal1.start_play = True
    tournament.semifinal1.start_time = int(time.time())
    tournament.semifinal1.save()

    tournament.semifinal2.player_names = [players[2], players[3]]
    tournament.semifinal2.player_pos = [0, 1]
    tournament.semifinal1.player_ids = [player_ids[2], player_ids[3]]
    tournament.semifinal2.start_play = True
    tournament.semifinal2.start_time = int(time.time())
    tournament.semifinal2.save()

    tournament.save()

    return tournament

@database_sync_to_async
def create_final(tournament_id, player_name, player_id):

    tournament = Tournament.objects.get(id=tournament_id)
    if not tournament.final_created:
        tournament.final = Game.objects.create_tournament_game('final', tournament.id)
        tournament.final.player_pos = [0, 1]
        tournament.final_created = True
        if tournament.semifinal1.winner == player_name:
            tournament.final.player_names[0] = player_name
            tournament.final.player_ids[0] = player_id
        else:
            tournament.final.player_names[1] = player_name
            tournament.final.player_ids[1] = player_id
    else:
        if tournament.semifinal1.winner == player_name:
            tournament.final.player_names[0] = player_name
            tournament.final.player_ids[0] = player_id
        else:
            tournament.final.player_names[1] = player_name
            tournament.final.player_ids[1] = player_id
        tournament.final.start_time = int(time.time())
        tournament.final.start_play = True

    tournament.final.save()
    tournament.save()
    return tournament
