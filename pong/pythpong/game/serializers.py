from rest_framework.serializers import ModelSerializer
from .models import Game, WaitingRoom, Tournament

class GameSerializer(ModelSerializer):

    class Meta:
        model = Game
        fields = ['game_id', 'start_time', 'player_id', 'player_names', 'points']

class WaitingRoomSerializer(ModelSerializer):

    class Meta:
        model = WaitingRoom
        fields = ['players']

class TournamentSerializer(ModelSerializer):
    class Meta:
        model = Tournament 
        fields = '__all__'
