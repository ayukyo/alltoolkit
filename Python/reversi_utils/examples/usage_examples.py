#!/usr/bin/env python3
"""
Reversi (Othello) Game Utilities - Usage Examples

This example demonstrates:
1. Basic game setup and gameplay
2. AI opponent usage
3. Game analysis
4. Serialization for saving/loading games
"""

import sys
import os

# Add the Python directory (parent of reversi_utils) to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from reversi_utils.mod import (
    ReversiBoard, BLACK, WHITE,
    get_best_move, get_greedy_move, get_opening_moves,
    analyze_game, evaluate_position
)


def example_basic_gameplay():
    """Example 1: Basic game setup and manual moves."""
    print("=" * 60)
    print("Example 1: Basic Gameplay")
    print("=" * 60)
    
    # Create a standard 8x8 board
    board = ReversiBoard()
    print("\nInitial board:")
    print(board)
    
    # Get valid moves for current player (Black)
    valid_moves = board.get_valid_moves()
    print(f"\nValid moves for Black: {valid_moves}")
    
    # Make a move
    move = valid_moves[0]
    print(f"\nBlack plays: {chr(ord('a') + move[1])}{move[0] + 1}")
    board.make_move(move[0], move[1])
    print(board)
    
    # Now it's White's turn
    print(f"\nCurrent player: {'Black' if board.current_player == BLACK else 'White'}")
    
    # Get valid moves for White
    white_moves = board.get_valid_moves()
    print(f"Valid moves for White: {white_moves}")
    
    # White makes a move
    if white_moves:
        move = white_moves[0]
        print(f"\nWhite plays: {chr(ord('a') + move[1])}{move[0] + 1}")
        board.make_move(move[0], move[1])
        print(board)
    
    # Check score
    black, white = board.get_score()
    print(f"\nScore - Black: {black}, White: {white}")


def example_ai_opponent():
    """Example 2: Playing against AI."""
    print("\n" + "=" * 60)
    print("Example 2: AI Opponent")
    print("=" * 60)
    
    board = ReversiBoard()
    print("\nYou are Black, AI (White) uses minimax algorithm")
    print(board)
    
    # Simulate a few moves
    move_count = 0
    while not board.is_game_over() and move_count < 10:
        if board.current_player == BLACK:
            # Player (Black) uses greedy AI for demonstration
            move = get_greedy_move(board, BLACK)
            if move:
                print(f"\nBlack plays: {chr(ord('a') + move[1])}{move[0] + 1}")
                board.make_move(move[0], move[1])
        else:
            # AI (White) uses minimax
            move = get_best_move(board, WHITE, depth=3)
            if move:
                print(f"\nWhite (AI) plays: {chr(ord('a') + move[1])}{move[0] + 1}")
                board.make_move(move[0], move[1])
        
        move_count += 1
        if move_count % 2 == 0:
            print(board)
    
    print("\nGame state after 10 moves:")
    print(board)
    
    black, white = board.get_score()
    print(f"\nScore - Black: {black}, White: {white}")


def example_game_analysis():
    """Example 3: Analyzing game positions."""
    print("\n" + "=" * 60)
    print("Example 3: Game Analysis")
    print("=" * 60)
    
    board = ReversiBoard()
    
    # Make some moves
    for _ in range(4):
        move = get_greedy_move(board, board.current_player)
        if move:
            board.make_move(move[0], move[1])
    
    print("\nCurrent board:")
    print(board)
    
    # Analyze the position
    analysis = analyze_game(board)
    print("\nPosition Analysis:")
    print(f"  Black pieces: {analysis['black_pieces']}")
    print(f"  White pieces: {analysis['white_pieces']}")
    print(f"  Empty squares: {analysis['empty_squares']}")
    print(f"  Black mobility (valid moves): {analysis['black_mobility']}")
    print(f"  White mobility (valid moves): {analysis['white_mobility']}")
    print(f"  Current player: {analysis['current_player']}")
    print(f"  Position score (for Black): {analysis['position_score']}")
    print(f"  Black territory: {analysis['black_territory']}")
    print(f"  White territory: {analysis['white_territory']}")
    
    # Evaluate position
    score = evaluate_position(board, BLACK)
    print(f"\nEvaluation for Black: {score} ({'advantage' if score > 0 else 'disadvantage' if score < 0 else 'equal'})")


def example_save_load_game():
    """Example 4: Saving and loading games."""
    print("\n" + "=" * 60)
    print("Example 4: Save and Load Games")
    print("=" * 60)
    
    # Create a game and make some moves
    board = ReversiBoard()
    for _ in range(3):
        move = get_greedy_move(board, board.current_player)
        if move:
            board.make_move(move[0], move[1])
    
    print("\nOriginal game:")
    print(board)
    
    # Save game to dict
    saved = board.serialize()
    print("\nSerialized game data:")
    print(f"  Size: {saved['size']}")
    print(f"  Current player: {'Black' if saved['current_player'] == BLACK else 'White'}")
    
    # Save to FEN notation
    fen = board.to_fen()
    print(f"\nFEN notation: {fen}")
    
    # Load from dict
    loaded = ReversiBoard.deserialize(saved)
    print("\nLoaded from dict:")
    print(loaded)
    
    # Load from FEN
    loaded_fen = ReversiBoard.from_fen(fen)
    print("Loaded from FEN:")
    print(loaded_fen)
    
    # Verify they match
    for row in range(loaded.size):
        for col in range(loaded.size):
            if loaded.get(row, col) != loaded_fen.get(row, col):
                print(f"  Mismatch at ({row}, {col})!")
    print("\n✅ Both loading methods produce identical boards")


def example_opening_strategy():
    """Example 5: Opening strategy and tips."""
    print("\n" + "=" * 60)
    print("Example 5: Opening Strategy")
    print("=" * 60)
    
    print("\nReversi Opening Tips:")
    for tip_type, tip in get_opening_moves():
        print(f"  • {tip_type}: {tip}")
    
    board = ReversiBoard()
    print("\n" + str(board))
    
    print("\nOpening move analysis:")
    valid_moves = board.get_valid_moves()
    print(f"Valid opening moves: {[(chr(ord('a') + c), r + 1) for r, c in valid_moves]}")
    
    # Evaluate each opening
    print("\nMove evaluations:")
    for move in valid_moves:
        test_board = board.copy()
        test_board.make_move(move[0], move[1])
        score = evaluate_position(test_board, BLACK)
        coord = f"{chr(ord('a') + move[1])}{move[0] + 1}"
        print(f"  {coord}: score = {score}")


def example_play_complete_game():
    """Example 6: Play a complete game."""
    print("\n" + "=" * 60)
    print("Example 6: Complete Game (AI vs AI)")
    print("=" * 60)
    
    board = ReversiBoard()
    moves = []
    
    print("\nGame progress:")
    move_num = 0
    while not board.is_game_over():
        # Use minimax for deeper search
        move = get_best_move(board, board.current_player, depth=3)
        if move:
            player = "Black" if board.current_player == BLACK else "White"
            coord = f"{chr(ord('a') + move[1])}{move[0] + 1}"
            moves.append(f"{player}: {coord}")
            
            if move_num % 10 == 0:
                black, white = board.get_score()
                print(f"  Move {move_num}: Black {black} - White {white}")
            
            board.make_move(move[0], move[1])
            move_num += 1
        else:
            # No valid move, skip turn
            if not board.skip_turn():
                break
    
    print("\nFinal board:")
    print(board)
    
    black, white = board.get_score()
    winner = board.get_winner()
    
    print(f"\nFinal Score - Black: {black}, White: {white}")
    if winner == BLACK:
        print("🏆 Black wins!")
    elif winner == WHITE:
        print("🏆 White wins!")
    else:
        print("🤝 It's a tie!")
    
    print(f"\nTotal moves: {len(moves)}")
    print("Move history (first 10):", moves[:10])


def example_show_valid_moves():
    """Example 7: Display board with valid moves highlighted."""
    print("\n" + "=" * 60)
    print("Example 7: Show Valid Moves")
    print("=" * 60)
    
    board = ReversiBoard()
    
    print("\nBoard with valid moves marked with '*':")
    print(board.to_string(show_valid_moves=True))
    
    print("\nLegend:")
    print("  ● = Black piece")
    print("  ○ = White piece")
    print("  · = Empty square")
    print("  * = Valid move for current player")


def main():
    """Run all examples."""
    example_basic_gameplay()
    example_ai_opponent()
    example_game_analysis()
    example_save_load_game()
    example_opening_strategy()
    example_play_complete_game()
    example_show_valid_moves()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()