import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
from tqdm import tqdm

class PerformanceMetrics:
    """
    Utility class for calculating and tracking performance metrics.
    """
    def __init__(self):
        """Initialize the performance metrics container."""
        self.metrics = {
            'games': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'execution_times': [],
            'nodes_visited': [],
            'win_rate': 0.0,
            'avg_execution_time': 0.0,
            'avg_nodes_visited': 0.0
        }
    
    def update(self, game, agent, opponent_name):
        """
        Update metrics based on a completed game.
        
        Args:
            game: The completed game.
            agent: The agent whose metrics are being tracked.
            opponent_name: Name of the opponent for reference.
        """
        self.metrics['games'] += 1
        
        # Update game outcome metrics
        if game.get_winner() == 'X':  # Agent is X
            self.metrics['wins'] += 1
        elif game.get_winner() == 'O':  # Opponent is O
            self.metrics['losses'] += 1
        else:  # Draw
            self.metrics['draws'] += 1
        
        # Update agent-specific metrics
        agent_stats = agent.get_stats()
        self.metrics['execution_times'].append(agent_stats.get('execution_time', 0))
        self.metrics['nodes_visited'].append(agent_stats.get('nodes_visited', 0))
        
        # Calculate derived metrics
        self.metrics['win_rate'] = self.metrics['wins'] / self.metrics['games']
        self.metrics['avg_execution_time'] = np.mean(self.metrics['execution_times'])
        
        if self.metrics['nodes_visited']:
            self.metrics['avg_nodes_visited'] = np.mean([n for n in self.metrics['nodes_visited'] if n > 0])
    
    def get_metrics(self):
        """Return a dictionary of the current metrics."""
        return {
            'games': self.metrics['games'],
            'wins': self.metrics['wins'],
            'losses': self.metrics['losses'],
            'draws': self.metrics['draws'],
            'win_rate': self.metrics['win_rate'],
            'avg_execution_time': self.metrics['avg_execution_time'],
            'avg_nodes_visited': self.metrics['avg_nodes_visited']
        }


class ExperimentRunner:
    """
    Class for running game-playing experiments and collecting metrics.
    """
    def __init__(self, game_class, num_games=100):
        """
        Initialize the experiment runner.
        
        Args:
            game_class: The game class to use for experiments.
            num_games: Number of games to play in each experiment.
        """
        self.game_class = game_class
        self.num_games = num_games
        self.results = {}
    
    def run_experiment(self, agent, opponent, experiment_name):
        """
        Run an experiment with the given agent against the opponent.
        
        Args:
            agent: The agent to test.
            opponent: The opponent to play against.
            experiment_name: Name of the experiment for reference.
            
        Returns:
            Performance metrics for the experiment.
        """
        metrics = PerformanceMetrics()
        
        for _ in tqdm(range(self.num_games), desc=f"Running {experiment_name}"):
            game = self.game_class()
            
            while not game.is_game_over():
                current_player = game.get_current_player()
                
                if current_player == 'X':  # Agent's turn
                    move = agent.get_move(game)
                    if isinstance(move, tuple):  # For Tic Tac Toe
                        row, col = move
                        game.make_move(row, col)
                    else:  # For Connect 4
                        game.make_move(move)
                else:  # Opponent's turn
                    move = opponent.get_move(game)
                    if isinstance(move, tuple):  # For Tic Tac Toe
                        row, col = move
                        game.make_move(row, col)
                    else:  # For Connect 4
                        game.make_move(move)
            
            # Update metrics after the game
            metrics.update(game, agent, type(opponent).__name__)
        
        # Store and return the results
        self.results[experiment_name] = metrics.get_metrics()
        return metrics.get_metrics()
    
    def get_results_dataframe(self):
        """Convert the results to a pandas DataFrame for easier analysis."""
        return pd.DataFrame.from_dict(self.results, orient='index')


class Visualizer:
    """
    Utility class for visualizing experimental results.
    """
    @staticmethod
    def plot_win_rates(results_df, title="Win Rates by Algorithm"):
        """
        Plot win rates for different algorithms.
        
        Args:
            results_df: DataFrame containing the results.
            title: Title for the plot.
        """
        plt.figure(figsize=(10, 6))
        
        # Extract win rates from the DataFrame
        win_rates = results_df['win_rate'].sort_values(ascending=False)
        
        # Create a bar chart
        bars = plt.bar(win_rates.index, win_rates.values, color='skyblue')
        
        # Add labels and title
        plt.xlabel('Algorithm')
        plt.ylabel('Win Rate')
        plt.title(title)
        plt.xticks(rotation=45, ha='right')
        
        # Add values on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{height:.2f}', ha='center', va='bottom')
        
        plt.tight_layout()
        return plt.gcf()
    
    @staticmethod
    def plot_execution_times(results_df, title="Average Execution Times by Algorithm"):
        """
        Plot average execution times for different algorithms.
        
        Args:
            results_df: DataFrame containing the results.
            title: Title for the plot.
        """
        plt.figure(figsize=(10, 6))
        
        # Extract execution times from the DataFrame
        exec_times = results_df['avg_execution_time'].sort_values()
        
        # Create a bar chart
        bars = plt.bar(exec_times.index, exec_times.values, color='lightgreen')
        
        # Add labels and title
        plt.xlabel('Algorithm')
        plt.ylabel('Average Execution Time (seconds)')
        plt.title(title)
        plt.xticks(rotation=45, ha='right')
        
        # Add values on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.0001,
                    f'{height:.4f}', ha='center', va='bottom')
        
        plt.tight_layout()
        return plt.gcf()
    
    @staticmethod
    def plot_nodes_visited(results_df, title="Average Nodes Visited by Algorithm"):
        """
        Plot average nodes visited for different algorithms (only applicable to Minimax).
        
        Args:
            results_df: DataFrame containing the results.
            title: Title for the plot.
        """
        plt.figure(figsize=(10, 6))
        
        # Extract nodes visited from the DataFrame, filtering out NaN values
        nodes_df = results_df[~np.isnan(results_df['avg_nodes_visited'])]
        nodes_visited = nodes_df['avg_nodes_visited'].sort_values()
        
        if nodes_visited.empty:
            plt.text(0.5, 0.5, "No nodes visited data available", 
                    ha='center', va='center', transform=plt.gca().transAxes)
        else:
            # Create a bar chart
            bars = plt.bar(nodes_visited.index, nodes_visited.values, color='salmon')
            
            # Add labels and title
            plt.xlabel('Algorithm')
            plt.ylabel('Average Nodes Visited')
            plt.title(title)
            plt.xticks(rotation=45, ha='right')
            
            # Add values on top of bars
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        return plt.gcf()
    
    @staticmethod
    def plot_outcome_distribution(results_df, title="Game Outcomes by Algorithm"):
        """
        Plot the distribution of wins, losses, and draws for each algorithm.
        
        Args:
            results_df: DataFrame containing the results.
            title: Title for the plot.
        """
        plt.figure(figsize=(12, 8))
        
        # Extract relevant columns
        outcomes_df = results_df[['wins', 'losses', 'draws']]
        
        # Create a grouped bar chart
        bar_width = 0.25
        index = np.arange(len(outcomes_df.index))
        
        plt.bar(index, outcomes_df['wins'], bar_width, label='Wins', color='green')
        plt.bar(index + bar_width, outcomes_df['losses'], bar_width, label='Losses', color='red')
        plt.bar(index + 2*bar_width, outcomes_df['draws'], bar_width, label='Draws', color='gray')
        
        # Add labels and title
        plt.xlabel('Algorithm')
        plt.ylabel('Number of Games')
        plt.title(title)
        plt.xticks(index + bar_width, outcomes_df.index, rotation=45, ha='right')
        plt.legend()
        
        plt.tight_layout()
        return plt.gcf()
    
    @staticmethod
    def save_all_plots(results_df, prefix="", formats=["png"]):
        """
        Save all plots to files.
        
        Args:
            results_df: DataFrame containing the results.
            prefix: Prefix for the filenames.
            formats: List of file formats to save (e.g., ["png", "pdf"]).
        """
        win_plot = Visualizer.plot_win_rates(results_df)
        time_plot = Visualizer.plot_execution_times(results_df)
        nodes_plot = Visualizer.plot_nodes_visited(results_df)
        outcome_plot = Visualizer.plot_outcome_distribution(results_df)
        
        plots = {
            "win_rates": win_plot,
            "execution_times": time_plot,
            "nodes_visited": nodes_plot,
            "outcome_distribution": outcome_plot
        }
        
        saved_files = []
        for plot_name, plot in plots.items():
            for fmt in formats:
                filename = f"{prefix}_{plot_name}.{fmt}"
                plot.savefig(filename, dpi=300, bbox_inches='tight')
                saved_files.append(filename)
            plt.close(plot)
        
        return saved_files