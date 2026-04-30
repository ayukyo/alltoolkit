# Morse Code Utils

A zero-dependency Rust library for encoding and decoding Morse code.

## Features

- **Text to Morse encoding**: Convert any text to standard Morse code
- **Morse to Text decoding**: Convert Morse code back to readable text
- **Full character support**: Letters (A-Z), numbers (0-9), and common punctuation
- **Audio signal generation**: Generate timing patterns for audio output
- **Binary representation**: Convert Morse code to binary on/off patterns

## Installation

Add this to your `Cargo.toml`:

```toml
[dependencies]
morse_code_utils = "0.1.0"
```

## Usage

### Basic Encoding and Decoding

```rust
use morse_code_utils::MorseCode;

let morse = MorseCode::new();

// Encode text to Morse code
let encoded = morse.encode_default("HELLO WORLD");
// Result: ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."

// Decode Morse code to text
let decoded = morse.decode_default("... --- ...");
// Result: "SOS"
```

### Custom Delimiters

```rust
let morse = MorseCode::new();

// Use custom delimiters
let encoded = morse.encode("SOS HELP", "|", "||");
// Result: "...|---|...||....|.|.-..|.--."
```

### Audio Signal Generation

```rust
use morse_code_utils::{MorseCode, to_signals, to_durations};

let morse = MorseCode::new();
let encoded = morse.encode_default("SOS");

// Get signal pattern
let signals = to_signals(&encoded);
// Returns: [Dit, IntraCharGap, Dit, IntraCharGap, Dit, LetterGap, ...]

// Get timing durations (in arbitrary units)
let durations = to_durations(&signals);
// Returns: [(Dit, 1), (IntraCharGap, 1), (Dit, 1), ...]
```

### Binary Representation

```rust
use morse_code_utils::{to_binary, from_binary};

// Convert to binary (1 = signal on, 0 = signal off)
let binary = to_binary(".-");
// Result: "10111" (dit=1, gap=0, dah=111)

// Convert back to Morse code
let morse = from_binary("10111");
// Result: Some(".-")
```

## API Reference

### `MorseCode`

| Method | Description |
|--------|-------------|
| `new()` | Create a new instance with standard mappings |
| `encode_default(text)` | Encode with default delimiters (space, /) |
| `encode(text, letter_delim, word_delim)` | Encode with custom delimiters |
| `decode_default(morse)` | Decode with default delimiters |
| `decode(morse, letter_delim, word_delim)` | Decode with custom delimiters |
| `can_encode(char)` | Check if a character can be encoded |
| `is_valid_morse(code)` | Check if a string is valid Morse code |
| `get_morse(char)` | Get Morse code for a single character |
| `get_char(code)` | Get character for a Morse sequence |

### Signal Functions

| Function | Description |
|----------|-------------|
| `to_signals(morse)` | Convert Morse code to signal pattern |
| `to_durations(signals)` | Convert signals to timing durations |
| `to_binary(morse)` | Convert to binary on/off pattern |
| `from_binary(binary)` | Convert binary back to Morse code |

## Standard Morse Code Timing

| Element | Duration (units) |
|---------|-----------------|
| Dit (.) | 1 |
| Dah (-) | 3 |
| Intra-character gap | 1 |
| Letter gap | 3 |
| Word gap | 7 |

## Supported Characters

### Letters
```
A: .-      B: -...    C: -.-.    D: -..     E: .
F: ..-.    G: --.     H: ....    I: ..      J: .---
K: -.-     L: .-..    M: --      N: -.      O: ---
P: .--.    Q: --.-    R: .-.     S: ...     T: -
U: ..-     V: ...-    W: .--     X: -..-    Y: -.--
Z: --..
```

### Numbers
```
0: -----   1: .----   2: ..---   3: ...--   4: ....-
5: .....   6: -....   7: --...   8: ---..   9: ----.
```

### Punctuation
```
.: .-.-.-   ,: --..--   ?: ..--..   ': .----.
!: -.-.--   /: -..-.    (: -.--.    ): -.--.-
&: .-...    : ---...    ;: -.-.-.   =: -...-
+: .-.-.    -: -....-   _: ..--.-   ": .-..-.
$: ...-..-  @: .--.-.
```

## License

MIT License