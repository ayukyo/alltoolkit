# Emoji Utils

A zero-dependency Rust library for emoji detection and manipulation.

## Features

- **Emoji Detection**: Check if characters or strings contain emojis
- **Counting**: Count individual emojis or emoji sequences
- **Extraction**: Extract emojis from text
- **Removal**: Remove emojis from strings
- **Replacement**: Replace emojis with custom text
- **Name Lookup**: Get human-readable names for common emojis
- **Categorization**: Determine emoji categories (faces, food, nature, etc.)
- **Statistics**: Get comprehensive emoji statistics for text
- **Unicode 15.1 Compatible**: Supports the latest emoji standards
- **Zero Dependencies**: Pure Rust implementation using only the standard library

## Installation

Add this to your `Cargo.toml`:

```toml
[dependencies]
emoji_utils = { path = "../emoji_utils" }
```

## Quick Start

```rust
use emoji_utils::{
    contains_emoji, count_emoji, extract_emoji, remove_emoji, replace_emoji,
    is_emoji, is_only_emoji, get_emoji_name, get_emoji_category, get_emoji_stats,
    EmojiCategory,
};

// Basic detection
assert!(is_emoji('👋'));
assert!(contains_emoji("Hello 👋 World"));
assert!(!is_only_emoji("Hello 👋"));
assert!(is_only_emoji("👋🌍😀"));

// Counting
assert_eq!(count_emoji("Hello 👋 World 🌍"), 2);

// Extraction
let emojis = extract_emoji("Hello 👋 World 🌍!");
assert_eq!(emojis, vec!["👋", "🌍"]);

// Removal
assert_eq!(remove_emoji("Hello 👋 World 🌍!"), "Hello  World !");

// Replacement
assert_eq!(replace_emoji("Hello 👋", "[emoji]"), "Hello [emoji]");

// Name lookup
assert_eq!(get_emoji_name('👋'), Some("waving hand"));
assert_eq!(get_emoji_name('🌍'), Some("globe showing Europe-Africa"));

// Categorization
assert_eq!(get_emoji_category('👋'), EmojiCategory::People);
assert_eq!(get_emoji_category('🍕'), EmojiCategory::Food);

// Statistics
let stats = get_emoji_stats("Hello 👋 World 🌍!");
assert_eq!(stats.count, 2);
assert_eq!(stats.unique_count, 2);
assert!(stats.has_emoji);
```

## API Reference

### Detection Functions

| Function | Description |
|----------|-------------|
| `is_emoji(c: char) -> bool` | Check if a character is an emoji |
| `contains_emoji(s: &str) -> bool` | Check if a string contains any emoji |
| `is_only_emoji(s: &str) -> bool` | Check if a string consists only of emojis |

### Counting Functions

| Function | Description |
|----------|-------------|
| `count_emoji(s: &str) -> usize` | Count individual emoji characters |
| `count_emoji_sequences(s: &str) -> usize` | Count emoji sequences (handles ZWJ) |

### Extraction Functions

| Function | Description |
|----------|-------------|
| `extract_emoji(s: &str) -> Vec<String>` | Extract all emoji characters |
| `extract_emoji_sequences(s: &str) -> Vec<String>` | Extract emoji sequences |

### Removal Functions

| Function | Description |
|----------|-------------|
| `remove_emoji(s: &str) -> String` | Remove all emoji from string |
| `remove_emoji_sequences(s: &str) -> String` | Remove emoji sequences |

### Replacement Functions

| Function | Description |
|----------|-------------|
| `replace_emoji(s: &str, replacement: &str) -> String` | Replace emojis with text |

### Lookup Functions

| Function | Description |
|----------|-------------|
| `get_emoji_name(c: char) -> Option<&'static str>` | Get name for common emojis |
| `get_emoji_category(c: char) -> EmojiCategory` | Get category of an emoji |

### Statistics

| Function | Description |
|----------|-------------|
| `get_emoji_stats(s: &str) -> EmojiStats` | Get comprehensive emoji statistics |

### EmojiCategory Enum

```rust
pub enum EmojiCategory {
    Smileys,    // Faces and emotions
    People,     // People and body parts
    Animals,    // Animals
    Food,       // Food and drink
    Nature,    // Nature and weather
    Objects,    // Objects
    Travel,     // Travel and places
    Activities, // Sports and activities
    Symbols,    // Symbols
    Flags,      // Country flags
    Unknown,    // Unknown category
}
```

### EmojiStats Struct

```rust
pub struct EmojiStats {
    pub count: usize,           // Total emoji count
    pub sequence_count: usize,   // Sequence count (ZWJ aware)
    pub has_emoji: bool,        // Contains any emoji
    pub is_only_emoji: bool,    // Only contains emoji
    pub unique_count: usize,    // Number of unique emojis
}
```

## Supported Emoji Ranges

- Emoticons (U+1F600-U+1F64F)
- Miscellaneous Symbols and Pictographs (U+1F300-U+1F5FF)
- Transport and Map Symbols (U+1F680-U+1F6FF)
- Supplemental Symbols and Pictographs (U+1F900-U+1F9FF)
- Symbols and Pictographs Extended-A (U+1FA00-U+1FA6F)
- Symbols and Pictographs Extended-B (U+1FA70-U+1FAFF)
- Dingbats (U+2700-U+27BF)
- Miscellaneous Symbols (U+2600-U+26FF)
- Regional Indicator Symbols (U+1F1E6-U+1F1FF)
- And more...

## Examples

Run the included examples:

```bash
cargo run --example usage_examples
```

## Testing

Run the test suite:

```bash
cargo test
```

## License

MIT License