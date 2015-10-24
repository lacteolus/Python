import simplegui
import random
#import time

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
outcome_result = ""
score = 0

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

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        self.list_of_cards = ''
        for i in range(len(self.hand)):
            self.list_of_cards += str(self.hand[i].get_suit() + self.hand[i].get_rank() + " ")
        return self.list_of_cards

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        self.result = 0
        for i in range(len(self.hand)):
            self.result += VALUES[self.hand[i].get_rank()]
        for i in range(len(self.hand)):
            if ('A' in self.hand[i].get_rank()) and (21 - self.result) >= 10:
                self.result += 10
        return self.result
   
    def draw(self, canvas, pos):
        for i in range(len(self.hand)):
            self.hand[i].draw(canvas, pos)
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck_of_cards = []
        for i in range(len(SUITS)):
            for j in range(len(RANKS)):
                self.deck_of_cards.append(Card(SUITS[i], RANKS[j]))

    def shuffle(self):
        random.shuffle(self.deck_of_cards)

    def deal_card(self):
        return self.deck_of_cards.pop(-1)
    
    def __str__(self):
        self.list_of_deck = ''
        for i in range(len(self.deck_of_cards)):
            self.list_of_deck += str(self.deck_of_cards[i].get_suit() + self.deck_of_cards[i].get_rank() + " ")
        return self.list_of_deck 

    
#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, new_deck, dealer_hand, score, outcome_result
    if in_play:
        outcome_result = "You lost this round. Press <Deal> button again"
        outcome = "New deal?"
        score -= 1
        in_play = False
        return
    new_deck = Deck()
    new_deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(new_deck.deal_card())
    dealer_hand.add_card(new_deck.deal_card())
    player_hand.add_card(new_deck.deal_card())
    dealer_hand.add_card(new_deck.deal_card())
    outcome = "Hit or stand?"
    in_play = True
    outcome_result = "In play"

def hit():
    global player_hand, new_deck, outcome, in_play, outcome_result, score
    if player_hand.get_value() <= 21:
        player_hand.add_card(new_deck.deal_card())
    if player_hand.get_value() > 21:
        in_play = False
        outcome = "New deal?"
        outcome_result = "You have busted. Dealer won"
        score -= 1
       
def stand():
    global player_hand, dealer_hand, new_deck, outcome, in_play, score, outcome_result
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(new_deck.deal_card())
        if dealer_hand.get_value() > 21:
            outcome_result = "Dealer has busted. You won"
            outcome = "New deal?"
            score -= 1
        else:
            if player_hand.get_value() > dealer_hand.get_value():
                outcome = "New deal?"
                outcome_result = "Player won"
                score += 1
            else:
                outcome = "New deal?"
                outcome_result = "Dealer won"
                score -= 1
        in_play = False
# draw handler    
def draw(canvas):
    global player_hand, frame, dealer_hand, outcome, score, outcome_result
    #draw palyer's hand
    canvas.draw_text("Player's hand", (10, 380), 30, 'White')
    for i in range(len(player_hand.hand)):
        player_hand.hand[i].draw(canvas, [CARD_SIZE[0] * i + 10, 400])
    
    #draw dealer's hand
    canvas.draw_text("Dealer's hand", (10, 180), 30, 'White')
    dealer_hand.hand[0].draw(canvas, [10, 200])
    canvas.draw_text(outcome, (10, 30), 30, 'White')
    if not in_play:
        for i in range(1, len(dealer_hand.hand)):
            dealer_hand.hand[i].draw(canvas, [CARD_SIZE[0] * i + 10, 200])
            canvas.draw_text(str(dealer_hand.get_value()), (500, 180), 30, 'White')
    else:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [10 + CARD_SIZE[0] + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    canvas.draw_text(str(player_hand.get_value()), (500, 380), 30, 'White')
    canvas.draw_text("Total: " + str(score), (450, 30), 30, 'White')
    canvas.draw_text(str(outcome_result), (10, 570), 30, 'White')

    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
