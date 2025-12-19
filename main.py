from game import Game
from auto_game import AutoGame
from basic_strategy import BasicStrategy

def main():
    while True:
        try:
            sim = input("\n[S]imulation or [G]ame? \n").lower()
            if sim in ['s', 'g']:
                break
        except ValueError:
            pass
        print("Please enter valid mode")
    if sim == 'g':    
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
                game_type = input("\n[A]uto game or [N]ormal game? \n").lower()
                if game_type in ['a', 'n']:
                    if game_type == 'a':
                        sim_type = input("\n[N]ormal simulation or [C]ard counting simulation? \n").lower()
                        if sim_type in ['n', 'c']:
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
            elif sim_type == 'c':
                game = AutoGame(balance, strategy, 1000, 10, use_counting=True)
        else:
            game = Game(balance)
        game.play()

    elif sim == 's':
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
    balance = int(input("Starting Bankroll: $"))
    rounds_per_session = 1000
    total_sessions = 100
    min_bet = 10

    one_to_tweleve_spread = {1: 1, 2: 2, 3: 4, 4: 8, 5: 12}
    one_to_seven_point_five_spread = {1: 1, 2: 2.5, 3: 2.5, 4: 7.5, 5: 7.5}

    results = {"Basic": {"busts": 0, "final_avg": 0}, 
               "Counting12": {"busts": 0, "final_avg": 0},
               "Counting7": {"busts": 0, "final_avg": 0}}

    print(f"\nRunning {total_sessions} sessions of {rounds_per_session} rounds...")

    for session in range(total_sessions):
        # 1. Run Basic Strategy Session
        sim_b = AutoGame(balance, BasicStrategy(), rounds_per_session, min_bet, use_counting=False,silent=True)
        if not sim_b.play(): results["Basic"]["busts"] += 1
        results["Basic"]["final_avg"] += sim_b.player.balance

        # 2. Run Card Counting Session, one_to_twleve
        sim_c = AutoGame(balance, BasicStrategy(), rounds_per_session, min_bet, use_counting=True, betting_spread=one_to_tweleve_spread, silent=True)
        if not sim_c.play(): results["Counting12"]["busts"] += 1
        results["Counting12"]["final_avg"] += sim_c.player.balance

        sim_d = AutoGame(balance, BasicStrategy(), rounds_per_session, min_bet, use_counting=True, betting_spread=one_to_seven_point_five_spread, silent=True)
        if not sim_d.play(): results["Counting7"]["busts"] += 1
        results["Counting7"]["final_avg"] += sim_d.player.balance




    # Calculate Risk of Ruin %
    basic_ror = (results["Basic"]["busts"] / total_sessions) * 100
    count_12_ror = (results["Counting12"]["busts"] / total_sessions) * 100
    count_7_ror = (results["Counting7"]["busts"] / total_sessions) * 100

    avg_basic = results["Basic"]["final_avg"] / total_sessions
    avg_c12 = results["Counting12"]["final_avg"] / total_sessions
    avg_c7 = results["Counting7"]["final_avg"] / total_sessions


    print("\n" + "=" * 85)
    print(f"{'METRIC':<20} | {'BASIC':^15} | {'COUNTING (1:12)':^20} | {'COUNTING (1:7.5)':^20}")
    print("-" * 85)
    print(f"{'Risk of Ruin %':<20} | {basic_ror:>14.1f}% | {count_12_ror:>19.1f}% | {count_7_ror:>19.1f}%")
    print(f"{'Avg Final Balance':<20} | ${avg_basic:>13,.0f} | ${avg_c12:>18,.0f} | ${avg_c7:>18,.0f}")
    print("=" * 85 + "\n")
if __name__ == "__main__":
    main()
