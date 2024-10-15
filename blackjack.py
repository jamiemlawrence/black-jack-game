import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card():
    def __init__(self, suit, rank):

        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        return self.rank + ' of ' + self.suit
    

class Deck():
    
    def __init__(self):
        # Creates the initial deck of 52 cards
        
        self.deck = []

        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()

        return "The deck has: " + deck_comp

    def shuffle(self):
        # Shuffles the existing deck of cards
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        # card passed in from Deck().deal --> single Card(suit,rank)
        self.cards.append(card)
        self.value += values[card.rank]

        # track aces
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips():

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet




def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except:
            print("Sorry please provide an integer")
        else:
            if chips.bet > chips.total:
                print('Sorry, you do not have enough chips! You have: {}'.format(chips.total))
            else:
                break

def hit(deck,hand):
    
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing
    
    while True:
        x = input('Hit or Stand? Enter h or s ')

        if x[0].lower() == 'h':
            hit(deck,hand)
        elif x[0].lower() == 's':
            print("Player stands, dealer's turn")
            playing = False
        else:
            print("Sorry, I did not understand that, please enter h or s only!")
            continue
        break

def show_some(player, dealer):

    # dealer.cards[1]

    # show only one of the dealer's cards
    print("\n Dealer's Hand: ")
    print("First card hidden!")
    print(dealer.cards[1])

    # show all (2 cards) of the player's hand/cards
    print("\n Player's hand: ")
    for card in player.cards:
        print(card)

def show_all(player,dealer):
    
    # show all the dealer's cards
    print("\n Dealer's hand: ",*dealer.cards, sep='\n')

    #calculate and display value of dealer's hand
    print(f"Value of Dealer's hand is: {dealer.value}")

    # show all the players cards
    print("\n Player's hand: ",*player.cards, sep='\n')

    #calculate and display value of player's hand
    print(f"Value of Player's hand is: {player.value}")

def player_busts(player,dealer,chips):
    print("PLAYER BUSTS!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("PLAYER WINS")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("PLAYER WINS! DEALER BUSTED")
    chips.win_bet()


def dealer_wins(player,dealer,chips):
    print("DEALER WINS")
    chips.lose_bet()

def push(player,dealer):
    print('Dealer and player tie! PUSH')


while True:
    
    print("Welcome to BlackJack!")

    # Create and shuffle deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the players chips
    player_chips = Chips()

    # prompt player for bet
    take_bet(player_chips)

    # Show cards, but keep one dealer card hidden
    show_some(player_hand,dealer_hand)

    while playing:
        
        # prompt for player to hit or stand
        hit_or_stand(deck,player_hand)

        # show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)

        # if players hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)

            break

    # if player hasnt busted, play dealers hand until dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck,dealer_hand)

        # Show all cards
        show_all(player_hand,dealer_hand)

        # run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)
    
    # inform player of their chips total
    print('\n Player total chips are at: {}'.format(player_chips.total))

    # ask to play again
    new_game = input("Would you like to play another hand? y/n ")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('Thank you for playing!')

    break


