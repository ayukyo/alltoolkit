"""
PageRank Utilities - Usage Examples

Demonstrates various use cases for PageRank algorithm:
1. Web page importance ranking
2. Social network influence analysis
3. Recommendation systems
4. Graph analysis and statistics
"""

import sys
import os

# Add parent directory (pagerank_utils) to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Graph, pagerank, pagerank_weighted, personalized_pagerank,
    get_top_k, get_rankings, compute_centrality, detect_communities_by_scores,
    build_graph_from_edge_list, build_graph_from_adjacency_list,
    l1_distance
)


def example_web_page_ranking():
    """
    Example 1: Ranking web pages by importance
    
    Simulates a simple website structure where PageRank identifies
    the most important pages based on link structure.
    """
    print("=" * 60)
    print("Example 1: Web Page Importance Ranking")
    print("=" * 60)
    
    # Create a website graph
    graph = Graph()
    
    # Homepage links to main sections
    graph.add_edge('home', 'products')
    graph.add_edge('home', 'about')
    graph.add_edge('home', 'blog')
    
    # Products section
    graph.add_edge('products', 'home')
    graph.add_edge('products', 'product1')
    graph.add_edge('products', 'product2')
    graph.add_edge('products', 'product3')
    
    # About section
    graph.add_edge('about', 'home')
    graph.add_edge('about', 'contact')
    
    # Blog section
    graph.add_edge('blog', 'home')
    graph.add_edge('blog', 'post1')
    graph.add_edge('blog', 'post2')
    graph.add_edge('post1', 'post2')
    graph.add_edge('post2', 'post1')
    
    # All subsections link back to home
    graph.add_edge('product1', 'products')
    graph.add_edge('product2', 'products')
    graph.add_edge('product3', 'products')
    graph.add_edge('contact', 'about')
    
    # Get graph statistics
    stats = graph.get_statistics()
    print(f"\nWebsite Statistics:")
    print(f"  Pages: {stats['node_count']}")
    print(f"  Links: {stats['edge_count']}")
    print(f"  Average outgoing links: {stats['avg_out_degree']:.2f}")
    
    # Compute PageRank
    scores = pagerank(graph, damping=0.85)
    
    # Show top pages
    top_pages = get_top_k(scores, 5)
    print(f"\nTop 5 Most Important Pages:")
    for page, score in top_pages:
        print(f"  {page}: {score:.4f} ({score*100:.2f}%)")
    
    # Show rankings
    rankings = get_rankings(scores)
    print(f"\nFull Rankings:")
    for page in sorted(rankings.keys(), key=lambda x: rankings[x]):
        print(f"  Rank {rankings[page]}: {page} (score: {scores[page]:.4f})")
    
    print()


def example_social_network():
    """
    Example 2: Social network influence analysis
    
    Analyzes who is most influential in a social network based on
    follower relationships.
    """
    print("=" * 60)
    print("Example 2: Social Network Influence Analysis")
    print("=" * 60)
    
    # Create social network (A follows B means edge A -> B)
    edges = [
        ('alice', 'bob'),
        ('alice', 'charlie'),
        ('bob', 'alice'),
        ('bob', 'david'),
        ('charlie', 'alice'),
        ('charlie', 'david'),
        ('david', 'alice'),
        ('david', 'eve'),
        ('eve', 'alice'),
        ('eve', 'charlie'),
        ('frank', 'bob'),
        ('frank', 'charlie'),
    ]
    
    graph = build_graph_from_edge_list(edges)
    
    print(f"\nNetwork Statistics:")
    stats = graph.get_statistics()
    print(f"  Users: {stats['node_count']}")
    print(f"  Follow relationships: {stats['edge_count']}")
    print(f"  Most outgoing follows: {stats['max_out_degree']}")
    print(f"  Most followers: {stats['max_in_degree']}")
    
    # Compute PageRank (influence score)
    scores = pagerank(graph)
    
    print(f"\nInfluence Rankings:")
    for user, score in get_top_k(scores, stats['node_count']):
        followers = graph.get_in_degree(user)
        print(f"  {user}: {score:.4f} ({followers} followers)")
    
    # Detect influence tiers
    tiers = detect_communities_by_scores(scores, num_tiers=3)
    print(f"\nInfluence Tiers:")
    for tier in [1, 2, 3]:
        tier_users = [u for u, t in tiers.items() if t == tier]
        print(f"  Tier {tier}: {', '.join(tier_users)}")
    
    print()


def example_weighted_network():
    """
    Example 3: Weighted network analysis
    
    Shows how edge weights affect PageRank scores.
    """
    print("=" * 60)
    print("Example 3: Weighted Network Analysis")
    print("=" * 60)
    
    graph = Graph()
    
    # Hub with weighted connections
    graph.add_edge('hub', 'page_a', weight=5.0)  # Strong link
    graph.add_edge('hub', 'page_b', weight=1.0)  # Weak link
    graph.add_edge('hub', 'page_c', weight=1.0)  # Weak link
    
    # Back links
    graph.add_edge('page_a', 'hub', weight=1.0)
    graph.add_edge('page_b', 'hub', weight=1.0)
    graph.add_edge('page_c', 'hub', weight=1.0)
    
    # Compare regular vs weighted PageRank (use relaxed threshold)
    regular_scores = pagerank(graph, threshold=1e-6)
    weighted_scores = pagerank_weighted(graph, threshold=1e-6)
    
    print(f"\nComparison of Regular vs Weighted PageRank:")
    print(f"\n{'Page':<10} {'Regular':<12} {'Weighted':<12} {'Difference':<12}")
    print("-" * 46)
    
    for page in sorted(graph.nodes):
        reg = regular_scores[page]
        wei = weighted_scores[page]
        diff = wei - reg
        print(f"{page:<10} {reg:.4f}       {wei:.4f}       {diff:+.4f}")
    
    # L1 distance between distributions
    distance = l1_distance(regular_scores, weighted_scores)
    print(f"\nL1 distance between distributions: {distance:.4f}")
    
    print("\nNote: Page A receives more rank in weighted version")
    print("      because it has higher incoming weight from hub.")
    print()


def example_personalized_search():
    """
    Example 4: Personalized PageRank for recommendations
    
    Uses personalized PageRank to find items relevant to user interests.
    """
    print("=" * 60)
    print("Example 4: Personalized PageRank for Recommendations")
    print("=" * 60)
    
    # Content graph: items link to related items
    graph = Graph()
    
    # Tech content cluster
    graph.add_edge('python_tutorial', 'machine_learning')
    graph.add_edge('python_tutorial', 'web_development')
    graph.add_edge('machine_learning', 'python_tutorial')
    graph.add_edge('machine_learning', 'data_science')
    graph.add_edge('data_science', 'machine_learning')
    graph.add_edge('web_development', 'javascript_guide')
    
    # Arts content cluster
    graph.add_edge('photography', 'design')
    graph.add_edge('design', 'photography')
    graph.add_edge('design', 'illustration')
    graph.add_edge('illustration', 'design')
    
    # Cross-cluster links
    graph.add_edge('web_development', 'design')
    graph.add_edge('javascript_guide', 'web_development')
    
    print(f"\nContent graph: {graph.node_count} topics, {graph.edge_count} relations")
    
    # User A is interested in tech (use relaxed threshold)
    tech_interests = ['python_tutorial', 'machine_learning']
    tech_scores = personalized_pagerank(graph, tech_interests, threshold=1e-6)
    
    print(f"\nUser A (Tech interests: {tech_interests}):")
    print("Recommended topics:")
    for topic, score in get_top_k(tech_scores, 5):
        print(f"  {topic}: {score:.4f}")
    
    # User B is interested in arts
    arts_interests = ['photography', 'design']
    arts_scores = personalized_pagerank(graph, arts_interests, threshold=1e-6)
    
    print(f"\nUser B (Arts interests: {arts_interests}):")
    print("Recommended topics:")
    for topic, score in get_top_k(arts_scores, 5):
        print(f"  {topic}: {score:.4f}")
    
    # Compare recommendations
    print(f"\nRecommendation difference:")
    diff = l1_distance(tech_scores, arts_scores)
    print(f"  L1 distance: {diff:.4f}")
    print("  (Higher distance = more personalized)")
    
    print()


def example_adjacency_list_input():
    """
    Example 5: Building graph from adjacency list
    
    Shows alternative ways to create graphs.
    """
    print("=" * 60)
    print("Example 5: Building Graph from Adjacency List")
    print("=" * 60)
    
    # Using dictionary format (with weights)
    weighted_adj = {
        'central': {'hub1': 2.0, 'hub2': 1.0, 'hub3': 1.0},
        'hub1': {'central': 1.0},
        'hub2': {'central': 1.0},
        'hub3': {'central': 1.0},
    }
    
    graph1 = build_graph_from_adjacency_list(weighted_adj)
    scores1 = pagerank_weighted(graph1, threshold=1e-6)
    
    print(f"\nWeighted adjacency list:")
    print(f"Graph: {graph1.node_count} nodes, {graph1.edge_count} edges")
    print(f"PageRank scores:")
    for node, score in get_top_k(scores1, graph1.node_count):
        print(f"  {node}: {score:.4f}")
    
    # Using set format (uniform weights)
    simple_adj = {
        'root': {'child1', 'child2', 'child3'},
        'child1': {'root'},
        'child2': {'root'},
        'child3': {'root'},
    }
    
    graph2 = build_graph_from_adjacency_list(simple_adj)
    scores2 = pagerank(graph2, threshold=1e-6)
    
    print(f"\nSimple adjacency list (sets):")
    print(f"Graph: {graph2.node_count} nodes, {graph2.edge_count} edges")
    print(f"PageRank scores:")
    for node, score in get_top_k(scores2, graph2.node_count):
        print(f"  {node}: {score:.4f}")
    
    print()


def example_centrality_analysis():
    """
    Example 6: Centrality and inequality analysis
    
    Analyzes the distribution of PageRank scores.
    """
    print("=" * 60)
    print("Example 6: Centrality and Inequality Analysis")
    print("=" * 60)
    
    # Create two different graph structures
    # Equal structure (cycle)
    cycle = Graph()
    for i in range(5):
        cycle.add_edge(str(i), str((i + 1) % 5))
    
    cycle_scores = pagerank(cycle)
    cycle_centrality = compute_centrality(cycle_scores)
    
    print(f"\nCycle graph (5 nodes in a ring):")
    print(f"  Gini coefficient: {cycle_centrality['gini']:.4f}")
    print(f"  (0 = perfect equality, all nodes equal importance)")
    print(f"  Mean score: {cycle_centrality['mean']:.4f}")
    print(f"  Std deviation: {cycle_centrality['std']:.4f}")
    
    # Unequal structure (hub-spoke)
    hub = Graph()
    hub.add_edge('center', 'spoke1')
    hub.add_edge('center', 'spoke2')
    hub.add_edge('center', 'spoke3')
    hub.add_edge('center', 'spoke4')
    hub.add_edge('spoke1', 'center')
    hub.add_edge('spoke2', 'center')
    hub.add_edge('spoke3', 'center')
    hub.add_edge('spoke4', 'center')
    
    hub_scores = pagerank(hub, threshold=1e-6)
    hub_centrality = compute_centrality(hub_scores)
    
    print(f"\nHub-spoke graph:")
    print(f"  Gini coefficient: {hub_centrality['gini']:.4f}")
    print(f"  (Higher = more inequality, hub dominates)")
    print(f"  Min score: {hub_centrality['min']:.4f} (spokes)")
    print(f"  Max score: {hub_centrality['max']:.4f} (center)")
    
    print("\nGini coefficient interpretation:")
    print("  < 0.3: Nearly equal importance")
    print("  0.3-0.5: Moderate inequality")
    print("  > 0.5: High inequality (dominant nodes)")
    
    print()


def example_dangling_nodes():
    """
    Example 7: Handling dangling nodes
    
    Shows how PageRank handles nodes with no outgoing edges.
    """
    print("=" * 60)
    print("Example 7: Dangling Nodes Handling")
    print("=" * 60)
    
    graph = Graph()
    
    # Sources link to targets, targets have no outgoing links
    graph.add_edge('source1', 'sink1')
    graph.add_edge('source1', 'sink2')
    graph.add_edge('source2', 'sink1')
    graph.add_edge('source2', 'sink3')
    
    # sink1, sink2, sink3 are dangling nodes
    dangling = graph.get_dangling_nodes()
    
    print(f"\nGraph structure:")
    print(f"  Sources: source1, source2 (have outgoing links)")
    print(f"  Sinks (dangling): {', '.join(dangling)}")
    
    scores = pagerank(graph)
    
    print(f"\nPageRank scores:")
    for node, score in get_top_k(scores, graph.node_count):
        is_dangling = node in dangling
        status = "(dangling)" if is_dangling else ""
        print(f"  {node}: {score:.4f} {status}")
    
    print("\nNote: Dangling nodes distribute their rank evenly to all nodes")
    print("      during teleportation, preventing rank loss.")
    
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("PageRank Utilities - Usage Examples")
    print("=" * 60 + "\n")
    
    example_web_page_ranking()
    example_social_network()
    example_weighted_network()
    example_personalized_search()
    example_adjacency_list_input()
    example_centrality_analysis()
    example_dangling_nodes()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()