__author__ = 'GAG569'

import random

class Suit:
    def __init__(self,name):
        self.name = name

class Symbol:
    def __init__(self,name,value):
        self.name = name
        self.value = value

class Card:
    def __init__(self,suit,symbol):
        self.suit = suit
        self.symbol = symbol

class Deck:
    def __init__(self):
        self.cards = []
    def add(self,card):
        self.cards.append(card)
    def get(self):
        if len(self.cards)>0:
            return self.cards.pop()
        return None
    def shuffle(self):
        random.shuffle(self.cards)

class DeckFactory:
    SUITS=["club","spade","diamond","heart"]
    SYMBOLS=["ace","two","three","four","five","six","seven","eight","nine","ten","jack","queen","king"]

    def create_deck(self):
        deck = Deck()
        for suit in DeckFactory.SUITS:
            for symbol in DeckFactory.SYMBOLS:
                deck.add(Card(Suit(suit),Symbol(symbol,DeckFactory.SYMBOLS.index(symbol)+1)))
        return deck
