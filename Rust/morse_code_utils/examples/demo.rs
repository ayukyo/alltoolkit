//! Example: Morse Code Demo
//! 
//! Run with: cargo run --example demo

use morse_code_utils::{MorseCode, to_signals, to_durations, to_binary, from_binary};

fn main() {
    let morse = MorseCode::new();

    println!("=== Morse Code Utils Demo ===\n");

    // Example 1: Basic encoding
    println!("1. Basic Encoding");
    println!("   Input:  \"SOS\"");
    let encoded = morse.encode_default("SOS");
    println!("   Output: \"{}\"\n", encoded);

    // Example 2: Encoding with words
    println!("2. Encoding Words");
    println!("   Input:  \"HELLO WORLD\"");
    let encoded = morse.encode_default("HELLO WORLD");
    println!("   Output: \"{}\"\n", encoded);

    // Example 3: Decoding
    println!("3. Decoding");
    println!("   Input:  \"... --- ...\"");
    let decoded = morse.decode_default("... --- ...");
    println!("   Output: \"{}\"\n", decoded);

    // Example 4: Numbers
    println!("4. Numbers");
    println!("   Input:  \"12345\"");
    let encoded = morse.encode_default("12345");
    println!("   Output: \"{}\"\n", encoded);

    // Example 5: Punctuation
    println!("5. Punctuation");
    println!("   Input:  \"OK, READY!\"");
    let encoded = morse.encode_default("OK, READY!");
    println!("   Output: \"{}\"\n", encoded);

    // Example 6: Audio signals
    println!("6. Audio Signals for \"SOS\"");
    let encoded = morse.encode_default("SOS");
    let signals = to_signals(&encoded);
    println!("   Signals: {:?}", signals);
    let durations = to_durations(&signals);
    println!("   Durations: {:?}\n", durations);

    // Example 7: Binary representation
    println!("7. Binary Representation");
    println!("   Morse: \".-\"");
    let binary = to_binary(".-");
    println!("   Binary: \"{}\"", binary);
    let restored = from_binary(&binary).unwrap();
    println!("   Restored: \"{}\"\n", restored);

    // Example 8: Custom delimiters
    println!("8. Custom Delimiters");
    println!("   Input: \"TEST\"");
    let encoded = morse.encode("TEST", "|", "||");
    println!("   With | and ||: \"{}\"\n", encoded);

    // Example 9: Character lookup
    println!("9. Character Lookup");
    println!("   'A' -> {:?}", morse.get_morse('A'));
    println!("   \".-\" -> {:?}", morse.get_char(".-"));
    println!("   '0' -> {:?}", morse.get_morse('0'));
    println!("   \"-----\" -> {:?}\n", morse.get_char("-----"));

    // Example 10: Validation
    println!("10. Validation");
    println!("    \"... --- ...\" is valid Morse? {}", morse.is_valid_morse("... --- ..."));
    println!("    \"abc\" is valid Morse? {}", morse.is_valid_morse("abc"));
    println!("    Can encode '~'? {}", morse.can_encode('~'));
    println!("    Can encode 'A'? {}", morse.can_encode('A'));
    println!();

    // Example 11: Interactive message
    println!("11. Encoded Message");
    let message = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG";
    let encoded = morse.encode_default(message);
    println!("    Original: \"{}\"", message);
    println!("    Encoded:  \"{}\"", encoded);
    let decoded = morse.decode_default(&encoded);
    println!("    Decoded:  \"{}\"", decoded);
}