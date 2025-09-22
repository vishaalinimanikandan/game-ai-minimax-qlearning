import random
import pickle
import time
import os
from tqdm import tqdm

class QLearning:
    """
    Implementation of the Q-learning algorithm for game-playing agents.
    """
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0,
                 exploration_decay=0.995, min_exploration_rate=0.01):
        """
        Initialize the Q-learning algorithm.
        
        Args:
            learning_rate: Alpha value for Q-value updates.
            discount_factor: Gamma value for future rewards.
            exploration_rate: Initial epsilon value for exploration.
            exploration_decay: Decay rate for exploration.
            min_exploration_rate: Minimum epsilon value for exploration.
        """
        self.q_table = {}  # State-action values
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate
        self.execution_time = 0
        
    def get_move(self, game):
        """
        Get the best move for the current player using the Q-table.
        
        Args:
            game: The game state to analyze.
            
        Returns:
            The best move according to the Q-table, or a random move if exploring.
        """
        start_time = time.time()
        
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return None
        
        state_key = game.get_state_key()
        
        # Exploration: choose a random action
        if random.random() < self.exploration_rate:
            move = random.choice(valid_moves)
        # Exploitation: choose the best action from Q-table
        else:
            # If state is not in Q-table, initialize it
            if state_key not in self.q_table:
                self.q_table[state_key] = {move: 0 for move in valid_moves}
            
            # Get Q-values for all valid moves
            q_values = self.q_table[state_key]
            
            # Find the moves with the maximum Q-value
            max_q_value = max([q_values.get(move, 0) for move in valid_moves])
            best_moves = [move for move in valid_moves if q_values.get(move, 0) == max_q_value]
            
            # If multiple moves have the same Q-value, choose randomly among them
            move = random.choice(best_moves)
        
        self.execution_time = time.time() - start_time
        return move
    
    def update(self, state, action, next_state, reward, done):
        """
        Update the Q-table using the Q-learning update rule.
        
        Args:
            state: Current state key.
            action: Action taken.
            next_state: Resulting state key.
            reward: Reward received.
            done: Whether the episode is completed.
        """
        # Initialize state in Q-table if not present
        if state not in self.q_table:
            self.q_table[state] = {}
        
        # Initialize action in state's Q-values if not present
        if action not in self.q_table[state]:
            self.q_table[state][action] = 0
        
        # Calculate the Q-learning update
        old_q_value = self.q_table[state][action]
        
        if done:
            # If terminal state, future Q-value is 0
            future_q_value = 0
        else:
            # If not in Q-table yet, initialize the next state
            if next_state not in self.q_table:
                self.q_table[next_state] = {}
            
            # If no actions in next state (should not happen), use 0
            if not self.q_table[next_state]:
                future_q_value = 0
            else:
                # Otherwise, take the maximum Q-value from the next state
                future_q_value = max(self.q_table[next_state].values())
        
        # Q-learning update rule
        new_q_value = old_q_value + self.learning_rate * (
            reward + self.discount_factor * future_q_value - old_q_value
        )
        
        # Update the Q-table
        self.q_table[state][action] = new_q_value
    
    def decay_exploration(self):
        """Decay the exploration rate after each episode."""
        self.exploration_rate = max(
            self.min_exploration_rate,
            self.exploration_rate * self.exploration_decay
        )
    
    def train(self, game_class, opponent, num_episodes=10000, reward_win=1.0, reward_draw=0.5, reward_loss=-1.0):
        """
        Train the Q-learning agent by playing against an opponent.
        
        Args:
            game_class: The game class to create instances from.
            opponent: The opponent to play against.
            num_episodes: Number of training episodes.
            reward_win: Reward for winning.
            reward_draw: Reward for a draw.
            reward_loss: Reward for losing.
            
        Returns:
            Training statistics.
        """
        wins = 0
        draws = 0
        losses = 0
        
        for episode in tqdm(range(num_episodes), desc="Training Q-learning"):
            game = game_class()
            game_history = []
            
            while not game.is_game_over():
                current_state = game.get_state_key()
                current_player = game.get_current_player()
                
                if current_player == 'X':  # Q-learning agent always plays as X
                    move = self.get_move(game)
                    if isinstance(move, tuple):  # For Tic Tac Toe
                        row, col = move
                        game_history.append((current_state, move))
                        game.make_move(row, col)
                    else:  # For Connect 4
                        game_history.append((current_state, move))
                        game.make_move(move)
                else:  # Opponent's turn
                    move = opponent.get_move(game)
                    if isinstance(move, tuple):  # For Tic Tac Toe
                        row, col = move
                        game.make_move(row, col)
                    else:  # For Connect 4
                        game.make_move(move)
            
            # Determine the reward based on the game outcome
            if game.get_winner() == 'X':  # Agent won
                reward = reward_win
                wins += 1
            elif game.get_winner() == 'O':  # Agent lost
                reward = reward_loss
                losses += 1
            else:  # Draw
                reward = reward_draw
                draws += 1
            
            # Update Q-values for all moves made by the agent
            for state, action in reversed(game_history):
                next_state = game.get_state_key()  # Final state
                self.update(state, action, next_state, reward, True)
                # The reward only directly applies to the final state
                # For previous states, the value will propagate through the discount factor
                reward = 0
            
            # Decay exploration rate
            self.decay_exploration()
        
        return {
            'episodes': num_episodes,
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'win_rate': wins / num_episodes,
            'final_exploration_rate': self.exploration_rate
        }
    
    def save(self, filename):
        """Save the Q-table to a file."""
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)
    
    def load(self, filename):
        """Load the Q-table from a file."""
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)
            return True
        return False
    
    def get_stats(self):
        """Return statistics about the last move computation."""
        return {
            'q_table_size': len(self.q_table),
            'exploration_rate': self.exploration_rate,
            'execution_time': self.execution_time,
            'algorithm': 'Q-Learning'
        }


class QLearningTicTacToe(QLearning):
    """Specialized Q-Learning implementation for Tic Tac Toe."""
    
    def get_move(self, game):
        """Get a move for Tic Tac Toe, handling the tuple format."""
        move = super().get_move(game)
        # Ensure the move is in the right format for the game
        return move


class QLearningConnect4(QLearning):
    """Specialized Q-Learning implementation for Connect 4.
    
    For Connect 4, we use a reduced state representation to make learning feasible.
    """
    
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0,
                 exploration_decay=0.99, min_exploration_rate=0.1):
        """Initialize with parameters adjusted for Connect 4."""
        super().__init__(learning_rate, discount_factor, exploration_rate,
                        exploration_decay, min_exploration_rate)
        
    def train(self, game_class, opponent, num_episodes=5000, reward_win=1.0, reward_draw=0.5, reward_loss=-1.0):
        """Train with fewer episodes due to the complexity of Connect 4."""
        return super().train(game_class, opponent, num_episodes, reward_win, reward_draw, reward_loss)