# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# variables definition
secert_number = 0
guess_number = 0
guesses_cnt = 0
total_guesses = 0

# helper function to start and restart the game
def new_game(low, high):
    # initialize global variables used in your code here

    global secert_number, guess_number, guesses_cnt, total_guesses
    secert_number = random.randrange(low, high)
    total_guesses = math.ceil(math.log(high - low, 2))
    guesses_cnt = 0

    print "New game. Range is from " + str(low) + " to " + str(high)
    print "Number of remaining guesses is " + str(total_guesses)
    print ""


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    new_game(0, 100)
    

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    new_game(0, 1000)
    
    
def input_guess(guess):
    global guesses_cnt, guess_number

    # judge textbox's content
    try:
        guess_number = int(guess)
    except:
        print "Please enter an integer!"
        print ""
        return None
    
    guesses_cnt += 1
    print "Guess was", str(int(guess_number))
    
    # judge the number
    binary_search()

def binary_search():
    global guesses_cnt, guess_number, total_guesses, secert_number

    end_of_game = False
    counter = total_guesses - guesses_cnt

    if counter and (not end_of_game):
        if guess_number == secert_number:
            print "Correct!"
            end_of_game = True
        elif guess_number < secert_number:
            print "Higher!"
        else:
            print "Lower!"
    else:
        if guess_number == secert_number:
            print "Correct!"
        else:
            print "GAME OVER"
        end_of_game = True

    print ""

    if end_of_game:
        new_game(0, 100)

# create frame

f = simplegui.create_frame("Guess the number", 100, 200)

# register event handlers for control elements and start frame
f.add_button("Range is [0, 100)", range100, 200)
f.add_button("Range is [0, 1000)", range1000, 200)
f.add_input("Enter a guess", input_guess, 200)

# call new_game 
f.start()
new_game(0, 100)


# always remember to check your completed program against the grading rubric

