# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 09:50:45 2023

@author: Myat
"""

###-------------    LIBRARY    -------------###

import random as r
import matplotlib.pyplot as plt
import pandas as pd
import time

###-------------    OOP    -------------###

class Card:
    
    def __init__(self, suit, num):
        self.suit = suit
        self.num = num
    
    def __str__(self):
        return f'{self.num} of {self.suit}'
    
    def get_value(self,ace_count):
        if self.num in ['Jack', 'Queen', 'King']:
            return 10
        elif self.num == 'Ace':
            if ace_count == 0:
                return 11
            else:
                return 1
        else:
            return int(self.num)

class Deck:
    
    def __init__(self):
        self.cards = []
        
        # Create Deck with 52 cards
        numbers = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King']
        suits = ['Hearts', 'Diamonds', 'Cross', 'Spades']
        for suit in suits:
            for num in numbers:
                self.cards.append(Card(suit, num))
                
    def shuffle(self):
        r.shuffle(self.cards)
    
    # Draw Cards
    def deal(self):
        return self.cards.pop()
        
class Player:
    
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.account = 1000
    
    # Player Draw Cards   
    def hit(self,card):
        self.hand.append(card)
        
    def show(self):
        print(f'{self.name}\'s hand:')
        for card in self.hand:
            print(card)
        print('')
    
    def count_card(self):
        a = len(self.hand)
        return a         
    
    def restart(self):
        self.hand = []
    
    # Bet win/lose    
    def game_end(self,result,bet):
        if result == 1:
            self.account = self.account + bet
        elif result == 2:
            self.account = self.account + 2*bet
        elif result == 9:
            self.account = self.account - bet
            
        print(f'{self.name}\'s current account is {self.account} Euro')
        print('--------------------------------------------------------------') 
        print(' ')
        

class Dealer(Player):
    
    def __init__(self):
        super().__init__('Dealer')
        
    def show(self):
        print('Dealer\'s hand: ')
        print(self.hand[0])
        print('???')
        print('')
        

###-------------    FUNCTIONS    -------------###

# Card comparison and results
    # player wins = 1
    # player blackjack = 2
    # dealer wins = 9
    # reset/draw = 0
    
def game_on(player_val, player_card, dealer_val, dealer_card):
    if player_val == 21 and player_card == 2:
        result = 2
    elif dealer_val == 21 and dealer_card == 2:
        result = 9
    elif dealer_card == 5 and dealer_val < 21:
        result = 9
    elif player_card == 5 and player_val < 21:
        result = 1
    elif dealer_val == player_val:
        result = 0
    elif dealer_val == 21:
        result = 9
    elif player_val == 21:
        result = 2
    elif dealer_val > 21 and player_val > 21:
        result = 0
    elif player_val > dealer_val and player_val < 22:
        result = 1
    elif dealer_val > player_val and dealer_val < 22:
        result = 9
    elif dealer_val > 21 and player_val < 22:
        result = 1
    else:
        result = 9
    return result

def game_result(num):
    if num == 0:
        print('The game is draw.')
    elif num == 1:
        print('Player',player.name,'wins.')
    elif num == 2:
        print('Player',player.name,'wins with Blackjack.')
    elif num == 9:
        print('Dealer wins. Player',player.name,'loses.')

def display():
   player.show()
   dealer.show()
   print('Player',player.name, 'Card value is', player_val, 'and number of cards are', player_card)
   print('Dealer Card value is', dealer_val, 'and number of cards are', dealer_card)
   print('')  


###-------------    VARIABLES    -------------###

game = 0
bet = 0 
dealer_val = 0  # Dealer Card Value Total
player_val = 0  # Player Card Value Total
result = 0  # Win/Lose or Blackjack
p_ace_check = 0 # To Check if there is already Ace in hand
d_ace_check = 0 # To Check if there is already Ace in hand

#for csv

dealer_first_card = []
result_history = []

ace_prob = 0    # For Probability Calculation
two_prob = 0
three_prob = 0
four_prob = 0
five_prob = 0
six_prob = 0
seven_prob = 0
eight_prob = 0
nine_prob = 0
ten_prob = 0

###-------------    MAIN CODE    -------------###
        
# Menu

print('You will start the game with 1000 Euros in your account.')
game_limit = int(input('Enter the amount of game to play: '))
game_speed = int(input('Which speed do you want to play? (0 = fast simulation, 1 = One game by one game: '))
if game_speed == 0: # for safety precaution
    game_speed = 0
else:
    game_speed = 1
name = input('Enter your name: ')

# Game Loop

deck = Deck()   # Create Deck
deck.shuffle()  # Shuffle the deck
dealer = Dealer()
player = Player(name) # Create Dealer and Player

while game < game_limit: 
    print('Game:', game + 1)
    
    bet = r.randint(1,20)   #Bet
    
    if game % 5 == 0:   #Shuffle every 5 games
        deck = Deck()   # Create Deck again
        deck.shuffle()
        
    # First Card
    
    ## Player
    pc = deck.deal()
    pc_v = pc.get_value(0)
    if pc_v == 11:
        p_ace_check = 1
    player.hit(pc)
    player_val = player_val + pc_v
    
    ## Dealer
    dc = deck.deal()
    dc_v = dc.get_value(0)
    if dc_v == 11:
        d_ace_check = 1
    dealer.hit(dc)
    dealer_val = dealer_val + dc_v
    
    # Collecting First Card For Plot
    card_deal = str(dc)
    card_deal = card_deal.split(' ',3)
    card_deal = card_deal[0]
    dealer_first_card.append(card_deal)   
    
    #--------------# 
    
    # Following Card
    
    ## Player
    pc = deck.deal()
    pc_v = pc.get_value(p_ace_check)
    if pc_v == 11:
        p_ace_check = 1
    player.hit(pc)
    player_val = player_val + pc_v
    
    ## Dealer
    dc = deck.deal()
    dc_v = dc.get_value(dc_v)
    if dc_v == 11:
        d_ace_check = 1
    dealer.hit(dc)
    dealer_val = dealer_val + dc_v
    
    ## Card Count
    player_card = player.count_card()
    dealer_card = dealer.count_card()
    
    #--------------# 
    
    # Game's On
    
    while player_val < 17 and player_card < 5:  # Player Behaviour
        pc = deck.deal()
        pc_v = pc.get_value(p_ace_check)
        if pc_v == 11:
            p_ace_check = 1
        player.hit(pc)
        player_val = player_val + pc_v
        player_card = player.count_card()
    
    while dealer_val < 15 and dealer_card < 5:  # Dealer First Behaviour before it reaches dealer's minimum value
        dc = deck.deal()
        dc_v = dc.get_value(dc_v)
        if dc_v == 11:
            d_ace_check = 1
        dealer.hit(dc)
        dealer_val = dealer_val + dc_v
        dealer_card = dealer.count_card()
        
    while dealer_val < player_val and dealer_card < 5 and player_card < 5 and player_val < 21: # Dealer Second Behaviour
        dc = deck.deal()
        dc_v = dc.get_value(dc_v)
        if dc_v == 11:
            d_ace_check = 1
        dealer.hit(dc)
        dealer_val = dealer_val + dc_v
        dealer_card = dealer.count_card()
    
    #--------------# 
    
    # Win or Lose Decision and Show
    result = game_on(player_val, player_card, dealer_val, dealer_card)
    display()
    game_result(result)
    result_history.append(result)
    
    player.game_end(result, bet)
     
    #--------------# 
    
    # End of Round (Reseting)
    player.restart()
    dealer.restart()
    result = 0  
    dealer_val = 0
    player_val = 0                            
    game += 1
    p_ace_check = 0
    d_ace_check = 0
    
    # Game Speed
    time.sleep(game_speed)
    #--------------#

# Result Display
    
player_wins = result_history.count(1)   # Win
player_blackjack = result_history.count(2)  # Win with Blackjack
win_rate = player_wins + player_blackjack
print('Player', player.name, 'has played', game, 'games and won', win_rate, 'games. His current account is', player.account,"Euros. \n")

###-------------    GRAPH    -------------###

# Data Processing

data = pd.DataFrame({'Dealer First Card':dealer_first_card, 'Result': result_history})  # Create Dataframe for the plot

## Count (Win Rate with first card)

ace_win = len(data[(data['Dealer First Card'] == 'Ace') & ((data['Result'] == 1) | (data['Result'] == 2))])
ace = len(data[data['Dealer First Card'] == 'Ace'])

two_win = len(data[(data['Dealer First Card'] == '2') & ((data['Result'] == 1) | (data['Result'] == 2))])
two = len(data[data['Dealer First Card'] == '2'])

three_win = len(data[(data['Dealer First Card'] == '3') & ((data['Result'] == 1) | (data['Result'] == 2))])
three = len(data[data['Dealer First Card'] == '3'])

four_win = len(data[(data['Dealer First Card'] == '4') & ((data['Result'] == 1) | (data['Result'] == 2))])
four = len(data[data['Dealer First Card'] == '4'])

five_win = len(data[(data['Dealer First Card'] == '5') & ((data['Result'] == 1) | (data['Result'] == 2))])
five = len(data[data['Dealer First Card'] == '5'])

six_win = len(data[(data['Dealer First Card'] == '6') & ((data['Result'] == 1) | (data['Result'] == 2))])
six = len(data[data['Dealer First Card'] == '6'])

seven_win = len(data[(data['Dealer First Card'] == '7') & ((data['Result'] == 1) | (data['Result'] == 2))])
seven = len(data[data['Dealer First Card'] == '7'])

eight_win = len(data[(data['Dealer First Card'] == '8') & ((data['Result'] == 1) | (data['Result'] == 2))])
eight = len(data[data['Dealer First Card'] == '8'])

nine_win = len(data[(data['Dealer First Card'] == '9') & ((data['Result'] == 1) | (data['Result'] == 2))])
nine = len(data[data['Dealer First Card'] == '9'])

ten_win = len(data[((data['Dealer First Card'] == '10') | (data['Dealer First Card'] == 'Jack') | (data['Dealer First Card'] == 'Queen') | (data['Dealer First Card'] == 'King')) & ((data['Result'] == 1) | (data['Result'] == 2))])
ten = len(data[(data['Dealer First Card'] == '10') | (data['Dealer First Card'] == 'Jack') | (data['Dealer First Card'] == 'Queen') | (data['Dealer First Card'] == 'King')])

## Probability Calculating

if ace != 0:
    ace_prob = ace_win/ace
if two != 0:   
    two_prob = two_win/two 
if three != 0:
    three_prob = three_win/three
if four != 0:
    four_prob = four_win/four
if five != 0:
    five_prob = five_win/five
if six != 0:
    six_prob = six_win/six
if seven != 0:
    seven_prob = seven_win/seven
if eight != 0:
    eight_prob = eight_win/eight
if nine != 0:
    nine_prob = nine_win/nine
if ten != 0:
    ten_prob = ten_win/ten

# Plotting

x_axis = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10']
prob = [ace_prob, two_prob, three_prob, four_prob, five_prob, six_prob, seven_prob, eight_prob, nine_prob, ten_prob]
c = ['red', 'yellow', 'pink', 'blue', 'orange', 'red', 'yellow', 'pink', 'blue', 'orange']

plt.bar(x_axis, prob, color = c)
plt.title('Statistics of winning probability')
plt.xlabel('Dealer\'s first card')
plt.ylabel('Probability of winning')
plt.show()

###-------------    END    -------------###