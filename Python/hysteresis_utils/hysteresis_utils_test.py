#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Hysteresis Utilities Test Suite
=============================================
Comprehensive tests for hysteresis utilities module.

Author: AllToolkit Contributors
License: MIT
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Hysteresis,
    SchmittTrigger,
    DeadZone,
    HysteresisFilter,
    MultiLevelHysteresis,
    HysteresisStateMachine,
    Thermostat,
    HysteresisConfig,
    HysteresisStats,
    EdgeMode,
    OutputState,
    create_thermostat,
    create_alarm,
    debounce_signal,
    detect_edges_with_hysteresis,
    on_off_controller,
)


def test_hysteresis_basic():
    """Test basic Hysteresis functionality."""
    print("Testing Hysteresis basic functionality...")
    
    # Create hysteresis with thresholds 18 and 22
    hyst = Hysteresis(low_threshold=18.0, high_threshold=22.0)
    
    # Initial state should be False (OFF)
    assert hyst.state == False, "Initial state should be False"
    
    # Test rising above high threshold - should turn ON
    assert hyst.update(23.0) == True, "Should turn ON at 23"
    
    # Between thresholds - should stay ON
    assert hyst.update(20.0) == True, "Should stay ON at 20 (between thresholds)"
    
    # Below low threshold - should turn OFF
    assert hyst.update(17.0) == False, "Should turn OFF at 17"
    
    # Between thresholds - should stay OFF
    assert hyst.update(20.0) == False, "Should stay OFF at 20 (between thresholds)"
    
    # Test hysteresis gap
    assert hyst.hysteresis_gap == 4.0, "Hysteresis gap should be 4"
    
    print("  ✓ Basic hysteresis tests passed")


def test_hysteresis_initial_state():
    """Test Hysteresis with initial state."""
    print("Testing Hysteresis initial state...")
    
    # Start with ON state
    hyst = Hysteresis(18.0, 22.0, initial_state=True)
    assert hyst.state == True, "Initial state should be True"
    
    # Between thresholds - stays ON
    assert hyst.update(20.0) == True, "Should stay ON at 20"
    
    # Below low threshold - turns OFF
    assert hyst.update(17.0) == False, "Should turn OFF at 17"
    
    print("  ✓ Initial state tests passed")


def test_hysteresis_threshold_validation():
    """Test that invalid thresholds raise errors."""
    print("Testing threshold validation...")
    
    # High must be greater than low
    try:
        Hysteresis(22.0, 18.0)  # Invalid: high < low
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "must be greater than" in str(e)
    
    # Equal thresholds are invalid
    try:
        Hysteresis(20.0, 20.0)  # Invalid: equal thresholds
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "must be greater than" in str(e)
    
    print("  ✓ Threshold validation tests passed")


def test_hysteresis_statistics():
    """Test hysteresis statistics tracking."""
    print("Testing hysteresis statistics...")
    
    hyst = Hysteresis(18.0, 22.0, track_history=True)
    
    # Process a sequence of values
    values = [15, 20, 23, 20, 25, 20, 17, 20, 18, 22]
    for v in values:
        hyst.update(v)
    
    stats = hyst.stats
    assert stats.total_updates == 10, f"Total updates should be 10, got {stats.total_updates}"
    assert stats.state_changes >= 2, "Should have at least 2 state changes"
    assert stats.rising_edges + stats.falling_edges == stats.state_changes
    
    # Check history
    history = hyst.history
    assert len(history) >= 2, "Should have at least 2 history entries"
    
    print("  ✓ Statistics tests passed")


def test_hysteresis_reset():
    """Test hysteresis reset functionality."""
    print("Testing hysteresis reset...")
    
    hyst = Hysteresis(18.0, 22.0)
    
    # Turn on
    hyst.update(25.0)
    assert hyst.state == True
    
    # Reset
    hyst.reset()
    assert hyst.state == False, "State should be False after reset"
    assert hyst.stats.total_updates == 0, "Stats should be reset"
    
    print("  ✓ Reset tests passed")


def test_schmitt_trigger():
    """Test Schmitt Trigger functionality."""
    print("Testing Schmitt Trigger...")
    
    # Create trigger with thresholds 0.4 and 0.6
    trigger = SchmittTrigger(low_threshold=0.4, high_threshold=0.6)
    
    # Process a sequence
    signal = [0.2, 0.5, 0.7, 0.5, 0.3, 0.5, 0.8]
    result = trigger.process(signal)
    
    # Expected: LOW until above 0.6, then HIGH until below 0.4
    expected = [False, False, True, True, False, False, True]
    assert result == expected, f"Expected {expected}, got {result}"
    
    print("  ✓ Schmitt Trigger tests passed")


def test_schmitt_trigger_inverted():
    """Test inverted Schmitt Trigger."""
    print("Testing inverted Schmitt Trigger...")
    
    trigger = SchmittTrigger(0.4, 0.6, invert=True)
    
    signal = [0.2, 0.7, 0.3]
    result = trigger.process(signal)
    
    # Inverted: HIGH when input is low, LOW when input is high
    assert result[0] == True, "First value (0.2) should be HIGH (inverted)"
    assert result[1] == False, "Second value (0.7) should be LOW (inverted)"
    
    print("  ✓ Inverted Schmitt Trigger tests passed")


def test_dead_zone():
    """Test Dead Zone functionality."""
    print("Testing Dead Zone...")
    
    # Create symmetric dead zone of size 2 centered at 0
    dz = DeadZone(size=2.0, center=0.0)
    
    # Test values
    assert dz.process(0.5) == 0.0, "0.5 should be in dead zone"
    assert dz.process(1.5) == 0.0, "1.5 should be in dead zone"
    assert dz.process(2.5) == 2.5, "2.5 should NOT be in dead zone"
    assert dz.process(-1.5) == 0.0, "-1.5 should be in dead zone"
    assert dz.process(-2.5) == -2.5, "-2.5 should NOT be in dead zone"
    
    # Check boundaries
    low, high = dz.boundaries
    assert low == -2.0, f"Low boundary should be -2.0, got {low}"
    assert high == 2.0, f"High boundary should be 2.0, got {high}"
    
    print("  ✓ Dead Zone tests passed")


def test_dead_zone_modes():
    """Test Dead Zone with different modes."""
    print("Testing Dead Zone modes...")
    
    # Positive only mode
    dz_pos = DeadZone(size=2.0, center=0.0, mode="positive_only")
    assert dz_pos.process(1.5) == 0.0, "1.5 in positive dead zone"
    assert dz_pos.process(-1.5) == -1.5, "-1.5 NOT in positive dead zone"
    
    # Negative only mode
    dz_neg = DeadZone(size=2.0, center=0.0, mode="negative_only")
    assert dz_neg.process(1.5) == 1.5, "1.5 NOT in negative dead zone"
    assert dz_neg.process(-1.5) == 0.0, "-1.5 in negative dead zone"
    
    print("  ✓ Dead Zone mode tests passed")


def test_hysteresis_filter():
    """Test Hysteresis Filter functionality."""
    print("Testing Hysteresis Filter...")
    
    filter = HysteresisFilter(threshold=1.0)
    
    # Process a sequence
    values = [10.0, 10.5, 11.0, 11.5, 12.5, 10.0]
    result = filter.filter(values)
    
    # With threshold 1.0, output should only change when diff >= 1.0
    # First value: 10.0 (output = 10.0)
    # Then: stays at 10.0 until change >= 1.0
    # At 12.5: diff from 10.0 is 2.5 >= 1.0, so output changes
    # At 10.0: diff from previous output is >= 1.0, changes back
    
    assert result[0] == 10.0, "First output should be 10.0"
    assert result[4] == 12.5, "Should change at 12.5"
    
    print("  ✓ Hysteresis Filter tests passed")


def test_multi_level_hysteresis():
    """Test Multi-Level Hysteresis functionality."""
    print("Testing Multi-Level Hysteresis...")
    
    # Create 4-level hysteresis (thresholds at 20, 40, 60)
    mh = MultiLevelHysteresis(
        thresholds=[20, 40, 60],
        hysteresis=5
    )
    
    assert mh.num_levels == 4, "Should have 4 levels"
    
    # Process values
    assert mh.update(10) == 0, "10 should be level 0"
    assert mh.update(25) == 1, "25 should be level 1"
    assert mh.update(50) == 2, "50 should be level 2"
    assert mh.update(70) == 3, "70 should be level 3"
    
    # Test hysteresis effect - going back down
    # With hysteresis 5, to drop from level 3 to level 2, value must be below (60 - 5) = 55
    mh.update(70)  # Start at level 3
    assert mh.update(55) == 3, "55 with hysteresis stays level 3 (need < 55)"
    assert mh.update(53) == 2, "53 drops to level 2 (below 55)"
    
    print("  ✓ Multi-Level Hysteresis tests passed")


def test_state_machine():
    """Test Hysteresis State Machine functionality."""
    print("Testing Hysteresis State Machine...")
    
    sm = HysteresisStateMachine()
    
    # Add states for a temperature system with clearer boundaries
    # Cold: below 15 (enter when <15, exit when >18)
    # Comfortable: between 18 and 25 (enter when in range 18-25)
    # Hot: above 25 (enter when >25, exit when <22)
    sm.add_state("cold", enter_below=16, exit_above=18)
    sm.add_state("comfortable", enter_above=18, enter_below=25, exit_above=28, exit_below=16)
    sm.add_state("hot", enter_above=25, exit_below=22)
    
    # Process temperature sequence
    temps = [10, 20, 30, 24, 15, 10]
    results = [sm.update(t) for t in temps]
    
    assert results[0] == "cold", "10°C should be cold"
    assert results[1] == "comfortable", "20°C should be comfortable"
    assert results[2] == "hot", "30°C should be hot"
    assert results[3] == "hot", "24°C stays hot (hysteresis: exit_below=22)"
    assert results[4] == "cold", "15°C should be cold (<16)"
    assert results[5] == "cold", "10°C should stay cold"
    
    print("  ✓ State Machine tests passed")


def test_create_thermostat():
    """Test thermostat creation utility."""
    print("Testing create_thermostat...")
    
    # Create thermostat: turn on at 18°C, off at 22°C
    thermostat = create_thermostat(heat_on=18.0, heat_off=22.0)
    
    # Temperature below 18 - heating should be ON
    assert thermostat.update(17.0) == True, "Heating should be ON at 17°C"
    
    # Temperature above 22 - heating should be OFF
    assert thermostat.update(23.0) == False, "Heating should be OFF at 23°C"
    
    print("  ✓ Thermostat tests passed")


def test_create_alarm():
    """Test alarm creation utility."""
    print("Testing create_alarm...")
    
    # Create alarm: trigger at 80, reset at 60
    alarm = create_alarm(trigger_threshold=80.0, reset_threshold=60.0)
    
    # Below 80 - not triggered
    assert alarm.update(70.0) == False, "Alarm should be OFF at 70"
    
    # Above 80 - triggered
    assert alarm.update(85.0) == True, "Alarm should be ON at 85"
    
    # Between 60 and 80 - stays triggered
    assert alarm.update(70.0) == True, "Alarm stays ON at 70 (between thresholds)"
    
    # Below 60 - reset
    assert alarm.update(55.0) == False, "Alarm should be OFF at 55"
    
    print("  ✓ Alarm tests passed")


def test_debounce_signal():
    """Test signal debouncing utility."""
    print("Testing debounce_signal...")
    
    # Create noisy signal
    signal = [10.0, 10.1, 10.2, 10.1, 10.3, 12.0, 12.1, 12.0, 11.9, 10.5]
    
    # Apply debouncing with threshold 1.0
    debounced = debounce_signal(signal, threshold=1.0)
    
    # First value should be preserved
    assert debounced[0] == 10.0
    
    # Check that values change only when threshold exceeded
    changes = 0
    for i in range(1, len(debounced)):
        if debounced[i] != debounced[i-1]:
            changes += 1
    
    # Should have fewer changes than original signal
    original_changes = sum(1 for i in range(1, len(signal)) if signal[i] != signal[i-1])
    assert changes <= original_changes
    
    print("  ✓ Debounce tests passed")


def test_detect_edges_with_hysteresis():
    """Test edge detection with hysteresis."""
    print("Testing detect_edges_with_hysteresis...")
    
    # Create signal with potential edges
    signal = [10, 15, 20, 25, 30, 25, 20, 15, 10, 15, 20]
    
    # Detect edges with thresholds 18 and 22
    edges = detect_edges_with_hysteresis(signal, low_threshold=18.0, high_threshold=22.0)
    
    # Should detect rising and falling edges
    assert len(edges) >= 2, "Should detect at least 2 edges"
    
    # Check edge types
    rising = [e for e in edges if e[1] == "rising"]
    falling = [e for e in edges if e[1] == "falling"]
    assert len(rising) >= 1, "Should have at least one rising edge"
    assert len(falling) >= 1, "Should have at least one falling edge"
    
    print("  ✓ Edge detection tests passed")


def test_on_off_controller():
    """Test on_off_controller utility."""
    print("Testing on_off_controller...")
    
    ctrl = on_off_controller(low=100, high=200)
    
    assert ctrl.update(50) == False, "Below low should be OFF"
    assert ctrl.update(250) == True, "Above high should be ON"
    assert ctrl.update(150) == True, "Between thresholds stays ON"
    
    print("  ✓ On-off controller tests passed")


def test_repr_methods():
    """Test __repr__ methods."""
    print("Testing __repr__ methods...")
    
    hyst = Hysteresis(18.0, 22.0)
    assert "Hysteresis" in repr(hyst)
    assert "18" in repr(hyst)
    assert "22" in repr(hyst)
    
    trigger = SchmittTrigger(0.4, 0.6)
    assert "SchmittTrigger" in repr(trigger)
    
    dz = DeadZone(2.0)
    assert "DeadZone" in repr(dz)
    
    mh = MultiLevelHysteresis([20, 40, 60])
    assert "MultiLevelHysteresis" in repr(mh)
    
    print("  ✓ __repr__ tests passed")


def test_threshold_update():
    """Test dynamic threshold updates."""
    print("Testing threshold updates...")
    
    hyst = Hysteresis(18.0, 22.0)
    
    # Update thresholds
    hyst.set_thresholds(20.0, 25.0)
    
    assert hyst.low_threshold == 20.0
    assert hyst.high_threshold == 25.0
    
    # Invalid update should raise error
    try:
        hyst.set_thresholds(25.0, 20.0)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("  ✓ Threshold update tests passed")


def test_state_string():
    """Test state string representation."""
    print("Testing state string...")
    
    hyst = Hysteresis(18.0, 22.0)
    assert hyst.get_state_str() == "OFF/LOW"
    
    hyst.update(25.0)
    assert hyst.get_state_str() == "ON/HIGH"
    
    print("  ✓ State string tests passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("AllToolkit - Hysteresis Utilities Test Suite")
    print("=" * 60 + "\n")
    
    tests = [
        test_hysteresis_basic,
        test_hysteresis_initial_state,
        test_hysteresis_threshold_validation,
        test_hysteresis_statistics,
        test_hysteresis_reset,
        test_schmitt_trigger,
        test_schmitt_trigger_inverted,
        test_dead_zone,
        test_dead_zone_modes,
        test_hysteresis_filter,
        test_multi_level_hysteresis,
        test_state_machine,
        test_create_thermostat,
        test_create_alarm,
        test_debounce_signal,
        test_detect_edges_with_hysteresis,
        test_on_off_controller,
        test_repr_methods,
        test_threshold_update,
        test_state_string,
    ]
    
    failed = []
    for test in tests:
        try:
            test()
        except AssertionError as e:
            failed.append((test.__name__, str(e)))
            print(f"  ✗ FAILED: {e}")
        except Exception as e:
            failed.append((test.__name__, str(e)))
            print(f"  ✗ ERROR: {e}")
    
    print("\n" + "=" * 60)
    if failed:
        print(f"FAILED: {len(failed)} tests")
        for name, error in failed:
            print(f"  - {name}: {error}")
    else:
        print("SUCCESS: All tests passed!")
    print("=" * 60 + "\n")
    
    return len(failed) == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)