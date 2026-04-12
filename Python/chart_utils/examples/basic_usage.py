#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chart Utils - Basic Usage Examples

This file demonstrates basic usage of all chart types.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    line_chart, bar_chart, pie_chart, scatter_plot, area_chart,
    DataSeries, ChartConfig, save_svg, create_sample_data
)


def example_line_chart():
    """Example: Line chart with multiple series."""
    print("Generating line chart...")
    
    data = [
        DataSeries(name="2025 年", 
                   data=[120, 150, 180, 220, 190, 240, 280, 260, 300, 320, 350, 380]),
        DataSeries(name="2026 年", 
                   data=[140, 170, 200, 250, 230, 280, 320, 300, 350, 380, 400, 420])
    ]
    
    svg = line_chart(
        data,
        title="年度销售对比",
        x_labels=["1 月", "2 月", "3 月", "4 月", "5 月", "6 月",
                  "7 月", "8 月", "9 月", "10 月", "11 月", "12 月"],
        y_label="销售额 (万元)"
    )
    
    save_svg(svg, "example_line_chart.svg")
    print("  ✓ example_line_chart.svg")


def example_bar_chart():
    """Example: Grouped bar chart."""
    print("Generating bar chart...")
    
    data = [
        DataSeries(name="第一季度", data=[100, 150, 200, 175]),
        DataSeries(name="第二季度", data=[120, 170, 220, 190]),
        DataSeries(name="第三季度", data=[140, 180, 240, 210])
    ]
    
    svg = bar_chart(
        data,
        title="季度产品销售",
        x_labels=["产品 A", "产品 B", "产品 C", "产品 D"],
        y_label="销量 (件)"
    )
    
    save_svg(svg, "example_bar_chart.svg")
    print("  ✓ example_bar_chart.svg")


def example_pie_chart():
    """Example: Pie chart with explode effect."""
    print("Generating pie chart...")
    
    data = [DataSeries(
        name="市场份额",
        data=[35, 25, 20, 12, 8],
        labels=["产品 A", "产品 B", "产品 C", "产品 D", "其他"]
    )]
    
    svg = pie_chart(
        data,
        title="产品市场份额",
        show_percentages=True,
        explode=[0.05, 0, 0, 0, 0]
    )
    
    save_svg(svg, "example_pie_chart.svg")
    print("  ✓ example_pie_chart.svg")


def example_scatter_plot():
    """Example: Scatter plot with trend line."""
    print("Generating scatter plot...")
    
    import random
    random.seed(42)
    
    x_vals = [random.uniform(0, 100) for _ in range(50)]
    y_vals = [x * 0.8 + random.uniform(-10, 10) for x in x_vals]
    
    svg = scatter_plot(
        x_vals, y_vals,
        title="广告投入与销售相关性",
        x_label="广告投入 (万元)",
        y_label="销售额 (万元)",
        trend_line=True
    )
    
    save_svg(svg, "example_scatter_plot.svg")
    print("  ✓ example_scatter_plot.svg")


def example_area_chart():
    """Example: Stacked area chart."""
    print("Generating area chart...")
    
    data = [
        DataSeries(name="移动端", data=[30, 40, 50, 60, 70, 80]),
        DataSeries(name="桌面端", data=[50, 45, 40, 35, 30, 25]),
        DataSeries(name="平板", data=[20, 25, 30, 35, 40, 45])
    ]
    
    svg = area_chart(
        data,
        title="访问设备分布",
        x_labels=["1 月", "2 月", "3 月", "4 月", "5 月", "6 月"],
        y_label="访问量 (千)",
        stacked=True
    )
    
    save_svg(svg, "example_area_chart.svg")
    print("  ✓ example_area_chart.svg")


def example_custom_style():
    """Example: Custom styled chart."""
    print("Generating custom styled chart...")
    
    config = ChartConfig(
        width=1000,
        height=600,
        background_color="#1a1a2e",
        grid_color="#16213e",
        text_color="#eaeaea",
        title_font_size=18
    )
    
    data = [DataSeries(name="数据", data=[10, 25, 40, 55, 70, 85, 95], color="#e94560")]
    
    svg = line_chart(
        data,
        title="深色主题图表",
        x_labels=["A", "B", "C", "D", "E", "F", "G"],
        config=config
    )
    
    save_svg(svg, "example_custom_style.svg")
    print("  ✓ example_custom_style.svg")


def main():
    """Run all examples."""
    print("=" * 60)
    print("Chart Utils - Examples")
    print("=" * 60)
    print()
    
    example_line_chart()
    example_bar_chart()
    example_pie_chart()
    example_scatter_plot()
    example_area_chart()
    example_custom_style()
    
    print()
    print("=" * 60)
    print("All examples generated successfully!")
    print("Open the .svg files in a browser to view them.")
    print("=" * 60)


if __name__ == "__main__":
    main()
