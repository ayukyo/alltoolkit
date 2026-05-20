"""
Dart Game Utilities

A comprehensive dart game scoring and analysis toolkit.

Features:
- Standard dart games: 501, 301, 701, Cricket, Around the Clock
- Score calculation with single, double, triple scoring zones
- Checkout suggestions for finishing games
- Game statistics and analysis
- Player management and game state tracking
- Support for multiple game variants

No external dependencies - pure Python implementation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Tuple, Set
from collections import defaultdict
import random
import math


class DartZone(Enum):
    """Dart board scoring zones."""
    MISS = 0  # Off the board
    SINGLE = 1  # Single scoring area
    DOUBLE = 2  # Double ring (outer ring)
    TRIPLE = 3  # Triple ring (inner ring)
    SINGLE_BULL = 25  # Outer bull (green)
    DOUBLE_BULL = 50  # Inner bull (red, double bull)


class GameType(Enum):
    """Standard dart game types."""
    X01 = "x01"  # 301, 501, 701, etc.
    CRICKET = "cricket"
    AROUND_THE_CLOCK = "around_the_clock"
    KILLER = "killer"
    SHANGHAI = "shanghai"


# Standard dartboard number arrangement (clockwise from top)
DARTBOARD_NUMBERS = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]

# All valid dart scores
VALID_SCORES = set(range(1, 21)) | {25}  # 1-20 and bull

# All possible dart hit values
ALL_DART_VALUES = (
    list(range(1, 21)) +  # Singles
    [x * 2 for x in range(1, 21)] +  # Doubles
    [x * 3 for x in range(1, 21)] +  # Triples
    [25, 50]  # Bulls
)


@dataclass
class DartThrow:
    """Represents a single dart throw."""
    number: int  # The number hit (1-20 or 25 for bull)
    zone: DartZone
    score: int = field(init=False)
    is_bust: bool = False
    
    def __post_init__(self):
        if self.zone == DartZone.MISS:
            self.score = 0
        elif self.zone == DartZone.SINGLE_BULL:
            self.score = 25
        elif self.zone == DartZone.DOUBLE_BULL:
            self.score = 50
        elif self.zone == DartZone.DOUBLE:
            self.score = self.number * 2
        elif self.zone == DartZone.TRIPLE:
            self.score = self.number * 3
        else:  # SINGLE
            self.score = self.number
    
    @classmethod
    def miss(cls) -> 'DartThrow':
        """Create a miss throw."""
        throw = cls(number=0, zone=DartZone.MISS)
        throw.score = 0
        return throw
    
    @classmethod
    def single(cls, number: int) -> 'DartThrow':
        """Create a single throw."""
        if number not in range(1, 21):
            raise ValueError(f"Invalid single number: {number}")
        return cls(number=number, zone=DartZone.SINGLE)
    
    @classmethod
    def double(cls, number: int) -> 'DartThrow':
        """Create a double throw."""
        if number not in range(1, 21):
            raise ValueError(f"Invalid double number: {number}")
        return cls(number=number, zone=DartZone.DOUBLE)
    
    @classmethod
    def triple(cls, number: int) -> 'DartThrow':
        """Create a triple throw."""
        if number not in range(1, 21):
            raise ValueError(f"Invalid triple number: {number}")
        return cls(number=number, zone=DartZone.TRIPLE)
    
    @classmethod
    def bull(cls, is_double: bool = False) -> 'DartThrow':
        """Create a bull throw."""
        zone = DartZone.DOUBLE_BULL if is_double else DartZone.SINGLE_BULL
        return cls(number=25, zone=zone)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'number': self.number,
            'zone': self.zone.value,
            'score': self.score,
            'is_bust': self.is_bust
        }


@dataclass
class Turn:
    """Represents a player's turn (up to 3 darts)."""
    darts: List[DartThrow] = field(default_factory=list)
    
    def add_dart(self, dart: DartThrow) -> int:
        """Add a dart to the turn. Returns total score."""
        self.darts.append(dart)
        return self.total_score
    
    @property
    def total_score(self) -> int:
        """Get total score for the turn."""
        return sum(d.score for d in self.darts)
    
    @property
    def dart_count(self) -> int:
        """Get number of darts thrown."""
        return len(self.darts)
    
    def clear(self):
        """Clear all darts."""
        self.darts.clear()
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'darts': [d.to_dict() for d in self.darts],
            'total_score': self.total_score,
            'dart_count': self.dart_count
        }


@dataclass
class Player:
    """Represents a player in a dart game."""
    name: str
    score: int = 0
    history: List[Turn] = field(default_factory=list)
    averages: Dict[str, float] = field(default_factory=lambda: {'1_dart': 0, '3_dart': 0})
    darts_thrown: int = 0
    total_score_thrown: int = 0
    highest_turn: int = 0
    checkout_attempts: int = 0
    checkout_successes: int = 0
    one_hundred_eighties: int = 0  # Perfect 180s
    one_hundred_plus: int = 0  # 100+ turns
    high_scores: List[int] = field(default_factory=list)
    
    def record_turn(self, turn: Turn):
        """Record a completed turn."""
        self.history.append(turn)
        self.darts_thrown += turn.dart_count
        self.total_score_thrown += turn.total_score
        turn_score = turn.total_score
        
        if turn_score > self.highest_turn:
            self.highest_turn = turn_score
        
        if turn_score >= 100:
            self.one_hundred_plus += 1
            self.high_scores.append(turn_score)
        
        if turn_score == 180:
            self.one_hundred_eighties += 1
        
        self._update_averages()
    
    def _update_averages(self):
        """Update average calculations."""
        if self.darts_thrown > 0:
            self.averages['1_dart'] = round(self.total_score_thrown / self.darts_thrown, 2)
        if self.darts_thrown >= 3:
            self.averages['3_dart'] = round(self.total_score_thrown / (self.darts_thrown / 3), 2)
    
    @property
    def checkout_percentage(self) -> float:
        """Calculate checkout percentage."""
        if self.checkout_attempts == 0:
            return 0.0
        return round((self.checkout_successes / self.checkout_attempts) * 100, 1)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'score': self.score,
            'averages': self.averages,
            'darts_thrown': self.darts_thrown,
            'total_score_thrown': self.total_score_thrown,
            'highest_turn': self.highest_turn,
            'checkout_attempts': self.checkout_attempts,
            'checkout_successes': self.checkout_successes,
            'one_hundred_eighties': self.one_hundred_eighties,
            'one_hundred_plus': self.one_hundred_plus,
            'checkout_percentage': self.checkout_percentage
        }


@dataclass
class X01Game:
    """X01 dart game (301, 501, 701, etc.)."""
    starting_score: int
    players: List[Player] = field(default_factory=list)
    current_player_index: int = 0
    current_turn: Turn = field(default_factory=Turn)
    is_finished: bool = False
    winner: Optional[str] = None
    double_in: bool = False  # Must start with a double
    double_out: bool = True  # Must finish with a double
    has_started: Dict[str, bool] = field(default_factory=dict)
    legs_won: Dict[str, int] = field(default_factory=dict)
    sets_won: Dict[str, int] = field(default_factory=dict)
    
    def __post_init__(self):
        for player in self.players:
            player.score = self.starting_score
            self.has_started[player.name] = not self.double_in
            self.legs_won[player.name] = 0
            self.sets_won[player.name] = 0
    
    def add_player(self, name: str):
        """Add a player to the game."""
        player = Player(name=name, score=self.starting_score)
        self.players.append(player)
        self.has_started[name] = not self.double_in
        self.legs_won[name] = 0
        self.sets_won[name] = 0
    
    @property
    def current_player(self) -> Player:
        """Get current player."""
        return self.players[self.current_player_index]
    
    def throw_dart(self, dart: DartThrow) -> Dict:
        """
        Process a dart throw.
        
        Returns dict with:
        - success: bool
        - message: str
        - is_bust: bool
        - remaining: int
        - checkout_required: bool
        """
        result = {
            'success': False,
            'message': '',
            'is_bust': False,
            'remaining': 0,
            'checkout_required': False,
            'game_over': False
        }
        
        if self.is_finished:
            result['message'] = 'Game is already finished'
            return result
        
        if self.current_turn.dart_count >= 3:
            result['message'] = 'Turn is complete. Call next_turn() first.'
            return result
        
        player = self.current_player
        new_score = player.score - dart.score
        
        # Check double-in
        if self.double_in and not self.has_started.get(player.name, True):
            if dart.zone not in (DartZone.DOUBLE, DartZone.DOUBLE_BULL):
                result['success'] = True
                result['message'] = f'Double-in required. Dart does not count.'
                self.current_turn.add_dart(dart)
                return result
            self.has_started[player.name] = True
        
        # Check bust conditions
        if new_score < 0:
            dart.is_bust = True
            result['is_bust'] = True
            result['message'] = f'Bust! Score goes below 0. Turn does not count.'
            self.current_turn.add_dart(dart)
            return result
        
        if new_score == 0:
            # Check double-out
            if self.double_out and dart.zone not in (DartZone.DOUBLE, DartZone.DOUBLE_BULL):
                dart.is_bust = True
                result['is_bust'] = True
                result['message'] = f'Bust! Double-out required. Turn does not count.'
                self.current_turn.add_dart(dart)
                return result
            
            # Winner!
            dart.is_bust = False
            self.current_turn.add_dart(dart)
            player.score = 0
            player.record_turn(self.current_turn)
            player.checkout_attempts += 1
            player.checkout_successes += 1
            
            self.is_finished = True
            self.winner = player.name
            self.legs_won[player.name] += 1
            
            result['success'] = True
            result['message'] = f'Game shot! {player.name} wins!'
            result['game_over'] = True
            result['remaining'] = 0
            return result
        
        if new_score == 1:
            # With double-out, can't leave 1 (need a double to finish)
            if self.double_out:
                dart.is_bust = True
                result['is_bust'] = True
                result['message'] = f'Bust! Cannot leave 1 with double-out. Turn does not count.'
                self.current_turn.add_dart(dart)
                return result
        
        # Valid throw
        dart.is_bust = False
        self.current_turn.add_dart(dart)
        player.score = new_score
        
        result['success'] = True
        result['message'] = f'{player.name} scored {dart.score}. Remaining: {new_score}'
        result['remaining'] = new_score
        
        # Check if checkout required
        if new_score <= 170:
            result['checkout_required'] = True
            result['checkout_darts'] = get_checkout(new_score)
        
        return result
    
    def next_turn(self) -> Dict:
        """
        End current turn and move to next player.
        
        Returns info about the turn and next player.
        """
        player = self.current_player
        
        # If bust, restore score
        if any(d.is_bust for d in self.current_turn.darts):
            player.score = self.starting_score if not self.has_started.get(player.name, True) else player.score
        else:
            player.record_turn(self.current_turn)
        
        turn_info = {
            'player': player.name,
            'turn_score': self.current_turn.total_score,
            'darts': self.current_turn.dart_count,
            'remaining': player.score
        }
        
        # Move to next player
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.current_turn = Turn()
        
        turn_info['next_player'] = self.current_player.name
        return turn_info
    
    def reset_leg(self):
        """Reset for a new leg."""
        for player in self.players:
            player.score = self.starting_score
        self.current_player_index = 0
        self.current_turn = Turn()
        self.is_finished = False
        self.winner = None
        self.has_started = {p.name: not self.double_in for p in self.players}
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'starting_score': self.starting_score,
            'players': [p.to_dict() for p in self.players],
            'current_player': self.current_player.name,
            'is_finished': self.is_finished,
            'winner': self.winner,
            'double_in': self.double_in,
            'double_out': self.double_out,
            'legs_won': self.legs_won,
            'sets_won': self.sets_won
        }


@dataclass
class CricketMark:
    """Represents marks in cricket game."""
    singles: int = 0
    doubles: int = 0
    triples: int = 0
    
    @property
    def total_marks(self) -> int:
        """Total number of marks."""
        return self.singles + self.doubles * 2 + self.triples * 3
    
    @property
    def is_closed(self) -> bool:
        """Check if number is closed (3+ marks)."""
        return self.total_marks >= 3
    
    @property
    def open_marks(self) -> int:
        """Marks that can still score (3 - current marks, if not closed)."""
        if self.is_closed:
            return 0
        return 3 - self.total_marks
    
    def add_marks(self, count: int) -> int:
        """
        Add marks and return extra marks beyond closure.
        
        Returns number of marks that count as score (if opponent not closed).
        """
        if self.is_closed:
            return count
        
        remaining = 3 - self.total_marks
        if count >= remaining:
            # Close the number
            if remaining == 3:
                self.triples += 1
            elif remaining == 2:
                self.doubles += 1
            elif remaining == 1:
                self.singles += 1
            
            # Handle extra
            extra = count - remaining
            if extra == 1:
                self.singles += 1
            elif extra == 2:
                self.doubles += 1
            
            return extra  # Extra marks beyond closure
        else:
            # Doesn't close yet
            if count == 3:
                self.triples += 1
            elif count == 2:
                self.doubles += 1
            else:
                self.singles += 1
            return 0
    
    def to_dict(self) -> dict:
        return {
            'singles': self.singles,
            'doubles': self.doubles,
            'triples': self.triples,
            'total_marks': self.total_marks,
            'is_closed': self.is_closed
        }


@dataclass
class CricketPlayer:
    """Player in a cricket game."""
    name: str
    marks: Dict[int, CricketMark] = field(default_factory=dict)
    score: int = 0
    history: List[Turn] = field(default_factory=list)
    
    def __post_init__(self):
        # Initialize marks for cricket numbers: 20, 19, 18, 17, 16, 15, and bull
        for num in [20, 19, 18, 17, 16, 15, 25]:  # 25 = bull
            self.marks[num] = CricketMark()
    
    @property
    def is_closed_out(self) -> bool:
        """Check if player has closed all numbers."""
        return all(m.is_closed for m in self.marks.values())
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'marks': {k: v.to_dict() for k, v in self.marks.items()},
            'score': self.score,
            'is_closed_out': self.is_closed_out
        }


@dataclass
class CricketGame:
    """Cricket dart game."""
    players: List[CricketPlayer] = field(default_factory=list)
    current_player_index: int = 0
    current_turn: Turn = field(default_factory=Turn)
    is_finished: bool = False
    winner: Optional[str] = None
    cricket_numbers: List[int] = field(default_factory=lambda: [20, 19, 18, 17, 16, 15, 25])
    
    def add_player(self, name: str):
        """Add a player to the game."""
        player = CricketPlayer(name=name)
        self.players.append(player)
    
    @property
    def current_player(self) -> CricketPlayer:
        """Get current player."""
        return self.players[self.current_player_index]
    
    def throw_dart(self, dart: DartThrow) -> Dict:
        """Process a dart throw in cricket."""
        result = {
            'success': False,
            'message': '',
            'marks_added': 0,
            'points_scored': 0,
            'closed': False
        }
        
        if self.is_finished:
            result['message'] = 'Game is already finished'
            return result
        
        # Check if valid cricket number
        number = dart.number if dart.zone != DartZone.MISS else 0
        if number not in self.cricket_numbers:
            # Handle bull specially
            if dart.zone in (DartZone.SINGLE_BULL, DartZone.DOUBLE_BULL):
                number = 25
            else:
                result['success'] = True
                result['message'] = f'Number {number} is not a cricket number'
                self.current_turn.add_dart(dart)
                return result
        
        if dart.zone == DartZone.MISS:
            result['success'] = True
            result['message'] = 'Miss!'
            self.current_turn.add_dart(dart)
            return result
        
        # Calculate marks
        marks = 0
        if dart.zone == DartZone.SINGLE:
            marks = 1
        elif dart.zone == DartZone.DOUBLE:
            marks = 2
        elif dart.zone == DartZone.TRIPLE:
            marks = 3
        elif dart.zone == DartZone.SINGLE_BULL:
            marks = 1
            number = 25
        elif dart.zone == DartZone.DOUBLE_BULL:
            marks = 2
            number = 25
        
        player = self.current_player
        old_closed = player.marks[number].is_closed
        extra_marks = player.marks[number].add_marks(marks)
        
        result['marks_added'] = marks
        result['closed'] = player.marks[number].is_closed and not old_closed
        
        # Check if can score points
        if extra_marks > 0:
            opponents_open = any(
                not p.marks[number].is_closed 
                for p in self.players 
                if p.name != player.name
            )
            if opponents_open:
                points = extra_marks * number
                if number == 25:
                    points = extra_marks * 25
                player.score += points
                result['points_scored'] = points
                result['message'] = f'{marks} marks on {number}, +{points} points!'
            else:
                result['message'] = f'{marks} marks on {number} (already closed by all)'
        else:
            result['message'] = f'{marks} mark(s) on {number}'
        
        self.current_turn.add_dart(dart)
        result['success'] = True
        
        # Check win condition
        if player.is_closed_out and player.score >= max(p.score for p in self.players):
            self.is_finished = True
            self.winner = player.name
            result['game_over'] = True
            result['message'] += f' Game shot! {player.name} wins!'
        
        return result
    
    def next_turn(self) -> Dict:
        """End current turn and move to next player."""
        player = self.current_player
        player.history.append(self.current_turn)
        
        turn_info = {
            'player': player.name,
            'turn_score': self.current_turn.total_score,
            'darts': self.current_turn.dart_count,
            'current_score': player.score
        }
        
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.current_turn = Turn()
        
        turn_info['next_player'] = self.current_player.name
        return turn_info
    
    def to_dict(self) -> dict:
        return {
            'players': [p.to_dict() for p in self.players],
            'current_player': self.current_player.name,
            'is_finished': self.is_finished,
            'winner': self.winner,
            'cricket_numbers': self.cricket_numbers
        }


@dataclass 
class AroundTheClockGame:
    """Around the Clock dart game."""
    players: List[Player] = field(default_factory=list)
    current_player_index: int = 0
    current_turn: Turn = field(default_factory=Turn)
    target_numbers: Dict[str, int] = field(default_factory=dict)  # player -> current target
    is_finished: bool = False
    winner: Optional[str] = None
    doubles_count: bool = False  # Doubles skip two numbers
    triples_count: bool = False  # Triples skip three numbers
    require_double_out: bool = False  # Must hit double on 20
    require_doubles: bool = False  # Must hit doubles for each number
    
    def add_player(self, name: str):
        """Add a player."""
        player = Player(name=name, score=1)
        self.players.append(player)
        self.target_numbers[name] = 1
    
    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]
    
    @property
    def current_target(self) -> int:
        return self.target_numbers[self.current_player.name]
    
    def throw_dart(self, dart: DartThrow) -> Dict:
        """Process a dart throw."""
        result = {
            'success': False,
            'message': '',
            'hit': False,
            'new_target': self.current_target
        }
        
        if self.is_finished:
            result['message'] = 'Game is already finished'
            return result
        
        player = self.current_player
        target = self.current_target
        hit = False
        
        # Check if hit the target
        if dart.number == target or (target == 25 and dart.zone in (DartZone.SINGLE_BULL, DartZone.DOUBLE_BULL)):
            hit = True
            advance = 1
            
            if dart.zone == DartZone.DOUBLE and self.doubles_count:
                advance = 2
            elif dart.zone == DartZone.TRIPLE and self.triples_count:
                advance = 3
            
            new_target = target + advance
            
            # Handle game finish
            if new_target > 20:
                if self.require_double_out and dart.zone != DartZone.DOUBLE:
                    # Single hit on 20 but double required - target stays at 20
                    result['message'] = f'Hit {target}, but double required for finish!'
                    result['hit'] = True
                    new_target = 20  # Stay on 20
                else:
                    self.is_finished = True
                    self.winner = player.name
                    result['message'] = f'Game shot! {player.name} wins!'
                    result['game_over'] = True
                    new_target = 21  # Past 20
            else:
                result['message'] = f'Hit {target}! Now target {new_target}'
            
            self.target_numbers[player.name] = new_target
            result['new_target'] = new_target
        else:
            result['message'] = f'Missed target {target}. Hit {dart.number}'
        
        result['success'] = True
        result['hit'] = hit
        self.current_turn.add_dart(dart)
        player.record_turn(self.current_turn)
        
        return result
    
    def next_turn(self) -> Dict:
        """Move to next player."""
        turn_info = {
            'player': self.current_player.name,
            'target': self.target_numbers[self.current_player.name]
        }
        
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.current_turn = Turn()
        
        turn_info['next_player'] = self.current_player.name
        turn_info['next_target'] = self.target_numbers[self.current_player.name]
        return turn_info
    
    def to_dict(self) -> dict:
        return {
            'players': [p.name for p in self.players],
            'target_numbers': self.target_numbers,
            'current_player': self.current_player.name,
            'current_target': self.current_target,
            'is_finished': self.is_finished,
            'winner': self.winner
        }


# Checkout tables - common finishes
CHECKOUTS = {
    170: ['T20', 'T20', 'DBULL'],
    167: ['T20', 'T19', 'DBULL'],
    164: ['T20', 'T18', 'DBULL'],
    161: ['T20', 'T17', 'DBULL'],
    160: ['T20', 'T20', 'D20'],
    158: ['T20', 'T20', 'D19'],
    157: ['T20', 'T19', 'D20'],
    156: ['T20', 'T20', 'D18'],
    155: ['T20', 'T19', 'D19'],
    154: ['T20', 'T18', 'D20'],
    153: ['T20', 'T19', 'D18'],
    152: ['T20', 'T20', 'D16'],
    151: ['T20', 'T17', 'D20'],
    150: ['T20', 'T18', 'D18'],
    149: ['T20', 'T19', 'D16'],
    148: ['T20', 'T20', 'D14'],
    147: ['T20', 'T17', 'D18'],
    146: ['T20', 'T18', 'D16'],
    145: ['T20', 'T19', 'D14'],
    144: ['T20', 'T20', 'D12'],
    143: ['T20', 'T17', 'D16'],
    142: ['T20', 'T18', 'D14'],
    141: ['T20', 'T19', 'D12'],
    140: ['T20', 'T20', 'D10'],
    139: ['T20', 'T17', 'D14'],
    138: ['T20', 'T18', 'D12'],
    137: ['T20', 'T19', 'D10'],
    136: ['T20', 'T20', 'D8'],
    135: ['T20', 'T17', 'D12'],
    134: ['T20', 'T18', 'D10'],
    133: ['T20', 'T19', 'D8'],
    132: ['T20', 'T20', 'D6'],
    131: ['T20', 'T17', 'D10'],
    130: ['T20', 'T18', 'D8'],
    129: ['T20', 'T19', 'D6'],
    128: ['T20', 'T18', 'D7'],
    127: ['T20', 'T17', 'D8'],
    126: ['T20', 'T19', 'D4'],
    125: ['T20', 'T18', 'D5'],
    124: ['T20', 'T16', 'D8'],
    123: ['T20', 'T17', 'D6'],
    122: ['T20', 'T18', 'D4'],
    121: ['T20', 'T17', 'D5'],
    120: ['T20', 'D20'],
    119: ['T20', 'D19'],
    118: ['T20', 'D18'],
    117: ['T20', 'D17'],
    116: ['T20', 'D16'],
    115: ['T20', 'D15'],
    114: ['T20', 'D14'],
    113: ['T20', 'D13'],
    112: ['T20', 'D12'],
    111: ['T20', 'D11'],
    110: ['T20', 'D10'],
    109: ['T20', 'D9'],
    108: ['T20', 'D8'],
    107: ['T20', 'D7'],
    106: ['T20', 'D6'],
    105: ['T20', 'D5'],
    104: ['T20', 'D4'],
    103: ['T20', 'D3'],
    102: ['T20', 'D2'],
    101: ['T20', 'D1'],
    100: ['T20', 'D20'],
    99: ['T19', 'D20'],
    98: ['T20', 'D18'],
    97: ['T19', 'D18'],
    96: ['T20', 'D16'],
    95: ['T19', 'D16'],
    94: ['T18', 'D20'],
    93: ['T19', 'D14'],
    92: ['T20', 'D12'],
    91: ['T17', 'D20'],
    90: ['T20', 'D10'],
    89: ['T19', 'D10'],
    88: ['T20', 'D8'],
    87: ['T17', 'D12'],
    86: ['T18', 'D10'],
    85: ['T15', 'D20'],
    84: ['T20', 'D6'],
    83: ['T17', 'D10'],
    82: ['T14', 'D20'],
    81: ['T15', 'D18'],
    80: ['T20', 'D4'],
    79: ['T17', 'D8'],
    78: ['T18', 'D6'],
    77: ['T15', 'D14'],
    76: ['T20', 'D2'],
    75: ['T17', 'D6'],
    74: ['T14', 'D16'],
    73: ['T19', 'D2'],
    72: ['T18', 'D4'],
    71: ['T17', 'D4'],
    70: ['T20', 'D5'],
    69: ['T13', 'D20'],
    68: ['T20', 'D4'],
    67: ['T17', 'D2'],
    66: ['T14', 'D12'],
    65: ['T19', 'D1'],
    64: ['T16', 'D8'],
    63: ['T17', 'D1'],
    62: ['T10', 'D20'],
    61: ['T15', 'D8'],
    60: ['D20'],
    59: ['D19'],
    58: ['D18'],
    57: ['D17'],
    56: ['D16'],
    55: ['D15'],
    54: ['D14'],
    53: ['D13'],
    52: ['D12'],
    51: ['D11'],
    50: ['DBULL'],
    49: ['T9', 'D11'],
    48: ['D16'],
    47: ['T9', 'D10'],
    46: ['D18'],
    45: ['D15'],
    44: ['D14'],
    43: ['D11'],
    42: ['D12'],
    41: ['D20'],
    40: ['D20'],
    39: ['D19'],
    38: ['D18'],
    37: ['D17'],
    36: ['D16'],
    35: ['D15'],
    34: ['D14'],
    33: ['D13'],
    32: ['D12'],
    31: ['D15'],
    30: ['D15'],
    29: ['D13'],
    28: ['D14'],
    27: ['D13'],
    26: ['D13'],
    25: ['D15'],
    24: ['D12'],
    23: ['D11'],
    22: ['D11'],
    21: ['D10'],
    20: ['D10'],
    19: ['D9'],
    18: ['D9'],
    17: ['D8'],
    16: ['D8'],
    15: ['D7'],
    14: ['D7'],
    13: ['D6'],
    12: ['D6'],
    11: ['D5'],
    10: ['D5'],
    9: ['D4'],
    8: ['D4'],
    7: ['D3'],
    6: ['D3'],
    5: ['D2'],
    4: ['D2'],
    3: ['D1'],
    2: ['D1'],
}


def get_checkout(score: int, darts_available: int = 3) -> Optional[List[str]]:
    """
    Get checkout suggestion for a score.
    
    Args:
        score: Score to checkout from
        darts_available: Number of darts available (1, 2, or 3)
    
    Returns:
        List of dart suggestions or None if not possible
    """
    if score < 2 or score > 170:
        return None
    
    # One dart checkouts only
    if darts_available == 1:
        if score == 50:
            return ['DBULL']
        if score <= 40 and score % 2 == 0:
            return [f'D{score // 2}']
        return None
    
    # Two dart checkouts
    if darts_available == 2:
        # Check if there's a 2-dart checkout in the table
        if score in CHECKOUTS and len(CHECKOUTS[score]) <= 2:
            return CHECKOUTS[score]
        # Try to construct one
        for first_score in range(60, 0, -1):
            remaining = score - first_score
            if remaining > 0:
                one_dart_checkout = get_checkout(remaining, 1)
                if one_dart_checkout:
                    # Format the first dart
                    if first_score == 50:
                        first_str = 'DBULL'
                    elif first_score == 25:
                        first_str = 'BULL'
                    elif first_score <= 60 and first_score % 3 == 0:
                        first_str = f'T{first_score // 3}'
                    elif first_score <= 40 and first_score % 2 == 0:
                        first_str = f'D{first_score // 2}'
                    else:
                        first_str = str(first_score)
                    return [first_str] + one_dart_checkout
        return None
    
    # Three dart checkouts (default)
    # Check if it's in our table
    if score in CHECKOUTS:
        return CHECKOUTS[score]
    
    # Try to construct one using 2 + 1 approach
    for first_score in range(60, 0, -1):
        remaining = score - first_score
        if remaining > 0:
            two_dart_checkout = get_checkout(remaining, 2)
            if two_dart_checkout:
                if first_score == 50:
                    first_str = 'DBULL'
                elif first_score == 25:
                    first_str = 'BULL'
                elif first_score <= 60 and first_score % 3 == 0:
                    first_str = f'T{first_score // 3}'
                elif first_score <= 40 and first_score % 2 == 0:
                    first_str = f'D{first_score // 2}'
                else:
                    first_str = str(first_score)
                return [first_str] + two_dart_checkout
    
    return None


def get_all_checkouts(score: int) -> List[List[str]]:
    """
    Get all possible checkout combinations for a score.
    
    Returns list of checkout options, each a list of dart throws.
    """
    if score < 2 or score > 170:
        return []
    
    checkouts = []
    
    # Start with standard checkout
    standard = get_checkout(score)
    if standard:
        checkouts.append(standard)
    
    # Add alternatives
    # This is simplified - a full implementation would enumerate all possibilities
    if score <= 40 and score % 2 == 0:
        checkouts.append([f'D{score // 2}'])
    
    if score == 50:
        checkouts.append(['DBULL'])
    
    return list(set(tuple(c) for c in checkouts))


def calculate_average_score(throws: List[DartThrow]) -> float:
    """Calculate average score per dart."""
    if not throws:
        return 0.0
    return round(sum(t.score for t in throws) / len(throws), 2)


def calculate_first_nine_average(throws: List[DartThrow]) -> float:
    """Calculate first 9 darts average (standard measure in darts)."""
    first_nine = throws[:9]
    if not first_nine:
        return 0.0
    return round(sum(t.score for t in first_nine) / 3, 2)  # Per 3 darts


def suggest_next_dart(score: int, darts_remaining: int = 3) -> Dict:
    """
    Suggest the optimal next dart to throw.
    
    Args:
        score: Current score remaining
        darts_remaining: How many darts left in turn
    
    Returns:
        Dictionary with suggestion details
    """
    result = {
        'score': score,
        'suggestion': None,
        'reason': '',
        'checkout_available': False
    }
    
    if score < 2:
        result['reason'] = 'Game already complete'
        return result
    
    if score > 170:
        # Aim for high score
        result['suggestion'] = 'T20'
        result['reason'] = 'Too high for checkout. Aim for maximum score.'
        return result
    
    # Check for checkout
    checkout = get_checkout(score, darts_remaining)
    if checkout:
        result['suggestion'] = checkout[0]
        result['reason'] = f'Checkout available: {" + ".join(checkout)}'
        result['checkout_available'] = True
        result['full_checkout'] = checkout
        return result
    
    # Suggest scoring dart
    result['suggestion'] = 'T20'
    result['reason'] = 'No checkout available. Score as high as possible.'
    return result


def get_statistics(player: Player) -> Dict:
    """Get comprehensive statistics for a player."""
    return {
        'name': player.name,
        'darts_thrown': player.darts_thrown,
        'total_score': player.total_score_thrown,
        'average_per_dart': player.averages['1_dart'],
        'average_per_3_darts': player.averages['3_dart'],
        'highest_turn': player.highest_turn,
        'one_hundred_plus': player.one_hundred_plus,
        'one_hundred_eighties': player.one_hundred_eighties,
        'checkout_attempts': player.checkout_attempts,
        'checkout_successes': player.checkout_successes,
        'checkout_percentage': player.checkout_percentage,
        'high_scores': sorted(player.high_scores, reverse=True)[:5]
    }


def create_game(game_type: str, **kwargs) -> object:
    """
    Factory function to create a dart game.
    
    Args:
        game_type: '501', '301', '701', 'cricket', 'around_clock'
        **kwargs: Additional game configuration
    
    Returns:
        Game instance
    """
    game_type = game_type.lower()
    
    if game_type in ('501', 'x01'):
        return X01Game(starting_score=kwargs.get('starting_score', 501), **kwargs)
    elif game_type == '301':
        return X01Game(starting_score=301, **kwargs)
    elif game_type == '701':
        return X01Game(starting_score=701, **kwargs)
    elif game_type == 'cricket':
        return CricketGame(**kwargs)
    elif game_type in ('around_clock', 'around_the_clock'):
        return AroundTheClockGame(**kwargs)
    else:
        raise ValueError(f"Unknown game type: {game_type}")


def analyze_turn(turn: Turn) -> Dict:
    """Analyze a turn and return statistics."""
    analysis = {
        'darts_thrown': turn.dart_count,
        'total_score': turn.total_score,
        'average': round(turn.total_score / turn.dart_count, 2) if turn.dart_count > 0 else 0,
        'is_180': turn.total_score == 180,
        'is_100_plus': turn.total_score >= 100,
        'is_140_plus': turn.total_score >= 140,
        'triples': 0,
        'doubles': 0,
        'singles': 0,
        'bulls': 0,
        'misses': 0,
        'scoring_darts': []
    }
    
    for dart in turn.darts:
        if dart.zone == DartZone.TRIPLE:
            analysis['triples'] += 1
        elif dart.zone == DartZone.DOUBLE:
            analysis['doubles'] += 1
        elif dart.zone == DartZone.SINGLE:
            analysis['singles'] += 1
        elif dart.zone in (DartZone.SINGLE_BULL, DartZone.DOUBLE_BULL):
            analysis['bulls'] += 1
        elif dart.zone == DartZone.MISS:
            analysis['misses'] += 1
        
        analysis['scoring_darts'].append({
            'number': dart.number,
            'zone': dart.zone.name,
            'score': dart.score
        })
    
    return analysis


def get_dartboard_neighbors(number: int) -> Tuple[int, int]:
    """
    Get the neighbors of a number on the dartboard.
    
    Returns tuple of (left_neighbor, right_neighbor) when facing the board.
    """
    if number not in DARTBOARD_NUMBERS:
        raise ValueError(f"Invalid dartboard number: {number}")
    
    idx = DARTBOARD_NUMBERS.index(number)
    left = DARTBOARD_NUMBERS[(idx - 1) % 20]
    right = DARTBOARD_NUMBERS[(idx + 1) % 20]
    return (left, right)


def get_dartboard_position(number: int) -> Dict:
    """
    Get position information for a number on the dartboard.
    
    Returns dict with angle, neighbors, and other info.
    """
    if number not in DARTBOARD_NUMBERS:
        if number == 25:  # Bull
            return {
                'number': 25,
                'angle': 0,
                'neighbors': None,
                'is_bull': True
            }
        raise ValueError(f"Invalid dartboard number: {number}")
    
    idx = DARTBOARD_NUMBERS.index(number)
    angle = idx * 18  # Each segment is 18 degrees
    
    left, right = get_dartboard_neighbors(number)
    
    return {
        'number': number,
        'index': idx,
        'angle_degrees': angle,
        'left_neighbor': left,
        'right_neighbor': right,
        'is_bull': False
    }


def calculate_expected_score(hit_probabilities: Dict[int, Dict[str, float]]) -> float:
    """
    Calculate expected score given hit probabilities.
    
    Args:
        hit_probabilities: Dict mapping target to probability breakdown
            e.g., {20: {'single': 0.4, 'double': 0.15, 'triple': 0.15, 'miss': 0.3}}
    
    Returns:
        Expected score
    """
    total_expected = 0.0
    
    for number, probs in hit_probabilities.items():
        if number == 25:  # Bull
            total_expected += probs.get('single_bull', 0) * 25
            total_expected += probs.get('double_bull', 0) * 50
        else:
            total_expected += probs.get('single', 0) * number
            total_expected += probs.get('double', 0) * number * 2
            total_expected += probs.get('triple', 0) * number * 3
    
    return round(total_expected, 2)


def validate_dart_throw(number: int, zone: str) -> Tuple[bool, str]:
    """
    Validate a dart throw specification.
    
    Args:
        number: Number hit (1-20 or 25 for bull)
        zone: Zone name (single, double, triple, miss, bull, dbull)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    zone = zone.lower()
    
    valid_zones = ['single', 'double', 'triple', 'miss', 'bull', 'dbull', 'single_bull', 'double_bull']
    if zone not in valid_zones:
        return False, f"Invalid zone: {zone}. Must be one of {valid_zones}"
    
    if zone in ('bull', 'single_bull', 'double_bull', 'dbull'):
        if number != 25 and zone != 'miss':
            return False, "Bull throws must have number 25"
    else:
        if number < 1 or number > 20:
            return False, f"Invalid number: {number}. Must be 1-20"
    
    return True, ""


def parse_dart_notation(notation: str) -> DartThrow:
    """
    Parse dart notation string into a DartThrow.
    
    Formats:
        - T20 = Triple 20
        - D20 = Double 20
        - 20 = Single 20
        - DBULL / DB = Double bull
        - BULL / B = Single bull
        - MISS / M = Miss
    
    Args:
        notation: Dart notation string
    
    Returns:
        DartThrow instance
    """
    notation = notation.strip().upper()
    
    if notation in ('MISS', 'M'):
        return DartThrow.miss()
    
    if notation in ('DBULL', 'DB', 'DOUBLE BULL'):
        return DartThrow.bull(is_double=True)
    
    if notation in ('BULL', 'B', 'SINGLE BULL', 'SB'):
        return DartThrow.bull(is_double=False)
    
    if notation.startswith('T'):
        number = int(notation[1:])
        return DartThrow.triple(number)
    
    if notation.startswith('D'):
        number = int(notation[1:])
        return DartThrow.double(number)
    
    # Just a number = single
    number = int(notation)
    return DartThrow.single(number)


def format_dart_throw(dart: DartThrow) -> str:
    """Format a DartThrow as notation string."""
    if dart.zone == DartZone.MISS:
        return 'MISS'
    if dart.zone == DartZone.DOUBLE_BULL:
        return 'DBULL'
    if dart.zone == DartZone.SINGLE_BULL:
        return 'BULL'
    if dart.zone == DartZone.TRIPLE:
        return f'T{dart.number}'
    if dart.zone == DartZone.DOUBLE:
        return f'D{dart.number}'
    return str(dart.number)


def get_highest_finish(score: int) -> Optional[int]:
    """
    Get the highest possible finish for a score.
    
    Returns the maximum score that can be checked out in one dart.
    """
    if score < 2:
        return None
    
    # Checkouts in one dart
    if score <= 50:
        if score == 50:
            return 50
        if score <= 40 and score % 2 == 0:
            return score
    
    return None


def is_checkout_possible(score: int, darts: int = 3) -> bool:
    """Check if a checkout is possible with given darts."""
    if score < 2:
        return False
    if score > 170:
        return False
    if darts == 1:
        return score in (50,) or (score <= 40 and score % 2 == 0)
    return True


# Export all classes and functions
__all__ = [
    'DartZone',
    'GameType', 
    'DartThrow',
    'Turn',
    'Player',
    'X01Game',
    'CricketMark',
    'CricketPlayer',
    'CricketGame',
    'AroundTheClockGame',
    'CHECKOUTS',
    'DARTBOARD_NUMBERS',
    'VALID_SCORES',
    'ALL_DART_VALUES',
    'get_checkout',
    'get_all_checkouts',
    'calculate_average_score',
    'calculate_first_nine_average',
    'suggest_next_dart',
    'get_statistics',
    'create_game',
    'analyze_turn',
    'get_dartboard_neighbors',
    'get_dartboard_position',
    'calculate_expected_score',
    'validate_dart_throw',
    'parse_dart_notation',
    'format_dart_throw',
    'get_highest_finish',
    'is_checkout_possible',
]