import matplotlib.pyplot as plt
from main import *

def run_comparison(num_games=3000, initial_budget=500):
    deck = Deck()
    dealer = Dealer(5000, deck)

    player_strategy2 = Player('Strategy2 Player', initial_budget, strategy2)
    player_strategy1 = Player('Strategy1 Player', initial_budget, strategy1)

    strategy2_budgets = [initial_budget]
    strategy1_budgets = [initial_budget]

    for i in range(num_games):
        # Reset deck and hands for new game
        deck = Deck()
        dealer = Dealer(5000, deck)
        player_strategy2.hand = Hand(dealer=False)
        player_strategy1.hand = Hand(dealer=False)

        game_log = []
        game = Game(dealer, [player_strategy2, player_strategy1], game_log)
        game.run()
        
        # Record budgets
        strategy2_budgets.append(player_strategy2.budget)
        strategy1_budgets.append(player_strategy1.budget)

    # plot results
    plt.figure(figsize=(10, 8))

    plt.subplot(211)
    plt.plot(range(num_games+1), strategy2_budgets)
    plt.grid(True)
    plt.title(f"Strategy 2 Performance (Initial Budget: ${initial_budget})")
    plt.xlabel('Games')
    plt.ylabel('Budget ($)')

    plt.subplot(212)
    plt.plot(range(num_games + 1), strategy1_budgets)
    plt.grid(True)
    plt.title(f"Strategy 1 Performance (Initial Budget: ${initial_budget})")
    plt.xlabel('Games')
    plt.ylabel('Budget ($)')
    
    plt.tight_layout()
    plt.show()

# Compare final results
    strategy2_final = strategy2_budgets[-1]
    strategy1_final = strategy1_budgets[-1]
    
    print(f"\nFinal Results after {num_games} games:")
    print(f"Strategy 2 final budget: ${strategy2_final}")
    print(f"Strategy 1 final budget: ${strategy1_final}")
    print(f"\nStrategy {'2' if strategy2_final > strategy1_final else '1'} performed better")

if __name__ == "__main__":
    run_comparison()