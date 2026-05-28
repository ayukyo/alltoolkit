//! Basic usage examples for Vigenère Cipher Utils

use vigenere_cipher_utils::{encrypt, decrypt, encrypt_with_config, decrypt_with_config, VigenereCipher, VigenereConfig};

fn main() {
    println!("=== Vigenère Cipher Utils Examples ===\n");
    
    // Example 1: Basic encryption and decryption
    println!("1. Basic Encryption/Decryption:");
    let plaintext = "HELLO WORLD";
    let key = "SECRET";
    
    let ciphertext = encrypt(plaintext, key).unwrap();
    println!("   Plaintext:  {}", plaintext);
    println!("   Key:        {}", key);
    println!("   Ciphertext: {}", ciphertext);
    
    let decrypted = decrypt(&ciphertext, key).unwrap();
    println!("   Decrypted:  {}", decrypted);
    println!();
    
    // Example 2: Preserving non-alphabetic characters
    println!("2. Preserving Non-Alphabetic Characters:");
    let text = "Attack at dawn! Use coordinates: 41.4025° N";
    let key = "LEMON";
    
    let config = VigenereConfig {
        preserve_non_alpha: true,
        ..Default::default()
    };
    
    let encrypted = encrypt_with_config(text, key, &config).unwrap();
    println!("   Original:   {}", text);
    println!("   Encrypted:  {}", encrypted);
    
    let decrypted = decrypt_with_config(&encrypted, key, &config).unwrap();
    println!("   Decrypted:  {}", decrypted);
    println!();
    
    // Example 3: Using the cipher instance
    println!("3. Using VigenereCipher Instance:");
    let cipher = VigenereCipher::new().unwrap();
    
    let messages = vec![
        ("MEET ME AT THE BRIDGE", "SPY"),
        ("THE PACKAGE ARRIVES TOMORROW", "AGENT"),
        ("CODE RED ABORT MISSION", "ALPHA"),
    ];
    
    for (msg, key) in messages {
        let enc = cipher.encrypt(msg, key).unwrap();
        let dec = cipher.decrypt(&enc, key).unwrap();
        println!("   '{}' -> '{}' (key: {})", msg, enc, key);
        assert_eq!(dec, msg);
    }
    println!();
    
    // Example 4: Autokey mode
    println!("4. Autokey Mode:");
    let autokey_config = VigenereConfig {
        autokey: true,
        ..Default::default()
    };
    
    let plaintext = "ATTACKATDAWN";
    let key = "QUEENLY";
    
    let encrypted = encrypt_with_config(plaintext, key, &autokey_config).unwrap();
    println!("   Plaintext:  {}", plaintext);
    println!("   Key:        {} (autokey)", key);
    println!("   Ciphertext: {}", encrypted);
    
    let decrypted = decrypt_with_config(&encrypted, key, &autokey_config).unwrap();
    println!("   Decrypted:  {}", decrypted);
    println!();
    
    // Example 5: Key length estimation (cryptanalysis)
    println!("5. Key Length Estimation (Kasiski Examination):");
    let cipher = VigenereCipher::new().unwrap();
    
    let long_text = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOGXTHEQUICKBROWNFOXJUMPSOVERTHELAZYDOGX";
    let key = "ABC";
    let encrypted = cipher.encrypt(long_text, key).unwrap();
    
    let estimated_lengths = cipher.estimate_key_length(&encrypted, 10);
    println!("   Original key length: {}", key.len());
    println!("   Estimated lengths: {:?}", estimated_lengths);
    println!();
    
    // Example 6: Index of Coincidence
    println!("6. Index of Coincidence:");
    let english_text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG";
    let ic = cipher.index_of_coincidence(english_text);
    println!("   IC for English text: {:.4}", ic);
    println!("   (English typically has IC around 0.067)");
    println!();
    
    // Example 7: Custom alphabet (alphanumeric)
    println!("7. Custom Alphabet (Alphanumeric):");
    let alphanumeric_cipher = VigenereCipher::with_alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789").unwrap();
    
    let message = "SECRET2024";
    let key = "KEY";
    
    let encrypted = alphanumeric_cipher.encrypt(message, key).unwrap();
    println!("   Message:    {}", message);
    println!("   Key:        {}", key);
    println!("   Encrypted:  {}", encrypted);
    
    let decrypted = alphanumeric_cipher.decrypt(&encrypted, key).unwrap();
    println!("   Decrypted:  {}", decrypted);
    println!();
    
    // Example 8: Lowercase output
    println!("8. Lowercase Output:");
    let lowercase_config = VigenereConfig {
        uppercase_output: false,
        ..Default::default()
    };
    
    let encrypted = encrypt_with_config("HELLO", "KEY", &lowercase_config).unwrap();
    println!("   'HELLO' + 'KEY' -> '{}' (lowercase)", encrypted);
    println!();
    
    println!("=== All examples completed successfully! ===");
}