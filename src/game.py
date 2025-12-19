from player import Player
from deck import Deck
from game_round import GameRound

class Game:
    def __init__(self, balance: int, num_decks: int = 1):
        self.player = Player(balance)
        self.deck = Deck(num_decks)
    
    def get_bet(self) -> int:
        """Get valid bet from player"""
        while True:
            try:
                bet = int(input(f"\nBalance: ${self.player.balance}\nEnter bet: $"))
                if bet > 0 and self.player.can_bet(bet):
                    return bet
                print("Invalid bet amount")
            except ValueError:
                print("Please enter a number")
    
    def play(self):
        """Main game loop"""
        print(f"Starting balance: ${self.player.balance}")
        
        while self.player.balance > 0:
            choice = input("\n[P]lay or [Q]uit? \n").lower()
            
            if choice == 'q':
                break
            elif choice == 'p':
                bet = self.get_bet()
                if not self.player.place_bet(bet):
                    continue
                
                round_game = GameRound(self.deck, self.player, bet)
                winnings = round_game.play()
                self.player.win(winnings)

        earnings = self.player.get_earnings()
        print(f"\nFinal balance: ${self.player.balance}")
        print(f"Total earnings: ${earnings:+d}")

        # Check if deck needs reshuffling before dealing
        if len(self.deck.cards) < 20:
            print("\n⚠️  Low on cards - shuffling new deck...")
            self.deck.shuffle()
        