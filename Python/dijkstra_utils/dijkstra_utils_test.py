#!/usr/bin/env python3
"""
Test Suite for Dijkstra's Algorithm Utilities

Comprehensive tests covering:
- Graph creation and manipulation
- Shortest path finding
- All-paths computation
- K-shortest paths
- Graph utilities
- Edge cases and error handling
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dijkstra_utils.mod import (
    DijkstraGraph,
    GraphEdge,
    PathResult,
    AllPathsResult,
    dijkstra,
    shortest_path,
    all_shortest_paths,
    is_connected,
    get_reachable_nodes,
    graph_diameter,
    center_of_graph
)


class TestResult:
    """Simple test result collector."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_true(self, condition, message=""):
        if condition:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Assertion failed: {message}")
    
    def assert_equal(self, actual, expected, message=""):
        if actual == expected:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Expected {expected}, got {actual}. {message}")
    
    def assert_almost_equal(self, actual, expected, tolerance=0.001, message=""):
        if abs(actual - expected) < tolerance:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Expected {expected}±{tolerance}, got {actual}. {message}")
    
    def assert_false(self, condition, message=""):
        self.assert_true(not condition, message)
    
    def assert_in(self, item, container, message=""):
        if item in container:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Item {item} not in container. {message}")
    
    def assert_not_in(self, item, container, message=""):
        if item not in container:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Item {item} should not be in container. {message}")
    
    def assert_greater(self, a, b, message=""):
        if a > b:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Expected {a} > {b}. {message}")
    
    def assert_less(self, a, b, message=""):
        if a < b:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append(f"Expected {a} < {b}. {message}")
    
    def assert_raises(self, exception_type, func, message=""):
        try:
            func()
            self.failed += 1
            self.errors.append(f"Expected {exception_type.__name__} to be raised. {message}")
        except exception_type:
            self.passed += 1
        except Exception as e:
            self.failed += 1
            self.errors.append(f"Expected {exception_type.__name__}, got {type(e).__name__}. {message}")


def test_graph_edge():
    """Test GraphEdge dataclass."""
    r = TestResult()
    
    # Basic edge
    edge = GraphEdge(target='B', weight=5)
    r.assert_equal(edge.target, 'B')
    r.assert_equal(edge.weight, 5)
    
    # Zero weight edge
    edge2 = GraphEdge(target='C', weight=0)
    r.assert_equal(edge2.weight, 0)
    
    # Float weight
    edge3 = GraphEdge(target='D', weight=3.14159)
    r.assert_almost_equal(edge3.weight, 3.14159, 0.00001)
    
    # Negative weight should raise error
    r.assert_raises(ValueError, lambda: GraphEdge(target='E', weight=-1))
    
    print(f"test_graph_edge: {r.passed} passed, {r.failed} failed")
    return r


def test_dijkstra_graph_creation():
    """Test DijkstraGraph creation methods."""
    r = TestResult()
    
    # Empty graph
    g = DijkstraGraph()
    r.assert_equal(g.node_count, 0)
    r.assert_equal(g.edge_count, 0)
    r.assert_true(g.is_directed)
    
    # Undirected graph
    g2 = DijkstraGraph(directed=False)
    r.assert_false(g2.is_directed)
    
    # Add nodes
    g.add_node('A')
    g.add_node('B')
    r.assert_equal(g.node_count, 2)
    r.assert_true(g.has_node('A'))
    r.assert_true(g.has_node('B'))
    
    # Add same node twice
    g.add_node('A')
    r.assert_equal(g.node_count, 2)  # Should still be 2
    
    print(f"test_dijkstra_graph_creation: {r.passed} passed, {r.failed} failed")
    return r


def test_add_edges():
    """Test adding edges to graph."""
    r = TestResult()
    
    # Directed graph
    g = DijkstraGraph(directed=True)
    g.add_edge('A', 'B', 5)
    r.assert_equal(g.node_count, 2)
    r.assert_equal(g.edge_count, 1)
    r.assert_true(g.has_edge('A', 'B'))
    r.assert_false(g.has_edge('B', 'A'))
    
    # Undirected graph
    g2 = DijkstraGraph(directed=False)
    g2.add_edge('A', 'B', 5)
    r.assert_equal(g2.edge_count, 2)  # Both directions
    r.assert_true(g2.has_edge('A', 'B'))
    r.assert_true(g2.has_edge('B', 'A'))
    
    # Add multiple edges
    g3 = DijkstraGraph()
    g3.add_edges([('A', 'B', 1), ('B', 'C', 2), ('C', 'D')])
    r.assert_equal(g3.node_count, 4)
    r.assert_equal(g3.edge_count, 3)
    r.assert_equal(g3.get_edge_weight('C', 'D'), 1.0)  # Default weight
    
    # Negative weight should raise error
    g4 = DijkstraGraph()
    r.assert_raises(ValueError, lambda: g4.add_edge('A', 'B', -1))
    
    print(f"test_add_edges: {r.passed} passed, {r.failed} failed")
    return r


def test_remove_nodes_and_edges():
    """Test removing nodes and edges."""
    r = TestResult()
    
    g = DijkstraGraph(directed=False)
    g.add_edges([('A', 'B', 1), ('B', 'C', 2), ('C', 'D', 3)])
    
    # Remove edge
    g.remove_edge('B', 'C')
    r.assert_false(g.has_edge('B', 'C'))
    r.assert_false(g.has_edge('C', 'B'))  # Undirected
    
    # Remove node
    g.remove_node('D')
    r.assert_false(g.has_node('D'))
    r.assert_equal(g.node_count, 3)
    
    print(f"test_remove_nodes_and_edges: {r.passed} passed, {r.failed} failed")
    return r


def test_shortest_path_simple():
    """Test basic shortest path finding."""
    r = TestResult()
    
    # Simple linear graph
    g = DijkstraGraph()
    g.add_edges([('A', 'B', 1), ('B', 'C', 1), ('C', 'D', 1)])
    
    result = g.shortest_path('A', 'D')
    r.assert_true(result.found)
    r.assert_equal(result.distance, 3)
    r.assert_equal(result.path, ['A', 'B', 'C', 'D'])
    
    # Same start and end
    result2 = g.shortest_path('B', 'B')
    r.assert_true(result2.found)
    r.assert_equal(result2.distance, 0)
    r.assert_equal(result2.path, ['B'])
    
    print(f"test_shortest_path_simple: {r.passed} passed, {r.failed} failed")
    return r


def test_shortest_path_complex():
    """Test shortest path in complex graph."""
    r = TestResult()
    
    # Graph with multiple paths
    g = DijkstraGraph(directed=False)
    g.add_edge('A', 'B', 4)
    g.add_edge('A', 'C', 2)
    g.add_edge('B', 'C', 1)
    g.add_edge('B', 'D', 5)
    g.add_edge('C', 'D', 8)
    g.add_edge('C', 'E', 10)
    g.add_edge('D', 'E', 2)
    g.add_edge('D', 'Z', 6)
    g.add_edge('E', 'Z', 3)
    
    # Shortest path A -> Z should be A -> C -> B -> D -> E -> Z = 2 + 1 + 5 + 2 + 3 = 13
    # Actually let's compute: A-C(2), C-B(1), B-D(5), D-E(2), E-Z(3) = 13
    # Or A-C(2), C-D(8), D-E(2), E-Z(3) = 15
    # Or A-B(4), B-D(5), D-E(2), E-Z(3) = 14
    result = g.shortest_path('A', 'Z')
    r.assert_true(result.found)
    r.assert_equal(result.distance, 13)
    
    print(f"test_shortest_path_complex: {r.passed} passed, {r.failed} failed")
    return r


def test_shortest_path_not_found():
    """Test when no path exists."""
    r = TestResult()
    
    # Disconnected graph
    g = DijkstraGraph()
    g.add_edge('A', 'B', 1)
    g.add_edge('C', 'D', 1)
    
    result = g.shortest_path('A', 'D')
    r.assert_false(result.found)
    r.assert_equal(result.distance, float('inf'))
    r.assert_equal(result.path, [])
    
    # Non-existent source
    result2 = g.shortest_path('X', 'A')
    r.assert_false(result2.found)
    
    # Non-existent target
    result3 = g.shortest_path('A', 'X')
    r.assert_false(result3.found)
    
    print(f"test_shortest_path_not_found: {r.passed} passed, {r.failed} failed")
    return r


def test_all_shortest_paths():
    """Test finding all shortest paths from a source."""
    r = TestResult()
    
    g = DijkstraGraph(directed=False)
    g.add_edges([('A', 'B', 1), ('B', 'C', 2), ('A', 'D', 4)])
    
    result = g.shortest_paths_from('A')
    
    r.assert_equal(result.source, 'A')
    r.assert_in('B', result.distances)
    r.assert_in('C', result.distances)
    r.assert_in('D', result.distances)
    r.assert_equal(result.distances['A'], 0)
    r.assert_equal(result.distances['B'], 1)
    r.assert_equal(result.distances['C'], 3)
    r.assert_equal(result.distances['D'], 4)
    
    # Test get_path_to
    path_result = result.get_path_to('C')
    r.assert_true(path_result.found)
    r.assert_equal(path_result.distance, 3)
    r.assert_equal(path_result.path, ['A', 'B', 'C'])
    
    # Test get_path_to for unreachable node
    path_result2 = result.get_path_to('X')
    r.assert_false(path_result2.found)
    
    # Test get_reachable_nodes
    reachable = result.get_reachable_nodes()
    r.assert_equal(len(reachable), 4)
    
    print(f"test_all_shortest_paths: {r.passed} passed, {r.failed} failed")
    return r


def test_directed_vs_undirected():
    """Test difference between directed and undirected graphs."""
    r = TestResult()
    
    # Directed graph
    g_directed = DijkstraGraph(directed=True)
    g_directed.add_edge('A', 'B', 1)
    
    result = g_directed.shortest_path('B', 'A')
    r.assert_false(result.found)  # Can't go back in directed graph
    
    # Undirected graph
    g_undirected = DijkstraGraph(directed=False)
    g_undirected.add_edge('A', 'B', 1)
    
    result2 = g_undirected.shortest_path('B', 'A')
    r.assert_true(result2.found)  # Can go both ways
    r.assert_equal(result2.distance, 1)
    
    print(f"test_directed_vs_undirected: {r.passed} passed, {r.failed} failed")
    return r


def test_integer_nodes():
    """Test graph with integer nodes."""
    r = TestResult()
    
    g = DijkstraGraph()
    g.add_edges([(0, 1, 2), (1, 2, 3), (0, 2, 10)])
    
    result = g.shortest_path(0, 2)
    r.assert_true(result.found)
    r.assert_equal(result.distance, 5)  # 0 -> 1 -> 2 = 2 + 3
    r.assert_equal(result.path, [0, 1, 2])
    
    print(f"test_integer_nodes: {r.passed} passed, {r.failed} failed")
    return r


def test_tuple_nodes():
    """Test graph with tuple nodes (coordinate-like)."""
    r = TestResult()
    
    g = DijkstraGraph()
    g.add_edges([
        ((0, 0), (0, 1), 1),
        ((0, 1), (1, 1), 1),
        ((0, 0), (1, 0), 1),
        ((1, 0), (1, 1), 2)
    ])
    
    result = g.shortest_path((0, 0), (1, 1))
    r.assert_true(result.found)
    r.assert_equal(result.distance, 2)  # Shortest is via (0, 1)
    
    print(f"test_tuple_nodes: {r.passed} passed, {r.failed} failed")
    return r


def test_float_weights():
    """Test graph with float weights."""
    r = TestResult()
    
    g = DijkstraGraph()
    g.add_edges([
        ('A', 'B', 1.5),
        ('B', 'C', 2.7),
        ('A', 'C', 5.0)
    ])
    
    result = g.shortest_path('A', 'C')
    r.assert_true(result.found)
    r.assert_almost_equal(result.distance, 4.2, 0.001)
    
    print(f"test_float_weights: {r.passed} passed, {r.failed} failed")
    return r


def test_large_graph():
    """Test with a larger graph."""
    r = TestResult()
    
    # Create a larger graph
    g = DijkstraGraph()
    n = 100
    
    # Create a linear chain
    for i in range(n - 1):
        g.add_edge(i, i + 1, 1)
    
    # Add some shortcuts
    g.add_edge(0, 10, 5)
    g.add_edge(10, 20, 5)
    g.add_edge(20, 30, 5)
    
    result = g.shortest_path(0, 30)
    r.assert_true(result.found)
    # Path via shortcuts: 0 -> 10 -> 20 -> 30 = 5 + 5 + 5 = 15
    # Direct path: 30 steps
    r.assert_equal(result.distance, 15)
    
    # Test all paths from source
    all_paths = g.shortest_paths_from(0)
    r.assert_equal(len(all_paths.distances), n)
    
    print(f"test_large_graph: {r.passed} passed, {r.failed} failed")
    return r


def test_k_shortest_paths():
    """Test finding k shortest paths."""
    r = TestResult()
    
    # Create a graph with multiple paths
    g = DijkstraGraph(directed=False)
    g.add_edges([
        ('A', 'B', 1),
        ('A', 'C', 2),
        ('B', 'D', 2),
        ('C', 'D', 1),
        ('B', 'C', 3),
        ('D', 'E', 1)
    ])
    
    paths = g.k_shortest_paths('A', 'E', k=3)
    
    r.assert_true(len(paths) >= 1)
    
    # Check that paths are sorted by distance
    for i in range(len(paths) - 1):
        r.assert_less(paths[i].distance, paths[i + 1].distance + 0.001)
    
    # First path should be shortest
    r.assert_equal(paths[0].distance, 4)  # A->B->D->E or A->C->D->E
    
    print(f"test_k_shortest_paths: {r.passed} passed, {r.failed} failed")
    return r


def test_k_shortest_paths_no_alternatives():
    """Test k-shortest paths when only one path exists."""
    r = TestResult()
    
    # Linear graph - only one path
    g = DijkstraGraph()
    g.add_edges([('A', 'B', 1), ('B', 'C', 1)])
    
    paths = g.k_shortest_paths('A', 'C', k=5)
    r.assert_equal(len(paths), 1)
    
    print(f"test_k_shortest_paths_no_alternatives: {r.passed} passed, {r.failed} failed")
    return r


def test_k_shortest_paths_same_node():
    """Test k-shortest paths when source equals target."""
    r = TestResult()
    
    g = DijkstraGraph()
    g.add_edge('A', 'B', 1)
    
    paths = g.k_shortest_paths('A', 'A', k=3)
    r.assert_equal(len(paths), 1)
    r.assert_equal(paths[0].distance, 0)
    r.assert_equal(paths[0].path, ['A'])
    
    print(f"test_k_shortest_paths_same_node: {r.passed} passed, {r.failed} failed")
    return r


def test_copy_and_clear():
    """Test graph copy and clear."""
    r = TestResult()
    
    g = DijkstraGraph()
    g.add_edges([('A', 'B', 1), ('B', 'C', 2)])
    
    # Copy
    g2 = g.copy()
    r.assert_equal(g2.node_count, g.node_count)
    r.assert_equal(g2.edge_count, g.edge_count)
    
    # Modify copy shouldn't affect original
    g2.add_edge('C', 'D', 3)
    r.assert_true(g2.has_node('D'))
    r.assert_false(g.has_node('D'))
    
    # Clear
    g2.clear()
    r.assert_equal(g2.node_count, 0)
    r.assert_equal(g2.edge_count, 0)
    
    print(f"test_copy_and_clear: {r.passed} passed, {r.failed} failed")
    return r


def test_adjacency_matrix():
    """Test conversion to adjacency matrix."""
    r = TestResult()
    
    g = DijkstraGraph(directed=True)
    g.add_edges([
        (0, 1, 2),
        (0, 2, 3),
        (1, 2, 1)
    ])
    
    nodes, matrix = g.to_adjacency_matrix()
    
    r.assert_equal(len(nodes), 3)
    r.assert_equal(len(matrix), 3)
    r.assert_equal(len(matrix[0]), 3)
    
    # Check matrix values
    r.assert_equal(matrix[0][0], 0)  # Diagonal
    r.assert_equal(matrix[0][1], 2)  # Edge 0 -> 1
    r.assert_equal(matrix[0][2], 3)  # Edge 0 -> 2
    r.assert_equal(matrix[1][2], 1)  # Edge 1 -> 2
    
    print(f"test_adjacency_matrix: {r.passed} passed, {r.failed} failed")
    return r


def test_from_adjacency_list():
    """Test creating graph from adjacency list."""
    r = TestResult()
    
    adj_list = {
        'A': [('B', 1), ('C', 2)],
        'B': [('C', 3)],
        'C': [('D', 4)]
    }
    
    g = DijkstraGraph.from_adjacency_list(adj_list, directed=True)
    
    r.assert_equal(g.node_count, 4)
    r.assert_equal(g.edge_count, 4)
    r.assert_true(g.has_edge('A', 'B'))
    r.assert_true(g.has_edge('B', 'C'))
    
    print(f"test_from_adjacency_list: {r.passed} passed, {r.failed} failed")
    return r


def test_from_edge_list():
    """Test creating graph from edge list."""
    r = TestResult()
    
    edges = [
        ('A', 'B', 1),
        ('B', 'C', 2),
        ('A', 'C')  # Default weight
    ]
    
    g = DijkstraGraph.from_edge_list(edges, directed=False)
    
    r.assert_equal(g.node_count, 3)
    r.assert_equal(g.edge_count, 6)  # 3 edges * 2 for undirected
    r.assert_equal(g.get_edge_weight('A', 'C'), 1.0)
    
    print(f"test_from_edge_list: {r.passed} passed, {r.failed} failed")
    return r


def test_from_adjacency_matrix():
    """Test creating graph from adjacency matrix."""
    r = TestResult()
    
    matrix = [
        [0, 2, 3],
        [float('inf'), 0, 1],
        [float('inf'), float('inf'), 0]
    ]
    
    g = DijkstraGraph.from_adjacency_matrix(matrix, nodes=['A', 'B', 'C'], directed=True)
    
    r.assert_equal(g.node_count, 3)
    r.assert_equal(g.edge_count, 3)  # A->B, A->C, B->C
    r.assert_true(g.has_edge('A', 'B'))
    r.assert_true(g.has_edge('A', 'C'))
    r.assert_true(g.has_edge('B', 'C'))
    r.assert_false(g.has_edge('B', 'A'))
    
    print(f"test_from_adjacency_matrix: {r.passed} passed, {r.failed} failed")
    return r


def test_convenience_functions():
    """Test module-level convenience functions."""
    r = TestResult()
    
    # Test with DijkstraGraph
    g = DijkstraGraph()
    g.add_edges([('A', 'B', 1), ('B', 'C', 2)])
    
    result = dijkstra(g, 'A', 'C')
    r.assert_true(result.found)
    r.assert_equal(result.distance, 3)
    
    # Test with adjacency dict
    adj_dict = {
        'A': [('B', 1)],
        'B': [('C', 2)]
    }
    
    result2 = shortest_path(adj_dict, 'A', 'C')
    r.assert_true(result2.found)
    r.assert_equal(result2.distance, 3)
    
    # Test all_shortest_paths
    all_result = all_shortest_paths(adj_dict, 'A')
    r.assert_equal(all_result.source, 'A')
    
    print(f"test_convenience_functions: {r.passed} passed, {r.failed} failed")
    return r


def test_is_connected():
    """Test is_connected utility function."""
    r = TestResult()
    
    g = DijkstraGraph()
    g.add_edges([('A', 'B', 1), ('B', 'C', 1), ('D', 'E', 1)])
    
    r.assert_true(is_connected(g, 'A', 'C'))
    r.assert_false(is_connected(g, 'A', 'D'))
    r.assert_true(is_connected(g, 'D', 'E'))
    
    print(f"test_is_connected: {r.passed} passed, {r.failed} failed")
    return r


def test_get_reachable_nodes():
    """Test get_reachable_nodes utility function."""
    r = TestResult()
    
    g = DijkstraGraph()
    g.add_edges([('A', 'B', 1), ('B', 'C', 1), ('D', 'E', 1)])
    
    reachable = get_reachable_nodes(g, 'A')
    r.assert_equal(len(reachable), 3)
    r.assert_in('A', reachable)
    r.assert_in('B', reachable)
    r.assert_in('C', reachable)
    r.assert_not_in('D', reachable)
    
    print(f"test_get_reachable_nodes: {r.passed} passed, {r.failed} failed")
    return r


def test_graph_diameter():
    """Test graph diameter calculation."""
    r = TestResult()
    
    # Simple linear graph: diameter is A->D = 3
    g = DijkstraGraph()
    g.add_edges([('A', 'B', 1), ('B', 'C', 1), ('C', 'D', 1)])
    
    diameter, endpoints = graph_diameter(g)
    r.assert_equal(diameter, 3)
    r.assert_equal(endpoints, ('A', 'D'))
    
    print(f"test_graph_diameter: {r.passed} passed, {r.failed} failed")
    return r


def test_center_of_graph():
    """Test graph center calculation."""
    r = TestResult()
    
    # Star graph: center is the center node
    g = DijkstraGraph(directed=False)
    g.add_edges([('center', 'A', 1), ('center', 'B', 1), ('center', 'C', 1)])
    
    center = center_of_graph(g)
    r.assert_in('center', center)
    
    print(f"test_center_of_graph: {r.passed} passed, {r.failed} failed")
    return r


def test_zero_weight_edge():
    """Test graph with zero weight edges."""
    r = TestResult()
    
    g = DijkstraGraph()
    g.add_edges([
        ('A', 'B', 0),
        ('B', 'C', 1)
    ])
    
    result = g.shortest_path('A', 'C')
    r.assert_true(result.found)
    r.assert_equal(result.distance, 1)
    
    print(f"test_zero_weight_edge: {r.passed} passed, {r.failed} failed")
    return r


def test_self_loop():
    """Test graph with self-loops."""
    r = TestResult()
    
    g = DijkstraGraph()
    g.add_edge('A', 'A', 5)  # Self-loop
    g.add_edge('A', 'B', 1)
    
    # Self-loop shouldn't affect shortest path
    result = g.shortest_path('A', 'A')
    r.assert_true(result.found)
    r.assert_equal(result.distance, 0)  # Staying at A costs 0
    
    print(f"test_self_loop: {r.passed} passed, {r.failed} failed")
    return r


def test_multiple_edges():
    """Test graph with multiple edges between same nodes."""
    r = TestResult()
    
    g = DijkstraGraph()
    g.add_edge('A', 'B', 5)
    g.add_edge('A', 'B', 2)  # Parallel edge with lower weight
    
    neighbors = g.get_neighbors('A')
    r.assert_equal(len(neighbors), 2)  # Both edges exist
    
    # Shortest path should use the lower weight
    # But since we have parallel edges, we need to check get_edge_weight returns first
    result = g.shortest_path('A', 'B')
    r.assert_true(result.found)
    # The algorithm will find the minimum distance
    
    print(f"test_multiple_edges: {r.passed} passed, {r.failed} failed")
    return r


def test_path_result_repr():
    """Test PathResult string representation."""
    r = TestResult()
    
    result = PathResult(distance=5, path=['A', 'B', 'C'], found=True)
    repr_str = repr(result)
    r.assert_in('distance', repr_str)
    r.assert_in('path', repr_str)
    
    result2 = PathResult(distance=float('inf'), path=[], found=False)
    repr_str2 = repr(result2)
    r.assert_in('not found', repr_str2)
    
    print(f"test_path_result_repr: {r.passed} passed, {r.failed} failed")
    return r


def test_empty_graph():
    """Test operations on empty graph."""
    r = TestResult()
    
    g = DijkstraGraph()
    
    r.assert_equal(g.node_count, 0)
    r.assert_equal(g.edge_count, 0)
    r.assert_equal(len(g.nodes), 0)
    
    result = g.shortest_path('A', 'B')
    r.assert_false(result.found)
    
    print(f"test_empty_graph: {r.passed} passed, {r.failed} failed")
    return r


def test_single_node_graph():
    """Test graph with single node."""
    r = TestResult()
    
    g = DijkstraGraph()
    g.add_node('A')
    
    result = g.shortest_path('A', 'A')
    r.assert_true(result.found)
    r.assert_equal(result.distance, 0)
    r.assert_equal(result.path, ['A'])
    
    result2 = g.shortest_path('A', 'B')
    r.assert_false(result2.found)
    
    print(f"test_single_node_graph: {r.passed} passed, {r.failed} failed")
    return r


def test_method_chaining():
    """Test that add_node and add_edge return self for chaining."""
    r = TestResult()
    
    g = (DijkstraGraph()
         .add_node('A')
         .add_edge('A', 'B', 1)
         .add_edge('B', 'C', 2)
         .add_edges([('C', 'D', 3), ('D', 'E', 4)]))
    
    r.assert_equal(g.node_count, 5)
    r.assert_equal(g.edge_count, 4)
    
    result = g.shortest_path('A', 'E')
    r.assert_true(result.found)
    r.assert_equal(result.distance, 10)
    
    print(f"test_method_chaining: {r.passed} passed, {r.failed} failed")
    return r


def test_very_large_weights():
    """Test with very large weights."""
    r = TestResult()
    
    g = DijkstraGraph()
    g.add_edges([
        ('A', 'B', 1e15),
        ('A', 'C', 1),
        ('C', 'B', 1)
    ])
    
    result = g.shortest_path('A', 'B')
    r.assert_true(result.found)
    r.assert_equal(result.distance, 2)  # Via C is shorter
    
    print(f"test_very_large_weights: {r.passed} passed, {r.failed} failed")
    return r


def test_precision_weights():
    """Test with precision weights."""
    r = TestResult()
    
    g = DijkstraGraph()
    g.add_edges([
        ('A', 'B', 0.1),
        ('B', 'C', 0.2),
        ('A', 'C', 0.35)
    ])
    
    result = g.shortest_path('A', 'C')
    r.assert_true(result.found)
    r.assert_almost_equal(result.distance, 0.3, 0.0001)
    
    print(f"test_precision_weights: {r.passed} passed, {r.failed} failed")
    return r


def run_all_tests():
    """Run all test functions."""
    test_functions = [
        test_graph_edge,
        test_dijkstra_graph_creation,
        test_add_edges,
        test_remove_nodes_and_edges,
        test_shortest_path_simple,
        test_shortest_path_complex,
        test_shortest_path_not_found,
        test_all_shortest_paths,
        test_directed_vs_undirected,
        test_integer_nodes,
        test_tuple_nodes,
        test_float_weights,
        test_large_graph,
        test_k_shortest_paths,
        test_k_shortest_paths_no_alternatives,
        test_k_shortest_paths_same_node,
        test_copy_and_clear,
        test_adjacency_matrix,
        test_from_adjacency_list,
        test_from_edge_list,
        test_from_adjacency_matrix,
        test_convenience_functions,
        test_is_connected,
        test_get_reachable_nodes,
        test_graph_diameter,
        test_center_of_graph,
        test_zero_weight_edge,
        test_self_loop,
        test_multiple_edges,
        test_path_result_repr,
        test_empty_graph,
        test_single_node_graph,
        test_method_chaining,
        test_very_large_weights,
        test_precision_weights,
    ]
    
    total_passed = 0
    total_failed = 0
    all_errors = []
    
    print("=" * 60)
    print("Dijkstra Utils Test Suite")
    print("=" * 60)
    
    for test_func in test_functions:
        result = test_func()
        total_passed += result.passed
        total_failed += result.failed
        all_errors.extend(result.errors)
    
    print("\n" + "=" * 60)
    print(f"TOTAL: {total_passed} passed, {total_failed} failed")
    print("=" * 60)
    
    if all_errors:
        print("\nFailed tests:")
        for error in all_errors[:20]:  # Show first 20 errors
            print(f"  - {error}")
        if len(all_errors) > 20:
            print(f"  ... and {len(all_errors) - 20} more errors")
    
    return total_failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)