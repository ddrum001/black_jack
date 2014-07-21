# Coding Challenge - Blackjack

import random

# initialize some useful global variables
in_play = False	# boolean used to see if a hand is currently in play
outcome = "Welcome to Blackjack: New Deal?"	# string to keep track of various outcomes
score = 100	# initial chip-count
bet = 1
end_of_hand_string = " Hit d for a new deal or q to quit: " # commonly used string

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}

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

    def draw(self):
        print(self.suit + self.rank),
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []	# create Hand object
        self.ace = False
        self.value = 0

    def __str__(self):
        # return a string representation of a hand
        s =  "Hand contains "
        for i in range(len(self.cards) ):
            s += str(self.cards[i]) + " "
        return s
            
    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand
        if card.rank == 'A':
            self.ace = True
        self.value += VALUES[card.rank]
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand
        if (self.ace == True and self.value < 12):
            return self.value + 10
        else:
            return self.value
            
    def draw(self, hidden):
        # draw a hand on the canvas, use the draw method for cards
		# start card is set to 1 for the dealer when the hole card is hidden and in play still
        if hidden == True and in_play == True:
			start_card = 1
        else:
			start_card = 0            
        for i in range(start_card, len(self.cards) ):
            self.cards[i].draw()

            
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object with two nested for loops
        self.deck = []
        for i in range(4):
            for j in range(13):
                self.deck.append(Card(SUITS[i], RANKS[j]) )
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()	# deal a card object from the deck
        
    def __str__(self):
        s =  "Deck contains "
        for i in range(len(self.deck) ):
            s += str(self.deck[i]) + " "
        return s	# return a string representing the deck
    
# define event handlers
def set_bet():
	global bet
	print "How many chips would you like to bet? (Min. 1 chip): "
	bet = 0
	while bet == 0:
		b = raw_input()	# place-holder for input to do 2 comparisons below
		try:
			b = int(b)
		except ValueError:
			b = 0
		if b >= 1 and b <= score:
			bet = b
		else:
			print "Invalid bet...Must be integer between 1 and your chip total of " + str(score) + ". Enter again: "

# handler for dealing
def deal():
	global outcome, in_play, deck, playHand, dealerHand, score, bet
	deck = Deck()
	deck.shuffle()
	set_bet()
	playHand = Hand()
	dealerHand = Hand()
	playHand.add_card(deck.deal_card() )
	playHand.add_card(deck.deal_card() )
	dealerHand.add_card(deck.deal_card() )
	dealerHand.add_card(deck.deal_card() )
	outcome = "Hit or Stand? Enter h or s: "
	if in_play == True:
		print "You folded. Better luck next time! "
		score -= bet
	in_play = True
	draw_and_prompt()

# handler for hitting
def hit():
	global in_play, score, deck, playHand, dealerHand, outcome, bet
	# if the hand is in play, hit the player
	if in_play == True:
		playHand.add_card(deck.deal_card() )
		# if busted, assign a message to outcome, update in_play and score
		if playHand.get_value() > 21:
			outcome = "You have busted." + end_of_hand_string
			score -= bet
			in_play = False
	else:
		outcome = "Can't hit." + end_of_hand_string
	draw_and_prompt()

# handler for standing
def stand():
	global in_play, score, deck, playHand, dealerHand, outcome, bet
	# if hand is in play, repeatedly hit dealer until his hand has value 17 or more
	if in_play == False:
		if playHand.get_value() > 0:
			outcome = "Can't stand. " + end_of_hand_string
	else:
		while dealerHand.get_value() < 17:
			dealerHand.add_card(deck.deal_card() )
			#outcome = "Dealer " + str(dealerHand) + str(dealerHand.get_value() )
			# assign a message to outcome, update in_play and score    
		if dealerHand.get_value() > 21:
			outcome = "Congrats! The dealer has busted." + end_of_hand_string
			score += bet
			in_play = False
		elif playHand.get_value() > dealerHand.get_value():
			outcome = "Congrats! You beat the dealer." + end_of_hand_string
			score += bet
			in_play = False
		elif playHand.get_value() == dealerHand.get_value():
			outcome = "Push...You tied the dealer." + end_of_hand_string
			in_play = False
		else:
			outcome = "Sorry! The dealer has won." + end_of_hand_string
			score -= bet
			in_play = False
	draw_and_prompt()

# draw handler to print to screen and prompt user
def draw_and_prompt():
	print
	print("Player Hand: "),
	playHand.draw(False)
	print " --- for a total of " + str(playHand.get_value() )
	print("Dealer Hand: "),
	dealerHand.draw(True)  	
	if in_play == False:
		print  " --- for a total of " + str(dealerHand.get_value() )
		print "Chip Total: " + str(score)
	else: 
		print "    --- with another card hidden in the hole"
	print outcome
	read_input()
	
# careful exit to allow for extra confirmation
def careful_exit():
	print "Are you sure you want to quit? (y or n): "
	if raw_input() == "y":
		exit()
	else:
		read_input()

# input commands, correcting case if needed
def read_input():
	user_input = raw_input().lower()
	if user_input == 'h':
		hit()
	elif user_input == 's':
		stand()
	elif user_input == 'd':
		deal()
	elif user_input == 'q':
		careful_exit()
	else:
		print "Invalid Input...Enter h, s, d, or q: "
		read_input()

def print_rules():
	print "Welcome to Blackjack!", "\n", "Developed by David E Drummond for the Insight Data Engineering Coding Challenge"
	print
	print "Here are the rules for this variation of black jack: Each player is dealt two card initially"
	print "Try to get as close to 21 without going over, scoring higher than the dealer to win"
	print "Take an extra card by hitting or keep your cards by standing."
	print "The dealer hides one card, not hitting or standing until after you choose."
	print "The dealer hits until 17 (including a 'soft' 17 with an ace)."
	print "Aces can count for 1 or 11, all face cards are 10"
	print "Suits: S = Spades, D = Diamonds, C = Clubs, H = Hearts"
	print "Good Luck!  Hit q at any time to quit." + "\n"

# initialize deck, shuffle, and start game
deck = Deck()
deck.shuffle()
playHand = Hand()
dealerHand = Hand()
print_rules()
deal()