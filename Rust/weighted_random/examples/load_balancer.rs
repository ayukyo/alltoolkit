//! Load balancer example using weighted_random
//!
//! Run with: cargo run --example load_balancer

use weighted_random::{Selector, WeightedItem};

/// Represents a backend server
#[derive(Debug, Clone)]
struct Backend {
    name: String,
    address: String,
    capacity: usize,
    current_load: usize,
}

impl Backend {
    fn new(name: &str, address: &str, capacity: usize) -> Self {
        Self {
            name: name.to_string(),
            address: address.to_string(),
            capacity,
            current_load: 0,
        }
    }

    fn weight(&self) -> f64 {
        (self.capacity - self.current_load) as f64
    }

    fn handle_request(&mut self) {
        self.current_load += 1;
    }

    fn is_overloaded(&self) -> bool {
        self.current_load >= self.capacity
    }
}

fn main() {
    println!("=== Weighted Round-Robin Load Balancer ===\n");

    // Create backend servers with different capacities
    let backends = vec![
        Backend::new("server-1", "10.0.0.1:8080", 100),
        Backend::new("server-2", "10.0.0.2:8080", 50),
        Backend::new("server-3", "10.0.0.3:8080", 30),
    ];

    println!("Backend servers:");
    for backend in &backends {
        println!("  {} ({}) - capacity: {} req/s", 
                 backend.name, backend.address, backend.capacity);
    }

    // Create weighted selector based on capacity
    let items: Vec<WeightedItem<Backend>> = backends
        .into_iter()
        .map(|b| WeightedItem::new(b, b.capacity as f64))
        .collect();

    let selector = Selector::new(items).unwrap();

    println!("\nDistributing 100 requests...");

    // Track request distribution
    let mut distribution: std::collections::HashMap<String, usize> = std::collections::HashMap::new();

    // Distribute requests
    for i in 1..=100 {
        let backend = selector.select();

        if i <= 10 {
            println!("  Request {} -> {} ({})", i, backend.name, backend.address);
        }

        *distribution.entry(backend.name.clone()).or_insert(0) += 1;
    }

    println!("\nRequest distribution:");
    for (name, count) in &distribution {
        let backend = selector.items().iter().find(|b| &b.name == name).unwrap();
        let percentage = *count as f64 / 100.0 * 100.0;
        let expected = backend.capacity as f64 / 180.0 * 100.0;
        println!("  {}: {} requests ({:.1}% vs expected {:.1}%)", 
                 name, count, percentage, expected);
    }

    println!("\n=== Dynamic Weight Adjustment ===\n");
    dynamic_load_balancing();
}

fn dynamic_load_balancing() {
    let mut backends = vec![
        Backend::new("server-1", "10.0.0.1:8080", 50),
        Backend::new("server-2", "10.0.0.2:8080", 30),
        Backend::new("server-3", "10.0.0.3:8080", 20),
    ];

    println!("Simulating 50 requests with dynamic weight adjustment...\n");

    for i in 1..=50 {
        // Recalculate weights based on current load
        let available: Vec<WeightedItem<Backend>> = backends
            .iter()
            .filter(|b| !b.is_overloaded())
            .map(|b| WeightedItem::new(b.clone(), b.weight()))
            .collect();

        if available.is_empty() {
            println!("  Request {}: All servers overloaded!", i);
            continue;
        }

        let selector = Selector::new(available).unwrap();
        let selected_name = selector.select().name.clone();

        for backend in &mut backends {
            if backend.name == selected_name {
                backend.handle_request();
                break;
            }
        }

        if i % 10 == 0 {
            println!("  After {} requests:", i);
            for backend in &backends {
                let utilization = backend.current_load as f64 / backend.capacity as f64 * 100.0;
                println!("    {}: {} / {} ({:.0}%) - weight: {:.0}", 
                         backend.name, backend.current_load, backend.capacity, 
                         utilization, backend.weight());
            }
            println!();
        }
    }

    println!("Final state:");
    for backend in &backends {
        println!("  {}: {} requests handled (capacity: {})", 
                 backend.name, backend.current_load, backend.capacity);
    }
}