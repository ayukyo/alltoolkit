#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Hysteresis Utilities Module
=========================================
A comprehensive hysteresis utility module for Python with zero external dependencies.

Hysteresis is a phenomenon where the output of a system depends not only on its 
current input but also on its history of past inputs. This module provides tools
for implementing hysteresis in various applications:

Features:
    - Basic Hysteresis: Simple on/off control with configurable thresholds
    - Schmitt Trigger: Digital circuit behavior with hysteresis
    - Dead Zone: Region where input changes don't affect output
    - Signal Filtering: Noise reduction using hysteresis
    - State Machine: State transitions with hysteresis bands
    - Multi-level Hysteresis: Multiple output levels with hysteresis
    - Configurable edge modes (rising/falling)
    - History tracking and statistics

Common Applications:
    - Thermostat control (turn on at X, turn off at Y)
    - Debouncing noisy signals
    - Edge detection with noise immunity
    - Alarm systems with hysteresis
    - Control systems
    - Audio processing

Author: AllToolkit Contributors
License: MIT
"""

from typing import Callable, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import math


# ============================================================================
# Type Aliases
# ============================================================================

Number = Union[int, float]


# ============================================================================
# Enums
# ============================================================================

class EdgeMode(Enum):
    """Edge triggering modes."""
    RISING = "rising"      # Trigger on rising edge only
    FALLING = "falling"    # Trigger on falling edge only
    BOTH = "both"          # Trigger on both edges


class OutputState(Enum):
    """Output state for binary hysteresis."""
    LOW = 0
    HIGH = 1


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class HysteresisConfig:
    """Configuration for hysteresis behavior."""
    low_threshold: float
    high_threshold: float
    initial_state: bool = False
    dead_zone: float = 0.0
    
    def __post_init__(self):
        if self.high_threshold <= self.low_threshold:
            raise ValueError(
                f"High threshold ({self.high_threshold}) must be greater than "
                f"low threshold ({self.low_threshold})"
            )
        if self.dead_zone < 0:
            raise ValueError(f"Dead zone must be non-negative, got {self.dead_zone}")


@dataclass
class HysteresisStats:
    """Statistics for hysteresis operations."""
    total_updates: int = 0
    state_changes: int = 0
    rising_edges: int = 0
    falling_edges: int = 0
    time_in_high: int = 0
    time_in_low: int = 0
    
    @property
    def high_ratio(self) -> float:
        """Ratio of time spent in high state."""
        total = self.time_in_high + self.time_in_low
        return self.time_in_high / total if total > 0 else 0.0


@dataclass
class HysteresisEvent:
    """Event record for hysteresis state change."""
    timestamp: int
    input_value: float
    from_state: bool
    to_state: bool
    edge_type: str  # 'rising' or 'falling'


# ============================================================================
# Basic Hysteresis Class
# ============================================================================

class Hysteresis:
    """
    Basic hysteresis implementation for on/off control.
    
    This class implements a simple hysteresis with two thresholds:
    - Output turns ON when input rises above high_threshold
    - Output turns OFF when input falls below low_threshold
    
    The gap between thresholds provides noise immunity and prevents
    rapid state changes near a single threshold point.
    
    Example:
        >>> hyst = Hysteresis(low_threshold=18.0, high_threshold=22.0)
        >>> hyst.update(20.0)  # Between thresholds - no change
        False
        >>> hyst.update(23.0)  # Above high threshold - turns on
        True
        >>> hyst.update(20.0)  # Between thresholds - stays on
        True
        >>> hyst.update(17.0)  # Below low threshold - turns off
        False
    """
    
    def __init__(
        self,
        low_threshold: float,
        high_threshold: float,
        initial_state: bool = False,
        track_history: bool = False
    ):
        """
        Initialize hysteresis controller.
        
        Args:
            low_threshold: Threshold for turning OFF (falling)
            high_threshold: Threshold for turning ON (rising)
            initial_state: Initial output state
            track_history: Whether to track state change history
        """
        if high_threshold <= low_threshold:
            raise ValueError(
                f"High threshold ({high_threshold}) must be greater than "
                f"low threshold ({low_threshold})"
            )
        
        self._low_threshold = low_threshold
        self._high_threshold = high_threshold
        self._state = initial_state
        self._track_history = track_history
        self._history: List[HysteresisEvent] = []
        self._stats = HysteresisStats()
        self._last_value: Optional[float] = None
    
    @property
    def state(self) -> bool:
        """Current output state."""
        return self._state
    
    @property
    def low_threshold(self) -> float:
        """Low threshold (OFF threshold)."""
        return self._low_threshold
    
    @property
    def high_threshold(self) -> float:
        """High threshold (ON threshold)."""
        return self._high_threshold
    
    @property
    def hysteresis_gap(self) -> float:
        """The gap between high and low thresholds."""
        return self._high_threshold - self._low_threshold
    
    @property
    def stats(self) -> HysteresisStats:
        """Statistics for this hysteresis."""
        return self._stats
    
    @property
    def history(self) -> List[HysteresisEvent]:
        """History of state changes."""
        return self._history.copy()
    
    def update(self, value: float) -> bool:
        """
        Update the hysteresis state based on input value.
        
        Args:
            value: Current input value
            
        Returns:
            Current output state after processing
        """
        old_state = self._state
        self._last_value = value
        self._stats.total_updates += 1
        
        # Apply hysteresis logic
        if value >= self._high_threshold:
            # Input above high threshold - turn ON
            self._state = True
        elif value <= self._low_threshold:
            # Input below low threshold - turn OFF
            self._state = False
        # else: between thresholds - maintain current state
        
        # Track statistics
        if self._state:
            self._stats.time_in_high += 1
        else:
            self._stats.time_in_low += 1
        
        # Record state change
        if self._state != old_state:
            self._stats.state_changes += 1
            if self._state:
                self._stats.rising_edges += 1
            else:
                self._stats.falling_edges += 1
            
            if self._track_history:
                self._history.append(HysteresisEvent(
                    timestamp=self._stats.total_updates,
                    input_value=value,
                    from_state=old_state,
                    to_state=self._state,
                    edge_type='rising' if self._state else 'falling'
                ))
        
        return self._state
    
    def reset(self, state: bool = False) -> None:
        """
        Reset the hysteresis to initial state.
        
        Args:
            state: Initial state after reset
        """
        self._state = state
        self._last_value = None
        self._history.clear()
        self._stats = HysteresisStats()
    
    def set_thresholds(self, low: float, high: float) -> None:
        """
        Update the thresholds.
        
        Args:
            low: New low threshold
            high: New high threshold
        """
        if high <= low:
            raise ValueError(f"High ({high}) must be greater than low ({low})")
        self._low_threshold = low
        self._high_threshold = high
    
    def get_state_str(self) -> str:
        """Get state as a string."""
        return "ON/HIGH" if self._state else "OFF/LOW"
    
    def __repr__(self) -> str:
        return (
            f"Hysteresis(low={self._low_threshold}, high={self._high_threshold}, "
            f"state={'ON' if self._state else 'OFF'})"
        )


# ============================================================================
# Schmitt Trigger
# ============================================================================

class SchmittTrigger:
    """
    Schmitt Trigger implementation with digital output.
    
    A Schmitt trigger is a comparator circuit with hysteresis implemented
    by positive feedback. It converts an analog input signal to a digital
    output signal, providing noise immunity at the threshold points.
    
    Example:
        >>> trigger = SchmittTrigger(low_threshold=0.4, high_threshold=0.6)
        >>> trigger.process([0.3, 0.5, 0.7, 0.5, 0.3])
        [False, False, True, True, False]
    """
    
    def __init__(
        self,
        low_threshold: float,
        high_threshold: float,
        initial_state: bool = False,
        invert: bool = False
    ):
        """
        Initialize Schmitt Trigger.
        
        Args:
            low_threshold: Threshold for switching to LOW
            high_threshold: Threshold for switching to HIGH
            initial_state: Initial output state
            invert: If True, invert output (HIGH becomes LOW, LOW becomes HIGH)
        """
        self._hysteresis = Hysteresis(low_threshold, high_threshold, initial_state)
        self._invert = invert
    
    @property
    def state(self) -> bool:
        """Current output state (optionally inverted)."""
        state = self._hysteresis.state
        return not state if self._invert else state
    
    @property
    def raw_state(self) -> bool:
        """Raw internal state (without inversion)."""
        return self._hysteresis.state
    
    def update(self, value: float) -> bool:
        """
        Process a single input value.
        
        Args:
            value: Input value
            
        Returns:
            Output state (optionally inverted)
        """
        self._hysteresis.update(value)
        return self.state
    
    def process(self, values: List[float]) -> List[bool]:
        """
        Process a sequence of input values.
        
        Args:
            values: List of input values
            
        Returns:
            List of output states
        """
        return [self.update(v) for v in values]
    
    def process_signal(self, signal: List[float]) -> List[bool]:
        """
        Alias for process() - process a signal sequence.
        
        Args:
            signal: Input signal values
            
        Returns:
            Output signal
        """
        return self.process(signal)
    
    def reset(self, state: bool = False) -> None:
        """Reset to initial state."""
        self._hysteresis.reset(state)
    
    @property
    def thresholds(self) -> Tuple[float, float]:
        """Get the (low, high) thresholds."""
        return (self._hysteresis.low_threshold, self._hysteresis.high_threshold)
    
    def __repr__(self) -> str:
        return (
            f"SchmittTrigger(low={self._hysteresis.low_threshold}, "
            f"high={self._hysteresis.high_threshold}, "
            f"invert={self._invert})"
        )


# ============================================================================
# Dead Zone Controller
# ============================================================================

class DeadZone:
    """
    Dead zone (dead band) implementation.
    
    A dead zone is a region around zero (or a setpoint) where input values
    are ignored. This is useful for:
    - Eliminating noise near zero
    - Preventing chattering in control systems
    - Implementing tolerance bands
    
    Example:
        >>> dz = DeadZone(size=2.0, center=0.0)
        >>> dz.process([0.5, 1.0, 1.5, 2.5, 3.0])
        [0.0, 0.0, 0.0, 2.5, 3.0]
    """
    
    def __init__(
        self,
        size: float,
        center: float = 0.0,
        mode: str = "symmetric"
    ):
        """
        Initialize dead zone.
        
        Args:
            size: Size of the dead zone
            center: Center point of the dead zone
            mode: "symmetric", "positive_only", or "negative_only"
        """
        if size < 0:
            raise ValueError(f"Dead zone size must be non-negative, got {size}")
        
        self._size = size
        self._center = center
        self._mode = mode
        
        # Calculate boundaries
        if mode == "symmetric":
            self._low = center - size
            self._high = center + size
        elif mode == "positive_only":
            self._low = center
            self._high = center + size
        elif mode == "negative_only":
            self._low = center - size
            self._high = center
        else:
            raise ValueError(f"Invalid mode: {mode}")
    
    @property
    def size(self) -> float:
        """Dead zone size."""
        return self._size
    
    @property
    def center(self) -> float:
        """Center point."""
        return self._center
    
    @property
    def boundaries(self) -> Tuple[float, float]:
        """Dead zone boundaries (low, high)."""
        return (self._low, self._high)
    
    def in_dead_zone(self, value: float) -> bool:
        """Check if value is within dead zone."""
        return self._low <= value <= self._high
    
    def process(self, value: float) -> float:
        """
        Process a single value through the dead zone.
        
        Args:
            value: Input value
            
        Returns:
            0.0 if in dead zone, original value otherwise
        """
        if self.in_dead_zone(value):
            return 0.0
        return value
    
    def process_with_offset(self, value: float) -> float:
        """
        Process value and offset to maintain continuity.
        
        Args:
            value: Input value
            
        Returns:
            Adjusted value with dead zone applied
        """
        if value > self._high:
            return value - self._high
        elif value < self._low:
            return value - self._low
        return 0.0
    
    def process_list(self, values: List[float]) -> List[float]:
        """Process a list of values."""
        return [self.process(v) for v in values]
    
    def process_signal(self, signal: List[float]) -> List[float]:
        """Alias for process_list."""
        return self.process_list(signal)
    
    def __repr__(self) -> str:
        return f"DeadZone(size={self._size}, center={self._center}, mode={self._mode})"


# ============================================================================
# Signal Filter with Hysteresis
# ============================================================================

class HysteresisFilter:
    """
    Signal filter using hysteresis for noise reduction.
    
    This filter applies hysteresis to reduce noise in a signal by requiring
    the signal to move beyond a certain threshold before changing the output.
    
    Example:
        >>> filter = HysteresisFilter(window_size=3, threshold=0.5)
        >>> filtered = filter.filter([1.0, 1.1, 1.2, 5.0, 5.1, 5.2])
    """
    
    def __init__(
        self,
        threshold: float,
        window_size: int = 1,
        initial_value: Optional[float] = None
    ):
        """
        Initialize hysteresis filter.
        
        Args:
            threshold: Minimum change required to update output
            window_size: Number of samples to consider (default: 1)
            initial_value: Initial output value
        """
        self._threshold = threshold
        self._window_size = max(1, window_size)
        self._output = initial_value
        self._buffer: List[float] = []
        self._updates = 0
    
    @property
    def output(self) -> Optional[float]:
        """Current filtered output."""
        return self._output
    
    @property
    def threshold(self) -> float:
        """Current threshold."""
        return self._threshold
    
    def update(self, value: float) -> float:
        """
        Update filter with new value.
        
        Args:
            value: New input value
            
        Returns:
            Current filtered output
        """
        self._updates += 1
        self._buffer.append(value)
        
        # Keep only last window_size values
        if len(self._buffer) > self._window_size:
            self._buffer.pop(0)
        
        # Calculate average of buffer
        avg = sum(self._buffer) / len(self._buffer)
        
        # Apply hysteresis
        if self._output is None:
            self._output = avg
        elif abs(avg - self._output) >= self._threshold:
            self._output = avg
        
        return self._output
    
    def filter(self, values: List[float]) -> List[float]:
        """
        Filter a sequence of values.
        
        Args:
            values: Input signal
            
        Returns:
            Filtered signal
        """
        result = []
        for v in values:
            result.append(self.update(v))
        return result
    
    def reset(self, initial_value: Optional[float] = None) -> None:
        """Reset filter state."""
        self._output = initial_value
        self._buffer.clear()
        self._updates = 0
    
    def __repr__(self) -> str:
        return f"HysteresisFilter(threshold={self._threshold}, window={self._window_size})"


# ============================================================================
# Multi-Level Hysteresis
# ============================================================================

class MultiLevelHysteresis:
    """
    Hysteresis with multiple output levels.
    
    This implements hysteresis with multiple threshold bands, useful for
    applications like:
    - Multi-stage heating/cooling systems
    - Battery charge level indicators
    - Traffic light controllers
    - Multi-zone alarm systems
    
    Example:
        >>> mh = MultiLevelHysteresis(
        ...     thresholds=[20, 40, 60, 80],
        ...     hysteresis=5
        ... )
        >>> mh.update(30)  # Level 1
        1
        >>> mh.update(50)  # Level 2
        2
    """
    
    def __init__(
        self,
        thresholds: List[float],
        hysteresis: float = 0.0,
        initial_level: int = 0
    ):
        """
        Initialize multi-level hysteresis.
        
        Args:
            thresholds: List of threshold values (ascending order)
            hysteresis: Hysteresis gap for each threshold
            initial_level: Initial output level
        """
        if not thresholds:
            raise ValueError("Thresholds cannot be empty")
        
        # Sort thresholds
        self._thresholds = sorted(thresholds)
        self._hysteresis = hysteresis
        self._level = initial_level
        self._num_levels = len(thresholds) + 1
        
        # Validate
        if hysteresis < 0:
            raise ValueError("Hysteresis must be non-negative")
        if initial_level < 0 or initial_level >= self._num_levels:
            raise ValueError(f"Initial level must be 0-{self._num_levels - 1}")
    
    @property
    def level(self) -> int:
        """Current output level."""
        return self._level
    
    @property
    def num_levels(self) -> int:
        """Number of output levels."""
        return self._num_levels
    
    @property
    def thresholds(self) -> List[float]:
        """Threshold values."""
        return self._thresholds.copy()
    
    def update(self, value: float) -> int:
        """
        Update level based on input value.
        
        Args:
            value: Current input value
            
        Returns:
            Current output level
        """
        # Calculate target level based on value (without hysteresis)
        target_level = 0
        for threshold in self._thresholds:
            if value >= threshold:
                target_level += 1
        
        # Apply hysteresis for transitions
        if target_level > self._level:
            # Rising: check if value exceeds threshold + hysteresis
            rise_threshold = self._thresholds[target_level - 1] + self._hysteresis
            if value >= rise_threshold:
                self._level = target_level
        elif target_level < self._level:
            # Falling: check if value is below threshold - hysteresis
            fall_threshold = self._thresholds[self._level - 1] - self._hysteresis
            if value < fall_threshold:
                self._level = target_level
        # else: target_level == self._level, no change needed
        
        return self._level
    
    def get_level_info(self) -> dict:
        """Get information about current level."""
        return {
            "level": self._level,
            "min_threshold": self._thresholds[0] if self._level > 0 else float("-inf"),
            "max_threshold": (
                self._thresholds[self._level] 
                if self._level < len(self._thresholds) 
                else float("inf")
            )
        }
    
    def reset(self, level: int = 0) -> None:
        """Reset to specified level."""
        if level < 0 or level >= self._num_levels:
            raise ValueError(f"Level must be 0-{self._num_levels - 1}")
        self._level = level
    
    def __repr__(self) -> str:
        return f"MultiLevelHysteresis(levels={self._num_levels}, hysteresis={self._hysteresis})"


# ============================================================================
# State Machine with Hysteresis
# ============================================================================

class HysteresisStateMachine:
    """
    State machine with hysteresis bands for state transitions.
    
    Each state has entry and exit thresholds, providing hysteresis
    behavior for state transitions.
    
    Example:
        >>> sm = HysteresisStateMachine()
        >>> sm.add_state("cold", enter_below=15, exit_above=18)
        >>> sm.add_state("comfortable", enter_below=22, exit_above=25)
        >>> sm.add_state("hot", enter_above=25, exit_below=22)
        >>> sm.update(20)  # Returns 'comfortable'
    """
    
    def __init__(self, initial_state: Optional[str] = None):
        """
        Initialize state machine.
        
        Args:
            initial_state: Initial state name
        """
        self._states: dict = {}
        self._current_state = initial_state
        self._history: List[Tuple[int, str, float]] = []
        self._updates = 0
    
    @property
    def state(self) -> Optional[str]:
        """Current state."""
        return self._current_state
    
    @property
    def history(self) -> List[Tuple[int, str, float]]:
        """State change history as (timestamp, state, value)."""
        return self._history.copy()
    
    def add_state(
        self,
        name: str,
        enter_above: Optional[float] = None,
        enter_below: Optional[float] = None,
        exit_above: Optional[float] = None,
        exit_below: Optional[float] = None
    ) -> None:
        """
        Add a state with entry/exit conditions.
        
        Args:
            name: State name
            enter_above: Enter state when value goes above this
            enter_below: Enter state when value goes below this
            exit_above: Exit state when value goes above this
            exit_below: Exit state when value goes below this
        """
        self._states[name] = {
            "enter_above": enter_above,
            "enter_below": enter_below,
            "exit_above": exit_above,
            "exit_below": exit_below
        }
    
    def update(self, value: float) -> str:
        """
        Update state machine with new value.
        
        Args:
            value: Current input value
            
        Returns:
            Current state name
        """
        self._updates += 1
        old_state = self._current_state
        
        # Check if we should exit current state
        if self._current_state and self._current_state in self._states:
            state_config = self._states[self._current_state]
            
            exit_above = state_config.get("exit_above")
            exit_below = state_config.get("exit_below")
            
            should_exit = False
            if exit_above is not None and value > exit_above:
                should_exit = True
            if exit_below is not None and value < exit_below:
                should_exit = True
            
            if should_exit:
                self._current_state = None
        
        # If no current state, find a state to enter
        if self._current_state is None:
            for name, config in self._states.items():
                enter_above = config.get("enter_above")
                enter_below = config.get("enter_below")
                
                should_enter = False
                
                # Handle different entry condition combinations
                if enter_above is not None and enter_below is not None:
                    # Both specified: enter when value is in range
                    should_enter = enter_above < value < enter_below
                elif enter_above is not None:
                    # enter_above only: enter when value > threshold
                    should_enter = value > enter_above
                elif enter_below is not None:
                    # enter_below only: enter when value < threshold
                    should_enter = value < enter_below
                
                if should_enter:
                    self._current_state = name
                    break
        
        # Record state change
        if self._current_state != old_state:
            self._history.append((self._updates, self._current_state, value))
        
        return self._current_state or "undefined"
    
    def reset(self, state: Optional[str] = None) -> None:
        """Reset state machine."""
        self._current_state = state
        self._history.clear()
        self._updates = 0
    
    def __repr__(self) -> str:
        return f"HysteresisStateMachine(states={len(self._states)}, current={self._current_state})"


# ============================================================================
# Thermostat Class (Inverted Logic for Heating/Cooling)
# ============================================================================

class Thermostat:
    """
    Thermostat controller with hysteresis (inverted logic for heating).
    
    For heating systems:
    - Turn ON when temperature drops below heat_on threshold
    - Turn OFF when temperature rises above heat_off threshold
    
    This is opposite to standard hysteresis behavior, hence the inverted logic.
    
    Example:
        >>> thermo = Thermostat(heat_on=18.0, heat_off=22.0)
        >>> thermo.update(17.0)  # Below 18 - heating ON
        True
        >>> thermo.update(23.0)  # Above 22 - heating OFF
        False
    """
    
    def __init__(
        self,
        heat_on: float,
        heat_off: float,
        initial_on: bool = False
    ):
        """
        Initialize thermostat.
        
        Args:
            heat_on: Temperature threshold to turn heating ON (when temp drops below)
            heat_off: Temperature threshold to turn heating OFF (when temp rises above)
            initial_on: Initial heating state
        """
        if heat_off <= heat_on:
            raise ValueError(
                f"heat_off ({heat_off}) must be greater than heat_on ({heat_on})"
            )
        
        self._heat_on = heat_on
        self._heat_off = heat_off
        self._heating = initial_on
        self._stats = HysteresisStats()
        self._last_temp: Optional[float] = None
    
    @property
    def heating(self) -> bool:
        """Whether heating is currently ON."""
        return self._heating
    
    @property
    def state(self) -> bool:
        """Alias for heating property."""
        return self._heating
    
    @property
    def heat_on_threshold(self) -> float:
        """Temperature threshold to turn heating ON."""
        return self._heat_on
    
    @property
    def heat_off_threshold(self) -> float:
        """Temperature threshold to turn heating OFF."""
        return self._heat_off
    
    @property
    def hysteresis_gap(self) -> float:
        """Gap between thresholds."""
        return self._heat_off - self._heat_on
    
    @property
    def stats(self) -> HysteresisStats:
        """Statistics for this thermostat."""
        return self._stats
    
    def update(self, temperature: float) -> bool:
        """
        Update thermostat state based on temperature.
        
        Args:
            temperature: Current temperature
            
        Returns:
            Current heating state (True = heating ON)
        """
        old_state = self._heating
        self._last_temp = temperature
        self._stats.total_updates += 1
        
        # Thermostat logic (inverted from standard hysteresis):
        # - Turn ON when temp drops below heat_on
        # - Turn OFF when temp rises above heat_off
        if temperature <= self._heat_on:
            self._heating = True  # Cold - turn heating ON
        elif temperature >= self._heat_off:
            self._heating = False  # Warm - turn heating OFF
        # else: between thresholds - maintain current state
        
        # Track statistics
        if self._heating:
            self._stats.time_in_high += 1
        else:
            self._stats.time_in_low += 1
        
        # Track state changes
        if self._heating != old_state:
            self._stats.state_changes += 1
            if self._heating:
                self._stats.rising_edges += 1
            else:
                self._stats.falling_edges += 1
        
        return self._heating
    
    def reset(self, heating: bool = False) -> None:
        """Reset thermostat state."""
        self._heating = heating
        self._last_temp = None
        self._stats = HysteresisStats()
    
    def __repr__(self) -> str:
        return (
            f"Thermostat(heat_on={self._heat_on}, heat_off={self._heat_off}, "
            f"heating={'ON' if self._heating else 'OFF'})"
        )


# ============================================================================
# Utility Functions
# ============================================================================

def create_thermostat(
    heat_on: float,
    heat_off: float,
    initial_on: bool = False
) -> Thermostat:
    """
    Create a thermostat-style hysteresis controller.
    
    Args:
        heat_on: Temperature to turn heating ON (when temp drops below)
        heat_off: Temperature to turn heating OFF (when temp rises above)
        initial_on: Initial heating state
        
    Returns:
        Configured Thermostat instance
    """
    return Thermostat(heat_on=heat_on, heat_off=heat_off, initial_on=initial_on)


def create_alarm(
    trigger_threshold: float,
    reset_threshold: float,
    initial_triggered: bool = False
) -> Hysteresis:
    """
    Create an alarm-style hysteresis controller.
    
    Args:
        trigger_threshold: Value that triggers the alarm
        reset_threshold: Value that resets the alarm
        initial_triggered: Initial alarm state
        
    Returns:
        Configured Hysteresis instance
    """
    return Hysteresis(
        low_threshold=reset_threshold,
        high_threshold=trigger_threshold,
        initial_state=initial_triggered
    )


def debounce_signal(
    signal: List[float],
    threshold: float
) -> List[float]:
    """
    Apply hysteresis-based debouncing to a signal.
    
    Args:
        signal: Input signal values
        threshold: Minimum change threshold
        
    Returns:
        Debounced signal
    """
    if not signal:
        return []
    
    result = [signal[0]]
    for value in signal[1:]:
        if abs(value - result[-1]) >= threshold:
            result.append(value)
        else:
            result.append(result[-1])
    return result


def detect_edges_with_hysteresis(
    signal: List[float],
    low_threshold: float,
    high_threshold: float
) -> List[Tuple[int, str]]:
    """
    Detect edges in a signal with hysteresis noise immunity.
    
    Args:
        signal: Input signal
        low_threshold: Low threshold
        high_threshold: High threshold
        
    Returns:
        List of (index, edge_type) tuples
    """
    hyst = Hysteresis(low_threshold, high_threshold)
    edges = []
    
    for i, value in enumerate(signal):
        old_state = hyst.state
        new_state = hyst.update(value)
        
        if new_state != old_state:
            edge_type = "rising" if new_state else "falling"
            edges.append((i, edge_type))
    
    return edges


# ============================================================================
# Convenience Aliases
# ============================================================================

# Create commonly used instances
def on_off_controller(low: float, high: float, initial: bool = False) -> Hysteresis:
    """Alias for Hysteresis with clearer name for control applications."""
    return Hysteresis(low, high, initial)


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Enums
    'EdgeMode',
    'OutputState',
    
    # Data classes
    'HysteresisConfig',
    'HysteresisStats',
    'HysteresisEvent',
    
    # Main classes
    'Hysteresis',
    'SchmittTrigger',
    'DeadZone',
    'HysteresisFilter',
    'MultiLevelHysteresis',
    'HysteresisStateMachine',
    'Thermostat',
    
    # Utility functions
    'create_thermostat',
    'create_alarm',
    'debounce_signal',
    'detect_edges_with_hysteresis',
    'on_off_controller',
]