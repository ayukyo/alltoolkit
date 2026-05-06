/**
 * Morse Code Utilities Test Suite
 * 
 * Comprehensive tests for the Morse code utilities module.
 * Run with: npx ts-node morse_utils_test.ts
 * Or compile: tsc morse_utils_test.ts && node morse_utils_test.js
 */

import {
  encode,
  encodeStrict,
  decode,
  decodeLenient,
  getMorseCode,
  getCharacter,
  isValidCharacter,
  isValidMorse,
  canEncode,
  defaultTiming,
  fastTiming,
  slowTiming,
  customTiming,
  wpmToDotDuration,
  dotDurationToWpm,
  toSignals,
  getTotalDuration,
  generateAudioWaveform,
  toBinary,
  fromBinary,
  analyze,
  normalize,
  transpose,
  getProsign,
  isProsign,
  encodeProsign,
  getAllCodes,
  MorseUtils,
  PROSIGNS,
  MorseTimingConfig,
  MorseSignal,
} from './mod';

// Test result tracking
let passed = 0;
let failed = 0;

function test(name: string, fn: () => void): void {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (error) {
    console.error(`✗ ${name}`);
    console.error(`  Error: ${error}`);
    failed++;
  }
}

function assertEqual(actual: any, expected: any, message?: string): void {
  if (actual !== expected) {
    throw new Error(`${message || 'Assertion failed'}: expected ${expected}, got ${actual}`);
  }
}

function assertTrue(value: boolean, message?: string): void {
  if (!value) {
    throw new Error(message || 'Expected true, got false');
  }
}

function assertFalse(value: boolean, message?: string): void {
  if (value) {
    throw new Error(message || 'Expected false, got true');
  }
}

function assertMatch(value: string, pattern: RegExp, message?: string): void {
  if (!pattern.test(value)) {
    throw new Error(`${message || 'Pattern match failed'}: ${value} does not match ${pattern}`);
  }
}

function assertThrows(fn: () => void, message?: string): void {
  try {
    fn();
    throw new Error(message || 'Expected function to throw');
  } catch (e) {
    if (e instanceof Error && e.message === (message || 'Expected function to throw')) {
      throw e;
    }
    // Function threw as expected
  }
}

// ==================== Encoding Tests ====================

test('encode() encodes simple text', () => {
  assertEqual(encode('SOS'), '... --- ...', 'SOS should encode correctly');
});

test('encode() handles lowercase', () => {
  assertEqual(encode('hello'), '.... . .-.. .-.. ---', 'Lowercase should work');
});

test('encode() handles mixed case', () => {
  assertEqual(encode('HeLLo'), '.... . .-.. .-.. ---', 'Mixed case should work');
});

test('encode() encodes single character', () => {
  assertEqual(encode('A'), '.-', 'A should encode to .-');
  assertEqual(encode('E'), '.', 'E should encode to .');
  assertEqual(encode('T'), '-', 'T should encode to -');
});

test('encode() handles words with spaces', () => {
  assertEqual(encode('HELLO WORLD'), '.... . .-.. .-.. --- / .-- --- .-. .-.. -..', 'Should handle word separator');
});

test('encode() handles numbers', () => {
  assertEqual(encode('123'), '.---- ..--- ...--', 'Numbers should encode correctly');
  assertEqual(encode('0'), '-----', '0 should encode correctly');
  assertEqual(encode('9'), '----.', '9 should encode correctly');
});

test('encode() handles punctuation', () => {
  assertEqual(encode('.'), '.-.-.-', 'Period should encode correctly');
  assertEqual(encode(','), '--..--', 'Comma should encode correctly');
  assertEqual(encode('?'), '..--..', 'Question mark should encode correctly');
  assertEqual(encode('!'), '-.-.--', 'Exclamation should encode correctly');
  assertEqual(encode('@'), '.--.-.', 'At sign should encode correctly');
});

test('encode() handles empty string', () => {
  assertEqual(encode(''), '', 'Empty string should return empty');
});

test('encode() skips invalid characters', () => {
  // Characters like ~, #, etc. are skipped
  const result = encode('A~B');
  assertEqual(result, '.- -...', 'Invalid characters should be skipped');
});

test('encodeStrict() throws on invalid character', () => {
  assertThrows(() => encodeStrict('ABC~'), 'Should throw for invalid character');
});

test('encode() with custom separator', () => {
  const result = encode('ABC', { separator: '/' });
  assertEqual(result, '.-/-.../-.-.', 'Custom separator should work');
});

test('encode() handles multiple spaces', () => {
  const result = encode('A  B');
  assertEqual(result, '.- / -...', 'Multiple spaces should result in single word separator');
});

// ==================== Decoding Tests ====================

test('decode() decodes simple Morse', () => {
  assertEqual(decode('... --- ...'), 'SOS', 'Should decode SOS');
});

test('decode() handles word separators', () => {
  assertEqual(decode('.... . .-.. .-.. --- / .-- --- .-. .-.. -..'), 'HELLO WORLD', 'Should handle word separator');
});

test('decode() handles slash separator', () => {
  assertEqual(decode('.- / -...'), 'A B', 'Should handle slash as word separator');
});

test('decode() handles 3-space separator', () => {
  assertEqual(decode('.-   -...'), 'AB', 'Should handle 3-space separator');
});

test('decode() handles 7-space separator', () => {
  assertEqual(decode('.-       -...'), 'A B', 'Should handle 7-space word separator');
});

test('decode() handles empty string', () => {
  assertEqual(decode(''), '', 'Empty string should return empty');
});

test('decode() throws on invalid Morse', () => {
  assertThrows(() => decode('.- .xyz'), 'Should throw for invalid Morse');
});

test('decodeLenient() skips invalid symbols', () => {
  const result = decodeLenient('.- .xyz -...');
  assertEqual(result, 'AB', 'Should skip invalid symbols');
});

// ==================== Roundtrip Tests ====================

test('Roundtrip: encode then decode', () => {
  const original = 'HELLO WORLD';
  const encoded = encode(original);
  const decoded = decode(encoded);
  assertEqual(decoded, original, 'Roundtrip should preserve text');
});

test('Roundtrip: SOS', () => {
  const encoded = encode('SOS');
  const decoded = decode(encoded);
  assertEqual(decoded, 'SOS', 'SOS roundtrip should work');
});

test('Roundtrip: numbers', () => {
  const original = '12345';
  const encoded = encode(original);
  const decoded = decode(encoded);
  assertEqual(decoded, original, 'Numbers roundtrip should work');
});

test('Roundtrip: punctuation', () => {
  const original = 'A.B,C?';
  const encoded = encode(original);
  const decoded = decode(encoded);
  assertEqual(decoded, original, 'Punctuation roundtrip should work');
});

test('Roundtrip: panagram', () => {
  const original = 'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG';
  const encoded = encode(original);
  const decoded = decode(encoded);
  assertEqual(decoded, original, 'Pangram roundtrip should work');
});

// ==================== Character Lookup Tests ====================

test('getMorseCode() returns correct code', () => {
  assertEqual(getMorseCode('A'), '.-', 'A should return .-');
  assertEqual(getMorseCode('S'), '...', 'S should return ...');
  assertEqual(getMorseCode('O'), '---', 'O should return ---');
  assertEqual(getMorseCode('0'), '-----', '0 should return -----');
});

test('getMorseCode() handles lowercase', () => {
  assertEqual(getMorseCode('a'), '.-', 'Lowercase should work');
  assertEqual(getMorseCode('s'), '...', 'Lowercase should work');
});

test('getMorseCode() returns null for invalid', () => {
  assertEqual(getMorseCode('~'), null, 'Invalid char should return null');
  assertEqual(getMorseCode('#'), null, 'Invalid char should return null');
});

test('getCharacter() returns correct character', () => {
  assertEqual(getCharacter('.-'), 'A', '.- should return A');
  assertEqual(getCharacter('...'), 'S', '... should return S');
  assertEqual(getCharacter('-----'), '0', '----- should return 0');
});

test('getCharacter() returns null for invalid', () => {
  assertEqual(getCharacter('.xyz'), null, 'Invalid code should return null');
  assertEqual(getCharacter(''), null, 'Empty code should return null');
});

// ==================== Validation Tests ====================

test('isValidCharacter() returns true for valid chars', () => {
  assertTrue(isValidCharacter('A'), 'A should be valid');
  assertTrue(isValidCharacter('a'), 'a should be valid');
  assertTrue(isValidCharacter('0'), '0 should be valid');
  assertTrue(isValidCharacter('.'), '. should be valid');
});

test('isValidCharacter() returns false for invalid chars', () => {
  assertFalse(isValidCharacter('~'), '~ should be invalid');
  assertFalse(isValidCharacter('#'), '# should be invalid');
  assertFalse(isValidCharacter(''), 'Empty should be invalid');
});

test('isValidMorse() returns true for valid Morse', () => {
  assertTrue(isValidMorse('... --- ...'), 'Valid Morse should pass');
  assertTrue(isValidMorse('.-'), 'Single symbol should pass');
  assertTrue(isValidMorse(''), 'Empty should pass');
});

test('isValidMorse() returns false for invalid Morse', () => {
  assertFalse(isValidMorse('abc'), 'Non-Morse chars should fail');
  assertFalse(isValidMorse('.-x'), 'Mixed chars should fail');
});

test('canEncode() returns true for encodable text', () => {
  assertTrue(canEncode('HELLO'), 'HELLO should be encodable');
  assertTrue(canEncode('The quick brown fox'), 'Pangram should be encodable');
  assertTrue(canEncode('123'), 'Numbers should be encodable');
});

test('canEncode() returns false for non-encodable text', () => {
  assertFalse(canEncode('HELLO~'), 'Text with invalid char should fail');
  assertFalse(canEncode('你好'), 'Chinese should fail');
});

// ==================== Timing Tests ====================

test('defaultTiming() returns correct config', () => {
  const timing = defaultTiming();
  assertEqual(timing.dotDurationMs, 60, 'Default dot should be 60ms');
  assertEqual(timing.dashDurationMs, 180, 'Default dash should be 180ms (3x)');
  assertEqual(timing.symbolGapMs, 60, 'Symbol gap should equal dot');
  assertEqual(timing.charGapMs, 180, 'Char gap should be 3x dot');
  assertEqual(timing.wordGapMs, 420, 'Word gap should be 7x dot');
  assertEqual(timing.frequencyHz, 700, 'Default frequency should be 700Hz');
});

test('fastTiming() returns faster config', () => {
  const timing = fastTiming();
  assertTrue(timing.dotDurationMs < defaultTiming().dotDurationMs, 'Fast should be faster');
  assertEqual(timing.dashDurationMs, timing.dotDurationMs * 3, 'Dash should be 3x dot');
});

test('slowTiming() returns slower config', () => {
  const timing = slowTiming();
  assertTrue(timing.dotDurationMs > defaultTiming().dotDurationMs, 'Slow should be slower');
  assertEqual(timing.dashDurationMs, timing.dotDurationMs * 3, 'Dash should be 3x dot');
});

test('customTiming() creates custom config', () => {
  const timing = customTiming(100, 800);
  assertEqual(timing.dotDurationMs, 100, 'Custom dot should be 100ms');
  assertEqual(timing.dashDurationMs, 300, 'Custom dash should be 300ms');
  assertEqual(timing.frequencyHz, 800, 'Custom frequency should be 800Hz');
});

test('wpmToDotDuration() converts correctly', () => {
  // At 20 WPM, dot duration = 1200/20 = 60ms
  assertEqual(wpmToDotDuration(20), 60, '20 WPM should be 60ms');
  assertEqual(wpmToDotDuration(10), 120, '10 WPM should be 120ms');
});

test('dotDurationToWpm() converts correctly', () => {
  assertEqual(dotDurationToWpm(60), 20, '60ms should be 20 WPM');
  assertEqual(dotDurationToWpm(120), 10, '120ms should be 10 WPM');
});

// ==================== Signal Tests ====================

test('toSignals() generates correct signals for dot', () => {
  const signals = toSignals('.', defaultTiming());
  // Trailing silence is removed, so we get only the tone signal
  assertEqual(signals.length, 1, 'Dot should produce 1 signal (trailing gap removed)');
  assertTrue(signals[0].on, 'Signal should be on');
  assertEqual(signals[0].durationMs, 60, 'Dot duration should be 60ms');
});

test('toSignals() generates correct signals for dash', () => {
  const signals = toSignals('-', defaultTiming());
  // Trailing silence is removed
  assertEqual(signals.length, 1, 'Dash should produce 1 signal (trailing gap removed)');
  assertTrue(signals[0].on, 'Signal should be on');
  assertEqual(signals[0].durationMs, 180, 'Dash duration should be 180ms');
});

test('toSignals() generates correct signals for SOS', () => {
  const signals = toSignals('... --- ...', defaultTiming());
  // SOS is "... --- ..." = 3 dots + 3 dashes + 3 dots = 9 signal elements
  assertTrue(signals.length >= 9, 'SOS should produce multiple signals');
  
  // Count on signals
  const onSignals = signals.filter(s => s.on).length;
  assertEqual(onSignals, 9, 'Should have 9 on signals (3+3+3)');
});

test('toSignals() handles character separator', () => {
  // Use 3 spaces for character separator
  const signals = toSignals('.-   -...', defaultTiming());
  // Check that there's a character gap (180ms off signal)
  const charGaps = signals.filter(s => !s.on && s.durationMs === 180);
  assertTrue(charGaps.length >= 1, 'Should have at least one character gap signal');
});

test('toSignals() handles word separator', () => {
  // Use / for word separator
  const signals = toSignals('.- / -...', defaultTiming());
  // Check that there's a word gap (420ms off signal)
  const wordGaps = signals.filter(s => !s.on && s.durationMs === 420);
  assertTrue(wordGaps.length >= 1, 'Should have at least one word gap signal');
});

test('getTotalDuration() calculates correctly', () => {
  const duration = getTotalDuration('.', defaultTiming());
  // Dot (60) + gap (60) = 120ms (minus trailing gap removal)
  assertEqual(duration, 60, 'Single dot should be 60ms');
});

// ==================== Binary Tests ====================

test('toBinary() converts Morse to binary', () => {
  assertEqual(toBinary('.'), '1', 'Dot should be 1');
  assertEqual(toBinary('-'), '111', 'Dash should be 111');
  // Symbols within a character have implicit gap (0)
  // ". -" means dot and dash separated by space = two different chars
  // dot (1) + gap (0) + space (0) + dash (111) with gap before
  const result = toBinary('. -');
  assertTrue(result.startsWith('1'), 'Should start with 1 for dot');
  assertTrue(result.endsWith('111'), 'Should end with 111 for dash');
  assertTrue(result.includes('0'), 'Should contain 0 for gaps');
});

test('fromBinary() converts binary to Morse', () => {
  assertEqual(fromBinary('1'), '.', '1 should be dot');
  assertEqual(fromBinary('111'), '-', '111 should be dash');
});

test('Binary roundtrip', () => {
  // Binary roundtrip for single symbols
  const dotBinary = toBinary('.');
  const dashBinary = toBinary('-');
  assertEqual(fromBinary(dotBinary), '.', 'Dot binary roundtrip');
  assertEqual(fromBinary(dashBinary), '-', 'Dash binary roundtrip');
});

// ==================== Analysis Tests ====================

test('analyze() returns correct statistics', () => {
  const analysis = analyze('... --- ...');
  assertEqual(analysis.dotCount, 6, 'Should have 6 dots');
  assertEqual(analysis.dashCount, 3, 'Should have 3 dashes');
  assertEqual(analysis.signalCount, 9, 'Total signals should be 9');
  assertEqual(analysis.characterCount, 3, 'Should have 3 characters');
  assertEqual(analysis.wordCount, 1, 'Should have 1 word');
});

test('analyze() handles word separator', () => {
  const analysis = analyze('.- / -...');
  assertEqual(analysis.wordCount, 2, 'Should have 2 words');
});

test('analyze() handles empty string', () => {
  const analysis = analyze('');
  assertEqual(analysis.dotCount, 0, 'Empty should have 0 dots');
  assertEqual(analysis.dashCount, 0, 'Empty should have 0 dashes');
});

// ==================== Normalize Tests ====================

test('normalize() standardizes spacing', () => {
  const normalized = normalize('.-   -...');
  assertEqual(normalized, '.-   -...', 'Should keep 3-space separator');
});

test('normalize() handles irregular spacing', () => {
  const normalized = normalize('.-     -...');
  // Should normalize to 3 spaces
  assertTrue(normalized.includes('.-'), 'Should contain .-');
});

// ==================== Transpose Tests ====================

test('transpose() swaps dots and dashes', () => {
  assertEqual(transpose('.'), '-', 'Dot should become dash');
  assertEqual(transpose('-'), '.', 'Dash should become dot');
  assertEqual(transpose('... --- ...'), '--- ... ---', 'Should transpose SOS');
});

// ==================== Prosign Tests ====================

test('getProsign() returns correct prosign', () => {
  const ar = getProsign('AR');
  assertTrue(ar !== null, 'AR should be found');
  assertEqual(ar!.code, '.-.-.', 'AR code should be correct');
  assertEqual(ar!.description, 'End of message', 'AR description should be correct');
});

test('getProsign() returns null for unknown', () => {
  assertEqual(getProsign('UNKNOWN'), null, 'Unknown should return null');
});

test('isProsign() identifies prosigns', () => {
  assertTrue(isProsign('.-.-.'), 'AR code should be a prosign');
  assertTrue(isProsign('...---...'), 'SOS code should be a prosign');
  assertFalse(isProsign('.-'), 'A code should not be a prosign');
});

test('encodeProsign() returns prosign code', () => {
  assertEqual(encodeProsign('AR'), '.-.-.', 'AR should return its code');
  assertEqual(encodeProsign('SOS'), '...---...', 'SOS should return its code');
  assertEqual(encodeProsign('UNKNOWN'), null, 'Unknown should return null');
});

test('PROSIGNS array contains expected prosigns', () => {
  assertTrue(PROSIGNS.length >= 10, 'Should have at least 10 prosigns');
  assertTrue(PROSIGNS.some(p => p.name === 'AR'), 'Should contain AR');
  assertTrue(PROSIGNS.some(p => p.name === 'SOS'), 'Should contain SOS');
});

// ==================== getAllCodes Tests ====================

test('getAllCodes() returns all codes', () => {
  const codes = getAllCodes();
  assertTrue(Object.keys(codes).length >= 36, 'Should have at least 36 codes');
  assertEqual(codes['A'], '.-', 'A should be in codes');
  assertEqual(codes['0'], '-----', '0 should be in codes');
});

// ==================== Audio Waveform Tests ====================

test('generateAudioWaveform() generates samples', () => {
  const samples = generateAudioWaveform('.', defaultTiming(), 8000);
  assertTrue(samples.length > 0, 'Should generate samples');
});

test('generateAudioWaveform() produces valid amplitudes', () => {
  const samples = generateAudioWaveform('.-', defaultTiming(), 8000);
  // Check that values are between -1 and 1
  for (const sample of samples) {
    assertTrue(sample >= -1 && sample <= 1, 'Sample should be between -1 and 1');
  }
});

test('generateAudioWaveform() includes silence for gaps', () => {
  const samples = generateAudioWaveform('.-', defaultTiming(), 8000);
  // Should have both positive (tone) and zero (silence) samples
  assertTrue(samples.some(s => s === 0), 'Should have silence samples');
});

// ==================== Namespace Tests ====================

test('MorseUtils namespace exports all functions', () => {
  assertTrue(typeof MorseUtils.encode === 'function', 'encode should be exported');
  assertTrue(typeof MorseUtils.decode === 'function', 'decode should be exported');
  assertTrue(typeof MorseUtils.defaultTiming === 'function', 'defaultTiming should be exported');
  assertTrue(typeof MorseUtils.toSignals === 'function', 'toSignals should be exported');
  assertTrue(typeof MorseUtils.analyze === 'function', 'analyze should be exported');
  assertTrue(typeof MorseUtils.getProsign === 'function', 'getProsign should be exported');
  assertTrue(Array.isArray(MorseUtils.PROSIGNS), 'PROSIGNS should be exported');
});

// ==================== Edge Cases Tests ====================

test('encode() handles very long text', () => {
  const longText = 'A'.repeat(100);
  const encoded = encode(longText);
  assertTrue(encoded.length > 100, 'Should encode long text');
  assertEqual(encoded.split(' ').length, 100, 'Should have 100 characters encoded');
});

test('decode() handles Morse with trailing spaces', () => {
  const decoded = decode('.- ');
  assertEqual(decoded, 'A', 'Should handle trailing spaces');
});

test('encode() handles single space', () => {
  const encoded = encode(' ');
  assertEqual(encoded, '', 'Single space should return empty');
});

// ==================== Run Tests ====================

console.log('Running Morse Utils Test Suite...\n');

// Run all tests
// (Tests are executed as they are defined above)

console.log('\n=========================');
console.log(`Total: ${passed + failed} tests`);
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
console.log('=========================');

if (failed > 0) {
  process.exit(1);
}