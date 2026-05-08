"""
Domino Utils - Complete domino game utilities toolkit.

Features:
- Domino tile representation and manipulation
- Standard double-six set and custom domino sets
- Chain building algorithms (longest chain, all chains)
- Solitaire puzzle solving
- Game logic for matching and scoring
- Domino hand analysis and statistics
- Zero external dependencies

Author: AllToolkit
Date: 2026-05-08
"""

from typing import List, Tuple, Optional, Set, Dict, Generator
from dataclasses import dataclass
from collections import defaultdict
from copy import deepcopy
import random


class Domino:
    """
    Represents a single domino tile.
    
    A domino has two ends (values), typically from 0 to 6 in standard sets.
    Dominoes are unordered for equality/hash: Domino(3, 5) == Domino(5, 3).
    But orientation is preserved for chain building.
    """
    
    __slots__ = ('_a', '_b')
    
    def __init__(self, a: int, b: int):
        """Create a domino with values a and b (order matters for display)."""
        self._a = a
        self._b = b
    
    @property
    def left(self) -> int:
        """Return the left end value."""
        return self._a
    
    @property
    def right(self) -> int:
        """Return the right end value."""
        return self._b
    
    def __str__(self) -> str:
        """Return string representation like [3|5] or [6|6]"""
        return "[{}|{}]".format(self._a, self._b)
    
    def __repr__(self) -> str:
        return "Domino({}, {})".format(self._a, self._b)
    
    def __hash__(self) -> int:
        # Hash based on unordered pair
        if self._a <= self._b:
            return hash((self._a, self._b))
        return hash((self._b, self._a))
    
    def __eq__(self, other) -> bool:
        # Equality based on unordered pair
        if not isinstance(other, Domino):
            return NotImplemented
        return (self._a, self._b) == (other._a, other._b) or \
               (self._a, self._b) == (other._b, other._a)
    
    @property
    def is_double(self) -> bool:
        """Check if this is a double domino (same value on both ends)."""
        return self._a == self._b
    
    @property
    def total(self) -> int:
        """Return the total pip count on this domino."""
        return self._a + self._b
    
    @property
    def max_value(self) -> int:
        """Return the maximum value on this domino."""
        return max(self._a, self._b)
    
    @property
    def min_value(self) -> int:
        """Return the minimum value on this domino."""
        return min(self._a, self._b)
    
    def can_connect(self, value: int) -> bool:
        """Check if this domino can connect to a specific value."""
        return self._a == value or self._b == value
    
    def other_end(self, value: int) -> Optional[int]:
        """
        Given one end value, return the other end.
        Returns None if the value is not on this domino.
        """
        if self._a == value:
            return self._b
        elif self._b == value:
            return self._a
        return None
    
    def flip(self) -> 'Domino':
        """Return a new domino with ends swapped."""
        return Domino(self._b, self._a)
    
    def contains(self, value: int) -> bool:
        """Check if this domino contains a specific value."""
        return self._a == value or self._b == value
    
    def values(self) -> Tuple[int, int]:
        """Return both values as a tuple."""
        return (self._a, self._b)
    
    def to_dict(self) -> Dict[str, int]:
        """Convert to dictionary representation."""
        return {'left': self._a, 'right': self._b}
    
    @classmethod
    def from_dict(cls, d: Dict[str, int]) -> 'Domino':
        """Create from dictionary representation."""
        return cls(d['left'], d['right'])
    
    @classmethod
    def from_tuple(cls, t: Tuple[int, int]) -> 'Domino':
        """Create from tuple representation."""
        return cls(t[0], t[1])


class DominoSet:
    """
    Represents a complete domino set (e.g., double-six set).
    """
    
    def __init__(self, max_value: int = 6):
        """
        Create a domino set with values from 0 to max_value.
        
        Args:
            max_value: Maximum pip value (6 for standard double-six set)
        """
        if max_value < 0:
            raise ValueError("max_value must be non-negative")
        self.max_value = max_value
        self._tiles: Set[Domino] = self._generate_set()
    
    def _generate_set(self) -> Set[Domino]:
        """Generate all unique dominoes for this set."""
        tiles = set()
        for i in range(self.max_value + 1):
            for j in range(i, self.max_value + 1):
                tiles.add(Domino(i, j))
        return tiles
    
    @property
    def tiles(self) -> Set[Domino]:
        """Return a copy of all tiles in the set."""
        return self._tiles.copy()
    
    @property
    def count(self) -> int:
        """Return the number of tiles in the set."""
        return len(self._tiles)
    
    def __len__(self) -> int:
        return self.count
    
    def __iter__(self):
        return iter(self._tiles)
    
    def __contains__(self, domino: Domino) -> bool:
        return domino in self._tiles
    
    def get_doubles(self) -> Set[Domino]:
        """Return all double tiles in the set."""
        return {d for d in self._tiles if d.is_double}
    
    def get_tiles_with_value(self, value: int) -> Set[Domino]:
        """Return all tiles containing a specific value."""
        if value < 0 or value > self.max_value:
            return set()
        return {d for d in self._tiles if d.contains(value)}
    
    def get_tiles_by_total(self, total: int) -> Set[Domino]:
        """Return all tiles with a specific total pip count."""
        return {d for d in self._tiles if d.total == total}
    
    def sample(self, n: int, seed: Optional[int] = None) -> List[Domino]:
        """
        Randomly sample n tiles from the set.
        
        Args:
            n: Number of tiles to sample
            seed: Random seed for reproducibility
            
        Returns:
            List of sampled dominoes
        """
        if n > self.count:
            raise ValueError(f"Cannot sample {n} tiles from set of {self.count}")
        if seed is not None:
            random.seed(seed)
        return random.sample(list(self._tiles), n)
    
    def shuffle(self, seed: Optional[int] = None) -> List[Domino]:
        """
        Return all tiles in random order.
        
        Args:
            seed: Random seed for reproducibility
            
        Returns:
            Shuffled list of all dominoes
        """
        if seed is not None:
            random.seed(seed)
        tiles = list(self._tiles)
        random.shuffle(tiles)
        return tiles
    
    def deal(self, num_players: int, tiles_per_player: Optional[int] = None,
             seed: Optional[int] = None) -> Tuple[List[List[Domino]], List[Domino]]:
        """
        Deal dominoes to players.
        
        Args:
            num_players: Number of players
            tiles_per_player: Tiles per player (None for even distribution)
            seed: Random seed for reproducibility
            
        Returns:
            Tuple of (list of player hands, remaining tiles/boneyard)
        """
        if num_players < 1:
            raise ValueError("num_players must be at least 1")
        
        shuffled = self.shuffle(seed)
        
        if tiles_per_player is None:
            # Even distribution: each player gets floor(count / num_players)
            tiles_per_player = self.count // num_players // 2
        
        if tiles_per_player * num_players > self.count:
            raise ValueError("Not enough tiles for all players")
        
        hands = []
        for i in range(num_players):
            start = i * tiles_per_player
            end = start + tiles_per_player
            hands.append(shuffled[start:end])
        
        boneyard = shuffled[tiles_per_player * num_players:]
        
        return hands, boneyard
    
    @property
    def statistics(self) -> Dict:
        """Return statistics about the domino set."""
        totals = defaultdict(int)
        for d in self._tiles:
            totals[d.total] += 1
        
        return {
            'max_value': self.max_value,
            'total_tiles': self.count,
            'doubles_count': len(self.get_doubles()),
            'total_pip_sum': sum(d.total for d in self._tiles),
            'tiles_by_total': dict(totals),
            'average_total': sum(d.total for d in self._tiles) / self.count
        }


class DominoChain:
    """
    Represents a chain of connected dominoes.
    """
    
    def __init__(self, start_domino: Optional[Domino] = None):
        """
        Initialize an empty chain or start with a domino.
        
        Args:
            start_domino: Optional first domino in the chain
        """
        self._chain: List[Tuple[Domino, int, int]] = []  # (domino, left_end, right_end)
        self._left_end: Optional[int] = None
        self._right_end: Optional[int] = None
        
        if start_domino:
            self._add_first(start_domino)
    
    def _add_first(self, domino: Domino) -> None:
        """Add the first domino to the chain."""
        self._chain.append((domino, domino.left, domino.right))
        self._left_end = domino.left
        self._right_end = domino.right
    
    @property
    def dominoes(self) -> List[Domino]:
        """Return list of dominoes in order."""
        return [item[0] for item in self._chain]
    
    @property
    def left_end(self) -> Optional[int]:
        """Return the value at the left end of the chain."""
        return self._left_end
    
    @property
    def right_end(self) -> Optional[int]:
        """Return the value at the right end of the chain."""
        return self._right_end
    
    @property
    def ends(self) -> Tuple[Optional[int], Optional[int]]:
        """Return both ends of the chain."""
        return (self._left_end, self._right_end)
    
    @property
    def length(self) -> int:
        """Return the number of dominoes in the chain."""
        return len(self._chain)
    
    @property
    def total_pips(self) -> int:
        """Return total pip count of all dominoes in chain."""
        return sum(d.total for d, _, _ in self._chain)
    
    def can_add(self, domino: Domino, end: str = 'right') -> bool:
        """
        Check if a domino can be added to the chain.
        
        Args:
            domino: Domino to add
            end: Which end to add to ('left' or 'right')
            
        Returns:
            True if the domino can be added
        """
        if not self._chain:
            return True
        
        if end == 'left':
            return domino.can_connect(self._left_end) if self._left_end is not None else True
        else:
            return domino.can_connect(self._right_end) if self._right_end is not None else True
    
    def add(self, domino: Domino, end: str = 'right') -> bool:
        """
        Add a domino to the chain.
        
        Args:
            domino: Domino to add
            end: Which end to add to ('left' or 'right')
            
        Returns:
            True if successfully added, False if not connectable
        """
        if not self._chain:
            self._add_first(domino)
            return True
        
        if end == 'left':
            if self._left_end is None or not domino.can_connect(self._left_end):
                return False
            # Determine orientation
            if domino.right == self._left_end:
                oriented = domino
            else:
                oriented = domino.flip()
            self._chain.insert(0, (oriented, oriented.left, oriented.right))
            self._left_end = oriented.left
        else:
            if self._right_end is None or not domino.can_connect(self._right_end):
                return False
            # Determine orientation
            if domino.left == self._right_end:
                oriented = domino
            else:
                oriented = domino.flip()
            self._chain.append((oriented, oriented.left, oriented.right))
            self._right_end = oriented.right
        
        return True
    
    def playable_tiles(self, tiles: Set[Domino]) -> Dict[Domino, List[str]]:
        """
        Find which tiles can be played and at which ends.
        
        Args:
            tiles: Set of tiles to check
            
        Returns:
            Dictionary mapping playable tiles to list of playable ends
        """
        playable = defaultdict(list)
        for tile in tiles:
            ends = []
            if self.can_add(tile, 'left'):
                ends.append('left')
            if self.can_add(tile, 'right'):
                ends.append('right')
            if ends:
                playable[tile] = ends
        return dict(playable)
    
    def copy(self) -> 'DominoChain':
        """Create a copy of this chain."""
        new_chain = DominoChain()
        new_chain._chain = self._chain.copy()
        new_chain._left_end = self._left_end
        new_chain._right_end = self._right_end
        return new_chain
    
    def __len__(self) -> int:
        return self.length
    
    def __str__(self) -> str:
        if not self._chain:
            return "(empty chain)"
        parts = [str(d) for d, _, _ in self._chain]
        return "-".join(parts)
    
    def __repr__(self) -> str:
        return f"DominoChain({self.length} tiles)"
    
    def to_list(self) -> List[Tuple[int, int]]:
        """Convert to list of tuples."""
        return [(d.left, d.right) for d, _, _ in self._chain]
    
    @classmethod
    def from_list(cls, tiles: List[Tuple[int, int]]) -> 'DominoChain':
        """Create chain from list of tuples."""
        chain = cls()
        for left, right in tiles:
            chain.add(Domino(left, right))
        return chain


class DominoHand:
    """
    Represents a player's hand of dominoes.
    """
    
    def __init__(self, tiles: Optional[List[Domino]] = None):
        """
        Initialize a hand with optional tiles.
        
        Args:
            tiles: Initial tiles for the hand
        """
        self._tiles: Set[Domino] = set(tiles) if tiles else set()
    
    def add(self, domino: Domino) -> None:
        """Add a domino to the hand."""
        self._tiles.add(domino)
    
    def remove(self, domino: Domino) -> bool:
        """
        Remove a domino from the hand.
        
        Returns:
            True if the domino was in the hand, False otherwise
        """
        try:
            self._tiles.remove(domino)
            return True
        except KeyError:
            return False
    
    def __contains__(self, domino: Domino) -> bool:
        return domino in self._tiles
    
    def __len__(self) -> int:
        return len(self._tiles)
    
    def __iter__(self):
        return iter(self._tiles)
    
    @property
    def tiles(self) -> Set[Domino]:
        """Return a copy of the tiles in the hand."""
        return self._tiles.copy()
    
    @property
    def total_pips(self) -> int:
        """Return total pip count in hand."""
        return sum(d.total for d in self._tiles)
    
    def has_double(self) -> bool:
        """Check if hand contains any doubles."""
        return any(d.is_double for d in self._tiles)
    
    def get_doubles(self) -> Set[Domino]:
        """Return all doubles in hand."""
        return {d for d in self._tiles if d.is_double}
    
    def get_highest_double(self) -> Optional[Domino]:
        """Return the highest double in hand, or None."""
        doubles = self.get_doubles()
        if not doubles:
            return None
        return max(doubles, key=lambda d: d.total)
    
    def get_tiles_with_value(self, value: int) -> Set[Domino]:
        """Return tiles containing a specific value."""
        return {d for d in self._tiles if d.contains(value)}
    
    def playable_tiles(self, chain: DominoChain) -> Dict[Domino, List[str]]:
        """
        Find which tiles in hand can be played on a chain.
        
        Args:
            chain: The current domino chain
            
        Returns:
            Dictionary mapping playable tiles to playable ends
        """
        return chain.playable_tiles(self._tiles)
    
    def can_play(self, chain: DominoChain) -> bool:
        """Check if any tile in hand can be played."""
        return bool(self.playable_tiles(chain))
    
    def best_play(self, chain: DominoChain, strategy: str = 'highest') -> Optional[Tuple[Domino, str]]:
        """
        Find the best tile to play based on strategy.
        
        Args:
            chain: The current domino chain
            strategy: 'highest' (highest pip count), 'double' (play doubles first),
                     'lowest' (lowest pip count), or 'strategic' (balance)
            
        Returns:
            Tuple of (domino, end) or None if no play possible
        """
        playable = self.playable_tiles(chain)
        if not playable:
            return None
        
        if strategy == 'highest':
            # Play highest pip count
            best = max(playable.keys(), key=lambda d: d.total)
        elif strategy == 'lowest':
            # Play lowest pip count
            best = min(playable.keys(), key=lambda d: d.total)
        elif strategy == 'double':
            # Play doubles first, then highest
            doubles = [d for d in playable if d.is_double]
            if doubles:
                best = max(doubles, key=lambda d: d.total)
            else:
                best = max(playable.keys(), key=lambda d: d.total)
        elif strategy == 'strategic':
            # Consider: play tiles that open more options
            best = self._strategic_play(playable, chain)
        else:
            best = list(playable.keys())[0]
        
        return (best, playable[best][0])
    
    def _strategic_play(self, playable: Dict[Domino, List[str]], 
                       chain: DominoChain) -> Domino:
        """Choose play that preserves most options."""
        # Score each tile by how many other tiles it connects with
        scores = {}
        remaining = self._tiles - set(playable.keys())
        
        for tile in playable:
            # Count how many remaining tiles share a value with this tile
            score = sum(1 for r in remaining if r.contains(tile.left) or r.contains(tile.right))
            scores[tile] = score
        
        # Choose tile with highest score (preserves connectivity)
        return max(playable.keys(), key=lambda d: scores[d])
    
    @property
    def statistics(self) -> Dict:
        """Return statistics about the hand."""
        value_counts = defaultdict(int)
        for d in self._tiles:
            value_counts[d.left] += 1
            value_counts[d.right] += 1
        
        return {
            'tile_count': len(self._tiles),
            'total_pips': self.total_pips,
            'doubles_count': len(self.get_doubles()),
            'value_distribution': dict(value_counts),
            'most_common_value': max(value_counts.items(), key=lambda x: x[1]) if value_counts else None,
            'unique_values': len(value_counts)
        }
    
    def to_list(self) -> List[Tuple[int, int]]:
        """Convert to list of tuples."""
        return [(d.left, d.right) for d in self._tiles]
    
    @classmethod
    def from_list(cls, tiles: List[Tuple[int, int]]) -> 'DominoHand':
        """Create hand from list of tuples."""
        return cls([Domino(t[0], t[1]) for t in tiles])


class DominoSolver:
    """
    Solver for domino puzzles and chain problems.
    """
    
    @staticmethod
    def find_longest_chain(tiles: List[Domino], 
                          start_value: Optional[int] = None) -> DominoChain:
        """
        Find the longest possible chain from a set of tiles.
        
        Args:
            tiles: List of domino tiles
            start_value: Optional value to start the chain with
            
        Returns:
            The longest chain found
        """
        if not tiles:
            return DominoChain()
        
        best_chain = DominoChain()
        
        def backtrack(current_chain: DominoChain, remaining: List[Domino]):
            nonlocal best_chain
            
            if current_chain.length > best_chain.length:
                best_chain = current_chain.copy()
            
            if not remaining:
                return
            
            for i, tile in enumerate(remaining):
                for end in ['left', 'right']:
                    if current_chain.can_add(tile, end):
                        new_chain = current_chain.copy()
                        new_chain.add(tile, end)
                        new_remaining = remaining[:i] + remaining[i+1:]
                        backtrack(new_chain, new_remaining)
        
        # Try starting with each tile
        for i, tile in enumerate(tiles):
            if start_value is not None:
                if not tile.contains(start_value):
                    continue
                # Orient tile correctly
                if tile.right == start_value:
                    chain = DominoChain(tile.flip())
                else:
                    chain = DominoChain(tile)
            else:
                chain = DominoChain(tile)
            
            remaining = tiles[:i] + tiles[i+1:]
            backtrack(chain, remaining)
        
        return best_chain
    
    @staticmethod
    def find_all_chains(tiles: List[Domino], 
                       min_length: int = 2) -> Generator[DominoChain, None, None]:
        """
        Find all possible chains of minimum length.
        
        Args:
            tiles: List of domino tiles
            min_length: Minimum chain length to return
            
        Yields:
            All chains that meet the minimum length
        """
        if len(tiles) < min_length:
            return
        
        def backtrack(current_chain: DominoChain, remaining: List[Domino]):
            if current_chain.length >= min_length:
                yield current_chain.copy()
            
            if not remaining:
                return
            
            for i, tile in enumerate(remaining):
                for end in ['left', 'right']:
                    if current_chain.can_add(tile, end):
                        new_chain = current_chain.copy()
                        new_chain.add(tile, end)
                        new_remaining = remaining[:i] + remaining[i+1:]
                        yield from backtrack(new_chain, new_remaining)
        
        for i, tile in enumerate(tiles):
            chain = DominoChain(tile)
            remaining = tiles[:i] + tiles[i+1:]
            yield from backtrack(chain, remaining)
    
    @staticmethod
    def can_form_single_chain(tiles: List[Domino]) -> bool:
        """
        Check if all tiles can form a single connected chain.
        
        Uses Eulerian path criteria: at most 2 values can have odd degree.
        
        Args:
            tiles: List of domino tiles
            
        Returns:
            True if a single chain is possible
        """
        if not tiles:
            return True
        
        # Count degree (occurrences) of each value
        degree = defaultdict(int)
        for d in tiles:
            degree[d.left] += 1
            degree[d.right] += 1
        
        # Count odd degrees
        odd_count = sum(1 for v in degree.values() if v % 2 == 1)
        
        return odd_count <= 2
    
    @staticmethod
    def find_chain_with_ends(tiles: List[Domino], 
                            start_value: int, 
                            end_value: int) -> Optional[DominoChain]:
        """
        Find a chain that starts with one value and ends with another.
        
        Args:
            tiles: List of domino tiles
            start_value: Value at the start of chain
            end_value: Value at the end of chain
            
        Returns:
            A chain with specified ends, or None if not possible
        """
        if not tiles:
            return None
        
        def backtrack(current_chain: DominoChain, remaining: List[Domino]) -> Optional[DominoChain]:
            if not remaining:
                if current_chain.left_end == start_value and current_chain.right_end == end_value:
                    return current_chain.copy()
                return None
            
            for i, tile in enumerate(remaining):
                for end in ['left', 'right']:
                    if current_chain.can_add(tile, end):
                        new_chain = current_chain.copy()
                        new_chain.add(tile, end)
                        new_remaining = remaining[:i] + remaining[i+1:]
                        result = backtrack(new_chain, new_remaining)
                        if result:
                            return result
            
            return None
        
        # Try starting with each tile
        for i, tile in enumerate(tiles):
            chain = DominoChain(tile)
            remaining = tiles[:i] + tiles[i+1:]
            result = backtrack(chain, remaining)
            if result:
                return result
        
        return None
    
    @staticmethod
    def solve_domino_solitaire(tiles: List[Domino]) -> Optional[DominoChain]:
        """
        Solve a domino solitaire puzzle (use all tiles in one chain).
        
        Args:
            tiles: List of domino tiles
            
        Returns:
            Complete chain using all tiles, or None if impossible
        """
        if not tiles:
            return DominoChain()
        
        # Quick check: can we form a single chain?
        if not DominoSolver.can_form_single_chain(tiles):
            return None
        
        longest = DominoSolver.find_longest_chain(tiles)
        if longest.length == len(tiles):
            return longest
        return None
    
    @staticmethod
    def count_possible_arrangements(tiles: List[Domino]) -> int:
        """
        Count the number of distinct chain arrangements possible.
        
        Note: This can be very large for many tiles.
        
        Args:
            tiles: List of domino tiles
            
        Returns:
            Number of possible arrangements
        """
        if len(tiles) <= 1:
            return len(tiles)
        
        count = 0
        for _ in DominoSolver.find_all_chains(tiles, min_length=len(tiles)):
            count += 1
        return count


class DominoGame:
    """
    Utilities for common domino game variants.
    """
    
    @staticmethod
    def draw_dominoes(game_type: str = 'standard', 
                     num_players: int = 2,
                     max_value: int = 6,
                     seed: Optional[int] = None) -> Dict:
        """
        Draw initial hands for a domino game.
        
        Args:
            game_type: 'standard' (7 each for 2 players), 'concentration', 'chicken_foot'
            num_players: Number of players
            max_value: Maximum pip value (6 for double-six)
            seed: Random seed
            
        Returns:
            Dictionary with 'hands' and 'boneyard'
        """
        domino_set = DominoSet(max_value)
        
        if game_type == 'standard':
            if num_players == 2:
                tiles_per_player = 7
            elif num_players == 3:
                tiles_per_player = 7
            else:
                tiles_per_player = 5
        else:
            tiles_per_player = 5
        
        hands, boneyard = domino_set.deal(num_players, tiles_per_player, seed)
        
        return {
            'hands': [DominoHand(h) for h in hands],
            'boneyard': boneyard,
            'total_tiles': domino_set.count
        }
    
    @staticmethod
    def determine_first_player(hands: List[DominoHand], 
                               rule: str = 'highest_double') -> int:
        """
        Determine which player goes first.
        
        Args:
            hands: List of player hands
            rule: 'highest_double', 'heaviest', or 'lowest_double'
            
        Returns:
            Index of player who goes first
        """
        if rule == 'highest_double':
            # Player with highest double goes first
            best_player = 0
            best_double = None
            
            for i, hand in enumerate(hands):
                highest = hand.get_highest_double()
                if highest is not None:
                    if best_double is None or highest.total > best_double.total:
                        best_double = highest
                        best_player = i
            
            if best_double:
                return best_player
            
            # No doubles: use heaviest
            rule = 'heaviest'
        
        if rule == 'heaviest':
            # Player with highest total pip count goes first
            return max(range(len(hands)), key=lambda i: hands[i].total_pips)
        
        if rule == 'lowest_double':
            best_player = 0
            best_double = None
            
            for i, hand in enumerate(hands):
                doubles = hand.get_doubles()
                if doubles:
                    lowest = min(doubles, key=lambda d: d.total)
                    if best_double is None or lowest.total < best_double.total:
                        best_double = lowest
                        best_player = i
            
            if best_double:
                return best_player
            return max(range(len(hands)), key=lambda i: hands[i].total_pips)
        
        return 0  # Default: first player
    
    @staticmethod
    def calculate_score_draw_game(hands: List[DominoHand]) -> Tuple[int, int]:
        """
        Calculate scores for a blocked/drawn game.
        Lowest pip count wins, and winner scores sum of all pips.
        
        Args:
            hands: List of player hands (remaining tiles)
            
        Returns:
            Tuple of (winner_index, score)
        """
        pip_counts = [hand.total_pips for hand in hands]
        winner = pip_counts.index(min(pip_counts))
        total_pips = sum(pip_counts)
        return winner, total_pips
    
    @staticmethod
    def is_round_over(hands: List[DominoHand], chain: DominoChain) -> bool:
        """
        Check if a round is over.
        
        A round ends when:
        1. A player plays all their tiles, OR
        2. No player can play (blocked)
        
        Args:
            hands: List of player hands
            chain: Current domino chain
            
        Returns:
            True if round is over
        """
        # Check if anyone is out
        if any(len(h) == 0 for h in hands):
            return True
        
        # Check if blocked (no one can play)
        if not any(hand.can_play(chain) for hand in hands):
            return True
        
        return False


# Convenience functions
def domino(left: int, right: int) -> Domino:
    """Create a domino tile."""
    return Domino(left, right)


def domino_set(max_value: int = 6) -> DominoSet:
    """Create a standard domino set."""
    return DominoSet(max_value)


def find_chain(tiles: List[Tuple[int, int]]) -> Optional[DominoChain]:
    """Find a chain using all tiles from list of tuples."""
    dominoes = [Domino(t[0], t[1]) for t in tiles]
    return DominoSolver.solve_domino_solitaire(dominoes)


def longest_chain(tiles: List[Tuple[int, int]]) -> DominoChain:
    """Find longest possible chain from list of tuples."""
    dominoes = [Domino(t[0], t[1]) for t in tiles]
    return DominoSolver.find_longest_chain(dominoes)


def can_chain_all(tiles: List[Tuple[int, int]]) -> bool:
    """Check if all tiles can form a single chain."""
    dominoes = [Domino(t[0], t[1]) for t in tiles]
    return DominoSolver.can_form_single_chain(dominoes)


def deal_hands(num_players: int = 2, max_value: int = 6, 
               seed: Optional[int] = None) -> Tuple[List[DominoHand], List[Domino]]:
    """Deal dominoes to players. Returns (hands, boneyard)."""
    result = DominoGame.draw_dominoes('standard', num_players, max_value, seed)
    return result['hands'], result['boneyard']