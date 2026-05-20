"""
Test suite for Connect Four game utilities.
Run with: python -m pytest test_connect_four.py -v
"""

import pytest
from .board import Board
from .player import HumanPlayer, RandomPlayer
from .ai import AIPlayer, create_ai_player
from .game import ConnectFourGame, GameStatus, create_game
from .constants import (
    ROWS, COLS, EMPTY, PLAYER_ONE, PLAYER_TWO,
    Difficulty, DIFFICULTY_DEPTHS
)


class TestBoard:
    """Tests for Board class."""
    
    def test_board_creation(self):
        """Test board initialization."""
        board = Board()
        assert board.is_empty()
        assert len(board.get_available_columns()) == COLS
        assert board.count_pieces(PLAYER_ONE) == 0
        assert board.count_pieces(PLAYER_TWO) == 0
    
    def test_drop_piece(self):
        """Test dropping a piece."""
        board = Board()
        
        # Drop in column 0
        row = board.drop_piece(0, PLAYER_ONE)
        assert row == ROWS - 1  # Should land at bottom
        assert board.get_cell(row, 0) == PLAYER_ONE
        assert not board.is_empty()
        
        # Drop again in same column
        row2 = board.drop_piece(0, PLAYER_TWO)
        assert row2 == ROWS - 2  # Should stack on top
        assert board.get_cell(row2, 0) == PLAYER_TWO
    
    def test_column_full(self):
        """Test column full detection."""
        board = Board()
        
        # Fill a column
        for _ in range(ROWS):
            board.drop_piece(0, PLAYER_ONE)
        
        assert board.is_column_full(0)
        assert 0 not in board.get_available_columns()
        
        # Try to drop in full column
        with pytest.raises(ValueError):
            board.drop_piece(0, PLAYER_ONE)
    
    def test_horizontal_win(self):
        """Test horizontal win detection."""
        board = Board()
        
        # Create horizontal win for player 1 in bottom row
        for col in range(4):
            board.drop_piece(col, PLAYER_ONE)
            if col < 3:
                board.drop_piece(col, PLAYER_TWO)
        
        assert board.check_win(PLAYER_ONE)
        assert not board.check_win(PLAYER_TWO)
    
    def test_vertical_win(self):
        """Test vertical win detection."""
        board = Board()
        
        # Create vertical win for player 1
        for _ in range(4):
            board.drop_piece(0, PLAYER_ONE)
            board.drop_piece(1, PLAYER_TWO)
        
        assert board.check_win(PLAYER_ONE)
        assert not board.check_win(PLAYER_TWO)
    
    def test_diagonal_win_positive(self):
        """Test diagonal win (positive slope)."""
        board = Board()
        
        # Create diagonal win
        # Column 0: 1 piece (P1)
        # Column 1: 2 pieces (P2, P1)
        # Column 2: 3 pieces (P1, P2, P1)
        # Column 3: 4 pieces (P2, P1, P2, P1)
        
        board.drop_piece(0, PLAYER_ONE)  # Col 0, row 5
        board.drop_piece(1, PLAYER_TWO)  # Col 1, row 5
        board.drop_piece(1, PLAYER_ONE)  # Col 1, row 4
        board.drop_piece(2, PLAYER_ONE)  # Col 2, row 5
        board.drop_piece(2, PLAYER_TWO)  # Col 2, row 4
        board.drop_piece(2, PLAYER_ONE)  # Col 2, row 3
        board.drop_piece(3, PLAYER_TWO)  # Col 3, row 5
        board.drop_piece(3, PLAYER_ONE)  # Col 3, row 4
        board.drop_piece(3, PLAYER_TWO)  # Col 3, row 3
        board.drop_piece(3, PLAYER_ONE)  # Col 3, row 2
        
        assert board.check_win(PLAYER_ONE)
    
    def test_diagonal_win_negative(self):
        """Test diagonal win (negative slope)."""
        board = Board()
        
        # Create diagonal win (negative slope)
        board.drop_piece(3, PLAYER_ONE)  # Col 3, row 5
        board.drop_piece(2, PLAYER_TWO)  # Col 2, row 5
        board.drop_piece(2, PLAYER_ONE)  # Col 2, row 4
        board.drop_piece(1, PLAYER_ONE)  # Col 1, row 5
        board.drop_piece(1, PLAYER_TWO)  # Col 1, row 4
        board.drop_piece(1, PLAYER_ONE)  # Col 1, row 3
        board.drop_piece(0, PLAYER_TWO)  # Col 0, row 5
        board.drop_piece(0, PLAYER_ONE)  # Col 0, row 4
        board.drop_piece(0, PLAYER_TWO)  # Col 0, row 3
        board.drop_piece(0, PLAYER_ONE)  # Col 0, row 2
        
        assert board.check_win(PLAYER_ONE)
    
    def test_draw(self):
        """Test draw detection."""
        board = Board()
        
        # Fill board without winning (alternating pattern)
        for col in range(COLS):
            for row in range(ROWS):
                player = PLAYER_ONE if (col + row) % 2 == 0 else PLAYER_TWO
                board._grid[row][col] = player
        
        # Remove wins if any
        board = Board()
        
        # Fill with alternating pattern that prevents wins
        for col in range(COLS):
            for row in range(ROWS):
                # Alternate players in a way that prevents 4 in a row
                if (col // 2 + row) % 2 == 0:
                    board._grid[ROWS - 1 - row][col] = PLAYER_ONE
                else:
                    board._grid[ROWS - 1 - row][col] = PLAYER_TWO
        
        assert board.is_full()
        assert not board.check_win(PLAYER_ONE)
        assert not board.check_win(PLAYER_TWO)
    
    def test_serialization(self):
        """Test board serialization."""
        board = Board()
        board.drop_piece(0, PLAYER_ONE)
        board.drop_piece(1, PLAYER_TWO)
        
        serialized = board.serialize()
        assert isinstance(serialized, str)
        
        restored = Board.deserialize(serialized)
        assert board == restored
    
    def test_copy(self):
        """Test board copying."""
        board = Board()
        board.drop_piece(0, PLAYER_ONE)
        
        copy = board.copy()
        assert board == copy
        
        # Modify original
        board.drop_piece(1, PLAYER_TWO)
        assert board != copy


class TestPlayer:
    """Tests for Player classes."""
    
    def test_human_player(self):
        """Test HumanPlayer."""
        player = HumanPlayer(PLAYER_ONE, "Test")
        assert player.player_id == PLAYER_ONE
        assert player.name == "Test"
        assert not player.is_ready()
        
        player.set_move(3)
        assert player.is_ready()
        
        board = Board()
        assert player.get_move(board) == 3
        assert not player.is_ready()  # Should clear after use
    
    def test_random_player(self):
        """Test RandomPlayer."""
        player = RandomPlayer(PLAYER_TWO, "Random")
        assert player.player_id == PLAYER_TWO
        
        board = Board()
        move = player.get_move(board)
        assert 0 <= move < COLS
    
    def test_invalid_player_id(self):
        """Test invalid player ID raises error."""
        with pytest.raises(ValueError):
            HumanPlayer(3, "Invalid")


class TestAIPlayer:
    """Tests for AIPlayer class."""
    
    def test_ai_creation(self):
        """Test AI player creation."""
        ai = AIPlayer(PLAYER_ONE, Difficulty.MEDIUM, "Test AI")
        assert ai.player_id == PLAYER_ONE
        assert ai.difficulty == Difficulty.MEDIUM
        assert ai.name == "Test AI"
    
    def test_ai_factory(self):
        """Test AI player factory function."""
        ai = create_ai_player(PLAYER_TWO, "hard", "Factory AI")
        assert ai.player_id == PLAYER_TWO
        assert ai.difficulty == Difficulty.HARD
        
        with pytest.raises(ValueError):
            create_ai_player(PLAYER_ONE, "invalid")
    
    def test_ai_makes_valid_move(self):
        """Test AI makes valid moves."""
        ai = AIPlayer(PLAYER_ONE, Difficulty.MEDIUM)
        board = Board()
        
        for _ in range(10):  # Test multiple times
            move = ai.get_move(board)
            assert 0 <= move < COLS
            assert not board.is_column_full(move)
    
    def test_ai_blocks_winning_move(self):
        """Test AI blocks opponent's winning move."""
        ai = AIPlayer(PLAYER_ONE, Difficulty.HARD)
        board = Board()
        
        # Set up situation where player 2 is about to win
        board.drop_piece(0, PLAYER_TWO)
        board.drop_piece(1, PLAYER_TWO)
        board.drop_piece(2, PLAYER_TWO)
        
        # AI should block column 3
        move = ai.get_move(board)
        assert move == 3  # Block the winning column
    
    def test_ai_takes_winning_move(self):
        """Test AI takes winning move when available."""
        ai = AIPlayer(PLAYER_ONE, Difficulty.HARD)
        board = Board()
        
        # Set up situation where AI can win
        board.drop_piece(0, PLAYER_ONE)
        board.drop_piece(1, PLAYER_ONE)
        board.drop_piece(2, PLAYER_ONE)
        
        # AI should take column 3 to win
        move = ai.get_move(board)
        assert move == 3
    
    def test_difficulty_levels(self):
        """Test different difficulty levels."""
        for diff in Difficulty:
            ai = AIPlayer(PLAYER_ONE, diff)
            assert ai.difficulty == diff
            assert ai._depth == DIFFICULTY_DEPTHS[diff]


class TestGame:
    """Tests for ConnectFourGame class."""
    
    def test_game_creation(self):
        """Test game initialization."""
        game = ConnectFourGame()
        assert game.status == GameStatus.IN_PROGRESS
        assert game.current_player_id == PLAYER_ONE
        assert game.move_count == 0
        assert not game.is_game_over()
    
    def test_make_move(self):
        """Test making moves."""
        game = ConnectFourGame()
        
        success, msg = game.make_move(3)
        assert success
        assert game.move_count == 1
        assert game.current_player_id == PLAYER_TWO
    
    def test_invalid_move(self):
        """Test invalid move handling."""
        game = ConnectFourGame()
        
        # Invalid column
        success, msg = game.make_move(10)
        assert not success
    
    def test_game_over_after_win(self):
        """Test game state after win."""
        game = ConnectFourGame()
        
        # Make winning moves for player 1
        for col in range(4):
            game.make_move(col)  # Player 1
            if col < 3:
                game.make_move(col)  # Player 2
        
        assert game.is_game_over()
        assert game.winner == PLAYER_ONE
        assert game.status == GameStatus.PLAYER_ONE_WINS
    
    def test_undo_move(self):
        """Test move undo."""
        game = ConnectFourGame()
        
        game.make_move(3)
        assert game.move_count == 1
        
        assert game.undo_last_move()
        assert game.move_count == 0
        assert game.current_player_id == PLAYER_ONE
    
    def test_game_reset(self):
        """Test game reset."""
        game = ConnectFourGame()
        
        game.make_move(3)
        game.make_move(2)
        game.reset()
        
        assert game.move_count == 0
        assert game.status == GameStatus.IN_PROGRESS
        assert game.board.is_empty()
    
    def test_serialization(self):
        """Test game serialization."""
        game = ConnectFourGame()
        game.make_move(3)
        game.make_move(2)
        
        data = game.serialize()
        assert 'board' in data
        assert 'current_player_id' in data
        assert 'move_history' in data
        
        restored = ConnectFourGame.deserialize(data)
        assert restored.current_player_id == game.current_player_id
        assert restored.move_count == game.move_count
    
    def test_json_serialization(self):
        """Test JSON serialization."""
        game = ConnectFourGame()
        game.make_move(3)
        
        json_str = game.to_json()
        restored = ConnectFourGame.from_json(json_str)
        
        assert restored.current_player_id == game.current_player_id


class TestCreateGame:
    """Tests for create_game factory function."""
    
    def test_human_vs_ai(self):
        """Test human vs AI mode."""
        game = create_game("human_vs_ai")
        assert isinstance(game.player1, HumanPlayer)
        assert isinstance(game.player2, AIPlayer)
    
    def test_human_vs_human(self):
        """Test human vs human mode."""
        game = create_game("human_vs_human")
        assert isinstance(game.player1, HumanPlayer)
        assert isinstance(game.player2, HumanPlayer)
    
    def test_ai_vs_ai(self):
        """Test AI vs AI mode."""
        game = create_game("ai_vs_ai")
        assert isinstance(game.player1, AIPlayer)
        assert isinstance(game.player2, AIPlayer)
    
    def test_ai_vs_random(self):
        """Test AI vs random mode."""
        game = create_game("ai_vs_random")
        assert isinstance(game.player1, AIPlayer)
        assert isinstance(game.player2, RandomPlayer)
    
    def test_invalid_mode(self):
        """Test invalid mode raises error."""
        with pytest.raises(ValueError):
            create_game("invalid_mode")


class TestWinningPositions:
    """Tests for winning positions detection."""
    
    def test_horizontal_winning_positions(self):
        """Test getting horizontal winning positions."""
        game = ConnectFourGame()
        
        # Create winning position
        for col in range(4):
            game.make_move(col)  # Player 1
            if col < 3:
                game.make_move(col)  # Player 2
        
        positions = game.winning_positions
        assert positions is not None
        assert len(positions) == 4
        
        # Check positions are correct (bottom row, columns 0-3)
        rows = [p[0] for p in positions]
        cols = [p[1] for p in positions]
        assert all(r == ROWS - 1 for r in rows)
        assert sorted(cols) == [0, 1, 2, 3]


class TestIntegration:
    """Integration tests for complete games."""
    
    def test_ai_vs_ai_game(self):
        """Test complete AI vs AI game."""
        game = create_game("ai_vs_ai", "medium")
        
        max_moves = ROWS * COLS
        moves = 0
        
        while not game.is_game_over() and moves < max_moves:
            move = game.get_ai_move()
            success, _ = game.make_move(move)
            assert success
            moves += 1
        
        assert game.is_game_over()
        assert game.status in [
            GameStatus.PLAYER_ONE_WINS,
            GameStatus.PLAYER_TWO_WINS,
            GameStatus.DRAW
        ]
    
    def test_ai_always_blocks_immediate_win(self):
        """Test that AI always blocks immediate winning threats."""
        for _ in range(10):  # Run multiple times for randomness
            game = create_game("ai_vs_ai", "hard")
            
            # Play until someone wins or draw
            moves = 0
            while not game.is_game_over() and moves < 42:
                move = game.get_ai_move()
                game.make_move(move)
                moves += 1
            
            # Game should complete
            assert game.is_game_over()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])