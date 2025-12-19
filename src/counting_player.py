from strategy_player import StrategyPlayer
from card_counter import CardCounter

class CountingPlayer(StrategyPlayer):
    def __init__(self,balance, strategy, counter: CardCounter, betting_spread: dict ,min_bet=10):
        super().__init__(balance, strategy)
        self.counter = counter
        self.min_bet = min_bet
        self.betting_spread = betting_spread

    def get_opening_bet(self) -> int:
        tc = int(self.counter.get_true_count())
        if tc < 1: return self.min_bet
        
        multiplier = self.betting_spread.get(tc, max(self.betting_spread.values()))
        return int(self.min_bet * multiplier)