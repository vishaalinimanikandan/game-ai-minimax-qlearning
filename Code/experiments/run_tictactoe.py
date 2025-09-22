import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

from games.tictactoe import TicTacToe
from algorithms.minimax import MinimaxTicTacToe
from algorithms.qlearning import QLearningTicTacToe
from opponents.default_opponent import DefaultOpponent, RandomOpponent
from utils.metrics import ExperimentRunner, Visualizer

def run_tictactoe_experiments(num_games=100, save_plots=True, save_results=True):
    """
    Run a comprehensive set of experiments for Tic Tac Toe.
    
    Args:
        num_games: Number of games to play for each experiment.
        save_plots: Whether to save the plots to files.
        save_results: Whether to save the results to a CSV file.
        
    Returns:
        DataFrame containing the experiment results.
    """
    print("\n===== Running Tic Tac Toe Experiments =====\n")
    
    # Create output directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    os.makedirs("results/plots", exist_ok=True)
    
    # Initialize the experiment runner
    runner = ExperimentRunner(TicTacToe, num_games=num_games)
    
    # Create the agents and opponents
    minimax = MinimaxTicTacToe(use_alpha_beta=False)
    minimax_ab = MinimaxTicTacToe(use_alpha_beta=True)
    
    qlearning = QLearningTicTacToe()
    
    # Train the Q-learning agent
    print("\nTraining Q-learning agent for Tic Tac Toe...")
    if os.path.exists("models/tictactoe_qlearning.pkl"):
        qlearning.load("models/tictactoe_qlearning.pkl")
        print("Loaded pre-trained Q-learning model.")
    else:
        os.makedirs("models", exist_ok=True)
        random_opponent = RandomOpponent()
        training_stats = qlearning.train(TicTacToe, random_opponent, num_episodes=10000)
        qlearning.save("models/tictactoe_qlearning.pkl")
        print(f"Trained Q-learning model. Win rate during training: {training_stats['win_rate']:.2f}")
    
    default_opponent = DefaultOpponent()
    
    # Run experiments: Algorithms vs Default Opponent
    print("\nRunning algorithms vs default opponent...")
    default_results = {}
    
    minimax_default = runner.run_experiment(minimax, default_opponent, "Minimax vs Default")
    minimax_ab_default = runner.run_experiment(minimax_ab, default_opponent, "Minimax-AB vs Default")
    qlearning_default = runner.run_experiment(qlearning, default_opponent, "Q-Learning vs Default")
    
    # Run experiments: Algorithms vs Each Other
    print("\nRunning algorithms vs each other...")
    
    # Minimax vs Q-Learning
    runner_minimax_vs_qlearning = ExperimentRunner(TicTacToe, num_games=num_games)
    minimax_vs_qlearning = runner_minimax_vs_qlearning.run_experiment(minimax, qlearning, "Minimax vs Q-Learning")
    
    # Minimax-AB vs Q-Learning
    runner_minimax_ab_vs_qlearning = ExperimentRunner(TicTacToe, num_games=num_games)
    minimax_ab_vs_qlearning = runner_minimax_ab_vs_qlearning.run_experiment(minimax_ab, qlearning, "Minimax-AB vs Q-Learning")
    
    # Get the combined results
    results_df = runner.get_results_dataframe()
    
    # Add algorithm vs algorithm results
    additional_results = pd.DataFrame({
        "Minimax vs Q-Learning": minimax_vs_qlearning,
        "Minimax-AB vs Q-Learning": minimax_ab_vs_qlearning
    }).T
    
    results_df = pd.concat([results_df, additional_results])
    
    # Save the results if requested
    if save_results:
        results_df.to_csv("results/tictactoe_results.csv")
    
    # Generate and save plots if requested
    if save_plots:
        Visualizer.save_all_plots(results_df, prefix="results/plots/tictactoe")
    
    print("\n===== Tic Tac Toe Experiments Completed =====\n")
    
    return results_df

if __name__ == "__main__":
    run_tictactoe_experiments()