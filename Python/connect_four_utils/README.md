# Connect Four Utils

A complete Connect Four game implementation with AI opponent using minimax algorithm with alpha-beta pruning.

## Features

- **Game Board**: Full 6x7 board management with piece dropping mechanics
- **Win Detection**: Horizontal, vertical, and diagonal win checking
- **AI Opponent**: Minimax algorithm with alpha-beta pruning
- **Difficulty Levels**: Easy, Medium, Hard, and Expert
- **Multiple Game Modes**: Human vs AI, Human vs Human, AI vs AI, AI vs Random
- **Undo Function**: Move history with undo capability
- **Serialization**: Save and restore game state (JSON support)
- **Customizable Display**: Custom symbols for board display

## Installation

No external dependencies required. Uses only Python standard library.

```python
from connect_four_utils import ConnectFourGame, create_game, Board, AIPlayer, Difficulty
```

## Quick Start

### Basic Game

```python
from connect_four_utils import ConnectFourGame

# Create game (default: Human vs AI)
game = ConnectFourGame()

# Make a move (column 0-6)
success, message = game.make_move(3)
print(game.display())

# Check game status
if game.is_game_over():
    print(f"Winner: {game.winner}")
```

### Different Game Modes

```python
from connect_four_utils import create_game

# Human vs AI (medium difficulty)
game = create_game("human_vs_ai", difficulty="medium")

# AI vs AI
game = create_game("ai_vs_ai", difficulty="hard")

# Human vs Human
game = create_game("human_vs_human")

# AI vs Random bot
game = create_game("ai_vs_random", difficulty="expert")
```

### Using AI Player

```python
from connect_four_utils import AIPlayer, Difficulty, Board

ai = AIPlayer(1, Difficulty.HARD)
board = Board()

# Get AI's move
best_column = ai.get_move(board)
print(f"AI suggests column {best_column}")
```

### Board Operations

```python
from connect_four_utils import Board, PLAYER_ONE, PLAYER_TWO

board = Board()

# Drop pieces
board.drop_piece(3, PLAYER_ONE)
board.drop_piece(2, PLAYER_TWO)

# Check available columns
available = board.get_available_columns()

# Check for win
if board.check_win(PLAYER_ONE):
    positions = board.get_winning_positions(PLAYER_ONE)
    print(f"Winning positions: {positions}")
```

### Undo Moves

```python
game = ConnectFourGame()
game.make_move(3)
game.make_move(2)

# Undo last move
game.undo_last_move()
print(f"Moves remaining: {game.move_count}")
```

### Save/Load Game State

```python
# Save to JSON
json_state = game.to_json()

# Load from JSON
restored_game = ConnectFourGame.from_json(json_state)
```

## API Reference

### Classes

#### `ConnectFourGame`
Main game manager class.

| Method | Description |
|--------|-------------|
| `make_move(column)` | Make a move in specified column |
| `get_ai_move()` | Get AI's recommended move |
| `undo_last_move()` | Undo the last move |
| `reset()` | Reset game to initial state |
| `is_game_over()` | Check if game has ended |
| `display()` | Get string representation of board |
| `to_json()` | Serialize game to JSON |
| `from_json(str)` | Deserialize game from JSON |

#### `Board`
Board state management.

| Method | Description |
|--------|-------------|
| `drop_piece(col, player)` | Drop piece in column |
| `check_win(player)` | Check if player has won |
| `get_winning_positions(player)` | Get winning piece positions |
| `is_column_full(col)` | Check if column is full |
| `get_available_columns()` | Get list of playable columns |
| `serialize()` | Serialize board state |
| `deserialize(str)` | Restore board from serialized state |

#### `AIPlayer`
AI opponent with minimax algorithm.

| Method | Description |
|--------|-------------|
| `get_move(board)` | Get best move for current board |
| `set_difficulty(diff)` | Change AI difficulty |

### Difficulty Levels

| Level | Description | Search Depth |
|-------|-------------|--------------|
| `EASY` | Random moves | 1 |
| `MEDIUM` | Basic strategy | 3 |
| `HARD` | Good strategy | 5 |
| `EXPERT` | Advanced strategy | 7 |

## Examples

Run the examples module to see all features:

```python
from connect_four_utils.examples import run_all_examples
run_all_examples()
```

Or from command line:

```bash
python -m connect_four_utils.examples
```

## Testing

Run tests with pytest:

```bash
python -m pytest connect_four_utils/test_connect_four.py -v
```

## Constants

- `ROWS = 6` - Number of rows
- `COLS = 7` - Number of columns
- `EMPTY = 0` - Empty cell value
- `PLAYER_ONE = 1` - Player 1 identifier
- `PLAYER_TWO = 2` - Player 2 identifier
- `WINNING_LENGTH = 4` - Pieces needed to win

## License

MIT License - Part of AllToolkit project.