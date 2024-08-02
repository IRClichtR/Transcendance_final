from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from .views import *

# create a router and register viewsets in it
# router = DefaultRouter()
# router.register(r'games', GameViewset, basename='game')
# router.register(r'waitingrooms', WaitingRoomViewset, basename='waitingroom')


urlpatterns = [
    path('pong/', index, name='index'),
    path('pong/start-game', start_game, name='start_game'),
    path('pong/start_local_game', start_local_game, name='start_local_game'),
    path('pong/play/<int:game_id>/<int:player_id>/<str:player_name>/', play_game, name='play_game'),
    path('pong/play/<int:game_id>/<str:player_name>/', play_local_game, name='play_local_game'),
    path('pong/waiting_room', waiting_room, name='waiting_room'),
    path('pong/waiting_room/<str:player_name>/', waiting_room_by_name, name='waiting_room_by_name'),
    path('pong/get_data', get_data, name='get_data'),
    path('pong/history/<str:player_name>/', get_history, name='get_history'),
    path('pong/debug/settings/', debug_settings, name='debug-settings'),
    re_path(r'^pong/api/games/(?P<player_name>.+)/$', GameViewset.as_view({'get': 'list'})),
    re_path(r'^pong/api/waiting-room/$', WaitingRoomViewset.as_view({'get': 'list'})),
    # include router-generated URL patterns
    # path('pong/api/', include(router.urls)),
]
