#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Terminal Progress Utils Examples

Usage:
    python examples.py [example_name]

Examples:
    python examples.py progress_bar    # Basic progress bar
    python examples.py spinner        # Spinner animation
    python examples.py table          # Table display
    python examples.py multi_step     # Multi-step progress
    python examples.py status         # Status indicators
    python examples.py all            # Run all examples
"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

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
)


def example_progress_bar():
    """Progress bar example"""
    print("\n" + "=" * 50)
    print("Example: Progress Bar")
    print("=" * 50)
    
    print("\nBasic progress bar:")
    bar = ProgressBar(total=100, width=30, prefix="Downloading")
    for i in range(101):
        bar.update(i)
        time.sleep(0.02)
    bar.finish()
    
    print("\nArrow style:")
    bar2 = ProgressBar(total=50, width=25, style=ProgressStyle.ARROW, show_percent=False)
    for i in range(51):
        bar2.update(i)
        time.sleep(0.03)
    bar2.finish()
    
    print("\n✓ Done!")


def example_spinner():
    """Spinner example"""
    print("\n" + "=" * 50)
    print("Example: Spinner")
    print("=" * 50)
    
    print("\nDot spinner:")
    spinner = Spinner(message="Processing data", style=SpinnerStyle.DOTS)
    spinner.start()
    time.sleep(2)
    spinner.stop(message="Data processed!")
    
    print("\nLine spinner:")
    spinner2 = Spinner(message="Loading", style=SpinnerStyle.LINE)
    spinner2.start()
    time.sleep(2)
    spinner2.stop(message="Loaded!")
    
    print("\n✓ Done!")


def example_table():
    """Table example"""
    print("\n" + "=" * 50)
    print("Example: Table Display")
    print("=" * 50)
    
    table = Table(
        headers=["Rank", "Name", "Score", "Grade"],
        alignments=[TableAlign.LEFT, TableAlign.LEFT, TableAlign.RIGHT, TableAlign.CENTER]
    )
    
    students = [
        ["1", "Alice Johnson", "98", "A+"],
        ["2", "Bob Smith", "85", "B"],
        ["3", "Carol White", "72", "C"],
        ["4", "David Brown", "91", "A"],
        ["5", "Eve Davis", "68", "D"],
    ]
    
    for row in students:
        table.add_row(row)
    
    print("\nStudent Results Table:")
    print(table.render())
    
    print("\n✓ Done!")


def example_multi_step():
    """Multi-step progress example"""
    print("\n" + "=" * 50)
    print("Example: Multi-Step Progress")
    print("=" * 50)
    
    steps = MultiStepProgress(["Download", "Extract", "Install", "Configure"], width=25)
    
    print("\nSimulating installation process:")
    steps.start()
    
    # Step 1: Download
    for i in range(101):
        steps.update(0, i)
        time.sleep(0.02)
    
    # Step 2: Extract
    steps.next_step()
    for i in range(101):
        steps.update(1, i)
        time.sleep(0.015)
    
    # Step 3: Install
    steps.next_step()
    for i in range(101):
        steps.update(2, i)
        time.sleep(0.02)
    
    # Step 4: Configure
    steps.next_step()
    for i in range(101):
        steps.update(3, i)
        time.sleep(0.01)
    
    steps.finish("Installation complete!")
    
    print("\n✓ Done!")


def example_status():
    """Status indicator example"""
    print("\n" + "=" * 50)
    print("Example: Status Indicators")
    print("=" * 50)
    
    indicator = StatusIndicator(width=50)
    
    states = [
        ("Initializing", "pending"),
        ("Loading configuration", "active"),
        ("Validating input", "active"),
        ("Processing request", "active"),
        ("Complete", "success"),
    ]
    
    print("\nTask states:")
    for label, status in states:
        indicator.show(label, status)
        time.sleep(0.5)
    
    print("\n\nError state:")
    error_indicator = StatusIndicator()
    error_indicator.show("Connection failed", "error")
    
    print("\n✓ Done!")


def example_live_value():
    """Live value display example"""
    print("\n" + "=" * 50)
    print("Example: Live Value Display")
    print("=" * 50)
    
    live = LiveValue(prefix="[PROGRESS] ", suffix="")
    
    print("\nSimulating live updates:")
    for i in range(101):
        live.update(f"Processing iteration {i}", f"{i}%")
        time.sleep(0.03)
    
    live.clear()
    print("Cleared!")
    
    print("\n✓ Done!")


def example_counter():
    """Counter example"""
    print("\n" + "=" * 50)
    print("Example: Animated Counter")
    print("=" * 50)
    
    print("\nCounter with decimals:")
    counter = Counter(prefix="Value: ", decimals=2)
    for i in range(0, 101, 5):
        counter.show(i / 10)
        time.sleep(0.1)
    
    print("\n\nInteger counter:")
    counter2 = Counter(suffix=" iterations")
    for i in range(50):
        counter2.show(i)
        time.sleep(0.05)
    
    print("\n✓ Done!")


def example_utilities():
    """Utility functions example"""
    print("\n" + "=" * 50)
    print("Example: Utility Functions")
    print("=" * 50)
    
    print("\nprogress_bar() output:")
    for pct in [0, 25, 50, 75, 100]:
        print(progress_bar(pct, 100, width=25), end="\r")
        time.sleep(0.3)
    print()
    
    print("\nloading_spinner() output:")
    for _ in range(20):
        print(loading_spinner("Loading..."), end="\r")
        time.sleep(0.1)
    print()
    
    print("\nstatus_bar() outputs:")
    print(status_bar("Task pending", "pending"))
    print(status_bar("Task in progress", "active"))
    print(status_bar("Task succeeded", "success"))
    print(status_bar("Task failed", "error"))
    print(status_bar("Warning message", "warning"))
    
    print("\n✓ Done!")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        example_name = sys.argv[1].lower()
        
        examples = {
            "progress_bar": example_progress_bar,
            "spinner": example_spinner,
            "table": example_table,
            "multi_step": example_multi_step,
            "status": example_status,
            "live_value": example_live_value,
            "counter": example_counter,
            "utilities": example_utilities,
            "all": lambda: [example_progress_bar(), example_spinner(), example_table(), 
                           example_multi_step(), example_status(), example_live_value(),
                           example_counter(), example_utilities()],
        }
        
        if example_name in examples:
            examples[example_name]()
        else:
            print(f"Unknown example: {example_name}")
            print("Available: " + ", ".join(examples.keys()))
            sys.exit(1)
    else:
        print(__doc__)
        print("\nRunning all examples (use Ctrl+C to stop)...\n")
        time.sleep(1)
        example_progress_bar()
        example_spinner()
        example_table()
        example_multi_step()
        example_status()
        example_live_value()
        example_counter()
        example_utilities()
        print("\n" + "=" * 50)
        print("All examples completed!")
        print("=" * 50)


if __name__ == "__main__":
    main()