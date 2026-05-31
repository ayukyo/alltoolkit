use base32_utils::{decode, encode, encode_nopad};

fn main() {
    // Basic encoding
    let data = b"Hello, World!";
    let encoded = encode(data);
    println!("Encoded '{}' -> '{}'", String::from_utf8_lossy(data), encoded);

    // Encoding without padding
    let encoded_nopad = encode_nopad(data);
    println!("Encoded (no pad) -> '{}'", encoded_nopad);

    // Decoding
    let decoded = decode(&encoded).unwrap();
    println!("Decoded '{}' -> '{}'", encoded, String::from_utf8_lossy(&decoded));

    // RFC 4648 test vectors
    println!("\nRFC 4648 Test Vectors:");
    let test_strings = ["", "f", "fo", "foo", "foob", "fooba", "foobar"];
    for s in &test_strings {
        let encoded = encode(s.as_bytes());
        println!("  '{}' -> '{}'", s, encoded);
    }

    // Valid check
    println!("\nValidation:");
    println!("  'MZXQ====' is valid: {}", base32_utils::is_valid("MZXQ===="));
    println!("  'MZXW6YT!' is valid: {}", base32_utils::is_valid("MZXW6YT!"));
}