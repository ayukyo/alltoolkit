//! Autocomplete system example using Trie

use trie_utils::Trie;

fn main() {
    println!("=== Autocomplete System Example ===\n");
    
    // Create a dictionary with words and their frequencies
    let mut dictionary: Trie<char, u32> = Trie::new();
    
    println!("Building dictionary with word frequencies...\n");
    
    // Common English words with frequency scores
    let words = [
        ("the", 1000),
        ("they", 500),
        ("there", 450),
        ("their", 400),
        ("then", 350),
        ("than", 300),
        ("that", 800),
        ("this", 600),
        ("these", 250),
        ("those", 200),
        ("think", 300),
        ("thing", 280),
        ("things", 150),
        ("thought", 180),
        ("through", 220),
        ("apple", 400),
        ("application", 200),
        ("apply", 300),
        ("approach", 180),
        ("appreciate", 150),
        ("approximate", 100),
        ("computer", 500),
        ("computing", 350),
        ("compute", 280),
        ("compatible", 150),
        ("compete", 200),
        ("competition", 180),
        ("program", 600),
        ("programming", 450),
        ("programmer", 380),
        ("progress", 250),
        ("project", 400),
        ("product", 350),
        ("provide", 300),
        ("hello", 1000),
        ("help", 800),
        ("helper", 200),
        ("helpful", 250),
        ("health", 300),
        ("healthy", 280),
        ("heart", 350),
        ("hear", 400),
        ("heard", 320),
    ];
    
    for (word, freq) in words {
        dictionary.insert_str(word, freq);
    }
    
    println!("Dictionary size: {} words\n", dictionary.len());
    
    // Simulate user typing
    println!("=== Simulating User Input ===\n");
    
    // Type "th"
    println!("User typed: 'th'");
    let suggestions = get_suggestions(&dictionary, "th", 5);
    println!("Suggestions:");
    for (word, freq) in suggestions {
        println!("  {} (frequency: {})", word, freq);
    }
    println!();
    
    // Type "the"
    println!("User typed: 'the'");
    let suggestions = get_suggestions(&dictionary, "the", 5);
    println!("Suggestions:");
    for (word, freq) in suggestions {
        println!("  {} (frequency: {})", word, freq);
    }
    println!();
    
    // Type "pro"
    println!("User typed: 'pro'");
    let suggestions = get_suggestions(&dictionary, "pro", 5);
    println!("Suggestions:");
    for (word, freq) in suggestions {
        println!("  {} (frequency: {})", word, freq);
    }
    println!();
    
    // Type "app"
    println!("User typed: 'app'");
    let suggestions = get_suggestions(&dictionary, "app", 5);
    println!("Suggestions:");
    for (word, freq) in suggestions {
        println!("  {} (frequency: {})", word, freq);
    }
    println!();
    
    // Spell check example
    println!("=== Spell Check Demo ===\n");
    
    let mut spell_checker: Trie<char, ()> = Trie::string_set();
    let dictionary_words = [
        "hello", "world", "rust", "programming", "computer",
        "algorithm", "data", "structure", "trie", "search",
        "insert", "delete", "find", "word", "spell",
        "check", "correct", "error", "typo", "dictionary",
    ];
    
    for word in dictionary_words {
        spell_checker.insert_word(word);
    }
    
    let test_words = ["hello", "wrld", "programing", "trie", "searche", "computer"];
    
    println!("Checking words against dictionary:");
    for word in test_words {
        let exists = spell_checker.contains_word(word);
        let status = if exists { "✓ correct" } else { "✗ misspelled" };
        println!("  '{}' -> {}", word, status);
        
        if !exists {
            // Find similar words using pattern
            let pattern = format!("?{}?", &word[1..word.len().saturating_sub(1)]);
            let similar = dictionary.search_pattern(&pattern);
            if !similar.is_empty() {
                println!("    Did you mean: {}?", 
                    similar.iter()
                        .take(3)
                        .map(|(w, _)| w.as_str())
                        .collect::<Vec<_>>()
                        .join(", "));
            }
        }
    }
    println!();
    
    // URL routing example
    println!("=== URL Routing Demo ===\n");
    
    let mut routes: Trie<char, &str> = Trie::new();
    
    routes.insert_str("/api/users", "UserController::index");
    routes.insert_str("/api/users/", "UserController::show");
    routes.insert_str("/api/posts", "PostController::index");
    routes.insert_str("/api/posts/", "PostController::show");
    routes.insert_str("/api/posts/comments", "CommentController::index");
    routes.insert_str("/static", "StaticController::serve");
    
    let test_urls = [
        "/api/users",
        "/api/users/123",
        "/api/posts",
        "/api/posts/456",
        "/api/posts/comments",
        "/static/css/style.css",
        "/unknown",
    ];
    
    println!("URL to route matching:");
    for url in test_urls {
        match routes.longest_prefix_str(url) {
            Some((prefix, handler)) => {
                println!("  '{}' -> {} (matched: '{}')", url, handler, prefix);
            }
            None => {
                println!("  '{}' -> 404 Not Found", url);
            }
        }
    }
    
    println!("\n=== Autocomplete Example Complete ===");
}

/// Get suggestions sorted by frequency (descending)
fn get_suggestions(trie: &Trie<char, u32>, prefix: &str, limit: usize) -> Vec<(String, u32)> {
    let mut suggestions: Vec<(String, u32)> = trie.get_by_prefix_str(prefix)
        .into_iter()
        .map(|(word, &freq)| (word, freq))
        .collect();
    
    // Sort by frequency (descending)
    suggestions.sort_by(|a, b| b.1.cmp(&a.1));
    
    // Limit results
    suggestions.truncate(limit);
    suggestions
}