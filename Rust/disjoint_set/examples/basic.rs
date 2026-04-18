//! Basic usage examples for DisjointSet
//!
//! Run with: cargo run --example basic

use disjoint_set::{DisjointSet, LabeledDisjointSet, UnionStrategy};

fn main() {
    println!("=== DisjointSet (Union-Find) Examples ===\n");
    
    // Example 1: Basic Union-Find Operations
    println!("1. Basic Union-Find Operations");
    println!("-------------------------------");
    basic_operations();
    
    // Example 2: Connected Components
    println!("\n2. Finding Connected Components");
    println!("--------------------------------");
    connected_components();
    
    // Example 3: Kruskal's MST Algorithm
    println!("\n3. Kruskal's Minimum Spanning Tree");
    println!("-----------------------------------");
    kruskal_mst();
    
    // Example 4: Union Strategies
    println!("\n4. Union Strategies (Rank vs Size)");
    println!("-----------------------------------");
    union_strategies();
    
    // Example 5: Labeled DisjointSet
    println!("\n5. Labeled DisjointSet with Strings");
    println!("-------------------------------------");
    labeled_example();
    
    // Example 6: Social Network Analysis
    println!("\n6. Social Network Analysis");
    println!("----------------------------");
    social_network();
    
    // Example 7: Image Connected Components
    println!("\n7. Image Connected Regions");
    println!("---------------------------");
    image_regions();
    
    // Example 8: Batch Operations
    println!("\n8. Batch Operations");
    println!("--------------------");
    batch_operations();
}

fn basic_operations() {
    let mut ds = DisjointSet::new(10);
    
    println!("Created DisjointSet with 10 elements");
    println!("Initial set count: {}", ds.set_count());
    
    // Union some elements
    ds.union(0, 1);
    ds.union(2, 3);
    ds.union(1, 2);
    
    println!("\nAfter union(0,1), union(2,3), union(1,2):");
    println!("  Set count: {}", ds.set_count());
    println!("  connected(0,3): {}", ds.connected(0, 3));
    println!("  connected(0,4): {}", ds.connected(0, 4));
    println!("  Set size of 0: {}", ds.set_size(0));
    
    // Reset
    ds.reset();
    println!("\nAfter reset:");
    println!("  Set count: {}", ds.set_count());
}

fn connected_components() {
    // Graph edges
    let edges = vec![
        (0, 1), (1, 2), (3, 4), (4, 5), (6, 7)
    ];
    
    let mut ds = DisjointSet::from_edges(8, edges);
    
    println!("Graph with edges: (0-1), (1-2), (3-4), (4-5), (6-7)");
    
    let sets = ds.all_sets();
    println!("\nFound {} connected components:", sets.len());
    
    for (i, set) in sets.iter().enumerate() {
        let elements: Vec<_> = set.iter().collect();
        println!("  Component {}: {:?}", i, elements);
    }
}

fn kruskal_mst() {
    // Graph: 4 vertices, weighted edges
    // [(from, to, weight)]
    let mut edges = vec![
        (0, 1, 10),
        (0, 2, 6),
        (0, 3, 5),
        (1, 3, 15),
        (2, 3, 4),
    ];
    
    // Sort edges by weight
    edges.sort_by_key(|e| e.2);
    
    let mut ds = DisjointSet::new(4);
    let mut mst_weight = 0;
    let mut mst_edges = Vec::new();
    
    println!("Edges sorted by weight:");
    for (u, v, w) in &edges {
        println!("  {} -- {} (weight: {})", u, v, w);
    }
    
    for (u, v, w) in edges {
        if ds.union(u, v) {
            mst_weight += w;
            mst_edges.push((u, v, w));
        }
    }
    
    println!("\nMinimum Spanning Tree:");
    for (u, v, w) in &mst_edges {
        println!("  {} -- {} (weight: {})", u, v, w);
    }
    println!("Total weight: {}", mst_weight);
}

fn union_strategies() {
    // Compare ByRank vs BySize
    let mut ds_rank = DisjointSet::with_strategy(8, UnionStrategy::ByRank);
    let mut ds_size = DisjointSet::with_strategy(8, UnionStrategy::BySize);
    
    println!("Creating tree with 8 elements:");
    
    // Create chain
    for i in 0..7 {
        ds_rank.union(i, i + 1);
        ds_size.union(i, i + 1);
    }
    
    println!("\nByRank strategy:");
    println!("  Final set count: {}", ds_rank.set_count());
    println!("  All elements connected: {}", ds_rank.connected(0, 7));
    
    println!("\nBySize strategy:");
    println!("  Final set count: {}", ds_size.set_count());
    println!("  All elements connected: {}", ds_size.connected(0, 7));
}

fn labeled_example() {
    let mut ds: LabeledDisjointSet<&str> = LabeledDisjointSet::from_elements(
        vec!["Alice", "Bob", "Charlie", "David", "Eve"]
    );
    
    println!("Created labeled set with: Alice, Bob, Charlie, David, Eve");
    
    // Create friend groups
    ds.union(&"Alice", &"Bob");
    ds.union(&"Bob", &"Charlie");
    ds.union(&"David", &"Eve");
    
    println!("\nFriend groups:");
    let groups = ds.all_sets();
    for (i, group) in groups.iter().enumerate() {
        let members: Vec<_> = group.iter().collect();
        println!("  Group {}: {:?}", i, members);
    }
    
    println!("\nAre Alice and Charlie in the same group? {}", 
        ds.connected(&"Alice", &"Charlie"));
    println!("Are Alice and David in the same group? {}", 
        ds.connected(&"Alice", &"David"));
}

fn social_network() {
    // Simulating a social network with friend connections
    let connections = vec![
        ("user1", "user2"),
        ("user2", "user3"),
        ("user4", "user5"),
        ("user5", "user6"),
        ("user7", "user8"),
    ];
    
    let mut ds: LabeledDisjointSet<&str> = LabeledDisjointSet::new();
    
    for (a, b) in &connections {
        ds.union(a, b);
    }
    
    println!("Social network analysis:");
    println!("  Total users: {}", ds.len());
    println!("  Friend groups: {}", ds.set_count());
    
    // Find the largest group
    let groups = ds.all_sets();
    let largest = groups.iter().max_by_key(|g| g.len()).unwrap();
    println!("  Largest group size: {}", largest.len());
    
    println!("\nGroup details:");
    for (i, group) in groups.iter().enumerate() {
        let members: Vec<_> = group.iter().collect();
        println!("  Group {} ({} members): {:?}", i, members.len(), members);
    }
}

fn image_regions() {
    // Simulating a 4x4 binary image
    // 1 1 0 0
    // 1 0 0 1
    // 0 0 1 1
    // 0 0 1 0
    let image = vec![
        1, 1, 0, 0,
        1, 0, 0, 1,
        0, 0, 1, 1,
        0, 0, 1, 0,
    ];
    
    let width = 4;
    let height = 4;
    let mut ds = DisjointSet::new(width * height);
    
    // Connect adjacent same-colored pixels
    for y in 0..height {
        for x in 0..width {
            let idx = y * width + x;
            
            // Check right neighbor
            if x + 1 < width && image[idx] == image[idx + 1] && image[idx] == 1 {
                ds.union(idx, idx + 1);
            }
            
            // Check bottom neighbor
            if y + 1 < height && image[idx] == image[idx + width] && image[idx] == 1 {
                ds.union(idx, idx + width);
            }
        }
    }
    
    println!("Binary image (1=foreground, 0=background):");
    for y in 0..height {
        let row: Vec<_> = (0..width).map(|x| image[y * width + x]).collect();
        println!("  {:?}", row);
    }
    
    // Count foreground regions
    let sets = ds.all_sets();
    let foreground_regions: Vec<_> = sets.iter()
        .filter(|s| {
            let &first = s.iter().next().unwrap();
            image[first] == 1
        })
        .collect();
    
    println!("\nFound {} foreground regions:", foreground_regions.len());
    for (i, region) in foreground_regions.iter().enumerate() {
        let pixels: Vec<_> = region.iter().collect();
        println!("  Region {} ({} pixels): {:?}", i, pixels.len(), pixels);
    }
}

fn batch_operations() {
    let mut ds = DisjointSet::new(100);
    
    // Batch union pairs
    let pairs: Vec<_> = (0..50).map(|i| (i * 2, i * 2 + 1)).collect();
    let merged = ds.batch_union(pairs);
    
    println!("Batch unioned 50 pairs:");
    println!("  Successful merges: {}", merged);
    println!("  Remaining sets: {}", ds.set_count());
    
    // Try batch union again (should merge 0)
    let pairs2: Vec<_> = (0..25).map(|i| (i * 4, i * 4 + 2)).collect();
    let merged2 = ds.batch_union(pairs2);
    
    println!("\nSecond batch (merging pairs into quads):");
    println!("  Successful merges: {}", merged2);
    println!("  Remaining sets: {}", ds.set_count());
    
    println!("\nLargest set size: {}", ds.largest_set_size());
    println!("Non-trivial sets: {}", ds.non_trivial_set_count());
    
    let isolated = ds.isolated_elements();
    println!("Isolated elements: {:?}", isolated);
}