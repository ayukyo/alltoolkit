#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sparkline Utils - Basic Examples

Basic usage examples for sparkline_utils module.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sparkline_utils.mod import (
    sparkline,
    sparkline_braille,
    sparkline_multiline,
    SparklineStyle,
)


def main():
    print("=" * 60)
    print("Sparkline Utils - Basic Examples")
    print("=" * 60)
    
    # Example 1: Basic sparkline
    print("\n1. Basic Sparkline")
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"   Data: {data}")
    print(f"   Unicode: {sparkline(data)}")
    print(f"   ASCII:   {sparkline(data, style=SparklineStyle.ASCII)}")
    
    # Example 2: Resampling
    print("\n2. Width Resampling")
    long_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    print(f"   Original length: {len(long_data)}")
    print(f"   Limited to 8: {sparkline(long_data, width=8)}")
    
    # Example 3: Custom range
    print("\n3. Custom Range")
    data = [10, 20, 30, 40, 50]
    print(f"   Default:       {sparkline(data)}")
    print(f"   Range 0-100:   {sparkline(data, min_val=0, max_val=100)}")
    print(f"   Range 30-40:   {sparkline(data, min_val=30, max_val=40)}")
    
    # Example 4: Braille sparkline
    print("\n4. Braille High-Resolution")
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"   Unicode: {sparkline(data)}")
    print(f"   Braille: {sparkline_braille(data)}")
    
    # Example 5: Multi-line chart
    print("\n5. Multi-Line Chart")
    data = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45]
    print(sparkline_multiline(data, width=15, height=4))
    
    # Example 6: Negative values
    print("\n6. Negative Values")
    data = [-5, -2, 0, 3, 7, 10, 8, 4, 1, -3]
    print(f"   {sparkline(data)}")
    
    # Example 7: Constant values
    print("\n7. Constant Values")
    data = [5, 5, 5, 5, 5, 5]
    print(f"   All same: {sparkline(data)}")


if __name__ == '__main__':
    main()