# Zig Morse Code Utils

A comprehensive Morse code utility library for Zig with zero external dependencies.

## Features

- **Encoding**: Convert text to Morse code
- **Decoding**: Convert Morse code back to text
- **Signal Generation**: Generate timed signal sequences for audio/visual output
- **Analysis**: Analyze text and Morse code properties
- **Punctuation Support**: Full support for common punctuation marks
- **Customizable Timing**: Configurable dot/dash durations and gaps
- **Validation**: Validate and clean Morse code strings

## Installation

Add to your `build.zig.zon`:

```zig
.{
    .dependencies = .{
        .morse_code_utils = .{
            .path = "path/to/morse_code_utils",
        },
    },
}
```

Or copy the `src/morse_code_utils.zig` file to your project.

## Usage

### Basic Encoding

```zig
const morse = @import("morse_code_utils");

const encoded = try morse.encode(allocator, "HELLO WORLD");
// Result: ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
```

### Basic Decoding

```zig
const decoded = try morse.decode(allocator, "... --- ...");
// Result: "SOS"
```

### Character Encoding

```zig
const char_code = morse.encodeChar('A');
// Result: ".-"

const char_code2 = morse.encodeChar('!');
// Result: "-.-.--"
```

### Custom Word Separator

```zig
const encoded = try morse.encodeWithSeparator(allocator, "HELLO WORLD", " | ");
// Result: ".... . .-.. .-.. --- | .-- --- .-. .-.. -.."
```

### Signal Generation

```zig
const timing = morse.Timing{
    .dot_duration_ms = 100,
    .dash_duration_ms = 300,
    .intra_char_gap_ms = 100,
    .inter_char_gap_ms = 300,
    .word_gap_ms = 700,
};

const signals = try morse.generateSignals(allocator, "... --- ...", timing);
defer morse.freeSignals(allocator, signals);

for (signals) |signal| {
    if (signal.active) {
        // Turn on output (LED, buzzer, etc.)
    } else {
        // Turn off output
    }
    std.time.sleep(signal.duration_ms * std.time.ns_per_ms);
}
```

### Duration Calculation

```zig
const timing = morse.Timing{};
const encoded = try morse.encode(allocator, "SOS");
const duration_ms = morse.calculateDuration(encoded, timing);
```

### Analysis

```zig
const stats = try morse.analyze(allocator, "HELLO WORLD", timing);
std.debug.print("Dots: {d}\n", .{stats.dots});
std.debug.print("Dashes: {d}\n", .{stats.dashes});
std.debug.print("Letters: {d}\n", .{stats.letters});
std.debug.print("Words: {d}\n", .{stats.words});
```

### Validation

```zig
if (morse.isValidMorse(".- -... -.-.")) {
    // Valid Morse code
}

const cleaned = try morse.cleanMorse(allocator, ".- x .-");
// Result: ".-  .-" (invalid characters removed)
```

### Visual Formatting

```zig
const visual = try morse.formatVisual(allocator, "... --- ...", '•', '—');
// Result: "••• ——— •••"
```

### Emergency Signal

```zig
const sos = try morse.encodeSOS(allocator);
// Result: "... --- ..."
```

## API Reference

### Types

#### `Timing`

```zig
pub const Timing = struct {
    dot_duration_ms: u32 = 100,      // Duration of a dot
    dash_duration_ms: u32 = 300,     // Duration of a dash
    intra_char_gap_ms: u32 = 100,    // Gap between dots/dashes in same letter
    inter_char_gap_ms: u32 = 300,    // Gap between letters
    word_gap_ms: u32 = 700,          // Gap between words
};
```

#### `SignalElement`

```zig
pub const SignalElement = struct {
    active: bool,         // Whether signal is on/off
    duration_ms: u32,     // Duration in milliseconds
};
```

#### `MorseStats`

```zig
pub const MorseStats = struct {
    total_chars: usize,           // Total characters in input
    encodable_chars: usize,      // Characters that can be encoded
    dots: usize,                  // Number of dots
    dashes: usize,                // Number of dashes
    letters: usize,               // Number of letters
    words: usize,                 // Number of words
    estimated_duration_ms: u64,   // Estimated transmission time
};
```

### Functions

| Function | Description |
|----------|-------------|
| `encodeChar(c)` | Encode single character to Morse code |
| `encode(allocator, text)` | Encode string to Morse code |
| `encodeWithSeparator(allocator, text, sep)` | Encode with custom word separator |
| `decode(allocator, morse)` | Decode Morse code to text |
| `decodeWithSeparators(allocator, morse, letter_sep, word_sep)` | Decode with custom separators |
| `generateSignals(allocator, morse, timing)` | Generate signal sequence |
| `freeSignals(allocator, signals)` | Free signal array |
| `isEncodable(c)` | Check if character can be encoded |
| `countEncodable(text)` | Count encodable characters |
| `calculateDuration(morse, timing)` | Calculate total duration |
| `countSymbols(morse)` | Count dots and dashes |
| `formatVisual(allocator, morse, dot, dash)` | Format with custom characters |
| `encodeSOS(allocator)` | Generate SOS distress signal |
| `isValidMorse(morse)` | Validate Morse code string |
| `cleanMorse(allocator, morse)` | Remove invalid characters |
| `analyze(allocator, text, timing)` | Analyze text and Morse properties |

## Supported Characters

- **Letters**: A-Z (case insensitive)
- **Numbers**: 0-9
- **Punctuation**: . , ? ' ! / ( ) & : ; = + - _ " $ @

## Morse Code Reference

| Character | Code | Character | Code |
|-----------|------|-----------|------|
| A | .- | N | -. |
| B | -... | O | --- |
| C | -.-. | P | .--. |
| D | -.. | Q | --.- |
| E | . | R | .-. |
| F | ..-. | S | ... |
| G | --. | T | - |
| H | .... | U | ..- |
| I | .. | V | ...- |
| J | .--- | W | .-- |
| K | -.- | X | -..- |
| L | .-.. | Y | -.-- |
| M | -- | Z | --.. |
| 0 | ----- | 6 | -.... |
| 1 | .---- | 7 | --... |
| 2 | ..--- | 8 | ---.. |
| 3 | ...-- | 9 | ----. |
| 4 | ....- | . | .-.-.- |
| 5 | ..... | , | --..-- |

## Building

```bash
# Run tests
zig build test

# Run example
zig build example
```

## License

MIT License