# Dart Game Utilities 🎯

A comprehensive dart game scoring and analysis toolkit for Python.

## Features

- **Standard Dart Games**: 501, 301, 701, Cricket, Around the Clock
- **Score Calculation**: Single, double, triple, and bull scoring zones
- **Checkout Suggestions**: Complete checkout tables for scores 2-170
- **Game Statistics**: Player averages, high scores, checkout percentages
- **Game Management**: Full game state tracking and serialization
- **No Dependencies**: Pure Python implementation using only standard library

## Installation

```python
# Import directly
from dart_game_utils import DartThrow, X01Game, CricketGame, get_checkout
```

## Quick Start

### 501 Game

```python
from dart_game_utils import X01Game, DartThrow

# Create a 501 game
game = X01Game(starting_score=501)
game.add_player("Phil")
game.add_player("Michael")

# Throw darts
game.throw_dart(DartThrow.triple(20))  # T20 = 60 points
game.throw_dart(DartThrow.triple(20))  # T20 = 60 points
game.throw_dart(DartThrow.triple(20))  # T20 = 60 points = 180!

# End turn
turn_info = game.next_turn()
print(f"Turn score: {turn_info['turn_score']}")  # 180

# Get checkout suggestions
from dart_game_utils import get_checkout
checkout = get_checkout(100)  # ['T20', 'D20']
print(f"Checkout for 100: {' + '.join(checkout)}")
```

### Cricket Game

```python
from dart_game_utils import CricketGame, DartThrow

game = CricketGame()
game.add_player("Player1")
game.add_player("Player2")

# Close numbers
game.throw_dart(DartThrow.triple(20))  # Close 20
game.throw_dart(DartThrow.triple(19))  # Close 19

# Score points (if opponent hasn't closed)
game.throw_dart(DartThrow.triple(20))  # +60 points
```

### Around the Clock

```python
from dart_game_utils import AroundTheClockGame, DartThrow

game = AroundTheClockGame()
game.add_player("Player1")

# Hit each number in sequence
game.throw_dart(DartThrow.single(1))  # Target now 2
game.throw_dart(DartThrow.single(2))  # Target now 3
# ... continue until 20
```

## Dart Throws

Create throws with factory methods:

```python
# Scoring zones
dart = DartThrow.single(20)     # Single 20 = 20 points
dart = DartThrow.double(20)     # Double 20 = 40 points
dart = DartThrow.triple(20)     # Triple 20 = 60 points
dart = DartThrow.bull(False)    # Single bull = 25 points
dart = DartThrow.bull(True)     # Double bull = 50 points
dart = DartThrow.miss()         # Miss = 0 points

# Parse notation
from dart_game_utils import parse_dart_notation
dart = parse_dart_notation("T20")   # Triple 20
dart = parse_dart_notation("D20")   # Double 20
dart = parse_dart_notation("DBULL") # Double bull
dart = parse_dart_notation("BULL")  # Single bull
dart = parse_dart_notation("MISS")  # Miss
```

## Checkout Suggestions

```python
from dart_game_utils import get_checkout, suggest_next_dart

# Get checkout for any score 2-170
checkout = get_checkout(170)  # ['T20', 'T20', 'DBULL']
checkout = get_checkout(100)  # ['T20', 'D20']
checkout = get_checkout(50)   # ['DBULL']
checkout = get_checkout(40)   # ['D20']

# With limited darts
checkout = get_checkout(100, darts_available=2)  # None (needs 3)
checkout = get_checkout(40, darts_available=1)   # ['D20']

# Get suggestion for next dart
suggestion = suggest_next_dart(100)
print(suggestion['suggestion'])  # 'T20'
print(suggestion['full_checkout'])  # ['T20', 'D20']
```

## Statistics

```python
from dart_game_utils import get_statistics, analyze_turn

# Get player statistics
stats = get_statistics(player)
print(f"Average: {stats['average_per_3_darts']}")
print(f"180s: {stats['one_hundred_eighties']}")
print(f"Checkout %: {stats['checkout_percentage']}")

# Analyze a turn
analysis = analyze_turn(turn)
print(f"Score: {analysis['total_score']}")
print(f"Triples: {analysis['triples']}")
print(f"Is 180: {analysis['is_180']}")
```

## Game Types

### X01 Games (501, 301, 701)

- Start at target score (501, 301, etc.)
- Count down to exactly 0
- Double-out required (finish with double or double bull)
- Optional double-in (must start with double)
- Bust if score goes below 0 or leaves 1 with double-out

### Cricket

- Close numbers: 20, 19, 18, 17, 16, 15, Bull
- Hit each number 3 times to close
- Score points on closed numbers if opponent hasn't closed
- Win: Close all numbers AND have highest score

### Around the Clock

- Hit numbers 1 through 20 in sequence
- Optional: Doubles skip 2 numbers, triples skip 3
- Optional: Double-out required on 20

## Dartboard Information

```python
from dart_game_utils import get_dartboard_neighbors, get_dartboard_position, DARTBOARD_NUMBERS

# Get neighbors of a number
left, right = get_dartboard_neighbors(20)  # (5, 1)

# Get position info
pos = get_dartboard_position(20)
print(f"Angle: {pos['angle_degrees']}°")
print(f"Left neighbor: {pos['left_neighbor']}")

# Dartboard numbers (clockwise from top)
print(DARTBOARD_NUMBERS)  # [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, ...]
```

## Factory Function

```python
from dart_game_utils import create_game

# Create any game type
game = create_game('501')
game = create_game('301')
game = create_game('cricket')
game = create_game('around_clock')
```

## Complete Example: Simulated 501 Game

```python
from dart_game_utils import X01Game, DartThrow, get_checkout, parse_dart_notation

# Create game
game = X01Game(starting_score=501, double_out=True)
game.add_player("Phil")
game.add_player("Michael")

# Play until finished
while not game.is_finished:
    remaining = game.current_player.score
    
    # Get checkout if in range
    checkout = get_checkout(remaining)
    
    if checkout:
        for dart_str in checkout:
            dart = parse_dart_notation(dart_str)
            result = game.throw_dart(dart)
            if result.get('game_over'):
                print(f"Winner: {game.winner}!")
                break
    else:
        # Score high
        game.throw_dart(DartThrow.triple(20))
        game.throw_dart(DartThrow.triple(20))
        game.throw_dart(DartThrow.triple(20))
    
    game.next_turn()

# Print final statistics
from dart_game_utils import get_statistics
for player in game.players:
    stats = get_statistics(player)
    print(f"{player.name}: Avg {stats['average_per_3_darts']}, 180s: {stats['one_hundred_eighties']}")
```

## API Reference

### Classes

- `DartThrow` - Single dart throw with zone and score
- `Turn` - A player's turn (up to 3 darts)
- `Player` - Player with statistics tracking
- `X01Game` - 501/301/701 game
- `CricketGame` - Cricket game
- `CricketMark` - Cricket number mark tracking
- `AroundTheClockGame` - Around the Clock game

### Functions

- `get_checkout(score, darts_available)` - Get checkout suggestion
- `get_all_checkouts(score)` - Get all possible checkouts
- `suggest_next_dart(score)` - Suggest optimal next dart
- `get_statistics(player)` - Get comprehensive player stats
- `analyze_turn(turn)` - Analyze a turn's composition
- `create_game(game_type)` - Factory for game creation
- `parse_dart_notation(notation)` - Parse T20, D20, BULL, etc.
- `format_dart_throw(dart)` - Format dart as notation
- `validate_dart_throw(number, zone)` - Validate throw parameters
- `get_dartboard_neighbors(number)` - Get adjacent numbers
- `get_dartboard_position(number)` - Get position info
- `is_checkout_possible(score, darts)` - Check if checkout possible
- `calculate_average_score(throws)` - Calculate average per dart
- `calculate_first_nine_average(throws)` - First 9 darts average

### Constants

- `DARTBOARD_NUMBERS` - Board number arrangement
- `CHECKOUTS` - Complete checkout table (2-170)
- `ALL_DART_VALUES` - All possible dart scores
- `VALID_SCORES` - Valid dart numbers (1-20, 25)

## Testing

```bash
python dart_game_utils_test.py
```

Runs 40 test functions with 117 assertions covering:
- Dart throw creation and scoring
- Turn and player statistics
- 501/301 game mechanics
- Bust conditions
- Checkout calculations
- Cricket game logic
- Around the Clock game
- Dart notation parsing
- Serialization

## License

MIT License - Part of AllToolkit project.