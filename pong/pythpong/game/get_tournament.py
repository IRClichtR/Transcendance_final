from .models import Tournament, Game
from asgiref.sync import sync_to_async
from .models import GameManager
from channels.db import database_sync_to_async
import time

@sync_to_async
def create_tournament(players, player_ids):
    print("Création du tournoi avec les joueurs :", player_ids)
    tournament = Tournament.objects.create()
    tournament.semifinal1 = Game.objects.create_tournament_game('semi_final1', tournament.id)
    tournament.semifinal2 = Game.objects.create_tournament_game('semi_final2', tournament.id)
    tournament.final = Game.objects.create_tournament_game('final', tournament.id)

    tournament.semifinal1.player_names = [players[0], players[1]]
    tournament.semifinal1.player_pos = [0, 1]
    tournament.semifinal1.player_ids = [player_ids[0], player_ids[1]]
    tournament.semifinal1.start_play = True
    tournament.semifinal1.start_time = int(time.time())
    tournament.semifinal1.save()

    tournament.semifinal2.player_names = [players[2], players[3]]
    tournament.semifinal2.player_pos = [0, 1]
    tournament.semifinal2.player_ids = [player_ids[2], player_ids[3]]
    tournament.semifinal2.start_play = True
    tournament.semifinal2.start_time = int(time.time())
    tournament.semifinal2.save()

    tournament.final.player_pos = [0, 1]
    tournament.final.player_names = ["",""]
    tournament.final.player_ids = ["", ""]
    tournament.final.save()

    print("Semifinal 1 Player IDs:", tournament.semifinal1.player_ids)
    print("Semifinal 2 Player IDs:", tournament.semifinal2.player_ids)

    tournament.save()

    return tournament

@database_sync_to_async
def create_final(tournament_id, player_name, player_id):
    print("CREATE FINAL", player_name, player_id, tournament_id)

    tournament = Tournament.objects.get(id=tournament_id)
    if not tournament.final_created:
        print("TOURNAMENT TO CREATE")
        try:
            tournament.final_created = True
            print("TOURNAMENT_FINALLLLLLLLL=", tournament.final.game_id)
            tournament.final.save()
            print("TOURNAMENT_FINAL=", tournament.final.game_id)
            if tournament.semifinal1.winner == player_id:
                tournament.final.player_names[0] = player_name
                tournament.final.player_ids[0] = player_id
                print("JE FILL 0")
            else:
                tournament.final.player_names[1] = player_name
                tournament.final.player_ids[1] = player_id
                print("JE FILL 1")
        except Exception as e:
            print(f"Error creating tournament: {e}")
    else:
        if tournament.semifinal1.winner == player_id:
            tournament.final.player_names[0] = player_name
            tournament.final.player_ids[0] = player_id
            print("JE FILL 0 cote deja cree")
        else:
            tournament.final.player_names[1] = player_name
            tournament.final.player_ids[1] = player_id
            print("JE FILL 1 cote deja cree")
        tournament.final.start_time = int(time.time())
        tournament.final.start_play = True
        print("TOURNAMENT STARTEDDDD")

    tournament.final.save()
    tournament.save()
    return tournament
