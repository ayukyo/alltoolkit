/**
 * AllToolkit - Morse Code Utilities Examples
 * ===========================================
 * Practical examples demonstrating morse_utils usage.
 */

const morse = require('../mod.js');

console.log('========================================');
console.log('Morse Code Utilities - Examples');
console.log('========================================\n');

// Example 1: Basic Encoding and Decoding
console.log('--- Example 1: Basic Encoding/Decoding ---');
const text = 'HELLO WORLD';
const encoded = morse.encode(text);
const decoded = morse.decode(encoded);

console.log(`Original: ${text}`);
console.log(`Encoded:  ${encoded}`);
console.log(`Decoded:  ${decoded}`);
console.log();

// Example 2: SOS Distress Signal
console.log('--- Example 2: SOS Distress Signal ---');
const sos = morse.encode('SOS');
const sosProsign = morse.encode('SOS', { charSeparator: '' }); // No gaps between chars
console.log(`SOS as text: ${sos}`);
console.log(`SOS prosign: ${sosProsign}`);
console.log();

// Example 3: Numbers and Punctuation
console.log('--- Example 3: Numbers and Punctuation ---');
console.log(`2024:     ${morse.encode('2024')}`);
console.log(`OK?:      ${morse.encode('OK?')}`);
console.log(`WAIT!     ${morse.encode('WAIT!')}`);
console.log();

// Example 4: Custom Symbols
console.log('--- Example 4: Custom Symbols ---');
const encoder = new morse.MorseEncoder({
  dotSymbol: '·',
  dashSymbol: '—'
});
console.log(`HELLO: ${encoder.encode('HELLO')}`);

const starEncoder = new morse.MorseEncoder({
  dotSymbol: '*',
  dashSymbol: '#'
});
console.log(`MORSE: ${starEncoder.encode('MORSE')}`);
console.log();

// Example 5: Speed Calculations
console.log('--- Example 5: Speed Calculations ---');
const generator = new morse.MorseSignalGenerator({ wpm: 15 });
console.log(`At 15 WPM:`);
console.log(`  Dot duration:    ${generator.getTiming().dot.toFixed(3)}s`);
console.log(`  Dash duration:   ${generator.getTiming().dash.toFixed(3)}s`);
console.log(`  Char gap:        ${generator.getTiming().interChar.toFixed(3)}s`);
console.log(`  Word gap:        ${generator.getTiming().wordSpace.toFixed(3)}s`);
console.log(`  HELLO duration:  ${generator.calculateDuration('HELLO').toFixed(3)}s`);

generator.setWpm(20);
console.log(`\nAt 20 WPM:`);
console.log(`  Dot duration:    ${generator.getTiming().dot.toFixed(3)}s`);
console.log(`  HELLO duration:  ${generator.calculateDuration('HELLO').toFixed(3)}s`);
console.log();

// Example 6: Visual Representation
console.log('--- Example 6: Visual Representation ---');
const visual = morse.toVisual('SOS', { unitWidth: 2 });
console.log(`SOS visual: ${visual}`);
console.log();

// Example 7: Statistics
console.log('--- Example 7: Statistics ---');
const stats = morse.getStats('THE QUICK BROWN FOX');
console.log(`Text:      ${stats.text}`);
console.log(`Morse:     ${stats.morse}`);
console.log(`Dots:      ${stats.dots}`);
console.log(`Dashes:    ${stats.dashes}`);
console.log(`Chars:     ${stats.characters}`);
console.log(`Words:     ${stats.words}`);
console.log(`Units:     ${stats.totalUnits}`);
console.log(`Dot/Dash:  ${stats.ratio}`);
console.log();

// Example 8: Signal Timing Pattern
console.log('--- Example 8: Signal Timing Pattern ---');
const pattern = generator.generateTimingPattern('HI');
console.log(`Timing pattern for "HI":`);
pattern.forEach(([state, duration], i) => {
  console.log(`  ${i + 1}. ${state.toUpperCase()}: ${duration.toFixed(3)}s`);
});
console.log();

// Example 9: Beep Schedule
console.log('--- Example 9: Beep Schedule ---');
const schedule = generator.generateBeepSchedule('ABC');
console.log(`Beep schedule for "ABC":`);
schedule.forEach((beep, i) => {
  console.log(`  ${i + 1}. ${beep.type.toUpperCase()}: ${beep.start.toFixed(3)}s - ${beep.end.toFixed(3)}s`);
});
console.log();

// Example 10: Practice Generator
console.log('--- Example 10: Practice Generator ---');
const practice = morse.generatePractice({
  chars: ['A', 'E', 'S', 'O', 'T', 'N'],
  count: 5
});
console.log(`Random practice items:`);
practice.forEach(item => {
  console.log(`  ${item.char} → ${item.morse}`);
});
console.log();

// Example 11: Roundtrip Test
console.log('--- Example 11: Roundtrip Test ---');
const testTexts = ['MORSE CODE', '2024', 'SOS HELP', 'I LOVE YOU'];
for (const test of testTexts) {
  const enc = morse.encode(test);
  const dec = morse.decode(enc);
  const match = dec === test ? '✓' : '✗';
  console.log(`  ${match} "${test}" → "${enc}" → "${dec}"`);
}
console.log();

// Example 12: Character Lookup
console.log('--- Example 12: Character Lookup ---');
console.log(`  A: ${morse.getMorseCode('A')}`);
console.log(`  E: ${morse.getMorseCode('E')}`);
console.log(`  S: ${morse.getMorseCode('S')}`);
console.log(`  O: ${morse.getMorseCode('O')}`);
console.log(`  T: ${morse.getMorseCode('T')}`);
console.log();

// Example 13: Validation
console.log('--- Example 13: Validation ---');
console.log(`  "HELLO" valid?    ${morse.isValidText('HELLO')}`);
console.log(`  "HELLO#" valid?   ${morse.isValidText('HELLO#')}`);
console.log(`  ".- -..." valid?  ${morse.isValidMorse('.- -...')}`);
console.log(`  ".-......" valid? ${morse.isValidMorse('.-......')}`);
console.log();

// Example 14: Time Estimation
console.log('--- Example 14: Time Estimation ---');
const message = 'CQ CQ CQ DE TEST TEST TEST K';
for (const wpm of [10, 15, 20, 25]) {
  const time = morse.estimateTime(message, wpm);
  console.log(`  ${wpm} WPM: ${time.toFixed(2)}s for "${message}"`);
}
console.log();

// Example 15: Binary Pattern
console.log('--- Example 15: Binary Pattern ---');
const binary = generator.generateBinaryPattern('E', 3); // E is a single dot
console.log(`Binary for "E" (dot): ${binary}`);
console.log(`Expected: 111000 (3 samples on, 3 off)`);
console.log();

console.log('========================================');
console.log('All examples completed successfully!');
console.log('========================================');