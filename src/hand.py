from .card import Card
from .deck import Deck

class Hand:

    def __init__(self):
        self.cards = []

    def add_card(self, card: Card) -> Card:
        self.cards.append(card)
        return card

    def get_value(self) -> int:
        """Calculate the value of the hand with ace handling"""
        total = sum(Deck.get_value(card.rank) for card in self.cards)

        aces = sum(1 for card in self.cards if card.rank == 'Ace')

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
    
        return total

    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.get_value() == 21
    
    def is_bust(self) -> bool:
        return self.get_value() > 21
        
    def is_pair(self) -> bool:
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank

    def is_soft_hand(self) -> bool:
        """
        Check if hand is soft (has an Ace counted as 11 without busting).
        """
        has_ace = any(card.rank == 'Ace' for card in self.cards)
        if not has_ace:
            return False
        
        # Calculate with all Aces as 1
        hard_value = sum(1 if card.rank == 'Ace' else Deck.get_value(card.rank) 
                        for card in self.cards)
        
        # Can we count one Ace as 11?
        return hard_value + 10 <= 21

    def __str__(self) -> str:
        # Creates a string like: "[Ace♠, 10♥] (Value: 21)"
        cards_str = ", ".join(str(card) for card in self.cards)
        return f"[{cards_str}] (Value: {self.get_value()})"
    
