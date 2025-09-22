class TicTacToe:
    """
    Implementation of the Tic Tac Toe game.
    """
    def __init__(self):
        """Initialize an empty 3x3 board."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # X always starts
        self.winner = None
        self.game_over = False
        self.moves_count = 0
    
    def reset(self):
        """Reset the game to its initial state."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
        self.moves_count = 0
        
    def get_board_state(self):
        """Return a copy of the current board state."""
        return [row[:] for row in self.board]
    
    def get_valid_moves(self):
        """Return a list of valid moves as (row, col) tuples."""
        valid_moves = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    valid_moves.append((row, col))
        return valid_moves
    
    def make_move(self, row, col):
        """
        Make a move at the specified position.
        Returns True if the move was valid, False otherwise.
        """
        if self.game_over or row < 0 or row >= 3 or col < 0 or col >= 3 or self.board[row][col] != ' ':
            return False
        
        self.board[row][col] = self.current_player
        self.moves_count += 1
        
        # Check for a winner
        if self._check_winner():
            self.winner = self.current_player
            self.game_over = True
        # Check for a draw
        elif self.moves_count == 9:
            self.game_over = True
        else:
            # Switch player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        return True
    
    def _check_winner(self):
        """Check if the current player has won."""
        # Check rows
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] == self.current_player:
                return True
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == self.current_player:
                return True
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.current_player:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == self.current_player:
            return True
        
        return False
    
    def get_state_key(self):
        """Convert the board to a unique string representation for RL state dictionary."""
        return ''.join([''.join(row) for row in self.board])
    
    def get_winner(self):
        """Return the winner of the game, or None if there's no winner yet."""
        return self.winner
    
    def is_game_over(self):
        """Return True if the game is over, False otherwise."""
        return self.game_over
    
    def get_current_player(self):
        """Return the current player ('X' or 'O')."""
        return self.current_player
    
    def display(self):
        """Print the current state of the board."""
        print("\n")
        for row in range(3):
            print(" | ".join(self.board[row]))
            if row < 2:
                print("-" * 9)
        print("\n")
    
    def clone(self):
        """Create a deep copy of the current game state."""
        new_game = TicTacToe()
        new_game.board = [row[:] for row in self.board]
        new_game.current_player = self.current_player
        new_game.winner = self.winner
        new_game.game_over = self.game_over
        new_game.moves_count = self.moves_count
        return new_game