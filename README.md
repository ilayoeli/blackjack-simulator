# Blackjack Strategy & Risk Simulator

A high-performance Python simulation engine designed to analyze the mathematical edge of various Blackjack strategies. This tool compares **Standard Basic Strategy** against **Hi-Lo Card Counting** across different betting spreads to visualize the trade-off between profit and volatility.

## 📈 Overview
In Blackjack, "Basic Strategy" reduces the house edge to roughly 0.5%, but the player is still mathematically expected to lose over time. This project simulates a "Card Counting" player who tracks the ratio of high-to-low cards to identify moments of player advantage.

### Key Metrics Tracked:
* **Expected Value (EV):** The average final balance after a set number of rounds.
* **Risk of Ruin (RoR):** The statistical probability that a player will lose their entire bankroll before completing the session.



## 🛠 Features
* **Object-Oriented Architecture:** Modular design with decoupled classes for `Deck`, `Hand`, `Player`, and `Strategy`.
* **Hi-Lo Counting Engine:** Real-time "True Count" calculation adjusted for deck penetration (number of decks remaining).
* **Custom Betting Spreads:** Dynamic bet sizing based on the True Count (e.g., 1-to-12 and 1-to-7.5 spreads).
* **Monte Carlo Simulation:** Runs hundreds of parallel "lifetimes" to eliminate variance and find the mathematical truth of a strategy.
* **Logging Control:** A centralized `_log` system allowing for high-speed "silent" simulations or verbose "step-by-step" game rounds.

## 🚀 How It Works
The simulator uses the industry-standard **Hi-Lo system**:
* **Low Cards (2-6):** +1
* **Neutral (7-9):** 0
* **High Cards (10-Ace):** -1

The `CardCounter` calculates the **True Count** by dividing the running count by the number of decks remaining. As the True Count rises, the `CountingPlayer` increases their bet size to capitalize on the higher probability of receiving high cards and dealer busts.

## 📊 Performance Comparison
*Sample results from 100 sessions of 1,000 rounds with a $1,000 bankroll:*

| METRIC              | BASIC STRATEGY | COUNTING (1:12) | COUNTING (1:7.5) |
| :------------------ | :------------- | :-------------- | :--------------- |
| **Risk of Ruin %** | 1.0%           | 43.0%           | 27.0%            |
| **Avg Final Balance** | $892           | $1,064          | $1,083           |

> **Note:** These results demonstrate the "Volatility Tax." While counting produces a positive return on average, the higher bet spreads significantly increase the chance of going bust during a "bad shoe."

## 💻 Installation & Usage
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/ilayoeli/blackjack-simulator.git](https://github.com/ilayoeli/blackjack-simulator.git)
    cd blackjack-simulator
    ```
2.  **Run the simulation:**
    ```bash
    python main.py
    ```

## 📂 Project Structure
* `main.py`: Entry point for running multi-strategy comparisons.
* `auto_game.py`: The simulation engine that manages rounds and sessions.
* `game_round.py`: Logic for a single round of Blackjack (dealing