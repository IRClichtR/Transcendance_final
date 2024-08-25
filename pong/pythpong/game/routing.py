from django.urls import re_path
from . import consumers_game, consumers_waiting_room

websocket_urlpatterns = [

    re_path(r'ws/game/(?P<game_id>\w+)/(?P<player_pos>\w+)/$', consumers_game.GameConsumer.as_asgi()),
    re_path(r'ws/waiting_room/(?P<player_name>\w+)/(?P<player_id>\w+)/$', consumers_waiting_room.WaitingRoomConsumer.as_asgi()),
]