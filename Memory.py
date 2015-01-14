# implementation of card game - Memory

import simplegui
import random

CARD_NUMBER = 16

WIDTH = 800
HEIGHT = 100
CARD_WIDTH = WIDTH // CARD_NUMBER

random_list = []
expose = [False] * 16
mouse_state = 0
pre_one = None
pre_two = None
latest = None
turn_cnt = 0

# helper function to initialize globals
def new_game():
    global random_list, expose, mouse_state, turn_cnt, pre_one, pre_two
    
    expose = [False] * 16   
    random_list = range(1, 9) + range(1, 9)
    random.shuffle(random_list)
    mouse_state = 0
    pre_one = pre_two = None
    turn_cnt = 0
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global expose, mouse_state, pre_one, pre_two, latest, turn_cnt
    
    latest = pos[0] // CARD_WIDTH
 
    if mouse_state == 0:
        mouse_state = 1
        expose[latest] = True
        pre_one = latest
    elif mouse_state == 1:
        if expose[latest] == False:
            mouse_state = 2
            expose[latest] = True
            turn_cnt += 1
            pre_two = latest
    else:
        if expose[latest] == False:
            mouse_state = 1
            expose[latest] = True
            if random_list[pre_one] != random_list[pre_two]:
                expose[pre_one] = expose[pre_two] = False
                pre_two = None
            pre_one = latest
                     
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global expose, random_list, turn_cnt
    for i in range(0, CARD_NUMBER):
        canvas.draw_text(str(random_list[i]),
                         (i * CARD_WIDTH + CARD_WIDTH // 4, HEIGHT // 2 + HEIGHT // 4),
                         54, "White")
        if expose[i] == False:
            canvas.draw_polygon([
                                [i * CARD_WIDTH, 0],[(i + 1) * CARD_WIDTH, 0],
                                [(i + 1) * CARD_WIDTH, HEIGHT],[i * CARD_WIDTH, HEIGHT]],
                                1, "Yellow", "Green")
    
    label.set_text("Turns = " + str(turn_cnt))

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
