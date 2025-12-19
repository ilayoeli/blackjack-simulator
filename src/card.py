class Card:

    def __init__(self, suit: str, rank: str) -> None:
        self.suit = suit
        self.rank = rank

    def __str__(self):
        symbols = {
            'Spades': '♠',
            'Hearts': '♥', 
            'Diamonds': '♦',
            'Clubs': '♣'
        }
        # Returns format like "10♠" or "Queen♥"
        return f"{self.rank}{symbols.get(self.suit, self.suit)}"
    
    def __repr__(self):
        # Ensures lists of cards print prettily
        return self.__str__()