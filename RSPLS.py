# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

import random

def name_to_number(name):
    # delete the following pass statement and fill in your code below

    num = -1

    if name == "rock":
        num = 0
    elif name == "Spock":
        num = 1
    elif name == "paper":
        num = 2
    elif name == "lizard":
        num = 3
    elif name == "scissors":
        num = 4
    else:
        print "Function name_to_number ERROR"

    return num
    

    # convert name to number using if/elif/else
    # don't forget to return the result!


def number_to_name(number):
    # delete the following pass statement and fill in your code below

    name = ""

    if number == 0:
        name = "rock"
    elif number == 1:
        name = "Spock"
    elif number == 2:
        name = "paper"
    elif number == 3:
        name = "lizard"
    elif number == 4:
        name = "scissors"
    else:
        print "Function number_to_name ERROR"

    return name 
    
    # convert number to a name using if/elif/else
    # don't forget to return the result!
    

def rpsls(player_choice): 
    # delete the following pass statement and fill in your code below
    
    # print a blank line to separate consecutive games

    print ""

    # print out the message for the player's choice

    print "Player choose " + player_choice

    # convert the player's choice to player_number using the function name_to_number()

    player_number = name_to_number(player_choice)

    # compute random guess for comp_number using random.randrange()

    computer_number = random.randrange(0, 5)

    # convert comp_number to comp_choice using the function number_to_name()

    computer_choice = number_to_name(computer_number)
    
    # print out the message for computer's choice

    print "Computer choose " + computer_choice

    # compute difference of comp_number and player_number modulo five

    mod = (computer_number - player_number) % 5

    # use if/elif/else to determine winner, print winner message

    if mod == 1 or mod == 2:
        print "Player wins!"
    elif mod == 0:
        print "Player and computer tie!"
    else:
        print "Computer wins!"

# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric



