"""
Tests for Prim's Algorithm Utilities

Comprehensive test suite for minimum spanning tree algorithms.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    PrimGraph, Edge, MSTResult, ForestResult, MSTAlgorithm,
    prim_mst, kruskal_mst, boruvka_mst, minimum_spanning_tree,
    is_connected_graph, get_connected_components, compare_algorithms
)


def test_basic_graph():
    """Test basic graph operations."""
    print("Test: Basic graph operations... ", end="")
    
    g = PrimGraph()
    g.add_edge('A', 'B', 4)
    g.add_edge('B', 'C', 3)
    
    assert g.node_count == 3
    assert g.edge_count == 2  # Undirected
    assert g.has_node('A')
    assert g.has_edge('A', 'B')
    assert g.has_edge('B', 'A')  # Undirected
    assert g.get_edge_weight('A', 'B') == 4
    
    print("PASSED")


def test_add_multiple_edges():
    """Test adding multiple edges at once."""
    print("Test: Add multiple edges... ", end="")
    
    g = PrimGraph()
    g.add_edges([
        ('A', 'B', 1),
        ('B', 'C', 2),
        ('C', 'D'),  # Default weight 1
    ])
    
    assert g.node_count == 4
    assert g.edge_count == 3
    assert g.get_edge_weight('C', 'D') == 1
    
    print("PASSED")


def test_prim_simple():
    """Test Prim's algorithm on a simple graph."""
    print("Test: Prim's algorithm simple... ", end="")
    
    g = PrimGraph()
    g.add_edges([
        ('A', 'B', 1),
        ('B', 'C', 2),
        ('A', 'C', 3),
    ])
    
    mst = g.minimum_spanning_tree()
    
    assert mst.connected
    assert mst.node_count == 3
    assert len(mst.edges) == 2  # MST has n-1 edges
    assert mst.total_weight == 3  # 1 + 2
    
    print("PASSED")


def test_prim_larger_graph():
    """Test Prim's algorithm on a larger graph."""
    print("Test: Prim's algorithm larger graph... ", end="")
    
    g = PrimGraph()
    g.add_edges([
        ('A', 'B', 4),
        ('A', 'C', 2),
        ('B', 'C', 1),
        ('B', 'D', 5),
        ('C', 'D', 8),
        ('C', 'E', 10),
        ('D', 'E', 2),
    ])
    
    mst = g.minimum_spanning_tree()
    
    assert mst.connected
    assert mst.node_count == 5
    assert len(mst.edges) == 4
    # MST should be: B-C (1), A-C (2), D-E (2), A-B (4) or B-D (5) but we need A
    # Actually: B-C (1), D-E (2), A-C (2), B-D (5) = 10
    # Wait, let me recalculate: 
    # We need 4 edges for 5 nodes
    # Cheapest: B-C (1), then D-E (2), then A-C (2), then B-D (5) = 10
    assert mst.total_weight == 10
    
    print("PASSED")


def test_kruskal():
    """Test Kruskal's algorithm."""
    print("Test: Kruskal's algorithm... ", end="")
    
    g = PrimGraph()
    g.add_edges([
        ('A', 'B', 1),
        ('B', 'C', 2),
        ('A', 'C', 3),
        ('C', 'D', 4),
    ])
    
    mst = g.minimum_spanning_tree(algorithm=MSTAlgorithm.KRUSKAL)
    
    assert mst.connected
    assert len(mst.edges) == 3
    assert mst.total_weight == 7  # 1 + 2 + 4
    
    print("PASSED")


def test_boruvka():
    """Test Borůvka's algorithm."""
    print("Test: Borůvka's algorithm... ", end="")
    
    g = PrimGraph()
    g.add_edges([
        ('A', 'B', 1),
        ('B', 'C', 2),
        ('A', 'C', 3),
        ('C', 'D', 4),
        ('D', 'E', 5),
    ])
    
    mst = g.minimum_spanning_tree(algorithm=MSTAlgorithm.BORUVKA)
    
    assert mst.connected
    assert len(mst.edges) == 4
    assert mst.total_weight == 12  # 1 + 2 + 4 + 5
    
    print("PASSED")


def test_algorithms_equivalence():
    """Test that all algorithms produce the same total weight."""
    print("Test: Algorithm equivalence... ", end="")
    
    g = PrimGraph()
    g.add_edges([
        ('A', 'B', 4),
        ('A', 'C', 2),
        ('B', 'C', 1),
        ('B', 'D', 5),
        ('C', 'D', 8),
        ('C', 'E', 10),
        ('D', 'E', 2),
        ('D', 'F', 6),
        ('E', 'F', 3),
    ])
    
    prim_result = g.minimum_spanning_tree(algorithm=MSTAlgorithm.PRIM)
    kruskal_result = g.minimum_spanning_tree(algorithm=MSTAlgorithm.KRUSKAL)
    boruvka_result = g.minimum_spanning_tree(algorithm=MSTAlgorithm.BORUVKA)
    
    assert prim_result.total_weight == kruskal_result.total_weight == boruvka_result.total_weight
    assert prim_result.connected == kruskal_result.connected == boruvka_result.connected
    assert len(prim_result.edges) == len(kruskal_result.edges) == len(boruvka_result.edges)
    
    print("PASSED")


def test_disconnected_graph():
    """Test on a disconnected graph."""
    print("Test: Disconnected graph... ", end="")
    
    g = PrimGraph()
    g.add_edges([('A', 'B', 1), ('B', 'C', 2)])
    g.add_edges([('D', 'E', 3), ('E', 'F', 4)])
    # Components: A-B-C and D-E-F
    
    assert not g.is_connected()
    components = g.get_connected_components()
    assert len(components) == 2
    
    # MST for disconnected graph should only cover one component
    mst = g.minimum_spanning_tree(start='A')
    assert not mst.connected
    assert mst.node_count == 3  # Only A, B, C
    
    print("PASSED")


def test_minimum_spanning_forest():
    """Test minimum spanning forest for disconnected graphs."""
    print("Test: Minimum spanning forest... ", end="")
    
    g = PrimGraph()
    g.add_edges([('A', 'B', 1), ('B', 'C', 2)])  # Component 1, MST weight = 3
    g.add_edges([('D', 'E', 3), ('E', 'F', 4)])  # Component 2, MST weight = 7
    
    forest = g.minimum_spanning_forest()
    
    assert forest.component_count == 2
    assert len(forest.trees) == 2
    assert forest.total_weight == 10  # 3 + 7
    
    print("PASSED")


def test_single_node():
    """Test graph with a single node."""
    print("Test: Single node graph... ", end="")
    
    g = PrimGraph()
    g.add_node('A')
    
    mst = g.minimum_spanning_tree()
    
    assert mst.connected
    assert mst.node_count == 1
    assert len(mst.edges) == 0
    assert mst.total_weight == 0
    
    print("PASSED")


def test_empty_graph():
    """Test empty graph."""
    print("Test: Empty graph... ", end="")
    
    g = PrimGraph()
    
    mst = g.minimum_spanning_tree()
    
    assert not mst.connected
    assert mst.node_count == 0
    assert len(mst.edges) == 0
    
    print("PASSED")


def test_integer_nodes():
    """Test with integer node labels."""
    print("Test: Integer nodes... ", end="")
    
    g = PrimGraph()
    g.add_edges([
        (0, 1, 2),
        (1, 2, 3),
        (0, 2, 4),
    ])
    
    mst = g.minimum_spanning_tree()
    
    assert mst.connected
    assert len(mst.edges) == 2
    assert mst.total_weight == 5  # 2 + 3
    
    print("PASSED")


def test_tuple_nodes():
    """Test with tuple node labels."""
    print("Test: Tuple nodes... ", end="")
    
    g = PrimGraph()
    g.add_edges([
        ((0, 0), (0, 1), 1),
        ((0, 1), (1, 1), 2),
        ((0, 0), (1, 1), 5),
        ((1, 1), (1, 0), 3),
    ])
    
    mst = g.minimum_spanning_tree()
    
    assert mst.connected
    assert len(mst.edges) == 3
    assert mst.total_weight == 6  # 1 + 2 + 3
    
    print("PASSED")


def test_directed_graph_error():
    """Test that directed graphs raise error for MST."""
    print("Test: Directed graph error... ", end="")
    
    g = PrimGraph(directed=True)
    g.add_edge('A', 'B', 1)
    
    try:
        g.minimum_spanning_tree()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "undirected" in str(e).lower()
    
    print("PASSED")


def test_remove_operations():
    """Test remove node and edge operations."""
    print("Test: Remove operations... ", end="")
    
    g = PrimGraph()
    g.add_edges([
        ('A', 'B', 1),
        ('B', 'C', 2),
        ('A', 'C', 3),
    ])
    
    assert g.edge_count == 3
    
    g.remove_edge('A', 'C')
    assert g.edge_count == 2
    assert not g.has_edge('A', 'C')
    
    g.remove_node('B')
    assert g.node_count == 2
    assert g.edge_count == 0
    
    print("PASSED")


def test_from_adjacency_list():
    """Test creating graph from adjacency list."""
    print("Test: From adjacency list... ", end="")
    
    adj = {
        'A': [('B', 1), ('C', 2)],
        'B': [('C', 3)],
        'C': []
    }
    
    g = PrimGraph.from_adjacency_list(adj)
    
    assert g.node_count == 3
    assert g.has_edge('A', 'B')
    assert g.has_edge('A', 'C')
    assert g.has_edge('B', 'C')
    
    mst = g.minimum_spanning_tree()
    assert mst.total_weight == 3  # 1 + 2
    
    print("PASSED")


def test_from_edge_list():
    """Test creating graph from edge list."""
    print("Test: From edge list... ", end="")
    
    edges = [
        ('A', 'B', 1),
        ('B', 'C', 2),
        ('A', 'C'),  # Default weight 1
    ]
    
    g = PrimGraph.from_edge_list(edges)
    
    assert g.node_count == 3
    assert g.edge_count == 3
    assert g.get_edge_weight('A', 'C') == 1
    
    print("PASSED")


def test_from_adjacency_matrix():
    """Test creating graph from adjacency matrix."""
    print("Test: From adjacency matrix... ", end="")
    
    matrix = [
        [0, 1, 4],
        [1, 0, 2],
        [4, 2, 0]
    ]
    
    g = PrimGraph.from_adjacency_matrix(matrix)
    
    assert g.node_count == 3
    assert g.has_edge(0, 1)
    assert g.has_edge(1, 2)
    
    mst = g.minimum_spanning_tree()
    assert mst.total_weight == 3  # 1 + 2
    
    print("PASSED")


def test_convenience_functions():
    """Test convenience functions."""
    print("Test: Convenience functions... ", end="")
    
    # Test with adjacency list
    adj = {
        'A': [('B', 1), ('C', 2)],
        'B': [('C', 3)],
        'C': []
    }
    
    mst = prim_mst(adj)
    assert mst.total_weight == 3
    
    mst = kruskal_mst(adj)
    assert mst.total_weight == 3
    
    mst = boruvka_mst(adj)
    assert mst.total_weight == 3
    
    # Test with edge list
    edges = [('A', 'B', 1), ('B', 'C', 2), ('A', 'C', 3)]
    mst = minimum_spanning_tree(edges)
    assert mst.total_weight == 3
    
    print("PASSED")


def test_compare_algorithms():
    """Test compare_algorithms function."""
    print("Test: Compare algorithms... ", end="")
    
    g = PrimGraph()
    g.add_edges([
        ('A', 'B', 4),
        ('A', 'C', 2),
        ('B', 'C', 1),
        ('B', 'D', 5),
        ('C', 'D', 8),
    ])
    
    results = compare_algorithms(g)
    
    assert 'prim' in results
    assert 'kruskal' in results
    assert 'boruvka' in results
    
    # All should give same weight
    weights = [r.total_weight for r in results.values()]
    assert len(set(weights)) == 1
    
    print("PASSED")


def test_mst_result_methods():
    """Test MSTResult helper methods."""
    print("Test: MSTResult methods... ", end="")
    
    g = PrimGraph()
    g.add_edges([('A', 'B', 1), ('B', 'C', 2), ('A', 'C', 3)])
    
    mst = g.minimum_spanning_tree()
    
    # Test get_edge_list
    edge_list = mst.get_edge_list()
    assert len(edge_list) == 2
    assert all(len(e) == 3 for e in edge_list)
    
    # Test get_adjacency_list
    adj = mst.get_adjacency_list()
    assert 'A' in adj
    assert 'B' in adj
    assert 'C' in adj
    
    print("PASSED")


def test_copy():
    """Test graph copy."""
    print("Test: Graph copy... ", end="")
    
    g1 = PrimGraph()
    g1.add_edges([('A', 'B', 1), ('B', 'C', 2)])
    
    g2 = g1.copy()
    
    assert g2.node_count == g1.node_count
    assert g2.edge_count == g1.edge_count
    
    # Modify g1, g2 should be unchanged
    g1.add_edge('C', 'D', 3)
    
    assert g1.node_count == 4
    assert g2.node_count == 3
    
    print("PASSED")


def test_large_graph():
    """Test with a larger graph for performance."""
    print("Test: Large graph... ", end="")
    
    g = PrimGraph()
    
    # Create a 50-node graph
    for i in range(50):
        for j in range(i + 1, min(i + 5, 50)):
            weight = abs(i - j) + 1
            g.add_edge(i, j, weight)
    
    mst = g.minimum_spanning_tree()
    
    assert mst.connected
    assert mst.node_count == 50
    assert len(mst.edges) == 49  # n-1 edges for MST
    
    print("PASSED")


def test_edge_cases():
    """Test edge cases."""
    print("Test: Edge cases... ", end="")
    
    g = PrimGraph()
    
    # Test has_node and has_edge on empty graph
    assert not g.has_node('A')
    assert not g.has_edge('A', 'B')
    
    # Test get_edge_weight for non-existent edge
    g.add_edge('A', 'B', 1)
    assert g.get_edge_weight('A', 'C') is None
    
    # Test with zero weight edge (MST should still include both edges for 3 nodes)
    g.add_edge('B', 'C', 0)
    mst = g.minimum_spanning_tree()
    assert mst.total_weight == 1  # A-B (1) + B-C (0)
    
    print("PASSED")


def test_is_connected_graph():
    """Test is_connected_graph helper."""
    print("Test: is_connected_graph helper... ", end="")
    
    g1 = PrimGraph()
    g1.add_edges([('A', 'B', 1), ('B', 'C', 2)])
    assert is_connected_graph(g1)
    
    g2 = PrimGraph()
    g2.add_edges([('A', 'B', 1)])
    g2.add_edges([('C', 'D', 2)])
    assert not is_connected_graph(g2)
    
    print("PASSED")


def test_get_connected_components():
    """Test get_connected_components helper."""
    print("Test: get_connected_components helper... ", end="")
    
    g = PrimGraph()
    g.add_edges([('A', 'B', 1), ('B', 'C', 2)])
    g.add_edges([('D', 'E', 3)])
    g.add_node('F')  # Isolated
    
    components = get_connected_components(g)
    
    assert len(components) == 3
    
    # Check component sizes
    sizes = sorted([len(c) for c in components])
    assert sizes == [1, 2, 3]
    
    print("PASSED")


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("Running Prim's Algorithm Tests")
    print("=" * 50 + "\n")
    
    tests = [
        test_basic_graph,
        test_add_multiple_edges,
        test_prim_simple,
        test_prim_larger_graph,
        test_kruskal,
        test_boruvka,
        test_algorithms_equivalence,
        test_disconnected_graph,
        test_minimum_spanning_forest,
        test_single_node,
        test_empty_graph,
        test_integer_nodes,
        test_tuple_nodes,
        test_directed_graph_error,
        test_remove_operations,
        test_from_adjacency_list,
        test_from_edge_list,
        test_from_adjacency_matrix,
        test_convenience_functions,
        test_compare_algorithms,
        test_mst_result_methods,
        test_copy,
        test_large_graph,
        test_edge_cases,
        test_is_connected_graph,
        test_get_connected_components,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)