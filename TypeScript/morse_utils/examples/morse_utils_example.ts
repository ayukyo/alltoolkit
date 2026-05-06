/**
 * Morse Code Utilities Examples
 * 
 * Demonstrates various features of the Morse code utilities module.
 * Run with: npx ts-node morse_utils_example.ts
 */

import {
  encode,
  decode,
  getMorseCode,
  getCharacter,
  isValidMorse,
  isValidCharacter,
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
  PROSIGNS,
  MorseUtils,
} from '../mod';

console.log('========================================');
console.log('  Morse Code Utilities Examples');
console.log('========================================\n');

// ==================== Basic Encoding ====================

console.log('--- Basic Encoding ---');
console.log('SOS:', encode('SOS'));
console.log('HELLO:', encode('HELLO'));
console.log('HELLO WORLD:', encode('HELLO WORLD'));
console.log('The quick brown fox:', encode('The quick brown fox'));
console.log('');

// ==================== Numbers and Punctuation ====================

console.log('--- Numbers and Punctuation ---');
console.log('123:', encode('123'));
console.log('Email:', encode('test@example.com'));
console.log('Question:', encode('What?'));
console.log('Phone:', encode('123-456-7890'));
console.log('');

// ==================== Basic Decoding ====================

console.log('--- Basic Decoding ---');
console.log('... --- ... =>', decode('... --- ...'));
console.log('.... . .-.. .-.. --- =>', decode('.... . .-.. .-.. ---'));
console.log('.- / -... =>', decode('.- / -...'));
console.log('');

// ==================== Roundtrip ====================

console.log('--- Roundtrip (Encode -> Decode) ---');
const original = 'HELLO WORLD';
const encoded = encode(original);
const decoded = decode(encoded);
console.log(`Original: "${original}"`);
console.log(`Encoded: "${encoded}"`);
console.log(`Decoded: "${decoded}"`);
console.log('Match:', decoded === original ? '✓ Yes' : '✗ No');
console.log('');

// ==================== Character Lookup ====================

console.log('--- Character Lookup ---');
console.log('A =>', getMorseCode('A'));
console.log('S =>', getMorseCode('S'));
console.log('0 =>', getMorseCode('0'));
console.log('. =>', getMorseCode('.'));
console.log('');
console.log('.- =>', getCharacter('.-'));
console.log('... =>', getCharacter('...'));
console.log('----- =>', getCharacter('-----'));
console.log('');

// ==================== Validation ====================

console.log('--- Validation ---');
console.log('isValidCharacter("A"):', isValidCharacter('A'));
console.log('isValidCharacter("~"):', isValidCharacter('~'));
console.log('isValidMorse("... --- ..."):', isValidMorse('... --- ...'));
console.log('isValidMorse("abc"):', isValidMorse('abc'));
console.log('canEncode("HELLO"):', canEncode('HELLO'));
console.log('canEncode("你好"):', canEncode('你好'));
console.log('');

// ==================== Timing Configuration ====================

console.log('--- Timing Configuration ---');
const defaultTime = defaultTiming();
console.log('Default timing:');
console.log(`  Dot: ${defaultTime.dotDurationMs}ms`);
console.log(`  Dash: ${defaultTime.dashDurationMs}ms`);
console.log(`  Char gap: ${defaultTime.charGapMs}ms`);
console.log(`  Word gap: ${defaultTime.wordGapMs}ms`);
console.log(`  Frequency: ${defaultTime.frequencyHz}Hz`);
console.log('');

const fastTime = fastTiming();
console.log(`Fast timing dot: ${fastTime.dotDurationMs}ms`);

const slowTime = slowTiming();
console.log(`Slow timing dot: ${slowTime.dotDurationMs}ms`);

const custom = customTiming(50, 800);
console.log(`Custom timing (50ms, 800Hz): dot=${custom.dotDurationMs}ms, freq=${custom.frequencyHz}Hz`);
console.log('');

// ==================== WPM Conversion ====================

console.log('--- WPM Conversion ---');
console.log('20 WPM =>', wpmToDotDuration(20), 'ms dot duration');
console.log('60ms dot =>', dotDurationToWpm(60), 'WPM');
console.log('');

// ==================== Signal Generation ====================

console.log('--- Signal Generation ---');
const signals = toSignals('SOS', defaultTiming());
console.log('SOS signals:');
signals.forEach((s, i) => {
  console.log(`  ${i}: ${s.on ? 'ON' : 'OFF'} for ${s.durationMs}ms`);
});
console.log('');

console.log(`Total duration for SOS: ${getTotalDuration('... --- ...', defaultTiming())}ms`);
console.log('');

// ==================== Binary Representation ====================

console.log('--- Binary Representation ---');
console.log('. =>', toBinary('.'));
console.log('- =>', toBinary('-'));
console.log('.- =>', toBinary('.-'));
console.log('SOS binary:', toBinary('... --- ...'));
console.log('');
console.log('1 =>', fromBinary('1'));
console.log('111 =>', fromBinary('111'));
console.log('');

// ==================== Analysis ====================

console.log('--- Analysis ---');
const analysis = analyze('... --- ...');
console.log('SOS analysis:');
console.log(`  Dots: ${analysis.dotCount}`);
console.log(`  Dashes: ${analysis.dashCount}`);
console.log(`  Total signals: ${analysis.signalCount}`);
console.log(`  Characters: ${analysis.characterCount}`);
console.log(`  Words: ${analysis.wordCount}`);
console.log('');

const analysis2 = analyze('.... . .-.. .-.. --- / .-- --- .-. .-.. -..');
console.log('HELLO WORLD analysis:');
console.log(`  Words: ${analysis2.wordCount}`);
console.log(`  Characters: ${analysis2.characterCount}`);
console.log('');

// ==================== Normalize and Transpose ====================

console.log('--- Normalize and Transpose ---');
console.log('Normalize ".-   -...":', normalize('.-   -...'));
console.log('Transpose ".-":', transpose('.-'));
console.log('Transpose SOS:', transpose('... --- ...'));
console.log('');

// ==================== Prosigns ====================

console.log('--- Prosigns ---');
console.log('Available prosigns:');
PROSIGNS.forEach(p => {
  console.log(`  ${p.name}: ${p.code} - "${p.description}"`);
});
console.log('');

console.log('getProsign("AR"):', getProsign('AR'));
console.log('isProsign(".-.-."):', isProsign('.-.-.'));
console.log('encodeProsign("SOS"):', encodeProsign('SOS'));
console.log('');

// ==================== Audio Waveform ====================

console.log('--- Audio Waveform Generation ---');
const waveform = generateAudioWaveform('.-', defaultTiming(), 8000);
console.log(`Generated ${waveform.length} samples for ".-" at 8kHz`);
console.log(`Min amplitude: ${Math.min(...waveform).toFixed(4)}`);
console.log(`Max amplitude: ${Math.max(...waveform).toFixed(4)}`);
console.log(`Has silence: ${waveform.some(s => s === 0)}`);
console.log('');

// ==================== All Codes ====================

console.log('--- All Supported Characters ---');
const allCodes = getAllCodes();
const letters = Object.entries(allCodes)
  .filter(([k]) => k.length === 1 && k >= 'A' && k <= 'Z')
  .map(([k, v]) => `${k}: ${v}`);
console.log('Letters:', letters.join(', '));
console.log('');

const numbers = Object.entries(allCodes)
  .filter(([k]) => k >= '0' && k <= '9')
  .map(([k, v]) => `${k}: ${v}`);
console.log('Numbers:', numbers.join(', '));
console.log('');

// ==================== Namespace Usage ====================

console.log('--- MorseUtils Namespace ---');
console.log('MorseUtils.encode("ABC"):', MorseUtils.encode('ABC'));
console.log('MorseUtils.decode(".- -... -.-."):', MorseUtils.decode('.- -... -.-.'));
console.log('MorseUtils.analyze("..."):', MorseUtils.analyze('...'));
console.log('');

// ==================== Practical Examples ====================

console.log('--- Practical Examples ---');

// Emergency signal
console.log('Emergency SOS:', encode('SOS SOS SOS'));
console.log('');

// Coordinates (simplified)
console.log('Location:', encode('N 40 W 74'));
console.log('');

// Common phrases
const phrases = ['OK', 'YES', 'NO', 'HELP', 'STOP'];
console.log('Common phrases:');
phrases.forEach(p => {
  console.log(`  ${p}: ${encode(p)}`);
});
console.log('');

// Calculate transmission time for a message
const message = 'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG';
const messageMorse = encode(message);
const messageTime = getTotalDuration(messageMorse, defaultTiming());
console.log(`"${message}"`);
console.log(`Transmission time at 20 WPM: ${messageTime / 1000}s (${(messageTime / 60000).toFixed(2)} min)`);
console.log('');

console.log('========================================');
console.log('  Examples Complete');
console.log('========================================');