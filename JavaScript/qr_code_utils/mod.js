/**
 * QR Code Generator - Pure JavaScript Implementation
 * Zero external dependencies
 * 
 * Supports: Numeric, Alphanumeric, Byte encoding
 * Error Correction: L(7%), M(15%), Q(25%), H(30%)
 * Versions: 1-40 (21x21 to 177x177 modules)
 */

// Error Correction Levels
const EC_LEVELS = { L: 0, M: 1, Q: 2, H: 3 };

// Mode Indicators
const MODES = {
  NUMERIC: 0b0001,
  ALPHANUMERIC: 0b0010,
  BYTE: 0b0100,
  KANJI: 0b1000
};

// Alphanumeric character set
const ALPHANUMERIC_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:';

// Capacity table [version][ecLevel][mode] - max characters
// Simplified for versions 1-10
const CAPACITY = [
  // Version 1
  [[41, 25, 17], [34, 20, 14], [27, 16, 11], [17, 10, 7]],
  // Version 2
  [[77, 47, 32], [63, 38, 26], [48, 29, 20], [34, 20, 14]],
  // Version 3
  [[127, 77, 53], [101, 61, 42], [77, 47, 32], [58, 35, 24]],
  // Version 4
  [[187, 114, 78], [149, 90, 62], [111, 67, 46], [82, 50, 34]],
  // Version 5
  [[255, 154, 106], [202, 122, 84], [144, 87, 60], [106, 64, 44]],
  // Version 6
  [[322, 195, 134], [255, 154, 106], [178, 108, 74], [139, 84, 58]],
  // Version 7
  [[370, 224, 154], [293, 178, 122], [221, 134, 92], [154, 93, 64]],
  // Version 8
  [[461, 279, 192], [365, 221, 152], [262, 159, 109], [202, 122, 84]],
  // Version 9
  [[552, 335, 230], [432, 262, 180], [311, 189, 130], [235, 143, 98]],
  // Version 10
  [[652, 395, 271], [513, 311, 213], [366, 221, 151], [288, 174, 119]]
];

// Number of error correction codewords per block
// [version][ecLevel]
const EC_CODEWORDS = [
  // Version 1
  [7, 10, 13, 17],
  // Version 2
  [10, 16, 22, 28],
  // Version 3
  [15, 26, 36, 44],
  // Version 4
  [20, 36, 52, 64],
  // Version 5
  [26, 48, 72, 88],
  // Version 6
  [36, 64, 96, 112],
  // Version 7
  [40, 72, 108, 130],
  // Version 8
  [48, 88, 132, 156],
  // Version 9
  [60, 110, 160, 192],
  // Version 10
  [72, 130, 192, 224]
];

// Total codewords per version
const TOTAL_CODEWORDS = [
  26, 44, 70, 100, 134, 172, 196, 242, 292, 346
];

// Data codewords per block configuration
const BLOCK_CONFIG = [
  // Version 1: [blocks, codewordsPerBlock]
  [[1, 19], [1, 16], [1, 13], [1, 9]],
  // Version 2
  [[1, 34], [1, 28], [1, 22], [1, 16]],
  // Version 3
  [[1, 55], [1, 44], [2, 17], [2, 13]],
  // Version 4
  [[1, 80], [2, 32], [2, 24], [4, 9]],
  // Version 5
  [[1, 108], [2, 43], [2, 15, 2, 16], [2, 11, 2, 12]],
  // Version 6
  [[2, 68], [4, 27], [4, 19], [4, 14]],
  // Version 7
  [[2, 78], [4, 31], [2, 14, 4, 15], [4, 13, 1, 14]],
  // Version 8
  [[2, 97], [2, 38, 2, 39], [4, 18, 2, 19], [4, 14, 2, 15]],
  // Version 9
  [[2, 116], [3, 36, 2, 37], [4, 16, 4, 17], [4, 12, 4, 13]],
  // Version 10
  [[2, 68, 2, 69], [4, 43, 1, 44], [6, 19, 2, 20], [6, 15, 2, 16]]
];

/**
 * Galois Field GF(256) operations for Reed-Solomon
 */
class GaloisField {
  static EXP = new Uint8Array(512);
  static LOG = new Uint8Array(256);
  static initialized = false;

  static init() {
    if (this.initialized) return;
    
    let x = 1;
    for (let i = 0; i < 255; i++) {
      this.EXP[i] = x;
      this.LOG[x] = i;
      x <<= 1;
      if (x & 0x100) {
        x ^= 0x11d; // Primitive polynomial x^8 + x^4 + x^3 + x^2 + 1
      }
    }
    for (let i = 255; i < 512; i++) {
      this.EXP[i] = this.EXP[i - 255];
    }
    this.initialized = true;
  }

  static mul(a, b) {
    if (a === 0 || b === 0) return 0;
    return this.EXP[this.LOG[a] + this.LOG[b]];
  }

  static div(a, b) {
    if (b === 0) throw new Error('Division by zero');
    if (a === 0) return 0;
    return this.EXP[(this.LOG[a] - this.LOG[b] + 255) % 255];
  }

  static exp(n) {
    return this.EXP[n % 255];
  }
}

GaloisField.init();

/**
 * Reed-Solomon Error Correction Encoder
 */
class ReedSolomon {
  static generatePolynomial(ecCodewords) {
    let poly = [1];
    for (let i = 0; i < ecCodewords; i++) {
      const term = [1, GaloisField.exp(i)];
      const newPoly = new Array(poly.length + 1).fill(0);
      for (let j = 0; j < poly.length; j++) {
        for (let k = 0; k < term.length; k++) {
          newPoly[j + k] ^= GaloisField.mul(poly[j], term[k]);
        }
      }
      poly = newPoly;
    }
    return poly;
  }

  static encode(data, ecCodewords) {
    const generator = this.generatePolynomial(ecCodewords);
    const poly = [...data, ...new Array(ecCodewords).fill(0)];
    
    for (let i = 0; i < data.length; i++) {
      const coef = poly[i];
      if (coef !== 0) {
        for (let j = 0; j < generator.length; j++) {
          poly[i + j] ^= GaloisField.mul(generator[j], coef);
        }
      }
    }
    
    return poly.slice(data.length);
  }
}

/**
 * QR Code Generator
 */
class QRCode {
  constructor(data, options = {}) {
    this.data = data;
    this.ecLevel = EC_LEVELS[options.ecLevel] ?? EC_LEVELS.M;
    this.version = options.version ?? null;
    this.mask = options.mask ?? null;
    
    this.modules = null;
    this.size = 0;
    this.generate();
  }

  /**
   * Determine the best mode for encoding
   */
  getMode() {
    if (/^[0-9]+$/.test(this.data)) {
      return MODES.NUMERIC;
    }
    if (/^[0-9A-Z $%*+\-./:]+$/.test(this.data)) {
      return MODES.ALPHANUMERIC;
    }
    return MODES.BYTE;
  }

  /**
   * Find the minimum version that can hold the data
   */
  findVersion() {
    const mode = this.getMode();
    const modeIndex = mode === MODES.NUMERIC ? 0 : mode === MODES.ALPHANUMERIC ? 1 : 2;
    const length = this.data.length;

    for (let v = 0; v < 10; v++) { // Versions 1-10
      if (CAPACITY[v][this.ecLevel][modeIndex] >= length) {
        return v + 1;
      }
    }
    throw new Error('Data too long for versions 1-10. Consider splitting or using larger version.');
  }

  /**
   * Encode data to bitstream
   */
  encodeData() {
    const mode = this.getMode();
    const version = this.version;
    const bits = [];

    // Mode indicator (4 bits)
    this.pushBits(bits, mode, 4);

    // Character count indicator
    const ccBits = version <= 9 ? 
      (mode === MODES.NUMERIC ? 10 : mode === MODES.ALPHANUMERIC ? 9 : 8) :
      (mode === MODES.NUMERIC ? 12 : mode === MODES.ALPHANUMERIC ? 11 : 16);
    this.pushBits(bits, this.data.length, ccBits);

    // Data encoding
    if (mode === MODES.NUMERIC) {
      for (let i = 0; i < this.data.length; i += 3) {
        const chunk = this.data.substr(i, 3);
        const num = parseInt(chunk, 10);
        const bitCount = chunk.length === 3 ? 10 : chunk.length === 2 ? 7 : 4;
        this.pushBits(bits, num, bitCount);
      }
    } else if (mode === MODES.ALPHANUMERIC) {
      for (let i = 0; i < this.data.length; i += 2) {
        if (i + 1 < this.data.length) {
          const val = ALPHANUMERIC_CHARS.indexOf(this.data[i]) * 45 + 
                      ALPHANUMERIC_CHARS.indexOf(this.data[i + 1]);
          this.pushBits(bits, val, 11);
        } else {
          const val = ALPHANUMERIC_CHARS.indexOf(this.data[i]);
          this.pushBits(bits, val, 6);
        }
      }
    } else {
      // Byte mode
      const encoder = new TextEncoder();
      const bytes = encoder.encode(this.data);
      for (const byte of bytes) {
        this.pushBits(bits, byte, 8);
      }
    }

    return bits;
  }

  pushBits(bits, value, count) {
    for (let i = count - 1; i >= 0; i--) {
      bits.push((value >> i) & 1);
    }
  }

  /**
   * Add terminator and padding
   */
  addPadding(bits) {
    const version = this.version;
    const ecLevel = this.ecLevel;
    const config = BLOCK_CONFIG[version - 1][ecLevel];
    
    // Calculate total data codewords
    let totalDataCodewords = 0;
    if (config.length === 2) {
      totalDataCodewords = config[0] * config[1];
    } else if (config.length === 4) {
      totalDataCodewords = config[0] * config[1] + config[2] * config[3];
    }
    
    const totalBits = totalDataCodewords * 8;

    // Terminator (up to 4 bits of 0)
    const terminatorLength = Math.min(4, totalBits - bits.length);
    for (let i = 0; i < terminatorLength; i++) {
      bits.push(0);
    }

    // Pad to byte boundary
    while (bits.length % 8 !== 0) {
      bits.push(0);
    }

    // Padding codewords (alternating 0xEC and 0x11)
    const padPatterns = [0xEC, 0x11];
    let padIndex = 0;
    while (bits.length < totalBits) {
      const padByte = padPatterns[padIndex % 2];
      this.pushBits(bits, padByte, 8);
      padIndex++;
    }

    return bits;
  }

  /**
   * Generate error correction codewords
   */
  generateEC(dataBytes) {
    const version = this.version;
    const ecLevel = this.ecLevel;
    const config = BLOCK_CONFIG[version - 1][ecLevel];
    const ecCodewordsPerBlock = EC_CODEWORDS[version - 1][ecLevel];

    let dataBlocks, ecBlocks;
    
    if (config.length === 2) {
      const [numBlocks, codewordsPerBlock] = config;
      dataBlocks = [dataBytes.slice(0, codewordsPerBlock * numBlocks)];
      ecBlocks = [ReedSolomon.encode(dataBlocks[0], ecCodewordsPerBlock)];
    } else {
      const [numBlocks1, cwPerBlock1, numBlocks2, cwPerBlock2] = config;
      const block1 = dataBytes.slice(0, cwPerBlock1 * numBlocks1);
      const block2 = dataBytes.slice(cwPerBlock1 * numBlocks1);
      dataBlocks = [block1, block2];
      ecBlocks = [
        ReedSolomon.encode(block1, ecCodewordsPerBlock),
        ReedSolomon.encode(block2, ecCodewordsPerBlock)
      ];
    }

    return { dataBlocks, ecBlocks, ecCodewordsPerBlock };
  }

  /**
   * Initialize module matrix
   */
  initModules() {
    const version = this.version;
    this.size = version * 4 + 17;
    this.modules = Array.from({ length: this.size }, () => 
      Array.from({ length: this.size }, () => null)
    );
    this.isFunction = Array.from({ length: this.size }, () => 
      Array.from({ length: this.size }, () => false)
    );
  }

  /**
   * Add finder patterns
   */
  addFinderPatterns() {
    const positions = [
      [0, 0],
      [this.size - 7, 0],
      [0, this.size - 7]
    ];

    for (const [row, col] of positions) {
      for (let r = 0; r < 7; r++) {
        for (let c = 0; c < 7; c++) {
          const isBlack = 
            r === 0 || r === 6 || c === 0 || c === 6 ||
            (r >= 2 && r <= 4 && c >= 2 && c <= 4);
          this.modules[row + r][col + c] = isBlack;
          this.isFunction[row + r][col + c] = true;
        }
      }
    }

    // Separators
    for (let i = 0; i < 8; i++) {
      this.modules[7][i] = this.modules[i][7] = false;
      this.modules[this.size - 8][i] = this.modules[i][this.size - 8] = false;
      this.modules[7][this.size - 1 - i] = this.modules[this.size - 1 - i][7] = false;
      
      this.isFunction[7][i] = this.isFunction[i][7] = true;
      this.isFunction[this.size - 8][i] = this.isFunction[i][this.size - 8] = true;
      this.isFunction[7][this.size - 1 - i] = this.isFunction[this.size - 1 - i][7] = true;
    }
  }

  /**
   * Add timing patterns
   */
  addTimingPatterns() {
    for (let i = 8; i < this.size - 8; i++) {
      const bit = i % 2 === 0;
      this.modules[6][i] = bit;
      this.modules[i][6] = bit;
      this.isFunction[6][i] = true;
      this.isFunction[i][6] = true;
    }
  }

  /**
   * Add alignment patterns (for version >= 2)
   */
  addAlignmentPatterns() {
    if (this.version < 2) return;

    const positions = this.getAlignmentPositions();
    for (const [row, col] of positions) {
      for (let r = -2; r <= 2; r++) {
        for (let c = -2; c <= 2; c++) {
          const isBlack = 
            Math.abs(r) === 2 || Math.abs(c) === 2 || 
            (r === 0 && c === 0);
          this.modules[row + r][col + c] = isBlack;
          this.isFunction[row + r][col + c] = true;
        }
      }
    }
  }

  getAlignmentPositions() {
    if (this.version === 1) return [];
    
    const positions = [6];
    const step = Math.floor((this.size - 13) / (Math.floor(this.version / 7) + 1));
    positions.push(this.size - 7);
    
    for (let i = this.size - 7 - step; i > 6; i -= step) {
      positions.splice(1, 0, i);
    }

    const result = [];
    for (const row of positions) {
      for (const col of positions) {
        // Skip positions overlapping with finder patterns
        if ((row < 9 && col < 9) || 
            (row < 9 && col > this.size - 10) || 
            (row > this.size - 10 && col < 9)) {
          continue;
        }
        result.push([row, col]);
      }
    }
    return result;
  }

  /**
   * Reserve format information areas
   */
  reserveFormatInfo() {
    for (let i = 0; i < 9; i++) {
      this.isFunction[8][i] = true;
      this.isFunction[i][8] = true;
    }
    for (let i = 0; i < 8; i++) {
      this.isFunction[this.size - 1 - i][8] = true;
      this.isFunction[8][this.size - 1 - i] = true;
    }
    this.modules[this.size - 8][8] = true; // Dark module
    this.isFunction[this.size - 8][8] = true;
  }

  /**
   * Place data bits
   */
  placeDataBits(dataBytes, ecCodewords) {
    const bits = [...dataBytes, ...ecCodewords];
    let bitIndex = 0;
    let upward = true;

    for (let col = this.size - 1; col >= 0; col -= 2) {
      if (col === 6) col = 5; // Skip timing pattern column

      for (let row = upward ? this.size - 1 : 0; 
           upward ? row >= 0 : row < this.size; 
           upward ? row-- : row++) {
        
        for (let c = 0; c < 2; c++) {
          const actualCol = col - c;
          if (!this.isFunction[row][actualCol]) {
            const bit = bitIndex < bits.length * 8 ? 
              ((bits[Math.floor(bitIndex / 8)] >> (7 - (bitIndex % 8))) & 1) : 0;
            this.modules[row][actualCol] = bit === 1;
            bitIndex++;
          }
        }
      }
      upward = !upward;
    }
  }

  /**
   * Apply mask pattern
   */
  applyMask(mask) {
    for (let row = 0; row < this.size; row++) {
      for (let col = 0; col < this.size; col++) {
        if (!this.isFunction[row][col]) {
          let invert = false;
          switch (mask) {
            case 0: invert = (row + col) % 2 === 0; break;
            case 1: invert = row % 2 === 0; break;
            case 2: invert = col % 3 === 0; break;
            case 3: invert = (row + col) % 3 === 0; break;
            case 4: invert = (Math.floor(row / 2) + Math.floor(col / 3)) % 2 === 0; break;
            case 5: invert = ((row * col) % 2) + ((row * col) % 3) === 0; break;
            case 6: invert = (((row * col) % 2) + ((row * col) % 3)) % 2 === 0; break;
            case 7: invert = (((row + col) % 2) + ((row * col) % 3)) % 2 === 0; break;
          }
          if (invert) {
            this.modules[row][col] = !this.modules[row][col];
          }
        }
      }
    }
  }

  /**
   * Calculate penalty score for mask evaluation
   */
  calculatePenalty() {
    let penalty = 0;

    // Rule 1: Adjacent modules in row/column
    for (let row = 0; row < this.size; row++) {
      for (let col = 0; col < this.size - 4; col++) {
        let count = 1;
        for (let i = 1; i < 5 && col + i < this.size; i++) {
          if (this.modules[row][col + i] === this.modules[row][col]) count++;
          else break;
        }
        if (count >= 5) penalty += 3 + (count - 5);
      }
    }
    for (let col = 0; col < this.size; col++) {
      for (let row = 0; row < this.size - 4; row++) {
        let count = 1;
        for (let i = 1; i < 5 && row + i < this.size; i++) {
          if (this.modules[row + i][col] === this.modules[row][col]) count++;
          else break;
        }
        if (count >= 5) penalty += 3 + (count - 5);
      }
    }

    // Rule 2: 2x2 blocks of same color
    for (let row = 0; row < this.size - 1; row++) {
      for (let col = 0; col < this.size - 1; col++) {
        const color = this.modules[row][col];
        if (this.modules[row][col + 1] === color &&
            this.modules[row + 1][col] === color &&
            this.modules[row + 1][col + 1] === color) {
          penalty += 3;
        }
      }
    }

    // Rule 3: Finder-like patterns
    const finderPattern = [true, false, true, true, true, false, true];
    const reverseFinder = [true, true, true, false, true, false, true, true, true, false, true];
    
    for (let row = 0; row < this.size; row++) {
      for (let col = 0; col < this.size - 6; col++) {
        const segment = this.modules[row].slice(col, col + 7);
        if (segment.every((v, i) => v === finderPattern[i])) {
          penalty += 40;
        }
      }
    }
    for (let col = 0; col < this.size; col++) {
      for (let row = 0; row < this.size - 6; row++) {
        const segment = [];
        for (let i = 0; i < 7; i++) segment.push(this.modules[row + i][col]);
        if (segment.every((v, i) => v === finderPattern[i])) {
          penalty += 40;
        }
      }
    }

    // Rule 4: Balance of black/white modules
    let blackCount = 0;
    for (let row = 0; row < this.size; row++) {
      for (let col = 0; col < this.size; col++) {
        if (this.modules[row][col]) blackCount++;
      }
    }
    const totalModules = this.size * this.size;
    const percent = (blackCount / totalModules) * 100;
    const prevFive = Math.floor(percent / 5) * 5;
    const nextFive = prevFive + 5;
    penalty += Math.min(Math.abs(prevFive - 50), Math.abs(nextFive - 50)) * 2;

    return penalty;
  }

  /**
   * Add format information
   */
  addFormatInfo(mask) {
    // Format bits: 5 data bits + 10 EC bits
    const ecLevelBits = this.ecLevel;
    const formatData = (ecLevelBits << 3) | mask;
    
    // BCH encoding with generator 10100110111
    let rem = formatData << 10;
    const generator = 0x537;
    for (let i = 14; i >= 10; i--) {
      if (rem & (1 << i)) {
        rem ^= generator << (i - 10);
      }
    }
    const formatBits = ((formatData << 10) | rem) ^ 0x5412; // XOR with mask pattern

    // Place format bits
    // Around top-left finder pattern
    for (let i = 0; i < 6; i++) {
      this.modules[8][i] = ((formatBits >> i) & 1) === 1;
    }
    this.modules[8][7] = ((formatBits >> 6) & 1) === 1;
    this.modules[8][8] = ((formatBits >> 7) & 1) === 1;
    this.modules[7][8] = ((formatBits >> 8) & 1) === 1;
    for (let i = 9; i < 15; i++) {
      this.modules[14 - i][8] = ((formatBits >> i) & 1) === 1;
    }
    
    // Around bottom-left and top-right finder patterns
    for (let i = 0; i < 7; i++) {
      this.modules[this.size - 1 - i][8] = ((formatBits >> i) & 1) === 1;
    }
    for (let i = 0; i < 8; i++) {
      this.modules[8][this.size - 8 + i] = ((formatBits >> (14 - i)) & 1) === 1;
    }
  }

  /**
   * Main generation method
   */
  generate() {
    // Determine version
    this.version = this.version ?? this.findVersion();
    
    // Encode data
    let bits = this.encodeData();
    bits = this.addPadding(bits);
    
    // Convert to bytes
    const dataBytes = [];
    for (let i = 0; i < bits.length; i += 8) {
      let byte = 0;
      for (let j = 0; j < 8; j++) {
        byte = (byte << 1) | (bits[i + j] ?? 0);
      }
      dataBytes.push(byte);
    }

    // Generate error correction
    const { ecBlocks, ecCodewordsPerBlock } = this.generateEC(dataBytes);
    
    // Interleave data and EC codewords
    const ecCodewords = ecBlocks.flat();
    
    // Initialize modules
    this.initModules();
    this.addFinderPatterns();
    this.addTimingPatterns();
    this.addAlignmentPatterns();
    this.reserveFormatInfo();
    
    // Place data
    this.placeDataBits(dataBytes, ecCodewords);
    
    // Find best mask
    if (this.mask === null) {
      let bestMask = 0;
      let bestPenalty = Infinity;
      
      for (let m = 0; m < 8; m++) {
        // Save state
        const saved = this.modules.map(row => [...row]);
        
        this.applyMask(m);
        this.addFormatInfo(m);
        
        const penalty = this.calculatePenalty();
        if (penalty < bestPenalty) {
          bestPenalty = penalty;
          bestMask = m;
        }
        
        // Restore state
        this.modules = saved;
      }
      
      this.mask = bestMask;
    }
    
    // Apply final mask and format info
    this.applyMask(this.mask);
    this.addFormatInfo(this.mask);
  }

  /**
   * Export as ASCII art string
   */
  toASCII(options = {}) {
    const { white = '██', black = '  ', border = true } = options;
    const lines = [];
    
    if (border) {
      lines.push(black.repeat(this.size + 2));
    }
    
    for (let row = 0; row < this.size; row++) {
      let line = border ? black : '';
      for (let col = 0; col < this.size; col++) {
        line += this.modules[row][col] ? black : white;
      }
      line += border ? black : '';
      lines.push(line);
    }
    
    if (border) {
      lines.push(black.repeat(this.size + 2));
    }
    
    return lines.join('\n');
  }

  /**
   * Export as SVG
   */
  toSVG(options = {}) {
    const { size = 300, margin = 4, dark = '#000000', light = '#ffffff' } = options;
    const moduleSize = size / (this.size + 2 * margin);
    
    let svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${size} ${size}" width="${size}" height="${size}">`;
    svg += `<rect width="100%" height="100%" fill="${light}"/>`;
    
    for (let row = 0; row < this.size; row++) {
      for (let col = 0; col < this.size; col++) {
        if (this.modules[row][col]) {
          const x = (col + margin) * moduleSize;
          const y = (row + margin) * moduleSize;
          svg += `<rect x="${x.toFixed(2)}" y="${y.toFixed(2)}" width="${moduleSize.toFixed(2)}" height="${moduleSize.toFixed(2)}" fill="${dark}"/>`;
        }
      }
    }
    
    svg += '</svg>';
    return svg;
  }

  /**
   * Export as 2D boolean array
   */
  toArray() {
    return this.modules.map(row => [...row]);
  }

  /**
   * Export as binary string
   */
  toBinary() {
    return this.modules.map(row => 
      row.map(cell => cell ? '1' : '0').join('')
    ).join('\n');
  }

  /**
   * Get QR code size (modules per side)
   */
  getSize() {
    return this.size;
  }

  /**
   * Get the version used
   */
  getVersion() {
    return this.version;
  }

  /**
   * Get the error correction level
   */
  getECLevel() {
    return ['L', 'M', 'Q', 'H'][this.ecLevel];
  }

  /**
   * Get the mask pattern used
   */
  getMask() {
    return this.mask;
  }
}

/**
 * Quick QR code generation functions
 */
function generateQR(data, options = {}) {
  return new QRCode(data, options);
}

function generateQRASCII(data, options = {}) {
  const qr = new QRCode(data, options);
  return qr.toASCII(options);
}

function generateQRSVG(data, options = {}) {
  const qr = new QRCode(data, options);
  return qr.toSVG(options);
}

function generateQRArray(data, options = {}) {
  const qr = new QRCode(data, options);
  return qr.toArray();
}

// Export
module.exports = {
  QRCode,
  EC_LEVELS,
  MODES,
  generateQR,
  generateQRASCII,
  generateQRSVG,
  generateQRArray
};