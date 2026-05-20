"""
Connect Four Game Examples
=========================

This module demonstrates how to use the Connect Four utilities.

Run with: python -m connect_four_utils.examples
"""

from .game import ConnectFourGame, create_game
from .board import Board
from .player import HumanPlayer, RandomPlayer
from .ai import AIPlayer, create_ai_player
from .constants import PLAYER_ONE, PLAYER_TWO, Difficulty


def example_basic_game():
    """Basic game example - manual moves."""
    print("=" * 60)
    print("Example 1: Basic Game (Manual Moves)")
    print("=" * 60)
    
    game = ConnectFourGame()
    print(game.display())
    
    # Make some moves
    moves = [3, 3, 2, 4, 2, 5, 1]  # Player 1 wins with column 1-4
    
    for col in moves:
        success, msg = game.make_move(col)
        print(f"\nMove {game.move_count}: Column {col}")
        print(game.display())
        
        if game.is_game_over():
            print(f"\n🎮 Game Over: {msg}")
            if game.winning_positions:
                print(f"Winning positions: {game.winning_positions}")
            break
    
    print()


def example_ai_game():
    """Example of AI vs AI game."""
    print("=" * 60)
    print("Example 2: AI vs AI Game")
    print("=" * 60)
    
    game = create_game("ai_vs_ai", "medium", "Alpha", "Beta")
    print(f"Player 1: {game.player1.name}")
    print(f"Player 2: {game.player2.name}")
    print()
    
    moves = 0
    while not game.is_game_over() and moves < 42:
        move = game.get_ai_move()
        success, msg = game.make_move(move)
        moves += 1
        
        if moves <= 6 or game.is_game_over():  # Show first few and final
            print(f"Move {moves}: {game.player1.name if moves % 2 == 1 else game.player2.name} plays column {move}")
            if game.is_game_over():
                print(game.display())
    
    if game.winner:
        winner_name = game.player1.name if game.winner == PLAYER_ONE else game.player2.name
        print(f"\n🏆 Winner: {winner_name}!")
    else:
        print("\n🤝 Draw!")
    print()


def example_human_vs_ai():
    """Example of human vs AI game (simulated human)."""
    print("=" * 60)
    print("Example 3: Human vs AI Game (Simulated)")
    print("=" * 60)
    
    game = create_game("human_vs_ai", "hard", "You", "Computer")
    print(f"Player 1 (You): {game.player1.name}")
    print(f"Player 2 (AI): {game.player2.name}")
    print()
    
    # Simulate human moves (would normally come from user input)
    human_moves = [3, 2, 4, 1, 5]  # Human's moves
    
    move_count = 0
    while not game.is_game_over() and move_count < 42:
        if isinstance(game.current_player, HumanPlayer):
            # Human's turn - use simulated moves
            if human_moves:
                col = human_moves.pop(0)
                # Check if column is valid
                if col not in game.get_available_columns():
                    col = game.get_available_columns()[0]  # Fallback
            else:
                col = game.get_available_columns()[0]
        else:
            # AI's turn
            col = game.get_ai_move()
        
        success, msg = game.make_move(col)
        move_count += 1
        print(f"Move {move_count}: {game.player1.name if move_count % 2 == 1 else game.player2.name} plays column {col}")
    
    print()
    print(game.display())
    
    if game.winner:
        winner_name = game.player1.name if game.winner == PLAYER_ONE else game.player2.name
        print(f"\n🏆 Winner: {winner_name}!")
    else:
        print("\n🤝 Draw!")
    print()


def example_difficulty_levels():
    """Example showing different AI difficulty levels."""
    print("=" * 60)
    print("Example 4: AI Difficulty Levels")
    print("=" * 60)
    
    for diff in ["easy", "medium", "hard", "expert"]:
        game = create_game("ai_vs_ai", diff)
        
        moves = 0
        while not game.is_game_over() and moves < 42:
            move = game.get_ai_move()
            game.make_move(move)
            moves += 1
        
        result = "Draw" if not game.winner else f"Player {game.winner} wins"
        print(f"{diff.upper():8} difficulty: {moves:2} moves, {result}")
    print()


def example_board_operations():
    """Example of board operations."""
    print("=" * 60)
    print("Example 5: Board Operations")
    print("=" * 60)
    
    board = Board()
    print("Empty board:")
    print(board.to_string())
    print()
    
    # Drop pieces
    board.drop_piece(3, PLAYER_ONE)
    board.drop_piece(3, PLAYER_TWO)
    board.drop_piece(2, PLAYER_ONE)
    
    print("After some moves:")
    print(board.to_string())
    print()
    
    # Board info
    print(f"Available columns: {board.get_available_columns()}")
    print(f"Column 3 height: {board.get_column_height(3)}")
    print(f"Player 1 pieces: {board.count_pieces(PLAYER_ONE)}")
    print(f"Player 2 pieces: {board.count_pieces(PLAYER_TWO)}")
    print()
    
    # Serialization
    serialized = board.serialize()
    print(f"Serialized: {serialized}")
    
    restored = Board.deserialize(serialized)
    print("Restored board:")
    print(restored.to_string())
    print()


def example_custom_symbols():
    """Example with custom display symbols."""
    print("=" * 60)
    print("Example 6: Custom Display Symbols")
    print("=" * 60)
    
    board = Board()
    board.drop_piece(3, PLAYER_ONE)
    board.drop_piece(2, PLAYER_TWO)
    board.drop_piece(4, PLAYER_ONE)
    
    print("Default symbols:")
    print(board.to_string())
    print()
    
    print("Custom symbols (empty='.', X/O):")
    print(board.to_string(symbols=('.', 'X', 'O')))
    print()
    
    print("Custom symbols (emoji):")
    print(board.to_string(symbols=('⬜', '🔴', '🟡')))
    print()


def example_game_state():
    """Example of game state management."""
    print("=" * 60)
    print("Example 7: Game State Management")
    print("=" * 60)
    
    game = create_game("ai_vs_ai", "medium")
    
    # Play a few moves
    for _ in range(6):
        move = game.get_ai_move()
        game.make_move(move)
    
    print("Current game state:")
    print(game.display())
    print(f"Move count: {game.move_count}")
    print(f"Current player: {game.current_player.name}")
    print()
    
    # Save state
    state = game.to_json()
    print("Saved state (JSON):")
    print(state)
    print()
    
    # Make more moves
    for _ in range(3):
        move = game.get_ai_move()
        game.make_move(move)
    
    print("After more moves:")
    print(game.display())
    print()
    
    # Restore state
    restored = ConnectFourGame.from_json(state)
    print("Restored to saved state:")
    print(restored.display())
    print()


def example_undo_moves():
    """Example of undo functionality."""
    print("=" * 60)
    print("Example 8: Undo Moves")
    print("=" * 60)
    
    game = ConnectFourGame()
    
    # Make some moves
    game.make_move(3)
    game.make_move(2)
    game.make_move(4)
    
    print("After 3 moves:")
    print(game.display())
    print(f"Move count: {game.move_count}")
    print()
    
    # Undo last move
    game.undo_last_move()
    print("After undo:")
    print(game.display())
    print(f"Move count: {game.move_count}")
    print()
    
    # Undo again
    game.undo_last_move()
    print("After second undo:")
    print(game.display())
    print(f"Move count: {game.move_count}")
    print()


def example_random_vs_ai():
    """Example of random player vs AI."""
    print("=" * 60)
    print("Example 9: Random Player vs AI")
    print("=" * 60)
    
    game = create_game("ai_vs_random", "hard", "Smart AI", "Lucky Bot")
    print(f"Player 1: {game.player1.name} (AI)")
    print(f"Player 2: {game.player2.name} (Random)")
    print()
    
    moves = 0
    while not game.is_game_over() and moves < 42:
        move = game.get_ai_move()
        game.make_move(move)
        moves += 1
    
    print(game.display())
    
    if game.winner:
        winner_name = game.player1.name if game.winner == PLAYER_ONE else game.player2.name
        print(f"\n🏆 Winner: {winner_name}!")
    else:
        print("\n🤝 Draw!")
    
    print(f"Total moves: {moves}")
    print()


def example_win_patterns():
    """Example showing different win patterns."""
    print("=" * 60)
    print("Example 10: Win Pattern Detection")
    print("=" * 60)
    
    # Horizontal win
    print("Horizontal Win:")
    board = Board()
    for col in range(4):
        board.drop_piece(col, PLAYER_ONE)
        if col < 3:
            board.drop_piece(col + 4, PLAYER_TWO)
    print(board.to_string())
    print(f"Player 1 wins: {board.check_win(PLAYER_ONE)}")
    positions = board.get_winning_positions(PLAYER_ONE)
    print(f"Winning positions: {positions}")
    print()
    
    # Vertical win
    print("Vertical Win:")
    board = Board()
    for _ in range(4):
        board.drop_piece(0, PLAYER_ONE)
        board.drop_piece(1, PLAYER_TWO)
    print(board.to_string())
    print(f"Player 1 wins: {board.check_win(PLAYER_ONE)}")
    positions = board.get_winning_positions(PLAYER_ONE)
    print(f"Winning positions: {positions}")
    print()
    
    # Diagonal win
    print("Diagonal Win:")
    board = Board()
    # Create diagonal
    board.drop_piece(0, PLAYER_ONE)
    board.drop_piece(1, PLAYER_TWO)
    board.drop_piece(1, PLAYER_ONE)
    board.drop_piece(2, PLAYER_TWO)
    board.drop_piece(2, PLAYER_ONE)
    board.drop_piece(2, PLAYER_TWO)
    board.drop_piece(2, PLAYER_ONE)
    board.drop_piece(3, PLAYER_TWO)
    board.drop_piece(3, PLAYER_ONE)
    board.drop_piece(3, PLAYER_TWO)
    board.drop_piece(3, PLAYER_ONE)
    print(board.to_string())
    print(f"Player 1 wins: {board.check_win(PLAYER_ONE)}")
    positions = board.get_winning_positions(PLAYER_ONE)
    print(f"Winning positions: {positions}")
    print()


def run_all_examples():
    """Run all examples."""
    print("\n" + "🎮" * 20)
    print("Connect Four Utilities - Examples")
    print("🎮" * 20 + "\n")
    
    example_basic_game()
    example_ai_game()
    example_human_vs_ai()
    example_difficulty_levels()
    example_board_operations()
    example_custom_symbols()
    example_game_state()
    example_undo_moves()
    example_random_vs_ai()
    example_win_patterns()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()