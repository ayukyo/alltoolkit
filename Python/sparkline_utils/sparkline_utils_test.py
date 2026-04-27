#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Sparkline Utilities Test Suite

Comprehensive tests for sparkline_utils module.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    sparkline,
    sparkline_braille,
    sparkline_multiline,
    bar_chart,
    horizontal_bar_chart,
    trend_indicator,
    trend_sparkline,
    delta_indicator,
    win_loss_sparkline,
    gauge,
    gauge_with_value,
    histogram,
    sparkline_stats,
    mini_chart,
    SparklineStyle,
    TREND_UP,
    TREND_DOWN,
    TREND_FLAT,
    TREND_UP_STRONG,
    TREND_DOWN_STRONG,
    _scale_value,
    _resample,
    _format_number,
)


class TestSparkline(unittest.TestCase):
    """Test basic sparkline functions."""
    
    def test_empty_data(self):
        """Test with empty data."""
        self.assertEqual(sparkline([]), '')
    
    def test_basic_sparkline(self):
        """Test basic sparkline generation."""
        data = [1, 2, 3, 4, 5, 6, 7, 8]
        result = sparkline(data)
        # Should contain sparkline characters
        self.assertTrue(len(result) == len(data))
        self.assertTrue(all(c in ' ▁▂▃▄▅▆▇█' for c in result))
    
    def test_sparkline_scaling(self):
        """Test sparkline with custom min/max."""
        data = [10, 20, 30, 40, 50]
        result = sparkline(data, min_val=0, max_val=100)
        # All values should be in lower range
        self.assertTrue(all(c in ' ▁▂▃▄' for c in result))
    
    def test_constant_data(self):
        """Test with constant values."""
        data = [5, 5, 5, 5, 5]
        result = sparkline(data)
        # Should still produce output
        self.assertEqual(len(result), len(data))
    
    def test_width_limit(self):
        """Test width limitation."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        result = sparkline(data, width=5)
        self.assertEqual(len(result), 5)
    
    def test_ascii_style(self):
        """Test ASCII style sparkline."""
        data = [1, 2, 3, 4, 5]
        result = sparkline(data, style=SparklineStyle.ASCII)
        self.assertTrue(all(c in ' .:|+*#@W█' for c in result))
    
    def test_bar_style(self):
        """Test bar style sparkline."""
        data = [1, 2, 3, 4, 5]
        result = sparkline(data, style=SparklineStyle.BAR)
        self.assertTrue(all(c in ' ▁▂▃▄▅▆▇█' for c in result))


class TestSparklineBraille(unittest.TestCase):
    """Test Braille sparkline functions."""
    
    def test_empty_data(self):
        """Test with empty data."""
        self.assertEqual(sparkline_braille([]), '')
    
    def test_basic_braille(self):
        """Test basic Braille sparkline."""
        data = [1, 2, 3, 4, 5, 6, 7, 8]
        result = sparkline_braille(data)
        # Should contain Braille characters
        self.assertTrue(len(result) > 0)
        # All characters should be in Braille range
        for c in result:
            self.assertTrue(0x2800 <= ord(c) <= 0x28FF)
    
    def test_braille_height(self):
        """Test Braille with different heights."""
        data = [1, 2, 3, 4]
        result = sparkline_braille(data, height=2)
        self.assertTrue(len(result) > 0)
    
    def test_braille_width_limit(self):
        """Test Braille width limitation."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        result = sparkline_braille(data, width=5)
        self.assertEqual(len(result), 5)


class TestSparklineMultiline(unittest.TestCase):
    """Test multi-line sparkline functions."""
    
    def test_empty_data(self):
        """Test with empty data."""
        self.assertEqual(sparkline_multiline([]), '')
    
    def test_basic_multiline(self):
        """Test basic multi-line sparkline."""
        data = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        result = sparkline_multiline(data, width=20, height=3)
        lines = result.split('\n')
        self.assertEqual(len(lines), 3)
    
    def test_multiline_with_axis(self):
        """Test multi-line sparkline with axis."""
        data = [1, 5, 10, 15, 20]
        result = sparkline_multiline(data, width=10, height=5, show_axis=True)
        lines = result.split('\n')
        # Should have axis markers
        self.assertTrue('┤' in result)
    
    def test_multiline_without_axis(self):
        """Test multi-line sparkline without axis."""
        data = [1, 5, 10, 15, 20]
        result = sparkline_multiline(data, width=10, height=3, show_axis=False)
        self.assertTrue('┤' not in result)


class TestBarChart(unittest.TestCase):
    """Test bar chart functions."""
    
    def test_empty_data(self):
        """Test with empty data."""
        self.assertEqual(bar_chart([]), '')
    
    def test_basic_bar_chart(self):
        """Test basic bar chart."""
        data = [3, 7, 2, 5, 9]
        result = bar_chart(data)
        self.assertTrue(len(result) > 0)
        self.assertTrue('█' in result)
    
    def test_bar_chart_with_labels(self):
        """Test bar chart with labels."""
        data = [3, 7, 2]
        labels = ['A', 'B', 'C']
        result = bar_chart(data, labels=labels)
        self.assertTrue('A' in result)
        self.assertTrue('B' in result)
        self.assertTrue('C' in result)
    
    def test_bar_chart_with_title(self):
        """Test bar chart with title."""
        data = [1, 2, 3]
        result = bar_chart(data, title='Test Chart')
        self.assertTrue('Test Chart' in result)
    
    def test_bar_chart_min_max(self):
        """Test bar chart with custom min/max."""
        data = [10, 20, 30]
        result = bar_chart(data, min_val=0, max_val=100)
        self.assertTrue('┤' in result)


class TestHorizontalBarChart(unittest.TestCase):
    """Test horizontal bar chart functions."""
    
    def test_empty_data(self):
        """Test with empty data."""
        self.assertEqual(horizontal_bar_chart([], []), '')
    
    def test_basic_horizontal_bar(self):
        """Test basic horizontal bar chart."""
        labels = ['A', 'B', 'C']
        data = [30, 50, 20]
        result = horizontal_bar_chart(labels, data)
        lines = result.split('\n')
        self.assertEqual(len(lines), len(labels))
    
    def test_horizontal_bar_with_title(self):
        """Test horizontal bar with title."""
        labels = ['A', 'B']
        data = [10, 20]
        result = horizontal_bar_chart(labels, data, title='Test')
        self.assertTrue('Test' in result)
    
    def test_horizontal_bar_without_values(self):
        """Test horizontal bar without value display."""
        labels = ['A', 'B']
        data = [10, 20]
        result = horizontal_bar_chart(labels, data, show_values=False)
        self.assertTrue('10' not in result)


class TestTrendIndicator(unittest.TestCase):
    """Test trend indicator functions."""
    
    def test_upward_trend(self):
        """Test upward trend."""
        data = [1, 2, 3, 4, 5]
        result = trend_indicator(data)
        # Could be TREND_UP or TREND_UP_STRONG depending on change magnitude
        self.assertTrue(result in [TREND_UP, TREND_UP_STRONG])
    
    def test_downward_trend(self):
        """Test downward trend."""
        data = [5, 4, 3, 2, 1]
        result = trend_indicator(data)
        # Could be TREND_DOWN or TREND_DOWN_STRONG depending on change magnitude
        self.assertTrue(result in [TREND_DOWN, TREND_DOWN_STRONG])
    
    def test_flat_trend(self):
        """Test flat trend."""
        data = [3, 3, 3, 3, 3]
        self.assertEqual(trend_indicator(data), TREND_FLAT)
    
    def test_strong_upward_trend(self):
        """Test strong upward trend."""
        data = [1, 10]  # 900% increase
        self.assertEqual(trend_indicator(data, threshold=0.5), TREND_UP_STRONG)
    
    def test_strong_downward_trend(self):
        """Test strong downward trend."""
        data = [10, 1]  # 90% decrease
        self.assertEqual(trend_indicator(data, threshold=0.5), TREND_DOWN_STRONG)
    
    def test_single_value(self):
        """Test with single value."""
        data = [5]
        self.assertEqual(trend_indicator(data), TREND_FLAT)
    
    def test_empty_data(self):
        """Test with empty data."""
        self.assertEqual(trend_indicator([]), TREND_FLAT)


class TestTrendSparkline(unittest.TestCase):
    """Test trend sparkline functions."""
    
    def test_basic_trend_sparkline(self):
        """Test basic trend sparkline."""
        data = [1, 2, 3, 4, 5]
        result = trend_sparkline(data)
        # Should show some upward trend indicator
        self.assertTrue(TREND_UP in result or TREND_UP_STRONG in result)
        self.assertTrue('5' in result)
    
    def test_trend_sparkline_without_value(self):
        """Test trend sparkline without value."""
        data = [1, 2, 3, 4, 5]
        result = trend_sparkline(data, show_value=False)
        self.assertTrue('5' not in result)
    
    def test_trend_sparkline_without_arrow(self):
        """Test trend sparkline without arrow."""
        data = [1, 2, 3, 4, 5]
        result = trend_sparkline(data, show_arrow=False)
        self.assertTrue(TREND_UP not in result)


class TestDeltaIndicator(unittest.TestCase):
    """Test delta indicator functions."""
    
    def test_positive_delta(self):
        """Test positive delta."""
        result = delta_indicator(100, 110)
        self.assertTrue('+10' in result)
        self.assertTrue(TREND_UP in result)
    
    def test_negative_delta(self):
        """Test negative delta."""
        result = delta_indicator(100, 90)
        self.assertTrue('-10' in result)
        self.assertTrue(TREND_DOWN in result)
    
    def test_zero_delta(self):
        """Test zero delta."""
        result = delta_indicator(100, 100)
        self.assertTrue(TREND_FLAT in result)
    
    def test_delta_without_percent(self):
        """Test delta without percentage."""
        result = delta_indicator(100, 110, show_percent=False)
        self.assertTrue('%' not in result)
    
    def test_delta_without_value(self):
        """Test delta without value."""
        result = delta_indicator(100, 110, show_value=False)
        # Should not show absolute value like "+10"
        # But should show percentage and arrow
        self.assertTrue('(+' in result or '%)' in result)


class TestWinLossSparkline(unittest.TestCase):
    """Test win/loss sparkline functions."""
    
    def test_basic_win_loss(self):
        """Test basic win/loss sparkline."""
        data = [1, 1, -1, 0, 1, -1]
        result = win_loss_sparkline(data)
        self.assertEqual(len(result), len(data))
    
    def test_all_wins(self):
        """Test all wins."""
        data = [1, 1, 1, 1]
        result = win_loss_sparkline(data)
        self.assertEqual(result, '████')
    
    def test_all_losses(self):
        """Test all losses."""
        data = [-1, -1, -1, -1]
        result = win_loss_sparkline(data)
        self.assertEqual(result, '▄▄▄▄')
    
    def test_all_draws(self):
        """Test all draws."""
        data = [0, 0, 0, 0]
        result = win_loss_sparkline(data)
        self.assertEqual(result, '────')
    
    def test_custom_chars(self):
        """Test with custom characters."""
        data = [1, -1, 0]
        result = win_loss_sparkline(data, win_char='W', loss_char='L', draw_char='D')
        self.assertEqual(result, 'WLD')


class TestGauge(unittest.TestCase):
    """Test gauge functions."""
    
    def test_basic_gauge(self):
        """Test basic gauge."""
        result = gauge(75, 100, 10)
        self.assertEqual(len(result), 10)
        self.assertTrue(result.startswith('████'))
    
    def test_full_gauge(self):
        """Test full gauge."""
        result = gauge(100, 100, 10)
        self.assertEqual(result, '██████████')
    
    def test_empty_gauge(self):
        """Test empty gauge."""
        result = gauge(0, 100, 10)
        self.assertEqual(result, '░░░░░░░░░░')
    
    def test_half_gauge(self):
        """Test half gauge."""
        result = gauge(50, 100, 10)
        # Due to rounding, could be 5 or 6 filled chars
        filled_count = result.count('█')
        self.assertTrue(filled_count >= 4 and filled_count <= 6)
    
    def test_custom_chars(self):
        """Test with custom characters."""
        result = gauge(50, 100, 4, filled_char='#', empty_char='-')
        self.assertEqual(result, '##--')


class TestGaugeWithValue(unittest.TestCase):
    """Test gauge with value functions."""
    
    def test_gauge_with_percent(self):
        """Test gauge with percentage."""
        result = gauge_with_value(75, 100, 10)
        self.assertTrue('75%' in result)
        self.assertTrue('[' in result)
        self.assertTrue(']' in result)
    
    def test_gauge_with_value_display(self):
        """Test gauge with actual value."""
        result = gauge_with_value(75, 100, 10, show_value=True)
        self.assertTrue('75/100' in result)
    
    def test_gauge_without_percent(self):
        """Test gauge without percentage."""
        result = gauge_with_value(75, 100, 10, show_percent=False)
        self.assertTrue('%' not in result)


class TestHistogram(unittest.TestCase):
    """Test histogram functions."""
    
    def test_empty_data(self):
        """Test with empty data."""
        self.assertEqual(histogram([]), '')
    
    def test_basic_histogram(self):
        """Test basic histogram."""
        data = [1, 1, 2, 2, 2, 3, 3, 4, 5]
        result = histogram(data, bins=5)
        self.assertTrue('┤' in result)
        self.assertTrue('█' in result)
    
    def test_histogram_bins(self):
        """Test histogram with different bin counts."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = histogram(data, bins=3)
        self.assertTrue(len(result) > 0)


class TestSparklineStats(unittest.TestCase):
    """Test sparkline stats functions."""
    
    def test_basic_stats(self):
        """Test basic stats."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = sparkline_stats(data)
        self.assertTrue('n=10' in result)
        self.assertTrue('min=1' in result)
        self.assertTrue('max=10' in result)
        self.assertTrue('avg' in result)
    
    def test_empty_stats(self):
        """Test with empty data."""
        self.assertEqual(sparkline_stats([]), 'no data')


class TestMiniChart(unittest.TestCase):
    """Test mini chart functions."""
    
    def test_line_chart(self):
        """Test line mini chart."""
        data = [1, 2, 3, 4, 5]
        result = mini_chart(data, 'line')
        self.assertTrue(len(result) == len(data))
    
    def test_bar_chart(self):
        """Test bar mini chart."""
        data = [1, 2, 3, 4, 5]
        result = mini_chart(data, 'bar')
        self.assertTrue(len(result) == len(data))
    
    def test_gauge_chart(self):
        """Test gauge mini chart."""
        result = mini_chart([75, 100], 'gauge')
        self.assertTrue('%' in result)
    
    def test_trend_chart(self):
        """Test trend mini chart."""
        data = [1, 2, 3, 4, 5]
        result = mini_chart(data, 'trend')
        # Should show some upward trend indicator
        self.assertTrue(TREND_UP in result or TREND_UP_STRONG in result)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_scale_value(self):
        """Test value scaling."""
        self.assertEqual(_scale_value(5, 0, 10, 0, 100), 50)
        self.assertEqual(_scale_value(0, 0, 10, 0, 100), 0)
        self.assertEqual(_scale_value(10, 0, 10, 0, 100), 100)
    
    def test_scale_value_negative(self):
        """Test scaling with negative values."""
        self.assertEqual(_scale_value(-5, -10, 0, 0, 100), 50)
    
    def test_resample(self):
        """Test resampling."""
        data = [1, 2, 3, 4, 5]
        result = _resample(data, 3)
        self.assertEqual(len(result), 3)
    
    def test_resample_expand(self):
        """Test resampling to larger size."""
        data = [1, 5]
        result = _resample(data, 5)
        self.assertEqual(len(result), 5)
        # First and last should match original
        self.assertEqual(result[0], 1)
        self.assertEqual(result[-1], 5)
    
    def test_resample_empty(self):
        """Test resampling empty data."""
        self.assertEqual(_resample([], 5), [])
    
    def test_format_number(self):
        """Test number formatting."""
        self.assertEqual(_format_number(5), '5')
        self.assertEqual(_format_number(5.0), '5')
        self.assertEqual(_format_number(5.5), '5.5')


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple functions."""
    
    def test_sparkline_with_trend(self):
        """Test sparkline combined with trend."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        line = sparkline(data)
        trend = trend_indicator(data)
        result = f"{line} {trend}"
        # Should show some upward trend indicator
        self.assertTrue(TREND_UP in result or TREND_UP_STRONG in result)
    
    def test_chart_workflow(self):
        """Test complete chart workflow."""
        data = [10, 20, 15, 30, 25, 40, 35]
        
        # Generate various representations
        line = sparkline(data)
        bars = bar_chart(data, height=5)
        h_bars = horizontal_bar_chart(['A', 'B', 'C', 'D', 'E', 'F', 'G'], data)
        stats = sparkline_stats(data)
        
        # All should have content
        self.assertTrue(len(line) > 0)
        self.assertTrue(len(bars) > 0)
        self.assertTrue(len(h_bars) > 0)
        self.assertTrue(len(stats) > 0)
    
    def test_data_visualization_pipeline(self):
        """Test data visualization pipeline."""
        # Create sample data
        raw_data = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        
        # Step 1: Quick sparkline
        quick_view = sparkline(raw_data)
        
        # Step 2: Detailed multiline
        detailed = sparkline_multiline(raw_data, width=20, height=5)
        
        # Step 3: Statistics
        stats = sparkline_stats(raw_data)
        
        # Step 4: Trend
        trend = trend_sparkline(raw_data, show_value=True, show_arrow=True)
        
        # All outputs should be valid
        self.assertTrue(len(quick_view) > 0)
        self.assertTrue(len(detailed.split('\n')) == 5)
        self.assertTrue('avg' in stats)
        # Should show some upward trend indicator
        self.assertTrue(TREND_UP in trend or TREND_UP_STRONG in trend)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)