# Morse Utils - Rust

A complete Morse code encoding and decoding library with zero external dependencies.

## Features

- **Text to Morse**: Convert text to Morse code
- **Morse to Text**: Decode Morse code back to text
- **Audio Support**: Generate Morse code audio signals (via frequency/samples)
- **Customizable**: Adjustable timing parameters (dot duration, pause, etc.)
- **International Support**: Supports A-Z, 0-9, and common punctuation
- **Error Handling**: Graceful handling of unknown characters

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
morse_utils = { path = "./morse_utils" }
```

## Usage

```rust
use morse_utils::{MorseEncoder, MorseDecoder, MorseConfig};

// Basic encoding
let encoded = MorseEncoder::encode("HELLO WORLD").unwrap();
assert_eq!(encoded, ".... . .-.. .-.. --- / .-- --- .-. .-.. -..");

// Basic decoding
let decoded = MorseDecoder::decode("... --- ...").unwrap();
assert_eq!(decoded, "SOS");

// With custom configuration
let config = MorseConfig {
    dot_duration_ms: 100,
    dash_duration_ms: 300,
    symbol_gap_ms: 100,
    char_gap_ms: 300,
    word_gap_ms: 700,
};
let encoder = MorseEncoder::with_config(config);
```

## API

### MorseEncoder
- `encode(text: &str) -> Result<String, MorseError>`
- `encode_char(c: char) -> Option<&'static str>`
- `with_config(config: MorseConfig) -> Self`

### MorseDecoder
- `decode(morse: &str) -> Result<String, MorseError>`
- `decode_symbol(symbol: &str) -> Option<char>`

### MorseConfig
- `dot_duration_ms: u32` - Duration of a dot in milliseconds
- `dash_duration_ms: u32` - Duration of a dash (default: 3x dot)
- `symbol_gap_ms: u32` - Gap between symbols
- `char_gap_ms: u32` - Gap between characters
- `word_gap_ms: u32` - Gap between words

## Morse Code Reference

```
A: .-      N: -.      0: -----
B: -...    O: ---     1: .----
C: -.-.    P: .--.    2: ..---
D: -..     Q: --.-    3: ...--
E: .       R: .-.     4: ....-
F: ..-.    S: ...     5: .....
G: --.     T: -       6: -....
H: ....    U: ..-     7: --...
I: ..      V: ...-    8: ---..
J: .---    W: .--     9: ----.
K: -.-     X: -..-
L: .-..    Y: -.--
M: --      Z: --..
```

## License

MIT