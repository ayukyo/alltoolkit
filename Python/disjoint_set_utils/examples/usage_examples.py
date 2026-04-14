#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Disjoint Set Utilities Usage Examples
====================================================
Practical examples demonstrating various use cases of the DisjointSet module.

Run with: python usage_examples.py
"""

import sys
import os
# Add the AllToolkit root directory to path
_alltoolkit_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, _alltoolkit_root)

# Import using the correct module path from AllToolkit root
import importlib.util
spec = importlib.util.spec_from_file_location("mod", os.path.join(_alltoolkit_root, "Python", "disjoint_set_utils", "mod.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

DisjointSet = mod.DisjointSet
count_connected_components = mod.count_connected_components
find_connected_groups = mod.find_connected_groups
is_connected_graph = mod.is_connected_graph
detect_cycle_undirected = mod.detect_cycle_undirected
kruskal_mst = mod.kruskal_mst
find_friend_circles = mod.find_friend_circles
get_circle_sizes = mod.get_circle_sizes
find_connected_pixels = mod.find_connected_pixels


def example_basic_operations():
    """Basic union-find operations."""
    print("=" * 60)
    print("Example 1: Basic Union-Find Operations")
    print("=" * 60)
    
    # Create a new disjoint set
    ds = DisjointSet[int]()
    
    # Add elements as individual sets
    ds.make_sets(1, 2, 3, 4, 5, 6, 7, 8)
    print(f"Created 8 elements: {list(ds)}")
    print(f"Component count: {ds.component_count()}")
    
    # Merge some sets
    ds.union(1, 2)
    ds.union(2, 3)
    ds.union(4, 5)
    ds.union_all(6, 7, 8)
    
    print(f"\nAfter unions:")
    print(f"  1-2-3 merged: {ds.connected(1, 3)}")
    print(f"  4-5 merged: {ds.connected(4, 5)}")
    print(f"  6-7-8 merged: {ds.connected(6, 8)}")
    print(f"  1 and 4 not connected: {not ds.connected(1, 4)}")
    print(f"Component count: {ds.component_count()}")
    
    # Query operations
    print(f"\nComponent containing 1: {ds.get_component(1)}")
    print(f"Size of component with 1: {ds.component_size(1)}")
    print(f"All components: {ds.get_components()}")


def example_network_connectivity():
    """Network connectivity analysis."""
    print("\n" + "=" * 60)
    print("Example 2: Network Connectivity Analysis")
    print("=" * 60)
    
    # Simulate a computer network
    computers = ["Server1", "Server2", "Server3", "Server4", "Server5", "Server6"]
    connections = [
        ("Server1", "Server2"),
        ("Server2", "Server3"),
        ("Server4", "Server5"),
        # Server6 is isolated
    ]
    
    # Find connected groups
    groups = find_connected_groups(computers, connections)
    
    print("Network topology:")
    print("  Server1 --- Server2 --- Server3")
    print("  Server4 --- Server5")
    print("  Server6 (isolated)")
    print(f"\nConnected groups: {groups}")
    print(f"Number of network segments: {len(groups)}")
    
    # Check if entire network is connected
    print(f"\nIs network fully connected: {is_connected_graph(computers, connections)}")
    
    # Check connectivity between specific servers
    ds = DisjointSet[str]()
    ds.add_connections(connections)
    print(f"\nServer1 connected to Server3: {ds.connected('Server1', 'Server3')}")
    print(f"Server1 connected to Server5: {ds.connected('Server1', 'Server5')}")


def example_cycle_detection():
    """Detect cycles in undirected graphs."""
    print("\n" + "=" * 60)
    print("Example 3: Cycle Detection in Graphs")
    print("=" * 60)
    
    # Graph with cycle
    nodes_with_cycle = [1, 2, 3, 4]
    edges_with_cycle = [(1, 2), (2, 3), (3, 4), (4, 1)]  # Square
    
    print("Graph 1 (square with cycle):")
    print("  1 --- 2")
    print("  |     |")
    print("  4 --- 3")
    print(f"  Has cycle: {detect_cycle_undirected(nodes_with_cycle, edges_with_cycle)}")
    
    # Graph without cycle (tree)
    nodes_tree = [1, 2, 3, 4, 5]
    edges_tree = [(1, 2), (1, 3), (3, 4), (3, 5)]
    
    print("\nGraph 2 (tree without cycle):")
    print("    1")
    print("   / \\")
    print("  2   3")
    print("     / \\")
    print("    4   5")
    print(f"  Has cycle: {detect_cycle_undirected(nodes_tree, edges_tree)}")


def example_minimum_spanning_tree():
    """Kruskal's Minimum Spanning Tree algorithm."""
    print("\n" + "=" * 60)
    print("Example 4: Minimum Spanning Tree (Kruskal's Algorithm)")
    print("=" * 60)
    
    # Network of cities with connection costs
    cities = ['New York', 'Boston', 'Philadelphia', 'Washington', 'Chicago']
    
    # (city1, city2, cost_millions)
    connections = [
        ('New York', 'Boston', 2.5),
        ('New York', 'Philadelphia', 1.8),
        ('New York', 'Washington', 3.2),
        ('Boston', 'Chicago', 8.5),
        ('Philadelphia', 'Washington', 2.0),
        ('New York', 'Chicago', 7.0),
        ('Washington', 'Chicago', 9.0),
    ]
    
    print("Finding minimum cost network connecting all cities...")
    print("\nAvailable connections (cost in millions):")
    for c1, c2, cost in sorted(connections, key=lambda x: x[2]):
        print(f"  {c1} <-> {c2}: ${cost}M")
    
    mst_edges, total_cost = kruskal_mst(cities, connections)
    
    print(f"\nMinimum Spanning Tree:")
    print(f"  Edges to build:")
    for c1, c2, cost in mst_edges:
        print(f"    {c1} <-> {c2}: ${cost}M")
    print(f"  Total cost: ${total_cost}M")
    print(f"  Cities connected: {len(mst_edges) + 1}/{len(cities)}")


def example_social_network():
    """Social network friend circle analysis."""
    print("\n" + "=" * 60)
    print("Example 5: Social Network Friend Circles")
    print("=" * 60)
    
    users = ['Alice', 'Bob', 'Carol', 'David', 'Eve', 'Frank', 'Grace']
    friendships = [
        ('Alice', 'Bob'),
        ('Bob', 'Carol'),
        ('David', 'Eve'),
        ('Eve', 'Frank'),
        # Grace has no friends yet :(
    ]
    
    print("Social Network:")
    print("  Alice -- Bob -- Carol")
    print("  David -- Eve -- Frank")
    print("  Grace (new user)")
    
    # Find friend circles
    circles = find_friend_circles(users, friendships)
    print(f"\nFriend circles (by representative):")
    circle_groups = {}
    for user, rep in circles.items():
        if rep not in circle_groups:
            circle_groups[rep] = []
        circle_groups[rep].append(user)
    
    for i, (rep, members) in enumerate(circle_groups.items(), 1):
        print(f"  Circle {i}: {members}")
    
    # Get circle sizes
    sizes = get_circle_sizes(users, friendships)
    print(f"\nCircle sizes:")
    for user in users:
        print(f"  {user}: {sizes[user]} friend(s) in circle")


def example_image_processing():
    """Connected component labeling in images."""
    print("\n" + "=" * 60)
    print("Example 6: Image Connected Component Labeling")
    print("=" * 60)
    
    # Binary image (1 = foreground, 0 = background)
    image = [
        [1, 1, 0, 0, 1],
        [1, 1, 0, 1, 1],
        [0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0]
    ]
    
    print("Original binary image:")
    for row in image:
        print("  " + " ".join(['█' if p else '·' for p in row]))
    
    # Label connected components
    labeled = find_connected_pixels(image, connectivity=4)
    
    print("\nLabeled components:")
    for row in labeled:
        print("  " + " ".join([str(c) if c > 0 else '·' for c in row]))
    
    # Count objects
    num_objects = max(max(row) for row in labeled)
    print(f"\nNumber of distinct objects detected: {num_objects}")
    
    # With 8-connectivity
    labeled_8 = find_connected_pixels(image, connectivity=8)
    num_objects_8 = max(max(row) for row in labeled_8)
    print(f"With 8-connectivity: {num_objects_8} objects")


def example_equivalence_classes():
    """Group elements by equivalence relations."""
    print("\n" + "=" * 60)
    print("Example 7: Equivalence Classes")
    print("=" * 60)
    
    # Suppose we have items that should be grouped as equivalent
    items = ['apple', 'orange', 'banana', 'carrot', 'potato', 'tomato']
    
    # Equivalence rules: fruits together, vegetables together
    equivalences = [
        ('apple', 'orange'),
        ('orange', 'banana'),
        ('carrot', 'potato'),
        ('potato', 'tomato'),  # tomato is technically a fruit but grouped as veg
    ]
    
    print("Items:", items)
    print("Equivalence rules:", equivalences)
    
    groups = find_connected_groups(items, equivalences)
    
    print("\nGrouped by equivalence:")
    for i, group in enumerate(groups, 1):
        print(f"  Group {i}: {sorted(group)}")


def example_island_counting():
    """Count islands in a grid (LeetCode style problem)."""
    print("\n" + "=" * 60)
    print("Example 8: Island Counting")
    print("=" * 60)
    
    # 1 = land, 0 = water
    grid = [
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1]
    ]
    
    print("Grid (█ = land, · = water):")
    for row in grid:
        print("  " + " ".join(['█' if c else '·' for c in row]))
    
    # Convert grid coordinates to nodes and find connected land
    rows, cols = len(grid), len(grid[0])
    nodes = []
    edges = []
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                nodes.append((r, c))
                # Add edges to adjacent land cells
                if r > 0 and grid[r-1][c] == 1:
                    edges.append(((r, c), (r-1, c)))
                if c > 0 and grid[r][c-1] == 1:
                    edges.append(((r, c), (r, c-1)))
    
    num_islands = count_connected_components(nodes, edges)
    print(f"\nNumber of islands: {num_islands}")


def example_dynamic_connectivity():
    """Dynamic connectivity problem."""
    print("\n" + "=" * 60)
    print("Example 9: Dynamic Connectivity Simulation")
    print("=" * 60)
    
    ds = DisjointSet[int]()
    
    # Simulate network connections over time
    operations = [
        ("add", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ("connect", 1, 2),
        ("connect", 3, 4),
        ("check", 1, 2),
        ("check", 1, 3),
        ("connect", 2, 3),
        ("check", 1, 4),
        ("connect", 5, 6),
        ("connect", 6, 7),
        ("connect", 8, 9),
        ("connect", 9, 10),
        ("connect", 7, 8),
        ("check", 5, 10),
        ("count", None, None),
        ("connect", 1, 5),
        ("count", None, None),
        ("check", 1, 10),
    ]
    
    for op in operations:
        if op[0] == "add":
            elements = op[1]
            ds.make_sets(*elements)
            print(f"Added elements: {elements}")
        
        elif op[0] == "connect":
            e1, e2 = op[1], op[2]
            ds.union(e1, e2)
            print(f"Connected {e1} <-> {e2}")
        
        elif op[0] == "check":
            e1, e2 = op[1], op[2]
            result = ds.connected(e1, e2)
            print(f"  Are {e1} and {e2} connected? {result}")
        
        elif op[0] == "count":
            print(f"  Component count: {ds.component_count()}")


def example_serialization():
    """Save and restore disjoint set state."""
    print("\n" + "=" * 60)
    print("Example 10: Serialization and Persistence")
    print("=" * 60)
    
    # Create and populate a disjoint set
    ds1 = DisjointSet[str]()
    ds1.make_sets('A', 'B', 'C', 'D', 'E')
    ds1.union('A', 'B')
    ds1.union('B', 'C')
    ds1.union('D', 'E')
    
    print("Original disjoint set:")
    print(f"  Components: {ds1.get_components()}")
    
    # Serialize to dictionary
    data = ds1.to_dict()
    print(f"\nSerialized (can be saved to JSON):")
    print(f"  parent mapping: {data['parent']}")
    print(f"  ranks: {data['rank']}")
    
    # Restore from dictionary
    ds2 = DisjointSet[str].from_dict(data)
    print(f"\nRestored disjoint set:")
    print(f"  Components: {ds2.get_components()}")
    print(f"  A connected to C: {ds2.connected('A', 'C')}")


def main():
    """Run all examples."""
    example_basic_operations()
    example_network_connectivity()
    example_cycle_detection()
    example_minimum_spanning_tree()
    example_social_network()
    example_image_processing()
    example_equivalence_classes()
    example_island_counting()
    example_dynamic_connectivity()
    example_serialization()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()