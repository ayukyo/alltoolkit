//! Basic usage examples for levenshtein_utils

use levenshtein_utils::{
    levenshtein_distance, similarity_ratio, find_closest, find_matches,
    jaro_winkler_similarity, edit_operations, EditOp, lcs_string,
};

fn main() {
    println!("=== Levenshtein Distance Examples ===\n");

    // Basic distance calculation
    let pairs = [
        ("kitten", "sitting"),
        ("book", "back"),
        ("saturday", "sunday"),
        ("algorithm", "altruistic"),
        ("hello", "hallo"),
    ];

    for (a, b) in &pairs {
        let dist = levenshtein_distance(a, b);
        let ratio = similarity_ratio(a, b);
        println!("'{}' -> '{}': distance={}, similarity={:.2}%", a, b, dist, ratio * 100.0);
    }

    println!("\n=== Fuzzy Search Examples ===\n");

    // Finding closest match
    let dictionary = vec![
        "apple", "banana", "cherry", "date", "elderberry",
        "fig", "grape", "honeydew", "kiwi", "lemon",
    ];

    let queries = vec!["aple", "bannana", "ceri", "leman"];
    for query in &queries {
        if let Some(closest) = find_closest(query, &dictionary) {
            let dist = levenshtein_distance(query, closest);
            println!("Query '{}' -> closest '{}' (distance={})", query, closest, dist);
        }
    }

    println!("\n=== Finding Matches Within Threshold ===\n");

    let words = vec!["hello", "hallo", "hola", "help", "held", "helm"];
    let query = "hello";

    for threshold in 0..=2 {
        let matches = find_matches(query, &words, threshold);
        println!("Matches within {} edits of '{}': {:?}", threshold, query, matches);
    }

    println!("\n=== Jaro-Winkler Similarity ===\n");

    let names = vec![
        ("Martha", "Marhta"),
        ("Jonathan", "Jonathon"),
        ("Michelle", "Michael"),
        ("Jenny", "Jenni"),
    ];

    for (a, b) in &names {
        let jw = jaro_winkler_similarity(a, b);
        println!("JW('{}', '{}') = {:.4}", a, b, jw);
    }

    println!("\n=== Edit Operations ===\n");

    let (from, to) = ("kitten", "sitting");
    println!("Transforming '{}' into '{}':", from, to);
    
    let ops = edit_operations(from, to);
    for op in &ops {
        match op {
            EditOp::Match(i, c) => println!("  [{}] '{}' - match", i, c),
            EditOp::Insert(i, c) => println!("  [{}] insert '{}'", i, c),
            EditOp::Delete(i, c) => println!("  [{}] delete '{}'", i, c),
            EditOp::Substitute(i, old, new) => {
                println!("  [{}] substitute '{}' -> '{}'", i, old, new);
            }
            EditOp::Transpose(i, j) => println!("  transpose [{}] <-> [{}]", i, j),
        }
    }

    println!("\n=== Longest Common Subsequence ===\n");

    let pairs = [
        ("ABCBDAB", "BDCABA"),
        ("PROGRAM", "GROOM"),
        ("kitten", "sitting"),
    ];

    for (a, b) in &pairs {
        let lcs = lcs_string(a, b);
        println!("LCS('{}', '{}') = '{}' (length={})", a, b, lcs, lcs.len());
    }

    println!("\n=== Autocomplete Suggestion ===\n");

    let commands = vec![
        "git add", "git commit", "git push", "git pull",
        "git status", "git branch", "git checkout", "git merge",
    ];

    let user_input = "git comit";
    if let Some(suggestion) = find_closest(user_input, &commands) {
        println!("Did you mean '{}'?", suggestion);
    }

    println!("\n=== Spell Check Example ===\n");

    let word_list = vec![
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
        "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
        "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
        "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
    ];

    let misspelled = vec!["thier", "recieve", "woudl", "thsi", "hte"];

    for word in &misspelled {
        let suggestions = find_matches(word, &word_list, 3);
        if suggestions.is_empty() {
            println!("'{}': no suggestions found", word);
        } else {
            println!("'{}': suggestions: {:?}", word, suggestions);
        }
    }
}