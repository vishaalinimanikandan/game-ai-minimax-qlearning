# CS7IS2 Artificial Intelligence Assignment 3
# Game Playing Algorithms: Minimax and Reinforcement Learning

This project implements and compares Minimax (with and without alpha-beta pruning) and Q-learning 
Reinforcement Learning algorithms for playing Tic Tac Toe and Connect 4 games.

## Project Structure

- games/
  - tictactoe.py         # Tic Tac Toe game implementation
  - connect4.py          # Connect 4 game implementation
- algorithms/
  - minimax.py           # Minimax implementations (with and without alpha-beta pruning)
  - qlearning.py         # Q-learning implementation
- opponents/
  - default_opponent.py  # Default and random opponent implementations
- experiments/
  - run_tictactoe.py     # Experiment runner for Tic Tac Toe
  - run_connect4.py      # Experiment runner for Connect 4
- utils/
  - metrics.py           # Performance metrics and visualization utilities
- main.py                # Main entry point for running experiments
- README.txt             # This file with instructions

## Requirements

- Python 3.7 or higher
- Required packages:
  - numpy
  - pandas
  - matplotlib
  - tqdm

You can install the required packages using:
```
pip install numpy pandas matplotlib tqdm
```

## Running the Experiments

### Running All Experiments

To run all experiments with default settings:
```
python main.py
```

### Running Specific Game Experiments

To run only Tic Tac Toe experiments:
```
python main.py --game tictactoe
```

To run only Connect 4 experiments:
```
python main.py --game connect4
```

### Additional Options

- Set the number of games for each experiment:
```
python main.py --num_games 50
```

- Disable saving plots:
```
python main.py --no_plots
```

- Disable saving results:
```
python main.py --no_save
```

## Running Individual Files

You can also run the experiment files directly:

For Tic Tac Toe:
```
python experiments/run_tictactoe.py
```

For Connect 4:
```
python experiments/run_connect4.py
```

For Visualised Demo:
```
python demo.py
```

## Output

The experiments will produce the following outputs:

- Printed results and statistics to the console
- CSV files with experiment results in the `results/` directory
- Trained Q-learning models in the `models/` directory

## Notes on Connect 4 Implementation

Due to the computational complexity of Connect 4 (with 4^42 possible states compared to 3^9 for Tic Tac Toe),
several optimizations have been implemented:

1. Depth-limited Minimax search with an evaluation function
2. Reduced state representation for Q-learning
3. Training against a random opponent for faster convergence
4. Fewer games in experiments to manage execution time

The code will automatically test different depth limits for Connect 4 and select an appropriate value based on
your system's performance.