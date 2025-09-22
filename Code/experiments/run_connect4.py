import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import time

from games.connect4 import Connect4
from algorithms.minimax import MinimaxConnect4
from algorithms.qlearning import QLearningConnect4
from opponents.default_opponent import DefaultOpponent, RandomOpponent
from utils.metrics import ExperimentRunner, Visualizer

def test_minimax_scalability(max_time_minutes=5):
    """
    Test the scalability of Minimax for Connect 4 by counting the number of moves
    explored within a time limit.
    
    Args:
        max_time_minutes: Maximum time to run the test in minutes.
        
    Returns:
        Dictionary with scalability test results.
    """
    print("\n===== Testing Connect 4 Minimax Scalability =====\n")
    
    max_time_seconds = max_time_minutes * 60
    
    # Create the game and algorithms
    game = Connect4()
    minimax = MinimaxConnect4(use_alpha_beta=False, max_depth=None)
    minimax_ab = MinimaxConnect4(use_alpha_beta=True, max_depth=None)
    
    # Test standard Minimax
    print(f"Testing standard Minimax (up to {max_time_minutes} minutes)...")
    start_time = time.time()
    minimax.get_move(game)
    elapsed_time = time.time() - start_time
    minimax_nodes = minimax.nodes_visited
    
    # Stop if we exceed the time limit
    if elapsed_time > max_time_seconds:
        print(f"Standard Minimax timed out after {elapsed_time:.2f} seconds.")
        print(f"Nodes visited: {minimax_nodes}")
    else:
        print(f"Standard Minimax completed in {elapsed_time:.2f} seconds.")
        print(f"Nodes visited: {minimax_nodes}")
    
    # Reset the game
    game = Connect4()
    
    # Test Minimax with Alpha-Beta pruning
    print(f"\nTesting Minimax with Alpha-Beta pruning (up to {max_time_minutes} minutes)...")
    start_time = time.time()
    minimax_ab.get_move(game)
    elapsed_time = time.time() - start_time
    minimax_ab_nodes = minimax_ab.nodes_visited
    
    # Stop if we exceed the time limit
    if elapsed_time > max_time_seconds:
        print(f"Minimax with Alpha-Beta pruning timed out after {elapsed_time:.2f} seconds.")
        print(f"Nodes visited: {minimax_ab_nodes}")
    else:
        print(f"Minimax with Alpha-Beta pruning completed in {elapsed_time:.2f} seconds.")
        print(f"Nodes visited: {minimax_ab_nodes}")
    
    # Calculate improvement from Alpha-Beta pruning
    if minimax_nodes > 0:
        pruning_efficiency = minimax_ab_nodes / minimax_nodes
        print(f"\nAlpha-Beta pruning efficiency: {pruning_efficiency:.2%} of nodes visited compared to standard Minimax")
    
    # Create depth-limited versions for actual experiments
    print("\nTesting depth-limited Minimax...")
    depths = [1, 2, 3, 4, 5]
    depth_results = []
    
    for depth in depths:
        game = Connect4()
        minimax_limited = MinimaxConnect4(use_alpha_beta=True, max_depth=depth)
        
        start_time = time.time()
        minimax_limited.get_move(game)
        elapsed_time = time.time() - start_time
        
        depth_results.append({
            'depth': depth,
            'nodes_visited': minimax_limited.nodes_visited,
            'execution_time': elapsed_time
        })
        
        print(f"Depth {depth}: {elapsed_time:.4f} seconds, {minimax_limited.nodes_visited} nodes")
    
    # Determine the best depth to use for experiments
    sorted_results = sorted(depth_results, key=lambda x: x['execution_time'])
    recommended_depth = sorted_results[-2]['depth'] if len(sorted_results) > 1 else sorted_results[0]['depth']
    
    print(f"\nRecommended depth for experiments: {recommended_depth}")
    
    # Return the test results
    return {
        'minimax_nodes': minimax_nodes,
        'minimax_time': elapsed_time if minimax_nodes > 0 else max_time_seconds,
        'minimax_ab_nodes': minimax_ab_nodes,
        'minimax_ab_time': elapsed_time if minimax_ab_nodes > 0 else max_time_seconds,
        'depth_results': depth_results,
        'recommended_depth': recommended_depth
    }

def run_connect4_experiments(num_games=50, max_depth=4, save_plots=True, save_results=True):
    """
    Run a comprehensive set of experiments for Connect 4.
    
    Args:
        num_games: Number of games to play for each experiment.
        max_depth: Maximum depth for Minimax search.
        save_plots: Whether to save the plots to files.
        save_results: Whether to save the results to a CSV file.
        
    Returns:
        DataFrame containing the experiment results.
    """
    print("\n===== Running Connect 4 Experiments =====\n")
    
    # Create output directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    os.makedirs("results/plots", exist_ok=True)
    
    # Initialize the experiment runner
    runner = ExperimentRunner(Connect4, num_games=num_games)
    
    # Create the agents and opponents
    minimax = MinimaxConnect4(use_alpha_beta=False, max_depth=max_depth)
    minimax_ab = MinimaxConnect4(use_alpha_beta=True, max_depth=max_depth)
    
    qlearning = QLearningConnect4()
    
    # Train the Q-learning agent
    print("\nTraining Q-learning agent for Connect 4...")
    if os.path.exists("models/connect4_qlearning.pkl"):
        qlearning.load("models/connect4_qlearning.pkl")
        print("Loaded pre-trained Q-learning model.")
    else:
        os.makedirs("models", exist_ok=True)
        random_opponent = RandomOpponent()
        # For Connect 4, we train against a random opponent to make learning more feasible
        training_stats = qlearning.train(Connect4, random_opponent, num_episodes=5000)
        qlearning.save("models/connect4_qlearning.pkl")
        print(f"Trained Q-learning model. Win rate during training: {training_stats['win_rate']:.2f}")
    
    # For Connect 4, we use a random opponent for some experiments due to the complexity
    random_opponent = RandomOpponent()
    default_opponent = DefaultOpponent()
    
    # Run experiments: Algorithms vs Random Opponent
    print("\nRunning algorithms vs random opponent...")
    
    minimax_random = runner.run_experiment(minimax, random_opponent, "Minimax vs Random")
    minimax_ab_random = runner.run_experiment(minimax_ab, random_opponent, "Minimax-AB vs Random")
    qlearning_random = runner.run_experiment(qlearning, random_opponent, "Q-Learning vs Random")
    
    # Run experiments: Algorithms vs Default Opponent (limited number of games)
    print("\nRunning algorithms vs default opponent...")
    
    # Use a smaller number of games for default opponent to speed up experiments
    small_runner = ExperimentRunner(Connect4, num_games=max(10, num_games // 5))
    
    minimax_default = small_runner.run_experiment(minimax, default_opponent, "Minimax vs Default")
    minimax_ab_default = small_runner.run_experiment(minimax_ab, default_opponent, "Minimax-AB vs Default")
    qlearning_default = small_runner.run_experiment(qlearning, default_opponent, "Q-Learning vs Default")
    
    # Run experiments: Algorithms vs Each Other (limited number of games)
    print("\nRunning algorithms vs each other...")
    
    # Minimax vs Q-Learning
    runner_minimax_vs_qlearning = ExperimentRunner(Connect4, num_games=max(10, num_games // 5))
    minimax_vs_qlearning = runner_minimax_vs_qlearning.run_experiment(minimax, qlearning, "Minimax vs Q-Learning")
    
    # Minimax-AB vs Q-Learning
    runner_minimax_ab_vs_qlearning = ExperimentRunner(Connect4, num_games=max(10, num_games // 5))
    minimax_ab_vs_qlearning = runner_minimax_ab_vs_qlearning.run_experiment(minimax_ab, qlearning, "Minimax-AB vs Q-Learning")
    
    # Get the combined results
    results_df = runner.get_results_dataframe()
    
    # Add additional results
    additional_results = pd.DataFrame({
        "Minimax vs Default": minimax_default,
        "Minimax-AB vs Default": minimax_ab_default,
        "Q-Learning vs Default": qlearning_default,
        "Minimax vs Q-Learning": minimax_vs_qlearning,
        "Minimax-AB vs Q-Learning": minimax_ab_vs_qlearning
    }).T
    
    results_df = pd.concat([results_df, additional_results])
    
    # Save the results if requested
    if save_results:
        results_df.to_csv("results/connect4_results.csv")
    
    # Generate and save plots if requested
    if save_plots:
        Visualizer.save_all_plots(results_df, prefix="results/plots/connect4")
    
    print("\n===== Connect 4 Experiments Completed =====\n")
    
    return results_df

if __name__ == "__main__":
    # First test scalability to determine a good depth limit
    scalability_results = test_minimax_scalability(max_time_minutes=1)
    recommended_depth = scalability_results['recommended_depth']
    
    # Run the experiments with the recommended depth
    run_connect4_experiments(max_depth=recommended_depth)