# Rotation Cipher Utilities

A comprehensive rotation cipher utility module for Go with **zero external dependencies**.

## Features

- **Caesar Cipher**: Arbitrary shift rotation cipher
- **ROT13**: Rotate letters by 13 (self-inverse)
- **ROT5**: Rotate digits by 5 (self-inverse)
- **ROT18**: Combination of ROT13 + ROT5 (self-inverse)
- **ROT47**: Rotate ASCII printable characters by 47 (self-inverse)
- **Atbash Cipher**: A↔Z, B↔Y substitution (self-inverse)
- **Vigenère Cipher**: Polyalphabetic substitution with keyword
- **Affine Cipher**: E(x) = (ax + b) mod 26
- **Brute Force Attack**: Automatic Caesar cipher breaking
- **Frequency Analysis**: Letter frequency analysis for cryptanalysis
- **Shift Detection**: Automatic detection of Caesar cipher shift

## Installation

```go
import "github.com/ayukyo/alltoolkit/Go/rotation_cipher_utils"
```

## Usage

### Basic Caesar Cipher

```go
package main

import (
    "fmt"
    rc "github.com/ayukyo/alltoolkit/Go/rotation_cipher_utils"
)

func main() {
    // Encrypt with shift 3
    encrypted := rc.CaesarCipher("HELLO", 3)
    fmt.Println(encrypted) // Output: KHOOR
    
    // Decrypt with negative shift
    decrypted := rc.CaesarCipher("KHOOR", -3)
    fmt.Println(decrypted) // Output: HELLO
}
```

### ROT13 (Self-Inverse)

```go
// ROT13 is its own inverse - applying twice returns original
text := "Hello, World!"
encoded := rc.ROT13(text)  // Output: Uryyb, Jbeyq!
decoded := rc.ROT13(encoded) // Output: Hello, World!
fmt.Println(encoded, decoded)
```

### ROT47 (Full ASCII Rotation)

```go
// ROT47 works on all ASCII printable characters
text := "Hello123!"
encoded := rc.ROT47(text)
decoded := rc.ROT47(encoded) // Self-inverse
fmt.Println(encoded) // Output: w6==@`abcE
```

### Vigenère Cipher

```go
// Polyalphabetic cipher with keyword
plaintext := "HELLO"
key := "KEY"

encrypted := rc.VigenereCipher(plaintext, key, false) // Encrypt
decrypted := rc.VigenereCipher(encrypted, key, true)  // Decrypt
fmt.Println(encrypted, decrypted) // Output: RIJVS HELLO
```

### Brute Force Attack

```go
// Automatically break Caesar cipher
ciphertext := "KHOOR ZRUOG"
results := rc.BruteForceCaesar(ciphertext, 5)

for _, r := range results {
    fmt.Printf("Shift %d: %s (score: %.2f)\n", 
               r.Shift, r.Decrypted, r.Score)
}
// Top result: Shift 3: HELLO WORLD
```

### Frequency Analysis

```go
// Analyze letter frequencies
text := "THE QUICK BROWN FOX"
freq := rc.FrequencyAnalysis(text)

for letter, percentage := range freq {
    fmt.Printf("%c: %.2f%%\n", letter, percentage)
}
```

### All ROT Methods

```go
// Apply all ROT ciphers at once
results := rc.ROTAll("Test123")
fmt.Println(results["rot5"])   // Test678
fmt.Println(results["rot13"])  // Grfg123
fmt.Println(results["rot18"])  // Grfg678
fmt.Println(results["rot47"])  // w6HHD`abc
fmt.Println(results["atbash"]) // Gvhg123
```

## API Reference

### Core Functions

| Function | Description |
|----------|-------------|
| `CaesarCipher(text, shift)` | Apply Caesar cipher with arbitrary shift |
| `ROT13(text)` | Apply ROT13 (rotate by 13) |
| `ROT5(text)` | Apply ROT5 (rotate digits by 5) |
| `ROT18(text)` | Apply ROT18 (ROT13 + ROT5) |
| `ROT47(text)` | Apply ROT47 (ASCII printable rotation) |
| `AtbashCipher(text)` | Apply Atbash cipher (A↔Z, B↔Y) |
| `VigenereCipher(text, key, decrypt)` | Apply Vigenère cipher |
| `AffineCipher(text, a, b, decrypt)` | Apply Affine cipher |

### Analysis Functions

| Function | Description |
|----------|-------------|
| `BruteForceCaesar(text, topN)` | Brute force attack returning top results |
| `FrequencyAnalysis(text)` | Return letter frequency percentages |
| `DetectCaesarShift(text)` | Auto-detect Caesar cipher shift |
| `IsROT13Encoded(text, threshold)` | Heuristic check for ROT13 encoding |

### Utility Functions

| Function | Description |
|----------|-------------|
| `CaesarEncrypt(text, shift)` | Encrypt with CipherResult object |
| `CaesarDecrypt(text, shift)` | Decrypt with CipherResult object |
| `MultiROT(text, rotations)` | Apply multiple rotations sequentially |
| `ROTAll(text)` | Apply all ROT methods, return map |
| `ShiftToROTName(shift)` | Convert shift to ROT naming convention |
| `CaesarCipherWithAlphabet(text, alphabet, shift)` | Custom alphabet rotation |

## Test Results

Run tests with:
```bash
go test -v ./rotation_cipher_utils
```

All tests pass with comprehensive coverage for:
- Basic cipher operations
- Self-inverse properties
- Edge cases (empty input, large shifts)
- Brute force detection accuracy
- Frequency analysis correctness

## Algorithm Details

### Caesar Cipher
Each letter is shifted by `n` positions in the alphabet:
- `E(x) = (x + n) mod 26`
- Case is preserved
- Non-alphabetic characters unchanged

### ROT13
Special case of Caesar cipher with shift 13:
- Self-inverse because `26 mod 13 = 0`
- `ROT13(ROT13(text)) == text`

### Vigenère Cipher
Polyalphabetic substitution using a keyword:
- Each letter uses a different shift based on keyword position
- `E(x) = (x + K[i]) mod 26`
- More resistant to frequency analysis

### Affine Cipher
Mathematical substitution:
- `E(x) = (ax + b) mod 26`
- `a` must be coprime with 26
- Decryption uses modular inverse of `a`

## License

MIT License - Part of AllToolkit Project