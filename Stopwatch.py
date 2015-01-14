# template for "Stopwatch: The Game"

import simplegui

# define global variables

total_millisecond = 0
accept_cnt = 0
total_cnt = 0
score = 0
mode = 0

width = 300
height = 200

per_second = 1000

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    millisecond = second = minute = 0
    
    minute = (t / 10) / 60
    second = (t / 10) % 60
    millisecond = t % 10
    
    if whichLevel() == "Easy":
        if second >= 10:
            return str(minute) + ":" + str(second) + "." + str(millisecond)
        else:
            return str(minute) + ":0" + str(second) + "." + str(millisecond)
    elif whichLevel() == "Medium":
        if second >= 10:
            return str(minute) + ":" + str(second) + "." + "*"
        else:
            return str(minute) + ":0" + str(second) + "." + "*"
    else:
        return str(minute) + ":" + str(second / 10) + "*.*"
    
def judge(t):
    global accept_cnt, total_cnt, score
    
    if t > 10 and t % 10 == 0:
        accept_cnt += 1
    total_cnt += 1
    score = float(accept_cnt) / float(total_cnt) * 100.0
    
def whichLevel():
    global mode
    
    if mode == 0:
        level = "Easy"
    elif mode == 1:
        level = "Medium"
    else:
        level = "Hard"
        
    return level

# define event handlers for buttons; "Start", "Stop", "Reset"

def start():
    timer.start()
    
def stop():
    global total_millisecond
    timer.stop()
    judge(total_millisecond)
    
def reset():
    global total_millisecond, accept_cnt, total_cnt, score, mode
    timer.stop()
    accept_cnt = 0
    total_cnt = 0
    total_millisecond = 0
    score = 0
    
def easy():
    global mode
    mode = 0
    
def medium():
    global mode
    mode = 1
    
def hard():
    global mode
    mode = 2


# define event handler for timer with 0.1 sec interval

def update():
    global total_millisecond
    total_millisecond += 1 

# define draw handler

def draw(canvas):
    global accept_cnt, total_cnt, score
    
    canvas.draw_text(format(total_millisecond), (width / 3, height / 2), 36, "White")    
    canvas.draw_text(str(accept_cnt) + "/" + str(total_cnt), (250, 25), 24, "Green")
    canvas.draw_text("Score: " + str(int(score)) + "%", (25, 25), 24, "Red")
    canvas.draw_text("Level: " + whichLevel(), (width / 3 + 50, height / 2 + 30), 18, "White")
    
# create frame

frame = simplegui.create_frame("Stopwatch", width, height)

# register event handlers

start_button = frame.add_button("Start", start, 100)
stop_button = frame.add_button("Stop", stop, 100)
reset_button = frame.add_button("Reset", reset, 100)
easy_button = frame.add_button("Easy", easy, 100)
medium_button = frame.add_button("Medium", medium, 100)
hard_button = frame.add_button("Hard", hard, 100)

frame.set_draw_handler(draw)

timer = simplegui.create_timer(per_second / 10, update)

# start frame

frame.start()

# Please remember to review the grading rubric
