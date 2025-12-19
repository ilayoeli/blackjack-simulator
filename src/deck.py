from card import Card
import random

class Deck:

    RANKS = [str(i) for i in range(2,11)] + ['Jack', 'Queen', 'King', 'Ace']
    SUITS = ['Diamonds', 'Hearts', 'Clubs', 'Spades']
    VALUES = {'2' : 2, '3' : 3, '4' : 4, '5' : 5,
              '6' : 6, '7' : 7, '8' : 8, '9' : 9,
              '10' : 10, 'Jack' : 10, 'Queen' : 10, 'King' : 10, 'Ace' : 11
                }
    
    def __init__(self, num_of_decks: int = 1):
        self.cards = []
        self.num_of_decks = num_of_decks
        self.shuffle()

    def shuffle(self):
        self.cards = []
        for _ in range(self.num_of_decks):
            for suit in self.SUITS:
                for rank in self.RANKS:
                    self.cards.append(Card(suit, rank))
        random.shuffle(self.cards)

    def deal(self) -> Card:
        return self.cards.pop()
    
    @staticmethod
    def get_value(rank: str) -> int:
        return Deck.VALUES[rank]


