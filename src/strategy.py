from hand import Hand
from card import Card

class Strategy:
    def __init__(self):
        pass

    
    @staticmethod
    def get_action(hand: Hand, dealer_up_card_rank: str, can_split_or_double: bool) -> str:
        hand_value = hand.get_value()
        
        # 1. Simple Hit/Stand Logic
        if hand_value <= 11:
            return 'hit'
        elif hand_value >= 17:
            return 'stand'
        
        # 2. Check for Splitting (Simple rule: always split Aces or 8s if allowed)
        if hand.is_pair() and hand.cards[0].rank in ('Ace', '8'):
            # Must check if action is valid first (e.g. if the game allows it now)
            return 'split'

        # 3. Default (If between 12 and 16, default to stand for this simple strategy)
        return 'stand'