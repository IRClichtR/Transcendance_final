from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class user(object):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    total_win = models.IntegerField(default=0)
    total_lose = models.IntegerField(default=0)
    total_games = models.IntegerField(default=0)
    # Inform if the user is currently logged in
    log_status = models.BooleanField(default = False)

def __str__(self):
    return self.username #return the username if I print the object



# class pong_match(object):
#     id_player_1
#     id_player_2
#     score_player1
#     score_player2
#     winner
#     pass
#
# class pong_tournament(object):
#     pass
#
# class webSockets(object):
#     pass
