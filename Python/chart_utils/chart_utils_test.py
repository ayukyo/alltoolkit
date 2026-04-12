#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Chart Utilities Test Suite

Comprehensive tests for chart_utils module.
Tests cover all chart types, edge cases, and utilities.

Author: AllToolkit
License: MIT
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    ChartConfig, DataSeries, Point, SVGBuilder,
    parse_color, lighten_color, darken_color,
    calculate_min_max, interpolate,
    line_chart, bar_chart, pie_chart, scatter_plot, area_chart,
    save_svg, svg_to_data_uri, create_sample_data,
    DEFAULT_COLORS
)


# =============================================================================
# Test Results Tracking
# =============================================================================

class TestResults:
    """Track test results."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def record(self, name: str, passed: bool, error: str = ""):
        if passed:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            self.errors.append((name, error))
            print(f"  ✗ {name}: {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Results: {self.passed}/{total} passed")
        if self.errors:
            print(f"\nFailed tests:")
            for name, error in self.errors:
                print(f"  - {name}: {error}")
        print(f"{'='*60}")
        return self.failed == 0


results = TestResults()


# =============================================================================
# Helper Functions
# =============================================================================

def assert_true(condition: bool, msg: str = ""):
    if not condition:
        raise AssertionError(msg or "Assertion failed")


def assert_equal(actual, expected, msg: str = ""):
    if actual != expected:
        raise AssertionError(msg or f"Expected {expected}, got {actual}")


def assert_contains(haystack: str, needle: str, msg: str = ""):
    if needle not in haystack:
        raise AssertionError(msg or f"'{needle}' not found in '{haystack}'")


def assert_svg_valid(svg: str):
    """Basic SVG validation."""
    assert_true(svg.startswith('<?xml'), "SVG should start with XML declaration")
    assert_true('<svg' in svg, "SVG should contain svg element")
    assert_true('</svg>' in svg, "SVG should close properly")


# =============================================================================
# Color Utility Tests
# =============================================================================

def test_parse_color():
    """Test color parsing."""
    assert_equal(parse_color("#FF5733"), "#FF5733")
    assert_equal(parse_color(""), DEFAULT_COLORS[0])
    assert_equal(parse_color("red"), "red")
    results.record("parse_color", True)


def test_lighten_color():
    """Test color lightening."""
    lightened = lighten_color("#000000", 0.5)
    assert_true(lightened.startswith("#"), "Should return hex color")
    results.record("lighten_color", True)


def test_darken_color():
    """Test color darkening."""
    darkened = darken_color("#FFFFFF", 0.5)
    assert_true(darkened.startswith("#"), "Should return hex color")
    results.record("darken_color", True)


# =============================================================================
# Math Utility Tests
# =============================================================================

def test_calculate_min_max():
    """Test min/max calculation with padding."""
    data = [10, 20, 30, 40, 50]
    min_val, max_val = calculate_min_max(data)
    assert_true(min_val < 10, "Min should be padded")
    assert_true(max_val > 50, "Max should be padded")
    results.record("calculate_min_max", True)


def test_calculate_min_max_empty():
    """Test min/max with empty data."""
    min_val, max_val = calculate_min_max([])
    assert_equal(min_val, 0)
    assert_equal(max_val, 1)
    results.record("calculate_min_max_empty", True)


def test_calculate_min_max_single():
    """Test min/max with single value."""
    min_val, max_val = calculate_min_max([42])
    assert_equal(min_val, 41)
    assert_equal(max_val, 43)
    results.record("calculate_min_max_single", True)


def test_interpolate():
    """Test linear interpolation."""
    assert_equal(interpolate(0, 100, 0.5), 50)
    assert_equal(interpolate(10, 20, 0.25), 12.5)
    assert_equal(interpolate(0, 100, 0), 0)
    assert_equal(interpolate(0, 100, 1), 100)
    results.record("interpolate", True)


# =============================================================================
# SVG Builder Tests
# =============================================================================

def test_svg_builder_rect():
    """Test SVG rectangle generation."""
    svg = SVGBuilder(400, 300)
    svg.rect(10, 10, 100, 50, fill="red")
    content = svg.build()
    assert_contains(content, '<rect')
    assert_contains(content, 'fill="red"')
    results.record("svg_builder_rect", True)


def test_svg_builder_circle():
    """Test SVG circle generation."""
    svg = SVGBuilder(400, 300)
    svg.circle(50, 50, 20, fill="blue")
    content = svg.build()
    assert_contains(content, '<circle')
    assert_contains(content, 'fill="blue"')
    results.record("svg_builder_circle", True)


def test_svg_builder_line():
    """Test SVG line generation."""
    svg = SVGBuilder(400, 300)
    svg.line(0, 0, 100, 100, stroke="green")
    content = svg.build()
    assert_contains(content, '<line')
    assert_contains(content, 'stroke="green"')
    results.record("svg_builder_line", True)


def test_svg_builder_polyline():
    """Test SVG polyline generation."""
    svg = SVGBuilder(400, 300)
    svg.polyline([(0, 0), (50, 50), (100, 0)], stroke="purple")
    content = svg.build()
    assert_contains(content, '<polyline')
    assert_contains(content, 'points="0,0 50,50 100,0"')
    results.record("svg_builder_polyline", True)


def test_svg_builder_text():
    """Test SVG text generation."""
    svg = SVGBuilder(400, 300)
    svg.text(100, 50, "Hello", font_size=16)
    content = svg.build()
    assert_contains(content, '<text')
    assert_contains(content, 'Hello')
    results.record("svg_builder_text", True)


def test_svg_builder_path():
    """Test SVG path generation."""
    svg = SVGBuilder(400, 300)
    svg.path("M 0 0 L 100 100", fill="orange")
    content = svg.build()
    assert_contains(content, '<path')
    assert_contains(content, 'd="M 0 0 L 100 100"')
    results.record("svg_builder_path", True)


def test_svg_builder_complete():
    """Test complete SVG document generation."""
    svg = SVGBuilder(800, 600)
    svg.rect(0, 0, 800, 600, fill="white")
    content = svg.build("Test Chart")
    assert_svg_valid(content)
    assert_contains(content, 'width="800"')
    assert_contains(content, 'height="600"')
    assert_contains(content, '<title>Test Chart</title>')
    results.record("svg_builder_complete", True)


# =============================================================================
# Data Series Tests
# =============================================================================

def test_data_series_creation():
    """Test DataSeries creation."""
    series = DataSeries(name="Test", data=[1, 2, 3, 4, 5])
    assert_equal(series.name, "Test")
    assert_equal(series.data, [1, 2, 3, 4, 5])
    results.record("data_series_creation", True)


def test_data_series_with_color():
    """Test DataSeries with custom color."""
    series = DataSeries(name="Test", data=[1, 2, 3], color="#FF0000")
    assert_equal(series.color, "#FF0000")
    results.record("data_series_with_color", True)


def test_data_series_with_labels():
    """Test DataSeries with labels."""
    series = DataSeries(name="Test", data=[1, 2, 3], labels=["A", "B", "C"])
    assert_equal(series.labels, ["A", "B", "C"])
    results.record("data_series_with_labels", True)


# =============================================================================
# Chart Config Tests
# =============================================================================

def test_chart_config_defaults():
    """Test ChartConfig default values."""
    config = ChartConfig()
    assert_equal(config.width, 800)
    assert_equal(config.height, 600)
    assert_equal(config.show_grid, True)
    assert_equal(config.show_legend, True)
    results.record("chart_config_defaults", True)


def test_chart_config_custom():
    """Test ChartConfig with custom values."""
    config = ChartConfig(width=1000, height=800, show_grid=False)
    assert_equal(config.width, 1000)
    assert_equal(config.height, 800)
    assert_equal(config.show_grid, False)
    results.record("chart_config_custom", True)


# =============================================================================
# Line Chart Tests
# =============================================================================

def test_line_chart_basic():
    """Test basic line chart generation."""
    data = [DataSeries(name="Sales", data=[10, 20, 30, 40, 50])]
    svg = line_chart(data, title="Sales Chart")
    assert_svg_valid(svg)
    assert_contains(svg, "Sales Chart")
    results.record("line_chart_basic", True)


def test_line_chart_multiple_series():
    """Test line chart with multiple data series."""
    data = [
        DataSeries(name="2025", data=[10, 20, 30, 40, 50]),
        DataSeries(name="2026", data=[15, 25, 35, 45, 55])
    ]
    svg = line_chart(data, title="Comparison")
    assert_svg_valid(svg)
    assert_contains(svg, "2025")
    assert_contains(svg, "2026")
    results.record("line_chart_multiple_series", True)


def test_line_chart_with_labels():
    """Test line chart with x-axis labels."""
    data = [DataSeries(name="Sales", data=[10, 20, 30])]
    svg = line_chart(data, x_labels=["Jan", "Feb", "Mar"])
    assert_contains(svg, "Jan")
    assert_contains(svg, "Feb")
    assert_contains(svg, "Mar")
    results.record("line_chart_with_labels", True)


def test_line_chart_no_grid():
    """Test line chart without grid."""
    config = ChartConfig(show_grid=False)
    data = [DataSeries(name="Test", data=[1, 2, 3])]
    svg = line_chart(data, config=config)
    assert_svg_valid(svg)
    results.record("line_chart_no_grid", True)


def test_line_chart_no_legend():
    """Test line chart without legend."""
    config = ChartConfig(show_legend=False)
    data = [DataSeries(name="Test", data=[1, 2, 3])]
    svg = line_chart(data, config=config)
    assert_svg_valid(svg)
    results.record("line_chart_no_legend", True)


# =============================================================================
# Bar Chart Tests
# =============================================================================

def test_bar_chart_basic():
    """Test basic bar chart generation."""
    data = [DataSeries(name="Values", data=[10, 20, 30, 40])]
    svg = bar_chart(data, title="Bar Chart")
    assert_svg_valid(svg)
    assert_contains(svg, '<rect')
    results.record("bar_chart_basic", True)


def test_bar_chart_multiple_series():
    """Test bar chart with grouped bars."""
    data = [
        DataSeries(name="Q1", data=[10, 20, 30]),
        DataSeries(name="Q2", data=[15, 25, 35])
    ]
    svg = bar_chart(data, title="Quarterly")
    assert_svg_valid(svg)
    assert_contains(svg, "Q1")
    assert_contains(svg, "Q2")
    results.record("bar_chart_multiple_series", True)


def test_bar_chart_horizontal():
    """Test horizontal bar chart."""
    data = [DataSeries(name="Values", data=[10, 20, 30])]
    svg = bar_chart(data, horizontal=True)
    assert_svg_valid(svg)
    results.record("bar_chart_horizontal", True)


def test_bar_chart_with_labels():
    """Test bar chart with x-axis labels."""
    data = [DataSeries(name="Values", data=[10, 20, 30])]
    svg = bar_chart(data, x_labels=["A", "B", "C"])
    assert_contains(svg, "A")
    assert_contains(svg, "B")
    assert_contains(svg, "C")
    results.record("bar_chart_with_labels", True)


# =============================================================================
# Pie Chart Tests
# =============================================================================

def test_pie_chart_basic():
    """Test basic pie chart generation."""
    data = [DataSeries(name="Categories", data=[30, 40, 30])]
    svg = pie_chart(data, title="Distribution")
    assert_svg_valid(svg)
    assert_contains(svg, '<path')
    results.record("pie_chart_basic", True)


def test_pie_chart_with_percentages():
    """Test pie chart with percentage labels."""
    data = [DataSeries(name="Categories", data=[25, 25, 25, 25])]
    svg = pie_chart(data, show_percentages=True)
    assert_contains(svg, "25.0%")
    results.record("pie_chart_with_percentages", True)


def test_pie_chart_with_labels():
    """Test pie chart with custom labels."""
    data = [DataSeries(name="Categories", data=[30, 40, 30],
                      labels=["A", "B", "C"])]
    svg = pie_chart(data, show_labels=True)
    assert_contains(svg, "A")
    assert_contains(svg, "B")
    assert_contains(svg, "C")
    results.record("pie_chart_with_labels", True)


def test_pie_chart_explode():
    """Test pie chart with exploded slices."""
    data = [DataSeries(name="Categories", data=[30, 40, 30])]
    svg = pie_chart(data, explode=[0, 0.1, 0])
    assert_svg_valid(svg)
    results.record("pie_chart_explode", True)


def test_pie_chart_no_legend():
    """Test pie chart without legend."""
    config = ChartConfig(show_legend=False)
    data = [DataSeries(name="Categories", data=[30, 40, 30])]
    svg = pie_chart(data, config=config)
    assert_svg_valid(svg)
    results.record("pie_chart_no_legend", True)


# =============================================================================
# Scatter Plot Tests
# =============================================================================

def test_scatter_plot_basic():
    """Test basic scatter plot generation."""
    x_data = [1, 2, 3, 4, 5]
    y_data = [2, 4, 6, 8, 10]
    svg = scatter_plot(x_data, y_data, title="Scatter")
    assert_svg_valid(svg)
    assert_contains(svg, '<circle')
    results.record("scatter_plot_basic", True)


def test_scatter_plot_with_trend():
    """Test scatter plot with trend line."""
    x_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y_data = [2.1, 3.9, 6.2, 7.8, 10.1, 12.0, 14.2, 15.9, 18.1, 20.0]
    svg = scatter_plot(x_data, y_data, trend_line=True)
    assert_svg_valid(svg)
    assert_contains(svg, '<line')
    results.record("scatter_plot_with_trend", True)


def test_scatter_plot_with_labels():
    """Test scatter plot with point labels."""
    x_data = [1, 2, 3]
    y_data = [2, 4, 6]
    labels = ["A", "B", "C"]
    svg = scatter_plot(x_data, y_data, point_labels=labels)
    assert_contains(svg, "A")
    assert_contains(svg, "B")
    assert_contains(svg, "C")
    results.record("scatter_plot_with_labels", True)


def test_scatter_plot_with_axis_labels():
    """Test scatter plot with axis labels."""
    x_data = [1, 2, 3]
    y_data = [2, 4, 6]
    svg = scatter_plot(x_data, y_data, x_label="X Axis", y_label="Y Axis")
    assert_contains(svg, "X Axis")
    assert_contains(svg, "Y Axis")
    results.record("scatter_plot_with_axis_labels", True)


# =============================================================================
# Area Chart Tests
# =============================================================================

def test_area_chart_basic():
    """Test basic area chart generation."""
    data = [DataSeries(name="Values", data=[10, 20, 30, 40])]
    svg = area_chart(data, title="Area Chart")
    assert_svg_valid(svg)
    assert_contains(svg, '<polygon')
    results.record("area_chart_basic", True)


def test_area_chart_stacked():
    """Test stacked area chart."""
    data = [
        DataSeries(name="Series 1", data=[10, 20, 30]),
        DataSeries(name="Series 2", data=[15, 25, 35])
    ]
    svg = area_chart(data, stacked=True)
    assert_svg_valid(svg)
    results.record("area_chart_stacked", True)


def test_area_chart_multiple_series():
    """Test area chart with multiple series."""
    data = [
        DataSeries(name="A", data=[10, 20, 30]),
        DataSeries(name="B", data=[15, 25, 35]),
        DataSeries(name="C", data=[20, 30, 40])
    ]
    svg = area_chart(data)
    assert_svg_valid(svg)
    assert_contains(svg, "A")
    assert_contains(svg, "B")
    assert_contains(svg, "C")
    results.record("area_chart_multiple_series", True)


# =============================================================================
# Utility Function Tests
# =============================================================================

def test_create_sample_data():
    """Test sample data creation."""
    data = create_sample_data()
    assert_equal(len(data), 2)
    assert_equal(len(data[0].data), 12)  # 12 months
    results.record("create_sample_data", True)


def test_svg_to_data_uri():
    """Test SVG to data URI conversion."""
    svg = '<?xml version="1.0"?><svg></svg>'
    uri = svg_to_data_uri(svg)
    assert_true(uri.startswith("data:image/svg+xml;base64,"))
    results.record("svg_to_data_uri", True)


def test_save_svg(tmp_path: str = "test_output.svg"):
    """Test saving SVG to file."""
    svg = '<?xml version="1.0"?><svg></svg>'
    try:
        save_svg(svg, tmp_path)
        assert_true(os.path.exists(tmp_path))
        with open(tmp_path, 'r') as f:
            content = f.read()
        assert_equal(content, svg)
        os.remove(tmp_path)
        results.record("test_save_svg", True)
    except Exception as e:
        results.record("test_save_svg", False, str(e))


# =============================================================================
# Edge Case Tests
# =============================================================================

def test_empty_data():
    """Test chart with empty data."""
    data = [DataSeries(name="Empty", data=[])]
    try:
        svg = line_chart(data)
        assert_svg_valid(svg)
        results.record("empty_data", True)
    except Exception as e:
        results.record("empty_data", False, str(e))


def test_single_value():
    """Test chart with single value."""
    data = [DataSeries(name="Single", data=[42])]
    try:
        svg = line_chart(data)
        assert_svg_valid(svg)
        results.record("single_value", True)
    except Exception as e:
        results.record("single_value", False, str(e))


def test_negative_values():
    """Test chart with negative values."""
    data = [DataSeries(name="Mixed", data=[-10, 0, 10, -5, 5])]
    try:
        svg = line_chart(data)
        assert_svg_valid(svg)
        results.record("negative_values", True)
    except Exception as e:
        results.record("negative_values", False, str(e))


def test_large_values():
    """Test chart with large values."""
    data = [DataSeries(name="Large", data=[1000000, 2000000, 3000000])]
    try:
        svg = line_chart(data)
        assert_svg_valid(svg)
        results.record("large_values", True)
    except Exception as e:
        results.record("large_values", False, str(e))


def test_unicode_labels():
    """Test chart with Unicode labels."""
    data = [DataSeries(name="测试", data=[1, 2, 3], labels=["一月", "二月", "三月"])]
    try:
        svg = line_chart(data, x_labels=["一月", "二月", "三月"])
        assert_svg_valid(svg)
        # Series name appears in legend only when multiple series, so just check x_labels
        assert_contains(svg, "一月")
        assert_contains(svg, "二月")
        results.record("unicode_labels", True)
    except Exception as e:
        results.record("unicode_labels", False, str(e))


# =============================================================================
# Integration Tests
# =============================================================================

def test_all_chart_types():
    """Test that all chart types can be generated."""
    data = create_sample_data()
    
    charts = [
        ("line", lambda: line_chart(data, title="Line")),
        ("bar", lambda: bar_chart(data, title="Bar")),
        ("pie", lambda: pie_chart([DataSeries(name="P", data=[30, 40, 30])], title="Pie")),
        ("scatter", lambda: scatter_plot([1,2,3], [2,4,6], title="Scatter")),
        ("area", lambda: area_chart(data, title="Area")),
    ]
    
    all_passed = True
    for name, chart_func in charts:
        try:
            svg = chart_func()
            assert_svg_valid(svg)
        except Exception as e:
            all_passed = False
            print(f"  ✗ {name} chart failed: {e}")
    
    results.record("all_chart_types", all_passed)


def test_custom_config():
    """Test charts with custom configuration."""
    config = ChartConfig(
        width=1000,
        height=800,
        background_color="#f0f0f0",
        show_grid=False,
        show_legend=False
    )
    data = [DataSeries(name="Test", data=[1, 2, 3, 4, 5])]
    
    svg = line_chart(data, config=config)
    assert_contains(svg, 'width="1000"')
    assert_contains(svg, 'height="800"')
    assert_contains(svg, '#f0f0f0')
    results.record("custom_config", True)


# =============================================================================
# Main Test Runner
# =============================================================================

def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Chart Utils Test Suite")
    print("=" * 60)
    
    # Color utilities
    print("\n📊 Color Utilities:")
    test_parse_color()
    test_lighten_color()
    test_darken_color()
    
    # Math utilities
    print("\n📐 Math Utilities:")
    test_calculate_min_max()
    test_calculate_min_max_empty()
    test_calculate_min_max_single()
    test_interpolate()
    
    # SVG Builder
    print("\n🎨 SVG Builder:")
    test_svg_builder_rect()
    test_svg_builder_circle()
    test_svg_builder_line()
    test_svg_builder_polyline()
    test_svg_builder_text()
    test_svg_builder_path()
    test_svg_builder_complete()
    
    # Data structures
    print("\n📋 Data Structures:")
    test_data_series_creation()
    test_data_series_with_color()
    test_data_series_with_labels()
    test_chart_config_defaults()
    test_chart_config_custom()
    
    # Line charts
    print("\n📈 Line Charts:")
    test_line_chart_basic()
    test_line_chart_multiple_series()
    test_line_chart_with_labels()
    test_line_chart_no_grid()
    test_line_chart_no_legend()
    
    # Bar charts
    print("\n📊 Bar Charts:")
    test_bar_chart_basic()
    test_bar_chart_multiple_series()
    test_bar_chart_horizontal()
    test_bar_chart_with_labels()
    
    # Pie charts
    print("\n🥧 Pie Charts:")
    test_pie_chart_basic()
    test_pie_chart_with_percentages()
    test_pie_chart_with_labels()
    test_pie_chart_explode()
    test_pie_chart_no_legend()
    
    # Scatter plots
    print("\n🔵 Scatter Plots:")
    test_scatter_plot_basic()
    test_scatter_plot_with_trend()
    test_scatter_plot_with_labels()
    test_scatter_plot_with_axis_labels()
    
    # Area charts
    print("\n📉 Area Charts:")
    test_area_chart_basic()
    test_area_chart_stacked()
    test_area_chart_multiple_series()
    
    # Utilities
    print("\n🔧 Utilities:")
    test_create_sample_data()
    test_svg_to_data_uri()
    test_save_svg()
    
    # Edge cases
    print("\n🔍 Edge Cases:")
    test_empty_data()
    test_single_value()
    test_negative_values()
    test_large_values()
    test_unicode_labels()
    
    # Integration
    print("\n🔗 Integration:")
    test_all_chart_types()
    test_custom_config()
    
    # Summary
    return results.summary()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
