import random
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Clubs', 'Spades', 'Diamonds']

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank in 'A':
            return 1,11
        else:
            return int(self.rank)
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = []
        for rank in ranks:
            for suit in suits:
                c = Card(rank, suit)
                self.cards.append(c)
    
    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if not self.cards:
            raise Exception("No more cards: empty deck!")
        card = self.cards.pop()
        return card
    
    def __str__(self):
        cards = []
        for c in self.cards:
            cards.append(str(c))
        return str(cards)

class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.dealer = dealer

    def add(self, card):
        self.cards.append(card)

    def value(self):
        value = 0
        aces = 0
        for card in self.cards:
            if card.rank == 'A':
                # no. of (length of) aces
                aces += 1
            else:
                value += card.value()
        for a in range(aces):
            if value + 11 <= 21:
                value += 11
            else:
                value += 1
        return value
    
    def __str__(self):
        cards = [str(c) for c in self.cards]
        return str(cards)

class Player:
    def __init__(self, name, budget, strategy):
        self.name = name
        self.budget = budget
        self.hand = Hand()
        self.state = 'playing'
        self.strategy = strategy
        self.cards = []
        self.bet = 0

    def place_bet(self):
        bet_amount = min(100, self.budget)
        self.budget -= bet_amount
        self.bet = bet_amount
        return bet_amount
    
    def win(self):
        self.budget += 2 * self.bet
        self.bet = 0

    def lose(self):
        self.budget -= self.bet
        penalty = 100
        self.budget -= penalty
        self.bet = 0

    def push(self):
        self.budget += self.bet
        self.bet = 0

    def play(self, dealer_hand):
        while not self.is_busted() and self.state == 'playing':
            action = self.strategy(self.hand, dealer_hand)
            if action == 'hit':
                self.hit(dealer_hand.draw_card())
            else:
                self.state = 'standing'

    def hit(self, card):
        self.hand.add(card)

    def is_broke(self):
        return self.budget <= 0

    def is_busted(self):
        return self.hand.value() > 21
    
    def __str__(self):
        return f"Player {self.name} with buget {self.budget} and hand {self.hand}"
    
class Dealer:
    def __init__(self, budget, deck):
        self.budget = budget
        self.hand = Hand(dealer=True)
        self.state = 'playing'
        self.deck = deck
    
    def shuffle(self):
        self.deck.shuffle()

    def draw_card(self):
        card = self.deck.draw_card()
        self.hand.add(card)
        return card
    
    def is_busted(self):
        return self.hand.value() > 21
    
    def __str__(self):
        return f"Dealer with hand {self.hand}"

class Game:
    def __init__(self, dealer, players, log):
        self.dealer = dealer
        self.players = players
        self.log = log

    def open(self):
        self.dealer.shuffle()
        for player in self.players:
           player.place_bet()
        
        for player in self.players:
            for p in range(2):
                player.hit(self.dealer.draw_card())
            self.log.append(f"{player.name} has been dealt: {player.hand}")
        # deal two cards to dealer
        for c in range(2):
            self.dealer.draw_card()

    def determine_winner(self, player):
        player_value = player.hand.value()
        dealer_value = self.dealer.hand.value()

        if player.is_busted():
            player.lose()
            return
        
        if self.dealer.is_busted():
            player.win()
            return
            
        if player_value > dealer_value:
            player.win()
        elif player_value < dealer_value:
            player.lose()
        else:
            player.push()

    def close(self):
        for player in self.players:
            self.determine_winner(player)
        self.log.append("Game closed.")

    def run(self):
        self.open()
        self.log.append("Game started.")
        # player's turn
        for player in self.players:
            player.play(self.dealer)
            self.log.append(f"{player.name} ends turn with: {player.hand}")

        # dealer's turn
        while not self.dealer.is_busted() and self.dealer.hand.value() < 17:
            self.dealer.draw_card()
            self.log.append(f"Dealer hits: {self.dealer.hand}")
        
        self.close()
    
    def history(self):
        return "\n".join(self.log)
    
    def is_finished(self):
        for player in self.players:
            if player.state not in ['standing', 'busted']:
                return False
        return True

def strategy1(player_hand, dealer_hand):
    player_value = player_hand.value()
    
    if player_value <= 11:
        return 'hit'  
    elif player_value >= 17:
        return 'stand'  
    else:
        # For values 12-16, hit if dealer shows 7 or higher
        if dealer_hand.hand and dealer_hand.hand[0].value() >= 7:
            return 'hit'
        else:
            return 'stand'

def strategy2(player_hand, dealer_hand):
    player_value = player_hand.value()
    
    if player_value <= 14:
        return 'hit'  
    elif player_value >= 19:
        return 'stand'  
    else:
        # For values 15-18, consider dealer's up card
        if dealer_hand.hand and dealer_hand.hand[0].value() >= 7 and player_value <= 16:
            return 'hit'
        elif dealer_hand.hand and dealer_hand.hand[0].value() <= 6 and player_value >= 15:
            return 'stand'
        else:
            return 'hit' if random.random() < 0.6 else 'stand'  # 60% chance to hit