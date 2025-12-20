class CardCounter:

    def __init__(self, num_decks: int):
        self.num_decks = num_decks
        self.running_count = 0
        self.cards_seen = 0

    def record_card(self, rank: str):
        if rank in ['2', '3', '4', '5', '6']:
            self.running_count += 1
        elif rank in ['10', 'Jack', 'Queen', 'King', 'Ace']:
            self.running_count -= 1

        self.cards_seen += 1

    def get_true_count(self) -> float:
        decks_remaining = self.num_decks - (self.cards_seen / 52)
        if decks_remaining < 0.5: decks_remaining = 0.5 # Avoid division by zero
        return self.running_count / decks_remaining

    def reset(self):
        self.running_count = 0
        self.cards_seen = 0
