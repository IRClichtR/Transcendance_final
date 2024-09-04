# Game global variables
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
BAT_WIDTH = 10
BAT_HEIGHT = 100
PLAYER1_START_X = 0
PLAYER_START_Y = WINDOW_HEIGHT / 2 - BAT_HEIGHT / 2
PLAYER2_START_X = WINDOW_WIDTH - PLAYER1_START_X - BAT_WIDTH
BALL_START_X = WINDOW_WIDTH / 2
BALL_START_Y = WINDOW_HEIGHT / 2
BALL_START_VELOCITY_X = 3
BALL_START_VELOCITY_Y = 1
BAT_MOVEMENT_SPEED = 20
BALL_DIAMETER = 20
MAX_POINT = 3
DIRECTION_CHOICES = [('positive', 'negative')]

# To adjust how velocity_x is modify
BALL_SPEED = 3
CORNER_BAT = 5 #Up velocity_y + up game_speed
MIDDLE_BAT = 0.5 #Reminder : minor velocity_y
QUARTER_BAT = 3 #up velocity_y
CORNER_UP_SPEED = 1.5
QUARTER_UP_SPEED = 1.25
FPS = 30
DELAY = 1 / 30