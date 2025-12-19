
from hand import Hand
class Player:

    def __init__(self, balance: int):
        self.balance : int = balance
        self.initial_balance = self.balance
        self.current_bet = 0
        
    def can_bet(self, amount: int) -> bool:
        return self.balance >= amount
    
    def place_bet(self, amount: int) -> bool:
        if not self.can_bet(amount):
            return False
        self.balance -= amount
        self.current_bet = amount
        return True

    def win(self, amount: int):
        self.balance += amount

    def get_earnings(self) -> int:
        return self.balance - self.initial_balance
    
    def get_action(self, hand: Hand, dealer_up_card_rank: str ,bet: int) -> str:
            """
            The base player implementation is to ask the user for input.
            This method will be overridden by the StrategyPlayer.
            """
            actions = self._get_valid_actions(hand, bet) 
            
            while True:
                choice = input(f"Choose {actions}: ").lower()
                if choice in actions:
                    return choice
                print("Invalid choice")

    def _get_valid_actions(self, hand: Hand, bet: int) -> list[str]:
        """Get valid action from player"""
        actions = ['hit', 'stand']
        
        if len(hand.cards) == 2:
            if self.can_bet(bet):
                actions.append('double')
                if hand.is_pair():
                    actions.append('split')
        
        return actions