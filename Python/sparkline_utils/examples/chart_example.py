#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sparkline Utils - Chart Examples

Chart examples for sparkline_utils module.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sparkline_utils.mod import (
    bar_chart,
    horizontal_bar_chart,
    histogram,
    gauge,
    gauge_with_value,
)


def main():
    print("=" * 60)
    print("Sparkline Utils - Chart Examples")
    print("=" * 60)
    
    # Example 1: Vertical bar chart
    print("\n1. Vertical Bar Chart - Weekly Sales")
    sales = [120, 180, 95, 210, 150, 70, 200]
    labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    print(bar_chart(sales, width=20, height=6, labels=labels, title='Weekly Sales'))
    
    # Example 2: Horizontal bar chart
    print("\n2. Horizontal Bar Chart - Department Performance")
    departments = ['Sales', 'Marketing', 'R&D', 'Support', 'HR']
    scores = [85, 72, 90, 68, 75]
    print(horizontal_bar_chart(departments, scores, width=25, title='Department Scores'))
    
    # Example 3: Gauge
    print("\n3. Gauge - Progress Indicators")
    print(f"   25%: {gauge(25, 100, 10)}")
    print(f"   50%: {gauge(50, 100, 10)}")
    print(f"   75%: {gauge(75, 100, 10)}")
    print(f"   100%: {gauge(100, 100, 10)}")
    
    # Example 4: Gauge with value
    print("\n4. Gauge with Value Display")
    print(f"   CPU: {gauge_with_value(65, 100, 20)}")
    print(f"   Memory: {gauge_with_value(8, 16, 15, show_value=True)}")
    print(f"   Disk: {gauge_with_value(450, 500, 20, show_percent=True, show_value=True)}")
    
    # Example 5: Histogram
    print("\n5. Histogram - Test Score Distribution")
    scores = [65, 72, 78, 80, 82, 85, 88, 90, 91, 92, 
              93, 95, 96, 97, 98, 75, 83, 87, 89, 94]
    print(histogram(scores, bins=5, width=20, height=6))
    
    # Example 6: Dashboard example
    print("\n6. Dashboard Simulation")
    print("-" * 40)
    
    # CPU history
    cpu_history = [20, 35, 50, 65, 75, 60, 45, 30]
    print(f"CPU Usage:    {gauge_with_value(65, 100, 15)}")
    
    # Memory
    print(f"Memory:       {gauge_with_value(78, 100, 15)}")
    
    # Network I/O
    net_in = [10, 15, 20, 25, 30, 25, 20, 15]
    net_out = [5, 8, 12, 18, 22, 18, 14, 10]
    print(f"Network In:   {gauge(25, 100, 10)} (KB/s)")
    print(f"Network Out:  {gauge(18, 100, 10)} (KB/s)")
    
    # Disk
    print(f"Disk I/O:     {gauge(40, 100, 10)} (MB/s)")
    print("-" * 40)


if __name__ == '__main__':
    main()