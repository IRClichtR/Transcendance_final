from rest_framework.serializers import ModelSerializer
from .models import Game

class GameSerializer(ModelSerializer):

    class Meta:
        model = Game
        fields = ['game_id', 'start_time', 'player_names', 'points']