# QR Code Generator (qr_code_utils)

A pure JavaScript QR code generator with zero external dependencies.

## Features

- ✅ Pure JavaScript implementation (no dependencies)
- ✅ Supports QR Code versions 1-10 (21x21 to 53x53 modules)
- ✅ Multiple encoding modes: Numeric, Alphanumeric, Byte (UTF-8)
- ✅ Four error correction levels: L (7%), M (15%), Q (25%), H (30%)
- ✅ Automatic version selection
- ✅ Automatic mask pattern optimization
- ✅ Multiple output formats: ASCII, SVG, Array, Binary
- ✅ Reed-Solomon error correction
- ✅ Customizable colors and styling

## Installation

Simply copy `mod.js` to your project. No npm dependencies required.

```javascript
const { generateQR, generateQRASCII, generateQRSVG } = require('./qr_code_utils/mod.js');
```

## Quick Start

```javascript
const { generateQRASCII, generateQRSVG } = require('./qr_code_utils/mod.js');

// Generate ASCII QR code
const ascii = generateQRASCII('Hello, World!');
console.log(ascii);

// Generate SVG
const svg = generateQRSVG('https://example.com', { size: 200 });
```

## API

### generateQR(data, options)

Creates a QRCode object.

```javascript
const qr = generateQR('Your data here', {
  ecLevel: 'M',    // L, M, Q, or H
  version: null,   // 1-10, or null for auto
  mask: null       // 0-7, or null for auto
});
```

### generateQRASCII(data, options)

Generates ASCII art QR code.

```javascript
const ascii = generateQRASCII('Hello', {
  white: '██',     // White module character
  black: '  ',     // Black module character
  border: true     // Include border
});
```

### generateQRSVG(data, options)

Generates SVG QR code.

```javascript
const svg = generateQRSVG('Hello', {
  size: 300,        // SVG size in pixels
  margin: 4,        // Quiet zone margin
  dark: '#000000',  // Dark module color
  light: '#ffffff'  // Light module color
});
```

### generateQRArray(data, options)

Returns 2D boolean array of modules.

```javascript
const arr = generateQRArray('Hello');
// arr[row][col] === true means dark module
```

## QRCode Class Methods

```javascript
const qr = generateQR('Hello');

qr.toASCII(options);      // ASCII art string
qr.toSVG(options);        // SVG string
qr.toArray();             // 2D boolean array
qr.toBinary();            // Binary string
qr.getSize();             // Module count per side
qr.getVersion();          // QR version (1-10)
qr.getECLevel();          // Error correction level
qr.getMask();             // Mask pattern used
```

## Examples

### URL Encoding

```javascript
generateQRSVG('https://github.com', { size: 200 });
```

### WiFi Network

```javascript
generateQRASCII('WIFI:T:WPA;S:MyNetwork;P:password123;;');
```

### Contact Card (vCard)

```javascript
const vCard = `BEGIN:VCARD
VERSION:3.0
N:Doe;John
FN:John Doe
TEL:+1234567890
EMAIL:john@example.com
END:VCARD`;

generateQRSVG(vCard, { ecLevel: 'H' });  // High EC for resilience
```

### Email

```javascript
generateQR('mailto:test@example.com?subject=Hello');
```

### Batch Generation

```javascript
const urls = ['https://site1.com', 'https://site2.com'];
urls.forEach(url => {
  const svg = generateQRSVG(url);
  // Save to file or send to client
});
```

## Error Correction Levels

| Level | Recovery | Use Case |
|-------|----------|----------|
| L | ~7% | Clean environments |
| M | ~15% | General purpose (default) |
| Q | ~25% | Some damage expected |
| H | ~30% | High damage, logos, overlays |

## Data Capacity (Version 10, M level)

| Mode | Characters |
|------|------------|
| Numeric | 271 |
| Alphanumeric | 164 |
| Byte | 113 |

## Running Tests

```bash
node test.js
```

## Running Examples

```bash
node examples.js
```

## Limitations

- Versions 1-10 supported (larger QR codes not yet implemented)
- Kanji mode not implemented
- Structured append not supported
- No decoding capability (encode only)

## License

MIT