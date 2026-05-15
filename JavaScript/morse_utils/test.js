/**
 * AllToolkit - Morse Code Utilities Tests
 * ========================================
 * Comprehensive test suite for morse_utils module.
 */

const assert = require('assert');
const morse = require('./mod.js');

// ============================================================================
// Test Helpers
// ============================================================================

let passedTests = 0;
let failedTests = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
    passedTests++;
  } catch (error) {
    console.log(`✗ ${name}`);
    console.log(`  Error: ${error.message}`);
    failedTests++;
  }
}

function group(name) {
  console.log(`\n=== ${name} ===`);
}

// ============================================================================
// Tests
// ============================================================================

group('Constants');

test('TIMING constants are defined', () => {
  assert.strictEqual(morse.TIMING.DOT, 1);
  assert.strictEqual(morse.TIMING.DASH, 3);
  assert.strictEqual(morse.TIMING.INTRA_CHAR, 1);
  assert.strictEqual(morse.TIMING.INTER_CHAR, 3);
  assert.strictEqual(morse.TIMING.WORD_SPACE, 7);
});

test('MORSE_CODE contains letters', () => {
  assert.strictEqual(morse.MORSE_CODE['A'], '.-');
  assert.strictEqual(morse.MORSE_CODE['B'], '-...');
  assert.strictEqual(morse.MORSE_CODE['E'], '.');
  assert.strictEqual(morse.MORSE_CODE['S'], '...');
  assert.strictEqual(morse.MORSE_CODE['O'], '---');
  assert.strictEqual(morse.MORSE_CODE['Z'], '--..');
});

test('MORSE_CODE contains numbers', () => {
  assert.strictEqual(morse.MORSE_CODE['0'], '-----');
  assert.strictEqual(morse.MORSE_CODE['5'], '.....');
  assert.strictEqual(morse.MORSE_CODE['9'], '----.');
});

test('MORSE_CODE contains punctuation', () => {
  assert.strictEqual(morse.MORSE_CODE['.'], '.-.-.-');
  assert.strictEqual(morse.MORSE_CODE[','], '--..--');
  assert.strictEqual(morse.MORSE_CODE['?'], '..--..');
  assert.strictEqual(morse.MORSE_CODE['!'], '-.-.--');
});

test('PROSIGNS are defined', () => {
  assert.strictEqual(morse.PROSIGNS['SOS'], '...---...');
  assert.strictEqual(morse.PROSIGNS['AR'], '.-.-.');
  assert.strictEqual(morse.PROSIGNS['SK'], '...-.-');
});

group('MorseEncoder');

test('encode simple text', () => {
  const encoder = new morse.MorseEncoder();
  assert.strictEqual(encoder.encode('SOS'), '... --- ...');
  assert.strictEqual(encoder.encode('HELLO'), '.... . .-.. .-.. ---');
  assert.strictEqual(encoder.encode('MORSE'), '-- --- .-. ... .');
});

test('encode with custom symbols', () => {
  const encoder = new morse.MorseEncoder({ dotSymbol: '*', dashSymbol: '_' });
  assert.strictEqual(encoder.encode('A'), '*_');
  assert.strictEqual(encoder.encode('B'), '_***');
});

test('encode numbers', () => {
  const encoder = new morse.MorseEncoder();
  assert.strictEqual(encoder.encode('123'), '.---- ..--- ...--');
  assert.strictEqual(encoder.encode('911'), '----. .---- .----');
});

test('encode sentence with spaces', () => {
  const encoder = new morse.MorseEncoder();
  const result = encoder.encode('HELLO WORLD');
  assert.strictEqual(result, '.... . .-.. .-.. ---   .-- --- .-. .-.. -..');
});

test('encode punctuation', () => {
  const encoder = new morse.MorseEncoder();
  assert.strictEqual(encoder.encode('OK?'), '--- -.- ..--..');
  assert.strictEqual(encoder.encode('YES!'), '-.-- . ... -.-.--');
});

test('encode single character', () => {
  const encoder = new morse.MorseEncoder();
  assert.strictEqual(encoder.encodeChar('A'), '.-');
  assert.strictEqual(encoder.encodeChar('E'), '.');
  assert.strictEqual(encoder.encodeChar('0'), '-----');
});

test('encode prosign', () => {
  const encoder = new morse.MorseEncoder();
  assert.strictEqual(encoder.encodeProsign('SOS'), '...---...');
  assert.strictEqual(encoder.encodeProsign('AR'), '.-.-.');
});

test('handle unknown characters', () => {
  const encoder = new morse.MorseEncoder();
  assert.strictEqual(encoder.encode('#'), '?');
  
  const strictEncoder = new morse.MorseEncoder({ throwOnError: true });
  assert.throws(() => strictEncoder.encode('#'), /Unknown character/);
});

test('canEncode check', () => {
  const encoder = new morse.MorseEncoder();
  assert.strictEqual(encoder.canEncode('A'), true);
  assert.strictEqual(encoder.canEncode('5'), true);
  assert.strictEqual(encoder.canEncode('#'), false);
  assert.strictEqual(encoder.canEncode(''), false);
  assert.strictEqual(encoder.canEncode('AB'), false);
});

test('getSupportedChars returns array', () => {
  const encoder = new morse.MorseEncoder();
  const chars = encoder.getSupportedChars();
  assert.ok(Array.isArray(chars));
  assert.ok(chars.includes('A'));
  assert.ok(chars.includes('0'));
  assert.ok(chars.length > 50);
});

test('handle empty input', () => {
  const encoder = new morse.MorseEncoder();
  assert.strictEqual(encoder.encode(''), '');
  assert.strictEqual(encoder.encode(null), '');
});

group('MorseDecoder');

test('decode simple Morse code', () => {
  const decoder = new morse.MorseDecoder();
  assert.strictEqual(decoder.decode('... --- ...'), 'SOS');
  assert.strictEqual(decoder.decode('.... . .-.. .-.. ---'), 'HELLO');
});

test('decode with custom symbols', () => {
  const decoder = new morse.MorseDecoder({ dotSymbol: '*', dashSymbol: '_' });
  assert.strictEqual(decoder.decode('*_'), 'A');
  assert.strictEqual(decoder.decode('_***'), 'B');
});

test('decode numbers', () => {
  const decoder = new morse.MorseDecoder();
  assert.strictEqual(decoder.decode('.---- ..--- ...--'), '123');
});

test('decode sentence with word spaces', () => {
  const decoder = new morse.MorseDecoder();
  assert.strictEqual(decoder.decode('.... . .-.. .-.. ---   .-- --- .-. .-.. -..'), 'HELLO WORLD');
});

test('decode punctuation', () => {
  const decoder = new morse.MorseDecoder();
  assert.strictEqual(decoder.decode('--- -.- ..--..'), 'OK?');
});

test('decode single character', () => {
  const decoder = new morse.MorseDecoder();
  assert.strictEqual(decoder.decodeChar('.-'), 'A');
  assert.strictEqual(decoder.decodeChar('.'), 'E');
});

test('decode prosign', () => {
  const decoder = new morse.MorseDecoder();
  assert.strictEqual(decoder.decodeChar('...---...'), 'SOS');
  assert.strictEqual(decoder.decodeChar('.-.-.'), 'AR');
});

test('handle unknown codes', () => {
  const decoder = new morse.MorseDecoder();
  assert.strictEqual(decoder.decode('...........'), '?');
  
  const strictDecoder = new morse.MorseDecoder({ throwOnError: true });
  assert.throws(() => strictDecoder.decode('...........'), /Unknown Morse code/);
});

test('lowercase output', () => {
  const decoder = new morse.MorseDecoder({ lowercase: true });
  assert.strictEqual(decoder.decode('.-'), 'a');
  assert.strictEqual(decoder.decode('.... . .-.. .-.. ---'), 'hello');
});

test('handle empty input', () => {
  const decoder = new morse.MorseDecoder();
  assert.strictEqual(decoder.decode(''), '');
  assert.strictEqual(decoder.decode(null), '');
});

test('canDecode check', () => {
  const decoder = new morse.MorseDecoder();
  assert.strictEqual(decoder.canDecode('.-'), true);
  assert.strictEqual(decoder.canDecode('...---...'), true);
  assert.strictEqual(decoder.canDecode('...........'), false);
});

group('Encode/Decode Roundtrip');

test('roundtrip: simple text', () => {
  const text = 'HELLO';
  const encoded = morse.encode(text);
  const decoded = morse.decode(encoded);
  assert.strictEqual(decoded, text);
});

test('roundtrip: sentence', () => {
  const text = 'THE QUICK BROWN FOX';
  const encoded = morse.encode(text);
  const decoded = morse.decode(encoded);
  assert.strictEqual(decoded, text);
});

test('roundtrip: numbers', () => {
  const text = '2024';
  const encoded = morse.encode(text);
  const decoded = morse.decode(encoded);
  assert.strictEqual(decoded, text);
});

test('roundtrip: mixed content', () => {
  const text = 'MORSE CODE TEST 123';
  const encoded = morse.encode(text);
  const decoded = morse.decode(encoded);
  assert.strictEqual(decoded, text);
});

group('MorseSignalGenerator');

test('set WPM changes timing', () => {
  const gen1 = new morse.MorseSignalGenerator({ wpm: 10 });
  const gen2 = new morse.MorseSignalGenerator({ wpm: 20 });
  
  const timing1 = gen1.getTiming();
  const timing2 = gen2.getTiming();
  
  // Higher WPM = shorter timing
  assert.ok(timing1.dot > timing2.dot);
  assert.strictEqual(timing1.dot, 0.12); // 1.2 / 10
  assert.strictEqual(timing2.dot, 0.06); // 1.2 / 20
});

test('getTiming returns correct values', () => {
  const gen = new morse.MorseSignalGenerator({ wpm: 15 });
  const timing = gen.getTiming();
  
  const expectedDot = 1.2 / 15;
  // Use approximate comparison for floating point
  assert.ok(Math.abs(timing.dot - expectedDot) < 0.0001);
  assert.ok(Math.abs(timing.dash - 3 * expectedDot) < 0.0001);
  assert.ok(Math.abs(timing.interChar - 3 * expectedDot) < 0.0001);
  assert.ok(Math.abs(timing.wordSpace - 7 * expectedDot) < 0.0001);
});

test('generateTimingPattern produces valid pattern', () => {
  const gen = new morse.MorseSignalGenerator({ wpm: 15 });
  const pattern = gen.generateTimingPattern('SOS');
  
  assert.ok(Array.isArray(pattern));
  assert.ok(pattern.length > 0);
  
  // First element should be 'on' (signal)
  assert.strictEqual(pattern[0][0], 'on');
  assert.ok(pattern[0][1] > 0);
});

test('generateBinaryPattern produces valid binary', () => {
  const gen = new morse.MorseSignalGenerator({ wpm: 15 });
  const binary = gen.generateBinaryPattern('A');
  
  assert.ok(binary.includes('1'));
  assert.ok(binary.includes('0'));
  // Pattern for A (.-) should have short 1s (dot) and long 1s (dash)
});

test('generateBeepSchedule produces valid schedule', () => {
  const gen = new morse.MorseSignalGenerator({ wpm: 15 });
  const schedule = gen.generateBeepSchedule('HELLO');
  
  assert.ok(Array.isArray(schedule));
  assert.ok(schedule.length > 0);
  
  for (const beep of schedule) {
    assert.ok(beep.start >= 0);
    assert.ok(beep.end > beep.start);
    assert.ok(['dot', 'dash'].includes(beep.type));
  }
});

test('calculateDuration returns positive number', () => {
  const gen = new morse.MorseSignalGenerator({ wpm: 15 });
  const duration = gen.calculateDuration('HELLO WORLD');
  
  assert.ok(duration > 0);
  assert.ok(typeof duration === 'number');
});

test('generateAudio produces Float32Array', () => {
  const gen = new morse.MorseSignalGenerator({ wpm: 15 });
  const audio = gen.generateAudio('HELLO');
  
  assert.ok(audio instanceof Float32Array);
  assert.ok(audio.length > 0);
  
  // Check that samples are in valid range
  for (let i = 0; i < audio.length; i++) {
    assert.ok(audio[i] >= -1 && audio[i] <= 1);
  }
});

test('invalid WPM throws error', () => {
  assert.throws(() => new morse.MorseSignalGenerator({ wpm: 0 }), /WPM must be positive/);
  assert.throws(() => new morse.MorseSignalGenerator({ wpm: -5 }), /WPM must be positive/);
});

group('MorseSignalParser');

test('parseIntervals decodes correctly', () => {
  const parser = new morse.MorseSignalParser({ wpm: 15 });
  
  // SOS at 15 WPM (unit time = 0.08 seconds)
  // ... --- ... 
  // dots: 0.08s, dashes: 0.24s
  const intervals = [
    [0.08, 1], [0.08, 0],  // .
    [0.08, 1], [0.08, 0],  // .
    [0.08, 1], [0.24, 0],  // . (word space after)
    [0.24, 1], [0.08, 0],  // ---
    [0.24, 1], [0.08, 0],
    [0.24, 1], [0.24, 0],  // ---
    [0.08, 1], [0.08, 0],  // .
    [0.08, 1], [0.08, 0],  // .
    [0.08, 1], [0.1, 0],   // .
  ];
  
  const result = parser.parseIntervals(intervals);
  assert.strictEqual(result.includes('.'), true);
  assert.strictEqual(result.includes('-'), true);
});

test('parseBinary decodes correctly', () => {
  const parser = new morse.MorseSignalParser();
  
  // Simple binary pattern for 'A' (._)
  // Dot = 3 samples, Dash = 9 samples, gaps = 3 samples
  const binary = '111000111111111000'; // . _ (with intra-char gap)
  
  const result = parser.parseBinary(binary);
  assert.strictEqual(result, '.-');
});

test('detectWpm estimates speed', () => {
  const parser = new morse.MorseSignalParser();
  
  // Intervals at 15 WPM (unit = 0.08s)
  const intervals = [
    [0.08, 1], [0.08, 0],
    [0.08, 1], [0.08, 0],
    [0.24, 1], [0.08, 0],
  ];
  
  const wpm = parser.detectWpm(intervals);
  assert.ok(wpm > 10 && wpm < 20);
});

test('handle empty intervals', () => {
  const parser = new morse.MorseSignalParser();
  assert.strictEqual(parser.parseIntervals([]), '');
  assert.strictEqual(parser.parseIntervals(null), '');
});

group('Utility Functions');

test('encode function works', () => {
  assert.strictEqual(morse.encode('HELLO'), '.... . .-.. .-.. ---');
  assert.strictEqual(morse.encode('SOS'), '... --- ...');
});

test('decode function works', () => {
  assert.strictEqual(morse.decode('.... . .-.. .-.. ---'), 'HELLO');
  assert.strictEqual(morse.decode('... --- ...'), 'SOS');
});

test('isValidText validates text', () => {
  assert.strictEqual(morse.isValidText('HELLO'), true);
  assert.strictEqual(morse.isValidText('HELLO WORLD'), true);
  assert.strictEqual(morse.isValidText('ABC#'), false);
  assert.strictEqual(morse.isValidText(''), true);
});

test('isValidMorse validates Morse code', () => {
  assert.strictEqual(morse.isValidMorse('.-'), true);
  assert.strictEqual(morse.isValidMorse('.- -...'), true);
  assert.strictEqual(morse.isValidMorse('... --- ...'), true);
  assert.strictEqual(morse.isValidMorse('.......'), false); // Invalid code
  assert.strictEqual(morse.isValidMorse(''), true);
});

test('getMorseCode returns correct code', () => {
  assert.strictEqual(morse.getMorseCode('A'), '.-');
  assert.strictEqual(morse.getMorseCode('E'), '.');
  assert.strictEqual(morse.getMorseCode('5'), '.....');
  assert.strictEqual(morse.getMorseCode('#'), null);
  assert.strictEqual(morse.getMorseCode(''), null);
  assert.strictEqual(morse.getMorseCode('AB'), null);
});

test('getCharFromMorse returns correct character', () => {
  assert.strictEqual(morse.getCharFromMorse('.-'), 'A');
  assert.strictEqual(morse.getCharFromMorse('.'), 'E');
  assert.strictEqual(morse.getCharFromMorse('.....'), '5');
  assert.strictEqual(morse.getCharFromMorse('.......'), null);
  assert.strictEqual(morse.getCharFromMorse(''), null);
});

test('getStats returns valid statistics', () => {
  const stats = morse.getStats('HELLO');
  
  assert.strictEqual(stats.text, 'HELLO');
  assert.ok(stats.morse.includes('.'));
  assert.ok(stats.morse.includes('-'));
  // HELLO = H(.... 4 dots) + E(. 1 dot) + L(.-.. 3 dots 1 dash) + L(.-.. 3 dots 1 dash) + O(--- 3 dashes)
  // Total: 11 dots + 5 dashes
  assert.strictEqual(stats.dots, 11);
  assert.strictEqual(stats.dashes, 5);
  assert.strictEqual(stats.characters, 5);
  assert.strictEqual(stats.words, 1);
  assert.ok(stats.totalUnits > 0);
});

test('toVisual produces visual pattern', () => {
  const visual = morse.toVisual('A');
  
  assert.ok(visual.includes('█'));
  assert.ok(visual.includes('░'));
  assert.ok(visual.length > 0);
});

test('estimateTime calculates duration', () => {
  const time = morse.estimateTime('HELLO', 15);
  
  assert.ok(time > 0);
  assert.ok(typeof time === 'number');
  
  // Higher WPM should give shorter time
  const fasterTime = morse.estimateTime('HELLO', 30);
  assert.ok(fasterTime < time);
});

test('generatePractice creates practice items', () => {
  const practice = morse.generatePractice({ count: 5 });
  
  assert.ok(Array.isArray(practice));
  assert.strictEqual(practice.length, 5);
  
  for (const item of practice) {
    assert.ok(item.char);
    assert.ok(item.morse);
    assert.ok(typeof item.char === 'string');
    assert.ok(typeof item.morse === 'string');
  }
});

test('generatePractice with custom chars', () => {
  const practice = morse.generatePractice({
    chars: ['A', 'B', 'C'],
    count: 10
  });
  
  assert.strictEqual(practice.length, 10);
  
  for (const item of practice) {
    assert.ok(['A', 'B', 'C'].includes(item.char));
  }
});

test('generatePractice with words', () => {
  const practice = morse.generatePractice({
    count: 20,
    includeWords: true
  });
  
  assert.strictEqual(practice.length, 20);
  
  // Some items should be words (length > 1)
  const words = practice.filter(p => p.char.length > 1);
  assert.ok(words.length > 0);
});

group('Edge Cases');

test('handle null/undefined inputs', () => {
  assert.strictEqual(morse.encode(null), '');
  assert.strictEqual(morse.encode(undefined), '');
  assert.strictEqual(morse.decode(null), '');
  assert.strictEqual(morse.decode(undefined), '');
});

test('handle whitespace-only input', () => {
  assert.strictEqual(morse.encode('   '), '');
  assert.strictEqual(morse.decode('   '), '');
});

test('handle very long text', () => {
  const longText = 'HELLO WORLD '.repeat(100);
  const encoded = morse.encode(longText);
  const decoded = morse.decode(encoded);
  
  assert.strictEqual(decoded, longText.trim());
  assert.ok(encoded.length > 1000);
});

test('handle special whitespace characters', () => {
  const encoder = new morse.MorseEncoder();
  
  // Tabs and newlines should be treated as word separators
  const result = encoder.encode('A\tB');
  assert.ok(result.includes('   ')); // Word space
  
  const result2 = encoder.encode('A\nB');
  assert.ok(result2.includes('   ')); // Word space
});

group('International Support');

test('encode Cyrillic characters', () => {
  const encoder = new morse.MorseEncoder();
  assert.strictEqual(encoder.encode('А'), '.-'); // Russian A
  assert.strictEqual(encoder.encode('Б'), '-...'); // Russian B
});

test('encode Greek characters', () => {
  const encoder = new morse.MorseEncoder();
  assert.strictEqual(encoder.encode('Α'), '.-'); // Greek Alpha
  assert.strictEqual(encoder.encode('Β'), '-...'); // Greek Beta
});

test('encode extended Latin characters', () => {
  const encoder = new morse.MorseEncoder();
  assert.strictEqual(encoder.encode('Ä'), '.-.-');
  assert.strictEqual(encoder.encode('Ö'), '---.');
  assert.strictEqual(encoder.encode('Ü'), '..--');
  assert.strictEqual(encoder.encode('Ñ'), '--.--');
});

// ============================================================================
// Summary
// ============================================================================

console.log('\n=================================');
console.log(`Tests: ${passedTests + failedTests}`);
console.log(`Passed: ${passedTests}`);
console.log(`Failed: ${failedTests}`);
console.log('=================================\n');

if (failedTests > 0) {
  process.exit(1);
} else {
  console.log('All tests passed! ✓');
  process.exit(0);
}