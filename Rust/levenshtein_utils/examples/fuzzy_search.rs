//! Fuzzy search example - building a simple fuzzy search engine

use levenshtein_utils::{
    similarity_ratio, jaro_winkler_similarity, find_top_matches,
};

/// A simple document in our search index
struct Document {
    id: usize,
    title: String,
    content: String,
}

impl Document {
    fn new(id: usize, title: &str, content: &str) -> Self {
        Document {
            id,
            title: title.to_string(),
            content: content.to_string(),
        }
    }
}

/// A simple fuzzy search engine
struct FuzzySearchEngine {
    documents: Vec<Document>,
}

impl FuzzySearchEngine {
    fn new() -> Self {
        FuzzySearchEngine {
            documents: Vec::new(),
        }
    }

    fn add_document(&mut self, doc: Document) {
        self.documents.push(doc);
    }

    /// Search for documents by title similarity
    fn search_by_title(&self, query: &str, threshold: f64) -> Vec<(usize, &Document, f64)> {
        let mut results: Vec<(usize, &Document, f64)> = self
            .documents
            .iter()
            .map(|doc| {
                let sim = jaro_winkler_similarity(query, &doc.title);
                (doc.id, doc, sim)
            })
            .filter(|(_, _, sim)| *sim >= threshold)
            .collect();

        results.sort_by(|a, b| b.2.partial_cmp(&a.2).unwrap());
        results
    }

    /// Search for documents containing words similar to query
    fn search_content(&self, query: &str, min_similarity: f64) -> Vec<(usize, &Document, f64)> {
        let query_lower = query.to_lowercase();
        let query_words: Vec<&str> = query_lower.split_whitespace().collect();

        let mut results: Vec<(usize, &Document, f64)> = Vec::new();

        for doc in &self.documents {
            let content_lower = doc.content.to_lowercase();
            let content_words: Vec<&str> = content_lower.split_whitespace().collect();

            let mut max_sim = 0.0;
            for q_word in &query_words {
                for c_word in &content_words {
                    let sim = similarity_ratio(q_word, c_word);
                    if sim > max_sim {
                        max_sim = sim;
                    }
                }
            }

            if max_sim >= min_similarity {
                results.push((doc.id, doc, max_sim));
            }
        }

        results.sort_by(|a, b| b.2.partial_cmp(&a.2).unwrap());
        results
    }
}

fn main() {
    println!("=== Fuzzy Search Engine Demo ===\n");

    let mut engine = FuzzySearchEngine::new();

    // Add some documents
    let docs = vec![
        Document::new(1, "Rust Programming", "Learn Rust programming language from scratch"),
        Document::new(2, "Python Basics", "Introduction to Python for beginners"),
        Document::new(3, "Web Development", "Build modern web applications with HTML CSS JavaScript"),
        Document::new(4, "Data Structures", "Understanding arrays linked lists trees and graphs"),
        Document::new(5, "Algorithms", "Sorting searching and optimization algorithms"),
        Document::new(6, "Machine Learning", "Introduction to neural networks and deep learning"),
        Document::new(7, "Database Design", "SQL and NoSQL database fundamentals"),
        Document::new(8, "API Development", "REST and GraphQL API design patterns"),
    ];

    for doc in docs {
        engine.add_document(doc);
    }

    // Search by title
    println!("--- Searching by Title ---\n");

    let queries = vec!["Rust Programing", "Pyton", "Machne Learn", "Algoritm"];
    
    for query in &queries {
        println!("Query: '{}'", query);
        let results = engine.search_by_title(query, 0.6);
        if results.is_empty() {
            println!("  No results found");
        } else {
            for (id, doc, sim) in results.iter().take(3) {
                println!("  [{:2}] '{}' (similarity: {:.2}%)", id, doc.title, sim * 100.0);
            }
        }
        println!();
    }

    // Search content
    println!("--- Searching by Content ---\n");

    let content_queries = vec!["programing", "databse", "sortin", "neural netwok"];
    
    for query in &content_queries {
        println!("Query: '{}'", query);
        let results = engine.search_content(query, 0.5);
        if results.is_empty() {
            println!("  No results found");
        } else {
            for (id, doc, sim) in results.iter().take(3) {
                println!("  [{:2}] '{}' (similarity: {:.2}%)", id, doc.title, sim * 100.0);
            }
        }
        println!();
    }

    // Command suggestion demo
    println!("--- Command Suggestion ---\n");

    let commands = vec![
        "install", "uninstall", "update", "upgrade", "remove",
        "search", "info", "list", "clean", "autoremove",
        "configure", "build", "test", "run", "deploy",
    ];

    let user_inputs = vec!["instal", "unintsall", "serch", "upgrde", "buidl"];

    for input in &user_inputs {
        let top3 = find_top_matches(input, &commands, 3);
        println!("Input: '{}'", input);
        for (i, result) in top3.iter().enumerate() {
            println!(
                "  {}. {} (distance: {}, similarity: {:.2}%)",
                i + 1,
                result.value,
                result.distance,
                result.similarity * 100.0
            );
        }
        println!();
    }

    // Product search demo
    println!("--- Product Search Demo ---\n");

    let products = vec![
        "Apple iPhone 15 Pro",
        "Apple iPhone 15",
        "Samsung Galaxy S24",
        "Samsung Galaxy Z Fold",
        "Google Pixel 8 Pro",
        "Google Pixel 8",
        "OnePlus 12",
        "Sony Xperia 1 V",
    ];

    let product_queries = vec!["iphone 15pro", "samsung galxy", "pixle pro", "onepls"];

    for query in &product_queries {
        println!("Search: '{}'", query);
        
        // Get top matches for each product
        let mut scored: Vec<(&str, f64)> = products
            .iter()
            .map(|&p| {
                // Compare against product name and its parts
                let name_sim = jaro_winkler_similarity(query, p);
                let parts_sim: f64 = p
                    .split_whitespace()
                    .map(|part| jaro_winkler_similarity(query, part))
                    .fold(0.0, |a, b| a.max(b));
                (p, name_sim.max(parts_sim))
            })
            .filter(|(_, sim)| *sim > 0.4)
            .collect();

        scored.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());

        for (i, (product, sim)) in scored.iter().take(3).enumerate() {
            println!("  {}. {} ({:.1}%)", i + 1, product, sim * 100.0);
        }
        println!();
    }
}