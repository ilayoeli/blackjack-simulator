from .deck import Deck
from .hand import Hand
from .card import Card
from .player import Player
from .card_counter import CardCounter
import time

class GameRound:
    def __init__(self, deck: Deck, player: Player, bet: int, counter=None, silent=False):
        self.deck = deck
        self.player = player
        self.bet = bet
        self.counter = counter
        self.silent = silent 
        
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.active_hands = []  # Hands currently being played (with their bets)
    
    def deal_initial(self):
        """Deal two cards to player and dealer"""
        for _ in range(2):
            self.player_hand.add_card(self._deal_and_record())
            self.dealer_hand.add_card(self._deal_and_record())
    
    def show_initial_state(self):
        self._log(f"\nDealer shows: [{self.dealer_hand.cards[0].rank}, ?]")
        self._log(f"Your hand: {self.player_hand}")
    
    def play_hand(self, hand: Hand, bet: int) -> tuple[Hand, int] | None:
        """
        Play a single hand until complete.
        Returns the final hand and bet amount (for later comparison with dealer).
        Returns None if hand busted.
        """
        while not hand.is_bust():
            action = self.player.get_action(hand, self.dealer_hand.cards[0].rank, bet)
            if action == 'stand':
                break
            elif action == 'hit':
                hand.add_card(self._deal_and_record())
                self._log(f"Your hand: {hand}")
            elif action == 'double':
                if self.player.can_bet(bet):
                    self.player.place_bet(bet)
                    bet *= 2
                    hand.add_card(self._deal_and_record())
                    self._log(f"Doubled! Your hand: {hand}")
                    break
                else:
                    self._log("Not enough balance to double")
            elif action == 'split':
                return self.handle_split(hand, bet)
        
        if hand.is_bust():
            self._log(f"Bust! Lost ${bet}")
            return None  # Busted hands don't get compared with dealer
        
        return (hand, bet)  # Return for later comparison
    
    def get_player_action(self, hand: Hand, bet: int) -> str:
        
        return self.player.get_action(hand, self.dealer_hand.cards[0].rank, bet)

    def play_dealer(self):
        """Dealer plays by fixed rules (hits until 17+)"""
        self._log(f"\nDealer reveals: {self.dealer_hand}")
        
        while self.dealer_hand.get_value() < 17:
            # time.sleep(1.0)  # Add delay for UX
            new_card = self._deal_and_record()
            self.dealer_hand.add_card(new_card)
            self._log(f"Dealer draws {new_card.rank}: {self.dealer_hand}")
        
        if self.dealer_hand.is_bust():
            self._log(f"Dealer busts with {self.dealer_hand.get_value()}!")
        else:
            self._log(f"Dealer stands with {self.dealer_hand.get_value()}")
    
    def compare_with_dealer(self, hand: Hand, bet: int) -> int:
        """
        Compare a single hand with dealer.
        Returns winnings (0 for loss, bet for push, 2*bet for win).
        """
        player_value = hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        self._log(f"\nYour hand: {hand}")
        
        if self.dealer_hand.is_bust():
            self._log(f"Dealer busted! You win ${bet}")
            return bet * 2
        elif player_value > dealer_value:
            self._log(f"You win ${bet}! ({player_value} vs {dealer_value})")
            return bet * 2
        elif player_value < dealer_value:
            self._log(f"Dealer wins. Lost ${bet} ({player_value} vs {dealer_value})")
            return 0
        else:
            self._log(f"Push - bet returned ({player_value} vs {dealer_value})")
            return bet
    
    def handle_split(self, hand: Hand, bet: int) -> tuple[Hand, int] | None:
        """
        Handle split logic.
        Returns None (all hands handled within this method).
        Adds resulting hands to self.active_hands for later dealer comparison.
        """
        if not self.player.can_bet(bet):
            self._log("Not enough balance to split")
            return self.play_hand(hand, bet)
        
        self.player.place_bet(bet)
        
        # Create two new hands with one card each
        hand1 = Hand()
        hand1.add_card(hand.cards[0])
        
        hand2 = Hand()
        hand2.add_card(hand.cards[1])
        
        # Check if splitting Aces (special rules)
        is_ace_split = hand.cards[0].rank == 'Ace'
        
        if is_ace_split:
            self._log("\nSplitting Aces - one card each, no further plays")
            
            # Deal one card to each Ace
            hand1.add_card(self._deal_and_record())
            self._log(f"First Ace hand: {hand1}")
            
            hand2.add_card(self._deal_and_record())
            self._log(f"Second Ace hand: {hand2}")
            
            # Add to active hands for comparison (unless busted, which is impossible with Aces)
            if not hand1.is_bust():
                self.active_hands.append((hand1, bet))
            else:
                self._log(f"First hand busted! Lost ${bet}")
                
            if not hand2.is_bust():
                self.active_hands.append((hand2, bet))
            else:
                self._log(f"Second hand busted! Lost ${bet}")
            
            return None  # Signal that split is complete
        
        else:
        # Normal split 
        # 1. Create hands and add the first card from the pair
            hand1 = Hand()
            hand1.add_card(hand.cards[0])
            hand2 = Hand()
            hand2.add_card(hand.cards[1])
    
            hand1.add_card(self._deal_and_record())
            hand2.add_card(self._deal_and_record())
            
            self._log("\n--- First split hand ---")
            self._log(f"Starting hand: {hand1}")
            result1 = self.play_hand(hand1, bet)

            if result1 is not None:
                # If it returns a tuple, it's a regular hand or another split
                if isinstance(result1, tuple):
                    self.active_hands.append(result1)
                # If None, the split was handled and hands already added
            
            self._log("\n--- Second split hand ---")
            self._log(f"Starting hand: {hand2}")
            result2 = self.play_hand(hand2, bet)
            if result2 is not None:
                if isinstance(result2, tuple):
                    self.active_hands.append(result2)
            
            return None  # Signal that split is complete
    
    def play(self) -> int:
        """Play the round, return total winnings"""
        self.deal_initial()
        self.show_initial_state()
        
        # Check for player blackjack
        if self.player_hand.is_blackjack():
            # Dealer must reveal to check for blackjack
            self._log(f"\nBlackjack! Checking dealer...")
            self._log(f"Dealer has: {self.dealer_hand}")
            
            if self.dealer_hand.is_blackjack():
                self._log("Dealer also has Blackjack - Push!")
                return self.bet
            else:
                self._log("You win with Blackjack!")
                return int(self.bet * 2.5)
        
        # Check for dealer blackjack (player doesn't have it)
        if self.dealer_hand.is_blackjack():
            self._log(f"\nDealer has: {self.dealer_hand}")
            self._log("Dealer has Blackjack! You lose.")
            return 0
        
        # Play player's hand(s)
        result = self.play_hand(self.player_hand, self.bet)
        
        # If play_hand returns a tuple, it's a single hand to compare
        # If it returns None, either busted or split was handled
        if result is not None:
            self.active_hands.append(result)
        
        # If no active hands (all busted), dealer doesn't play
        if not self.active_hands:
            self._log("\nAll hands busted! Dealer wins.")
            return 0
        
        # Dealer plays once for all remaining hands
        self.play_dealer()
        
        # Compare all active hands with dealer
        total_winnings = 0
        for hand, bet in self.active_hands:
            winnings = self.compare_with_dealer(hand, bet)
            total_winnings += winnings
        
        return total_winnings
    
    def _deal_and_record(self):
        card = self.deck.deal()
        if self.counter:
            self.counter.record_card(card.rank)
        return card
    
    def _log(self, message: str):
        """Helper to self._log only if not in silent mode"""
        if not self.silent:
            time.sleep(1.0)
            print(message)