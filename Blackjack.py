# Mini-project #6 - Blackjack

import simpleguitk as simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
WIDTH = 600
HEIGHT = 600

in_play = False
outcome = ""
current = ""
score = 0
player = []
dealer = []
deck = []

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos, face_down):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE,
                          [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)
        if face_down == True:
            card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
            canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE,
                              [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]],
                              CARD_BACK_SIZE)

# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        string = "Hand contains "
        for tmp in self.cards:
            string += str(tmp) + ' '
        return string

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        ans = 0
        ace = False
        for card in self.cards:
            ans += VALUES.get(card.get_rank())
            if card.get_rank() == 'A':
                ace = True
        if ace and ans + 10 <= 21:
            return ans + 10
        else:
            return ans
        
    def hit(self, deck):
        self.cards.append(deck.deal_card())
    
    def bursted(self):
        if self.get_value() > 21:
            return True
        else:
            return False
        
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.cards:
            pos[0] = 50 + 80 * self.cards.index(card)
            card.draw(canvas, pos, False)
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.cards.append(card)
        self.shuffle()

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()
    
    def __str__(self):
        # return a string representing the deck
        string = "Deck contains "
        for tmp in self.cards:
            string += str(tmp) + ' '
        return string

#define event handlers for buttons
def deal():
    global outcome, in_play
    global player, dealer, deck, score
    
    if in_play:
        score -= 1
    player = Hand()
    dealer = Hand()
    deck = Deck()
    
    outcome = ""
    current = "Hit or Stand?" 
    in_play = True
    
    player.hit(deck)
    dealer.hit(deck)
    player.hit(deck)
    dealer.hit(deck)

def hit():
    global in_play, outcome, current, score
 
    # if the hand is in play, hit the player
    if in_play:
        player.hit(deck)
        # if busted, assign a message to outcome, update in_play and score
        if player.bursted():
            outcome = "You went bust!"
            current = "New deal?"
            in_play = False
            score -= 1
        if player.get_value() == 21:
            outcome = "You got BLACKJACK!"
            current = "New deal?"
            in_play = False
            score += 1
       
def stand():
    global in_play, outcome, current, score 
    
    if in_play:
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        while dealer.get_value() < 17:
            dealer.hit(deck)
            if dealer.bursted():
                outcome = "Dealer went bust!"
                score += 1
        # assign a message to outcome, update in_play and score
        if not dealer.bursted():
            if dealer.get_value() > player.get_value():
                outcome = "Dealer won."
                score -= 1
            elif dealer.get_value() == player.get_value():
                outcome = "It's a tie."
            else:
                outcome = "You won."
                score += 1
    in_play = False
    current = "New deal?"

# draw handler    
def draw(canvas):
    global in_play, score, outcome, current
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Score: " + str(score), (400, 100), 26, "Black")
    canvas.draw_text("Blackjack", (70, 100), 38, "Blue")
    canvas.draw_text("Dealer", (70, 180), 26, "Black")
    canvas.draw_text(outcome, (220, 180), 26, "Black")
    canvas.draw_text("Player", (70, 380), 26, "Black")
    canvas.draw_text(current, (220, 380), 26, "Black")
    
    dealer.draw(canvas, [0, 200])
    player.draw(canvas, [0, 400])
    
    card = Card("S", "A")
    if in_play:
        card.draw(canvas, [50, 200], True)


# initialization frame
frame = simplegui.create_frame("Blackjack", WIDTH, HEIGHT)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
