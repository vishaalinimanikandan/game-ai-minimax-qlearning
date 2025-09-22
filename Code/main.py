import os
import pandas as pd
import matplotlib.pyplot as plt
import time
import argparse

from experiments.run_tictactoe import run_tictactoe_experiments
from experiments.run_connect4 import run_connect4_experiments
from fix_connect4_timeout import test_minimax_scalability

def export_metrics_to_excel(results, filename="results/metrics.xlsx"):
    """
    Export all metrics to a well-formatted Excel file.
    
    Args:
        results: Dictionary containing experiment results
        filename: Path to save the Excel file
    """
    # Create a Pandas Excel writer
    writer = pd.ExcelWriter(filename, engine='openpyxl')
    
    # Create separate sheets for each game and comparison type
    
    # Tic Tac Toe metrics
    if 'tictactoe' in results:
        tictactoe_df = results['tictactoe']
        tictactoe_df.to_excel(writer, sheet_name='Tic Tac Toe')
        
        # Create additional sheets with specific metrics
        # Win/Loss/Draw metrics
        tictactoe_outcomes = tictactoe_df[['wins', 'losses', 'draws', 'win_rate']]
        tictactoe_outcomes.to_excel(writer, sheet_name='TicTacToe_Outcomes')
        
        # Performance metrics
        tictactoe_performance = tictactoe_df[['avg_execution_time', 'avg_nodes_visited']]
        tictactoe_performance.to_excel(writer, sheet_name='TicTacToe_Performance')
    
    # Connect 4 metrics
    if 'connect4' in results:
        connect4_df = results['connect4']
        connect4_df.to_excel(writer, sheet_name='Connect 4')
        
        # Create additional sheets with specific metrics
        # Win/Loss/Draw metrics
        connect4_outcomes = connect4_df[['wins', 'losses', 'draws', 'win_rate']]
        connect4_outcomes.to_excel(writer, sheet_name='Connect4_Outcomes')
        
        # Performance metrics
        connect4_performance = connect4_df[['avg_execution_time', 'avg_nodes_visited']]
        connect4_performance.to_excel(writer, sheet_name='Connect4_Performance')
    
    # Combined metrics
    if 'tictactoe' in results and 'connect4' in results:
        # Combine results from both games
        combined_df = pd.concat([
            results['tictactoe'].assign(Game='Tic Tac Toe'),
            results['connect4'].assign(Game='Connect 4')
        ])
        
        combined_df.to_excel(writer, sheet_name='Combined')
        
        # Create summary sheet with key metrics
        # Group by algorithm and game
        grouped_df = combined_df.reset_index()
        grouped_df['Algorithm'] = grouped_df['index'].str.split(' vs ').str[0]
        
        # Average metrics by algorithm and game
        avg_metrics = grouped_df.groupby(['Algorithm', 'Game']).agg({
            'win_rate': 'mean',
            'avg_execution_time': 'mean',
            'avg_nodes_visited': 'mean'
        }).reset_index()
        
        # Pivot table for win rates
        win_rates_pivot = avg_metrics.pivot(index='Algorithm', columns='Game', values='win_rate')
        win_rates_pivot.to_excel(writer, sheet_name='Summary_WinRates')
        
        # Pivot table for execution times
        exec_times_pivot = avg_metrics.pivot(index='Algorithm', columns='Game', values='avg_execution_time')
        exec_times_pivot.to_excel(writer, sheet_name='Summary_ExecTimes')
    
    # Save the Excel file
    writer.close()
    
    print(f"\nMetrics exported to Excel file: {filename}")

def main():
    """Main entry point for running all experiments."""
    parser = argparse.ArgumentParser(description='AI Game Playing Experiment Runner')
    parser.add_argument('--game', type=str, choices=['tictactoe', 'connect4', 'both'], default='both',
                        help='Game to run experiments on (default: both)')
    parser.add_argument('--num_games', type=int, default=100,
                        help='Number of games to play for each experiment (default: 100)')
    parser.add_argument('--no_plots', action='store_true',
                        help='Disable saving plots')
    parser.add_argument('--no_save', action='store_true',
                        help='Disable saving results')
    
    args = parser.parse_args()
    
    # Create results directory
    os.makedirs("results", exist_ok=True)
    os.makedirs("results/plots", exist_ok=True)
    
    results = {}
    
    # Run Tic Tac Toe experiments
    if args.game in ['tictactoe', 'both']:
        start_time = time.time()
        tictactoe_results = run_tictactoe_experiments(
            num_games=args.num_games,
            save_plots=not args.no_plots,
            save_results=not args.no_save
        )
        results['tictactoe'] = tictactoe_results
        print(f"Tic Tac Toe experiments completed in {time.time() - start_time:.2f} seconds.")
    
    # Run Connect 4 experiments
    if args.game in ['connect4', 'both']:
        start_time = time.time()
        
        # First test scalability to determine a good depth limit
        print("\nTesting Connect 4 Minimax scalability...")
        scalability_results = test_minimax_scalability(max_time_minutes=1)
        recommended_depth = scalability_results['recommended_depth']
        print(f"Recommended depth for Connect 4 Minimax: {recommended_depth}")
        
        # Run the experiments with the recommended depth
        connect4_results = run_connect4_experiments(
            num_games=max(50, args.num_games // 2),  # Use fewer games for Connect 4
            max_depth=recommended_depth,
            save_plots=not args.no_plots,
            save_results=not args.no_save
        )
        results['connect4'] = connect4_results
        print(f"Connect 4 experiments completed in {time.time() - start_time:.2f} seconds.")
    
    # Compare algorithms overall (across both games)
    if args.game == 'both' and not args.no_plots:
        print("\nGenerating overall comparison plots...")
        
        # Combine results from both games
        combined_df = pd.concat([
            results['tictactoe'].assign(Game='Tic Tac Toe'),
            results['connect4'].assign(Game='Connect 4')
        ])
        
        # Save combined results
        if not args.no_save:
            combined_df.to_csv("results/combined_results.csv")
        
        # Create overall plots
        plt.figure(figsize=(12, 8))
        
        # Group by algorithm (removing the opponent info) and game
        grouped_df = combined_df.reset_index()
        grouped_df['Algorithm'] = grouped_df['index'].str.split(' vs ').str[0]
        
        # Handle duplicate algorithms by averaging their win rates
        avg_win_rates = grouped_df.groupby(['Algorithm', 'Game'])['win_rate'].mean().reset_index()
        
        # Create a pivot table from the averages
        win_rates_pivot = avg_win_rates.pivot(index='Algorithm', columns='Game', values='win_rate')
        
        # Create a grouped bar chart for win rates
        ax = win_rates_pivot.plot(kind='bar', figsize=(10, 6))
        plt.title('Win Rates by Algorithm and Game')
        plt.xlabel('Algorithm')
        plt.ylabel('Win Rate')
        plt.xticks(rotation=45)
        plt.ylim(0, 1)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(title='Game')
        
        # Add values on top of bars
        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f', padding=3)
        
        plt.tight_layout()
        
        if not args.no_plots:
            plt.savefig("results/plots/overall_win_rates.png", dpi=300, bbox_inches='tight')
        
        plt.close()
    
    # Export all metrics to Excel
    if not args.no_save:
        export_metrics_to_excel(results)
    
    print("\nAll experiments completed!")

if __name__ == "__main__":
    main()