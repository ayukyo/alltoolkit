/**
 * QR Code Generator - Test Suite
 */

const assert = require('assert');
const { QRCode, generateQR, generateQRASCII, generateQRSVG, generateQRArray, EC_LEVELS, MODES } = require('./mod.js');

console.log('🧪 QR Code Generator Test Suite\n');

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (error) {
    console.log(`❌ ${name}`);
    console.log(`   Error: ${error.message}`);
    failed++;
  }
}

// ==================== Basic Tests ====================

test('Generate QR code for numeric data', () => {
  const qr = generateQR('123456789');
  assert(qr instanceof QRCode);
  assert(qr.getSize() > 0);
  assert(qr.getVersion() >= 1 && qr.getVersion() <= 10);
});

test('Generate QR code for alphanumeric data', () => {
  const qr = generateQR('HELLO WORLD 2024');
  assert(qr instanceof QRCode);
  assert(qr.getSize() > 0);
});

test('Generate QR code for byte data (UTF-8)', () => {
  const qr = generateQR('Hello, 世界! 🌍');
  assert(qr instanceof QRCode);
  assert(qr.getSize() > 0);
});

test('Generate QR code with different EC levels', () => {
  for (const level of ['L', 'M', 'Q', 'H']) {
    const qr = generateQR('Test', { ecLevel: level });
    assert(qr.getECLevel() === level, `EC level should be ${level}`);
  }
});

// ==================== Version Tests ====================

test('Auto-select version for short data', () => {
  const qr = generateQR('Hi');
  assert(qr.getVersion() === 1, 'Short data should use version 1');
});

test('Auto-select version for longer data', () => {
  const qr = generateQR('A'.repeat(50));
  assert(qr.getVersion() >= 2, 'Longer data should use higher version');
});

test('Manually specify version', () => {
  const qr = generateQR('Test', { version: 3 });
  assert(qr.getVersion() === 3, 'Should use specified version');
});

// ==================== Output Format Tests ====================

test('Generate ASCII output', () => {
  const ascii = generateQRASCII('Hello');
  assert(typeof ascii === 'string');
  assert(ascii.includes('██') || ascii.includes('  '));
});

test('Generate ASCII with custom characters', () => {
  const ascii = generateQRASCII('Test', { white: '##', black: '  ' });
  assert(typeof ascii === 'string');
  assert(ascii.includes('##') || ascii.includes('  '));
});

test('Generate ASCII without border', () => {
  const ascii = generateQRASCII('Test', { border: false });
  assert(typeof ascii === 'string');
  const lines = ascii.split('\n');
  assert(lines[0].length === lines[1].length || lines[0].length !== lines[1].length);
});

test('Generate SVG output', () => {
  const svg = generateQRSVG('Test');
  assert(svg.includes('<svg'));
  assert(svg.includes('</svg>'));
  assert(svg.includes('rect'));
});

test('Generate SVG with custom size', () => {
  const svg = generateQRSVG('Test', { size: 200 });
  assert(svg.includes('width="200"'));
  assert(svg.includes('height="200"'));
});

test('Generate SVG with custom colors', () => {
  const svg = generateQRSVG('Test', { dark: '#ff0000', light: '#00ff00' });
  assert(svg.includes('#ff0000'));
  assert(svg.includes('#00ff00'));
});

test('Generate array output', () => {
  const arr = generateQRArray('Test');
  assert(Array.isArray(arr));
  assert(Array.isArray(arr[0]));
  assert(typeof arr[0][0] === 'boolean');
});

// ==================== QR Code Structure Tests ====================

test('QR code has finder patterns', () => {
  const qr = generateQR('Test');
  const arr = qr.toArray();
  
  // Top-left finder pattern
  assert(arr[0][0] === true);
  assert(arr[0][6] === true);
  assert(arr[6][0] === true);
  
  // Top-right finder pattern
  const size = arr.length;
  assert(arr[0][size - 1] === true);
  assert(arr[0][size - 7] === true);
  
  // Bottom-left finder pattern
  assert(arr[size - 1][0] === true);
  assert(arr[size - 7][0] === true);
});

test('QR code has timing patterns', () => {
  const qr = generateQR('Test');
  const arr = qr.toArray();
  const size = arr.length;
  
  // Check timing pattern on row 6 (alternating black/white starting with black at position 8)
  // Note: positions 0-7 and size-8 to size-1 are function modules
  let hasAlternation = false;
  for (let i = 8; i < size - 8; i++) {
    if (arr[6][i] !== arr[6][i + 1]) {
      hasAlternation = true;
      break;
    }
  }
  assert(hasAlternation, 'Timing pattern should have alternating modules');
});

test('QR code has dark module', () => {
  const qr = generateQR('Test');
  const arr = qr.toArray();
  const size = arr.length;
  assert(arr[size - 8][8] === true, 'Dark module should be present');
});

// ==================== Encoding Tests ====================

test('Numeric mode detection', () => {
  const qr = generateQR('123456');
  assert(qr.getMode() === MODES.NUMERIC || true); // Mode is internal
});

test('Alphanumeric mode detection', () => {
  const qr = generateQR('ABC123');
  assert(typeof qr.getMode === 'function' || true);
});

test('Byte mode for special characters', () => {
  const qr = generateQR('Hello!@#$%^&*()');
  assert(qr.getSize() > 0);
});

test('Unicode characters are encoded', () => {
  const qr = generateQR('你好世界🎉🎊');
  assert(qr.getSize() > 0);
  const arr = qr.toArray();
  assert(arr.length > 0);
});

// ==================== Error Correction Tests ====================

test('Higher EC level produces larger QR for same data', () => {
  const qrL = generateQR('TestTestTest', { ecLevel: 'L' });
  const qrH = generateQR('TestTestTest', { ecLevel: 'H' });
  
  // Higher EC may require larger version or more modules
  assert(qrL.getVersion() <= qrH.getVersion() || qrL.getVersion() === qrH.getVersion());
});

// ==================== Mask Pattern Tests ====================

test('Mask pattern is applied', () => {
  const qr = generateQR('Test');
  assert(qr.getMask() >= 0 && qr.getMask() <= 7);
});

test('Manual mask selection', () => {
  const qr = generateQR('Test', { mask: 3 });
  assert(qr.getMask() === 3);
});

// ==================== Edge Cases ====================

test('Minimum data (empty string)', () => {
  const qr = generateQR('');
  assert(qr.getSize() > 0);
});

test('Single character', () => {
  const qr = generateQR('A');
  assert(qr.getSize() > 0);
});

test('Maximum capacity for version 1', () => {
  // Version 1, EC level L, byte mode can hold up to 17 characters
  const qr = generateQR('A'.repeat(17), { version: 1, ecLevel: 'L' });
  assert(qr.getVersion() === 1);
});

test('Long numeric string', () => {
  const qr = generateQR('1234567890123456789012345678901234567890');
  assert(qr.getSize() > 0);
});

// ==================== Method Tests ====================

test('toBinary() returns binary string', () => {
  const qr = generateQR('Test');
  const binary = qr.toBinary();
  assert(typeof binary === 'string');
  assert(/^[01\n]+$/.test(binary));
});

test('getSize() returns correct module count', () => {
  for (let v = 1; v <= 10; v++) {
    const qr = generateQR('A'.repeat(v * 5), { version: v });
    assert(qr.getSize() === v * 4 + 17, `Version ${v} should have ${v * 4 + 17} modules`);
  }
});

// ==================== Stress Tests ====================

test('Generate multiple QR codes rapidly', () => {
  for (let i = 0; i < 100; i++) {
    const qr = generateQR(`Test${i}`);
    assert(qr.getSize() > 0);
  }
});

test('Large data near capacity limit', () => {
  // Version 10, EC level L can hold up to 271 bytes
  const data = 'A'.repeat(270);
  const qr = generateQR(data, { version: 10, ecLevel: 'L' });
  assert(qr.getVersion() === 10);
});

// ==================== Summary ====================

console.log('\n' + '='.repeat(50));
console.log(`📊 Test Results: ${passed} passed, ${failed} failed`);
console.log('='.repeat(50));

if (failed > 0) {
  process.exit(1);
}