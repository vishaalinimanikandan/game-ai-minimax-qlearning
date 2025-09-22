import os
import argparse
import time
from visualization.game_visualizer import GameVisualizer
from games.tictactoe import TicTacToe
from games.connect4 import Connect4
from algorithms.minimax import MinimaxTicTacToe, MinimaxConnect4
from algorithms.qlearning import QLearningTicTacToe, QLearningConnect4
from opponents.default_opponent import DefaultOpponent, RandomOpponent

def run_visualization_demo():
    """Run a demo of game visualizations with different algorithms."""
    parser = argparse.ArgumentParser(description='AI Game Playing Visualization Demo')
    parser.add_argument('--game', type=str, choices=['tictactoe', 'connect4', 'both'], default='both',
                      help='Game to visualize (default: both)')
    parser.add_argument('--matches', type=int, default=3,
                      help='Number of matches to play for each combination (default: 3)')
    parser.add_argument('--delay', type=float, default=0.5,
                      help='Delay between moves in seconds (default: 0.5)')
    parser.add_argument('--cell_size', type=int, default=100,
                      help='Cell size in pixels (default: 100)')
    
    args = parser.parse_args()
    
    # Define algorithm combinations to visualize
    algorithm_combinations = [
    ('minimax', 'default'),      # Standard Minimax vs Default
    ('minimax_ab', 'default'),   # Minimax AB vs Default
    ('qlearning', 'default'),    # Q-Learning vs Default
    ('minimax', 'minimax_ab'),   # Standard Minimax vs Minimax AB 
    ('minimax_ab', 'qlearning')  # Minimax AB vs Q-Learning
]
    # Run games
    if args.game in ['tictactoe', 'both']:
        print("\n===== Visualizing Tic Tac Toe Games =====\n")
        run_game_visualizations(
            game_type='tictactoe', 
            algorithm_combinations=algorithm_combinations, 
            num_matches=args.matches,
            cell_size=args.cell_size,
            delay=args.delay
        )
    
    if args.game in ['connect4', 'both']:
        print("\n===== Visualizing Connect 4 Games =====\n")
        run_game_visualizations(
            game_type='connect4', 
            algorithm_combinations=algorithm_combinations, 
            num_matches=args.matches,
            cell_size=args.cell_size,
            delay=args.delay
        )
    
    print("\nAll visualizations completed!")

def run_game_visualizations(game_type, algorithm_combinations, num_matches=3, cell_size=100, delay=0.5):
    """
    Run visualizations for a specific game type with different algorithm combinations.
    
    Args:
        game_type: Type of game ('tictactoe' or 'connect4')
        algorithm_combinations: List of tuples with algorithm pairs to test
        num_matches: Number of matches to play for each combination
        cell_size: Size of each cell in pixels
        delay: Delay between moves in seconds
    """
    # Set up game class and window size
    if game_type == 'tictactoe':
        game_class = TicTacToe
        window_size = max(cell_size * 2, 500)  # Minimum window size 300px
    else:  # connect4
        game_class = Connect4
        window_size = max(cell_size * 7, 500)  # Minimum window size 500px
    
    # Run visualizations for each algorithm combination
    for player1_type, player2_type in algorithm_combinations:
        print(f"\nVisualization: {player1_type} vs {player2_type} in {game_type}")
        
        # Create players
        player1 = create_player(player1_type, game_type, game_class)
        player2 = create_player(player2_type, game_type, game_class)
        
        # Create descriptive names for the algorithms
        player1_name = get_algorithm_display_name(player1_type)
        player2_name = get_algorithm_display_name(player2_type)
        
        # Play multiple matches
        for match in range(num_matches):
            print(f"Playing match {match+1}/{num_matches}")
            
            # Create the visualizer with appropriate window size
            visualizer = GameVisualizer(
                game_type=game_type, 
                cell_size=cell_size, 
                animation_speed=0.2,
                window_width=window_size,
                window_height=window_size + 100,  # Extra space for info panel
                player1_name=player1_name,
                player2_name=player2_name,
                match_info=f"Match {match+1}/{num_matches}"
            )
            
            # Run the visualization
            game = visualizer.visualize_game(game_class, player1, player2, delay=delay)
            
            # Game result
            if game.get_winner() == 'X':
                print(f"Player 1 ({player1_type}) wins!")
            elif game.get_winner() == 'O':
                print(f"Player 2 ({player2_type}) wins!")
            else:
                print("The game ended in a draw!")
            
            # Small delay between matches
            time.sleep(1)

def create_player(player_type, game_type, game_class):
    """
    Create a player based on type and game.
    
    Args:
        player_type: Type of player algorithm
        game_type: Type of game
        game_class: Game class
        
    Returns:
        Player instance
    """
    if player_type == 'minimax':
        if game_type == 'tictactoe':
            return MinimaxTicTacToe(use_alpha_beta=False)
        else:
            return MinimaxConnect4(use_alpha_beta=False, max_depth=4)
    elif player_type == 'minimax_ab':
        if game_type == 'tictactoe':
            return MinimaxTicTacToe(use_alpha_beta=True)
        else:
            return MinimaxConnect4(use_alpha_beta=True, max_depth=4)
    elif player_type == 'qlearning':
        if game_type == 'tictactoe':
            player = QLearningTicTacToe()
            # Try to load pre-trained model
            model_path = "models/tictactoe_qlearning.pkl"
            if os.path.exists(model_path):
                player.load(model_path)
                print(f"Loaded pre-trained Q-learning model for Tic Tac Toe")
            else:
                print("No pre-trained model found for Tic Tac Toe. Training a new Q-learning agent...")
                player.train(game_class, RandomOpponent(), num_episodes=5000)
                os.makedirs("models", exist_ok=True)
                player.save(model_path)
            return player
        else:
            player = QLearningConnect4()
            # Try to load pre-trained model
            model_path = "models/connect4_qlearning.pkl"
            if os.path.exists(model_path):
                player.load(model_path)
                print(f"Loaded pre-trained Q-learning model for Connect 4")
            else:
                print("No pre-trained model found for Connect 4. Training a new Q-learning agent...")
                player.train(game_class, RandomOpponent(), num_episodes=3000)
                os.makedirs("models", exist_ok=True)
                player.save(model_path)
            return player
    elif player_type == 'default':
        return DefaultOpponent()
    else:  # random
        return RandomOpponent()

def get_algorithm_display_name(algorithm_type):
    """Get a display-friendly name for an algorithm."""
    if algorithm_type == 'minimax':
        return "Minimax"
    elif algorithm_type == 'minimax_ab':
        return "Minimax α-β"
    elif algorithm_type == 'qlearning':
        return "Q-Learning"
    elif algorithm_type == 'default':
        return "Default Opponent"
    else:
        return "Random"

if __name__ == "__main__":
    run_visualization_demo()