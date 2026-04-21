#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sparkline Utils - Trend Examples

Trend indicator examples for sparkline_utils module.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sparkline_utils.mod import (
    trend_indicator,
    trend_sparkline,
    delta_indicator,
    win_loss_sparkline,
    sparkline_stats,
    TREND_UP,
    TREND_DOWN,
    TREND_FLAT,
)


def main():
    print("=" * 60)
    print("Sparkline Utils - Trend Examples")
    print("=" * 60)
    
    # Example 1: Trend indicators
    print("\n1. Trend Indicator Arrows")
    
    upward = [1, 2, 3, 4, 5, 6, 7, 8]
    print(f"   Upward trend: {trend_indicator(upward)} (expected: ↑)")
    
    downward = [8, 7, 6, 5, 4, 3, 2, 1]
    print(f"   Downward trend: {trend_indicator(downward)} (expected: ↓)")
    
    flat = [5, 5, 5, 5, 5]
    print(f"   Flat trend: {trend_indicator(flat)} (expected: →)")
    
    volatile = [1, 10, 1, 10]
    print(f"   Volatile: {trend_indicator(volatile)}")
    
    # Example 2: Trend sparkline
    print("\n2. Trend Sparkline (with value and arrow)")
    
    prices = [100, 102, 105, 108, 110, 115, 120]
    print(f"   Prices: {trend_sparkline(prices)}")
    
    costs = [50, 48, 45, 43, 40, 38, 35]
    print(f"   Costs:  {trend_sparkline(costs)}")
    
    stable = [75, 75, 75, 75, 75]
    print(f"   Stable: {trend_sparkline(stable)}")
    
    # Example 3: Delta indicator
    print("\n3. Delta Change Indicators")
    
    print(f"   +10 from 100: {delta_indicator(100, 110)}")
    print(f"   -10 from 100: {delta_indicator(100, 90)}")
    print(f"   +50 from 50:  {delta_indicator(50, 100)}")
    print(f"   No change:    {delta_indicator(100, 100)}")
    
    # Example 4: Win/Loss sparkline
    print("\n4. Win/Loss Visualization")
    
    results = [1, 1, 1, -1, 1, 0, 1, -1, 1, 1]
    print(f"   Game results: {win_loss_sparkline(results)}")
    print(f"   Legend: █=Win ▄=Loss ─=Draw")
    
    wins = [1, 1, 1, 1, 1, 1]
    print(f"   All wins:     {win_loss_sparkline(wins)}")
    
    losses = [-1, -1, -1, -1]
    print(f"   All losses:   {win_loss_sparkline(losses)}")
    
    draws = [0, 0, 0, 0]
    print(f"   All draws:    {win_loss_sparkline(draws)}")
    
    # Example 5: Statistics summary
    print("\n5. Statistics Summary with Sparkline")
    
    data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    print(f"   {sparkline_stats(data)}")
    
    small = [5, 10, 15]
    print(f"   {sparkline_stats(small)}")
    
    # Example 6: Stock market simulation
    print("\n6. Stock Market Dashboard")
    print("-" * 50)
    
    stocks = {
        'AAPL': [150, 155, 160, 158, 162, 165, 170],
        'GOOG': [120, 118, 122, 125, 128, 130, 127],
        'MSFT': [300, 305, 308, 312, 315, 318, 320],
        'AMZN': [80, 78, 76, 75, 77, 79, 82],
    }
    
    for symbol, prices in stocks.items():
        change = delta_indicator(prices[0], prices[-1], show_percent=True)
        print(f"   {symbol}: {trend_sparkline(prices, width=8)} | {change}")
    
    print("-" * 50)
    
    # Example 7: Performance monitoring
    print("\n7. Performance Monitoring")
    
    response_times = [50, 55, 60, 45, 40, 35, 30, 28]
    print(f"   Response Time: {trend_sparkline(response_times)} ms")
    
    error_rates = [0.5, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01, 0]
    print(f"   Error Rate:    {sparkline_stats(error_rates)}")


if __name__ == '__main__':
    main()