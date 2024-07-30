from rest_framework.serializers import ModelSerializer
from .models import Game, WaitingRoom

class GameSerializer(ModelSerializer):

    class Meta:
        model = Game
        fields = ['game_id', 'start_time', 'player_names', 'points']

class WaitingRoomSerializer(ModelSerializer):

    class Meta:
        model = WaitingRoom
        fields = ['players']