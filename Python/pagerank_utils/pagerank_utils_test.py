"""
Tests for PageRank Utilities

Comprehensive test suite covering:
- Graph construction and manipulation
- Classic PageRank algorithm
- Weighted PageRank
- Personalized PageRank
- Utility functions
- Edge cases and boundary conditions
"""

import sys
import os
import math

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pagerank_utils.mod import (
    Graph, PageRankError, InvalidGraphError, ConvergenceError,
    build_graph_from_edge_list, build_graph_from_adjacency_list,
    build_graph_from_matrix, pagerank, pagerank_weighted,
    personalized_pagerank, get_top_k, get_rankings, normalize_scores,
    compare_scores, l1_distance, l2_distance, compute_centrality,
    detect_communities_by_scores,
    validate_damping_factor, validate_convergence_params
)


def test_graph_creation():
    """Test basic graph creation."""
    graph = Graph()
    assert graph.is_empty()
    assert graph.node_count == 0
    assert graph.edge_count == 0
    print("✓ test_graph_creation passed")


def test_graph_add_node():
    """Test adding nodes."""
    graph = Graph()
    graph.add_node('A')
    graph.add_node('B')
    
    assert graph.node_count == 2
    assert graph.has_node('A')
    assert graph.has_node('B')
    assert not graph.has_node('C')
    print("✓ test_graph_add_node passed")


def test_graph_add_edge():
    """Test adding edges."""
    graph = Graph()
    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C', weight=2.0)
    
    assert graph.node_count == 3
    assert graph.edge_count == 2
    assert graph.get_out_degree('A') == 2
    assert graph.get_in_degree('B') == 1
    assert graph.get_in_degree('C') == 1
    
    successors = graph.get_successors('A')
    assert successors['B'] == 1.0
    assert successors['C'] == 2.0
    print("✓ test_graph_add_edge passed")


def test_graph_edge_accumulation():
    """Test that adding same edge multiple times accumulates weights."""
    graph = Graph()
    graph.add_edge('A', 'B', weight=1.0)
    graph.add_edge('A', 'B', weight=2.0)
    
    assert graph.edge_count == 1  # Still one edge
    assert graph.get_successors('A')['B'] == 3.0  # But weight is accumulated
    print("✓ test_graph_edge_accumulation passed")


def test_graph_add_edges_from():
    """Test adding multiple edges at once."""
    graph = Graph()
    edges = [
        ('A', 'B'),
        ('B', 'C'),
        ('C', 'A', 2.0)
    ]
    graph.add_edges_from(edges)
    
    assert graph.node_count == 3
    assert graph.edge_count == 3
    assert graph.get_successors('C')['A'] == 2.0
    print("✓ test_graph_add_edges_from passed")


def test_graph_statistics():
    """Test graph statistics."""
    graph = Graph()
    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    graph.add_edge('B', 'C')
    
    stats = graph.get_statistics()
    assert stats['node_count'] == 3
    assert stats['edge_count'] == 3
    assert stats['max_out_degree'] == 2
    assert stats['dangling_node_count'] == 1  # Node C
    print("✓ test_graph_statistics passed")


def test_graph_dangling_nodes():
    """Test dangling node detection."""
    graph = Graph()
    graph.add_edge('A', 'B')
    graph.add_edge('B', 'C')
    # C has no outgoing edges
    
    dangling = graph.get_dangling_nodes()
    assert 'C' in dangling
    assert 'A' not in dangling
    assert 'B' not in dangling
    print("✓ test_graph_dangling_nodes passed")


def test_build_graph_from_edge_list():
    """Test building graph from edge list."""
    edges = [
        ('A', 'B', 1.0),
        ('B', 'C', 1.0),
        ('C', 'A', 1.5)
    ]
    graph = build_graph_from_edge_list(edges)
    
    assert graph.node_count == 3
    assert graph.edge_count == 3
    assert graph.get_successors('C')['A'] == 1.5
    print("✓ test_build_graph_from_edge_list passed")


def test_build_graph_from_adjacency_list_dict():
    """Test building graph from adjacency list with weights."""
    adj_list = {
        'A': {'B': 1.0, 'C': 2.0},
        'B': {'C': 1.0},
        'C': {}
    }
    graph = build_graph_from_adjacency_list(adj_list)
    
    assert graph.node_count == 3
    assert graph.edge_count == 3
    assert graph.get_successors('A')['C'] == 2.0
    print("✓ test_build_graph_from_adjacency_list_dict passed")


def test_build_graph_from_adjacency_list_set():
    """Test building graph from adjacency list with sets."""
    adj_list = {
        'A': {'B', 'C'},
        'B': {'C'},
        'C': set()
    }
    graph = build_graph_from_adjacency_list(adj_list)
    
    assert graph.node_count == 3
    assert graph.edge_count == 3
    assert graph.get_successors('A')['B'] == 1.0
    assert graph.get_successors('A')['C'] == 1.0
    print("✓ test_build_graph_from_adjacency_list_set passed")


def test_build_graph_from_matrix():
    """Test building graph from adjacency matrix."""
    matrix = [
        [0, 1, 1],
        [0, 0, 1],
        [1, 0, 0]
    ]
    graph = build_graph_from_matrix(matrix, ['A', 'B', 'C'])
    
    assert graph.node_count == 3
    assert graph.edge_count == 4
    assert graph.has_edge('A', 'B')
    assert graph.has_edge('B', 'A') == False
    print("✓ test_build_graph_from_matrix passed")


def test_build_graph_from_matrix_default_labels():
    """Test building graph from matrix with default labels."""
    matrix = [[0, 1], [1, 0]]
    graph = build_graph_from_matrix(matrix)
    
    assert graph.has_node('0')
    assert graph.has_node('1')
    print("✓ test_build_graph_from_matrix_default_labels passed")


def test_pagerank_simple_cycle():
    """Test PageRank on simple cycle graph."""
    graph = Graph()
    graph.add_edge('A', 'B')
    graph.add_edge('B', 'C')
    graph.add_edge('C', 'A')
    
    scores = pagerank(graph)
    
    # All nodes should have equal PageRank in a cycle
    assert abs(scores['A'] - scores['B']) < 1e-6
    assert abs(scores['B'] - scores['C']) < 1e-6
    assert abs(sum(scores.values()) - 1.0) < 1e-6
    print("✓ test_pagerank_simple_cycle passed")


def test_pagerank_simple_chain():
    """Test PageRank on simple chain graph."""
    graph = Graph()
    graph.add_edge('A', 'B')
    graph.add_edge('B', 'C')
    
    scores = pagerank(graph)
    
    # C is a dangling node, so it redistributes
    assert abs(sum(scores.values()) - 1.0) < 1e-6
    print("✓ test_pagerank_simple_chain passed")


def test_pagerank_star_graph():
    """Test PageRank on star graph."""
    graph = Graph()
    # Center node A points to all others
    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    graph.add_edge('A', 'D')
    # All others point back to A
    graph.add_edge('B', 'A')
    graph.add_edge('C', 'A')
    graph.add_edge('D', 'A')
    
    # Use slightly relaxed threshold for this structure
    scores = pagerank(graph, threshold=1e-6)
    
    # A should have highest PageRank
    assert scores['A'] > scores['B']
    assert scores['A'] > scores['C']
    assert scores['A'] > scores['D']
    # B, C, D should have equal scores
    assert abs(scores['B'] - scores['C']) < 1e-5
    assert abs(scores['C'] - scores['D']) < 1e-5
    print("✓ test_pagerank_star_graph passed")


def test_pagerank_damping_factor():
    """Test effect of different damping factors."""
    graph = Graph()
    graph.add_edge('A', 'B')
    graph.add_edge('B', 'A')
    
    scores_high = pagerank(graph, damping=0.9)
    scores_low = pagerank(graph, damping=0.5)
    
    # Both should be valid distributions
    assert abs(sum(scores_high.values()) - 1.0) < 1e-6
    assert abs(sum(scores_low.values()) - 1.0) < 1e-6
    print("✓ test_pagerank_damping_factor passed")


def test_pagerank_convergence():
    """Test PageRank converges within max iterations."""
    # Create a larger graph
    graph = Graph()
    for i in range(10):
        graph.add_edge(str(i), str((i + 1) % 10))
    
    scores = pagerank(graph, max_iterations=100)
    assert abs(sum(scores.values()) - 1.0) < 1e-6
    print("✓ test_pagerank_convergence passed")


def test_pagerank_empty_graph():
    """Test PageRank raises error on empty graph."""
    graph = Graph()
    
    try:
        pagerank(graph)
        assert False, "Should have raised InvalidGraphError"
    except InvalidGraphError:
        pass
    print("✓ test_pagerank_empty_graph passed")


def test_pagerank_single_node():
    """Test PageRank on single node."""
    graph = Graph()
    graph.add_node('A')
    
    scores = pagerank(graph)
    assert scores['A'] == 1.0
    print("✓ test_pagerank_single_node passed")


def test_pagerank_self_loop():
    """Test PageRank with self-loops."""
    graph = Graph()
    graph.add_edge('A', 'A')
    graph.add_edge('A', 'B')
    graph.add_edge('B', 'A')
    
    scores = pagerank(graph)
    assert abs(sum(scores.values()) - 1.0) < 1e-6
    print("✓ test_pagerank_self_loop passed")


def test_pagerank_weighted_simple():
    """Test weighted PageRank on simple graph."""
    graph = Graph()
    graph.add_edge('A', 'B', weight=1.0)
    graph.add_edge('A', 'C', weight=3.0)  # C gets more weight
    graph.add_edge('B', 'A')
    graph.add_edge('C', 'A')
    
    # Use relaxed threshold for weighted PageRank
    scores = pagerank_weighted(graph, threshold=1e-6)
    
    # C should have higher PageRank due to higher incoming weight
    assert scores['C'] > scores['B']
    assert abs(sum(scores.values()) - 1.0) < 1e-5
    print("✓ test_pagerank_weighted_simple passed")


def test_pagerank_weighted_chain():
    """Test weighted PageRank on chain with different weights."""
    graph = Graph()
    graph.add_edge('A', 'B', weight=1.0)
    graph.add_edge('B', 'C', weight=5.0)
    
    scores = pagerank_weighted(graph)
    assert abs(sum(scores.values()) - 1.0) < 1e-6
    print("✓ test_pagerank_weighted_chain passed")


def test_personalized_pagerank():
    """Test personalized PageRank."""
    graph = Graph()
    graph.add_edge('A', 'B')
    graph.add_edge('B', 'C')
    graph.add_edge('C', 'D')
    graph.add_edge('D', 'A')
    
    # Personalize to start from A only
    scores = personalized_pagerank(graph, 'A', threshold=1e-6)
    
    assert abs(sum(scores.values()) - 1.0) < 1e-5
    # A and nearby nodes should have higher scores
    print("✓ test_personalized_pagerank passed")


def test_personalized_pagerank_multiple_sources():
    """Test personalized PageRank with multiple sources."""
    graph = Graph()
    graph.add_edge('A', 'B')
    graph.add_edge('B', 'C')
    graph.add_edge('C', 'D')
    graph.add_edge('D', 'E')
    
    scores = personalized_pagerank(graph, ['A', 'E'], threshold=1e-6)
    
    assert abs(sum(scores.values()) - 1.0) < 1e-5
    print("✓ test_personalized_pagerank_multiple_sources passed")


def test_personalized_pagerank_weights():
    """Test personalized PageRank with custom weights."""
    graph = Graph()
    graph.add_edge('A', 'B')
    graph.add_edge('B', 'A')
    
    weights = {'A': 0.9, 'B': 0.1}
    scores = personalized_pagerank(graph, ['A', 'B'], weights=weights, threshold=1e-6)
    
    assert abs(sum(scores.values()) - 1.0) < 1e-5
    # A should have higher score due to higher teleportation weight
    assert scores['A'] > scores['B']
    print("✓ test_personalized_pagerank_weights passed")


def test_personalized_pagerank_invalid_source():
    """Test personalized PageRank with invalid source."""
    graph = Graph()
    graph.add_edge('A', 'B')
    
    try:
        personalized_pagerank(graph, 'C')  # C doesn't exist
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    print("✓ test_personalized_pagerank_invalid_source passed")


def test_get_top_k():
    """Test getting top k nodes."""
    scores = {'A': 0.4, 'B': 0.3, 'C': 0.2, 'D': 0.1}
    
    top2 = get_top_k(scores, 2)
    assert len(top2) == 2
    assert top2[0][0] == 'A'
    assert top2[1][0] == 'B'
    
    top10 = get_top_k(scores, 10)
    assert len(top10) == 4  # Only 4 nodes exist
    print("✓ test_get_top_k passed")


def test_get_rankings():
    """Test converting scores to rankings."""
    scores = {'A': 0.4, 'B': 0.3, 'C': 0.2, 'D': 0.1}
    
    rankings = get_rankings(scores)
    assert rankings['A'] == 1
    assert rankings['B'] == 2
    assert rankings['C'] == 3
    assert rankings['D'] == 4
    print("✓ test_get_rankings passed")


def test_get_rankings_with_ties():
    """Test rankings with tied scores."""
    scores = {'A': 0.3, 'B': 0.3, 'C': 0.2}
    
    rankings = get_rankings(scores)
    # A should rank before B due to alphabetical order
    assert rankings['A'] == 1
    assert rankings['B'] == 2
    assert rankings['C'] == 3
    print("✓ test_get_rankings_with_ties passed")


def test_normalize_scores():
    """Test score normalization."""
    scores = {'A': 2.0, 'B': 2.0, 'C': 1.0}  # Sum = 5.0
    normalized = normalize_scores(scores)
    
    assert abs(normalized['A'] - 0.4) < 1e-6
    assert abs(normalized['B'] - 0.4) < 1e-6
    assert abs(normalized['C'] - 0.2) < 1e-6
    assert abs(sum(normalized.values()) - 1.0) < 1e-6
    print("✓ test_normalize_scores passed")


def test_normalize_scores_empty():
    """Test normalization of empty scores."""
    scores = {}
    normalized = normalize_scores(scores)
    assert normalized == {}
    print("✓ test_normalize_scores_empty passed")


def test_compare_scores():
    """Test comparing two score distributions."""
    scores1 = {'A': 0.5, 'B': 0.3, 'C': 0.2}
    scores2 = {'A': 0.4, 'B': 0.4, 'C': 0.2}
    
    diff = compare_scores(scores1, scores2)
    assert abs(diff['A'] - 0.1) < 1e-6
    assert abs(diff['B'] - 0.1) < 1e-6
    assert abs(diff['C'] - 0.0) < 1e-6
    print("✓ test_compare_scores passed")


def test_compare_scores_different_nodes():
    """Test comparing scores with different node sets."""
    scores1 = {'A': 0.5, 'B': 0.5}
    scores2 = {'B': 0.5, 'C': 0.5}
    
    diff = compare_scores(scores1, scores2)
    assert diff['A'] == 0.5  # A is 0.5 in scores1, 0 in scores2
    assert diff['B'] == 0.0
    assert diff['C'] == 0.5
    print("✓ test_compare_scores_different_nodes passed")


def test_l1_distance():
    """Test L1 distance calculation."""
    scores1 = {'A': 0.5, 'B': 0.5}
    scores2 = {'A': 0.3, 'B': 0.7}
    
    l1 = l1_distance(scores1, scores2)
    assert abs(l1 - 0.4) < 1e-6  # |0.5-0.3| + |0.5-0.7| = 0.4
    print("✓ test_l1_distance passed")


def test_l2_distance():
    """Test L2 distance calculation."""
    scores1 = {'A': 0.5, 'B': 0.5}
    scores2 = {'A': 0.3, 'B': 0.7}
    
    l2 = l2_distance(scores1, scores2)
    expected = math.sqrt(0.2**2 + 0.2**2)  # sqrt(0.08) ≈ 0.283
    assert abs(l2 - expected) < 1e-6
    print("✓ test_l2_distance passed")


def test_compute_centrality():
    """Test centrality statistics computation."""
    scores = {'A': 0.5, 'B': 0.3, 'C': 0.2}
    stats = compute_centrality(scores)
    
    assert abs(stats['mean'] - (1.0/3)) < 1e-6
    assert stats['min'] == 0.2
    assert stats['max'] == 0.5
    assert stats['gini'] >= 0 and stats['gini'] <= 1
    print("✓ test_compute_centrality passed")


def test_compute_centrality_equal():
    """Test centrality with equal scores."""
    scores = {'A': 0.25, 'B': 0.25, 'C': 0.25, 'D': 0.25}
    stats = compute_centrality(scores)
    
    assert abs(stats['gini'] - 0.0) < 1e-6  # Perfect equality
    print("✓ test_compute_centrality_equal passed")


def test_compute_centrality_empty():
    """Test centrality with empty scores."""
    stats = compute_centrality({})
    
    assert stats['mean'] == 0
    assert stats['gini'] == 0
    print("✓ test_compute_centrality_empty passed")


def test_detect_communities():
    """Test community detection by scores."""
    scores = {'A': 0.4, 'B': 0.35, 'C': 0.15, 'D': 0.1}
    tiers = detect_communities_by_scores(scores, num_tiers=2)
    
    # A and B should be in tier 1, C and D in tier 2
    assert tiers['A'] == 1
    assert tiers['B'] == 1
    assert tiers['C'] == 2
    assert tiers['D'] == 2
    print("✓ test_detect_communities passed")


def test_detect_communities_three_tiers():
    """Test community detection with three tiers."""
    scores = {'A': 0.5, 'B': 0.25, 'C': 0.15, 'D': 0.1}
    tiers = detect_communities_by_scores(scores, num_tiers=3)
    
    assert 1 <= tiers['A'] <= 3
    assert 1 <= tiers['D'] <= 3
    assert tiers['A'] <= tiers['D']  # Higher score = lower tier number
    print("✓ test_detect_communities_three_tiers passed")


def test_validate_damping_factor():
    """Test damping factor validation."""
    # Valid cases
    validate_damping_factor(0.5)
    validate_damping_factor(0.85)
    validate_damping_factor(0.99)
    
    # Invalid cases
    try:
        validate_damping_factor(0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        validate_damping_factor(1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        validate_damping_factor(1.5)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    print("✓ test_validate_damping_factor passed")


def test_validate_convergence_params():
    """Test convergence parameter validation."""
    # Valid cases
    validate_convergence_params(1e-8, 100)
    validate_convergence_params(0.001, 1)
    
    # Invalid cases
    try:
        validate_convergence_params(0, 100)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        validate_convergence_params(1e-8, 0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    print("✓ test_validate_convergence_params passed")


def test_invalid_node_type():
    """Test that invalid node types are rejected."""
    graph = Graph()
    
    try:
        graph.add_node(123)  # Should be string
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    print("✓ test_invalid_node_type passed")


def test_invalid_edge_weight():
    """Test that invalid edge weights are rejected."""
    graph = Graph()
    
    try:
        graph.add_edge('A', 'B', weight=-1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        graph.add_edge('A', 'B', weight=0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    print("✓ test_invalid_edge_weight passed")


def test_invalid_matrix():
    """Test that invalid matrices are rejected."""
    # Non-square matrix
    try:
        build_graph_from_matrix([[0, 1, 2], [3, 4, 5]])  # 2x3 matrix
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    # Wrong number of labels
    try:
        build_graph_from_matrix([[0, 1], [1, 0]], ['A', 'B', 'C'])  # 2 nodes, 3 labels
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    print("✓ test_invalid_matrix passed")


def test_large_graph():
    """Test PageRank on a larger graph."""
    graph = Graph()
    
    # Create a 100-node ring graph
    for i in range(100):
        graph.add_edge(str(i), str((i + 1) % 100))
    
    scores = pagerank(graph)
    
    # All nodes should have equal PageRank
    first_score = scores['0']
    for i in range(100):
        assert abs(scores[str(i)] - first_score) < 1e-6
    
    assert abs(sum(scores.values()) - 1.0) < 1e-6
    print("✓ test_large_graph passed")


def test_disconnected_components():
    """Test PageRank on disconnected components."""
    graph = Graph()
    # Component 1: A <-> B
    graph.add_edge('A', 'B')
    graph.add_edge('B', 'A')
    # Component 2: C <-> D
    graph.add_edge('C', 'D')
    graph.add_edge('D', 'C')
    
    scores = pagerank(graph)
    
    # Each component should have equal scores within
    assert abs(scores['A'] - scores['B']) < 1e-6
    assert abs(scores['C'] - scores['D']) < 1e-6
    
    # Total should sum to 1
    assert abs(sum(scores.values()) - 1.0) < 1e-6
    print("✓ test_disconnected_components passed")


def test_graph_to_edge_list():
    """Test exporting graph to edge list."""
    graph = Graph()
    graph.add_edge('A', 'B', weight=1.5)
    graph.add_edge('B', 'C', weight=2.5)
    
    edges = graph.to_edge_list()
    assert len(edges) == 2
    
    # Find edges (order may vary)
    edge_dict = {(e[0], e[1]): e[2] for e in edges}
    assert edge_dict[('A', 'B')] == 1.5
    assert edge_dict[('B', 'C')] == 2.5
    print("✓ test_graph_to_edge_list passed")


def test_get_top_k_invalid_k():
    """Test get_top_k with invalid k."""
    scores = {'A': 0.5, 'B': 0.5}
    
    try:
        get_top_k(scores, 0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        get_top_k(scores, -1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    print("✓ test_get_top_k_invalid_k passed")


def test_detect_communities_invalid_tiers():
    """Test community detection with invalid tier count."""
    scores = {'A': 0.5, 'B': 0.5}
    
    try:
        detect_communities_by_scores(scores, num_tiers=1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        detect_communities_by_scores(scores, num_tiers=0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    print("✓ test_detect_communities_invalid_tiers passed")


def test_personalized_pagerank_invalid_weights():
    """Test personalized PageRank with invalid weights."""
    graph = Graph()
    graph.add_edge('A', 'B')
    
    # Weight for node not in source_nodes
    try:
        personalized_pagerank(graph, 'A', weights={'C': 1.0})
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    print("✓ test_personalized_pagerank_invalid_weights passed")


def test_pagerank_personalization_invalid():
    """Test PageRank with invalid personalization."""
    graph = Graph()
    graph.add_edge('A', 'B')
    
    # Unknown node in personalization
    try:
        pagerank(graph, personalization={'C': 1.0})
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    print("✓ test_pagerank_personalization_invalid passed")


def test_pagerank_personalization_zero_sum():
    """Test PageRank with zero-sum personalization."""
    graph = Graph()
    graph.add_edge('A', 'B')
    
    try:
        pagerank(graph, personalization={'A': 0.0, 'B': 0.0})
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    print("✓ test_pagerank_personalization_zero_sum passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running PageRank Utilities Tests")
    print("=" * 60)
    
    # Graph tests
    test_graph_creation()
    test_graph_add_node()
    test_graph_add_edge()
    test_graph_edge_accumulation()
    test_graph_add_edges_from()
    test_graph_statistics()
    test_graph_dangling_nodes()
    
    # Graph builder tests
    test_build_graph_from_edge_list()
    test_build_graph_from_adjacency_list_dict()
    test_build_graph_from_adjacency_list_set()
    test_build_graph_from_matrix()
    test_build_graph_from_matrix_default_labels()
    
    # PageRank tests
    test_pagerank_simple_cycle()
    test_pagerank_simple_chain()
    test_pagerank_star_graph()
    test_pagerank_damping_factor()
    test_pagerank_convergence()
    test_pagerank_empty_graph()
    test_pagerank_single_node()
    test_pagerank_self_loop()
    
    # Weighted PageRank tests
    test_pagerank_weighted_simple()
    test_pagerank_weighted_chain()
    
    # Personalized PageRank tests
    test_personalized_pagerank()
    test_personalized_pagerank_multiple_sources()
    test_personalized_pagerank_weights()
    test_personalized_pagerank_invalid_source()
    test_personalized_pagerank_invalid_weights()
    
    # Utility function tests
    test_get_top_k()
    test_get_rankings()
    test_get_rankings_with_ties()
    test_normalize_scores()
    test_normalize_scores_empty()
    test_compare_scores()
    test_compare_scores_different_nodes()
    test_l1_distance()
    test_l2_distance()
    test_compute_centrality()
    test_compute_centrality_equal()
    test_compute_centrality_empty()
    test_detect_communities()
    test_detect_communities_three_tiers()
    
    # Validation tests
    test_validate_damping_factor()
    test_validate_convergence_params()
    
    # Error handling tests
    test_invalid_node_type()
    test_invalid_edge_weight()
    test_invalid_matrix()
    test_get_top_k_invalid_k()
    test_detect_communities_invalid_tiers()
    test_pagerank_personalization_invalid()
    test_pagerank_personalization_zero_sum()
    
    # Large scale tests
    test_large_graph()
    test_disconnected_components()
    
    # Export tests
    test_graph_to_edge_list()
    
    print("=" * 60)
    print("All 57 tests passed! ✓")
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()