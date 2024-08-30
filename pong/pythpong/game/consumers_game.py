import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from .models import Game, Tournament
from channels.db import database_sync_to_async
from .update_game_state import update_game_state, update_player_y
from .constants import DELAY
from .get_tournament import create_final
from .eth import store_data
from asgiref.sync import sync_to_async

class GameConsumer(AsyncWebsocketConsumer):

    async def websocket_connect(self, event):

        try:
            self.connected = True
            self.game_id = self.scope['url_route']['kwargs']['game_id']
            self.player_pos = self.scope['url_route']['kwargs']['player_pos']
            self.room_group_name = f'game_{self.game_id}'

            #protection vs reconnection
            game = await self.get_game()
            if game.end_play:
                await self.close()
                return
            
            try:
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
            except Exception as e:
                print(f"Error adding channel to group: {e}")
                await self.close()
                return

            try:
                await self.accept()
                print(f"WebSocket connected: Game ID {self.game_id}, Player Pos {self.player_pos}")
            except Exception as e:
                print(f"Error during WebSocket accept: {e}")
                await self.close()
                return

            # Start the loop to send game state periodically
            try:
                self.update_task = asyncio.create_task(self.update_game_loop())
            except Exception as e:
                print(f"Error in update loop: {e}")
        except Exception as e:
            print(f"Unexpected error during WebSocket connection: {e}")
            await self.close()

    async def disconnect(self, close_code):
        self.connected = False
        if (close_code == 1001):
            game = await self.get_game()
            if len(game.player_ids) == 1:
                await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
                await database_sync_to_async(game.delete)()

    async def websocket_receive(self, event):
        message = event['text']
        data = json.loads(message)

        game_data = data.get('game')
        
        # The only thing player can update is player[player_pos]_y
        await update_player_y(game_data['game_id'], game_data['player_pos'], game_data['player_y'])

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'player_move',
                'game': game_data
            }
        )

    async def player_move(self, event):
        game = event['game']

        await self.send(text_data=json.dumps({
            'type': 'player_move',
            'game': game
        }))

    @database_sync_to_async
    def get_game_state(self):
        game = Game.objects.get(game_id=self.game_id)
        return {
            'game_id': game.game_id,
            'ball_x': game.ball_x,
            'ball_y': game.ball_y,
            'player_names': game.player_names,
            'start_play': game.start_play,
            'msg': game.msg,
            'end_play': game.end_play,
            'points': game.points,
        }

    async def update_game_loop(self):
        game_started = False
        while self.connected:

            game = await self.get_game()
            if game.start_play:
                if not game_started:
                    for i in range(3, 0, -1):
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                'type': 'game_timer',
                                'message': f'Game starts in {i} seconds!'
                            }
                        )
                        await asyncio.sleep(1)
                    game_started = True
                while self.connected and game.start_play:
                    
                    await self.call_update_game_state(self.game_id)
                    game_state = await self.get_game_state()
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'game_update',
                            'game_state': game_state
                        }
                    )
                    if game_state['end_play']:
                        await self.handle_end_game()
                        return
                        
                    await asyncio.sleep(DELAY)
            else:
                await asyncio.sleep(1)

    #handle tournament final
    async def handle_end_game(self):
        game = await self.get_game()
        if (game.game_type == 'regular' or game.game_type == 'local' or game.player_ids[int(self.player_pos)] != game.winner):
            return
        elif game.game_type == 'final':
            tournament = await self.get_tournament(game.tournament_id)
            if tournament:
                await sync_to_async(store_data)(tournament)
            return
        tournament = await create_final(game.tournament_id, game.player_names[int(self.player_pos)], game.player_ids[int(self.player_pos)])
        tournament_url  = await tournament.get_final_url()
        await self.notify_players(tournament_url)

        await self.close_websocket()
        
    async def notify_players(self, tournament_url):
        for player_name, url in tournament_url.items():
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'redirect_player',
                    'player_name': player_name,
                    'url': url
                }
            )    

    async def redirect_player(self, event):
        player_name = event['player_name']
        url = event['url']
        #print(f"Redirecting {player_name} to {url}")
        await self.send(text_data=json.dumps({
            'type': 'redirect',
            'player_name': player_name,
            'url': url
        }))
    
    @database_sync_to_async
    def call_update_game_state(self, game_id):
        update_game_state(game_id)

    async def game_update(self, event):
        game_state = event.get('game_state')
        if game_state and self.connected == True:
            await self.send(text_data=json.dumps(game_state))
    
    async def game_timer(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'type': 'game_timer',
            'message': message
        }))

    async def close_websocket(self):

        game_state = await self.get_game_state()
        #Winner have to send the last message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_update',
                'game_state': game_state
            }
        )
        self.connected = False
        game = await self.get_game()
        if (game.game_type not in ['semi_final1', 'semi_final2']) or \
             (game.game_type in ['semi_final1', 'semi_final2'] and game.winner == game.player_names[int(self.player_pos)]):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        await self.close()
        self.update_task.cancel()

    @database_sync_to_async
    def get_game(self):
        return Game.objects.get(game_id=self.game_id)
    
    @database_sync_to_async
    def get_tournament(self, tournament_id):
        try:
            return Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return None