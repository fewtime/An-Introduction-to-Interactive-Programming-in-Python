# Implementation of classic arcade game Pong

import simpleguitk as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
UP = False
DOWN = True
PADDLE_SPEED = 5
BALL_ACCELERATED_SPEED = 1.1
BALL_HOR_RANGE = (120, 240)
BALL_VER_RANGE = (60, 180)
REFRESH_RATE = 60

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
ball_dir = None
ball_init = None

paddle1_pos = [PAD_WIDTH / 2, HEIGHT / 2 - 1]
paddle1_vel = [0, 0]
paddle2_pos = [WIDTH - 1 - PAD_WIDTH / 2, HEIGHT / 2 - 1]
paddle2_vel = [0, 0]

left_score = 0
right_score = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(hor_direction, ver_direction):
    global ball_pos, ball_vel, ball_init # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    # generate the horizontal velocity
    if hor_direction == RIGHT:
        ball_vel[0] = random.randrange(BALL_HOR_RANGE[0], BALL_HOR_RANGE[1]) / REFRESH_RATE
    else:
        ball_vel[0] = -random.randrange(BALL_HOR_RANGE[0], BALL_HOR_RANGE[1]) / REFRESH_RATE
    # generate the vertical velocity             
    if ver_direction == UP:
        ball_vel[1] = -random.randrange(BALL_VER_RANGE[0], BALL_VER_RANGE[1]) / REFRESH_RATE
    else:
        ball_vel[1] = random.randrange(BALL_VER_RANGE[0], BALL_VER_RANGE[1]) / REFRESH_RATE
        
    ball_init = True

def update_ball():
    global ball_pos, ball_vel
    check_for_collision()
    ball_pos = [ball_pos[0] + ball_vel[0], ball_pos[1] + ball_vel[1]]
    
def check_for_collision():
    global ball_pos, ball_vel, ball_dir, paddle1_pos, paddle2_pos
    
    # check for left paddle
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH and\
        ball_pos[1] >= paddle1_pos[1] - HALF_PAD_HEIGHT and\
        ball_pos[1] <= paddle1_pos[1] + HALF_PAD_HEIGHT:
            ball_vel[0] *= -BALL_ACCELERATED_SPEED
    
    # check for right paddle
    if ball_pos[0] + BALL_RADIUS >= WIDTH - 1 - PAD_WIDTH and\
        ball_pos[1] >= paddle2_pos[1] - HALF_PAD_HEIGHT and\
        ball_pos[1] <= paddle2_pos[1] + HALF_PAD_HEIGHT:
            ball_vel[0] *= -BALL_ACCELERATED_SPEED
    
    # check for button
    if ball_pos[1] - BALL_RADIUS <= 0:
        ball_vel[1] *= -1
    
    # check for float
    if ball_pos[1] + BALL_RADIUS >= HEIGHT - 1:
        ball_vel[1] *= -1
    
    # (ball drop in left size)point for left
    if ball_pos[0] < 0:
        ball_dir = LEFT
    
    # (ball drop in right size)point for right
    if ball_pos[0] > WIDTH:
        ball_dir = RIGHT
          
def update_paddle():
    global paddle1_pos, paddle1_vel, paddle2_pos, paddle2_vel
    
    # paddle1 detection
    paddle1_pos[1] += paddle1_vel[1]
    if paddle1_pos[1] - HALF_PAD_HEIGHT <= 0:
        paddle1_pos[1] = HALF_PAD_HEIGHT
    if paddle1_pos[1] + HALF_PAD_HEIGHT >= HEIGHT - 1:
        paddle1_pos[1] = HEIGHT - 1 - HALF_PAD_HEIGHT
        
    # paddle2 detection
    paddle2_pos[1] += paddle2_vel[1]
    if paddle2_pos[1] - HALF_PAD_HEIGHT <= 0:
        paddle2_pos[1] = HALF_PAD_HEIGHT
    if paddle2_pos[1] + HALF_PAD_HEIGHT >= HEIGHT - 1:
        paddle2_pos[1] = HEIGHT - 1 - HALF_PAD_HEIGHT
        
def cal_score():
    global left_score, right_score, ball_dir, ball_init
    
    if ball_dir == LEFT:
        ball_dir = None
        right_score += 1
        ball_init = False
        
    if ball_dir == RIGHT:
        ball_dir = None
        left_score += 1
        ball_init = False
    

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global left_score, right_score  # these are ints
    
    paddle1_pos = [PAD_WIDTH / 2, HEIGHT / 2 - 1]
    paddle1_vel = [0, 0]
    paddle2_pos = [WIDTH - 1 - PAD_WIDTH / 2, HEIGHT / 2 - 1]
    paddle2_vel = [0, 0]
    
    left_score = 0
    right_score = 0
    
    spawn_ball(random.choice([LEFT,  RIGHT]), [UP, DOWN])
    ball_dir = None
    
    ball_init = True

def draw(canvas):
    global left_score, right_score, paddle1_pos\
        ,paddle2_pos, ball_pos, ball_vel, ball_init
      
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_init == False:
        spawn_ball(random.choice([LEFT, RIGHT]),
                   random.choice([UP, DOWN]))
    update_ball()
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    update_paddle()
    
    # draw paddles
    
    canvas.draw_polygon([
                         (0, paddle1_pos[1] - HALF_PAD_HEIGHT), 
                         (PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT),
                         (PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT),
                         (0, paddle1_pos[1] + HALF_PAD_HEIGHT)
                        ], 1, "White", "White")
    canvas.draw_polygon([
                         (WIDTH - 1, paddle2_pos[1] - HALF_PAD_HEIGHT),
                         (WIDTH - 1 - PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT),
                         (WIDTH - 1 - PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT),
                         (WIDTH - 1, paddle2_pos[1] + HALF_PAD_HEIGHT)
                        ], 1, "White", "White")
    
    # draw scores
    cal_score()
    canvas.draw_text(str(left_score), (WIDTH / 3, HEIGHT / 3), 36, "Green")
    canvas.draw_text(str(right_score), (2 * WIDTH / 3, HEIGHT / 3), 36, "Red")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel[1] = -PADDLE_SPEED
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel[1] = PADDLE_SPEED
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = -PADDLE_SPEED
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = PADDLE_SPEED
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['s']:
        paddle1_vel[1] = 0
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
new_game_button = frame.add_button("Reset", new_game)

# start frame
new_game()
frame.start()

