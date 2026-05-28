//! Basic usage examples for base64_utils

use base64_utils::{Base64, Base32, Base64Variant};

fn main() {
    println!("=== Base64 Utils - Basic Usage Examples ===\n");

    // ===== Base64 Encoding =====
    println!("--- Base64 Encoding ---");
    
    let data = b"Hello, World!";
    let encoded = Base64::encode(data);
    println!("Original: {:?}", String::from_utf8_lossy(data));
    println!("Base64:   {}", encoded);

    // Without padding (URL-safe)
    let url_encoded = Base64::encode_url_safe(data);
    println!("URL-safe: {}", url_encoded);

    // Using variant enum
    let std_encoded = Base64::encode_with_variant(b"Test", Base64Variant::Standard);
    let url_enc = Base64::encode_with_variant(b"Test", Base64Variant::UrlSafe);
    println!("Standard variant: {}", std_encoded);
    println!("URL variant:      {}", url_enc);

    // ===== Base64 Decoding =====
    println!("\n--- Base64 Decoding ---");
    
    let decoded = Base64::decode("SGVsbG8sIFdvcmxkIQ==").unwrap();
    println!("Decoded: {:?}", String::from_utf8_lossy(&decoded));

    let url_decoded = Base64::decode_url_safe("SGVsbG8sIFdvcmxkIQ").unwrap();
    println!("URL decoded: {:?}", String::from_utf8_lossy(&url_decoded));

    // Auto-detect variant
    let auto_decoded = Base64::decode_auto("SGVsbG8sIFdvcmxkIQ==").unwrap();
    println!("Auto decoded: {:?}", String::from_utf8_lossy(&auto_decoded));

    // ===== Validation =====
    println!("\n--- Validation ---");
    
    println!("'SGVsbG8=' is valid: {}", Base64::is_valid("SGVsbG8="));
    println!("'SGVs!m8=' is valid: {}", Base64::is_valid("SGVs!m8="));

    // Strict validation (requires padding)
    println!("'SGVsbG8' strict: {}", Base64::is_valid_strict("SGVsbG8", true));
    println!("'SGVsbG8=' strict: {}", Base64::is_valid_strict("SGVsbG8=", true));

    // ===== Length Calculations =====
    println!("\n--- Length Calculations ---");
    
    println!("Encoded length for 5 bytes: {}", Base64::encoded_len(5));
    println!("Decoded length for 8 chars: {}", Base64::decoded_len(8));

    // ===== Base32 Encoding =====
    println!("\n--- Base32 Encoding ---");
    
    let b32_encoded = Base32::encode(b"Hello");
    println!("Base32 of 'Hello': {}", b32_encoded);

    let b32_long = Base32::encode(b"Hello, World!");
    println!("Base32 of 'Hello, World!': {}", b32_long);

    // ===== Base32 Decoding =====
    println!("\n--- Base32 Decoding ---");
    
    let b32_decoded = Base32::decode("JBSWY3DP").unwrap();
    println!("Decoded 'JBSWY3DP': {:?}", String::from_utf8_lossy(&b32_decoded));

    // Lowercase is also supported
    let b32_lower = Base32::decode("jbswy3dp").unwrap();
    println!("Decoded 'jbswy3dp': {:?}", String::from_utf8_lossy(&b32_lower));

    // ===== Round-trip Test =====
    println!("\n--- Round-trip Test ---");
    
    let original = b"The quick brown fox jumps over the lazy dog";
    println!("Original: {:?}", String::from_utf8_lossy(original));
    
    let b64_enc = Base64::encode(original);
    println!("Base64:   {}", b64_enc);
    
    let b64_dec = Base64::decode(&b64_enc).unwrap();
    println!("Decoded:  {:?}", String::from_utf8_lossy(&b64_dec));
    println!("Match:    {}", b64_dec == original);

    let b32_enc = Base32::encode(original);
    println!("\nBase32:   {}", b32_enc);
    
    let b32_dec = Base32::decode(&b32_enc).unwrap();
    println!("Decoded:  {:?}", String::from_utf8_lossy(&b32_dec));
    println!("Match:    {}", b32_dec == original);

    // ===== Binary Data =====
    println!("\n--- Binary Data ---");
    
    let binary: Vec<u8> = (0..=255).collect();
    let b64_binary = Base64::encode(&binary);
    println!("Binary data (0-255) encoded to {} characters", b64_binary.len());
    
    let b64_decoded = Base64::decode(&b64_binary).unwrap();
    println!("Round-trip success: {}", binary == b64_decoded);

    // ===== Error Handling =====
    println!("\n--- Error Handling ---");
    
    match Base64::decode("invalid!@#$") {
        Ok(data) => println!("Decoded: {:?}", data),
        Err(e) => println!("Error: {}", e),
    }

    match Base32::decode("12345678") {
        Ok(data) => println!("Decoded: {:?}", data),
        Err(e) => println!("Error: {}", e),
    }
}