import random
import time

class DefaultOpponent:
    """
    A semi-intelligent opponent that:
    1. Selects a winning move if available
    2. Blocks opponent's winning move if available
    3. Otherwise, selects a random valid move
    """
    def __init__(self):
        self.execution_time = 0
    
    def get_move(self, game):
        """
        Get the next move for the default opponent.
        
        Args:
            game: The current game state.
            
        Returns:
            The selected move.
        """
        start_time = time.time()
        
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return None
        
        # Check if there's a winning move
        winning_move = self._find_winning_move(game, valid_moves)
        if winning_move:
            self.execution_time = time.time() - start_time
            return winning_move
        
        # Check if there's a blocking move (opponent's winning move)
        blocking_move = self._find_blocking_move(game, valid_moves)
        if blocking_move:
            self.execution_time = time.time() - start_time
            return blocking_move
        
        # Otherwise, select a random valid move
        move = random.choice(valid_moves)
        
        self.execution_time = time.time() - start_time
        return move
    
    def _find_winning_move(self, game, valid_moves):
        """
        Find a move that would result in an immediate win.
        
        Args:
            game: The current game state.
            valid_moves: List of valid moves.
            
        Returns:
            A winning move if available, None otherwise.
        """
        current_player = game.get_current_player()
        
        for move in valid_moves:
            # Create a copy of the game to simulate the move
            game_copy = game.clone()
            
            # Apply the move
            if isinstance(move, tuple):  # For Tic Tac Toe
                row, col = move
                game_copy.make_move(row, col)
            else:  # For Connect 4
                game_copy.make_move(move)
            
            # Check if this move results in a win
            if game_copy.is_game_over() and game_copy.get_winner() == current_player:
                return move
        
        return None
    
    def _find_blocking_move(self, game, valid_moves):
        """
        Find a move that would block the opponent's immediate win.
        
        Args:
            game: The current game state.
            valid_moves: List of valid moves.
            
        Returns:
            A blocking move if available, None otherwise.
        """
        # Create a copy of the game to simulate the opponent's next turn
        game_copy = game.clone()
        
        # Switch to the opponent's turn
        game_copy.current_player = 'O' if game_copy.current_player == 'X' else 'X'
        
        # Find a winning move for the opponent
        opponent_winning_move = self._find_winning_move(game_copy, valid_moves)
        
        return opponent_winning_move
    
    def get_stats(self):
        """Return statistics about the last move computation."""
        return {
            'execution_time': self.execution_time,
            'algorithm': 'Default Opponent'
        }


class RandomOpponent:
    """
    A completely random opponent that selects moves at random.
    Used for training and benchmarking.
    """
    def __init__(self):
        self.execution_time = 0
    
    def get_move(self, game):
        """
        Get a random move.
        
        Args:
            game: The current game state.
            
        Returns:
            A random valid move.
        """
        start_time = time.time()
        
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return None
        
        move = random.choice(valid_moves)
        
        self.execution_time = time.time() - start_time
        return move
    
    def get_stats(self):
        """Return statistics about the last move computation."""
        return {
            'execution_time': self.execution_time,
            'algorithm': 'Random Opponent'
        }