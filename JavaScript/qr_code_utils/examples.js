/**
 * QR Code Generator - Usage Examples
 */

const { 
  QRCode, 
  generateQR, 
  generateQRASCII, 
  generateQRSVG, 
  generateQRArray,
  EC_LEVELS 
} = require('./mod.js');
const fs = require('fs');

console.log('📱 QR Code Generator Examples\n');

// ==================== Basic Usage ====================

console.log('1. Basic QR Code Generation');
console.log('-'.repeat(40));

// Simple text QR code
const qr1 = generateQR('Hello, World!');
console.log(`   Version: ${qr1.getVersion()}`);
console.log(`   Size: ${qr1.getSize()}x${qr1.getSize()} modules`);
console.log(`   EC Level: ${qr1.getECLevel()}`);
console.log(`   Mask: ${qr1.getMask()}`);

// ==================== ASCII Output ====================

console.log('\n2. ASCII Art Output');
console.log('-'.repeat(40));

const qr2 = generateQRASCII('QR Code!');
console.log(qr2);

// Custom ASCII characters
console.log('\n   With custom characters:');
const qr2Custom = generateQRASCII('Hi', { 
  white: '░░', 
  black: '██',
  border: false 
});
console.log(qr2Custom);

// ==================== SVG Output ====================

console.log('\n3. SVG Output');
console.log('-'.repeat(40));

const qr3 = generateQRSVG('https://example.com', { 
  size: 200,
  dark: '#000000',
  light: '#ffffff',
  margin: 4
});

console.log('   Generated SVG for URL:');
console.log('   ' + qr3.substring(0, 100) + '...');

// Save to file
fs.writeFileSync('example-qr.svg', qr3);
console.log('   ✅ Saved to example-qr.svg');

// ==================== Different Data Types ====================

console.log('\n4. Different Data Types');
console.log('-'.repeat(40));

// Numeric only
const numQR = generateQR('1234567890');
console.log(`   Numeric: '1234567890' → Version ${numQR.getVersion()}`);

// Alphanumeric
const alphaQR = generateQR('HELLO-WORLD-2024');
console.log(`   Alphanumeric: 'HELLO-WORLD-2024' → Version ${alphaQR.getVersion()}`);

// URL
const urlQR = generateQR('https://github.com/ayukyo/alltoolkit');
console.log(`   URL: → Version ${urlQR.getVersion()}`);

// Email
const emailQR = generateQR('mailto:test@example.com?subject=Hello');
console.log(`   Email: → Version ${emailQR.getVersion()}`);

// WiFi (using string format)
const wifiQR = generateQR('WIFI:T:WPA;S:MyNetwork;P:password123;;');
console.log(`   WiFi: → Version ${wifiQR.getVersion()}`);

// ==================== Error Correction Levels ====================

console.log('\n5. Error Correction Levels');
console.log('-'.repeat(40));

const data = 'Sample Text';
for (const level of ['L', 'M', 'Q', 'H']) {
  const qr = generateQR(data, { ecLevel: level });
  const capacity = level === 'L' ? '~7%' : level === 'M' ? '~15%' : level === 'Q' ? '~25%' : '~30%';
  console.log(`   Level ${level}: Version ${qr.getVersion()}, Can recover ${capacity} of data`);
}

// ==================== Version Control ====================

console.log('\n6. Manual Version Selection');
console.log('-'.repeat(40));

const qr6 = generateQR('Short', { version: 4 });
console.log(`   Forced Version 4: Size ${qr6.getSize()}x${qr6.getSize()} modules`);

// ==================== Mask Pattern Selection ====================

console.log('\n7. Mask Pattern Selection');
console.log('-'.repeat(40));

const qr7auto = generateQR('Test');
console.log(`   Auto-selected mask: ${qr7auto.getMask()}`);

const qr7manual = generateQR('Test', { mask: 2 });
console.log(`   Manual mask 2: ${qr7manual.getMask()}`);

// ==================== Array Output ====================

console.log('\n8. Array Output (for custom rendering)');
console.log('-'.repeat(40));

const qr8 = generateQRArray('AB');
console.log(`   Boolean array: ${qr8.length}x${qr8[0].length}`);
console.log('   First row (partial):', qr8[0].slice(0, 10).map(b => b ? '1' : '0').join(''), '...');

// ==================== Colorful QR Codes ====================

console.log('\n9. Colorful SVG QR Codes');
console.log('-'.repeat(40));

const colorfulQR = generateQRSVG('Colorful!', {
  size: 250,
  dark: '#3498db',
  light: '#ecf0f1'
});
fs.writeFileSync('colorful-qr.svg', colorfulQR);
console.log('   ✅ Saved colorful QR to colorful-qr.svg');

// ==================== Batch Generation ====================

console.log('\n10. Batch Generation Example');
console.log('-'.repeat(40));

const urls = [
  'https://google.com',
  'https://github.com',
  'https://stackoverflow.com'
];

urls.forEach((url, i) => {
  const svg = generateQRSVG(url, { size: 150 });
  fs.writeFileSync(`batch-qr-${i + 1}.svg`, svg);
  console.log(`   ✅ Generated batch-qr-${i + 1}.svg`);
});

// ==================== QR Code for Contact ====================

console.log('\n11. Contact Card (vCard)');
console.log('-'.repeat(40));

const vCard = `BEGIN:VCARD
VERSION:3.0
N:Doe;John
FN:John Doe
TEL:+1234567890
EMAIL:john@example.com
END:VCARD`;

const contactQR = generateQR(vCard, { ecLevel: 'M' });
console.log(`   Contact card: Version ${contactQR.getVersion()}`);

// ==================== Size Comparison ====================

console.log('\n12. Size vs Data Length');
console.log('-'.repeat(40));

for (let len = 5; len <= 100; len += 20) {
  const qr = generateQR('A'.repeat(len));
  console.log(`   ${len} chars → Version ${qr.getVersion()} (${qr.getSize()}x${qr.getSize()})`);
}

// ==================== Cleanup ====================

console.log('\n' + '='.repeat(50));
console.log('✅ All examples completed!');
console.log('   Generated files: example-qr.svg, colorful-qr.svg, batch-qr-*.svg');

// Clean up example files
fs.unlinkSync('example-qr.svg');
fs.unlinkSync('colorful-qr.svg');
for (let i = 1; i <= 3; i++) {
  fs.unlinkSync(`batch-qr-${i}.svg`);
}
console.log('   🧹 Cleaned up example files');