import random
from django.db import models
from .constants import *
from django.urls import reverse
from channels.db import database_sync_to_async
import time


def get_current_time():
    return int(time.time())

class GameManager(models.Manager):
    def create_game(self, player_name, player_id, game_type):
        game = self.create(
            ball_direction_x=random.choice(['positive', 'negative']),
            ball_direction_y=random.choice(['positive', 'negative']),
            points=[0, 0],
            player_x = [PLAYER1_START_X, PLAYER2_START_X],
            player_y = [PLAYER_START_Y, PLAYER_START_Y],
            player_pos = [0],
            player_ids = [player_id],
            player_names = [player_name],
            game_type = game_type
        )
        return game
    
    def create_tournament_game(self, game_type, tournament_id):
        game = self.create(
            ball_direction_x=random.choice(['positive', 'negative']),
            ball_direction_y=random.choice(['positive', 'negative']),
            points=[0, 0],
            player_x=[PLAYER1_START_X, PLAYER2_START_X],
            player_y=[PLAYER_START_Y, PLAYER_START_Y],
            player_pos=[],
            player_names=["",""],
            player_ids=[],
            game_type = game_type,
            tournament_id = tournament_id
        )
        return game

class Game(models.Model):
    #Containing data for one game.

    game_id = models.AutoField(primary_key=True)
    game_type = models.CharField(max_length=20, default='regular')
    tournament_id = models.IntegerField(default=0)
    player_ids = models.JSONField(default=list) 
    player_pos = models.JSONField(default=list)
    player_names = models.JSONField(default=list)
    player_x = models.JSONField(default=list)
    player_y = models.JSONField(default=list)
    ball_speed = models.FloatField(default=BALL_SPEED)
    ball_x = models.FloatField(default=BALL_START_X)
    ball_y = models.FloatField(default=BALL_START_Y)
    ball_velocity_x = models.FloatField(default=BALL_START_VELOCITY_X)
    ball_velocity_y = models.FloatField(default=BALL_START_VELOCITY_Y)
    ball_direction_x = models.CharField(max_length=8, choices=DIRECTION_CHOICES, default='positive')
    ball_direction_y = models.CharField(max_length=8, choices=DIRECTION_CHOICES, default='positive')
    start_play = models.BooleanField(default=False)
    msg = models.CharField(max_length=255, blank=True)
    end_play = models.BooleanField(default=False)
    points = models.JSONField(default=list)
    winner = models.CharField(max_length=255, blank=True)
    start_time = models.IntegerField(default=get_current_time)

    objects = GameManager()

    def __str__(self):
        return f"Pong {self.game_id}"
    
class Tournament(models.Model):

    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True)
    winner = models.CharField(max_length=100, null=True, blank=True)
    semifinal1 = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, related_name='tournament_semifinal1')
    semifinal2 = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, related_name='tournament_semifinal2')
    final = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, related_name='tournament_final')
    final_created = models.BooleanField(default=False)

    def __str__(self):
        return f"Winner {self.winner}"
    
    async def get_player_urls(self):
        return {
            self.semifinal1.player_names[0]: reverse('play_game', args=[self.semifinal1.game_id, 0, self.semifinal1.player_names[0]]),
            self.semifinal1.player_names[1]: reverse('play_game', args=[self.semifinal1.game_id, 1, self.semifinal1.player_names[1]]),
            self.semifinal2.player_names[0]: reverse('play_game', args=[self.semifinal2.game_id, 0, self.semifinal2.player_names[0]]),
            self.semifinal2.player_names[1]: reverse('play_game', args=[self.semifinal2.game_id, 1, self.semifinal2.player_names[1]]),
        }
    
    async def get_final_url(self):
        players_url = {}
        if self.final.player_names[0]:
            players_url[self.final.player_names[0]] = reverse('play_game', args=[self.final.game_id, 0, self.final.player_names[0]])
        if self.final.player_names[1]:
            players_url[self.final.player_names[1]] = reverse('play_game', args=[self.final.game_id, 1, self.final.player_names[1]])
        return players_url
    
    
class WaitingRoom(models.Model):
    players = models.JSONField(default=list)
    player_ids = models.JSONField(default=list) 
    tournament_created = models.BooleanField(default=False)