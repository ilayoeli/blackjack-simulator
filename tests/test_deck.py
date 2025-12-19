import unittest
from deck import Deck

class TestDeck(unittest.TestCase):
    
    def test_multilpe_of_52_cards(self):
        deck = Deck(3)
        self.assertEqual(len(deck.cards) % 52, 0)

    def test_deal(self):
        deck = Deck()
        num_of_cards = len(deck.cards)
        deck.deal()
        self.assertEqual(len(deck.cards), num_of_cards - 1)

    def test_shuffle(self):
        deck = Deck()
        deck.cards = []
        self.assertEqual(len(deck.cards), 0)

        deck.shuffle()
        self.assertEqual(len(deck.cards), 52)
        
