import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from .models import WaitingRoom, Tournament
from .get_tournament import create_tournament
from channels.db import database_sync_to_async

class WaitingRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.connected = True
        self.player_name = self.scope['url_route']['kwargs']['player_name']
        self.group_name = 'waiting_room'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        asyncio.create_task(self.send_players_list())

    #this function refresh player list and notify when tournament can start
    async def send_players_list(self):
        while self.connected:
            players = await self.get_players()
            await self.send(text_data=json.dumps({'players': players}))
            if (len(players) >= 4):
                #Start tournament!!
                waiting_room = await self.get_waiting_room()
                await self.set_tournament_created(waiting_room, False)
                if waiting_room.tournament_created == False:
                    tournament = await create_tournament(players)
                    await self.set_tournament_created(waiting_room, True)
                    await self.clear_waiting_room(waiting_room)
                    player_urls = await tournament.get_player_urls()
                    await self.notify_players(player_urls)
                    await self.set_tournament_created(waiting_room, False)
            await asyncio.sleep(1)

    async def notify_players(self, player_urls):
        for player_name, url in player_urls.items():
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'redirect_player',
                    'player_name': player_name,
                    'url': url
                }
            )

    async def redirect_player(self, event):
        player_name = event['player_name']
        url = event['url']
        print(f"Redirecting {player_name} to {url}")
        await self.send(text_data=json.dumps({
            'type': 'redirect',
            'player_name': player_name,
            'url': url
        }))

    @database_sync_to_async
    def get_players(self):
        waiting_room = WaitingRoom.objects.first()
        return waiting_room.players
    
    @database_sync_to_async
    def get_waiting_room(self):
        waiting_room = WaitingRoom.objects.first()
        return waiting_room

    @database_sync_to_async
    def clear_waiting_room(self, waiting_room):
        waiting_room.players = []
        waiting_room.save()

    @database_sync_to_async
    def set_tournament_created(self, waiting_room, value):
        waiting_room.tournament_created = value
        waiting_room.save()