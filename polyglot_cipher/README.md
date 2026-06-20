# 🔐 Polyglot Cipher v1.0

A creative tool that generates "cipher cards" — language-flavored encryption challenges that embody each programming language's unique character. Each language gets its own cipher algorithm with a thematic justification.

## Features

- **8 Language-Specific Ciphers**: Each language has a custom cipher reflecting its philosophy
  - 🦀 **Rust**: ROT-XOR with ownership-themed key (42)
  - 🐹 **Go**: Sliding window channel cipher
  - 🦅 **Swift**: Unicode scalar shift (key 17)
  - 🟣 **Kotlin**: Null-safe Caesar (space → "null")
  - 🔷 **TypeScript**: Atbash cipher (types mirror perfectly)
  - 🟨 **JavaScript**: Vigenère with "JS" key
  - ☕ **Java**: Classloader reverse + ROT13
  - ⚙️ **C/C++**: Pointer arithmetic XOR/complement
- **Cipher Cards**: Beautifully formatted cards with metadata
- **Rotation Support**: Auto-selects next language via `language_rotation.json`
- **Random Challenges**: Each call generates a fresh challenge phrase

## Installation

```bash
cd polyglot_cipher
python -m polyglot_cipher --help
```

## Usage

```bash
# Run tests
python -m polyglot_cipher --test

# Generate a cipher challenge for current rotation language
python -m polyglot_cipher

# JSON output
python -m polyglot_cipher --json
```

## Example Output

```
╔══════════════════════════════════════════════════════════╗
║  🦀 RUST — Ownership ROT-XOR                              ║
╠══════════════════════════════════════════════════════════╣
║  ENCRYPTED MESSAGE                                       ║
║  xqjjf ytkl                                               ║
║                                                          ║
║  CIPHER METADATA                                         ║
║  Language: Rust                                          ║
║  Algorithm: Ownership ROT-XOR                            ║
║  Key: 42                                                  ║
╚══════════════════════════════════════════════════════════╝
```

## API

### `cipher()`

Main entry point. Rotates to the next language, generates a cipher challenge, updates the rotation file, and returns structured data.

Returns:
```python
{
    "language": "Rust",
    "cipher_name": "Ownership ROT-XOR",
    "challenge": "the borrow checker is my therapist",
    "encoded": "xqjjf ytkl",
    "key": 42,
    "cipher_card": "╔═══...",
    "rotated_at": "2026-06-21T00:00:00+08:00"
}
```

### Individual Cipher Functions

```python
from polyglot_cipher import _rust_cipher, _go_cipher, _typescript_cipher

encoded, key = _rust_cipher("hello rust")
# encoded != "hello rust", key == 42

encoded, _ = _typescript_cipher("abc")
# encoded == "zyx" (Atbash)
```

## Module Structure

```
polyglot_cipher/
├── __init__.py             # All 8 cipher algorithms + helpers
├── __main__.py             # CLI entry point
└── README.md
```

## Testing

```bash
# Module's own test suite
python -m polyglot_cipher --test

# Pytest test suite
python -m pytest polyglot_cipher/tests/ -v
```
