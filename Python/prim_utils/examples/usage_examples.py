"""
Prim's Algorithm Utilities - Usage Examples

Comprehensive examples demonstrating all features of the prim_utils module.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    PrimGraph, Edge, MSTAlgorithm,
    prim_mst, kruskal_mst, boruvka_mst, minimum_spanning_tree,
    compare_algorithms, is_connected_graph, get_connected_components
)


def example_basic_usage():
    """Basic usage example."""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    # Create a graph
    g = PrimGraph()
    g.add_edge('A', 'B', 4)
    g.add_edge('A', 'C', 2)
    g.add_edge('B', 'C', 1)
    g.add_edge('B', 'D', 5)
    g.add_edge('C', 'D', 8)
    g.add_edge('C', 'E', 10)
    g.add_edge('D', 'E', 2)
    
    print("\nGraph created with 5 nodes and 7 edges")
    
    # Find MST
    mst = g.minimum_spanning_tree()
    
    print(f"\nMinimum Spanning Tree:")
    print(f"  Connected: {mst.connected}")
    print(f"  Nodes: {mst.node_count}")
    print(f"  Edges: {mst.edge_count}")
    print(f"  Total Weight: {mst.total_weight}")
    print(f"\nMST Edges:")
    for edge in mst.edges:
        print(f"    {edge.source} -- {edge.target} (weight: {edge.weight})")


def example_adding_edges():
    """Different ways to add edges."""
    print("\n" + "=" * 60)
    print("Example 2: Adding Edges")
    print("=" * 60)
    
    g = PrimGraph()
    
    # Add single edge
    g.add_edge('A', 'B', 1)
    
    # Add multiple edges at once
    g.add_edges([
        ('B', 'C', 2),
        ('C', 'D', 3),
        ('D', 'E', 4),
        ('E', 'A', 5),
    ])
    
    # Edge with default weight (1.0)
    g.add_edge('A', 'C')
    
    print(f"\nGraph has {g.node_count} nodes and {g.edge_count} edges")
    
    mst = g.minimum_spanning_tree()
    print(f"MST weight: {mst.total_weight}")


def example_different_algorithms():
    """Compare Prim's, Kruskal's, and Borůvka's algorithms."""
    print("\n" + "=" * 60)
    print("Example 3: Comparing Algorithms")
    print("=" * 60)
    
    g = PrimGraph()
    g.add_edges([
        ('A', 'B', 4),
        ('A', 'C', 2),
        ('B', 'C', 1),
        ('B', 'D', 5),
        ('C', 'D', 8),
        ('D', 'E', 2),
    ])
    
    print("\n--- Prim's Algorithm ---")
    prim_result = g.minimum_spanning_tree(algorithm=MSTAlgorithm.PRIM)
    for edge in prim_result.edges:
        print(f"  {edge.source} -- {edge.target}: {edge.weight}")
    print(f"  Total: {prim_result.total_weight}")
    
    print("\n--- Kruskal's Algorithm ---")
    kruskal_result = g.minimum_spanning_tree(algorithm=MSTAlgorithm.KRUSKAL)
    for edge in kruskal_result.edges:
        print(f"  {edge.source} -- {edge.target}: {edge.weight}")
    print(f"  Total: {kruskal_result.total_weight}")
    
    print("\n--- Borůvka's Algorithm ---")
    boruvka_result = g.minimum_spanning_tree(algorithm=MSTAlgorithm.BORUVKA)
    for edge in boruvka_result.edges:
        print(f"  {edge.source} -- {edge.target}: {edge.weight}")
    print(f"  Total: {boruvka_result.total_weight}")
    
    # Using compare_algorithms helper
    print("\n--- Using compare_algorithms() ---")
    results = compare_algorithms(g)
    for name, result in results.items():
        print(f"  {name}: weight = {result.total_weight}")


def example_graph_representations():
    """Create graphs from different representations."""
    print("\n" + "=" * 60)
    print("Example 4: Graph Representations")
    print("=" * 60)
    
    # From adjacency list
    print("\n--- From Adjacency List ---")
    adj_list = {
        'A': [('B', 1), ('C', 2)],
        'B': [('C', 3)],
        'C': [('D', 4)],
        'D': []
    }
    g1 = PrimGraph.from_adjacency_list(adj_list)
    mst1 = g1.minimum_spanning_tree()
    print(f"MST weight: {mst1.total_weight}")
    
    # From edge list
    print("\n--- From Edge List ---")
    edge_list = [
        ('A', 'B', 1),
        ('B', 'C', 2),
        ('C', 'D', 3),
        ('D', 'A', 4),
    ]
    g2 = PrimGraph.from_edge_list(edge_list)
    mst2 = g2.minimum_spanning_tree()
    print(f"MST weight: {mst2.total_weight}")
    
    # From adjacency matrix
    print("\n--- From Adjacency Matrix ---")
    matrix = [
        [0, 2, 0, 1],
        [2, 0, 3, 4],
        [0, 3, 0, 2],
        [1, 4, 2, 0]
    ]
    nodes = ['A', 'B', 'C', 'D']
    g3 = PrimGraph.from_adjacency_matrix(matrix, nodes=nodes)
    mst3 = g3.minimum_spanning_tree()
    print(f"MST weight: {mst3.total_weight}")


def example_disconnected_graph():
    """Handle disconnected graphs."""
    print("\n" + "=" * 60)
    print("Example 5: Disconnected Graphs")
    print("=" * 60)
    
    g = PrimGraph()
    
    # Component 1: A-B-C
    g.add_edges([('A', 'B', 1), ('B', 'C', 2)])
    
    # Component 2: D-E-F
    g.add_edges([('D', 'E', 3), ('E', 'F', 4), ('D', 'F', 5)])
    
    # Isolated node
    g.add_node('G')
    
    print(f"\nGraph has {g.node_count} nodes")
    print(f"Is connected: {is_connected_graph(g)}")
    
    components = get_connected_components(g)
    print(f"Number of components: {len(components)}")
    for i, comp in enumerate(components, 1):
        print(f"  Component {i}: {sorted(comp)}")
    
    # Find MST for each component
    print("\n--- Minimum Spanning Forest ---")
    forest = g.minimum_spanning_forest()
    print(f"Total weight: {forest.total_weight}")
    for i, tree in enumerate(forest.trees, 1):
        print(f"\nTree {i}: {tree.node_count} nodes, weight {tree.total_weight}")
        for edge in tree.edges:
            print(f"    {edge.source} -- {edge.target}")


def example_different_node_types():
    """Use different types of node labels."""
    print("\n" + "=" * 60)
    print("Example 6: Different Node Types")
    print("=" * 60)
    
    # Integer nodes
    print("\n--- Integer Nodes ---")
    g_int = PrimGraph()
    g_int.add_edges([
        (0, 1, 2),
        (1, 2, 3),
        (0, 2, 4),
    ])
    mst = g_int.minimum_spanning_tree()
    print(f"MST weight: {mst.total_weight}")
    
    # Tuple nodes (grid coordinates)
    print("\n--- Tuple Nodes (Grid) ---")
    g_grid = PrimGraph()
    g_grid.add_edges([
        ((0, 0), (0, 1), 1),
        ((0, 0), (1, 0), 2),
        ((0, 1), (1, 1), 3),
        ((1, 0), (1, 1), 4),
        ((0, 1), (1, 0), 5),
    ])
    mst = g_grid.minimum_spanning_tree()
    print(f"MST weight: {mst.total_weight}")
    for edge in mst.edges:
        print(f"  {edge.source} -- {edge.target}")


def example_convenience_functions():
    """Use convenience functions for quick MST computation."""
    print("\n" + "=" * 60)
    print("Example 7: Convenience Functions")
    print("=" * 60)
    
    # Using adjacency list directly
    adj = {
        'A': [('B', 1), ('C', 3)],
        'B': [('C', 2), ('D', 4)],
        'C': [('D', 5)],
        'D': []
    }
    
    print("\n--- Using prim_mst() ---")
    mst = prim_mst(adj)
    print(f"MST weight: {mst.total_weight}")
    
    print("\n--- Using kruskal_mst() ---")
    mst = kruskal_mst(adj)
    print(f"MST weight: {mst.total_weight}")
    
    print("\n--- Using boruvka_mst() ---")
    mst = boruvka_mst(adj)
    print(f"MST weight: {mst.total_weight}")
    
    # Using edge list directly
    print("\n--- Using edge list ---")
    edges = [('A', 'B', 1), ('B', 'C', 2), ('C', 'D', 3), ('A', 'D', 4)]
    mst = minimum_spanning_tree(edges)
    print(f"MST weight: {mst.total_weight}")


def example_network_design():
    """Real-world example: Network design problem."""
    print("\n" + "=" * 60)
    print("Example 8: Network Design Problem")
    print("=" * 60)
    
    # Cities and their connection costs (in thousands)
    cities = [
        ('New York', 'Boston', 215),
        ('New York', 'Philadelphia', 97),
        ('New York', 'Washington', 225),
        ('Boston', 'Chicago', 983),
        ('Philadelphia', 'Washington', 140),
        ('Chicago', 'Detroit', 280),
        ('Detroit', 'Cleveland', 170),
        ('Cleveland', 'Pittsburgh', 135),
        ('Pittsburgh', 'Philadelphia', 305),
        ('Washington', 'Atlanta', 640),
        ('Atlanta', 'Miami', 660),
        ('Miami', 'Tampa', 280),
    ]
    
    g = PrimGraph()
    g.add_edges(cities)
    
    print(f"\nNetwork: {g.node_count} cities, {g.edge_count} potential connections")
    
    # Find minimum cost to connect all cities
    mst = g.minimum_spanning_tree()
    
    print(f"\nMinimum Spanning Tree (optimal network):")
    print(f"  Total cost: ${mst.total_weight * 1000:,.0f}")
    print(f"  Connections needed: {mst.edge_count}")
    print("\n  Optimal connections:")
    for edge in sorted(mst.edges, key=lambda e: e.weight):
        print(f"    {edge.source} -- {edge.target}: ${edge.weight * 1000:,.0f}")


def example_circuit_design():
    """Real-world example: PCB circuit design."""
    print("\n" + "=" * 60)
    print("Example 9: PCB Circuit Design")
    print("=" * 60)
    
    # Components on a PCB with wire lengths
    # Using coordinates as node labels
    components = {
        'CPU': (0, 0),
        'RAM': (0, 2),
        'GPU': (2, 0),
        'SSD': (2, 2),
        'USB': (4, 0),
        'Power': (4, 2),
    }
    
    g = PrimGraph()
    
    # Calculate distances between all components
    comp_names = list(components.keys())
    for i in range(len(comp_names)):
        for j in range(i + 1, len(comp_names)):
            c1, c2 = comp_names[i], comp_names[j]
            x1, y1 = components[c1]
            x2, y2 = components[c2]
            distance = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
            g.add_edge(c1, c2, distance)
    
    print(f"\nPCB has {g.node_count} components")
    
    # Minimum wire length to connect all components
    mst = g.minimum_spanning_tree()
    
    print(f"\nMinimum wire length: {mst.total_weight:.2f} units")
    print("Optimal wiring:")
    for edge in mst.edges:
        print(f"  {edge.source} -- {edge.target}: {edge.weight:.2f} units")


def example_pipeline_network():
    """Real-world example: Pipeline network."""
    print("\n" + "=" * 60)
    print("Example 10: Pipeline Network")
    print("=" * 60)
    
    # Oil wells and refinery connections
    # Costs in millions
    pipeline_costs = [
        ('Well_1', 'Refinery', 2.5),
        ('Well_2', 'Refinery', 3.1),
        ('Well_3', 'Refinery', 2.8),
        ('Well_1', 'Well_2', 1.2),
        ('Well_2', 'Well_3', 0.9),
        ('Well_1', 'Well_3', 1.5),
        ('Well_3', 'Well_4', 1.1),
        ('Well_4', 'Refinery', 2.2),
    ]
    
    g = PrimGraph()
    g.add_edges(pipeline_costs)
    
    print(f"\nOil field: {g.node_count} nodes (4 wells + 1 refinery)")
    
    mst = g.minimum_spanning_tree()
    
    print(f"\nOptimal pipeline network:")
    print(f"  Total cost: ${mst.total_weight:.1f}M")
    print("  Pipelines to build:")
    for edge in sorted(mst.edges, key=lambda e: e.weight):
        print(f"    {edge.source} -- {edge.target}: ${edge.weight:.1f}M")


def example_clustering():
    """Use MST for clustering."""
    print("\n" + "=" * 60)
    print("Example 11: MST-based Clustering")
    print("=" * 60)
    
    # Points in 2D space
    points = {
        'A': (0, 0),
        'B': (1, 0),
        'C': (0, 1),
        'D': (8, 8),
        'E': (9, 8),
        'F': (8, 9),
        'G': (4, 4),  # Outlier
    }
    
    g = PrimGraph()
    
    # Connect all points with distances
    names = list(points.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            n1, n2 = names[i], names[j]
            x1, y1 = points[n1]
            x2, y2 = points[n2]
            dist = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
            g.add_edge(n1, n2, dist)
    
    mst = g.minimum_spanning_tree()
    
    print("\nPoints and their positions:")
    for name, pos in points.items():
        print(f"  {name}: {pos}")
    
    print(f"\nMST total length: {mst.total_weight:.2f}")
    
    # Remove the longest edge to get 2 clusters
    sorted_edges = sorted(mst.edges, key=lambda e: e.weight, reverse=True)
    longest = sorted_edges[0]
    
    print(f"\nLongest edge: {longest.source} -- {longest.target} ({longest.weight:.2f})")
    print("Removing it creates 2 clusters")
    
    # Create graph without longest edge
    g_cluster = g.copy()
    g_cluster.remove_edge(longest.source, longest.target)
    
    clusters = g_cluster.get_connected_components()
    print(f"\nClusters ({len(clusters)}):")
    for i, cluster in enumerate(clusters, 1):
        print(f"  Cluster {i}: {sorted(cluster)}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("PRIM'S ALGORITHM UTILITIES - USAGE EXAMPLES")
    print("=" * 60)
    
    example_basic_usage()
    example_adding_edges()
    example_different_algorithms()
    example_graph_representations()
    example_disconnected_graph()
    example_different_node_types()
    example_convenience_functions()
    example_network_design()
    example_circuit_design()
    example_pipeline_network()
    example_clustering()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()