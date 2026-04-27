#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - DOT Utilities Test Module
=======================================
Comprehensive tests for the Graphviz DOT utilities module.
"""

import sys
import os

# Add module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Graph, Node, Edge, Subgraph,
    GraphType, NodeShape, ArrowType, Style, Color, RankDir,
    create_digraph, create_graph,
    html_table, record_label,
    create_state_machine, create_tree, create_flowchart,
    create_cluster_diagram, quick_graph,
    parse_dot,
    escape_dot_string, is_valid_id, quote_id,
    DotAttribute
)


def test_node_creation():
    """Test node creation and attributes."""
    print("Testing Node creation...")
    
    # Basic node
    node = Node("test")
    assert node.name == "test"
    assert node.attributes == {}
    
    # Node with attributes
    node = Node("test", {"label": "Test Node", "shape": "box"})
    assert node.attributes["label"] == "Test Node"
    
    # Attribute chaining
    node = Node("chain_test")
    node.label("Chained").shape(NodeShape.CIRCLE).color(Color.RED)
    assert node.attributes["label"] == "Chained"
    assert node.attributes["shape"] == "circle"
    assert node.attributes["color"] == "red"
    
    # Fillcolor
    node = Node("filled")
    node.fillcolor(Color.BLUE)
    assert node.attributes["fillcolor"] == "blue"
    assert node.attributes["style"] == "filled"
    
    # Empty name should raise error
    try:
        Node("")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("✓ Node creation tests passed")


def test_node_to_dot():
    """Test node DOT output."""
    print("Testing Node DOT output...")
    
    # Simple node
    node = Node("simple")
    dot = node.to_dot()
    assert "simple;" in dot
    
    # Quoted node name
    node = Node("node with spaces")
    dot = node.to_dot()
    assert '"node with spaces"' in dot
    
    # Node with attributes
    node = Node("attrs")
    node.label("Label").shape(NodeShape.BOX)
    dot = node.to_dot()
    assert "attrs [" in dot
    assert 'label="Label"' in dot
    assert "shape=box" in dot
    
    # HTML label
    node = Node("html")
    node.label("<B>Bold</B>", html=True)
    dot = node.to_dot()
    assert "label=<B>Bold</B>" in dot
    
    # Numeric node name
    node = Node("123")
    dot = node.to_dot()
    assert '"123"' in dot
    
    print("✓ Node DOT output tests passed")


def test_edge_creation():
    """Test edge creation and attributes."""
    print("Testing Edge creation...")
    
    # Basic edge
    edge = Edge("A", "B")
    assert edge.source == "A"
    assert edge.target == "B"
    assert edge.directed == True
    
    # Undirected edge
    edge = Edge("A", "B", directed=False)
    assert edge.directed == False
    
    # Edge with attributes
    edge = Edge("A", "B", {"label": "connect"})
    assert edge.attributes["label"] == "connect"
    
    # Attribute chaining
    edge = Edge("X", "Y")
    edge.label("path").color(Color.GREEN).weight(2.5)
    assert edge.attributes["label"] == "path"
    assert edge.attributes["color"] == "green"
    assert edge.attributes["weight"] == 2.5
    
    # Arrow types
    edge = Edge("A", "B")
    edge.arrowhead(ArrowType.DIAMOND).arrowtail(ArrowType.TEE)
    assert edge.attributes["arrowhead"] == "diamond"
    assert edge.attributes["arrowtail"] == "tee"
    
    print("✓ Edge creation tests passed")


def test_edge_to_dot():
    """Test edge DOT output."""
    print("Testing Edge DOT output...")
    
    # Directed edge
    edge = Edge("A", "B")
    dot = edge.to_dot()
    assert "A -> B;" in dot
    
    # Undirected edge
    edge = Edge("A", "B", directed=False)
    dot = edge.to_dot()
    assert "A -- B;" in dot
    
    # Edge with attributes
    edge = Edge("A", "B")
    edge.label("label").color("red")
    dot = edge.to_dot()
    assert "A -> B [" in dot
    assert 'label="label"' in dot
    assert "color=red" in dot
    
    # Quoted names
    edge = Edge("edge source", "edge target")
    dot = edge.to_dot()
    assert '"edge source"' in dot
    assert '"edge target"' in dot
    
    print("✓ Edge DOT output tests passed")


def test_subgraph():
    """Test subgraph creation."""
    print("Testing Subgraph...")
    
    # Basic subgraph
    sub = Subgraph("sub1")
    sub.add_node("n1")
    sub.add_node("n2")
    sub.add_edge("n1", "n2")
    
    dot = sub.to_dot()
    assert "subgraph sub1" in dot
    assert "n1;" in dot
    assert "n2;" in dot
    assert "n1 -> n2;" in dot
    
    # Cluster subgraph
    cluster = Subgraph("cluster1", is_cluster=True)
    cluster.label("Cluster 1").style(Style.ROUNDED).bgcolor(Color.LIGHTGRAY)
    cluster.add_node("c1")
    
    dot = cluster.to_dot()
    assert "subgraph cluster_cluster1" in dot
    assert 'label="Cluster 1"' in dot
    assert "style=rounded" in dot
    assert "bgcolor=lightgray" in dot
    
    # Default attributes
    sub = Subgraph("defaults")
    sub.set_node_defaults(shape=NodeShape.BOX, color=Color.BLUE)
    sub.set_edge_defaults(color=Color.RED)
    
    dot = sub.to_dot()
    assert "node [shape=box, color=blue]" in dot
    assert "edge [color=red]" in dot
    
    print("✓ Subgraph tests passed")


def test_graph_creation():
    """Test graph creation."""
    print("Testing Graph creation...")
    
    # Directed graph
    g = create_digraph("test_digraph")
    assert g.graph_type == GraphType.DIRECTED
    assert g.name == "test_digraph"
    
    # Undirected graph
    g = create_graph("test_graph")
    assert g.graph_type == GraphType.UNDIRECTED
    assert g.name == "test_graph"
    
    # Strict graph
    g = Graph("strict_g", GraphType.DIRECTED, strict=True)
    assert g.strict == True
    
    print("✓ Graph creation tests passed")


def test_graph_to_dot():
    """Test graph DOT output."""
    print("Testing Graph DOT output...")
    
    # Basic graph
    g = create_digraph("G")
    g.add_node("A")
    g.add_node("B")
    g.add_edge("A", "B")
    
    dot = g.to_dot()
    assert "digraph G" in dot
    assert "{" in dot
    assert "}" in dot
    assert "A;" in dot
    assert "B;" in dot
    assert "A -> B;" in dot
    
    # Undirected graph
    g = create_graph("U")
    g.add_edge("A", "B")
    
    dot = g.to_dot()
    assert "graph U" in dot
    assert "A -- B;" in dot
    
    # Graph attributes
    g = create_digraph("Attrs")
    g.rankdir(RankDir.LR).nodesep(0.5).ranksep(1.0)
    g.set_node_defaults(shape=NodeShape.CIRCLE)
    
    dot = g.to_dot()
    assert "rankdir=LR" in dot
    assert "nodesep=0.5" in dot
    assert "ranksep=1.0" in dot
    assert "node [shape=circle]" in dot
    
    # Strict graph
    g = Graph("S", GraphType.DIRECTED, strict=True)
    dot = g.to_dot()
    assert "strict digraph" in dot
    
    print("✓ Graph DOT output tests passed")


def test_html_table():
    """Test HTML table generation."""
    print("Testing HTML table...")
    
    table = html_table(
        rows=[["Header1", "Header2"], ["Data1", "Data2"]],
        border=1,
        bgcolor="lightgray"
    )
    
    assert "<TABLE" in table
    assert 'BORDER="1"' in table
    assert 'BGCOLOR="lightgray"' in table
    assert "Header1" in table
    assert "Data1" in table
    assert "<TR>" in table
    assert "<TD>" in table
    
    print("✓ HTML table tests passed")


def test_record_label():
    """Test record label generation."""
    print("Testing record label...")
    
    label = record_label(["field1", "field2", "field3"])
    assert "field1" in label
    assert "field2" in label
    assert "field3" in label
    assert "|" in label
    
    label = record_label(["a", "b"], vertical=True)
    assert "a" in label
    assert "b" in label
    
    print("✓ Record label tests passed")


def test_state_machine():
    """Test state machine creation."""
    print("Testing state machine...")
    
    sm = create_state_machine(
        states=["idle", "running", "stopped"],
        transitions=[
            ("idle", "running", "start"),
            ("running", "stopped", "stop"),
            ("stopped", "idle", "reset")
        ],
        initial="idle",
        accepting=["stopped"],
        name="TestStateMachine"
    )
    
    dot = sm.to_dot()
    
    assert "digraph TestStateMachine" in dot
    assert "rankdir" in dot
    assert "__start" in dot  # Initial marker
    assert "__start -> idle" in dot
    assert "idle -> running" in dot
    assert "running -> stopped" in dot
    assert "stopped -> idle" in dot
    assert 'label="start"' in dot
    
    # Accepting state should be doublecircle
    assert "shape=doublecircle" in dot
    
    print("✓ State machine tests passed")


def test_tree():
    """Test tree creation."""
    print("Testing tree...")
    
    tree = create_tree(
        nodes={
            "root": ["left", "right"],
            "left": ["ll", "lr"]
        },
        node_labels={"root": "Root Node"},
        name="TestTree"
    )
    
    dot = tree.to_dot()
    
    assert "digraph TestTree" in dot
    assert "root -> left" in dot
    assert "root -> right" in dot
    assert "left -> ll" in dot
    assert "left -> lr" in dot
    
    print("✓ Tree tests passed")


def test_flowchart():
    """Test flowchart creation."""
    print("Testing flowchart...")
    
    fc = create_flowchart(
        steps=[
            ("start", "process", "begin", NodeShape.OVAL),
            ("process", "decision", "done?", NodeShape.BOX),
            ("decision", "end", "yes", NodeShape.DIAMOND),
            ("decision", "process", "no", None)
        ],
        name="TestFlowchart"
    )
    
    dot = fc.to_dot()
    
    assert "digraph TestFlowchart" in dot
    assert "start -> process" in dot
    assert "process -> decision" in dot
    assert "decision -> end" in dot
    assert "decision -> process" in dot
    assert 'label="begin"' in dot
    assert "shape=oval" in dot
    assert "shape=box" in dot
    assert "shape=diamond" in dot
    
    print("✓ Flowchart tests passed")


def test_cluster_diagram():
    """Test cluster diagram creation."""
    print("Testing cluster diagram...")
    
    cd = create_cluster_diagram(
        clusters={
            "GroupA": ["a1", "a2"],
            "GroupB": ["b1", "b2"]
        },
        edges=[
            ("a1", "b1", "connect"),
            ("a2", "b2", None)
        ],
        name="TestClusters"
    )
    
    dot = cd.to_dot()
    
    assert "digraph TestClusters" in dot
    assert "subgraph cluster_GroupA" in dot
    assert "subgraph cluster_GroupB" in dot
    assert 'label="GroupA"' in dot
    assert 'label="GroupB"' in dot
    assert "a1;" in dot
    assert "a1 -> b1" in dot
    assert 'label="connect"' in dot
    
    print("✓ Cluster diagram tests passed")


def test_quick_graph():
    """Test quick graph creation."""
    print("Testing quick graph...")
    
    g = quick_graph(
        nodes=["a", "b", "c"],
        edges=[("a", "b"), ("b", "c"),
 ("c", "a")],
        directed=True,
        name="Quick"
    )
    
    dot = g.to_dot()
    
    assert "digraph Quick" in dot
    assert "a;" in dot
    assert "b;" in dot
    assert "c;" in dot
    assert "a -> b;" in dot
    assert "b -> c;" in dot
    assert "c -> a;" in dot
    
    # Undirected
    g = quick_graph(["x", "y"], [("x", "y")], directed=False)
    dot = g.to_dot()
    assert "graph G" in dot
    assert "x -- y;" in dot
    
    print("✓ Quick graph tests passed")


def test_parse_dot():
    """Test DOT parsing."""
    print("Testing DOT parsing...")
    
    # Simple graph
    result = parse_dot('digraph G { A -> B; }')
    assert result['type'] == 'digraph'
    assert result['name'] == 'G'
    assert len(result['edges']) == 1
    assert result['edges'][0][0] == 'A'
    assert result['edges'][0][1] == 'B'
    
    # Graph with attributes
    result = parse_dot('digraph Test { A -> B [label="edge"]; B -> C; }')
    assert result['type'] == 'digraph'
    assert len(result['edges']) == 2
    assert result['edges'][0][2].get('label') == 'edge'
    
    # Undirected graph
    result = parse_dot('graph U { A -- B; }')
    assert result['type'] == 'graph'
    
    # Strict graph
    result = parse_dot('strict digraph S { A -> B; }')
    assert result['strict'] == True
    
    print("✓ DOT parsing tests passed")


def test_utility_functions():
    """Test utility functions."""
    print("Testing utility functions...")
    
    # escape_dot_string
    assert escape_dot_string("test") == "test"
    assert escape_dot_string('say "hello"') == 'say \\"hello\\"'
    assert escape_dot_string("line\nbreak") == "line\\nbreak"
    
    # is_valid_id
    assert is_valid_id("valid_id") == True
    assert is_valid_id("Valid123") == True
    assert is_valid_id("_underscore") == True
    assert is_valid_id("123start") == False
    assert is_valid_id("has space") == False
    assert is_valid_id("hyphen-name") == False
    
    # quote_id
    assert quote_id("valid") == "valid"
    assert quote_id("has spaces") == '"has spaces"'
    assert quote_id('with"quote') == '"with\\"quote"'
    
    # Color RGB
    assert Color.rgb(255, 128, 0) == "#ff8000"
    assert Color.rgb(0, 0, 255) == "#0000ff"
    
    print("✓ Utility function tests passed")


def test_complex_graph():
    """Test a complex graph with all features."""
    print("Testing complex graph...")
    
    g = create_digraph("Complex")
    g.rankdir(RankDir.TB).nodesep(0.8).ranksep(1.5)
    g.set_node_defaults(fontsize=12, fontname="Arial")
    g.set_edge_defaults(color=Color.GRAY)
    
    # Nodes with various attributes
    g.add_node("start").shape(NodeShape.OVAL).fillcolor(Color.LIGHTGREEN)
    g.add_node("process").shape(NodeShape.BOX).label("Process Data")
    g.add_node("decision").shape(NodeShape.DIAMOND).label("Check?")
    g.add_node("end").shape(NodeShape.DOUBLECIRCLE).fillcolor(Color.LIGHTPINK)
    
    # Edges with attributes
    g.add_edge("start", "process").label("begin").color(Color.BLUE)
    g.add_edge("process", "decision").label("done").style(Style.DASHED)
    g.add_edge("decision", "end").label("yes").penwidth(2)
    g.add_edge("decision", "process").label("no").style(Style.DOTTED)
    
    # Add a cluster
    cluster = g.add_subgraph("error_handling", is_cluster=True)
    cluster.label("Error Handling").bgcolor(Color.LIGHTYELLOW).style(Style.ROUNDED)
    cluster.add_node("error").shape(NodeShape.BOX).color(Color.RED)
    cluster.add_node("retry").shape(NodeShape.BOX)
    cluster.add_edge("error", "retry").label("retry")
    
    # Connect cluster node to main graph
    g.add_edge("process", "error").label("fail").style(Style.DASHED)
    
    dot = g.to_dot()
    
    # Verify all elements are present
    assert "digraph Complex" in dot
    assert "rankdir=TB" in dot
    assert "nodesep=0.8" in dot
    assert "ranksep=1.5" in dot
    assert "node [fontsize=12" in dot
    assert "edge [color=gray]" in dot
    assert "start" in dot
    assert "process" in dot
    assert "decision" in dot
    assert "end" in dot
    assert "subgraph cluster_error_handling" in dot
    assert "bgcolor=lightyellow" in dot
    assert "error" in dot
    assert "retry" in dot
    
    print("✓ Complex graph tests passed")


def test_render_to_file():
    """Test rendering to file."""
    print("Testing render to file...")
    
    g = create_digraph("FileTest")
    g.add_node("A")
    g.add_node("B")
    g.add_edge("A", "B")
    
    # Render without file
    dot = g.render()
    assert "digraph FileTest" in dot
    
    # Render to temp file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.dot', delete=False) as f:
        temp_path = f.name
    
    try:
        dot = g.render(temp_path)
        
        # Read file and verify
        with open(temp_path, 'r') as f:
            content = f.read()
        assert "digraph FileTest" in content
        assert "A -> B;" in content
    finally:
        os.unlink(temp_path)
    
    print("✓ Render to file tests passed")


def test_node_special_attributes():
    """Test node special attributes like tooltip, URL, image."""
    print("Testing node special attributes...")
    
    node = Node("special")
    node.tooltip("This is a tooltip")
    assert node.attributes["tooltip"] == "This is a tooltip"
    
    node.url("https://example.com")
    assert node.attributes["URL"] == "https://example.com"
    
    node.image("path/to/image.png")
    assert node.attributes["image"] == "path/to/image.png"
    
    node.width(2.5).height(1.5)
    assert node.attributes["width"] == 2.5
    assert node.attributes["height"] == 1.5
    
    print("✓ Node special attributes tests passed")


def test_edge_special_attributes():
    """Test edge special attributes like constraint, dir."""
    print("Testing edge special attributes...")
    
    edge = Edge("A", "B")
    edge.constraint(False)
    assert edge.attributes["constraint"] == False
    
    edge.dir("both")
    assert edge.attributes["dir"] == "both"
    
    edge.arrowsize(1.5)
    assert edge.attributes["arrowsize"] == 1.5
    
    print("✓ Edge special attributes tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("AllToolkit - DOT Utilities Test Suite")
    print("=" * 60)
    
    tests = [
        test_node_creation,
        test_node_to_dot,
        test_edge_creation,
        test_edge_to_dot,
        test_subgraph,
        test_graph_creation,
        test_graph_to_dot,
        test_html_table,
        test_record_label,
        test_state_machine,
        test_tree,
        test_flowchart,
        test_cluster_diagram,
        test_quick_graph,
        test_parse_dot,
        test_utility_functions,
        test_complex_graph,
        test_render_to_file,
        test_node_special_attributes,
        test_edge_special_attributes,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ FAILED: {test.__name__}")
            print(f"  Error: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ ERROR: {test.__name__}")
            print(f"  Exception: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)