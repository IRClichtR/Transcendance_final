# pong_cli.py
import argparse
import asyncio
import curses
import json
import os
import websockets

class PongGameCLI:
    def __init__(self, stdscr, game_id, player_id, player_name):
        self.stdscr = stdscr
        self.game_id = game_id
        self.player_id = player_id
        self.player_name = player_name
        self.ball = {'x': 0, 'y': 0, 'radius': 1}
        self.player1 = {'name': 'default', 'x': 0, 'y': 0, 'width': 1, 'height': 5, 'score': 0}
        self.player2 = {'name': 'default', 'x': 0, 'y': 0, 'width': 1, 'height': 5, 'score': 0}
        self.initialized = False
        self.msg = 'Waiting for opponent...'
        self.running = True

    async def handle_messages(self, websocket):
        async for message in websocket:
            data = json.loads(message)
            if data['type'] == 'player_move':
                game = data['game']
                if game['player_id'] == 0:
                    self.player1['y'] = game['player_y'][0]
                else:
                    self.player2['y'] = game['player_y'][1]
            elif data['type'] == 'game_timer':
                self.msg = data['message']
            elif data['type'] == 'redirect':
                if self.player_name == data['player_name']:
                    self.running = False
            else:
                if not self.initialized:
                    self.msg = data['msg']
                    self.ball.update({'x': data['ball_x'], 'y': data['ball_y']})
                    self.player1.update({'x': data['player1_x'], 'y': data['start_pos_y'], 'name': data['player_names'][0], 'width': data['bat_width'], 'height': data['bat_height']})
                    self.player2.update({'x': data['player2_x'], 'y': data['start_pos_y'], 'name': data['player_names'][1], 'width': data['bat_width'], 'height': data['bat_height']})
                    self.initialized = True
                else:
                    self.msg = data['msg']
                    self.ball.update({'x': data['ball_x'], 'y': data['ball_y']})
                    self.player1['score'] = data['points'][0]
                    self.player2['score'] = data['points'][1]

    async def handle_input(self, websocket):
        while self.running:
            key = self.stdscr.getch()
            if key == ord('q'):
                self.running = False
            elif key == curses.KEY_UP and self.player1['y'] > 0:
                self.player1['y'] -= 1
            elif key == curses.KEY_DOWN and self.player1['y'] < curses.LINES - self.player1['height']:
                self.player1['y'] += 1
            await websocket.send(json.dumps({
                'game': {
                    'game_id': self.game_id,
                    'player_id': self.player_id,
                    'player_y': [self.player1['y'], self.player2['y']]
                }
            }))
            await asyncio.sleep(0.05)

    def draw(self):
        self.stdscr.clear()
        self.stdscr.border(0)
        self.stdscr.addstr(0, 2, f"{self.player1['name']}: {self.player1['score']}")
        self.stdscr.addstr(0, curses.COLS - 12, f"{self.player2['name']}: {self.player2['score']}")
        self.stdscr.addstr(curses.LINES // 3, curses.COLS // 2 - len(self.msg) // 2, self.msg)
        self.stdscr.addch(int(self.ball['y']), int(self.ball['x']), 'O')
        for i in range(int(self.player1['height'])):
            self.stdscr.addch(int(self.player1['y']) + i, int(self.player1['x']), '|')
            self.stdscr.addch(int(self.player2['y']) + i, int(self.player2['x']), '|')
        self.stdscr.refresh()

    async def run(self):
        async with websockets.connect(f"{SERVER_URL}{self.game_id}/{self.player_id}/") as websocket:
            await websocket.send(json.dumps({
                'type': 'join',
                'player_name': self.player_name
            }))
            while self.running:
                self.draw()
                await asyncio.gather(
                    self.handle_messages(websocket),
                    self.handle_input(websocket)
                )
                await asyncio.sleep(1 / 30)

def main(stdscr, game_id, player_id, player_name):
    game = PongGameCLI(stdscr, game_id, player_id, player_name)
    asyncio.run(game.run())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pong CLI Client")
    parser.add_argument("game_id", type=int, help="Game ID to join")
    parser.add_argument("player_id", type=int, help="Player ID (0 or 1)")
    parser.add_argument("player_name", type=str, help="Player name")
    args = parser.parse_args()

    curses.wrapper(main, args.game_id, args.player_id, args.player_name)
