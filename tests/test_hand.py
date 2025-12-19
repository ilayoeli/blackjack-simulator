import unittest
from card import Card
from hand import Hand

class TestHandLogic(unittest.TestCase):
    
    def test_basic_sum(self):
        hand = Hand()
        hand.add_card(Card('Hearts', '10'))
        hand.add_card(Card('Diamonds', '7'))
        self.assertEqual(hand.get_value(), 17)

    def test_soft_bust(self):
        hand = Hand()
        hand.add_card(Card('Spades', 'Ace'))
        hand.add_card(Card('Clubs', '7'))
        hand.add_card(Card('Clubs', '8')) # 11 + 7 + 8 = 26 -> 1 + 7 + 8 = 16
        self.assertEqual(hand.get_value(), 16)

    def test_blackjack(self):
        hand = Hand()
        hand.add_card(Card('Hearts', 'Ace'))
        hand.add_card(Card('Clubs', 'Jack'))
        self.assertEqual(hand.get_value(), 21)

    def test_soft_hand(self):
        hand = Hand()
        hand.add_card(Card('Spades', 'Ace'))
        hand.add_card(Card('Diamonds', '7'))
        self.assertEqual(hand.get_value(), 18)

    def test_hard_bust(self):
        hand = Hand()
        hand.add_card(Card('Hearts', '8'))
        hand.add_card(Card('Spades', '7'))
        hand.add_card(Card('Spades', '7'))
        self.assertEqual(hand.get_value(), 22)
    
    def test_multiple_aces(self):
        hand = Hand()
        hand.add_card(Card('Diamonds', '9'))
        hand.add_card(Card('Diamonds', 'Ace'))
        hand.add_card(Card('Clubs', 'Ace'))
        self.assertEqual(hand.get_value(), 21)

if __name__ == '__main__':
    unittest.main()