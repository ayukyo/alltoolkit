#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Graphviz DOT Utilities Module
===========================================
A comprehensive Graphviz DOT format generation utility module for Python with zero external dependencies.

Features:
    - DOT language generation for graph visualization
    - Directed graphs (digraph) and undirected graphs (graph)
    - Subgraph and cluster support
    - Node and edge attributes (color, shape, style, label)
    - HTML label support
    - Record-based nodes (tables)
    - Graph ranking and layout hints
    - State machine diagram generation
    - Tree visualization helpers
    - DOT parsing and manipulation

Author: AllToolkit Contributors
License: MIT
"""

from typing import Union, List, Optional, Dict, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import re


# ============================================================================
# Enums and Constants
# ============================================================================

class GraphType(Enum):
    """Graph type enumeration."""
    DIRECTED = "digraph"
    UNDIRECTED = "graph"


class NodeShape(Enum):
    """Common node shapes for Graphviz."""
    BOX = "box"
    POLYGON = "polygon"
    ELLIPSE = "ellipse"
    OVAL = "oval"
    CIRCLE = "circle"
    POINT = "point"
    EGG = "egg"
    TRIANGLE = "triangle"
    PLAINTEXT = "plaintext"
    PLAIN = "plain"
    DIAMOND = "diamond"
    TRAPEZIUM = "trapezium"
    PARALLELOGRAM = "parallelogram"
    HOUSE = "house"
    PENTAGON = "pentagon"
    HEXAGON = "hexagon"
    SEPTAGON = "septagon"
    OCTAGON = "octagon"
    DOUBLECIRCLE = "doublecircle"
    DOUBLEOCTAGON = "doubleoctagon"
    TRIPLEOCTAGON = "tripleoctagon"
    INVTRIANGLE = "invtriangle"
    INVTRAPEZIUM = "invtrapezium"
    INVHOUSE = "invhouse"
    MDIAMOND = "Mdiamond"
    MSQUARE = "Msquare"
    MCIRCLE = "Mcircle"
    RECORD = "record"
    MRECORD = "Mrecord"
    RECT = "rect"
    RECTANGLE = "rectangle"
    SQUARE = "square"
    STAR = "star"
    NONE = "none"
    UNDERLINE = "underline"
    CYLINDER = "cylinder"
    NOTE = "note"
    TAB = "tab"
    FOLDER = "folder"
    BOX3D = "box3d"
    COMPONENT = "component"
    PROMOTER = "promoter"
    CDS = "cds"
    TERMINATOR = "terminator"
    UTR = "utr"
    PRIMERSITE = "primersite"
    RESTRICTIONSITE = "restrictionsite"
    FIVEPOVERHANG = "fivepoverhang"
    THREEPOVERHANG = "threepoverhang"
    NOVERHANG = "noverhang"
    ASSEMBLY = "assembly"
    SIGNATURE = "signature"
    INSULATOR = "insulator"
    RIBOSITE = "ribosite"
    RNASTAB = "rnastab"
    PROTEASESITE = "proteasesite"
    PROTEINSTAB = "proteinstab"
    RPROMOTER = "rpromoter"
    RARROW = "rarrow"
    LARROW = "larrow"
    LPROMOTER = "lpromoter"


class ArrowType(Enum):
    """Arrow types for edge heads and tails."""
    NORMAL = "normal"
    ARROW = "arrow"
    INV = "inv"
    DOT = "dot"
    INVDOT = "invdot"
    INVO = "invo"
    NONE = "none"
    EMPTY = "empty"
    TEE = "tee"
    DIAMOND = "diamond"
    INVDIAMOND = "invdiamond"
    EDIAMOND = "ediamond"
    CROW = "crow"
    BOX = "box"
    VEE = "vee"
    LNORMAL = "lnormal"
    LARROW = "larrow"
    RNORMAL = "rnormal"
    RARROW = "rarrow"
    ODOT = "odot"
    OLNORMAL = "olnormal"
    ORNORMAL = "ornormal"


class Color:
    """Common color constants for Graphviz."""
    # Basic colors
    BLACK = "black"
    WHITE = "white"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    CYAN = "cyan"
    MAGENTA = "magenta"
    ORANGE = "orange"
    PURPLE = "purple"
    PINK = "pink"
    BROWN = "brown"
    GRAY = "gray"
    GREY = "grey"
    
    # Extended colors
    LIGHTGRAY = "lightgray"
    LIGHTGREY = "lightgrey"
    DARKGRAY = "darkgray"
    DARKGREY = "darkgrey"
    LIGHTBLUE = "lightblue"
    LIGHTGREEN = "lightgreen"
    LIGHTYELLOW = "lightyellow"
    LIGHTPINK = "lightpink"
    LIGHTCYAN = "lightcyan"
    LIGHTMAGENTA = "lightmagenta"
    DARKBLUE = "darkblue"
    DARKGREEN = "darkgreen"
    DARKRED = "darkred"
    DARKORANGE = "darkorange"
    DARKYELLOW = "darkyellow"
    FORESTGREEN = "forestgreen"
    NAVY = "navy"
    MAROON = "maroon"
    TEAL = "teal"
    OLIVE = "olive"
    AQUA = "aqua"
    FUCHSIA = "fuchsia"
    LIME = "lime"
    SILVER = "silver"
    CORAL = "coral"
    GOLD = "gold"
    KHAKI = "khaki"
    LAVENDER = "lavender"
    LINEN = "linen"
    SALMON = "salmon"
    TAN = "tan"
    TURQUOISE = "turquoise"
    VIOLET = "violet"
    WHEAT = "wheat"
    
    @staticmethod
    def rgb(r: int, g: int, b: int) -> str:
        """Create RGB color string."""
        return f"#{r:02x}{g:02x}{b:02x}"
    
    @staticmethod
    def rgba(r: int, g: int, b: int, a: float) -> str:
        """Create RGBA color string."""
        return f"#{r:02x}{g:02x}{b:02x}{int(a * 255):02x}"


class RankDir(Enum):
    """Rank direction for graph layout."""
    TB = "TB"  # Top to bottom
    LR = "LR"  # Left to right
    BT = "BT"  # Bottom to top
    RL = "RL"  # Right to left


class Style(Enum):
    """Common style values for nodes and edges."""
    SOLID = "solid"
    DASHED = "dashed"
    DOTTED = "dotted"
    BOLD = "bold"
    ROUNDED = "rounded"
    DIAGONALS = "diagonals"
    FILLED = "filled"
    STRIPED = "striped"
    WEDGED = "wedged"
    INVIS = "invis"


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class DotAttribute:
    """Container for DOT attribute with optional HTML escaping."""
    key: str
    value: Any
    escape: bool = True
    
    # Attributes that should not be quoted (bare values)
    BARE_ATTRS = {'shape', 'style', 'dir', 'arrowhead', 'arrowtail', 'arrowsize',
                  'layout', 'rankdir', 'splines', 'compound', 'constraint', 'strict',
                  'bgcolor', 'color', 'fillcolor', 'fontcolor', 'labelfontcolor',
                  'headlabel', 'taillabel'}
    
    def to_dot(self) -> str:
        """Convert attribute to DOT format."""
        if self.value is None:
            return ""
        
        # Check if this is a bare attribute
        is_bare = self.key in self.BARE_ATTRS
        
        if isinstance(self.value, bool):
            val = "true" if self.value else "false"
        elif isinstance(self.value, (int, float)):
            val = str(self.value)
        elif isinstance(self.value, Enum):
            val = self.value.value
        else:
            val = str(self.value)
            if not is_bare and self.escape and not val.startswith("<"):
                # Escape special characters unless HTML label or bare attribute
                val = self._escape_string(val)
        
        return f'{self.key}={val}'
    
    def _escape_string(self, s: str) -> str:
        """Escape special characters for DOT format."""
        # DOT strings need escaping for quotes and backslashes
        s = s.replace('\\', '\\\\')
        s = s.replace('"', '\\"')
        return f'"{s}"'


@dataclass
class Node:
    """DOT node representation."""
    name: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate node name."""
        if not self.name:
            raise ValueError("Node name cannot be empty")
    
    def set(self, key: str, value: Any) -> 'Node':
        """Set an attribute and return self for chaining."""
        self.attributes[key] = value
        return self
    
    def label(self, text: str, html: bool = False) -> 'Node':
        """Set node label."""
        if html:
            # Only wrap if not already wrapped
            if text.startswith('<') and text.endswith('>'):
                self.attributes['label'] = text
            else:
                self.attributes['label'] = f"<{text}>"
        else:
            self.attributes['label'] = text
        return self
    
    def shape(self, shape: Union[NodeShape, str]) -> 'Node':
        """Set node shape."""
        if isinstance(shape, NodeShape):
            self.attributes['shape'] = shape.value
        else:
            self.attributes['shape'] = shape
        return self
    
    def color(self, color: str) -> 'Node':
        """Set node color (border/fill)."""
        self.attributes['color'] = color
        return self
    
    def fillcolor(self, color: str) -> 'Node':
        """Set node fill color."""
        self.attributes['fillcolor'] = color
        self.attributes['style'] = 'filled'
        return self
    
    def style(self, style: Union[Style, str]) -> 'Node':
        """Set node style."""
        if isinstance(style, Style):
            self.attributes['style'] = style.value
        else:
            self.attributes['style'] = style
        return self
    
    def width(self, width: float) -> 'Node':
        """Set node width in inches."""
        self.attributes['width'] = width
        return self
    
    def height(self, height: float) -> 'Node':
        """Set node height in inches."""
        self.attributes['height'] = height
        return self
    
    def fontsize(self, size: int) -> 'Node':
        """Set font size."""
        self.attributes['fontsize'] = size
        return self
    
    def fontname(self, name: str) -> 'Node':
        """Set font name."""
        self.attributes['fontname'] = name
        return self
    
    def tooltip(self, text: str) -> 'Node':
        """Set tooltip text (for SVG output)."""
        self.attributes['tooltip'] = text
        return self
    
    def url(self, url: str) -> 'Node':
        """Set URL for clickable node."""
        self.attributes['URL'] = url
        return self
    
    def image(self, path: str) -> 'Node':
        """Set node image."""
        self.attributes['image'] = path
        return self
    
    def to_dot(self) -> str:
        """Convert node to DOT format."""
        # Escape node name if needed
        name = self._escape_id(self.name)
        
        if not self.attributes:
            return f"    {name};"
        
        attrs = self._format_attributes()
        return f"    {name} [{attrs}];"
    
    def _escape_id(self, name: str) -> str:
        """Escape identifier for DOT format."""
        # If it's a valid identifier, return as-is
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
            return name
        # Otherwise, quote it
        return f'"{name}"'
    
    def _format_attributes(self) -> str:
        """Format attributes as DOT attribute list."""
        # Attributes that should not be quoted (bare values)
        bare_attrs = {'shape', 'style', 'dir', 'arrowhead', 'arrowtail', 'arrowsize',
                      'layout', 'rankdir', 'splines', 'compound', 'constraint',
                      'bgcolor', 'color', 'fillcolor', 'fontcolor'}
        
        parts = []
        for key, value in self.attributes.items():
            # Handle enum values - convert to their string value
            if isinstance(value, Enum):
                val = value.value
            elif isinstance(value, bool):
                val = "true" if value else "false"
            elif isinstance(value, (int, float)):
                val = str(value)
            else:
                val = str(value)
            
            if key == 'label' and val.startswith('<'):
                # HTML label - don't escape
                parts.append(f'label={val}')
            elif key in bare_attrs:
                # Bare attribute - no quotes
                parts.append(f'{key}={val}')
            else:
                # String value - needs quotes
                escaped = self._escape_string(val)
                parts.append(f'{key}="{escaped}"')
        return ', '.join(parts)
    
    def _escape_string(self, s: str) -> str:
        """Escape special characters for DOT format."""
        s = s.replace('\\', '\\\\')
        s = s.replace('"', '\\"')
        return s


@dataclass
class Edge:
    """DOT edge representation."""
    source: str
    target: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    directed: bool = True
    
    def __post_init__(self):
        """Validate edge endpoints."""
        if not self.source or not self.target:
            raise ValueError("Edge source and target cannot be empty")
    
    def set(self, key: str, value: Any) -> 'Edge':
        """Set an attribute and return self for chaining."""
        self.attributes[key] = value
        return self
    
    def label(self, text: str, html: bool = False) -> 'Edge':
        """Set edge label."""
        if html:
            # Only wrap if not already wrapped
            if text.startswith('<') and text.endswith('>'):
                self.attributes['label'] = text
            else:
                self.attributes['label'] = f"<{text}>"
        else:
            self.attributes['label'] = text
        return self
    
    def color(self, color: str) -> 'Edge':
        """Set edge color."""
        self.attributes['color'] = color
        return self
    
    def style(self, style: Union[Style, str]) -> 'Edge':
        """Set edge style."""
        if isinstance(style, Style):
            self.attributes['style'] = style.value
        else:
            self.attributes['style'] = style
        return self
    
    def penwidth(self, width: float) -> 'Edge':
        """Set edge pen width."""
        self.attributes['penwidth'] = width
        return self
    
    def weight(self, weight: float) -> 'Edge':
        """Set edge weight for layout."""
        self.attributes['weight'] = weight
        return self
    
    def arrowhead(self, arrow: Union[ArrowType, str]) -> 'Edge':
        """Set arrow head type."""
        if isinstance(arrow, ArrowType):
            self.attributes['arrowhead'] = arrow.value
        else:
            self.attributes['arrowhead'] = arrow
        return self
    
    def arrowtail(self, arrow: Union[ArrowType, str]) -> 'Edge':
        """Set arrow tail type."""
        if isinstance(arrow, ArrowType):
            self.attributes['arrowtail'] = arrow.value
        else:
            self.attributes['arrowtail'] = arrow
        return self
    
    def arrowsize(self, size: float) -> 'Edge':
        """Set arrow size."""
        self.attributes['arrowsize'] = size
        return self
    
    def dir(self, direction: str) -> 'Edge':
        """Set edge direction: 'forward', 'back', 'both', 'none'."""
        self.attributes['dir'] = direction
        return self
    
    def constraint(self, value: bool) -> 'Edge':
        """Set if edge affects ranking."""
        self.attributes['constraint'] = value
        return self
    
    def to_dot(self) -> str:
        """Convert edge to DOT format."""
        # Escape identifiers
        source = self._escape_id(self.source)
        target = self._escape_id(self.target)
        
        # Use correct edge operator
        op = "->" if self.directed else "--"
        
        if not self.attributes:
            return f"    {source} {op} {target};"
        
        attrs = self._format_attributes()
        return f"    {source} {op} {target} [{attrs}];"
    
    def _escape_id(self, name: str) -> str:
        """Escape identifier for DOT format."""
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
            return name
        return f'"{name}"'
    
    def _format_attributes(self) -> str:
        """Format attributes as DOT attribute list."""
        # Attributes that should not be quoted (bare values)
        bare_attrs = {'shape', 'style', 'dir', 'arrowhead', 'arrowtail', 'arrowsize',
                      'layout', 'rankdir', 'splines', 'compound', 'constraint',
                      'bgcolor', 'color', 'fillcolor', 'fontcolor'}
        
        parts = []
        for key, value in self.attributes.items():
            # Handle enum values - convert to their string value
            if isinstance(value, Enum):
                val = value.value
            elif isinstance(value, bool):
                val = "true" if value else "false"
            elif isinstance(value, (int, float)):
                val = str(value)
            else:
                val = str(value)
            
            if key == 'label' and val.startswith('<'):
                parts.append(f'label={val}')
            elif key in bare_attrs:
                parts.append(f'{key}={val}')
            else:
                escaped = self._escape_string(val)
                parts.append(f'{key}="{escaped}"')
        return ', '.join(parts)
    
    def _escape_string(self, s: str) -> str:
        """Escape special characters for DOT format."""
        s = s.replace('\\', '\\\\')
        s = s.replace('"', '\\"')
        return s


@dataclass
class Subgraph:
    """DOT subgraph representation."""
    name: Optional[str] = None
    is_cluster: bool = False
    attributes: Dict[str, Any] = field(default_factory=dict)
    nodes: List[Node] = field(default_factory=list)
    edges: List[Edge] = field(default_factory=list)
    subgraphs: List['Subgraph'] = field(default_factory=list)
    node_defaults: Dict[str, Any] = field(default_factory=dict)
    edge_defaults: Dict[str, Any] = field(default_factory=dict)
    
    def set(self, key: str, value: Any) -> 'Subgraph':
        """Set a graph attribute."""
        self.attributes[key] = value
        return self
    
    def label(self, text: str) -> 'Subgraph':
        """Set subgraph label."""
        self.attributes['label'] = text
        return self
    
    def style(self, style: Union[Style, str]) -> 'Subgraph':
        """Set subgraph style."""
        if isinstance(style, Style):
            self.attributes['style'] = style.value
        else:
            self.attributes['style'] = style
        return self
    
    def color(self, color: str) -> 'Subgraph':
        """Set subgraph color."""
        self.attributes['color'] = color
        return self
    
    def bgcolor(self, color: str) -> 'Subgraph':
        """Set subgraph background color."""
        self.attributes['bgcolor'] = color
        return self
    
    def add_node(self, node: Union[Node, str], **attrs) -> Node:
        """Add a node to the subgraph."""
        if isinstance(node, str):
            node = Node(node, attrs)
        self.nodes.append(node)
        return node
    
    def add_edge(self, source: str, target: str, **attrs) -> Edge:
        """Add an edge to the subgraph."""
        edge = Edge(source, target, attrs)
        self.edges.append(edge)
        return edge
    
    def add_subgraph(self, name: Optional[str] = None, is_cluster: bool = False) -> 'Subgraph':
        """Add a nested subgraph."""
        sub = Subgraph(name, is_cluster)
        self.subgraphs.append(sub)
        return sub
    
    def set_node_defaults(self, **attrs) -> 'Subgraph':
        """Set default node attributes."""
        self.node_defaults.update(attrs)
        return self
    
    def set_edge_defaults(self, **attrs) -> 'Subgraph':
        """Set default edge attributes."""
        self.edge_defaults.update(attrs)
        return self
    
    def to_dot(self, indent: int = 1) -> str:
        """Convert subgraph to DOT format."""
        lines = []
        ind = '    ' * indent
        
        # Determine subgraph name
        if self.is_cluster:
            sub_name = f"cluster_{self.name}" if self.name else "cluster"
        else:
            sub_name = self.name or ""
        
        # Subgraph header
        if sub_name:
            lines.append(f"{ind}subgraph {self._escape_id(sub_name)} {{")
        else:
            lines.append(f"{ind}{{")
        
        # Graph attributes
        for key, value in self.attributes.items():
            attr = DotAttribute(key, value)
            lines.append(f"{ind}    {attr.to_dot()};")
        
        # Node defaults
        if self.node_defaults:
            attrs = self._format_attrs(self.node_defaults)
            lines.append(f"{ind}    node [{attrs}];")
        
        # Edge defaults
        if self.edge_defaults:
            attrs = self._format_attrs(self.edge_defaults)
            lines.append(f"{ind}    edge [{attrs}];")
        
        # Nodes
        for node in self.nodes:
            lines.append(f"{ind}{node.to_dot().strip()}")
        
        # Edges
        for edge in self.edges:
            lines.append(f"{ind}{edge.to_dot().strip()}")
        
        # Nested subgraphs
        for sub in self.subgraphs:
            lines.append(sub.to_dot(indent + 1))
        
        lines.append(f"{ind}}}")
        return '\n'.join(lines)
    
    def _escape_id(self, name: str) -> str:
        """Escape identifier."""
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
            return name
        return f'"{name}"'
    
    def _format_attrs(self, attrs: Dict[str, Any]) -> str:
        """Format attribute dictionary."""
        parts = []
        for key, value in attrs.items():
            attr = DotAttribute(key, value)
            parts.append(attr.to_dot())
        return ', '.join(parts)


class Graph(Subgraph):
    """DOT graph representation (main graph or digraph)."""
    
    def __init__(
        self,
        name: str = "G",
        graph_type: GraphType = GraphType.DIRECTED,
        strict: bool = False
    ):
        """
        Initialize a DOT graph.
        
        Args:
            name: Graph name
            graph_type: Directed or undirected
            strict: If True, no parallel edges or self-loops
        """
        super().__init__(name)
        self.graph_type = graph_type
        self.strict = strict
        
        # Update edge directed status based on graph type
        self._edge_directed = graph_type == GraphType.DIRECTED
    
    def add_edge(self, source: str, target: str, **attrs) -> Edge:
        """Add an edge with correct direction for graph type."""
        edge = Edge(source, target, attrs, directed=self._edge_directed)
        self.edges.append(edge)
        return edge
    
    def rankdir(self, direction: Union[RankDir, str]) -> 'Graph':
        """Set rank direction for layout."""
        if isinstance(direction, RankDir):
            self.attributes['rankdir'] = direction.value
        else:
            self.attributes['rankdir'] = direction
        return self
    
    def ranksep(self, sep: float) -> 'Graph':
        """Set rank separation."""
        self.attributes['ranksep'] = sep
        return self
    
    def nodesep(self, sep: float) -> 'Graph':
        """Set node separation."""
        self.attributes['nodesep'] = sep
        return self
    
    def size(self, width: float, height: float) -> 'Graph':
        """Set graph size in inches."""
        self.attributes['size'] = f"{width},{height}"
        return self
    
    def dpi(self, dpi: int) -> 'Graph':
        """Set output DPI."""
        self.attributes['dpi'] = dpi
        return self
    
    def bgcolor(self, color: str) -> 'Graph':
        """Set background color."""
        self.attributes['bgcolor'] = color
        return self
    
    def fontname(self, name: str) -> 'Graph':
        """Set default font name."""
        self.attributes['fontname'] = name
        return self
    
    def fontsize(self, size: int) -> 'Graph':
        """Set default font size."""
        self.attributes['fontsize'] = size
        return self
    
    def compound(self, value: bool = True) -> 'Graph':
        """Allow edges between clusters."""
        self.attributes['compound'] = value
        return self
    
    def splines(self, value: str) -> 'Graph':
        """Set edge spline type: 'none', 'line', 'polyline', 'curved', 'ortho', 'spline'."""
        self.attributes['splines'] = value
        return self
    
    def to_dot(self) -> str:
        """Convert graph to DOT format."""
        lines = []
        
        # Graph header
        header_parts = []
        if self.strict:
            header_parts.append("strict")
        header_parts.append(self.graph_type.value)
        header_parts.append(self._escape_id(self.name) if self.name else "")
        header_parts.append("{")
        lines.append(' '.join(header_parts))
        
        # Graph attributes
        for key, value in self.attributes.items():
            attr = DotAttribute(key, value)
            lines.append(f"    {attr.to_dot()};")
        
        # Node defaults
        if self.node_defaults:
            attrs = self._format_attrs(self.node_defaults)
            lines.append(f"    node [{attrs}];")
        
        # Edge defaults
        if self.edge_defaults:
            attrs = self._format_attrs(self.edge_defaults)
            lines.append(f"    edge [{attrs}];")
        
        # Nodes
        for node in self.nodes:
            lines.append(node.to_dot())
        
        # Edges
        for edge in self.edges:
            lines.append(edge.to_dot())
        
        # Subgraphs
        for sub in self.subgraphs:
            lines.append(sub.to_dot())
        
        lines.append("}")
        return '\n'.join(lines)
    
    def render(self, filename: Optional[str] = None) -> str:
        """
        Return DOT source, optionally saving to file.
        
        Args:
            filename: Optional file path to save DOT source
        
        Returns:
            DOT source string
        """
        dot = self.to_dot()
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(dot)
        return dot


# ============================================================================
# Convenience Functions
# ============================================================================

def create_digraph(name: str = "G") -> Graph:
    """Create a directed graph."""
    return Graph(name, GraphType.DIRECTED)


def create_graph(name: str = "G") -> Graph:
    """Create an undirected graph."""
    return Graph(name, GraphType.UNDIRECTED)


def html_table(
    rows: List[List[str]],
    border: int = 0,
    cellborder: int = 1,
    cellspacing: int = 0,
    cellpadding: int = 4,
    bgcolor: Optional[str] = None
) -> str:
    """
    Create an HTML table label for nodes.
    
    Args:
        rows: List of rows, each row is a list of cell contents
        border: Table border width
        cellborder: Cell border width
        cellspacing: Cell spacing
        cellpadding: Cell padding
        bgcolor: Background color
    
    Returns:
        HTML table string for DOT label
    
    Example:
        >>> html_table([["Name", "Value"], ["foo", "bar"]])
    """
    parts = [f'<TABLE BORDER="{border}" CELLBORDER="{cellborder}" CELLSPACING="{cellspacing}" CELLPADDING="{cellpadding}"']
    if bgcolor:
        parts.append(f' BGCOLOR="{bgcolor}"')
    parts.append('>')
    
    for row in rows:
        parts.append('<TR>')
        for cell in row:
            parts.append(f'<TD>{cell}</TD>')
        parts.append('</TR>')
    
    parts.append('</TABLE>')
    return ''.join(parts)


def record_label(fields: List[str], vertical: bool = False) -> str:
    """
    Create a record-based label for nodes.
    
    Args:
        fields: List of field labels
        vertical: If True, arrange fields vertically
    
    Returns:
        Record label string (without quotes - will be added by DOT formatter)
    
    Example:
        >>> record_label(["header", "body", "footer"])
    """
    sep = " | " if vertical else " | "
    return sep.join(fields)  # Don't add quotes here


def create_state_machine(
    states: List[str],
    transitions: List[Tuple[str, str, Optional[str]]],
    initial: Optional[str] = None,
    accepting: Optional[List[str]] = None,
    name: str = "StateMachine"
) -> Graph:
    """
    Create a state machine diagram.
    
    Args:
        states: List of state names
        transitions: List of (from_state, to_state, label) tuples
        initial: Initial state name
        accepting: List of accepting state names
        name: Graph name
    
    Returns:
        Graph representing the state machine
    
    Example:
        >>> create_state_machine(
        ...     states=["idle", "running", "done"],
        ...     transitions=[("idle", "running", "start"), ("running", "done", "finish")],
        ...     initial="idle",
        ...     accepting=["done"]
        ... )
    """
    g = create_digraph(name)
    g.rankdir(RankDir.LR)
    
    # Add initial state marker
    if initial:
        g.add_node("__start", shape=NodeShape.POINT, width=0.2)
        g.add_edge("__start", initial)
    
    # Add states
    accepting = accepting or []
    for state in states:
        if state in accepting:
            # Double circle for accepting states
            g.add_node(state, shape=NodeShape.DOUBLECIRCLE)
        else:
            g.add_node(state, shape=NodeShape.CIRCLE)
    
    # Add transitions
    for from_state, to_state, label in transitions:
        edge = g.add_edge(from_state, to_state)
        if label:
            edge.label(label)
    
    return g


def create_tree(
    nodes: Dict[str, List[str]],
    node_labels: Optional[Dict[str, str]] = None,
    name: str = "Tree"
) -> Graph:
    """
    Create a tree diagram.
    
    Args:
        nodes: Dict mapping parent node to list of children
        node_labels: Optional dict mapping node names to display labels
        name: Graph name
    
    Returns:
        Graph representing the tree
    
    Example:
        >>> create_tree({
        ...     "root": ["child1", "child2"],
        ...     "child1": ["grandchild1"]
        ... })
    """
    g = create_digraph(name)
    g.rankdir(RankDir.TB)
    
    node_labels = node_labels or {}
    
    # Track all nodes
    all_nodes = set()
    
    # Add edges (nodes are created implicitly)
    for parent, children in nodes.items():
        all_nodes.add(parent)
        for child in children:
            all_nodes.add(child)
            g.add_edge(parent, child)
    
    # Apply labels
    for node_name in all_nodes:
        if node_name in node_labels:
            # Find and update the node
            for node in g.nodes:
                if node.name == node_name:
                    node.label(node_labels[node_name])
                    break
    
    return g


def create_flowchart(
    steps: List[Tuple[str, str, str, Optional[str]]],
    name: str = "Flowchart"
) -> Graph:
    """
    Create a flowchart.
    
    Args:
        steps: List of (from_node, to_node, label, shape) tuples
        name: Graph name
    
    Returns:
        Graph representing the flowchart
    
    Example:
        >>> create_flowchart([
        ...     ("start", "process", "begin", NodeShape.OVAL),
        ...     ("process", "decision", "done", NodeShape.BOX),
        ...     ("decision", "end", "yes", NodeShape.DIAMOND)
        ... ])
    """
    g = create_digraph(name)
    g.rankdir(RankDir.TB)
    
    added_nodes = set()
    
    for from_node, to_node, label, shape in steps:
        # Add nodes if not already added
        if from_node not in added_nodes:
            node = g.add_node(from_node)
            if shape:
                if isinstance(shape, NodeShape):
                    node.shape(shape)
                else:
                    node.shape(shape)
            added_nodes.add(from_node)
        
        if to_node not in added_nodes:
            node = g.add_node(to_node)
            if shape:
                if isinstance(shape, NodeShape):
                    node.shape(shape)
                else:
                    node.shape(shape)
            added_nodes.add(to_node)
        
        # Add edge
        edge = g.add_edge(from_node, to_node)
        if label:
            edge.label(label)
    
    return g


def create_cluster_diagram(
    clusters: Dict[str, List[str]],
    edges: List[Tuple[str, str, Optional[str]]],
    name: str = "Clusters"
) -> Graph:
    """
    Create a diagram with clustered nodes.
    
    Args:
        clusters: Dict mapping cluster name to list of node names
        edges: List of (from_node, to_node, label) tuples
        name: Graph name
    
    Returns:
        Graph with clusters
    
    Example:
        >>> create_cluster_diagram(
        ...     clusters={"group1": ["a", "b"], "group2": ["c", "d"]},
        ...     edges=[("a", "c", "connect")]
        ... )
    """
    g = create_digraph(name)
    g.compound(True)
    
    # Create subgraphs for clusters
    for cluster_name, node_names in clusters.items():
        sub = g.add_subgraph(cluster_name, is_cluster=True)
        sub.label(cluster_name)
        for node_name in node_names:
            sub.add_node(node_name)
    
    # Add edges
    for from_node, to_node, label in edges:
        edge = g.add_edge(from_node, to_node)
        if label:
            edge.label(label)
    
    return g


def quick_graph(
    nodes: List[str],
    edges: List[Tuple[str, str]],
    directed: bool = True,
    name: str = "G"
) -> Graph:
    """
    Quickly create a simple graph.
    
    Args:
        nodes: List of node names
        edges: List of (from, to) tuples
        directed: True for directed graph
        name: Graph name
    
    Returns:
        Simple graph
    
    Example:
        >>> quick_graph(["a", "b", "c"], [("a", "b"), ("b", "c")])
    """
    g = Graph(name, GraphType.DIRECTED if directed else GraphType.UNDIRECTED)
    
    for node in nodes:
        g.add_node(node)
    
    for source, target in edges:
        g.add_edge(source, target)
    
    return g


# ============================================================================
# DOT Parsing (Basic)
# ============================================================================

def parse_dot(dot_string: str) -> Dict[str, Any]:
    """
    Parse a simple DOT string into a dictionary representation.
    
    This is a basic parser that handles common DOT structures.
    For complex DOT files, consider using a specialized parser.
    
    Args:
        dot_string: DOT format string
    
    Returns:
        Dictionary with graph structure
    
    Example:
        >>> parse_dot('digraph G { a -> b; }')
        {'type': 'digraph', 'name': 'G', 'nodes': [], 'edges': [('a', 'b', {})]}
    """
    result = {
        'type': 'graph',
        'name': '',
        'strict': False,
        'nodes': [],
        'edges': [],
        'attributes': {},
        'subgraphs': []
    }
    
    # Remove comments
    dot_string = re.sub(r'//.*$', '', dot_string, flags=re.MULTILINE)
    dot_string = re.sub(r'/\*.*?\*/', '', dot_string, flags=re.DOTALL)
    
    # Check for strict
    if dot_string.strip().startswith('strict'):
        result['strict'] = True
        dot_string = dot_string.strip()[6:].strip()
    
    # Check graph type
    if dot_string.strip().startswith('digraph'):
        result['type'] = 'digraph'
        dot_string = dot_string.strip()[8:].strip()
    elif dot_string.strip().startswith('graph'):
        result['type'] = 'graph'
        dot_string = dot_string.strip()[6:].strip()
    
    # Extract name (before first {)
    brace_idx = dot_string.find('{')
    if brace_idx > 0:
        result['name'] = dot_string[:brace_idx].strip()
        dot_string = dot_string[brace_idx:]
    
    # Simple edge pattern
    edge_pattern = r'(\w+)\s*(->|--)\s*(\w+)(?:\s*\[([^\]]*)\])?;'
    
    for match in re.finditer(edge_pattern, dot_string):
        source = match.group(1)
        target = match.group(3)
        attrs_str = match.group(4) or ''
        
        # Parse attributes
        attrs = {}
        if attrs_str:
            attr_pattern = r'(\w+)\s*=\s*(?:"([^"]*)"|(\w+))'
            for attr_match in re.finditer(attr_pattern, attrs_str):
                key = attr_match.group(1)
                value = attr_match.group(2) or attr_match.group(3)
                attrs[key] = value
        
        result['edges'].append((source, target, attrs))
    
    # Simple node pattern
    node_pattern = r'(\w+)(?:\s*\[([^\]]*)\])?;'
    
    for match in re.finditer(node_pattern, dot_string):
        name = match.group(1)
        attrs_str = match.group(2) or ''
        
        # Skip if this is part of an edge
        if any(name in (e[0], e[1]) for e in result['edges']):
            continue
        
        # Parse attributes
        attrs = {}
        if attrs_str:
            attr_pattern = r'(\w+)\s*=\s*(?:"([^"]*)"|(\w+))'
            for attr_match in re.finditer(attr_pattern, attrs_str):
                key = attr_match.group(1)
                value = attr_match.group(2) or attr_match.group(3)
                attrs[key] = value
        
        result['nodes'].append((name, attrs))
    
    return result


# ============================================================================
# Utility Functions
# ============================================================================

def escape_dot_string(s: str) -> str:
    """Escape a string for use in DOT format."""
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '\\r')
    s = s.replace('\t', '\\t')
    return s


def is_valid_id(name: str) -> bool:
    """Check if a name is a valid DOT identifier."""
    return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name))


def quote_id(name: str) -> str:
    """Quote an identifier if needed."""
    if is_valid_id(name):
        return name
    return f'"{escape_dot_string(name)}"'


if __name__ == '__main__':
    # Quick demo
    print("=== Basic Graph ===")
    g = create_digraph("demo")
    g.add_node("A").label("Start").shape(NodeShape.OVAL).fillcolor(Color.LIGHTBLUE)
    g.add_node("B").label("Process").shape(NodeShape.BOX).fillcolor(Color.LIGHTGREEN)
    g.add_node("C").label("End").shape(NodeShape.DOUBLECIRCLE).fillcolor(Color.LIGHTPINK)
    
    g.add_edge("A", "B").label("begin")
    g.add_edge("B", "C").label("finish")
    
    print(g.to_dot())
    
    print("\n=== State Machine ===")
    sm = create_state_machine(
        states=["idle", "active", "done"],
        transitions=[
            ("idle", "active", "start"),
            ("active", "active", "work"),
            ("active", "done", "finish"),
            ("done", "idle", "reset")
        ],
        initial="idle",
        accepting=["done"]
    )
    print(sm.to_dot())
    
    print("\n=== Tree ===")
    tree = create_tree({
        "root": ["left", "right"],
        "left": ["ll", "lr"],
        "right": ["rl", "rr"]
    })
    print(tree.to_dot())