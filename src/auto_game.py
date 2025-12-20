# auto_game.py (Refactored for Simulation)

from .deck import Deck
from .game_round import GameRound
from .strategy_player import StrategyPlayer
from .strategy import Strategy
from .card_counter import CardCounter
from .counting_player import CountingPlayer

class AutoGame:
    
    def __init__(self,
                 balance: int,
                 strategy: Strategy,
                 num_rounds: int,
                 bet_amount: int,
                 num_decks: int = 6,
                 use_counting=False,
                 betting_spread=None,
                 silent=True):

        self.player = StrategyPlayer(balance, strategy)
        self.deck = Deck(num_decks)
        self.num_rounds = num_rounds
        self.bet_amount = bet_amount
        self.silent = silent

        if use_counting:
            self.counter = CardCounter(num_decks)
            self.player = CountingPlayer(balance, strategy, self.counter, betting_spread ,bet_amount) #bet_amount will be mininum bet
        else:
            self.counter = None
            self.player = StrategyPlayer(balance, strategy)


    def play(self) -> bool:
        """Main simulation loop - runs automatically without input"""
        self._log(f"\n--- Starting {self.num_rounds} Round Simulation ---")
        self._log(f"Initial Balance: ${self.player.balance} | Strategy: {self.player.strategy.__class__.__name__}")
        
        for i in range(1, self.num_rounds + 1):
            """Deal two cards to player and dealer"""
            # Check if deck needs reshuffling before dealing
            if len(self.deck.cards) < 30:
                self._log("\n⚠️  Low on cards - shuffling new deck...")
                self.deck.shuffle()
                if self.counter:
                    self.counter.reset()
            # CRITICAL CHECK: Ensure player has enough money to place the initial bet
            current_bet = self.player.get_opening_bet() if hasattr(self.player, 'get_opening_bet') else self.bet_amount
            if self.counter: self._log(f"True Count is: {int(self.counter.get_true_count())}, bet is {current_bet}")
            if not self.player.can_bet(current_bet):
                self._log(f"Simulation stopped: Player ran out of money before Round {i}.")
                return False
            
            
            # 1. Place the initial bet (handled by the player object)
            self.player.place_bet(current_bet)


            
            round = GameRound(self.deck, self.player, current_bet, counter=self.counter,silent=self.silent)
            winnings = round.play() # The strategy player runs silently here
            

            self.player.win(winnings)
            
            if i % 100 == 0 or i == self.num_rounds:
                self._log(f"Round {i: <4}: Balance: ${self.player.balance: <8} | Earnings: ${self.player.get_earnings():+d}")
            
        # Final Report
        earnings = self.player.get_earnings()
        self._log("\n--- Simulation Complete ---")
        self._log(f"Final balance: ${self.player.balance}")
        self._log(f"Total earnings: ${earnings:+d}")
        
        return True

    def _log(self, msg: str):
        if not self.silent:
            print(msg)