# Domino Utils 🎲

Complete domino game utilities toolkit for Python. Zero external dependencies.

## Features

### 🧱 Domino Tile (`Domino`)
- Tile representation with automatic normalization
- Double detection and pip counting
- Connection checking and value lookup
- Flip, contains, other_end operations
- Hashable for set membership

### 📦 Domino Set (`DominoSet`)
- Standard double-six set (28 tiles)
- Custom sets (double-nine, double-twelve, etc.)
- Shuffle, sample, and deal functions
- Get tiles by value, total, or doubles
- Statistics and statistics generation

### 🔗 Domino Chain (`DominoChain`)
- Build connected chains of dominoes
- Automatic orientation handling
- Playable tile detection
- Chain manipulation and copying

### 🤚 Domino Hand (`DominoHand`)
- Player hand management
- Pip counting and doubles detection
- Best play selection (multiple strategies)
- Playability checking

### 🧩 Domino Solver (`DominoSolver`)
- Find longest possible chain
- Solve domino solitaire puzzles
- Check if single chain is possible
- Find chains with specific ends
- Count possible arrangements

### 🎮 Domino Game (`DominoGame`)
- Draw initial hands for games
- Determine first player
- Calculate draw game scores
- Check round completion

## Quick Start

```python
from domino_utils import Domino, DominoSet, DominoChain, DominoSolver

# Create dominoes
d1 = Domino(3, 5)   # [3|5]
d2 = Domino(5, 2)   # [5|2]
d3 = Domino(2, 4)   # [2|4]

# Check properties
print(d1.total)      # 8 (pip count)
print(d1.is_double)  # False
print(d1.can_connect(5))  # True

# Create a set
set = DominoSet(6)   # Double-six (28 tiles)
print(set.count)     # 28

# Deal hands
hands, boneyard = set.deal(2, 7)  # 2 players, 7 tiles each

# Build a chain
chain = DominoChain()
chain.add(d1)
chain.add(d2)
chain.add(d3)
print(chain)         # [3|5]-[5|2]-[2|4]

# Solve solitaire
tiles = [Domino(3, 5), Domino(5, 2), Domino(2, 4)]
result = DominoSolver.solve_domino_solitaire(tiles)
print(result)        # Complete chain
```

## Domino Set Variants

```python
# Double-six (28 tiles)
set6 = DominoSet(6)

# Double-nine (55 tiles)
set9 = DominoSet(9)

# Double-twelve (91 tiles)
set12 = DominoSet(12)

# Custom set
custom = DominoSet(15)  # 136 tiles
```

## Chain Building

```python
from domino_utils import DominoChain

chain = DominoChain(Domino(3, 5))

# Add to right end
chain.add(Domino(5, 2))  # [3|5]-[5|2]

# Add to left end
chain.add(Domino(1, 3), 'left')  # [1|3]-[3|5]-[5|2]

# Check ends
print(chain.left_end)   # 1
print(chain.right_end)  # 2
print(chain.length)     # 3
```

## Hand Management

```python
from domino_utils import DominoHand

hand = DominoHand([Domino(3, 5), Domino(5, 6), Domino(2, 4)])

# Find playable tiles
chain = DominoChain(Domino(2, 3))
playable = hand.playable_tiles(chain)

# Best play strategies
best = hand.best_play(chain, 'highest')  # Highest pip count
best = hand.best_play(chain, 'double')   # Doubles first
best = hand.best_play(chain, 'strategic')  # Preserve options

# Statistics
stats = hand.statistics
print(stats['total_pips'])      # Sum of all pips
print(stats['doubles_count'])   # Number of doubles
```

## Solitaire Solver

```python
from domino_utils import DominoSolver, Domino

tiles = [
    Domino(3, 5), Domino(5, 2), Domino(2, 4),
    Domino(4, 6), Domino(6, 1), Domino(1, 3)
]

# Check if single chain possible
can_chain = DominoSolver.can_form_single_chain(tiles)  # True

# Find complete chain
chain = DominoSolver.solve_domino_solitaire(tiles)
print(chain)  # Full chain using all tiles

# Find longest chain (if not complete)
longest = DominoSolver.find_longest_chain(tiles)

# Find chain with specific ends
specific = DominoSolver.find_chain_with_ends(tiles, start_value=3, end_value=1)
```

## Game Utilities

```python
from domino_utils import DominoGame

# Setup 2-player game
game = DominoGame.draw_dominoes('standard', num_players=2, max_value=6)
hands = game['hands']
boneyard = game['boneyard']

# Determine first player (highest double rule)
first_player = DominoGame.determine_first_player(hands, 'highest_double')

# Check if round is over
is_over = DominoGame.is_round_over(hands, chain)

# Calculate score for drawn game
winner, score = DominoGame.calculate_score_draw_game(hands)
```

## Convenience Functions

```python
from domino_utils import (
    domino, domino_set, find_chain, 
    longest_chain, can_chain_all, deal_hands
)

# Quick domino creation
d = domino(3, 5)

# Quick set creation
s = domino_set(6)

# Quick chain finding
chain = find_chain([(3, 5), (5, 2), (2, 4)])

# Quick longest chain
longest = longest_chain([(3, 5), (1, 2)])

# Check if all can chain
can = can_chain_all([(3, 5), (5, 2), (2, 4)])  # True

# Quick dealing
hands, boneyard = deal_hands(2)
```

## Test Coverage

- **51 unit tests** covering all major functionality
- Domino creation, normalization, equality
- DominoSet variants and statistics
- DominoChain building and orientation
- DominoHand management and strategies
- DominoSolver algorithms
- DominoGame utilities
- Edge cases and error handling

Run tests:
```bash
python domino_utils/domino_utils_test.py
```

## Implementation Details

### Domino Representation
- Immutable `Domino` class (frozen dataclass)
- Automatic normalization: smaller value on left
- Hashable for set/dict membership

### Chain Algorithm
- Backtracking search for longest chain
- Eulerian path criteria for single-chain feasibility
- End-specific chain finding

### Best Play Strategies
- `highest`: Play highest pip count (score points)
- `lowest`: Play lowest pip count (preserve heavy tiles)
- `double`: Play doubles first (limit options for opponents)
- `strategic`: Choose tiles that preserve connectivity

## Use Cases

- Domino game implementations
- Solitaire puzzle solving
- Domino AI/strategy development
- Domino probability analysis
- Educational games

## License

MIT License - Part of AllToolkit collection.