"""Usage examples for graph_metrics_utils."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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


def main():
    # Social network example
    print("=== Social Network Analysis ===")
    social_graph = {
        "Alice":   ["Bob", "Carol", "David"],
        "Bob":     ["Alice", "Carol", "Eve"],
        "Carol":   ["Alice", "Bob", "David", "Eve"],
        "David":   ["Alice", "Carol"],
        "Eve":     ["Bob", "Carol"],
    }

    print("\nDegree Centrality:")
    for person in social_graph:
        dc = degree_centrality(social_graph, person)
        print(f"  {person}: {dc:.3f}")

    print("\nCloseness Centrality:")
    for person in social_graph:
        cc = closeness_centrality(social_graph, person)
        print(f"  {person}: {cc:.3f}")

    print("\nPageRank:")
    ranks = page_rank(social_graph)
    for person, rank in sorted(ranks.items(), key=lambda x: -x[1]):
        print(f"  {person}: {rank:.4f}")

    print("\nClustering Coefficient:")
    for person in social_graph:
        coef = clustering_coefficient(social_graph, person)
        print(f"  {person}: {coef:.3f}")
    print(f"  Average: {average_clustering_coefficient(social_graph):.3f}")

    # Infrastructure network example
    print("\n=== Infrastructure Network ===")
    network_graph = {
        "RouterA": ["RouterB", "RouterC"],
        "RouterB": ["RouterA", "RouterC", "RouterD"],
        "RouterC": ["RouterA", "RouterB", "Server1"],
        "RouterD": ["RouterB", "Server2"],
        "Server1": ["RouterC"],
        "Server2": ["RouterD"],
    }

    print(f"Connected: {is_connected(network_graph)}")
    print(f"Components: {count_connected_components(network_graph)}")
    print(f"Density: {graph_density(network_graph):.3f}")
    print(f"Diameter: {graph_diameter(network_graph)}")
    print(f"Radius: {graph_radius(network_graph)}")

    print("\nShortest paths:")
    print(f"  RouterA -> Server1: {shortest_path_length(network_graph, 'RouterA', 'Server1')} hops")
    print(f"  RouterA -> Server2: {shortest_path_length(network_graph, 'RouterA', 'Server2')} hops")

    print("\nAll-pairs shortest paths (sample):")
    paths = all_pairs_shortest_paths(network_graph)
    sample_keys = [("RouterA", "Server1"), ("RouterA", "Server2"), ("RouterD", "RouterC")]
    for k in sample_keys:
        print(f"  {k[0]} -> {k[1]}: {paths.get(k, 'N/A')}")

    # Betweenness centrality example
    print("\nBetweenness Centrality:")
    for node in network_graph:
        bc = betweenness_centrality(network_graph, node)
        print(f"  {node}: {bc:.3f}")


if __name__ == "__main__":
    main()