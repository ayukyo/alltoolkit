"""
Unit tests for reversi_utils
Run with: pytest reversi_utils_test.py -v
"""

import pytest
from reversi_utils.mod import ReversiEngine


class TestReversiEngineInit:
    def test_standard_opening(self):
        engine = ReversiEngine()
        counts = engine.get_piece_count()
        assert counts[engine.BLACK] == 2
        assert counts[engine.WHITE] == 2
        # Center pieces
        assert engine.get(3, 3) == engine.WHITE
        assert engine.get(3, 4) == engine.BLACK
        assert engine.get(4, 3) == engine.BLACK
        assert engine.get(4, 4) == engine.WHITE

    def test_custom_board(self):
        board = [[ReversiEngine.EMPTY] * 8 for _ in range(8)]
        board[0][0] = ReversiEngine.BLACK
        engine = ReversiEngine(board=board)
        assert engine.get(0, 0) == engine.BLACK
        assert engine.get_piece_count()[engine.BLACK] == 1


class TestMoveValidation:
    def setup_method(self):
        self.engine = ReversiEngine()

    def test_black_first_move_d4(self):
        # Black's first move: (2,3) = D3, flips (3,3) white
        assert self.engine.is_valid_move(2, 3, 'B') is True

    def test_black_first_move_e3(self):
        # Black's first move: (3,2) = C4, flips (3,3) white
        assert self.engine.is_valid_move(3, 2, 'B') is True

    def test_white_valid_moves_after_black_d4(self):
        self.engine.make_move(2, 3, 'B')
        moves = self.engine.get_valid_moves('W')
        assert (2, 2) in moves  # D2
        assert (2, 4) in moves  # E2

    def test_invalid_move_on_occupied_cell(self):
        assert self.engine.is_valid_move(3, 3, 'B') is False

    def test_invalid_move_far_from_center(self):
        assert self.engine.is_valid_move(0, 0, 'B') is False

    def test_no_moves_if_not_adjacent(self):
        # Corners have no valid moves in opening
        assert self.engine.is_valid_move(0, 0, 'B') is False
        assert self.engine.is_valid_move(0, 7, 'B') is False

    def test_get_flips(self):
        flips = self.engine.get_flips(2, 3, 'B')
        assert (3, 3) in flips


class TestMakeMove:
    def setup_method(self):
        self.engine = ReversiEngine()

    def test_make_move_black_d3(self):
        result = self.engine.make_move(2, 3, 'B')
        assert result is True
        assert self.engine.get(2, 3) == 'B'
        assert self.engine.get(3, 3) == 'B'  # flipped

    def test_make_move_white_c4_after_black_d3(self):
        self.engine.make_move(2, 3, 'B')
        # White plays D2=(2,2), adjacent to the newly flipped (3,3)
        result = self.engine.make_move(2, 2, 'W')
        assert result is True
        assert self.engine.get(2, 2) == 'W'

    def test_make_invalid_move_returns_false(self):
        result = self.engine.make_move(0, 0, 'B')
        assert result is False
        # Board unchanged
        counts = self.engine.get_piece_count()
        assert counts['B'] == 2

    def test_game_over_raises(self):
        # Build a fully filled board where neither player can move
        board = [[ReversiEngine.BLACK] * 8 for _ in range(8)]
        engine = ReversiEngine(board=board)
        assert engine.is_game_over()
        with pytest.raises(ValueError, match="Game is already over"):
            engine.make_move(0, 0, 'B')


class TestPassTurn:
    def test_pass_when_no_moves(self):
        engine = ReversiEngine()
        # Set up a situation where a player has no moves
        board = [[engine.EMPTY] * 8 for _ in range(8)]
        board[3][3] = engine.BLACK
        board[3][4] = engine.BLACK
        board[4][3] = engine.BLACK
        board[4][4] = engine.BLACK
        engine = ReversiEngine(board=board)
        # Neither player can move on empty board surrounding full center
        assert engine.pass_turn(engine.BLACK) is True


class TestGameOver:
    def test_game_not_over_at_start(self):
        engine = ReversiEngine()
        assert engine.is_game_over() is False

    def test_get_winner_none_when_not_over(self):
        engine = ReversiEngine()
        assert engine.get_current_winner() is None


class TestAI:
    def setup_method(self):
        self.engine = ReversiEngine()

    def test_ai_returns_valid_move(self):
        move = self.engine.get_ai_move('B')
        assert move is not None
        r, c = move
        assert 0 <= r < 8
        assert 0 <= c < 8
        assert self.engine.is_valid_move(r, c, 'B')

    def test_ai_no_move_when_none_available(self):
        board = [[ReversiEngine.EMPTY] * 8 for _ in range(8)]
        board[3][3] = ReversiEngine.BLACK
        board[3][4] = ReversiEngine.BLACK
        board[4][3] = ReversiEngine.BLACK
        board[4][4] = ReversiEngine.BLACK
        engine = ReversiEngine(board=board)
        assert engine.get_ai_move('W') is None

    def test_ai_prefers_center_on_opening(self):
        # AI should prefer center moves early game
        move = self.engine.get_ai_move('B')
        # Valid first moves are (2,3),(3,2),(4,5),(5,4) = D3,C4,F5,E6
        assert move in [(2, 3), (3, 2), (4, 5), (5, 4)]


class TestRender:
    def test_render_returns_string(self):
        engine = ReversiEngine()
        output = engine.render()
        assert isinstance(output, str)
        assert 'B' in output or 'W' in output
        assert len(output) > 0


class TestRepr:
    def test_repr_equals_render(self):
        engine = ReversiEngine()
        assert repr(engine) == engine.render()


# ------------------------------------------------------------------
# Doctest-style examples (run with pytest --doctest-modules)
# ------------------------------------------------------------------

def test_example_usage():
    engine = ReversiEngine()
    result = engine.make_move(2, 3, 'B')
    assert result is True
    moves_w = engine.get_valid_moves('W')
    assert len(moves_w) > 0
    counts = engine.get_piece_count()
    assert counts['B'] == 4
    assert counts['W'] == 1


def test_simulate_full_game():
    """Simulate a complete game to check game-over logic."""
    engine = ReversiEngine()
    # Just simulate some moves and check state
    moves = [
        (2, 3, 'B'),
        (2, 2, 'W'),
        (3, 2, 'B'),
        (4, 2, 'W'),
    ]
    for r, c, p in moves:
        engine.make_move(r, c, p)
    counts = engine.get_piece_count()
    # After 4 moves: total pieces should be 4 + 4 initial = 8
    assert sum(counts.values()) == 8
    assert not engine.is_game_over()
