class Connect4:
    """
    Implementation of the Connect 4 game.
    """
    def __init__(self, rows=6, cols=7):
        """Initialize an empty Connect 4 board with specified dimensions."""
        self.rows = rows
        self.cols = cols
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.current_player = 'X'  # X always starts
        self.winner = None
        self.game_over = False
        self.moves_count = 0
        self.last_move = None  # Keep track of the last move for evaluation
    
    def reset(self):
        """Reset the game to its initial state."""
        self.board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
        self.moves_count = 0
        self.last_move = None
    
    def get_board_state(self):
        """Return a copy of the current board state."""
        return [row[:] for row in self.board]
    
    def get_valid_moves(self):
        """Return a list of valid moves (column indices)."""
        valid_moves = []
        for col in range(self.cols):
            if self.board[0][col] == ' ':  # If the top cell in a column is empty
                valid_moves.append(col)
        return valid_moves
    
    def make_move(self, col):
        """
        Make a move in the specified column.
        Returns True if the move was valid, False otherwise.
        """
        if self.game_over or col < 0 or col >= self.cols or self.board[0][col] != ' ':
            return False
        
        # Find the lowest empty row in the selected column
        row = self.rows - 1
        while row >= 0 and self.board[row][col] != ' ':
            row -= 1
        
        self.board[row][col] = self.current_player
        self.last_move = (row, col)
        self.moves_count += 1
        
        # Check for a winner
        if self._check_winner(row, col):
            self.winner = self.current_player
            self.game_over = True
        # Check for a draw
        elif self.moves_count == self.rows * self.cols:
            self.game_over = True
        else:
            # Switch player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        return True
    
    def _check_winner(self, row, col):
        """Check if the current player has won after placing at (row, col)."""
        player = self.board[row][col]
        
        # Define the four directions: horizontal, vertical, diagonal /,  diagonal \
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1  # Starting count (the piece just placed)
            
            # Check in the positive direction
            r, c = row + dr, col + dc
            while 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            
            # Check in the negative direction
            r, c = row - dr, col - dc
            while 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc
            
            if count >= 4:
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
        for row in range(self.rows):
            print("| " + " | ".join(self.board[row]) + " |")
        
        # Print column numbers
        print("  " + "   ".join(str(i) for i in range(self.cols)))
        print("\n")
    
    def clone(self):
        """Create a deep copy of the current game state."""
        new_game = Connect4(self.rows, self.cols)
        new_game.board = [row[:] for row in self.board]
        new_game.current_player = self.current_player
        new_game.winner = self.winner
        new_game.game_over = self.game_over
        new_game.moves_count = self.moves_count
        new_game.last_move = self.last_move
        return new_game
    
    def evaluate_board(self, player):
        """
        Evaluate the board state for the given player.
        Used for depth-limited Minimax in Connect 4.
        Returns a score indicating how favorable the position is.
        """
        score = 0
        opponent = 'O' if player == 'X' else 'X'
        
        # Define the four directions: horizontal, vertical, diagonal /,  diagonal \
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        # Check all possible 4-in-a-row windows
        for row in range(self.rows):
            for col in range(self.cols):
                for dr, dc in directions:
                    # Skip if window extends outside the board
                    if (row + 3*dr >= self.rows or row + 3*dr < 0 or 
                        col + 3*dc >= self.cols or col + 3*dc < 0):
                        continue
                    
                    window = [self.board[row + i*dr][col + i*dc] for i in range(4)]
                    
                    # Count pieces in the window
                    player_count = window.count(player)
                    opponent_count = window.count(opponent)
                    empty_count = window.count(' ')
                    
                    # Score the window based on piece counts
                    if player_count == 4:
                        score += 100  # Winning window
                    elif player_count == 3 and empty_count == 1:
                        score += 5    # Three in a row with an empty space
                    elif player_count == 2 and empty_count == 2:
                        score += 2    # Two in a row with two empty spaces
                    
                    if opponent_count == 3 and empty_count == 1:
                        score -= 4    # Block opponent's potential win
        
        # Favor the center column
        center_col = self.cols // 2
        center_count = 0
        for row in range(self.rows):
            if self.board[row][center_col] == player:
                center_count += 1
        score += center_count * 3
        
        return score