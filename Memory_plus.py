# implementation of card game - Memory

import simpleguitk as simplegui
import math
import random

card_per_row = 16
card_per_col = 1
card_number = 20

WIDTH = 600
HEIGHT = 400
card_width = WIDTH // card_per_row
card_height = HEIGHT // card_per_col
font_size = 0

warming_str = ""

random_list = []
expose = []
mouse_state = 0
pre_one = None
pre_two = None
latest = None
turn_cnt = 0

# helper function to initialize globals
def new_game():
    global warming_str
    global card_number, card_per_row, card_per_col, card_width, card_height, font_size
    global random_list, expose, mouse_state, turn_cnt, pre_one, pre_two, latest
    
    card_per_col = (int)(math.floor(math.sqrt(card_number)))
    if (card_number // card_per_col) * card_per_col == card_number:
        card_per_row = int(card_number // card_per_col)
    else:
        for card_per_col in range(card_per_col, 0, -1):
            card_per_row = int(card_number // card_per_col)
            if card_per_row * card_per_col == card_number:
                break
    
    card_width = (int)(math.floor(WIDTH // card_per_row))
    card_height = (int)(math.floor(HEIGHT // card_per_col))
   
    font_size = (card_width * card_height) // 250
    if font_size < 10:
        font_size = 10
    elif font_size > 150:
        font_size = 150
    
    expose = [[False for x in range(card_per_row)] for y in range(card_per_col)]
    
    temp_list = range(1, (card_number // 2) + 1) + range(1, (card_number // 2) + 1)
    random.shuffle(temp_list)
    random_list = [[0 for x in range(card_per_row)] for y in range(card_per_col)]
    
    for i in range(0, card_per_col):
        for j in range(0, card_per_row):
            random_list[i][j] = temp_list[i * card_per_row + j]
    
    mouse_state = 0
    pre_one = [0] * 2
    pre_two = [0] * 2
    latest = [0] * 2
    turn_cnt = 0
    
    warming_str = ""

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global expose, mouse_state, pre_one, pre_two, latest, turn_cnt
    
    latest[1] = pos[0] // card_width
    latest[0] = pos[1] // card_height

    
    if mouse_state == 0:
        mouse_state = 1
        expose[latest[0]][latest[1]] = True
        pre_one[0] = latest[0]
        pre_one[1] = latest[1]
    elif mouse_state == 1:
        if expose[latest[0]][latest[1]] == False:
            mouse_state = 2
            expose[latest[0]][latest[1]] = True
            turn_cnt += 1
            pre_two[0] = latest[0]
            pre_two[1] = latest[1]
    else:
        if expose[latest[0]][latest[1]] == False:
            mouse_state = 1
            expose[latest[0]][latest[1]] = True
            if random_list[pre_one[0]][pre_one[1]] != random_list[pre_two[0]][pre_two[1]]:
                expose[pre_one[0]][pre_one[1]] = expose[pre_two[0]][pre_two[1]] = False
                pre_two = [0] * 2
            pre_one[0] = latest[0]
            pre_one[1] = latest[1]
            
def input_card_number(set_card_number):
    global card_number, warming_str
    try:
        card_number = int(set_card_number)
        assert not(card_number % 2)
        new_game()
    except AssertionError:
        warming_str = "card number must be an even"
    except:
        warming_str = "card number must be integer"
                     
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global expose, random_list, turn_cnt

    for i in range(0, card_per_col):
        for j in range(0, card_per_row):
            canvas.draw_text(str(random_list[i][j]),
                             (j * card_width + card_width // 2 - card_width // 4,
                              i * card_height + card_height // 2 + card_height // 4),
                             font_size, "White")
            if expose[i][j] == False:
                canvas.draw_polygon([
                                     [j * card_width, i * card_height],
                                     [(j + 1) * card_width, i * card_height],
                                     [(j + 1) * card_width, (i + 1) * card_height],
                                     [j * card_width, (i + 1) * card_height]
                                     ],1, "Yellow", "Green")
    
    label.set_text("Turns = " + str(turn_cnt))
    warming_label.set_text(warming_str)

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Reset", new_game)
frame.add_input("Enter the card number", input_card_number, 200)
label = frame.add_label("Turns = 0")
warming_label = frame.add_label("")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
