//! # Emoji Utilities Usage Examples
//!
//! This example demonstrates various features of the emoji_utils library.

use emoji_utils::{
    contains_emoji, count_emoji, count_emoji_sequences, extract_emoji, extract_emoji_sequences,
    get_emoji_category, get_emoji_name, get_emoji_stats, is_emoji, is_only_emoji, remove_emoji,
    remove_emoji_sequences, replace_emoji,
};

fn main() {
    println!("=== Emoji Utils Examples ===\n");

    // Basic detection
    basic_detection();

    // Counting
    counting_examples();

    // Extraction
    extraction_examples();

    // Removal
    removal_examples();

    // Replacement
    replacement_examples();

    // Name and category lookup
    name_and_category_examples();

    // Statistics
    statistics_examples();

    // Edge cases
    edge_cases();
}

fn basic_detection() {
    println!("--- Basic Detection ---");

    // Check if a character is an emoji
    println!("Is '👋' an emoji? {}", is_emoji('👋'));
    println!("Is 'A' an emoji? {}", is_emoji('A'));
    println!("Is '😀' an emoji? {}", is_emoji('😀'));
    println!("Is '❤' an emoji? {}", is_emoji('❤'));

    // Check if a string contains any emoji
    let text1 = "Hello 👋 World!";
    let text2 = "No emoji here";
    println!("'{}' contains emoji? {}", text1, contains_emoji(text1));
    println!("'{}' contains emoji? {}", text2, contains_emoji(text2));

    // Check if string is ONLY emoji
    let text3 = "👋🌍😀";
    let text4 = "Hello 👋";
    println!("'{}' is only emoji? {}", text3, is_only_emoji(text3));
    println!("'{}' is only emoji? {}", text4, is_only_emoji(text4));

    println!();
}

fn counting_examples() {
    println!("--- Counting Examples ---");

    // Count individual emoji characters
    let text = "Hello 👋 World 🌍! Great day 😊";
    println!("Text: '{}'", text);
    println!("Emoji count: {}", count_emoji(text));

    // Count emoji sequences (complex emojis as single unit)
    let text2 = "😀😃😄";
    println!("\nText: '{}'", text2);
    println!("Individual count: {}", count_emoji(text2));
    println!("Sequence count: {}", count_emoji_sequences(text2));

    println!();
}

fn extraction_examples() {
    println!("--- Extraction Examples ---");

    let text = "I love 🍕 and 🍔!";

    // Extract as individual characters
    let emojis = extract_emoji(text);
    println!("Text: '{}'", text);
    println!("Extracted emojis: {:?}", emojis);

    // Extract as sequences
    let text2 = "Party 🎉🎉🎉 time!";
    let sequences = extract_emoji_sequences(text2);
    println!("\nText: '{}'", text2);
    println!("Extracted sequences: {:?}", sequences);

    // More complex example
    let text3 = "Nature 🌸🌻🍁 Animals 🐶🐱🦋";
    let emojis3 = extract_emoji(text3);
    println!("\nText: '{}'", text3);
    println!("All emojis: {:?}", emojis3);

    println!();
}

fn removal_examples() {
    println!("--- Removal Examples ---");

    let text = "Hello 👋 World 🌍!";
    println!("Original: '{}'", text);
    println!("After removal: '{}'", remove_emoji(text));

    let text2 = "This is a test 😀 with emoji 🎉";
    println!("\nOriginal: '{}'", text2);
    println!("After removal: '{}'", remove_emoji(text2));

    // Removing sequences
    let text3 = "Clean this text 👋🌍😀";
    println!("\nOriginal: '{}'", text3);
    println!("After sequence removal: '{}'", remove_emoji_sequences(text3));

    println!();
}

fn replacement_examples() {
    println!("--- Replacement Examples ---");

    let text = "Hello 👋 World 🌍!";
    println!("Original: '{}'", text);
    println!("Replace with [emoji]: '{}'", replace_emoji(text, "[emoji]"));

    let text2 = "Great day 😊! Love it ❤";
    println!("\nOriginal: '{}'", text2);
    println!("Replace with *: '{}'", replace_emoji(text2, "*"));

    println!();
}

fn name_and_category_examples() {
    println!("--- Name and Category Lookup ---");

    // Get emoji names
    let emojis = ['👋', '🌍', '😀', '❤', '🍕', '🐶', '☀'];
    for emoji in emojis {
        if let Some(name) = get_emoji_name(emoji) {
            println!("{}: {}", emoji, name);
        } else {
            println!("{}: (unknown)", emoji);
        }
    }

    println!();

    // Get emoji categories
    let more_emojis = ['👋', '🌍', '😀', '🍕', '🐶', '⚽', '🎉'];
    for emoji in more_emojis {
        let category = get_emoji_category(emoji);
        println!("{}: {:?}", emoji, category);
    }

    println!();
}

fn statistics_examples() {
    println!("--- Statistics Examples ---");

    let text = "Hello 👋 World 🌍! Have a great day 😊";
    let stats = get_emoji_stats(text);

    println!("Text: '{}'", text);
    println!("  Total emoji count: {}", stats.count);
    println!("  Sequence count: {}", stats.sequence_count);
    println!("  Has emoji: {}", stats.has_emoji);
    println!("  Is only emoji: {}", stats.is_only_emoji);
    println!("  Unique emojis: {}", stats.unique_count);

    let text2 = "🎉🎉🎉 Party!";
    let stats2 = get_emoji_stats(text2);
    println!("\nText: '{}'", text2);
    println!("  Total emoji count: {}", stats2.count);
    println!("  Unique emojis: {}", stats2.unique_count);

    println!();
}

fn edge_cases() {
    println!("--- Edge Cases ---");

    // Empty string
    println!("Empty string:");
    println!("  contains_emoji: {}", contains_emoji(""));
    println!("  count: {}", count_emoji(""));
    println!("  is_only_emoji: {}", is_only_emoji(""));

    // Only whitespace
    println!("\nWhitespace only:");
    println!("  contains_emoji: {}", contains_emoji("   "));
    println!("  is_only_emoji: {}", is_only_emoji("   "));

    // No emoji
    let text = "Just plain text 123!@#";
    println!("\nNo emoji text: '{}'", text);
    println!("  contains_emoji: {}", contains_emoji(text));
    println!("  count: {}", count_emoji(text));
    println!("  extracted: {:?}", extract_emoji(text));

    // Multiple emoji types
    let mixed = "Faces 😀😃😄 Hands 👋✌👏 Hearts ❤💙💚 Food 🍕🍔🍩";
    println!("\nMixed emoji text:");
    let stats = get_emoji_stats(mixed);
    println!("  Total: {}", stats.count);
    println!("  Unique: {}", stats.unique_count);

    println!();
}