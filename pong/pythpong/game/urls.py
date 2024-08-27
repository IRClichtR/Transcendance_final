from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from .views import *

# create a router and register viewsets in it
router = DefaultRouter()
router.register(r'games', GameViewset, basename='game')
router.register(r'waitingroom', WaitingRoomViewset, basename='waitingrooms')
router.register(r'tournaments', TournamentViewSet, basename='tournament')

api_patterns = [
        path('', include(router.urls)),
        re_path(r'^games/(?P<player_id>.+)/$', GameViewset.as_view({'get': 'list'})),
        re_path(r'^waiting-room/$', WaitingRoomViewset.as_view({'get': 'list'})),
        path('tournament-history/<int:player_id>', get_history, name='get_history'),
        path('games-history/<int:player_id>', get_regular_history, name='get_regular_history')
        ]

app_patterns = [
    path('', index, name='index'),
    path('start-game', start_game, name='start_game'),
    path('start_local_game', start_local_game, name='start_local_game'),
    path('play/<int:game_id>/<int:player_pos>/<str:player_name>/', play_game, name='play_game'),
    path('play/<int:game_id>/<str:player_name>/', play_local_game, name='play_local_game'),
    path('waiting_room', waiting_room, name='waiting_room'),
    path('waiting_room/<str:player_name>/<int:player_id>', waiting_room_by_name, name='waiting_room_by_name'),
    path('get_data', get_data, name='get_data'),
    path('bc', store_tournament_data, name='store_tournament_data'),
    # path('pong/debug/settings/', debug_settings, name='debug-settings'),
    # include router-generated URL patterns
    # path('pong/api/', include(router.urls)),
]

urlpatterns = [
        # path('pong/admin/', admin.site.urls),
        path('pong/api/', include(api_patterns)),
        path('pong/', include(app_patterns)),
        ]
