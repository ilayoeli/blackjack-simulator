from src.game import Game
from src.auto_game import AutoGame
from src.basic_strategy import BasicStrategy

def main():
    print("=" * 20)
    print("Blackjack simulator\n")
    print("=" * 20)
    while True:
        try:
            mode = input("\n[S]imulation or [G]ame? \n").lower()
            if mode in ['s', 'g']:
                break
        except ValueError:
            pass
        print("Please enter valid mode")
    if mode == 'g':    
        while True:
            try:
                balance = int(input("Enter starting balance: $"))
                if balance > 0:
                    break
            except ValueError:
                pass
            print("Please enter a valid amount")

        while True:
            try:
                game_type = input("\n[A]uto game (simulator) or [N]ormal game? \n").lower()
                if game_type in ['a', 'n']:
                    if game_type == 'a':
                        sim_type = input("\nEnable card counting? (y/n)\n").lower()
                        if sim_type in ['y', 'n']:
                            break
                    break
            except ValueError:
                pass
            print("Please enter valid game")

    
        if game_type == 'a':
            print("\nStarting automatic game for simulation. Number of rounds: 1000")
            print("\nBase bet amount: 10$")
            strategy = BasicStrategy()
            if sim_type == 'n':
                game = AutoGame(balance, strategy, 1000, 10)
            elif sim_type == 'y':
                game = AutoGame(balance, strategy, 1000, 10, use_counting=True)
        else:
            game = Game(balance)
        game.play()

    elif mode == 's':
        run_comparison_simulation()
        


def run_comparison():
    balance = int(input("Enter starting balance for both players: $"))
    rounds = int(input("Enter number of rounds: "))
    base_bet = int(input("Enter base/min bet: $"))
    
    strategy = BasicStrategy()
    print("\n[1/2] Running Basic Strategy Simulation...")
    sim_basic = AutoGame(balance, strategy, rounds, base_bet, use_counting=False)
    sim_basic.play()
    print("\n[2/2] Running Card Counting Simulation...")
    sim_counting = AutoGame(balance, strategy, rounds, base_bet, use_counting=True)
    sim_counting.play()
    # --- Final Comparison Report ---
    print("\n" + "="*45)
    print(f"{'METRIC':<20} | {'BASIC':<10} | {'COUNTING':<10}")
    print("-" * 45)
    
    basic_earnings = sim_basic.player.get_earnings()
    count_earnings = sim_counting.player.get_earnings()
    
    print(f"{'Final Balance':<20} | ${sim_basic.player.balance:<9} | ${sim_counting.player.balance:<9}")
    print(f"{'Total Profit/Loss':<20} | {basic_earnings:+<10} | {count_earnings:+<10}")
    
    # Calculate ROI
    basic_roi = (basic_earnings / balance) * 100
    count_roi = (count_earnings / balance) * 100
    print(f"{'Return on Capital':<20} | {basic_roi:>8.2f}% | {count_roi:>8.2f}%")
    print("="*45)



def run_comparison_simulation():
    # User Inputs
    while True:
        try:
            balance = int(input("Starting Bankroll: $"))
            min_bet = int(input("Enter Minimum Bet: $"))
            if balance > 0 and min_bet > 0:
                break
        except ValueError:
            print("Please enter valid numbers.")

    rounds_per_session = 1000
    total_sessions = 100

    # Calculate and show theoretical projections first
    print_theoretical_projections(balance, min_bet)

    one_to_twelve_spread = {1: 1, 2: 2, 3: 4, 4: 8, 5: 12}
    one_to_seven_point_five_spread = {1: 1, 2: 2.5, 3: 2.5, 4: 7.5, 5: 7.5}

    results = {
        "Basic": {"busts": 0, "final_avg": 0}, 
        "Counting12": {"busts": 0, "final_avg": 0},
        "Counting7": {"busts": 0, "final_avg": 0}
    }

    print(f"\nRunning {total_sessions} sessions of {rounds_per_session} rounds...")

    for session in range(total_sessions):
        # 1. Basic Strategy
        sim_b = AutoGame(balance, BasicStrategy(), rounds_per_session, min_bet, use_counting=False, silent=True)
        if not sim_b.play(): 
            results["Basic"]["busts"] += 1
        results["Basic"]["final_avg"] += sim_b.player.balance

        # 2. Counting 1:12
        sim_c = AutoGame(balance, BasicStrategy(), rounds_per_session, min_bet, use_counting=True, betting_spread=one_to_twelve_spread, silent=True)
        if not sim_c.play(): 
            results["Counting12"]["busts"] += 1
        results["Counting12"]["final_avg"] += sim_c.player.balance

        # 3. Counting 1:7.5
        sim_d = AutoGame(balance, BasicStrategy(), rounds_per_session, min_bet, use_counting=True, betting_spread=one_to_seven_point_five_spread, silent=True)
        if not sim_d.play(): 
            results["Counting7"]["busts"] += 1
        results["Counting7"]["final_avg"] += sim_d.player.balance

    # Final Metrics Calculation
    basic_ror = (results["Basic"]["busts"] / total_sessions) * 100
    count_12_ror = (results["Counting12"]["busts"] / total_sessions) * 100
    count_7_ror = (results["Counting7"]["busts"] / total_sessions) * 100

    avg_basic = results["Basic"]["final_avg"] / total_sessions
    avg_c12 = results["Counting12"]["final_avg"] / total_sessions
    avg_c7 = results["Counting7"]["final_avg"] / total_sessions

    # Correct ROI Calculation based on original balance
    avg_roi_basic = ((avg_basic - balance) / balance) * 100
    avg_roi_c12 = ((avg_c12 - balance) / balance) * 100
    avg_roi_c7 = ((avg_c7 - balance) / balance) * 100

    # Print Formatted Table
    width = 85
    print("\n" + "=" * width)
    print(f"{'METRIC':<20} | {'BASIC':^15} | {'COUNTING (1:12)':^20} | {'COUNTING (1:7.5)':^20}")
    print("-" * width)
    print(f"{'Risk of Ruin %':<20} | {basic_ror:>14.1f}% | {count_12_ror:>19.1f}% | {count_7_ror:>19.1f}%")
    print(f"{'Avg Final Balance':<20} | ${avg_basic:>13,.0f} | ${avg_c12:>18,.0f} | ${avg_c7:>18,.0f}")
    print(f"{'Avg Session ROI':<20} | {avg_roi_basic:>14.2f}% | {avg_roi_c12:>19.2f}% | {avg_roi_c7:>19.2f}%")
    print("=" * width + "\n")


import math

def print_theoretical_projections(balance, min_bet):
    # Simplified theoretical constants for a standard 6-deck game
    # EV percentages (as decimals)
    ev_basic = -0.005   # -0.5%
    ev_c7 = 0.008       # +0.8%
    ev_c12 = 0.012      # +1.2%
    
    # Standard Deviation (Volatility) per hand
    # Counting increases variance significantly
    sd_basic = 1.15 
    sd_c7 = 3.5
    sd_c12 = 5.0

    def calculate_theoretical_ror(ev, sd, bankroll):
        if ev <= 0: return 1.0  # Theoretically, a negative game always hits 0 eventually
        # Formula: e ^ (-2 * EV * Bankroll / SD^2)
        return math.exp(-2 * ev * bankroll / (sd**2))

    print("\n" + "="*40)
    print("THEORETICAL PROJECTIONS (Pre-Simulation)")
    print("="*40)
    print(f"{'Strategy':<15} | {'Exp. EV':<10} | {'Est. Risk of Ruin':<10}")
    print("-" * 40)
    
    # Basic Strategy
    print(f"{'Basic':<15} | {ev_basic:>9.1%} | {'~100%' if ev_basic < 0 else 'Low'}")
    
    # Counting 1:7.5
    ror7 = calculate_theoretical_ror(ev_c7, sd_c7, balance/min_bet)
    print(f"{'Counting 1:7.5':<15} | {ev_c7:>9.1%} | {ror7:>9.1%}")
    
    # Counting 1:12
    ror12 = calculate_theoretical_ror(ev_c12, sd_c12, balance/min_bet)
    print(f"{'Counting 1:12':<15} | {ev_c12:>9.1%} | {ror12:>9.1%}")
    print("="*40 + "\n")

if __name__ == "__main__":
    main()
