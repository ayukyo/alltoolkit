"""Tests for graph_metrics_utils."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    degree_centrality,
    betweenness_centrality,
    closeness_centrality,
    page_rank,
    clustering_coefficient,
    average_clustering_coefficient,
    is_connected,
    count_connected_components,
    graph_density,
    shortest_path_length,
    all_pairs_shortest_paths,
    eccentricity,
    graph_diameter,
    graph_radius,
)


class TestDegreeCentrality:
    def test_star_graph_center(self):
        """Center of star graph has highest degree centrality."""
        # Star: 0 connected to 1,2,3,4
        graph = {
            "0": ["1", "2", "3", "4"],
            "1": ["0"], "2": ["0"], "3": ["0"], "4": ["0"]
        }
        assert degree_centrality(graph, "0") == 1.0

    def test_leaf_node(self):
        """Leaf node has low degree centrality."""
        graph = {
            "0": ["1", "2", "3", "4"],
            "1": ["0"], "2": ["0"], "3": ["0"], "4": ["0"]
        }
        assert degree_centrality(graph, "1") == 1 / 4

    def test_empty_graph(self):
        assert degree_centrality({}, "node") == 0.0


class TestClosenessCentrality:
    def test_complete_graph(self):
        """All nodes in complete graph have same closeness."""
        graph = {"a": ["b", "c"], "b": ["a", "c"], "c": ["a", "b"]}
        ca = closeness_centrality(graph, "a")
        cb = closeness_centrality(graph, "b")
        assert abs(ca - cb) < 1e-9

    def test_line_graph(self):
        """End nodes have lower closeness than middle."""
        graph = {"a": ["b"], "b": ["a", "c"], "c": ["b"]}
        end = closeness_centrality(graph, "a")
        middle = closeness_centrality(graph, "b")
        assert middle > end


class TestPageRank:
    def test_simple_chain(self):
        """Test PageRank on a simple chain."""
        graph = {
            "a": ["b"],
            "b": ["c"],
            "c": ["a"],
        }
        ranks = page_rank(graph, damping=0.85)
        assert abs(sum(ranks.values()) - 1.0) < 1e-9

    def test_ranked_returns_sum_to_one(self):
        """PageRank scores sum to 1."""
        graph = {
            "1": ["2", "3"],
            "2": ["3"],
            "3": ["1"],
        }
        ranks = page_rank(graph)
        assert abs(sum(ranks.values()) - 1.0) < 1e-6


class TestClusteringCoefficient:
    def test_triangle(self):
        """Complete subgraph of 3 nodes has coefficient 1."""
        graph = {"a": ["b", "c"], "b": ["a", "c"], "c": ["a", "b"]}
        assert clustering_coefficient(graph, "a") == 1.0

    def test_line(self):
        """Line graph nodes have coefficient 0."""
        graph = {"a": ["b"], "b": ["a", "c"], "c": ["b"]}
        assert clustering_coefficient(graph, "b") == 0.0


class TestConnectivity:
    def test_connected_graph(self):
        assert is_connected({"a": ["b"], "b": ["a", "c"], "c": ["b"]}) is True

    def test_disconnected_graph(self):
        assert is_connected({"a": ["b"], "c": ["d"], "d": ["c"]}) is False

    def test_connected_components(self):
        graph = {"a": ["b"], "c": ["d"], "e": []}
        assert count_connected_components(graph) == 3


class TestGraphDensity:
    def test_empty_graph(self):
        assert graph_density({}) == 0.0

    def test_complete_graph(self):
        """Complete graph K4 has density 1."""
        graph = {"a": ["b", "c", "d"], "b": ["a", "c", "d"],
                 "c": ["a", "b", "d"], "d": ["a", "b", "c"]}
        assert abs(graph_density(graph) - 1.0) < 1e-9

    def test_star_graph(self):
        """Star graph K1,4 density."""
        graph = {"0": ["1", "2", "3", "4"],
                 "1": ["0"], "2": ["0"], "3": ["0"], "4": ["0"]}
        # 4 edges / 10 possible = 0.4
        assert abs(graph_density(graph) - 0.4) < 1e-9


class TestShortestPath:
    def test_direct_path(self):
        graph = {"a": ["b"], "b": ["a"]}
        assert shortest_path_length(graph, "a", "b") == 1

    def test_no_path(self):
        graph = {"a": [], "b": []}
        assert shortest_path_length(graph, "a", "b") is None

    def test_longer_path(self):
        graph = {"a": ["b"], "b": ["c"], "c": []}
        assert shortest_path_length(graph, "a", "c") == 2


class TestAllPairsShortestPaths:
    def test_small_graph(self):
        graph = {"a": ["b"], "b": ["c"], "c": []}
        paths = all_pairs_shortest_paths(graph)
        assert paths[("a", "c")] == 2
        # Directed graph: only "b" -> "a" if "a" in b's neighbors, but it's not
        # Instead check "b" -> "c" exists
        assert paths[("b", "c")] == 1


class TestEccentricityRadiusDiameter:
    def test_diameter_and_radius_complete(self):
        """Complete graph K3: diameter = 1, radius = 1."""
        graph = {"a": ["b", "c"], "b": ["a", "c"], "c": ["a", "b"]}
        assert graph_diameter(graph) == 1
        assert graph_radius(graph) == 1

    def test_diameter_line_graph(self):
        """Line graph of 3 nodes: diameter = 2, radius = 1 (middle)."""
        graph = {"a": ["b"], "b": ["a", "c"], "c": ["b"]}
        assert graph_diameter(graph) == 2
        assert graph_radius(graph) == 1