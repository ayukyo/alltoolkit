#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Chart Utilities Module

Comprehensive chart generation utilities for Python with zero external dependencies.
Provides line charts, bar charts, pie charts, scatter plots, and more using SVG.

Author: AllToolkit
License: MIT
"""

import math
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass, field


# =============================================================================
# Type Aliases
# =============================================================================

Number = Union[int, float]
Color = str  # Hex color like "#FF5733" or named color like "red"


# =============================================================================
# Constants
# =============================================================================

DEFAULT_COLORS = [
    "#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6",
    "#1abc9c", "#e67e22", "#34495e", "#95a5a6", "#d35400",
    "#27ae60", "#2980b9", "#8e44ad", "#f1c40f", "#16a085"
]

SVG_NS = "http://www.w3.org/2000/svg"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class ChartConfig:
    """Configuration for chart appearance."""
    width: int = 800
    height: int = 600
    margin_top: int = 60
    margin_right: int = 60
    margin_bottom: int = 80
    margin_left: int = 80
    background_color: Color = "#ffffff"
    grid_color: Color = "#e0e0e0"
    text_color: Color = "#333333"
    font_family: str = "Arial, sans-serif"
    font_size: int = 12
    title_font_size: int = 16
    show_grid: bool = True
    show_legend: bool = True
    legend_position: str = "top-right"  # top-right, top-left, bottom-right, bottom-left
    animation: bool = False


@dataclass
class DataSeries:
    """A single data series for charts."""
    name: str
    data: List[Number]
    color: Color = ""
    labels: List[str] = field(default_factory=list)


@dataclass
class Point:
    """A point in 2D space."""
    x: Number
    y: Number


# =============================================================================
# Color Utilities
# =============================================================================

def parse_color(color: Color) -> str:
    """Ensure color is in valid format."""
    if not color:
        return DEFAULT_COLORS[0]
    return color


def lighten_color(color: Color, factor: float = 0.2) -> Color:
    """Lighten a color by a factor (0-1)."""
    if color.startswith("#"):
        hex_color = color[1:]
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    return color


def darken_color(color: Color, factor: float = 0.2) -> Color:
    """Darken a color by a factor (0-1)."""
    if color.startswith("#"):
        hex_color = color[1:]
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        r = int(r * (1 - factor))
        g = int(g * (1 - factor))
        b = int(b * (1 - factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    return color


# =============================================================================
# Math Utilities
# =============================================================================

def calculate_min_max(data: List[Number], padding: float = 0.1) -> Tuple[Number, Number]:
    """Calculate min and max values with padding."""
    if not data:
        return 0, 1
    
    min_val = min(data)
    max_val = max(data)
    
    if min_val == max_val:
        return min_val - 1, max_val + 1
    
    range_val = max_val - min_val
    padding_val = range_val * padding
    
    return min_val - padding_val, max_val + padding_val


def interpolate(start: Number, end: Number, t: float) -> Number:
    """Linear interpolation between start and end."""
    return start + (end - start) * t


# =============================================================================
# SVG Generation Utilities
# =============================================================================

class SVGBuilder:
    """Helper class for building SVG content."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.elements: List[str] = []
    
    def add(self, element: str) -> 'SVGBuilder':
        """Add an SVG element."""
        self.elements.append(element)
        return self
    
    def rect(self, x: Number, y: Number, width: Number, height: Number,
             fill: Color = "none", stroke: Color = "none", 
             stroke_width: int = 1, rx: int = 0,
             fill_opacity: float = None) -> 'SVGBuilder':
        """Add a rectangle."""
        opacity_attr = f' fill-opacity="{fill_opacity}"' if fill_opacity is not None else ""
        self.add(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" '
                 f'rx="{rx}"{opacity_attr}/>')
        return self
    
    def circle(self, cx: Number, cy: Number, r: Number,
               fill: Color = "none", stroke: Color = "none",
               stroke_width: int = 1) -> 'SVGBuilder':
        """Add a circle."""
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>')
        return self
    
    def line(self, x1: Number, y1: Number, x2: Number, y2: Number,
             stroke: Color = "#000000", stroke_width: int = 1,
             stroke_dasharray: str = "") -> 'SVGBuilder':
        """Add a line."""
        dash_attr = f' stroke-dasharray="{stroke_dasharray}"' if stroke_dasharray else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                 f'stroke="{stroke}" stroke-width="{stroke_width}"{dash_attr}/>')
        return self
    
    def polyline(self, points: List[Tuple[Number, Number]],
                 fill: Color = "none", stroke: Color = "#000000",
                 stroke_width: int = 2) -> 'SVGBuilder':
        """Add a polyline."""
        points_str = " ".join(f"{x},{y}" for x, y in points)
        self.add(f'<polyline points="{points_str}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>')
        return self
    
    def polygon(self, points: List[Tuple[Number, Number]],
                fill: Color = "none", stroke: Color = "#000000",
                stroke_width: int = 1) -> 'SVGBuilder':
        """Add a polygon."""
        points_str = " ".join(f"{x},{y}" for x, y in points)
        self.add(f'<polygon points="{points_str}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>')
        return self
    
    def path(self, d: str, fill: Color = "none", stroke: Color = "#000000",
             stroke_width: int = 2) -> 'SVGBuilder':
        """Add a path."""
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" '
                 f'stroke-width="{stroke_width}"/>')
        return self
    
    def text(self, x: Number, y: Number, text: str,
             fill: Color = "#000000", font_size: int = 12,
             font_family: str = "Arial", text_anchor: str = "start",
             dominant_baseline: str = "baseline",
             font_weight: str = "normal") -> 'SVGBuilder':
        """Add text."""
        self.add(f'<text x="{x}" y="{y}" fill="{fill}" font-size="{font_size}" '
                 f'font-family="{font_family}" text-anchor="{text_anchor}" '
                 f'dominant-baseline="{dominant_baseline}" '
                 f'font-weight="{font_weight}">{text}</text>')
        return self
    
    def group(self, elements: List[str], transform: str = "") -> 'SVGBuilder':
        """Add a group of elements."""
        transform_attr = f' transform="{transform}"' if transform else ""
        self.add(f'<g{transform_attr}>')
        for elem in elements:
            self.add(elem)
        self.add('</g>')
        return self
    
    def build(self, title: str = "") -> str:
        """Build the complete SVG document."""
        svg_parts = [
            f'<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="{SVG_NS}" width="{self.width}" height="{self.height}" '
            f'viewBox="0 0 {self.width} {self.height}">'
        ]
        
        if title:
            svg_parts.append(f'  <title>{title}</title>')
        
        svg_parts.extend(f'  {elem}' for elem in self.elements)
        svg_parts.append('</svg>')
        
        return '\n'.join(svg_parts)


# =============================================================================
# Line Chart
# =============================================================================

def line_chart(data: List[DataSeries], title: str = "", 
               x_labels: List[str] = None, y_label: str = "",
               config: ChartConfig = None) -> str:
    """
    Create a line chart.
    
    Args:
        data: List of data series
        title: Chart title
        x_labels: Labels for x-axis
        y_label: Label for y-axis
        config: Chart configuration
        
    Returns:
        SVG string
    """
    config = config or ChartConfig()
    
    # Calculate chart area
    chart_width = config.width - config.margin_left - config.margin_right
    chart_height = config.height - config.margin_top - config.margin_bottom
    
    # Find data range
    all_values = []
    for series in data:
        all_values.extend(series.data)
    
    y_min, y_max = calculate_min_max(all_values)
    x_max = max(len(series.data) for series in data) - 1 if data else 0
    
    # Build SVG
    svg = SVGBuilder(config.width, config.height)
    
    # Background
    svg.rect(0, 0, config.width, config.height, fill=config.background_color)
    
    # Title
    if title:
        svg.text(config.width / 2, 30, title, fill=config.text_color,
                font_size=config.title_font_size, text_anchor="middle",
                font_weight="bold")
    
    # Grid lines
    if config.show_grid:
        num_grid_lines = 5
        for i in range(num_grid_lines + 1):
            y = config.margin_top + (chart_height * i / num_grid_lines)
            value = y_max - (y_max - y_min) * (i / num_grid_lines)
            
            svg.line(config.margin_left, y, 
                    config.width - config.margin_right, y,
                    stroke=config.grid_color, stroke_dasharray="2,2")
            
            svg.text(config.margin_left - 10, y, f"{value:.1f}",
                    fill=config.text_color, font_size=config.font_size,
                    text_anchor="end", dominant_baseline="middle")
    
    # X-axis labels
    if x_labels:
        for i, label in enumerate(x_labels[:len(data[0].data) if data else 0]):
            x = config.margin_left + (chart_width * i / max(x_max, 1))
            svg.text(x, config.height - config.margin_bottom + 20, label,
                    fill=config.text_color, font_size=config.font_size,
                    text_anchor="middle")
    
    # Y-axis label
    if y_label:
        svg.text(20, config.height / 2, y_label, fill=config.text_color,
                font_size=config.font_size, text_anchor="middle")
    
    # Draw lines
    for series in data:
        color = parse_color(series.color)
        points = []
        
        for i, value in enumerate(series.data):
            x = config.margin_left + (chart_width * i / max(x_max, 1))
            y = config.margin_top + chart_height * (1 - (value - y_min) / (y_max - y_min))
            points.append((x, y))
        
        svg.polyline(points, fill="none", stroke=color, stroke_width=2)
        
        # Add data points
        for x, y in points:
            svg.circle(x, y, 4, fill=color, stroke="#ffffff", stroke_width=2)
    
    # Legend
    if config.show_legend and len(data) > 1:
        legend_x = config.width - config.margin_right - 150
        legend_y = config.margin_top + 10
        
        for i, series in enumerate(data):
            color = parse_color(series.color)
            y = legend_y + i * 20
            svg.rect(legend_x, y - 8, 15, 15, fill=color, stroke=color)
            svg.text(legend_x + 20, y, series.name, fill=config.text_color,
                    font_size=config.font_size)
    
    # Axes
    svg.line(config.margin_left, config.margin_top,
            config.margin_left, config.height - config.margin_bottom,
            stroke=config.text_color, stroke_width=2)
    svg.line(config.margin_left, config.height - config.margin_bottom,
            config.width - config.margin_right, config.height - config.margin_bottom,
            stroke=config.text_color, stroke_width=2)
    
    return svg.build(title)


# =============================================================================
# Bar Chart
# =============================================================================

def bar_chart(data: List[DataSeries], title: str = "",
              x_labels: List[str] = None, y_label: str = "",
              config: ChartConfig = None, horizontal: bool = False) -> str:
    """
    Create a bar chart.
    
    Args:
        data: List of data series
        title: Chart title
        x_labels: Labels for x-axis
        y_label: Label for y-axis
        config: Chart configuration
        horizontal: If True, create horizontal bar chart
        
    Returns:
        SVG string
    """
    config = config or ChartConfig()
    
    chart_width = config.width - config.margin_left - config.margin_right
    chart_height = config.height - config.margin_top - config.margin_bottom
    
    # Find data range
    all_values = []
    for series in data:
        all_values.extend(series.data)
    
    y_min, y_max = calculate_min_max(all_values, padding=0.15)
    if y_min > 0:
        y_min = 0
    
    num_bars = max(len(series.data) for series in data) if data else 0
    bar_width = chart_width / num_bars * 0.8 / len(data) if num_bars > 0 else 0
    bar_gap = chart_width / num_bars * 0.2 if num_bars > 0 else 0
    
    svg = SVGBuilder(config.width, config.height)
    
    # Background
    svg.rect(0, 0, config.width, config.height, fill=config.background_color)
    
    # Title
    if title:
        svg.text(config.width / 2, 30, title, fill=config.text_color,
                font_size=config.title_font_size, text_anchor="middle",
                font_weight="bold")
    
    # Grid lines
    if config.show_grid:
        num_grid_lines = 5
        for i in range(num_grid_lines + 1):
            y = config.margin_top + (chart_height * i / num_grid_lines)
            value = y_max - (y_max - y_min) * (i / num_grid_lines)
            
            svg.line(config.margin_left, y,
                    config.width - config.margin_right, y,
                    stroke=config.grid_color, stroke_dasharray="2,2")
            
            svg.text(config.margin_left - 10, y, f"{value:.1f}",
                    fill=config.text_color, font_size=config.font_size,
                    text_anchor="end", dominant_baseline="middle")
    
    # Bars
    for series_idx, series in enumerate(data):
        color = parse_color(series.color) or DEFAULT_COLORS[series_idx % len(DEFAULT_COLORS)]
        
        for i, value in enumerate(series.data):
            bar_height = chart_height * (value - y_min) / (y_max - y_min)
            
            if horizontal:
                x = config.margin_left
                y = config.margin_top + i * (chart_height / num_bars) + series_idx * bar_width
                bar_w = bar_height
                bar_h = bar_width - 1
            else:
                x = config.margin_left + i * (chart_width / num_bars) + series_idx * bar_width + bar_gap / 2
                y = config.margin_top + chart_height - bar_height
                bar_w = bar_width - 1
                bar_h = bar_height
            
            svg.rect(x, y, bar_w, bar_h, fill=color, stroke=darken_color(color),
                    stroke_width=1, rx=2)
    
    # X-axis labels
    if x_labels:
        for i, label in enumerate(x_labels[:num_bars]):
            if horizontal:
                y = config.margin_top + i * (chart_height / num_bars) + chart_height / num_bars / 2
                svg.text(config.margin_left - 10, y, label,
                        fill=config.text_color, font_size=config.font_size,
                        text_anchor="end", dominant_baseline="middle")
            else:
                x = config.margin_left + i * (chart_width / num_bars) + chart_width / num_bars / 2
                svg.text(x, config.height - config.margin_bottom + 20, label,
                        fill=config.text_color, font_size=config.font_size,
                        text_anchor="middle")
    
    # Legend
    if config.show_legend and len(data) > 1:
        legend_x = config.width - config.margin_right - 150
        legend_y = config.margin_top + 10
        
        for i, series in enumerate(data):
            color = parse_color(series.color) or DEFAULT_COLORS[i % len(DEFAULT_COLORS)]
            y = legend_y + i * 20
            svg.rect(legend_x, y - 8, 15, 15, fill=color, stroke=color)
            svg.text(legend_x + 20, y, series.name, fill=config.text_color,
                    font_size=config.font_size)
    
    # Axes
    svg.line(config.margin_left, config.margin_top,
            config.margin_left, config.height - config.margin_bottom,
            stroke=config.text_color, stroke_width=2)
    svg.line(config.margin_left, config.height - config.margin_bottom,
            config.width - config.margin_right, config.height - config.margin_bottom,
            stroke=config.text_color, stroke_width=2)
    
    return svg.build(title)


# =============================================================================
# Pie Chart
# =============================================================================

def pie_chart(data: List[DataSeries], title: str = "",
              show_percentages: bool = True, show_labels: bool = True,
              config: ChartConfig = None, explode: List[float] = None) -> str:
    """
    Create a pie chart.
    
    Args:
        data: Single data series (or first series from list)
        title: Chart title
        show_percentages: If True, show percentage labels
        show_labels: If True, show category labels
        config: Chart configuration
        explode: List of distances to explode slices (0-0.5)
        
    Returns:
        SVG string
    """
    config = config or ChartConfig()
    
    # Use first series or create one
    if not data:
        data = [DataSeries(name="Data", data=[1, 1, 1, 1])]
    series = data[0]
    
    total = sum(series.data)
    if total == 0:
        total = 1
    
    center_x = config.width / 2
    center_y = (config.height + config.margin_top - config.margin_bottom) / 2
    chart_width = config.width - config.margin_left - config.margin_right
    chart_height = config.height - config.margin_top - config.margin_bottom
    radius = min(config.width, config.height) / 2 * 0.7
    
    svg = SVGBuilder(config.width, config.height)
    
    # Background
    svg.rect(0, 0, config.width, config.height, fill=config.background_color)
    
    # Title
    if title:
        svg.text(config.width / 2, 30, title, fill=config.text_color,
                font_size=config.title_font_size, text_anchor="middle",
                font_weight="bold")
    
    # Draw slices
    start_angle = -90  # Start from top
    labels = series.labels or [f"Item {i+1}" for i in range(len(series.data))]
    explode = explode or [0] * len(series.data)
    
    for i, value in enumerate(series.data):
        percentage = value / total
        angle = percentage * 360
        end_angle = start_angle + angle
        
        color = parse_color(series.color) or DEFAULT_COLORS[i % len(DEFAULT_COLORS)]
        
        # Calculate slice points
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        explode_dist = explode[i] * radius if i < len(explode) else 0
        cx = center_x + explode_dist * math.cos(start_rad + angle * math.pi / 360)
        cy = center_y + explode_dist * math.sin(start_rad + angle * math.pi / 360)
        
        x1 = cx + radius * math.cos(start_rad)
        y1 = cy + radius * math.sin(start_rad)
        x2 = cx + radius * math.cos(end_rad)
        y2 = cy + radius * math.sin(end_rad)
        
        # Create path
        large_arc = 1 if angle > 180 else 0
        d = f"M {cx} {cy} L {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} Z"
        svg.path(d, fill=color, stroke="#ffffff", stroke_width=2)
        
        # Label
        if show_labels or show_percentages:
            label_angle = start_angle + angle / 2
            label_rad = math.radians(label_angle)
            label_radius = radius * 0.65
            
            lx = cx + label_radius * math.cos(label_rad)
            ly = cy + label_radius * math.sin(label_rad)
            
            label_text = ""
            if show_labels:
                label_text = labels[i] if i < len(labels) else f"Item {i+1}"
            if show_percentages:
                if label_text:
                    label_text += f"\n({percentage*100:.1f}%)"
                else:
                    label_text = f"{percentage*100:.1f}%"
            
            # Use tspan for multi-line
            if "\n" in label_text:
                lines = label_text.split("\n")
                svg.text(lx, ly - 5, lines[0], fill="#ffffff", font_size=config.font_size,
                        text_anchor="middle", dominant_baseline="middle", font_weight="bold")
                if len(lines) > 1:
                    svg.text(lx, ly + 10, lines[1], fill="#ffffff", font_size=config.font_size - 2,
                            text_anchor="middle", dominant_baseline="middle")
            else:
                svg.text(lx, ly, label_text, fill="#ffffff", font_size=config.font_size,
                        text_anchor="middle", dominant_baseline="middle", font_weight="bold")
        
        start_angle = end_angle
    
    # Legend
    if config.show_legend:
        legend_x = config.width - config.margin_right - 150
        legend_y = config.margin_top + 10
        
        for i, (value, label) in enumerate(zip(series.data, labels)):
            color = DEFAULT_COLORS[i % len(DEFAULT_COLORS)]
            y = legend_y + i * 20
            percentage = value / total * 100
            
            svg.rect(legend_x, y - 8, 15, 15, fill=color, stroke=color)
            svg.text(legend_x + 20, y, f"{label}: {percentage:.1f}%",
                    fill=config.text_color, font_size=config.font_size)
    
    return svg.build(title)


# =============================================================================
# Scatter Plot
# =============================================================================

def scatter_plot(x_data: List[Number], y_data: List[Number],
                 title: str = "", x_label: str = "", y_label: str = "",
                 point_labels: List[str] = None, trend_line: bool = False,
                 config: ChartConfig = None) -> str:
    """
    Create a scatter plot.
    
    Args:
        x_data: X-axis values
        y_data: Y-axis values
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        point_labels: Labels for each point
        trend_line: If True, add linear regression trend line
        config: Chart configuration
        
    Returns:
        SVG string
    """
    config = config or ChartConfig()
    
    chart_width = config.width - config.margin_left - config.margin_right
    chart_height = config.height - config.margin_top - config.margin_bottom
    
    x_min, x_max = calculate_min_max(x_data)
    y_min, y_max = calculate_min_max(y_data)
    
    svg = SVGBuilder(config.width, config.height)
    
    # Background
    svg.rect(0, 0, config.width, config.height, fill=config.background_color)
    
    # Title
    if title:
        svg.text(config.width / 2, 30, title, fill=config.text_color,
                font_size=config.title_font_size, text_anchor="middle",
                font_weight="bold")
    
    # Grid
    if config.show_grid:
        num_grid_lines = 5
        for i in range(num_grid_lines + 1):
            # Vertical lines
            x = config.margin_left + (chart_width * i / num_grid_lines)
            x_val = x_min + (x_max - x_min) * (i / num_grid_lines)
            svg.line(x, config.margin_top, x, config.height - config.margin_bottom,
                    stroke=config.grid_color, stroke_dasharray="2,2")
            svg.text(x, config.height - config.margin_bottom + 20, f"{x_val:.1f}",
                    fill=config.text_color, font_size=config.font_size,
                    text_anchor="middle")
            
            # Horizontal lines
            y = config.margin_top + (chart_height * i / num_grid_lines)
            y_val = y_max - (y_max - y_min) * (i / num_grid_lines)
            svg.line(config.margin_left, y, config.width - config.margin_right, y,
                    stroke=config.grid_color, stroke_dasharray="2,2")
            svg.text(config.margin_left - 10, y, f"{y_val:.1f}",
                    fill=config.text_color, font_size=config.font_size,
                    text_anchor="end", dominant_baseline="middle")
    
    # Trend line
    if trend_line and len(x_data) > 1:
        # Calculate linear regression
        n = len(x_data)
        sum_x = sum(x_data)
        sum_y = sum(y_data)
        sum_xy = sum(x * y for x, y in zip(x_data, y_data))
        sum_x2 = sum(x * x for x in x_data)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x) if (n * sum_x2 - sum_x * sum_x) != 0 else 0
        intercept = (sum_y - slope * sum_x) / n
        
        # Draw trend line
        x1_plot = x_min
        y1_plot = slope * x_min + intercept
        x2_plot = x_max
        y2_plot = slope * x_max + intercept
        
        def to_svg_x(val):
            return config.margin_left + chart_width * (val - x_min) / (x_max - x_min)
        
        def to_svg_y(val):
            return config.margin_top + chart_height * (1 - (val - y_min) / (y_max - y_min))
        
        svg.line(to_svg_x(x1_plot), to_svg_y(y1_plot),
                to_svg_x(x2_plot), to_svg_y(y2_plot),
                stroke="#e74c3c", stroke_width=2, stroke_dasharray="5,5")
    
    # Points
    color = DEFAULT_COLORS[0]
    for i, (x, y) in enumerate(zip(x_data, y_data)):
        svg_x = config.margin_left + chart_width * (x - x_min) / (x_max - x_min)
        svg_y = config.margin_top + chart_height * (1 - (y - y_min) / (y_max - y_min))
        
        svg.circle(svg_x, svg_y, 6, fill=color, stroke="#ffffff", stroke_width=2)
        
        if point_labels and i < len(point_labels):
            svg.text(svg_x + 10, svg_y - 10, point_labels[i],
                    fill=config.text_color, font_size=config.font_size - 2)
    
    # Axes labels
    if x_label:
        svg.text(config.width / 2, config.height - 20, x_label,
                fill=config.text_color, font_size=config.font_size,
                text_anchor="middle")
    
    if y_label:
        svg.text(20, config.height / 2, y_label, fill=config.text_color,
                font_size=config.font_size, text_anchor="middle")
    
    # Axes
    svg.line(config.margin_left, config.margin_top,
            config.margin_left, config.height - config.margin_bottom,
            stroke=config.text_color, stroke_width=2)
    svg.line(config.margin_left, config.height - config.margin_bottom,
            config.width - config.margin_right, config.height - config.margin_bottom,
            stroke=config.text_color, stroke_width=2)
    
    return svg.build(title)


# =============================================================================
# Area Chart
# =============================================================================

def area_chart(data: List[DataSeries], title: str = "",
               x_labels: List[str] = None, y_label: str = "",
               config: ChartConfig = None, stacked: bool = False) -> str:
    """
    Create an area chart.
    
    Args:
        data: List of data series
        title: Chart title
        x_labels: Labels for x-axis
        y_label: Label for y-axis
        config: Chart configuration
        stacked: If True, stack areas
        
    Returns:
        SVG string
    """
    config = config or ChartConfig()
    
    chart_width = config.width - config.margin_left - config.margin_right
    chart_height = config.height - config.margin_top - config.margin_bottom
    
    if stacked:
        # Calculate stacked values
        max_points = max(len(series.data) for series in data) if data else 0
        stacked_totals = [0] * max_points
        for series in data:
            for i, val in enumerate(series.data):
                if i < len(stacked_totals):
                    stacked_totals[i] += val
        y_min, y_max = 0, max(stacked_totals) * 1.1
    else:
        all_values = []
        for series in data:
            all_values.extend(series.data)
        y_min, y_max = calculate_min_max(all_values)
    
    x_max = max(len(series.data) for series in data) - 1 if data else 0
    
    svg = SVGBuilder(config.width, config.height)
    
    # Background
    svg.rect(0, 0, config.width, config.height, fill=config.background_color)
    
    # Title
    if title:
        svg.text(config.width / 2, 30, title, fill=config.text_color,
                font_size=config.title_font_size, text_anchor="middle",
                font_weight="bold")
    
    # Grid
    if config.show_grid:
        num_grid_lines = 5
        for i in range(num_grid_lines + 1):
            y = config.margin_top + (chart_height * i / num_grid_lines)
            value = y_max - (y_max - y_min) * (i / num_grid_lines)
            svg.line(config.margin_left, y,
                    config.width - config.margin_right, y,
                    stroke=config.grid_color, stroke_dasharray="2,2")
            svg.text(config.margin_left - 10, y, f"{value:.1f}",
                    fill=config.text_color, font_size=config.font_size,
                    text_anchor="end", dominant_baseline="middle")
    
    # Draw areas
    cumulative = [0] * (x_max + 2) if stacked else None
    
    for series_idx, series in enumerate(data):
        color = parse_color(series.color) or DEFAULT_COLORS[series_idx % len(DEFAULT_COLORS)]
        
        points = []
        bottom_points = []
        
        for i, value in enumerate(series.data):
            x = config.margin_left + (chart_width * i / max(x_max, 1))
            
            if stacked and cumulative:
                base_value = cumulative[i]
                cumulative[i] += value
                y_top = config.margin_top + chart_height * (1 - (cumulative[i] - y_min) / (y_max - y_min))
                y_bottom = config.margin_top + chart_height * (1 - (base_value - y_min) / (y_max - y_min))
            else:
                y_top = config.margin_top + chart_height * (1 - (value - y_min) / (y_max - y_min))
                y_bottom = config.margin_top + chart_height
            
            points.append((x, y_top))
            bottom_points.append((x, y_bottom))
        
        # Close the path
        if points:
            path_points = points + list(reversed(bottom_points))
            points_str = " ".join(f"{x},{y}" for x, y in path_points)
            
            svg.add(f'<polygon points="{points_str}" fill="{color}" '
                   f'fill-opacity="0.6" stroke="{darken_color(color)}" stroke-width="2"/>')
    
    # X-axis labels
    if x_labels:
        for i, label in enumerate(x_labels[:len(data[0].data) if data else 0]):
            x = config.margin_left + (chart_width * i / max(x_max, 1))
            svg.text(x, config.height - config.margin_bottom + 20, label,
                    fill=config.text_color, font_size=config.font_size,
                    text_anchor="middle")
    
    # Y-axis label
    if y_label:
        svg.text(20, config.height / 2, y_label, fill=config.text_color,
                font_size=config.font_size, text_anchor="middle")
    
    # Legend
    if config.show_legend and len(data) > 1:
        legend_x = config.width - config.margin_right - 150
        legend_y = config.margin_top + 10
        
        for i, series in enumerate(data):
            color = parse_color(series.color) or DEFAULT_COLORS[i % len(DEFAULT_COLORS)]
            y = legend_y + i * 20
            svg.rect(legend_x, y - 8, 15, 15, fill=color, stroke=color, fill_opacity=0.6)
            svg.text(legend_x + 20, y, series.name, fill=config.text_color,
                    font_size=config.font_size)
    
    # Axes
    svg.line(config.margin_left, config.margin_top,
            config.margin_left, config.height - config.margin_bottom,
            stroke=config.text_color, stroke_width=2)
    svg.line(config.margin_left, config.height - config.margin_bottom,
            config.width - config.margin_right, config.height - config.margin_bottom,
            stroke=config.text_color, stroke_width=2)
    
    return svg.build(title)


# =============================================================================
# Utility Functions
# =============================================================================

def save_svg(svg_content: str, filepath: str) -> None:
    """
    Save SVG content to a file.
    
    Args:
        svg_content: SVG string
        filepath: Output file path
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg_content)


def svg_to_data_uri(svg_content: str) -> str:
    """
    Convert SVG to data URI.
    
    Args:
        svg_content: SVG string
        
    Returns:
        Data URI string
    """
    import base64
    encoded = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{encoded}"


def create_sample_data() -> List[DataSeries]:
    """Create sample data for testing."""
    return [
        DataSeries(name="Sales 2025", data=[120, 150, 180, 220, 190, 240, 280, 260, 300, 320, 350, 380],
                  labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]),
        DataSeries(name="Sales 2026", data=[140, 170, 200, 250, 230, 280, 320, 300, 350, 380, 400, 420]),
    ]


# =============================================================================
# Main (Demo)
# =============================================================================

if __name__ == "__main__":
    # Demo: Generate sample charts
    print("Generating sample charts...")
    
    # Line chart
    data = create_sample_data()
    svg = line_chart(data, title="Monthly Sales Comparison",
                    x_labels=data[0].labels, y_label="Sales ($K)")
    save_svg(svg, "line_chart.svg")
    print("  ✓ line_chart.svg")
    
    # Bar chart
    svg = bar_chart(data, title="Monthly Sales Comparison",
                   x_labels=data[0].labels, y_label="Sales ($K)")
    save_svg(svg, "bar_chart.svg")
    print("  ✓ bar_chart.svg")
    
    # Pie chart
    pie_data = [DataSeries(name="Categories", data=[30, 45, 15, 10],
                          labels=["Product A", "Product B", "Product C", "Product D"])]
    svg = pie_chart(pie_data, title="Product Distribution", show_percentages=True)
    save_svg(svg, "pie_chart.svg")
    print("  ✓ pie_chart.svg")
    
    # Scatter plot
    import random
    random.seed(42)
    x_vals = [random.uniform(0, 100) for _ in range(50)]
    y_vals = [x * 0.5 + random.uniform(-10, 10) for x in x_vals]
    svg = scatter_plot(x_vals, y_vals, title="Correlation Analysis",
                      x_label="X Value", y_label="Y Value", trend_line=True)
    save_svg(svg, "scatter_plot.svg")
    print("  ✓ scatter_plot.svg")
    
    # Area chart
    svg = area_chart(data, title="Cumulative Sales",
                    x_labels=data[0].labels, y_label="Sales ($K)", stacked=True)
    save_svg(svg, "area_chart.svg")
    print("  ✓ area_chart.svg")
    
    print("\nAll charts generated successfully!")
    print("Open the .svg files in a browser to view them.")
