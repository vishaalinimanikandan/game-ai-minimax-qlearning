import time
import random

class Minimax:
    """
    Implementation of the Minimax algorithm for game-playing agents.
    """
    def __init__(self, use_alpha_beta=False, max_depth=None):
        """
        Initialize the Minimax algorithm.
        
        Args:
            use_alpha_beta: Whether to use alpha-beta pruning.
            max_depth: Maximum depth for depth-limited search (None for full search).
        """
        self.use_alpha_beta = use_alpha_beta
        self.max_depth = max_depth
        self.nodes_visited = 0
        self.execution_time = 0
        
    def get_move(self, game):
        """
        Get the best move for the current player using Minimax.
        
        Args:
            game: The game state to analyze.
            
        Returns:
            The best move according to the Minimax algorithm.
        """
        self.nodes_visited = 0
        start_time = time.time()
        
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return None
        
        best_score = float('-inf')
        best_move = valid_moves[0]
        is_maximizing = True  # Current player is always maximizing
        
        for move in valid_moves:
            # Create a deep copy of the game to simulate the move
            game_copy = game.clone()
            
            # Apply the move to the copied game state
            if isinstance(move, tuple):  # For Tic Tac Toe
                row, col = move
                game_copy.make_move(row, col)
            else:  # For Connect 4
                game_copy.make_move(move)
            
            # Calculate the score for this move
            if self.use_alpha_beta:
                score = self._minimax_alpha_beta(game_copy, 0, float('-inf'), float('inf'), not is_maximizing)
            else:
                score = self._minimax(game_copy, 0, not is_maximizing)
            
            # Update the best move if needed
            if score > best_score:
                best_score = score
                best_move = move
        
        self.execution_time = time.time() - start_time
        return best_move
    
    def _minimax(self, game, depth, is_maximizing):
        """
        Standard Minimax algorithm implementation.
        
        Args:
            game: Current game state.
            depth: Current depth in the search tree.
            is_maximizing: Whether the current player is maximizing.
            
        Returns:
            The best score for the current player.
        """
        self.nodes_visited += 1
        
        # Check if the game is over
        if game.is_game_over():
            return self._evaluate_terminal(game, depth)
        
        # Check if we've reached the maximum depth
        if self.max_depth is not None and depth >= self.max_depth:
            return self._evaluate_non_terminal(game)
        
        valid_moves = game.get_valid_moves()
        
        if is_maximizing:
            best_score = float('-inf')
            for move in valid_moves:
                # Create a deep copy of the game to simulate the move
                game_copy = game.clone()
                
                # Apply the move to the copied game state
                if isinstance(move, tuple):  # For Tic Tac Toe
                    row, col = move
                    game_copy.make_move(row, col)
                else:  # For Connect 4
                    game_copy.make_move(move)
                
                # Recursive call
                score = self._minimax(game_copy, depth + 1, False)
                best_score = max(best_score, score)
            
            return best_score
        else:
            best_score = float('inf')
            for move in valid_moves:
                # Create a deep copy of the game to simulate the move
                game_copy = game.clone()
                
                # Apply the move to the copied game state
                if isinstance(move, tuple):  # For Tic Tac Toe
                    row, col = move
                    game_copy.make_move(row, col)
                else:  # For Connect 4
                    game_copy.make_move(move)
                
                # Recursive call
                score = self._minimax(game_copy, depth + 1, True)
                best_score = min(best_score, score)
            
            return best_score
    
    def _minimax_alpha_beta(self, game, depth, alpha, beta, is_maximizing):
        """
        Minimax with alpha-beta pruning implementation.
        
        Args:
            game: Current game state.
            depth: Current depth in the search tree.
            alpha: Alpha value for pruning.
            beta: Beta value for pruning.
            is_maximizing: Whether the current player is maximizing.
            
        Returns:
            The best score for the current player.
        """
        self.nodes_visited += 1
        
        # Check if the game is over
        if game.is_game_over():
            return self._evaluate_terminal(game, depth)
        
        # Check if we've reached the maximum depth
        if self.max_depth is not None and depth >= self.max_depth:
            return self._evaluate_non_terminal(game)
        
        valid_moves = game.get_valid_moves()
        
        if is_maximizing:
            best_score = float('-inf')
            for move in valid_moves:
                # Create a deep copy of the game to simulate the move
                game_copy = game.clone()
                
                # Apply the move to the copied game state
                if isinstance(move, tuple):  # For Tic Tac Toe
                    row, col = move
                    game_copy.make_move(row, col)
                else:  # For Connect 4
                    game_copy.make_move(move)
                
                # Recursive call
                score = self._minimax_alpha_beta(game_copy, depth + 1, alpha, beta, False)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                
                # Alpha-beta pruning
                if beta <= alpha:
                    break
            
            return best_score
        else:
            best_score = float('inf')
            for move in valid_moves:
                # Create a deep copy of the game to simulate the move
                game_copy = game.clone()
                
                # Apply the move to the copied game state
                if isinstance(move, tuple):  # For Tic Tac Toe
                    row, col = move
                    game_copy.make_move(row, col)
                else:  # For Connect 4
                    game_copy.make_move(move)
                
                # Recursive call
                score = self._minimax_alpha_beta(game_copy, depth + 1, alpha, beta, True)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                
                # Alpha-beta pruning
                if beta <= alpha:
                    break
            
            return best_score
    
    def _evaluate_terminal(self, game, depth):
        """
        Evaluate a terminal game state (game over).
        
        Args:
            game: The game state to evaluate.
            depth: Current depth in the search tree.
            
        Returns:
            A score for the terminal state.
        """
        # If X wins
        if game.get_winner() == 'X':
            return 10 - depth  # Prefer winning sooner
        # If O wins
        elif game.get_winner() == 'O':
            return depth - 10  # Prefer losing later
        # If it's a draw
        else:
            return 0
    
    def _evaluate_non_terminal(self, game):
        """
        Evaluate a non-terminal game state (for depth-limited search).
        
        Args:
            game: The game state to evaluate.
            
        Returns:
            A heuristic score for the non-terminal state.
        """
        # For Connect4, use the built-in evaluation function if available
        if hasattr(game, 'evaluate_board'):
            player = game.get_current_player()
            return game.evaluate_board(player)
        
        # For TicTacToe or if no evaluation function is available,
        # use a simple heuristic based on position control
        return 0  # Default to neutral position if no specific heuristic
    
    def get_stats(self):
        """Return statistics about the last move computation."""
        return {
            'nodes_visited': self.nodes_visited,
            'execution_time': self.execution_time,
            'algorithm': 'Minimax with Alpha-Beta' if self.use_alpha_beta else 'Minimax'
        }


class MinimaxTicTacToe(Minimax):
    """Specialized Minimax implementation for Tic Tac Toe."""
    
    def _evaluate_non_terminal(self, game):
        """
        Evaluate a non-terminal game state for Tic Tac Toe.
        Since the game tree for Tic Tac Toe is small, we don't need a sophisticated
        evaluation function, but this could be enhanced for better play.
        """
        return random.uniform(-0.1, 0.1)  # Small random noise to avoid deterministic play


class MinimaxConnect4(Minimax):
    """Specialized Minimax implementation for Connect 4."""
    
    def __init__(self, use_alpha_beta=False, max_depth=4):
        """
        Initialize the Minimax algorithm for Connect 4.
        Default to depth 4 because the full game tree is too large.
        """
        super().__init__(use_alpha_beta, max_depth)