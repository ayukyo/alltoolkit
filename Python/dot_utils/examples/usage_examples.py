#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - DOT Utilities Usage Examples
==========================================
Demonstrates various use cases for the Graphviz DOT utilities module.
"""

import sys
import os

# Add module to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dot_utils.mod import (
    Graph, Node, Edge, Subgraph,
    GraphType, NodeShape, ArrowType, Style, Color, RankDir,
    create_digraph, create_graph,
    html_table, record_label,
    create_state_machine, create_tree, create_flowchart,
    create_cluster_diagram, quick_graph,
    escape_dot_string
)


def example_basic_graph():
    """Basic directed graph example."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Directed Graph")
    print("=" * 60)
    
    g = create_digraph("example1")
    
    # Add nodes
    g.add_node("A").label("Node A")
    g.add_node("B").label("Node B")
    g.add_node("C").label("Node C")
    
    # Add edges
    g.add_edge("A", "B").label("connects")
    g.add_edge("B", "C").label("leads to")
    g.add_edge("C", "A").label("back").style(Style.DOTTED)
    
    print(g.to_dot())


def example_styled_graph():
    """Graph with various styling options."""
    print("\n" + "=" * 60)
    print("Example 2: Styled Graph with Colors and Shapes")
    print("=" * 60)
    
    g = create_digraph("styled")
    g.rankdir(RankDir.LR).bgcolor(Color.WHITE)
    
    # Styled nodes
    g.add_node("start").shape(NodeShape.OVAL).fillcolor(Color.LIGHTGREEN).label("Start")
    g.add_node("process").shape(NodeShape.BOX).fillcolor(Color.LIGHTBLUE).label("Process")
    g.add_node("decision").shape(NodeShape.DIAMOND).fillcolor(Color.LIGHTYELLOW).label("Decide")
    g.add_node("end").shape(NodeShape.DOUBLECIRCLE).fillcolor(Color.LIGHTPINK).label("End")
    
    # Styled edges
    g.add_edge("start", "process").color(Color.BLUE).penwidth(2)
    g.add_edge("process", "decision").color(Color.GREEN)
    g.add_edge("decision", "end").label("yes").color(Color.GREEN)
    g.add_edge("decision", "process").label("no").color(Color.RED).style(Style.DASHED)
    
    print(g.to_dot())


def example_state_machine():
    """State machine diagram example."""
    print("\n" + "=" * 60)
    print("Example 3: State Machine Diagram")
    print("=" * 60)
    
    sm = create_state_machine(
        states=["idle", "connecting", "connected", "disconnected", "error"],
        transitions=[
            ("idle", "connecting", "connect"),
            ("connecting", "connected", "success"),
            ("connecting", "error", "fail"),
            ("connected", "disconnected", "disconnect"),
            ("connected", "error", "error"),
            ("disconnected", "idle", "reset"),
            ("error", "idle", "reset")
        ],
        initial="idle",
        accepting=["connected"],
        name="ConnectionStateMachine"
    )
    
    print(sm.to_dot())


def example_tree_structure():
    """Tree structure visualization."""
    print("\n" + "=" * 60)
    print("Example 4: Tree Structure")
    print("=" * 60)
    
    tree = create_tree(
        nodes={
            "root": ["child1", "child2", "child3"],
            "child1": ["grandchild1a", "grandchild1b"],
            "child2": ["grandchild2a"],
            "child3": ["grandchild3a", "grandchild3b", "grandchild3c"]
        },
        node_labels={
            "root": "Root",
            "child1": "Left",
            "child2": "Middle",
            "child3": "Right"
        },
        name="FamilyTree"
    )
    
    print(tree.to_dot())


def example_flowchart():
    """Business flowchart example."""
    print("\n" + "=" * 60)
    print("Example 5: Business Process Flowchart")
    print("=" * 60)
    
    fc = create_flowchart(
        steps=[
            ("start", "input", "begin", NodeShape.OVAL),
            ("input", "validate", "received", NodeShape.BOX),
            ("validate", "process", "valid", NodeShape.DIAMOND),
            ("validate", "input", "invalid", None),
            ("process", "output", "complete", NodeShape.BOX),
            ("output", "end", "done", NodeShape.OVAL),
            ("process", "error", "exception", None),
            ("error", "input", "retry", NodeShape.BOX)
        ],
        name="DataProcessFlowchart"
    )
    
    fc.set_node_defaults(shape=NodeShape.BOX)
    
    print(fc.to_dot())


def example_clusters():
    """Graph with clusters (subgraphs)."""
    print("\n" + "=" * 60)
    print("Example 6: Clustered Diagram")
    print("=" * 60)
    
    cd = create_cluster_diagram(
        clusters={
            "Frontend": ["ui", "router", "state"],
            "Backend": ["api", "database", "cache"],
            "Services": ["auth", "logging", "metrics"]
        },
        edges=[
            ("ui", "router", None),
            ("router", "api", "HTTP"),
            ("api", "database", "SQL"),
            ("api", "cache", "Redis"),
            ("api", "auth", "verify"),
            ("state", "ui", "update"),
            ("logging", "metrics", None)
        ],
        name="SystemArchitecture"
    )
    
    cd.compound(True).rankdir(RankDir.LR)
    
    print(cd.to_dot())


def example_html_labels():
    """Nodes with HTML table labels."""
    print("\n" + "=" * 60)
    print("Example 7: HTML Table Labels")
    print("=" * 60)
    
    g = create_digraph("tables")
    g.rankdir(RankDir.TB)
    
    # Node with HTML table label
    table1 = html_table(
        rows=[
            ["<B>Person</B>", ""],
            ["Name", "John Doe"],
            ["Age", "30"],
            ["City", "New York"]
        ],
        border=1,
        cellborder=1,
        bgcolor=Color.LIGHTGRAY
    )
    g.add_node("person").label(table1, html=True).shape(NodeShape.NONE)
    
    table2 = html_table(
        rows=[
            ["<B>Company</B>", ""],
            ["Name", "Tech Corp"],
            ["Employees", "500"]
        ],
        border=1,
        cellborder=1,
        bgcolor=Color.LIGHTBLUE
    )
    g.add_node("company").label(table2, html=True).shape(NodeShape.NONE)
    
    g.add_edge("person", "company").label("works at")
    
    print(g.to_dot())


def example_record_nodes():
    """Record-based node labels."""
    print("\n" + "=" * 60)
    print("Example 8: Record-Based Nodes")
    print("=" * 60)
    
    g = create_digraph("records")
    
    # Horizontal record
    label1 = record_label(["header", "body", "footer"])
    g.add_node("record1").label(label1).shape(NodeShape.RECORD)
    
    # Vertical record
    label2 = record_label(["top", "middle", "bottom"], vertical=True)
    g.add_node("record2").label(label2).shape(NodeShape.MRECORD)
    
    # Complex record
    label3 = record_label(["<f0> left", "<f1> middle", "<f2> right"])
    g.add_node("record3").label(label3).shape(NodeShape.RECORD)
    
    # Edge with port reference
    g.add_edge("record1:f0", "record3:f2").label("connect")
    
    print(g.to_dot())


def example_custom_styling():
    """Advanced custom styling."""
    print("\n" + "=" * 60)
    print("Example 9: Advanced Custom Styling")
    print("=" * 60)
    
    g = create_digraph("advanced")
    g.splines("ortho").dpi(150)
    
    # Node with multiple styles
    node = g.add_node("important")
    node.shape(NodeShape.HEXAGON)
    node.fillcolor(Color.GOLD)
    node.color(Color.ORANGE)
    node.style("filled,rounded")  # Combine styles with comma
    node.fontsize(16)
    node.fontname("Helvetica-Bold")
    
    # Edge with custom arrow
    edge = g.add_edge("important", "target")
    edge.arrowhead(ArrowType.CROW)
    edge.arrowtail(ArrowType.DIAMOND)
    edge.dir("both")
    edge.color(Color.PURPLE)
    edge.penwidth(2)
    edge.weight(10)
    
    # Target node with gradient (wedge style)
    target = g.add_node("target")
    target.shape(NodeShape.CIRCLE)
    target.style(Style.WEDGED)
    target.fillcolor("blue:green:red")
    
    print(g.to_dot())


def example_quick_graph():
    """Quick graph creation."""
    print("\n" + "=" * 60)
    print("Example 10: Quick Graph Creation")
    print("=" * 60)
    
    # Simple directed graph
    g = quick_graph(
        nodes=["a", "b", "c", "d"],
        edges=[("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")],
        directed=True,
        name="Cycle"
    )
    
    print(g.to_dot())
    
    # Simple undirected graph
    print("\n--- Undirected Version ---")
    g2 = quick_graph(
        nodes=["a", "b", "c", "d"],
        edges=[("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")],
        directed=False,
        name="Mesh"
    )
    
    print(g2.to_dot())


def example_nested_subgraphs():
    """Nested subgraphs example."""
    print("\n" + "=" * 60)
    print("Example 11: Nested Subgraphs")
    print("=" * 60)
    
    g = create_digraph("nested")
    
    # Outer cluster
    outer = g.add_subgraph("outer", is_cluster=True)
    outer.label("Outer Cluster").bgcolor(Color.LIGHTGRAY)
    outer.add_node("n1")
    outer.add_node("n2")
    
    # Inner cluster within outer
    inner = outer.add_subgraph("inner", is_cluster=True)
    inner.label("Inner Cluster").bgcolor(Color.LIGHTBLUE)
    inner.add_node("n3")
    inner.add_node("n4")
    
    # Edges
    outer.add_edge("n1", "n2")
    inner.add_edge("n3", "n4")
    g.add_edge("n2", "n3")
    
    print(g.to_dot())


def example_tcp_state_machine():
    """TCP connection state machine."""
    print("\n" + "=" * 60)
    print("Example 12: TCP Connection State Machine")
    print("=" * 60)
    
    sm = create_state_machine(
        states=[
            "CLOSED", "LISTEN", "SYN_SENT", "SYN_RECEIVED",
            "ESTABLISHED", "FIN_WAIT_1", "FIN_WAIT_2",
            "CLOSING", "TIME_WAIT", "CLOSE_WAIT", "LAST_ACK"
        ],
        transitions=[
            ("CLOSED", "LISTEN", "open"),
            ("LISTEN", "SYN_SENT", "send SYN"),
            ("LISTEN", "SYN_RECEIVED", "recv SYN"),
            ("SYN_SENT", "ESTABLISHED", "recv SYN+ACK"),
            ("SYN_RECEIVED", "ESTABLISHED", "send ACK"),
            ("ESTABLISHED", "FIN_WAIT_1", "close"),
            ("FIN_WAIT_1", "FIN_WAIT_2", "recv ACK"),
            ("FIN_WAIT_1", "CLOSING", "recv FIN"),
            ("FIN_WAIT_2", "TIME_WAIT", "recv FIN"),
            ("CLOSING", "TIME_WAIT", "recv ACK"),
            ("TIME_WAIT", "CLOSED", "timeout"),
            ("ESTABLISHED", "CLOSE_WAIT", "recv FIN"),
            ("CLOSE_WAIT", "LAST_ACK", "close"),
            ("LAST_ACK", "CLOSED", "recv ACK"),
            ("LISTEN", "CLOSED", "close"),
            ("SYN_SENT", "CLOSED", "close"),
        ],
        initial="CLOSED",
        accepting=["CLOSED"],
        name="TCPStateMachine"
    )
    
    sm.rankdir(RankDir.TB)
    
    print(sm.to_dot())


def example_mind_map():
    """Mind map style diagram."""
    print("\n" + "=" * 60)
    print("Example 13: Mind Map")
    print("=" * 60)
    
    g = create_digraph("mindmap")
    g.rankdir(RankDir.LR)
    
    # Central concept
    center = g.add_node("center")
    center.label("Python Programming").shape(NodeShape.OVAL).fillcolor(Color.LIGHTBLUE).fontsize(18)
    
    # Main topics
    topics = ["Basics", "Data Structures", "OOP", "Libraries", "Web"]
    for topic in topics:
        node = g.add_node(topic)
        node.label(topic).shape(NodeShape.BOX).fillcolor(Color.LIGHTGREEN)
        g.add_edge("center", topic)
    
    # Subtopics
    basics_subs = ["Variables", "Functions", "Loops"]
    for sub in basics_subs:
        node = g.add_node(sub)
        node.label(sub).shape(NodeShape.PLAINTEXT)
        g.add_edge("Basics", sub)
    
    ds_subs = ["Lists", "Dicts", "Sets"]
    for sub in ds_subs:
        node = g.add_node(sub)
        node.label(sub).shape(NodeShape.PLAINTEXT)
        g.add_edge("Data Structures", sub)
    
    print(g.to_dot())


def example_dependency_graph():
    """Software dependency graph."""
    print("\n" + "=" * 60)
    print("Example 14: Dependency Graph")
    print("=" * 60)
    
    g = create_digraph("deps")
    g.rankdir(RankDir.TB)
    
    # Application layer
    app = g.add_subgraph("app", is_cluster=True)
    app.label("Application").bgcolor(Color.LIGHTBLUE)
    app.add_node("main").label("Main App")
    app.add_node("ui").label("UI Module")
    app.add_edge("main", "ui")
    
    # Core layer
    core = g.add_subgraph("core", is_cluster=True)
    core.label("Core").bgcolor(Color.LIGHTGREEN)
    core.add_node("utils").label("Utilities")
    core.add_node("config").label("Config")
    core.add_edge("utils", "config")
    
    # External layer
    ext = g.add_subgraph("external", is_cluster=True)
    ext.label("External").bgcolor(Color.LIGHTYELLOW)
    ext.add_node("lib1").label("Library 1")
    ext.add_node("lib2").label("Library 2")
    
    # Dependencies across layers
    g.add_edge("ui", "utils")
    g.add_edge("utils", "lib1")
    g.add_edge("config", "lib2")
    
    print(g.to_dot())


def run_all_examples():
    """Run all examples."""
    print("=" * 60)
    print("AllToolkit - DOT Utilities Examples")
    print("=" * 60)
    print("\nThese examples generate DOT code that can be rendered")
    print("using Graphviz tools (dot, neato, etc.)")
    print("Install: apt-get install graphviz  # Linux")
    print("Or use: https://dreampuf.github.io/GraphvizOnline/")
    
    examples = [
        example_basic_graph,
        example_styled_graph,
        example_state_machine,
        example_tree_structure,
        example_flowchart,
        example_clusters,
        example_html_labels,
        example_record_nodes,
        example_custom_styling,
        example_quick_graph,
        example_nested_subgraphs,
        example_tcp_state_machine,
        example_mind_map,
        example_dependency_graph,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"Error in {example.__name__}: {e}")
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    run_all_examples()