#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Terminal Progress Utils Tests"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from mod import (
    ProgressBar,
    Spinner,
    StatusIndicator,
    Table,
    MultiStepProgress,
    LiveValue,
    Counter,
    progress_bar,
    loading_spinner,
    status_bar,
    ProgressStyle,
    SpinnerStyle,
    TableAlign,
)


def test_progress_bar():
    """Test ProgressBar class"""
    print("\n=== Test ProgressBar ===")
    
    # Simulate progress (not actual terminal rendering)
    bar = ProgressBar(total=100, width=20, show_percent=True, show_count=True)
    
    # Test progress calculation
    results = []
    for i in range(0, 101, 25):
        bar.update(i)
        results.append((i, i / 100))
    
    assert bar.current == 100
    assert bar.total == 100
    print("✓ ProgressBar update works correctly")
    
    # Test increment
    bar2 = ProgressBar(total=10)
    bar2.increment(3)
    assert bar2.current == 3
    bar2.increment(2)
    assert bar2.current == 5
    print("✓ ProgressBar increment works correctly")
    
    return True


def test_spinner():
    """Test Spinner class"""
    print("\n=== Test Spinner ===")
    
    spinner = Spinner(message="Testing", style=SpinnerStyle.LINE)
    assert spinner.message == "Testing"
    assert spinner.style == SpinnerStyle.LINE
    assert not spinner._running
    print("✓ Spinner initialization works correctly")
    
    # Test start/stop (quick test, no actual delay)
    spinner.start()
    assert spinner._running
    spinner.stop(message="Done")
    assert not spinner._running
    print("✓ Spinner start/stop works correctly")
    
    return True


def test_status_indicator():
    """Test StatusIndicator class"""
    print("\n=== Test StatusIndicator ===")
    
    status = StatusIndicator(width=40)
    status.show("Test task", "pending")
    status.show("Running", "active")
    status.show("Complete", "success")
    status.show("Failed", "error")
    status.show("Warning", "warning")
    
    assert "pending" in StatusIndicator.STATUS_SYMBOLS
    assert "success" in StatusIndicator.STATUS_SYMBOLS
    assert "error" in StatusIndicator.STATUS_SYMBOLS
    print("✓ StatusIndicator works correctly")
    
    return True


def test_table():
    """Test Table class"""
    print("\n=== Test Table ===")
    
    table = Table(headers=["Name", "Score", "Status"])
    table.add_row(["Alice", "95", "Pass"])
    table.add_row(["Bob", "78", "Pass"])
    table.add_row(["Charlie", "55", "Fail"])
    
    output = table.render()
    assert "Name" in output
    assert "Alice" in output
    assert "Charlie" in output
    print("✓ Table rendering works correctly")
    
    # Test with alignments
    table2 = Table(headers=["Rank", "Name"], alignments=[TableAlign.RIGHT, TableAlign.LEFT])
    table2.add_row(["1", "Alice"])
    table2.add_row(["10", "Bob"])
    output2 = table2.render()
    assert "1" in output2
    print("✓ Table with alignments works correctly")
    
    return True


def test_multi_step_progress():
    """Test MultiStepProgress class"""
    print("\n=== Test MultiStepProgress ===")
    
    steps = MultiStepProgress(["Step A", "Step B", "Step C"], width=15)
    assert len(steps.step_names) == 3
    assert steps.current_step == 0
    
    steps.update(0, 50)
    assert steps.step_progress[0] == 50
    
    steps.next_step()
    assert steps.current_step == 1
    assert steps.step_progress[0] == 100
    
    steps.finish("All done")
    print("✓ MultiStepProgress works correctly")
    
    return True


def test_live_value():
    """Test LiveValue class"""
    print("\n=== Test LiveValue ===")
    
    live = LiveValue(prefix="[", suffix="]")
    live.update("Value", 42)
    live.update("Count", 100)
    live.clear()
    
    print("✓ LiveValue works correctly")
    return True


def test_counter():
    """Test Counter class"""
    print("\n=== Test Counter ===")
    
    counter = Counter(prefix="Count: ", decimals=2)
    counter.show(10.5)
    counter.show(25.75)
    
    counter2 = Counter(prefix="", suffix=" items")
    counter2.show(100)
    
    print("✓ Counter works correctly")
    return True


def test_utility_functions():
    """Test utility functions"""
    print("\n=== Test Utility Functions ===")
    
    # Test progress_bar
    bar_str = progress_bar(50, 100, width=20)
    assert "[" in bar_str
    assert "50.0%" in bar_str
    print("✓ progress_bar() works correctly")
    
    # Test loading_spinner
    spinner_str = loading_spinner("Test", SpinnerStyle.DOTS)
    assert "Test" in spinner_str
    print("✓ loading_spinner() works correctly")
    
    # Test status_bar
    status_str = status_bar("Task complete", "success", width=40)
    assert "Task complete" in status_str
    print("✓ status_bar() works correctly")
    
    return True


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("Running Terminal Progress Utils Tests")
    print("=" * 50)
    
    tests = [
        test_progress_bar,
        test_spinner,
        test_status_indicator,
        test_table,
        test_multi_step_progress,
        test_live_value,
        test_counter,
        test_utility_functions,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)