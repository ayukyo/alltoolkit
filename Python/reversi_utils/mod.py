"""
Reversi (Othello) Game Engine

A zero-dependency Reversi/Othello game engine with move validation,
game state management, and AI opponent implementation.

Board: 8x8 grid, Black ('B') vs White ('W')
- Black moves first
- A move must flip at least one opponent piece
- Valid moves must capture in any of 8 directions
- If a player has no valid moves, they pass
- Game ends when neither player can move
- Winner: most pieces on board

Example:
    >>> from reversi_utils.mod import ReversiEngine
    >>> engine = ReversiEngine()
    >>> engine.make_move(2, 3, 'B')
    True
    >>> engine.get_valid_moves('W')
    [(2, 2), (3, 3), ...]
    >>> engine.get_piece_count()
    {'B': 4, 'W': 1}
"""

from typing import Optional, List, Dict, Tuple


class ReversiEngine:
    """Reversi/Othello game engine with board state and move validation."""

    EMPTY = '.'
    BLACK = 'B'
    WHITE = 'W'

    DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    def __init__(self, board: Optional[List[List[str]]] = None):
        """
        Initialize the Reversi board with standard starting position.

        Args:
            board: Optional 8x8 board to use instead of standard setup.
                   Use EMPTY, BLACK, WHITE as cell values.
        """
        if board:
            self.board = [row[:] for row in board]
        else:
            self.board = [[self.EMPTY] * 8 for _ in range(8)]
            # Standard starting position: 2 each in center
            self.board[3][3] = self.WHITE
            self.board[3][4] = self.BLACK
            self.board[4][3] = self.BLACK
            self.board[4][4] = self.WHITE
        self._last_move: Optional[Tuple[int, int]] = None
        self._last_player: Optional[str] = None

    # ------------------------------------------------------------------
    # Board query
    # ------------------------------------------------------------------

    def get_board(self) -> List[List[str]]:
        """Return a deep copy of the current board."""
        return [row[:] for row in self.board]

    def get_piece_count(self) -> Dict[str, int]:
        """Return piece counts for both players."""
        counts = {self.BLACK: 0, self.WHITE: 0}
        for row in self.board:
            for cell in row:
                if cell in counts:
                    counts[cell] += 1
        return counts

    def get(self, row: int, col: int) -> str:
        """Return piece at row, col (or EMPTY if out of bounds)."""
        if not (0 <= row < 8 and 0 <= col < 8):
            return self.EMPTY
        return self.board[row][col]

    def is_on_board(self, row: int, col: int) -> bool:
        """Check if (row, col) is within the 8x8 board."""
        return 0 <= row < 8 and 0 <= col < 8

    def is_game_over(self) -> bool:
        """Return True if neither player has any valid moves."""
        return (
            len(self.get_valid_moves(self.BLACK)) == 0
            and len(self.get_valid_moves(self.WHITE)) == 0
        )

    def get_current_winner(self) -> Optional[str]:
        """
        Return the winning player, EMPTY ('.') for draw, or None if game
        is not yet over.
        """
        if not self.is_game_over():
            return None
        counts = self.get_piece_count()
        if counts[self.BLACK] > counts[self.WHITE]:
            return self.BLACK
        if counts[self.WHITE] > counts[self.BLACK]:
            return self.WHITE
        return self.EMPTY

    # ------------------------------------------------------------------
    # Move validation
    # ------------------------------------------------------------------

    def _get_flips_in_direction(
        self, row: int, col: int, player: str, d_row: int, d_col: int
    ) -> List[Tuple[int, int]]:
        """
        Starting from (row, col) and moving in direction (d_row, d_col),
        collect opponent pieces that would be flipped.
        Returns list of (r, c) positions to flip.
        """
        opponent = self.WHITE if player == self.BLACK else self.BLACK
        cur_row, cur_col = row + d_row, col + d_col
        flips: List[Tuple[int, int]] = []

        # Walk along direction collecting opponent pieces
        while self.is_on_board(cur_row, cur_col) and self.get(cur_row, cur_col) == opponent:
            flips.append((cur_row, cur_col))
            cur_row += d_row
            cur_col += d_col

        # Valid only if we end on our own piece
        if not flips or not self.is_on_board(cur_row, cur_col):
            return []
        if self.get(cur_row, cur_col) != player:
            return []
        return flips

    def get_flips(self, row: int, col: int, player: str) -> List[Tuple[int, int]]:
        """
        Return list of all (r, c) positions that would be flipped if player
        places a piece at (row, col). Empty if invalid move.
        """
        if not self.is_on_board(row, col) or self.get(row, col) != self.EMPTY:
            return []
        all_flips: List[Tuple[int, int]] = []
        for d in self.DIRECTIONS:
            flips = self._get_flips_in_direction(row, col, player, d[0], d[1])
            all_flips.extend(flips)
        return all_flips

    def is_valid_move(self, row: int, col: int, player: str) -> bool:
        """Return True if (row, col) is a valid move for player."""
        return bool(self.get_flips(row, col, player))

    def get_valid_moves(self, player: str) -> List[Tuple[int, int]]:
        """Return all valid move positions for player, sorted (row, col)."""
        moves: List[Tuple[int, int]] = []
        for r in range(8):
            for c in range(8):
                if self.is_valid_move(r, c, player):
                    moves.append((r, c))
        return sorted(moves)

    # ------------------------------------------------------------------
    # Making moves
    # ------------------------------------------------------------------

    def make_move(self, row: int, col: int, player: str) -> bool:
        """
        Place a piece at (row, col) for player and flip captured pieces.

        Returns True on success, False if the move is invalid.
        Raises ValueError if the game is already over.
        """
        if self.is_game_over():
            raise ValueError("Game is already over.")

        flips = self.get_flips(row, col, player)
        if not flips:
            return False

        self.board[row][col] = player
        for r, c in flips:
            self.board[r][c] = player
        self._last_move = (row, col)
        self._last_player = player
        return True

    def pass_turn(self, player: str) -> bool:
        """
        Register a pass for player. Returns True if the pass was valid
        (no valid moves available), False if the player had moves.
        """
        if self.get_valid_moves(player):
            return False
        self._last_move = None
        self._last_player = player
        return True

    # ------------------------------------------------------------------
    # Board rendering
    # ------------------------------------------------------------------

    def render(self) -> str:
        """Return a human-readable string representation of the board."""
        col_headers = "    " + "  ".join(str(i) for i in range(8))
        separator = "  +" + "-" * 17 + "+"
        lines = [col_headers, separator]
        for i, row in enumerate(self.board):
            cells = "  ".join(cell for cell in row)
            lines.append(f"{i} |{cells} |")
        lines.append(separator)
        return "\n".join(lines)

    def __repr__(self) -> str:
        return self.render()

    # ------------------------------------------------------------------
    # AI Opponent
    # ------------------------------------------------------------------

    @staticmethod
    def _mobility_score(player: str, opponent: str, board: List[List[str]]) -> int:
        """Count valid moves for player."""
        moves = 0
        for r in range(8):
            for c in range(8):
                if board[r][c] != ReversiEngine.EMPTY:
                    continue
                if ReversiEngine._has_flip(r, c, player, opponent, board):
                    moves += 1
        return moves

    @staticmethod
    def _has_flip(
        row: int, col: int, player: str, opponent: str, board: List[List[str]]
    ) -> bool:
        """Return True if placing at (row, col) would flip at least one piece."""
        for d_r, d_c in ReversiEngine.DIRECTIONS:
            cur_r, cur_c = row + d_r, col + d_c
            found_opponent = False
            while 0 <= cur_r < 8 and 0 <= cur_c < 8 and board[cur_r][cur_c] == opponent:
                found_opponent = True
                cur_r += d_r
                cur_c += d_c
            if found_opponent and 0 <= cur_r < 8 and 0 <= cur_c < 8:
                if board[cur_r][cur_c] == player:
                    return True
        return False

    @staticmethod
    def _positional_score(board: List[List[str]]) -> Dict[str, float]:
        """
        Positional weights for corner and edge dominance.
        Corners are most valuable; edges are stable.
        """
        weights = [
            [100, -20, 10,  5,  5, 10, -20, 100],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [ 10,  -2,  1,  1,  1,  1,  -2,  10],
            [  5,  -2,  1,  1,  1,  1,  -2,   5],
            [  5,  -2,  1,  1,  1,  1,  -2,   5],
            [ 10,  -2,  1,  1,  1,  1,  -2,  10],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [100, -20, 10,  5,  5, 10, -20, 100],
        ]
        scores: Dict[str, float] = {ReversiEngine.BLACK: 0.0, ReversiEngine.WHITE: 0.0}
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece in scores:
                    scores[piece] += weights[r][c]
        return scores

    def get_ai_move(self, player: str) -> Optional[Tuple[int, int]]:
        """
        Return the best move for the AI using a minimax-style evaluation
        combining mobility, piece count, and positional advantage.

        Returns None if player has no valid moves.
        """
        valid_moves = self.get_valid_moves(player)
        if not valid_moves:
            return None

        opponent = self.WHITE if player == self.BLACK else self.BLACK
        best_move: Optional[Tuple[int, int]] = None
        best_score = float("-inf")

        for move_r, move_c in valid_moves:
            flips = self.get_flips(move_r, move_c, player)
            # Simulate the move
            original = self.board[move_r][move_c]
            self.board[move_r][move_c] = player
            for fr, fc in flips:
                self.board[fr][fc] = player

            # Evaluate board
            piece_counts = self.get_piece_count()
            pos_scores = self._positional_score(self.board)
            mobility = self._mobility_score(player, opponent, self.board)
            opp_mobility = self._mobility_score(opponent, player, self.board)

            # Weighted score: piece count + positional + mobility advantage
            piece_score = piece_counts[player] - piece_counts[opponent]
            pos_score = pos_scores[player] - pos_scores[opponent]
            mobility_score = mobility - opp_mobility
            total = piece_score + pos_score * 0.5 + mobility_score * 2.0

            if total > best_score:
                best_score = total
                best_move = (move_r, move_c)

            # Undo simulation
            self.board[move_r][move_c] = original
            for fr, fc in flips:
                self.board[fr][fc] = opponent

        return best_move
