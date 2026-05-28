# Vigenère Cipher Utils

A comprehensive Rust implementation of the Vigenère cipher, a classic polyalphabetic substitution cipher.

## Features

- **Core Operations**: Encrypt and decrypt text using the Vigenère cipher
- **Custom Alphabets**: Support for custom character sets beyond A-Z
- **Autokey Mode**: Implements the autokey variant for enhanced security
- **Cryptanalysis Tools**: Key length estimation via Kasiski examination
- **Index of Coincidence**: Statistical analysis for cipher strength
- **Zero Dependencies**: Pure Rust implementation with no external crates

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
vigenere_cipher_utils = "1.0.0"
```

## Quick Start

```rust
use vigenere_cipher_utils::{encrypt, decrypt};

// Basic usage
let plaintext = "HELLO WORLD";
let key = "SECRET";

let ciphertext = encrypt(plaintext, key).unwrap();
println!("Encrypted: {}", ciphertext);

let decrypted = decrypt(&ciphertext, key).unwrap();
println!("Decrypted: {}", decrypted);
```

## Usage Examples

### Using VigenereCipher Instance

```rust
use vigenere_cipher_utils::VigenereCipher;

let cipher = VigenereCipher::new().unwrap();

let ciphertext = cipher.encrypt("ATTACK AT DAWN", "LEMON").unwrap();
let decrypted = cipher.decrypt(&ciphertext, "LEMON").unwrap();
```

### Custom Configuration

```rust
use vigenere_cipher_utils::{VigenereCipher, VigenereConfig};

let config = VigenereConfig {
    preserve_non_alpha: true,   // Keep spaces and punctuation
    uppercase_output: false,    // Output lowercase
    autokey: false,
    alphabet: String::from("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
};

let cipher = VigenereCipher::with_config(config).unwrap();
```

### Autokey Mode

The autokey cipher uses the plaintext itself as part of the key, providing better security:

```rust
use vigenere_cipher_utils::{encrypt_with_config, VigenereConfig};

let config = VigenereConfig {
    autokey: true,
    ..Default::default()
};

let ciphertext = encrypt_with_config("ATTACKATDAWN", "QUEENLY", &config).unwrap();
```

### Custom Alphabet

```rust
use vigenere_cipher_utils::VigenereCipher;

// Support numbers in encryption
let cipher = VigenereCipher::with_alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789").unwrap();

let encrypted = cipher.encrypt("SECRET2024", "KEY").unwrap();
```

### Cryptanalysis

```rust
use vigenere_cipher_utils::VigenereCipher;

let cipher = VigenereCipher::new().unwrap();

// Estimate key length using Kasiski examination
let ciphertext = "YOUR_ENCRYPTED_TEXT_HERE";
let estimated_lengths = cipher.estimate_key_length(ciphertext, 10);

// Calculate Index of Coincidence
let ic = cipher.index_of_coincidence(ciphertext);
println!("IC: {:.4}", ic);
```

## How It Works

The Vigenère cipher uses a keyword to determine the shift for each letter:

1. Each letter in the key determines a shift value (A=0, B=1, ..., Z=25)
2. The key repeats to match the length of the plaintext
3. Each plaintext letter is shifted by its corresponding key letter

Example with key "KEY":
```
Plaintext:  H E L L O W O R L D
Key:        K E Y K E Y K E Y K
Shift:      10 4 24 10 4 24 10 4 24 10
Ciphertext: R I J V S K Y V R N
```

## API Reference

### Functions

- `encrypt(plaintext, key)` - Encrypt text with default settings
- `decrypt(ciphertext, key)` - Decrypt text with default settings
- `encrypt_with_config(plaintext, key, config)` - Encrypt with custom configuration
- `decrypt_with_config(ciphertext, key, config)` - Decrypt with custom configuration

### VigenereCipher

- `new()` - Create cipher with default configuration
- `with_alphabet(alphabet)` - Create cipher with custom alphabet
- `with_config(config)` - Create cipher with custom configuration
- `encrypt(plaintext, key)` - Encrypt text
- `decrypt(ciphertext, key)` - Decrypt text
- `estimate_key_length(ciphertext, max_length)` - Estimate key length
- `index_of_coincidence(text)` - Calculate IC

### VigenereConfig

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `alphabet` | `String` | A-Z | Character set for encryption |
| `preserve_non_alpha` | `bool` | `true` | Keep non-alphabet characters |
| `uppercase_output` | `bool` | `true` | Output in uppercase |
| `autokey` | `bool` | `false` | Use autokey variant |

## Security Note

The Vigenère cipher is a classical cipher and should **not** be used for real security purposes. It can be broken relatively easily using modern cryptanalysis techniques. This library is intended for educational purposes, puzzles, and historical interest only.

## Running Examples

```bash
cargo run --example basic
```

## Running Tests

```bash
cargo test
```

## License

MIT License