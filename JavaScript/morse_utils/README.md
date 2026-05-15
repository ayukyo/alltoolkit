# Morse Code Utilities (morse_utils)

A comprehensive Morse code encoding, decoding, and signal processing utility module for JavaScript. Zero external dependencies, pure JavaScript implementation.

## Features

- **Text to Morse code encoding** - Convert any text to standard Morse code
- **Morse code to text decoding** - Convert Morse code back to readable text
- **Multi-language support** - English, numbers, punctuation, Cyrillic, Greek, extended Latin
- **Audio signal generation** - Generate timing patterns and audio samples for transmission
- **Visual signal patterns** - Create LED/flashlight patterns
- **Signal detection and parsing** - Parse incoming Morse signals
- **Speed control (WPM)** - Words Per Minute for timing calculations
- **Prosign support** - Special combined signals (SOS, AR, SK, etc.)
- **International standard compliant** - Follows ITU-R M.1677-1 standard

## Installation

```javascript
// Import the module
const morse = require('./morse_utils/mod.js');
```

## Quick Start

### Basic Encoding and Decoding

```javascript
const morse = require('./morse_utils/mod.js');

// Encode text to Morse code
console.log(morse.encode('HELLO'));
// Output: ".... . .-.. .-.. ---"

console.log(morse.encode('SOS'));
// Output: "... --- ..."

// Decode Morse code to text
console.log(morse.decode('.... . .-.. .-.. ---'));
// Output: "HELLO"
```

### Custom Symbols

```javascript
const encoder = new morse.MorseEncoder({
  dotSymbol: '*',
  dashSymbol: '_'
});

console.log(encoder.encode('HELLO'));
// Output: "**** * *_** *_** ___"
```

### Signal Generation

```javascript
const generator = new morse.MorseSignalGenerator({ wpm: 15 });

// Get timing for each element
const timing = generator.getTiming();
console.log(timing);
// { dot: 0.08, dash: 0.24, interChar: 0.24, wordSpace: 0.56 }

// Generate timing pattern
const pattern = generator.generateTimingPattern('SOS');
console.log(pattern);
// [['on', 0.08], ['off', 0.08], ...]

// Calculate transmission duration
const duration = generator.calculateDuration('HELLO WORLD');
console.log(`Duration: ${duration.toFixed(2)} seconds`);
```

### Visual Representation

```javascript
// Generate visual pattern for display
console.log(morse.toVisual('HELLO'));
// Output: "███░███░███░███░███░░░░░███..."
```

### Statistics

```javascript
const stats = morse.getStats('HELLO WORLD');
console.log(stats);
// {
//   dots: 14,
//   dashes: 6,
//   characters: 10,
//   words: 2,
//   totalUnits: 62
// }
```

## API Reference

### Constants

- `TIMING` - Standard timing units (DOT, DASH, INTRA_CHAR, INTER_CHAR, WORD_SPACE)
- `MORSE_CODE` - Character to Morse code mapping
- `MORSE_DECODE` - Morse code to character mapping
- `PROSIGNS` - Prosign mappings (SOS, AR, SK, etc.)

### Classes

#### MorseEncoder

```javascript
const encoder = new morse.MorseEncoder(options);
```

Options:
- `dotSymbol` - Symbol for dot (default: '.')
- `dashSymbol` - Symbol for dash (default: '-')
- `charSeparator` - Separator between characters (default: ' ')
- `wordSeparator` - Separator between words (default: '   ')
- `lowercase` - Output in lowercase (default: false)
- `throwOnError` - Throw on unknown characters (default: false)
- `unknownChar` - Character for unknown codes (default: '?')

Methods:
- `encode(text)` - Encode text to Morse code
- `encodeChar(char)` - Encode a single character
- `encodeProsign(name)` - Encode a prosign
- `canEncode(char)` - Check if character can be encoded
- `getSupportedChars()` - Get list of supported characters

#### MorseDecoder

```javascript
const decoder = new morse.MorseDecoder(options);
```

Options:
- `dotSymbol` - Symbol for dot (default: '.')
- `dashSymbol` - Symbol for dash (default: '-')
- `charSeparator` - Separator between characters (default: ' ')
- `wordSeparator` - Separator between words (default: '   ')
- `lowercase` - Output in lowercase (default: false)
- `throwOnError` - Throw on unknown codes (default: false)
- `unknownChar` - Character for unknown codes (default: '?')

Methods:
- `decode(morse)` - Decode Morse code to text
- `decodeChar(code)` - Decode a single Morse code
- `canDecode(code)` - Check if code can be decoded

#### MorseSignalGenerator

```javascript
const generator = new morse.MorseSignalGenerator(options);
```

Options:
- `wpm` - Words per minute (default: 15)
- `frequency` - Audio frequency in Hz (default: 600)
- `sampleRate` - Audio sample rate (default: 44100)

Methods:
- `setWpm(wpm)` - Set speed
- `getTiming()` - Get timing values
- `generateTimingPattern(text)` - Generate timing array
- `generateBinaryPattern(text)` - Generate binary pattern
- `generateAudio(text)` - Generate audio samples (Float32Array)
- `generateBeepSchedule(text)` - Generate beep schedule
- `calculateDuration(text)` - Calculate transmission duration

#### MorseSignalParser

```javascript
const parser = new morse.MorseSignalParser(options);
```

Options:
- `wpm` - Words per minute (default: 15)
- `tolerance` - Timing tolerance (default: 0.3)

Methods:
- `parseIntervals(intervals)` - Parse timing intervals
- `parseBinary(binary)` - Parse binary pattern
- `detectWpm(intervals)` - Detect speed from intervals

### Utility Functions

- `encode(text, options)` - Quick encode
- `decode(morse, options)` - Quick decode
- `isValidText(text)` - Check if text is valid
- `isValidMorse(morse)` - Check if Morse code is valid
- `getMorseCode(char)` - Get code for character
- `getCharFromMorse(code)` - Get character for code
- `getStats(text)` - Get statistics for text
- `toVisual(text, options)` - Generate visual pattern
- `estimateTime(text, wpm)` - Estimate transmission time
- `generatePractice(options)` - Generate practice sequence

## Supported Characters

### Letters
ABCDEFGHIJKLMNOPQRSTUVWXYZ

### Numbers
0123456789

### Punctuation
. , ? ' ! / ( ) & : ; = + - _ " $ @ ¿ ¡

### Extended Latin
À Ä Å Æ Ç Ð È É Ê Ë Ì Î Ñ Ö Ø Ś Š Þ Ü Ů Ź Ż

### Cyrillic (Russian)
А Б В Г Д Е Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я

### Greek
Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω

## Prosigns

| Prosign | Code | Meaning |
|---------|------|---------|
| SOS | `...---...` | Distress signal |
| AR | `.-.-.` | End of message |
| SK | `...-.-` | End of work |
| BT | `-...-` | Separator |
| AA | `.-.-` | End of line |
| AS | `.-...` | Wait |
| KN | `-.--.` | Invitation |
| HH | `........` | Error |

## Examples

See `test.js` for comprehensive test coverage and usage examples.

## Standard Compliance

This implementation follows the international Morse code standard (ITU-R M.1677-1) for timing:
- 1 unit for dot
- 3 units for dash
- 1 unit for intra-character gap
- 3 units for inter-character gap  
- 7 units for word gap

The word "PARIS" is used as the standard for calculating Words Per Minute (WPM), containing exactly 50 timing units.

## License

MIT License