from player import Player
from hand import Hand
from strategy import Strategy




class StrategyPlayer(Player):
    """A player that uses a strategy given by a strategy matrix"""

    def __init__(self, balance: int, strategy: Strategy):
        super().__init__(balance)
        self.strategy = strategy 
        print("Strategy")

    
    def get_action(self, hand: Hand, dealer_up_card_rank: str, bet: int) -> str:
        valid_actions = self._get_valid_actions(hand,bet)

        can_bet_options = 'double' in valid_actions

        startegy_action = self.strategy.get_action(hand, dealer_up_card_rank, can_bet_options)

        if startegy_action in valid_actions:
            return startegy_action
        
        if startegy_action == 'split' or startegy_action == 'double':
            can_bet_options_recheck = False

            fallback_action = self.strategy.get_action(hand, dealer_up_card_rank, can_bet_options_recheck)

            if fallback_action in valid_actions:
                return fallback_action
            
        return 'stand' #Safety
