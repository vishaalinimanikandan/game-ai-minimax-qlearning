import pygame
import time
import sys
from pygame.locals import *

class GameVisualizer:
    """
    A pygame-based visualizer for Tic Tac Toe and Connect 4 games.
    Shows games in progress with animated moves.
    """
    def __init__(self, game_type="tictactoe", cell_size=100, animation_speed=0.5, 
                 window_width=None, window_height=None, player1_name="Player 1", 
                 player2_name="Player 2", match_info=""):
        """
        Initialize the game visualizer.
        
        Args:
            game_type: Type of game to visualize ("tictactoe" or "connect4")
            cell_size: Size of each cell in pixels
            animation_speed: Delay between animation frames in seconds
            window_width: Custom window width (if None, calculated based on cell_size)
            window_height: Custom window height (if None, calculated based on cell_size)
            player1_name: Display name for player 1 (X)
            player2_name: Display name for player 2 (O)
            match_info: Additional match information to display
        """
        pygame.init()
        
        self.game_type = game_type
        self.cell_size = cell_size
        self.animation_speed = animation_speed
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.match_info = match_info
        
        # Set up display dimensions based on game type
        if game_type == "tictactoe":
            self.rows, self.cols = 3, 3
            self.title = "Tic Tac Toe Visualization"
        else:  # connect4
            self.rows, self.cols = 6, 7
            self.title = "Connect 4 Visualization"
        
        # Calculate window dimensions if not provided
        self.width = window_width if window_width else self.cols * cell_size
        self.height = window_height if window_height else self.rows * cell_size + 150  # Extra space for info panel
        
        # Set up the display
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        
        # Define colors
        self.bg_color = (240, 240, 240)
        self.line_color = (0, 0, 0)
        self.x_color = (30, 100, 200)  # Blue for X
        self.o_color = (200, 50, 50)    # Red for O
        self.info_color = (50, 50, 50)
        self.highlight_color = (70, 130, 180, 128)  # Semi-transparent blue for highlighting
        
        # Font for displaying information
        self.font = pygame.font.Font(None, 30)
        self.title_font = pygame.font.Font(None, 36)
        
        # Game state
        self.board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 'X'
        self.move_history = []
        
        # For Connect 4 animation
        self.falling_piece = None
        self.falling_position = None
        
        # For last move highlighting
        self.last_move = None
    
    def draw_board(self):
        """Draw the game board on the screen."""
        self.screen.fill(self.bg_color)
        
        # Draw title and game information
        title_text = f"{self.player1_name} (X) vs {self.player2_name} (O)"
        title_surface = self.title_font.render(title_text, True, self.info_color)
        title_rect = title_surface.get_rect(center=(self.width/2, 30))
        self.screen.blit(title_surface, title_rect)
        
        # Draw current player indicator
        current_player_text = f"Current Player: {'X' if self.current_player == 'X' else 'O'}"
        text_surface = self.font.render(current_player_text, True, 
                                      self.x_color if self.current_player == 'X' else self.o_color)
        text_rect = text_surface.get_rect(center=(self.width/2, 65))
        self.screen.blit(text_surface, text_rect)
        
        # Draw match info if provided
        if self.match_info:
            info_surface = self.font.render(self.match_info, True, self.info_color)
            info_rect = info_surface.get_rect(center=(self.width/2, self.height - 25))
            self.screen.blit(info_surface, info_rect)
        
        if self.game_type == "tictactoe":
            self._draw_tictactoe_board()
        else:
            self._draw_connect4_board()
        
        pygame.display.flip()
    
    def _draw_tictactoe_board(self):
        """Draw the Tic Tac Toe board grid and pieces."""
        # Calculate board position to center it
        board_size = self.cell_size * 3
        board_x = (self.width - board_size) // 2
        board_y = 100  # Start below the info panel
        self.board_offset_x = board_x  # Store for move calculations
        self.board_offset_y = board_y
        
        # Draw board background
        board_rect = pygame.Rect(board_x, board_y, board_size, board_size)
        pygame.draw.rect(self.screen, (220, 220, 220), board_rect)
        pygame.draw.rect(self.screen, self.line_color, board_rect, 3)
        
        # Draw grid lines
        for i in range(1, self.rows):
            # Horizontal lines
            pygame.draw.line(
                self.screen, self.line_color, 
                (board_x, board_y + i * self.cell_size), 
                (board_x + board_size, board_y + i * self.cell_size),
                3
            )
            
            # Vertical lines
            pygame.draw.line(
                self.screen, self.line_color, 
                (board_x + i * self.cell_size, board_y), 
                (board_x + i * self.cell_size, board_y + board_size),
                3
            )
        
        # Draw X's and O's
        for row in range(self.rows):
            for col in range(self.cols):
                cell_x = board_x + col * self.cell_size
                cell_y = board_y + row * self.cell_size
                
                # Highlight last move
                if self.last_move and self.last_move == (row, col):
                    highlight_rect = pygame.Rect(
                        cell_x, cell_y, 
                        self.cell_size, self.cell_size
                    )
                    highlight_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                    pygame.draw.rect(highlight_surface, self.highlight_color, 
                                    highlight_surface.get_rect())
                    self.screen.blit(highlight_surface, highlight_rect)
                
                if self.board[row][col] == 'X':
                    self._draw_x(cell_x, cell_y)
                elif self.board[row][col] == 'O':
                    self._draw_o(cell_x, cell_y)
# Add these methods to the end of your GameVisualizer class:

    def _draw_connect4_board(self):
        """Draw the Connect 4 board grid and pieces."""
        # Calculate board position to center it
        board_width = self.cell_size * self.cols
        board_height = self.cell_size * self.rows
        board_x = (self.width - board_width) // 2
        board_y = 100  # Start below the info panel
        self.board_offset_x = board_x  # Store for move calculations
        self.board_offset_y = board_y
        
        # Draw the blue board background
        board_rect = pygame.Rect(
            board_x, board_y, 
            board_width, board_height
        )
        pygame.draw.rect(self.screen, (30, 50, 150), board_rect)
        pygame.draw.rect(self.screen, (20, 40, 120), board_rect, 3)  # Border
        
        # Draw the holes/pieces
        for row in range(self.rows):
            for col in range(self.cols):
                center_x = board_x + col * self.cell_size + self.cell_size // 2
                center_y = board_y + row * self.cell_size + self.cell_size // 2
                radius = self.cell_size // 2 - 10
                
                # Highlight last move
                if self.last_move and self.last_move == (row, col):
                    highlight_radius = radius + 5
                    pygame.draw.circle(
                        self.screen,
                        self.highlight_color,
                        (center_x, center_y),
                        highlight_radius
                    )
                
                # Draw the empty hole (white circle)
                if self.board[row][col] == ' ':
                    pygame.draw.circle(
                        self.screen, 
                        self.bg_color,  # White for empty holes
                        (center_x, center_y), 
                        radius
                    )
                # Draw the pieces
                elif self.board[row][col] == 'X':
                    pygame.draw.circle(
                        self.screen, 
                        self.x_color, 
                        (center_x, center_y), 
                        radius
                    )
                elif self.board[row][col] == 'O':
                    pygame.draw.circle(
                        self.screen, 
                        self.o_color, 
                        (center_x, center_y), 
                        radius
                    )
        
        # Draw falling piece animation if applicable
        if self.falling_piece is not None:
            col, current_row, target_row = self.falling_position
            center_x = board_x + col * self.cell_size + self.cell_size // 2
            center_y = board_y + current_row * self.cell_size + self.cell_size // 2
            radius = self.cell_size // 2 - 10
            
            color = self.x_color if self.falling_piece == 'X' else self.o_color
            pygame.draw.circle(self.screen, color, (center_x, center_y), radius)
            
        # Draw column numbers at the bottom
        for col in range(self.cols):
            col_text = str(col)
            text_surface = self.font.render(col_text, True, self.bg_color)
            text_rect = text_surface.get_rect(
                center=(board_x + col * self.cell_size + self.cell_size // 2, 
                       board_y + board_height + 25)
            )
            self.screen.blit(text_surface, text_rect)
            
    def _draw_x(self, x, y):
        """Draw an X in the specified position."""
        # Draw the X (two diagonal lines)
        padding = self.cell_size // 4
        pygame.draw.line(
            self.screen, self.x_color,
            (x + padding, y + padding),
            (x + self.cell_size - padding, y + self.cell_size - padding),
            5
        )
        pygame.draw.line(
            self.screen, self.x_color,
            (x + self.cell_size - padding, y + padding),
            (x + padding, y + self.cell_size - padding),
            5
        )
    
    def _draw_o(self, x, y):
        """Draw an O in the specified position."""
        # Calculate the center position
        center_x = x + self.cell_size // 2
        center_y = y + self.cell_size // 2
        radius = self.cell_size // 2 - 15
        
        # Draw the circle
        pygame.draw.circle(
            self.screen, self.o_color,
            (center_x, center_y),
            radius, 5
        )
    
    def animate_move(self, game_state, move, player):
        """
        Animate a move on the board.
        
        Args:
            game_state: Current game state
            move: Move to animate (row, col) for Tic Tac Toe, col for Connect 4
            player: Player making the move ('X' or 'O')
        """
        # Store as last move for highlighting
        if self.game_type == "tictactoe":
            self._animate_tictactoe_move(move, player)
            self.last_move = move  # Store as (row, col)
        else:
            target_row = self._animate_connect4_move(game_state, move, player)
            if target_row is not None:
                self.last_move = (target_row, move)  # Store as (row, col)
        
        # Update the internal board representation
        self.update_board(game_state)
    
    def _animate_tictactoe_move(self, move, player):
        """Animate a Tic Tac Toe move."""
        row, col = move
        
        # Simple animation - just update and redraw
        self.board[row][col] = player
        self.current_player = 'O' if player == 'X' else 'X'
        self.draw_board()
        pygame.display.flip()
        time.sleep(self.animation_speed)
    
    def _animate_connect4_move(self, game_state, col, player):
        """
        Animate a Connect 4 move with falling piece animation.
        
        Returns:
            The target row where the piece landed, or None if move was invalid
        """
        # Find the target row (lowest empty row in the column)
        target_row = self.rows - 1
        while target_row >= 0 and self.board[target_row][col] != ' ':
            target_row -= 1
        
        if target_row < 0:  # Column is full
            return None
        
        # Animate the piece falling
        self.falling_piece = player
        
        # Animate the piece falling from the top
        steps = 10  # Number of animation steps
        for step in range(steps + 1):
            current_row = step * target_row / steps
            self.falling_position = (col, current_row, target_row)
            
            self.draw_board()
            pygame.display.flip()
            time.sleep(self.animation_speed / steps)
        
        # Reset falling piece animation
        self.falling_piece = None
        self.falling_position = None
        
        # Update the board with the final position
        self.board[target_row][col] = player
        self.current_player = 'O' if player == 'X' else 'X'
        self.draw_board()
        
        return target_row
    
    def update_board(self, game_state):
        """
        Update the internal board representation from the game state.
        
        Args:
            game_state: Current game state with board information
        """
        if self.game_type == "tictactoe":
            self.board = [row[:] for row in game_state.board]
        else:  # connect4
            self.board = [row[:] for row in game_state.board]
        
        self.current_player = game_state.current_player
        self.draw_board()
    
    def visualize_game(self, game_class, player1, player2, delay=0.5):
        """
        Visualize a complete game between two players.
        
        Args:
            game_class: The game class to create instances from
            player1: First player (algorithm) - plays as X
            player2: Second player (algorithm or opponent) - plays as O
            delay: Delay between moves in seconds
            
        Returns:
            The final game state
        """
        game = game_class()
        self.update_board(game)
        self.draw_board()
        
        # Main game loop
        while not game.is_game_over():
            # Check for quit events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
            current_player = game.get_current_player()
            
            # Get move from the appropriate player
            if current_player == 'X':  # First player's turn
                move = player1.get_move(game)
            else:  # Second player's turn
                move = player2.get_move(game)
            
            # Apply the move to the game
            if isinstance(move, tuple):  # For Tic Tac Toe
                row, col = move
                game.make_move(row, col)
                self.animate_move(game, move, current_player)
            else:  # For Connect 4
                game.make_move(move)
                self.animate_move(game, move, current_player)
            
            # Add small delay between moves
            time.sleep(delay)
        
        # Show the final state for a moment
        time.sleep(1)
        
        # Display the result
        self._display_game_result(game)
        
        # Wait for user to close the window or press a key
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT or event.type == KEYDOWN:
                    waiting = False
        
        return game
    
    def _display_game_result(self, game):
        """Display the game result on the screen."""
        result_text = "Draw!"
        if game.get_winner() == 'X':
            result_text = f"{self.player1_name} wins!"
            text_color = self.x_color
        elif game.get_winner() == 'O':
            result_text = f"{self.player2_name} wins!"
            text_color = self.o_color
        else:
            text_color = self.info_color
        
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Draw result text
        font = pygame.font.Font(None, 48)
        text_surface = font.render(result_text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.width // 2, self.height // 2)
        
        # Add a background to the text for better visibility
        padding = 20
        background_rect = pygame.Rect(
            text_rect.left - padding,
            text_rect.top - padding,
            text_rect.width + 2 * padding,
            text_rect.height + 2 * padding
        )
        pygame.draw.rect(self.screen, (255, 255, 255, 230), background_rect)
        pygame.draw.rect(self.screen, text_color, background_rect, 2)
        
        self.screen.blit(text_surface, text_rect)
        
        # Add "Press any key to continue" message
        font_small = pygame.font.Font(None, 24)
        continue_text = "Press any key to continue"
        continue_surface = font_small.render(continue_text, True, self.info_color)
        continue_rect = continue_surface.get_rect()
        continue_rect.center = (self.width // 2, text_rect.bottom + 40)
        self.screen.blit(continue_surface, continue_rect)
        
        pygame.display.flip()