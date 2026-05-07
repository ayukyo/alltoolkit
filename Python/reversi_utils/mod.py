"""
Reversi (Othello) Game Utilities

A complete implementation of the classic Reversi/Othello board game with:
- Game board management
- Move validation and execution
- Piece flipping logic
- Win/loss detection
- Simple AI (Minimax algorithm)
- Game serialization

Zero external dependencies - uses only Python standard library.
"""

from typing import Optional, Tuple, List, Set
from copy import deepcopy


# Constants
EMPTY = 0
BLACK = 1  # Black moves first
WHITE = 2

# Directions for checking valid moves (8 directions)
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]


class ReversiBoard:
    """
    Reversi/Othello game board manager.
    
    Board coordinates: (row, col) where both are 0-indexed.
    Standard board size is 8x8.
    """
    
    def __init__(self, size: int = 8):
        """
        Initialize a new Reversi board.
        
        Args:
            size: Board size (default 8 for standard Reversi)
        """
        if size < 4 or size % 2 != 0:
            raise ValueError("Board size must be an even number >= 4")
        
        self.size = size
        self.board = [[EMPTY] * size for _ in range(size)]
        self.current_player = BLACK
        self._setup_initial_position()
    
    def _setup_initial_position(self) -> None:
        """Set up the initial 4 pieces in the center."""
        center = self.size // 2
        # Standard starting position: diagonal pieces
        self.board[center - 1][center - 1] = WHITE
        self.board[center - 1][center] = BLACK
        self.board[center][center - 1] = BLACK
        self.board[center][center] = WHITE
    
    def copy(self) -> 'ReversiBoard':
        """Create a deep copy of the board."""
        new_board = ReversiBoard.__new__(ReversiBoard)
        new_board.size = self.size
        new_board.board = [row[:] for row in self.board]
        new_board.current_player = self.current_player
        return new_board
    
    def get(self, row: int, col: int) -> int:
        """
        Get the piece at a position.
        
        Args:
            row: Row index (0-indexed)
            col: Column index (0-indexed)
            
        Returns:
            EMPTY (0), BLACK (1), or WHITE (2)
        """
        return self.board[row][col]
    
    def set(self, row: int, col: int, piece: int) -> None:
        """Set a piece at a position (internal use)."""
        self.board[row][col] = piece
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if a position is within the board."""
        return 0 <= row < self.size and 0 <= col < self.size
    
    def opponent(self, player: int) -> int:
        """Get the opponent of a player."""
        if player == BLACK:
            return WHITE
        elif player == WHITE:
            return BLACK
        return EMPTY
    
    def get_flips(self, row: int, col: int, player: int) -> List[Tuple[int, int]]:
        """
        Get all pieces that would be flipped by placing a piece at (row, col).
        
        Args:
            row: Row index
            col: Column index
            player: The player making the move
            
        Returns:
            List of (row, col) positions that would be flipped
        """
        if self.board[row][col] != EMPTY:
            return []
        
        opponent = self.opponent(player)
        all_flips = []
        
        for dr, dc in DIRECTIONS:
            flips = []
            r, c = row + dr, col + dc
            
            # Follow the direction while we see opponent pieces
            while self.is_valid_position(r, c) and self.board[r][c] == opponent:
                flips.append((r, c))
                r += dr
                c += dc
            
            # If we ended on our own piece, these are valid flips
            if flips and self.is_valid_position(r, c) and self.board[r][c] == player:
                all_flips.extend(flips)
        
        return all_flips
    
    def is_valid_move(self, row: int, col: int, player: Optional[int] = None) -> bool:
        """
        Check if a move is valid.
        
        Args:
            row: Row index
            col: Column index
            player: Player making the move (defaults to current player)
            
        Returns:
            True if the move is valid
        """
        if player is None:
            player = self.current_player
        
        if not self.is_valid_position(row, col):
            return False
        
        if self.board[row][col] != EMPTY:
            return False
        
        return len(self.get_flips(row, col, player)) > 0
    
    def get_valid_moves(self, player: Optional[int] = None) -> List[Tuple[int, int]]:
        """
        Get all valid moves for a player.
        
        Args:
            player: Player to check (defaults to current player)
            
        Returns:
            List of (row, col) positions where the player can move
        """
        if player is None:
            player = self.current_player
        
        valid_moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))
        
        return valid_moves
    
    def has_valid_moves(self, player: Optional[int] = None) -> bool:
        """Check if a player has any valid moves."""
        return len(self.get_valid_moves(player)) > 0
    
    def make_move(self, row: int, col: int, player: Optional[int] = None) -> bool:
        """
        Make a move and flip pieces.
        
        Args:
            row: Row index
            col: Column index
            player: Player making the move (defaults to current player)
            
        Returns:
            True if the move was successful
        """
        if player is None:
            player = self.current_player
        
        if not self.is_valid_move(row, col, player):
            return False
        
        # Get pieces to flip
        flips = self.get_flips(row, col, player)
        
        # Place the piece
        self.board[row][col] = player
        
        # Flip opponent pieces
        for r, c in flips:
            self.board[r][c] = player
        
        # Switch player
        self.current_player = self.opponent(player)
        
        # If new player has no moves, switch back
        if not self.has_valid_moves(self.current_player):
            self.current_player = player
        
        return True
    
    def skip_turn(self) -> bool:
        """
        Skip the current player's turn (when no valid moves available).
        
        Returns:
            True if turn was skipped, False if player had valid moves
        """
        if self.has_valid_moves():
            return False
        
        self.current_player = self.opponent(self.current_player)
        return True
    
    def count_pieces(self) -> Tuple[int, int, int]:
        """
        Count pieces on the board.
        
        Returns:
            Tuple of (black_count, white_count, empty_count)
        """
        black = white = empty = 0
        for row in range(self.size):
            for col in range(self.size):
                piece = self.board[row][col]
                if piece == BLACK:
                    black += 1
                elif piece == WHITE:
                    white += 1
                else:
                    empty += 1
        
        return black, white, empty
    
    def get_pieces(self, player: int) -> Set[Tuple[int, int]]:
        """
        Get all positions occupied by a player.
        
        Args:
            player: BLACK or WHITE
            
        Returns:
            Set of (row, col) positions
        """
        positions = set()
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == player:
                    positions.add((row, col))
        
        return positions
    
    def is_game_over(self) -> bool:
        """
        Check if the game is over.
        
        Game ends when neither player can make a valid move.
        """
        return not (self.has_valid_moves(BLACK) or self.has_valid_moves(WHITE))
    
    def get_winner(self) -> Optional[int]:
        """
        Get the winner of the game.
        
        Returns:
            BLACK, WHITE, or None (for tie or game not over)
        """
        if not self.is_game_over():
            return None
        
        black, white, _ = self.count_pieces()
        
        if black > white:
            return BLACK
        elif white > black:
            return WHITE
        else:
            return None  # Tie
    
    def get_score(self) -> Tuple[int, int]:
        """
        Get the current score.
        
        Returns:
            Tuple of (black_score, white_score)
        """
        black, white, _ = self.count_pieces()
        return black, white
    
    def to_string(self, show_valid_moves: bool = False) -> str:
        """
        Convert the board to a string representation.
        
        Args:
            show_valid_moves: If True, mark valid moves with '*'
            
        Returns:
            String representation of the board
        """
        valid = set(self.get_valid_moves()) if show_valid_moves else set()
        
        symbols = {EMPTY: '·', BLACK: '●', WHITE: '○'}
        
        # Column headers
        header = '   ' + ' '.join(chr(ord('a') + i) for i in range(self.size))
        lines = [header]
        
        # Board rows
        for row in range(self.size):
            row_str = f'{row + 1:2} '
            for col in range(self.size):
                if (row, col) in valid:
                    row_str += '* '
                else:
                    row_str += symbols[self.board[row][col]] + ' '
            lines.append(row_str)
        
        # Score
        black, white, _ = self.count_pieces()
        lines.append(f'\nBlack ●: {black}  White ○: {white}')
        
        # Current player
        player_name = 'Black' if self.current_player == BLACK else 'White'
        lines.append(f'Current: {player_name}')
        
        return '\n'.join(lines)
    
    def __str__(self) -> str:
        return self.to_string()
    
    def serialize(self) -> dict:
        """
        Serialize the game state to a dictionary.
        
        Returns:
            Dictionary containing game state
        """
        return {
            'size': self.size,
            'board': self.board,
            'current_player': self.current_player
        }
    
    @classmethod
    def deserialize(cls, data: dict) -> 'ReversiBoard':
        """
        Create a board from serialized data.
        
        Args:
            data: Dictionary from serialize()
            
        Returns:
            ReversiBoard instance
        """
        board = cls.__new__(cls)
        board.size = data['size']
        board.board = [row[:] for row in data['board']]
        board.current_player = data['current_player']
        return board
    
    def to_fen(self) -> str:
        """
        Export board to FEN-like notation.
        
        Format: <board>/<current_player>/<scores>
        Board: B=Black, W=White, numbers=consecutive empties
        """
        rows = []
        for row in range(self.size):
            row_str = ''
            empty_count = 0
            for col in range(self.size):
                piece = self.board[row][col]
                if piece == EMPTY:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        row_str += str(empty_count)
                        empty_count = 0
                    row_str += 'B' if piece == BLACK else 'W'
            if empty_count > 0:
                row_str += str(empty_count)
            rows.append(row_str)
        
        board_str = '/'.join(rows)
        player_str = 'b' if self.current_player == BLACK else 'w'
        
        return f"{board_str} {player_str}"
    
    @classmethod
    def from_fen(cls, fen: str) -> 'ReversiBoard':
        """
        Create a board from FEN-like notation.
        
        Args:
            fen: FEN string from to_fen()
            
        Returns:
            ReversiBoard instance
        """
        parts = fen.split(' ')
        board_str = parts[0]
        player_str = parts[1] if len(parts) > 1 else 'b'
        
        rows = board_str.split('/')
        size = len(rows)
        
        board = cls.__new__(cls)
        board.size = size
        board.board = [[EMPTY] * size for _ in range(size)]
        board.current_player = BLACK if player_str == 'b' else WHITE
        
        for row, row_str in enumerate(rows):
            col = 0
            for char in row_str:
                if char.isdigit():
                    col += int(char)
                elif char == 'B':
                    board.board[row][col] = BLACK
                    col += 1
                elif char == 'W':
                    board.board[row][col] = WHITE
                    col += 1
        
        return board


def get_opening_moves() -> List[Tuple[str, str]]:
    """
    Get recommended opening moves for Black.
    
    Returns:
        List of (situation, recommendation) tuples
    """
    return [
        ("Standard opening", "d3 or c4 - avoid giving corners early"),
        ("Diagonal opening", "c4 or d3 - controls center diagonals"),
        ("Avoid X-squares", "Never play to squares adjacent to corners"),
        ("Edge strategy", "Build towards edges but avoid early edge moves"),
        ("Corner priority", "Corners can never be flipped - prioritize them"),
    ]


def evaluate_position(board: ReversiBoard, player: int) -> int:
    """
    Evaluate a board position for a player.
    
    Uses a simple heuristic based on:
    - Corner control (high value)
    - Edge control (medium value)
    - X-squares (adjacent to corners, negative value)
    - Piece count
    
    Args:
        board: The game board
        player: The player to evaluate for
        
    Returns:
        Position score (higher is better)
    """
    if board.is_game_over():
        winner = board.get_winner()
        if winner == player:
            return 10000
        elif winner is not None:
            return -10000
        return 0
    
    score = 0
    opponent = board.opponent(player)
    size = board.size
    last = size - 1
    
    # Corner weights
    corners = [(0, 0), (0, last), (last, 0), (last, last)]
    corner_weight = 25
    
    # X-squares (adjacent to corners diagonally)
    x_squares = [(1, 1), (1, last-1), (last-1, 1), (last-1, last-1)]
    x_weight = -25
    
    # C-squares (adjacent to corners orthogonally)
    c_squares = [
        (0, 1), (1, 0),
        (0, last-1), (1, last),
        (last-1, 0), (last, 1),
        (last-1, last), (last, last-1)
    ]
    c_weight = -10
    
    # Edge weight
    edge_weight = 5
    
    for row in range(size):
        for col in range(size):
            piece = board.get(row, col)
            if piece == EMPTY:
                continue
            
            value = 1  # Base value
            
            # Corner bonus
            if (row, col) in corners:
                value = corner_weight
            # X-square penalty
            elif (row, col) in x_squares:
                # Only penalize if adjacent corner is empty
                adj_corner = None
                if row == 1 and col == 1:
                    adj_corner = (0, 0)
                elif row == 1 and col == last - 1:
                    adj_corner = (0, last)
                elif row == last - 1 and col == 1:
                    adj_corner = (last, 0)
                elif row == last - 1 and col == last - 1:
                    adj_corner = (last, last)
                
                if adj_corner and board.get(*adj_corner) == EMPTY:
                    value = x_weight
            # C-square penalty
            elif (row, col) in c_squares:
                value = c_weight
            # Edge bonus
            elif row == 0 or row == last or col == 0 or col == last:
                value = edge_weight
            
            if piece == player:
                score += value
            else:
                score -= value
    
    # Mobility bonus (number of valid moves)
    player_moves = len(board.get_valid_moves(player))
    opponent_moves = len(board.get_valid_moves(opponent))
    score += 2 * (player_moves - opponent_moves)
    
    return score


def minimax(board: ReversiBoard, depth: int, player: int,
            maximizing: bool = True, alpha: int = float('-inf'),
            beta: int = float('inf')) -> Tuple[int, Optional[Tuple[int, int]]]:
    """
    Minimax algorithm with alpha-beta pruning for Reversi AI.
    
    Args:
        board: Current board state
        depth: Search depth
        player: The AI player
        maximizing: True if maximizing player's turn
        alpha: Alpha value for pruning
        beta: Beta value for pruning
        
    Returns:
        Tuple of (score, best_move)
    """
    if depth == 0 or board.is_game_over():
        return evaluate_position(board, player), None
    
    current = player if maximizing else board.opponent(player)
    moves = board.get_valid_moves(current)
    
    if not moves:
        # Pass turn
        new_board = board.copy()
        new_board.current_player = board.opponent(current)
        return minimax(new_board, depth - 1, player, not maximizing, alpha, beta)
    
    best_move = moves[0] if moves else None
    
    if maximizing:
        max_eval = float('-inf')
        for move in moves:
            new_board = board.copy()
            new_board.make_move(move[0], move[1], current)
            eval_score, _ = minimax(new_board, depth - 1, player, False, alpha, beta)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = board.copy()
            new_board.make_move(move[0], move[1], current)
            eval_score, _ = minimax(new_board, depth - 1, player, True, alpha, beta)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move


def get_best_move(board: ReversiBoard, player: int, depth: int = 4) -> Optional[Tuple[int, int]]:
    """
    Get the best move for a player using minimax.
    
    Args:
        board: Current board state
        player: The player to find a move for
        depth: Search depth (default 4)
        
    Returns:
        Best move as (row, col), or None if no moves available
    """
    _, move = minimax(board, depth, player)
    return move


def get_greedy_move(board: ReversiBoard, player: int) -> Optional[Tuple[int, int]]:
    """
    Get a greedy move (maximizes immediate piece flips).
    
    This is a simple AI that picks the move flipping the most pieces.
    
    Args:
        board: Current board state
        player: The player to find a move for
        
    Returns:
        Best greedy move as (row, col), or None if no moves available
    """
    moves = board.get_valid_moves(player)
    if not moves:
        return None
    
    best_move = moves[0]
    best_flips = 0
    
    for move in moves:
        flips = len(board.get_flips(move[0], move[1], player))
        # Bonus for corners
        if move in [(0, 0), (0, board.size-1), (board.size-1, 0), (board.size-1, board.size-1)]:
            flips += 100
        if flips > best_flips:
            best_flips = flips
            best_move = move
    
    return best_move


def play_game_random() -> Tuple[int, int]:
    """
    Play a game with random moves for both players.
    
    Returns:
        Final score as (black_score, white_score)
    """
    import random
    
    board = ReversiBoard()
    
    while not board.is_game_over():
        moves = board.get_valid_moves()
        if moves:
            move = random.choice(moves)
            board.make_move(move[0], move[1])
        else:
            board.skip_turn()
    
    return board.get_score()


def analyze_game(board: ReversiBoard) -> dict:
    """
    Analyze a game position.
    
    Args:
        board: The game board
        
    Returns:
        Dictionary with analysis results
    """
    black, white, empty = board.count_pieces()
    black_moves = board.get_valid_moves(BLACK)
    white_moves = board.get_valid_moves(WHITE)
    
    # Calculate territory (pieces that cannot be flipped)
    black_territory = 0
    white_territory = 0
    
    for row in range(board.size):
        for col in range(board.size):
            piece = board.get(row, col)
            if piece == EMPTY:
                continue
            
            # Check if this piece can potentially be flipped
            # A piece is territory if all 8 directions either:
            # - Hit the edge, or
            # - Hit a piece of the same color first
            opponent = board.opponent(piece)
            can_flip = False
            
            for dr, dc in DIRECTIONS:
                r, c = row + dr, col + dc
                path = []
                
                while board.is_valid_position(r, c):
                    path_piece = board.get(r, c)
                    if path_piece == EMPTY:
                        break  # Empty square - not a line
                    if path_piece == opponent:
                        path.append((r, c))
                    elif path_piece == piece:
                        # Found our piece on the other end
                        # This direction is safe
                        break
                    r += dr
                    c += dc
                else:
                    # Hit the edge - direction is safe
                    continue
                
                if path:
                    # There's a potential flip direction
                    can_flip = True
                    break
            
            if piece == BLACK:
                if not can_flip:
                    black_territory += 1
            else:
                if not can_flip:
                    white_territory += 1
    
    return {
        'black_pieces': black,
        'white_pieces': white,
        'empty_squares': empty,
        'black_mobility': len(black_moves),
        'white_mobility': len(white_moves),
        'current_player': 'black' if board.current_player == BLACK else 'white',
        'game_over': board.is_game_over(),
        'winner': 'black' if board.get_winner() == BLACK else 
                  'white' if board.get_winner() == WHITE else None,
        'black_territory': black_territory,
        'white_territory': white_territory,
        'position_score': evaluate_position(board, BLACK)
    }


# Piece constants for easy import
__all__ = [
    'EMPTY', 'BLACK', 'WHITE', 'DIRECTIONS',
    'ReversiBoard',
    'evaluate_position',
    'minimax',
    'get_best_move',
    'get_greedy_move',
    'get_opening_moves',
    'play_game_random',
    'analyze_game'
]