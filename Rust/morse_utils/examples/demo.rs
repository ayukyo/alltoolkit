//! Example usage of morse_utils

use morse_utils::{encode, decode, MorseEncoder, MorseConfig};

fn main() {
    println!("=== Morse Code Utils Demo ===\n");

    // Basic encoding
    println!("1. Basic Encoding:");
    let text = "HELLO WORLD";
    let encoded = encode(text).unwrap();
    println!("   Text:   \"{}\"", text);
    println!("   Morse:  \"{}\"", encoded);

    // Basic decoding
    println!("\n2. Basic Decoding:");
    let morse = "... --- ...";
    let decoded = decode(morse).unwrap();
    println!("   Morse:  \"{}\"", morse);
    println!("   Text:   \"{}\"", decoded);

    // SOS distress signal
    println!("\n3. SOS Distress Signal:");
    let sos = encode("SOS").unwrap();
    println!("   SOS encoded: \"{}\"", sos);
    println!("   Pattern: dot-dot-dot dash-dash-dash dot-dot-dot");

    // Numbers and punctuation
    println!("\n4. Numbers and Punctuation:");
    println!("   \"123\" -> \"{}\"", encode("123").unwrap());
    println!("   \"Hello!\" -> \"{}\"", encode("Hello!").unwrap());
    println!("   \"What?\" -> \"{}\"", encode("What?").unwrap());

    // Custom timing configuration
    println!("\n5. Custom Timing Configuration:");
    let config = MorseConfig::new(100); // 100ms dot duration
    let encoder = MorseEncoder::with_config(config);
    println!("   Dot duration:   {}ms", encoder.config().dot_duration_ms);
    println!("   Dash duration:  {}ms", encoder.config().dash_duration_ms);
    println!("   Char gap:       {}ms", encoder.config().char_gap_ms);
    println!("   Word gap:       {}ms", encoder.config().word_gap_ms);

    // Roundtrip encoding-decoding
    println!("\n6. Roundtrip Test:");
    let original = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG";
    let encoded = encode(original).unwrap();
    let decoded = decode(&encoded).unwrap();
    println!("   Original: \"{}\"", original);
    println!("   Decoded:  \"{}\"", decoded);
    println!("   Match:    {}", original == decoded);

    // Audio generation sample count
    println!("\n7. Audio Generation:");
    let encoder = MorseEncoder::new();
    let samples = encoder.generate_audio("SOS", 8000, 600.0).unwrap();
    println!("   Generated {} audio samples for \"SOS\" at 8000Hz", samples.len());
    let duration_ms = samples.len() as f32 / 8.0;
    println!("   Duration: {:.1}ms", duration_ms);

    // Character-by-character encoding
    println!("\n8. Character-by-Character Encoding:");
    let encoder = MorseEncoder::new();
    for c in "ABC".chars() {
        if let Some(morse) = encoder.encode_char(c) {
            println!("   '{}' -> \"{}\"", c, morse);
        }
    }

    println!("\n=== Demo Complete ===");
}