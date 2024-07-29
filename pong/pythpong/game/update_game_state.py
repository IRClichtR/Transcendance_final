import random
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Game
from .constants import *

#   updates the state of the game
#   moves the ball and updates the ball position.
#   resets the position id ball hits any wall.
#   increase players points

def update_game_state(game_id):

    try:
        #get game instance
        game = Game.objects.get(game_id=game_id)
    except Game.DoesNotExist:
        return

    if game.start_play == False:
        game.msg = "Waiting for the opponent..."
        game.save()
        return
    
    if game.end_play == True:
        return
    
    game.msg = ""
    # Ball going to the right
    if game.ball_direction_x == 'positive': 
        # check if the ball is far from right wall
        if game.ball_x < (PLAYER2_START_X - (BALL_DIAMETER / 2) - game.ball_velocity_x):
            # Move ball towards right
            game.ball_x += game.ball_velocity_x * game.ball_speed
        # check if the ball is near the right wall : did it hit the left player?
        elif game.ball_x >= (PLAYER2_START_X - (BALL_DIAMETER / 2) - game.ball_velocity_x):
            #HIT!
            if game.player_y[1] - BALL_DIAMETER / 2 <= game.ball_y <= (game.player_y[1] + BAT_HEIGHT) + BALL_DIAMETER / 2:
            # Based on which part of the bat (4 parts), the ball has hit, the vertical direction of ball is updated.
                if (game.player_y[1] > game.ball_y >= game.player_y[1] - BALL_DIAMETER / 2):
                    game.ball_velocity_y += game.ball_velocity_y * CORNER_BAT
                    game.ball_speed *= CORNER_UP_SPEED
                    game.ball_direction_y = 'negative'
                elif (game.player_y[1] + BAT_HEIGHT * 0.25) > game.ball_y >= game.player_y[1]:
                    game.ball_velocity_y += game.ball_velocity_y * QUARTER_BAT
                    game.ball_speed *= QUARTER_UP_SPEED
                    game.ball_direction_y = 'negative'
                elif (game.player_y[1] + BAT_HEIGHT * 0.5) > game.ball_y >= (game.player_y[1] + BAT_HEIGHT * 0.25):
                    game.ball_velocity_y -= game.ball_velocity_y * MIDDLE_BAT
                    game.ball_direction_y = 'negative'
                elif (game.player_y[1] + BAT_HEIGHT * 0.75) > game.ball_y >= (game.player_y[1] + BAT_HEIGHT * 0.5):
                    game.ball_velocity_y -=  game.ball_velocity_y * MIDDLE_BAT
                    game.ball_direction_y = 'positive'
                elif (game.player_y[1] + BAT_HEIGHT) > game.ball_y >= (game.player_y[1] + BAT_HEIGHT * 0.75):
                    game.ball_velocity_y += game.ball_velocity_y * QUARTER_BAT
                    game.ball_speed *= QUARTER_UP_SPEED
                    game.ball_direction_y = 'positive'
                elif (game.player_y[1] + BAT_HEIGHT + BALL_DIAMETER / 2) >= game.ball_y > (game.player_y[1] + BAT_HEIGHT):
                    game.ball_velocity_y += game.ball_velocity_y * CORNER_BAT
                    game.ball_speed *= CORNER_UP_SPEED
                    game.ball_direction_y = 'positive'
                game.ball_direction_x = 'negative'
            #MISS!
            else:
                # If ball hits right wall, start ball from center position with default speed and direction
                game.ball_x = BALL_START_X
                game.ball_y = BALL_START_Y
                game.ball_velocity_x = BALL_START_VELOCITY_X
                game.ball_velocity_y = BALL_START_VELOCITY_Y
                game.ball_direction_x = random.choice(('positive', 'negative'))
                game.ball_direction_y = random.choice(('positive', 'negative'))
                game.ball_speed = BALL_SPEED
                # Increment left player's point
                game.points[0] += 1
                if (game.points[0] == MAX_POINT):
                    if game.game_type == 'final':
                        game.msg = f"{game.player_names[0]} Win the tournament!!!"
                    else:
                        game.msg = f"{game.player_names[0]} Win!"
                    game.winner = game.player_names[0]
                    game.end_play = True

    # Ball going to the left
    elif game.ball_direction_x == 'negative':
        # check if the ball is far from left wall
        if game.ball_x > (PLAYER1_START_X + BAT_WIDTH + (BALL_DIAMETER / 2) + game.ball_velocity_x):
            # Move ball towards left
            game.ball_x -= game.ball_velocity_x * game.ball_speed
        # check if the ball is near the left wall : did it hit the left player?
        elif game.ball_x <= (PLAYER1_START_X + BAT_WIDTH + (BALL_DIAMETER / 2) + game.ball_velocity_x):
            #HIT!
            if game.player_y[0] - BALL_DIAMETER / 2 <= game.ball_y <= (game.player_y[0] + BAT_HEIGHT) + BALL_DIAMETER / 2:
                # Based on which part of the bat (4 parts), the ball has hit, the vertical direction of ball is updated.
                if (game.player_y[0] > game.ball_y >= game.player_y[0] - BALL_DIAMETER / 2):
                    game.ball_velocity_y += game.ball_velocity_y * CORNER_BAT
                    game.ball_speed *= CORNER_UP_SPEED
                    game.ball_direction_y = 'negative'
                elif (game.player_y[0] + (BAT_HEIGHT * 0.25)) > game.ball_y >= game.player_y[0]:
                    game.ball_velocity_y += game.ball_velocity_y * QUARTER_BAT
                    game.ball_speed *= QUARTER_UP_SPEED
                    game.ball_direction_y = 'negative'
                elif (game.player_y[0] + (BAT_HEIGHT * 0.5)) > game.ball_y >= (game.player_y[0] + (BAT_HEIGHT * 0.25)):
                    game.ball_velocity_y -= game.ball_velocity_y * MIDDLE_BAT
                    game.ball_direction_y = 'negative'
                elif (game.player_y[0] + (BAT_HEIGHT * 0.75)) > game.ball_y >= (game.player_y[0] + (BAT_HEIGHT * 0.5)):
                    game.ball_velocity_y -= game.ball_velocity_y * MIDDLE_BAT
                    game.ball_direction_y = 'positive'
                elif (game.player_y[0] + BAT_HEIGHT) >= game.ball_y >= (game.player_y[0] + (BAT_HEIGHT * 0.75)):
                    game.ball_velocity_y += game.ball_velocity_y * QUARTER_BAT
                    game.ball_speed *= QUARTER_UP_SPEED
                    game.ball_direction_y = 'positive'
                elif (game.player_y[0] + BAT_HEIGHT + BALL_DIAMETER / 2) >= game.ball_y > (game.player_y[0] + BAT_HEIGHT):
                    game.ball_velocity_y += game.ball_velocity_y * CORNER_BAT
                    game.ball_speed *= CORNER_UP_SPEED
                    game.ball_direction_y = 'positive'
                game.ball_direction_x = 'positive'
            #MISS!    
            else:
                # If ball hits left wall, start ball from center position with default speed and direction
                game.ball_x = BALL_START_X
                game.ball_y = BALL_START_Y
                game.ball_velocity_x = BALL_START_VELOCITY_X
                game.ball_velocity_y = BALL_START_VELOCITY_Y
                game.ball_direction_x = random.choice(('positive', 'negative'))
                game.ball_direction_y = random.choice(('positive', 'negative'))
                game.ball_speed = BALL_SPEED
                # Increment right player's point
                game.points[1] += 1
                if (game.points[1] == MAX_POINT):
                    if game.game_type == 'final':
                        game.msg = f"{game.player_names[1]} Win the tournament!!!"
                    else:
                        game.msg = f"{game.player_names[1]} Win!"
                    game.winner = game.player_names[1]
                    game.end_play = True

    #ball going down
    if game.ball_direction_y == 'positive':
        # Check if ball is away from bottom wall
        if game.ball_y < (WINDOW_HEIGHT - (BALL_DIAMETER / 2) - game.ball_velocity_y):
            game.ball_y += game.ball_velocity_y
        # hit the wall   
        elif game.ball_y >= (WINDOW_HEIGHT - (BALL_DIAMETER / 2) - game.ball_velocity_y):
            game.ball_direction_y = 'negative'
    #ball going up
    elif game.ball_direction_y == 'negative':
        if game.ball_y > (BALL_DIAMETER / 2 + game.ball_velocity_y):
            game.ball_y -= game.ball_velocity_y
        elif game.ball_y <= (BALL_DIAMETER / 2 + game.ball_velocity_y):
            game.ball_direction_y = 'positive'

    game.save()

@database_sync_to_async
def update_player_y(game_id, player_id, player_y):
    game = Game.objects.get(game_id=game_id)
    game.player_y[player_id] = player_y[player_id]
    game.save()