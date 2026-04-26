//! Usage examples for text_distance_utils
//!
//! Demonstrates all distance and similarity algorithms.

use text_distance_utils::*;

fn main() {
    println!("=== Text Distance Utilities Examples ===\n");

    // ========================================
    // Hamming Distance
    // ========================================
    println!("--- Hamming Distance ---");
    println!(
        "hamming_distance(\"karolin\", \"kathrin\") = {:?}",
        hamming_distance("karolin", "kathrin")
    );
    println!(
        "hamming_distance(\"0000\", \"1111\") = {:?}",
        hamming_distance("0000", "1111")
    );
    println!(
        "hamming_distance(\"hello\", \"hello\") = {:?}",
        hamming_distance("hello", "hello")
    );
    println!(
        "hamming_similarity(\"karolin\", \"kathrin\") = {:?}",
        hamming_similarity("karolin", "kathrin")
    );
    println!();

    // ========================================
    // Levenshtein Distance
    // ========================================
    println!("--- Levenshtein Distance ---");
    println!(
        "levenshtein_distance(\"kitten\", \"sitting\") = {}",
        levenshtein_distance("kitten", "sitting")
    );
    println!(
        "levenshtein_distance(\"book\", \"back\") = {}",
        levenshtein_distance("book", "back")
    );
    println!(
        "levenshtein_distance(\"saturday\", \"sunday\") = {}",
        levenshtein_distance("saturday", "sunday")
    );
    println!(
        "levenshtein_similarity(\"kitten\", \"sitting\") = {:.3}",
        levenshtein_similarity("kitten", "sitting")
    );
    println!();

    // ========================================
    // Damerau-Levenshtein Distance
    // ========================================
    println!("--- Damerau-Levenshtein Distance ---");
    println!(
        "damerau_levenshtein_distance(\"ca\", \"ac\") = {}",
        damerau_levenshtein_distance("ca", "ac")
    );
    println!(
        "damerau_levenshtein_distance(\"abcd\", \"acbd\") = {}",
        damerau_levenshtein_distance("abcd", "acbd")
    );
    println!(
        "damerau_levenshtein_similarity(\"abcd\", \"acbd\") = {:.3}",
        damerau_levenshtein_similarity("abcd", "acbd")
    );
    println!();

    // ========================================
    // Jaro Similarity
    // ========================================
    println!("--- Jaro Similarity ---");
    println!(
        "jaro_similarity(\"MARTHA\", \"MARHTA\") = {:.3}",
        jaro_similarity("MARTHA", "MARHTA")
    );
    println!(
        "jaro_similarity(\"DWAYNE\", \"DUANE\") = {:.3}",
        jaro_similarity("DWAYNE", "DUANE")
    );
    println!(
        "jaro_similarity(\"hello\", \"hello\") = {:.3}",
        jaro_similarity("hello", "hello")
    );
    println!();

    // ========================================
    // Jaro-Winkler Similarity
    // ========================================
    println!("--- Jaro-Winkler Similarity ---");
    println!(
        "jaro_winkler_similarity(\"MARTHA\", \"MARHTA\") = {:.3}",
        jaro_winkler_similarity("MARTHA", "MARHTA")
    );
    println!(
        "jaro_winkler_similarity(\"DWAYNE\", \"DUANE\") = {:.3}",
        jaro_winkler_similarity("DWAYNE", "DUANE")
    );
    println!(
        "jaro_winkler_similarity(\"hello\", \"hello\") = {:.3}",
        jaro_winkler_similarity("hello", "hello")
    );
    println!();

    // ========================================
    // N-gram Similarity
    // ========================================
    println!("--- N-gram Similarity ---");
    println!(
        "ngram_similarity(\"hello\", \"hella\", 2) = {:.3}",
        ngram_similarity("hello", "hella", 2)
    );
    println!(
        "ngram_similarity(\"hello\", \"hella\", 3) = {:.3}",
        ngram_similarity("hello", "hella", 3)
    );

    println!("Bigrams of \"hello\": {:?}", generate_ngrams("hello", 2));
    println!("Trigrams of \"hello\": {:?}", generate_ngrams("hello", 3));
    println!();

    // ========================================
    // Dice Coefficient
    // ========================================
    println!("--- Dice Coefficient ---");
    println!(
        "dice_coefficient(\"night\", \"nacht\") = {:.3}",
        dice_coefficient("night", "nacht")
    );
    println!(
        "dice_coefficient(\"hello\", \"hallo\") = {:.3}",
        dice_coefficient("hello", "hallo")
    );
    println!(
        "dice_coefficient(\"hello\", \"hello\") = {:.3}",
        dice_coefficient("hello", "hello")
    );
    println!();

    // ========================================
    // Cosine Similarity
    // ========================================
    println!("--- Cosine Similarity ---");
    println!(
        "cosine_similarity(\"hello world\", \"world hello\") = {:.3}",
        cosine_similarity("hello world", "world hello")
    );
    println!(
        "cosine_similarity(\"the quick brown fox\", \"the quick blue cat\") = {:.3}",
        cosine_similarity("the quick brown fox", "the quick blue cat")
    );
    println!(
        "cosine_similarity(\"hello world\", \"foo bar\") = {:.3}",
        cosine_similarity("hello world", "foo bar")
    );
    println!(
        "cosine_ngram_similarity(\"hello\", \"hella\", 2) = {:.3}",
        cosine_ngram_similarity("hello", "hella", 2)
    );
    println!();

    // ========================================
    // Overlap Coefficient
    // ========================================
    println!("--- Overlap Coefficient ---");
    println!(
        "overlap_coefficient(\"hello world\", \"hello\") = {:.3}",
        overlap_coefficient("hello world", "hello")
    );
    println!(
        "overlap_coefficient(\"hello world test\", \"hello foo\") = {:.3}",
        overlap_coefficient("hello world test", "hello foo")
    );
    println!();

    // ========================================
    // Q-gram Distance
    // ========================================
    println!("--- Q-gram Distance ---");
    println!(
        "qgram_distance(\"hello\", \"hella\", 2) = {}",
        qgram_distance("hello", "hella", 2)
    );
    println!(
        "qgram_distance(\"hello\", \"world\", 2) = {}",
        qgram_distance("hello", "world", 2)
    );
    println!();

    // ========================================
    // Fuzzy Matching
    // ========================================
    println!("--- Fuzzy Matching ---");
    let candidates = vec!["hello", "hallo", "hola", "hi", "help", "held"];
    println!("Candidates: {:?}", candidates);

    let result = best_match("hell", &candidates);
    println!("best_match(\"hell\", candidates) = {:?}", result);

    let result = best_match("helo", &candidates);
    println!("best_match(\"helo\", candidates) = {:?}", result);

    let matches = find_matches("hell", &candidates, 0.5);
    println!("find_matches(\"hell\", candidates, 0.5) = {:?}", matches);
    println!();

    // ========================================
    // Compare Strings (All Metrics)
    // ========================================
    println!("--- Compare Strings (All Metrics) ---");
    let metrics = compare_strings("kitten", "sitting");
    println!("Comparing \"kitten\" vs \"sitting\":");
    for (name, value) in &metrics {
        println!("  {}: {:.3}", name, value);
    }
    println!();

    // ========================================
    // Practical Use Cases
    // ========================================
    println!("--- Practical Use Cases ---");

    // 1. Spell checking
    println!("1. Spell Checking:");
    let dictionary = vec![
        "apple", "banana", "cherry", "date", "elderberry", "fig", "grape",
    ];
    let typo = "aple";
    let result = best_match(typo, &dictionary);
    println!(
        "  User typed \"{}\", best match: {:?}",
        typo,
        result.map(|(i, s)| (dictionary[i], s))
    );

    // 2. Name matching
    println!("2. Name Matching:");
    let names = vec!["John Smith", "John Smyth", "Jon Smith", "Jane Smith"];
    let search = "John Smith";
    let matches = find_matches(search, &names, 0.85);
    println!("  Searching for \"{}\":", search);
    for (idx, score) in matches {
        println!("    {} (similarity: {:.3})", names[idx], score);
    }

    // 3. Duplicate detection
    println!("3. Duplicate Detection:");
    let records = vec![
        "The Quick Brown Fox",
        "the quick brown fox",
        "The Quick Brown Fox.",
        "Quick Brown Fox",
    ];
    println!("  Records: {:?}", records);
    println!("  Comparing first two records:");
    let sim = cosine_similarity(records[0], records[1]);
    println!("    Cosine similarity: {:.3} (case insensitive, identical)", sim);

    // 4. DNA sequence comparison
    println!("4. DNA Sequence Comparison:");
    let seq1 = "ACGTACGT";
    let seq2 = "ACGTACGA";
    println!("  Sequence 1: {}", seq1);
    println!("  Sequence 2: {}", seq2);
    println!(
        "  Hamming distance: {:?}",
        hamming_distance(seq1, seq2)
    );
    println!(
        "  Levenshtein distance: {}",
        levenshtein_distance(seq1, seq2)
    );

    // 5. Unicode support
    println!("5. Unicode Support:");
    println!(
        "  levenshtein_distance(\"你好世界\", \"你好世异\") = {}",
        levenshtein_distance("你好世界", "你好世异")
    );
    println!(
        "  jaro_similarity(\"日本語\", \"日本国\") = {:.3}",
        jaro_similarity("日本語", "日本国")
    );

    println!("\n=== All examples completed successfully ===");
}