/**
 * AllToolkit - Morse Code Utilities Module
 * ==========================================
 * A comprehensive morse code encoding, decoding, and signal processing utility module.
 * Zero external dependencies, pure JavaScript implementation.
 * 
 * Features:
 * - Text to Morse code encoding
 * - Morse code to text decoding
 * - Support for multiple languages (English, numbers, punctuation, Cyrillic, Greek)
 * - Audio signal generation (timing patterns)
 * - Visual signal patterns (LED, flashlight)
 * - Signal detection and parsing
 * - Speed control (WPM - Words Per Minute)
 * - Prosign support (special combined signals)
 * - International Morse code standard compliant
 * 
 * @author AllToolkit
 * @license MIT
 */

// ============================================================================
// Constants
// ============================================================================

/**
 * Standard Morse code timing units
 * Based on international Morse code standard (ITU-R M.1677-1)
 */
const TIMING = {
  DOT: 1,           // Basic unit
  DASH: 3,          // 3 units
  INTRA_CHAR: 1,    // Within character: 1 unit
  INTER_CHAR: 3,    // Between characters: 3 units
  WORD_SPACE: 7,    // Between words: 7 units
};

/**
 * International Morse code mapping for Latin alphabet
 */
const MORSE_CODE = {
  // Letters
  'A': '.-',
  'B': '-...',
  'C': '-.-.',
  'D': '-..',
  'E': '.',
  'F': '..-.',
  'G': '--.',
  'H': '....',
  'I': '..',
  'J': '.---',
  'K': '-.-',
  'L': '.-..',
  'M': '--',
  'N': '-.',
  'O': '---',
  'P': '.--.',
  'Q': '--.-',
  'R': '.-.',
  'S': '...',
  'T': '-',
  'U': '..-',
  'V': '...-',
  'W': '.--',
  'X': '-..-',
  'Y': '-.--',
  'Z': '--..',
  
  // Numbers
  '0': '-----',
  '1': '.----',
  '2': '..---',
  '3': '...--',
  '4': '....-',
  '5': '.....',
  '6': '-....',
  '7': '--...',
  '8': '---..',
  '9': '----.',
  
  // Punctuation
  '.': '.-.-.-',
  ',': '--..--',
  '?': '..--..',
  "'": '.----.',
  '!': '-.-.--',
  '/': '-..-.',
  '(': '-.--.',
  ')': '-.--.-',
  '&': '.-...',
  ':': '---...',
  ';': '-.-.-.',
  '=': '-...-',
  '+': '.-.-.',
  '-': '-....-',
  '_': '..--.-',
  '"': '.-..-.',
  '$': '...-..-',
  '@': '.--.-.',
  '¿': '..-.-',
  '¡': '--...-',
  
  // Extended Latin characters
  'À': '.--.-',
  'Ä': '.-.-',
  'Å': '.--.-',
  'Æ': '.-.-',
  'Ç': '-.-..',
  'Ð': '..-.',
  'È': '.-..-',
  'É': '..-..',
  'Ê': '-..-.',
  'Ë': '..-..',
  'Ì': '.---.',
  'Î': '..-..',
  'Ñ': '--.--',
  'Ö': '---.',
  'Ø': '---.',
  'Ś': '...-...',
  'Š': '----',
  'Þ': '.--..',
  'Ü': '..--',
  'Ů': '..--',
  'Ź': '--..-.',
  'Ż': '--..-',
  
  // Cyrillic alphabet (Russian Morse code)
  'А': '.-',
  'Б': '-...',
  'В': '.--',
  'Г': '--.',
  'Д': '-..',
  'Е': '.',
  'Ж': '...-',
  'З': '--..',
  'И': '..',
  'Й': '.---',
  'К': '-.-',
  'Л': '.-..',
  'М': '--',
  'Н': '-.',
  'О': '---',
  'П': '.--.',
  'Р': '.-.',
  'С': '...',
  'Т': '-',
  'У': '..-',
  'Ф': '..-.',
  'Х': '....',
  'Ц': '-.-.',
  'Ч': '---.',
  'Ш': '----',
  'Щ': '--.-',
  'Ъ': '-.--.-',
  'Ы': '-.--',
  'Ь': '-..-',
  'Э': '..-..',
  'Ю': '..--',
  'Я': '.-.-',
  
  // Greek alphabet
  'Α': '.-',
  'Β': '-...',
  'Γ': '--.',
  'Δ': '-..',
  'Ε': '.',
  'Ζ': '--..',
  'Η': '....',
  'Θ': '-.-.',
  'Ι': '..',
  'Κ': '-.-',
  'Λ': '.-..',
  'Μ': '--',
  'Ν': '-.',
  'Ξ': '-..-',
  'Ο': '---',
  'Π': '.--.',
  'Ρ': '.-.',
  'Σ': '...',
  'Τ': '-',
  'Υ': '-.--',
  'Φ': '..-.',
  'Χ': '-----',
  'Ψ': '--.--',
  'Ω': '.--',
};

/**
 * Reverse mapping for decoding
 * Latin characters are prioritized over Greek/Cyrillic that share the same codes
 */
const MORSE_DECODE = {};

// Priority order: Latin letters/numbers first, then punctuation, then extended
const PRIORITY_CHARS = [
  // Latin letters (highest priority)
  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
  // Numbers
  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
  // Punctuation
  '.', ',', '?', "'", '!', '/', '(', ')', '&', ':', ';', '=', '+', '-', '_', '"', '$', '@', '¿', '¡',
];

// First add priority characters
for (const char of PRIORITY_CHARS) {
  if (MORSE_CODE[char]) {
    MORSE_DECODE[MORSE_CODE[char]] = char;
  }
}

// Then add remaining characters only if they don't conflict
for (const [char, code] of Object.entries(MORSE_CODE)) {
  if (!MORSE_DECODE[code]) {
    MORSE_DECODE[code] = char;
  }
}

/**
 * Prosigns (Procedure Signals) - Combined signals without inter-character gaps
 */
const PROSIGNS = {
  'AA': '.-.-',        // End of line (newline)
  'AR': '.-.-.',       // End of message
  'AS': '.-...',       // Wait
  'BK': '-...-.-',     // Break
  'BT': '-...-',       // Separator (new paragraph)
  'CL': '-.-..-..',    // Going off the air (closing)
  'CT': '-.-.-',       // Start copying
  'DO': '-..---',      // Change to transmit
  'KN': '-.--.',       // Invite a specific station to transmit
  'SK': '...-.-',      // End of work (end of contact)
  'SN': '...-.',       // Understood
  'SOS': '...---...',  // Distress signal
  'HH': '........',    // Error (8 dots)
};

/**
 * Reverse prosign mapping for decoding
 */
const PROSIGN_DECODE = {};
for (const [name, code] of Object.entries(PROSIGNS)) {
  PROSIGN_DECODE[code] = name;
}

// ============================================================================
// Encoder Class
// ============================================================================

/**
 * Morse code encoder
 */
class MorseEncoder {
  /**
   * Create a new Morse encoder
   * @param {Object} options - Encoder options
   * @param {string} [options.dotSymbol='.'] - Symbol for dot
   * @param {string} [options.dashSymbol='-'] - Symbol for dash
   * @param {string} [options.charSeparator='/'] - Separator between characters
   * @param {string} [options.wordSeparator='//'] - Separator between words
   * @param {boolean} [options.lowercase=false] - Convert to lowercase output
   * @param {boolean} [options.throwOnError=false] - Throw on unknown characters
   */
  constructor(options = {}) {
    this.dotSymbol = options.dotSymbol || '.';
    this.dashSymbol = options.dashSymbol || '-';
    this.charSeparator = options.charSeparator || ' ';
    this.wordSeparator = options.wordSeparator || '   ';
    this.lowercase = options.lowercase || false;
    this.throwOnError = options.throwOnError || false;
    this.unknownChar = options.unknownChar || '?';
  }

  /**
   * Encode text to Morse code
   * @param {string} text - Text to encode
   * @returns {string} Morse code representation
   */
  encode(text) {
    if (!text) return '';
    
    const words = text.split(/\s+/);
    const encodedWords = [];
    
    for (const word of words) {
      if (!word) continue;
      const encodedChars = [];
      
      for (const char of word) {
        const upperChar = char.toUpperCase();
        let morse = MORSE_CODE[upperChar];
        
        if (morse) {
          morse = this._formatCode(morse);
        } else {
          if (this.throwOnError) {
            throw new Error(`Unknown character: ${char}`);
          }
          morse = this.unknownChar;
        }
        
        encodedChars.push(morse);
      }
      
      encodedWords.push(encodedChars.join(this.charSeparator));
    }
    
    return encodedWords.join(this.wordSeparator);
  }

  /**
   * Encode a single character
   * @param {string} char - Character to encode
   * @returns {string} Morse code for the character
   */
  encodeChar(char) {
    if (!char || char.length !== 1) {
      if (this.throwOnError) {
        throw new Error('Input must be a single character');
      }
      return this.unknownChar;
    }
    
    const morse = MORSE_CODE[char.toUpperCase()];
    if (morse) {
      return this._formatCode(morse);
    }
    
    if (this.throwOnError) {
      throw new Error(`Unknown character: ${char}`);
    }
    return this.unknownChar;
  }

  /**
   * Encode a prosign
   * @param {string} name - Prosign name (e.g., 'AR', 'SOS')
   * @returns {string} Morse code for the prosign
   */
  encodeProsign(name) {
    const code = PROSIGNS[name.toUpperCase()];
    if (!code) {
      if (this.throwOnError) {
        throw new Error(`Unknown prosign: ${name}`);
      }
      return this.unknownChar;
    }
    return this._formatCode(code);
  }

  /**
   * Format Morse code with custom symbols
   * @private
   */
  _formatCode(code) {
    let formatted = code;
    if (this.dotSymbol !== '.') {
      formatted = formatted.replace(/\./g, this.dotSymbol);
    }
    if (this.dashSymbol !== '-') {
      formatted = formatted.replace(/-/g, this.dashSymbol);
    }
    return this.lowercase ? formatted.toLowerCase() : formatted;
  }

  /**
   * Check if a character can be encoded
   * @param {string} char - Character to check
   * @returns {boolean} True if character can be encoded
   */
  canEncode(char) {
    if (!char || char.length !== 1) return false;
    return MORSE_CODE[char.toUpperCase()] !== undefined;
  }

  /**
   * Get list of supported characters
   * @returns {string[]} Array of supported characters
   */
  getSupportedChars() {
    return Object.keys(MORSE_CODE);
  }
}

// ============================================================================
// Decoder Class
// ============================================================================

/**
 * Morse code decoder
 */
class MorseDecoder {
  /**
   * Create a new Morse decoder
   * @param {Object} options - Decoder options
   * @param {string} [options.dotSymbol='.'] - Symbol for dot
   * @param {string} [options.dashSymbol='-'] - Symbol for dash
   * @param {string} [options.charSeparator=' '] - Separator between characters
   * @param {string} [options.wordSeparator='   '] - Separator between words
   * @param {string} [options.unknownChar='?'] - Character for unknown codes
   * @param {boolean} [options.lowercase=false] - Output in lowercase
   * @param {boolean} [options.throwOnError=false] - Throw on unknown codes
   */
  constructor(options = {}) {
    this.dotSymbol = options.dotSymbol || '.';
    this.dashSymbol = options.dashSymbol || '-';
    this.charSeparator = options.charSeparator || ' ';
    this.wordSeparator = options.wordSeparator || '   ';
    this.unknownChar = options.unknownChar || '?';
    this.lowercase = options.lowercase || false;
    this.throwOnError = options.throwOnError || false;
  }

  /**
   * Decode Morse code to text
   * @param {string} morse - Morse code to decode
   * @returns {string} Decoded text
   */
  decode(morse) {
    if (!morse) return '';
    
    // Normalize the input
    morse = this._normalizeInput(morse);
    
    const words = morse.split(this.wordSeparator);
    const decodedWords = [];
    
    for (const word of words) {
      if (!word.trim()) continue;
      const chars = word.split(this.charSeparator);
      const decodedChars = [];
      
      for (const char of chars) {
        if (!char.trim()) continue;
        
        // Check for prosign first
        let decoded = PROSIGN_DECODE[char];
        
        if (!decoded) {
          decoded = MORSE_DECODE[char];
        }
        
        if (decoded) {
          decodedChars.push(this.lowercase ? decoded.toLowerCase() : decoded);
        } else {
          if (this.throwOnError) {
            throw new Error(`Unknown Morse code: ${char}`);
          }
          decodedChars.push(this.unknownChar);
        }
      }
      
      decodedWords.push(decodedChars.join(''));
    }
    
    return decodedWords.join(' ');
  }

  /**
   * Decode a single Morse code character
   * @param {string} code - Morse code to decode
   * @returns {string} Decoded character
   */
  decodeChar(code) {
    if (!code) {
      if (this.throwOnError) {
        throw new Error('Empty Morse code');
      }
      return this.unknownChar;
    }
    
    code = this._normalizeInput(code);
    
    // Check for prosign
    let decoded = PROSIGN_DECODE[code];
    if (decoded) {
      return this.lowercase ? decoded.toLowerCase() : decoded;
    }
    
    decoded = MORSE_DECODE[code];
    if (decoded) {
      return this.lowercase ? decoded.toLowerCase() : decoded;
    }
    
    if (this.throwOnError) {
      throw new Error(`Unknown Morse code: ${code}`);
    }
    return this.unknownChar;
  }

  /**
   * Normalize Morse code input
   * @private
   */
  _normalizeInput(code) {
    let normalized = code;
    
    // Replace custom symbols with standard
    if (this.dotSymbol !== '.') {
      const dotRegex = new RegExp(this._escapeRegex(this.dotSymbol), 'g');
      normalized = normalized.replace(dotRegex, '.');
    }
    if (this.dashSymbol !== '-') {
      const dashRegex = new RegExp(this._escapeRegex(this.dashSymbol), 'g');
      normalized = normalized.replace(dashRegex, '-');
    }
    
    return normalized;
  }

  /**
   * Escape special regex characters
   * @private
   */
  _escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  /**
   * Check if a Morse code can be decoded
   * @param {string} code - Morse code to check
   * @returns {boolean} True if code can be decoded
   */
  canDecode(code) {
    if (!code) return false;
    code = this._normalizeInput(code);
    return MORSE_DECODE[code] !== undefined || PROSIGN_DECODE[code] !== undefined;
  }
}

// ============================================================================
// Signal Generator Class
// ============================================================================

/**
 * Morse code signal generator for audio/visual output
 */
class MorseSignalGenerator {
  /**
   * Create a new signal generator
   * @param {Object} options - Generator options
   * @param {number} [options.wpm=15] - Words per minute (speed)
   * @param {number} [options.frequency=600] - Audio frequency in Hz
   * @param {number} [options.sampleRate=44100] - Audio sample rate
   */
  constructor(options = {}) {
    this.setWpm(options.wpm !== undefined ? options.wpm : 15);
    this.frequency = options.frequency !== undefined ? options.frequency : 600;
    this.sampleRate = options.sampleRate !== undefined ? options.sampleRate : 44100;
  }

  /**
   * Set speed in words per minute
   * @param {number} wpm - Words per minute
   */
  setWpm(wpm) {
    if (wpm <= 0) throw new Error('WPM must be positive');
    this.wpm = wpm;
    // PARIS standard: 50 units per word
    // 1 unit = 1.2 / wpm seconds
    this.unitTime = 1.2 / wpm; // in seconds
  }

  /**
   * Get timing for each element
   * @returns {Object} Timing values in seconds
   */
  getTiming() {
    return {
      dot: this.unitTime * TIMING.DOT,
      dash: this.unitTime * TIMING.DASH,
      intraChar: this.unitTime * TIMING.INTRA_CHAR,
      interChar: this.unitTime * TIMING.INTER_CHAR,
      wordSpace: this.unitTime * TIMING.WORD_SPACE,
    };
  }

  /**
   * Generate timing pattern for text
   * @param {string} text - Text to convert
   * @returns {Array} Array of timing tuples [on/off, duration]
   */
  generateTimingPattern(text) {
    const encoder = new MorseEncoder();
    const morse = encoder.encode(text);
    const pattern = [];
    const timing = this.getTiming();
    
    let i = 0;
    while (i < morse.length) {
      const char = morse[i];
      
      if (char === encoder.dotSymbol) {
        pattern.push(['on', timing.dot]);
        i++;
        // Add intra-character gap if next is dot/dash
        if (i < morse.length && (morse[i] === encoder.dotSymbol || morse[i] === encoder.dashSymbol)) {
          pattern.push(['off', timing.intraChar]);
        }
      } else if (char === encoder.dashSymbol) {
        pattern.push(['on', timing.dash]);
        i++;
        // Add intra-character gap if next is dot/dash
        if (i < morse.length && (morse[i] === encoder.dotSymbol || morse[i] === encoder.dashSymbol)) {
          pattern.push(['off', timing.intraChar]);
        }
      } else if (char === encoder.charSeparator) {
        // Inter-character gap
        pattern.push(['off', timing.interChar]);
        i++;
      } else if (morse.substring(i, i + 3) === encoder.wordSeparator) {
        // Word gap
        pattern.push(['off', timing.wordSpace]);
        i += 3;
      } else {
        i++;
      }
    }
    
    return pattern;
  }

  /**
   * Generate binary pattern (1 = on, 0 = off)
   * @param {string} text - Text to convert
   * @param {number} [resolution=100] - Samples per unit time
   * @returns {string} Binary pattern string
   */
  generateBinaryPattern(text, resolution = 100) {
    const encoder = new MorseEncoder();
    const morse = encoder.encode(text);
    let binary = '';
    
    for (const char of morse) {
      if (char === encoder.dotSymbol) {
        binary += '1'.repeat(TIMING.DOT * resolution);
        binary += '0'.repeat(TIMING.INTRA_CHAR * resolution);
      } else if (char === encoder.dashSymbol) {
        binary += '1'.repeat(TIMING.DASH * resolution);
        binary += '0'.repeat(TIMING.INTRA_CHAR * resolution);
      } else if (char === encoder.charSeparator) {
        // Remove last intra-char gap and add inter-char gap
        if (binary.endsWith('0'.repeat(TIMING.INTRA_CHAR * resolution))) {
          binary = binary.slice(0, -TIMING.INTRA_CHAR * resolution);
        }
        binary += '0'.repeat(TIMING.INTER_CHAR * resolution);
      } else if (char === ' ') {
        // Word space - remove last inter-char gap and add word space
        if (binary.endsWith('0'.repeat(TIMING.INTER_CHAR * resolution))) {
          binary = binary.slice(0, -TIMING.INTER_CHAR * resolution);
        }
        binary += '0'.repeat(TIMING.WORD_SPACE * resolution);
      }
    }
    
    return binary;
  }

  /**
   * Generate audio samples for text
   * @param {string} text - Text to convert to audio
   * @returns {Float32Array} Audio samples (-1.0 to 1.0)
   */
  generateAudio(text) {
    const pattern = this.generateTimingPattern(text);
    const timing = this.getTiming();
    
    // Calculate total duration
    let totalDuration = 0;
    for (const [, duration] of pattern) {
      totalDuration += duration;
    }
    
    // Add some silence at the end
    totalDuration += 0.1;
    
    const numSamples = Math.ceil(totalDuration * this.sampleRate);
    const samples = new Float32Array(numSamples);
    
    let sampleIndex = 0;
    
    for (const [state, duration] of pattern) {
      const samplesForState = Math.ceil(duration * this.sampleRate);
      
      if (state === 'on') {
        // Generate sine wave
        for (let i = 0; i < samplesForState && sampleIndex < numSamples; i++, sampleIndex++) {
          const t = sampleIndex / this.sampleRate;
          samples[sampleIndex] = Math.sin(2 * Math.PI * this.frequency * t);
        }
      } else {
        // Silence
        for (let i = 0; i < samplesForState && sampleIndex < numSamples; i++, sampleIndex++) {
          samples[sampleIndex] = 0;
        }
      }
    }
    
    return samples;
  }

  /**
   * Generate a beep schedule for visual/audio cues
   * @param {string} text - Text to convert
   * @returns {Array} Array of {start, end, type} objects
   */
  generateBeepSchedule(text) {
    const pattern = this.generateTimingPattern(text);
    const schedule = [];
    let currentTime = 0;
    
    for (const [state, duration] of pattern) {
      if (state === 'on') {
        schedule.push({
          start: currentTime,
          end: currentTime + duration,
          duration: duration,
          type: duration < 0.2 ? 'dot' : 'dash',
        });
      }
      currentTime += duration;
    }
    
    return schedule;
  }

  /**
   * Calculate total duration for text
   * @param {string} text - Text to calculate duration for
   * @returns {number} Duration in seconds
   */
  calculateDuration(text) {
    const encoder = new MorseEncoder();
    const morse = encoder.encode(text);
    const timing = this.getTiming();
    
    let duration = 0;
    let lastWasSignal = false;
    
    for (let i = 0; i < morse.length; i++) {
      const char = morse[i];
      
      if (char === encoder.dotSymbol) {
        duration += timing.dot;
        lastWasSignal = true;
      } else if (char === encoder.dashSymbol) {
        duration += timing.dash;
        lastWasSignal = true;
      } else if (char === encoder.charSeparator) {
        if (lastWasSignal) {
          duration += timing.intraChar; // Gap after last signal
        }
        duration += timing.interChar - timing.intraChar;
        lastWasSignal = false;
      } else if (char === ' ') {
        if (lastWasSignal) {
          duration += timing.intraChar;
        }
        duration += timing.wordSpace - timing.intraChar;
        lastWasSignal = false;
      }
    }
    
    return duration;
  }
}

// ============================================================================
// Signal Parser Class
// ============================================================================

/**
 * Parse Morse signals from timing data
 */
class MorseSignalParser {
  /**
   * Create a new signal parser
   * @param {Object} options - Parser options
   * @param {number} [options.wpm=15] - Words per minute (for timing thresholds)
   * @param {number} [options.tolerance=0.3] - Tolerance ratio for timing detection
   */
  constructor(options = {}) {
    this.setWpm(options.wpm !== undefined ? options.wpm : 15);
    this.tolerance = options.tolerance !== undefined ? options.tolerance : 0.3;
  }

  /**
   * Set words per minute
   * @param {number} wpm - Words per minute
   */
  setWpm(wpm) {
    if (wpm <= 0) throw new Error('WPM must be positive');
    this.wpm = wpm;
    this.unitTime = 1.2 / wpm;
  }

  /**
   * Parse timing intervals to Morse code
   * @param {Array} intervals - Array of [duration, state] where state is 1 (on) or 0 (off)
   * @returns {string} Morse code string
   */
  parseIntervals(intervals) {
    if (!intervals || intervals.length === 0) return '';
    
    // Calculate average unit time from the intervals
    const onDurations = intervals
      .filter(([_, state]) => state === 1)
      .map(([duration]) => duration);
    
    if (onDurations.length === 0) return '';
    
    // Use the shortest on duration as the dot duration estimate
    const minOn = Math.min(...onDurations);
    
    // Threshold between dot and dash (2 units)
    const dashThreshold = minOn * 2;
    
    // Threshold between intra-char, inter-char, and word space
    const charSpaceThreshold = minOn * 2; // 2 units = between dot and inter-char
    const wordSpaceThreshold = minOn * 5; // 5 units = between inter-char and word
    
    let morse = '';
    
    for (const [duration, state] of intervals) {
      if (state === 1) {
        // On state - it's a dot or dash
        if (duration < dashThreshold) {
          morse += '.';
        } else {
          morse += '-';
        }
      } else {
        // Off state - it's a gap
        if (duration < charSpaceThreshold) {
          // Intra-character gap - no separator needed
          // Do nothing
        } else if (duration < wordSpaceThreshold) {
          // Inter-character gap
          morse += ' ';
        } else {
          // Word gap
          morse += '   ';
        }
      }
    }
    
    return morse.trim();
  }

  /**
   * Parse binary pattern to Morse code
   * @param {string} binary - Binary pattern string
   * @param {number} [unitSamples] - Optional: number of samples per unit time
   * @returns {string} Morse code string
   */
  parseBinary(binary, unitSamples) {
    if (!binary) return '';
    
    // Find transitions
    const transitions = [];
    let lastState = binary[0];
    let count = 1;
    
    for (let i = 1; i < binary.length; i++) {
      if (binary[i] === lastState) {
        count++;
      } else {
        transitions.push({ state: parseInt(lastState), duration: count });
        lastState = binary[i];
        count = 1;
      }
    }
    transitions.push({ state: parseInt(lastState), duration: count });
    
    // If unitSamples not provided, estimate from the shortest on duration
    if (!unitSamples) {
      const onDurations = transitions
        .filter(t => t.state === 1)
        .map(t => t.duration);
      if (onDurations.length > 0) {
        unitSamples = Math.min(...onDurations);
      } else {
        unitSamples = 1;
      }
    }
    
    // Convert to intervals
    const intervals = transitions.map(t => [t.duration / unitSamples, t.state]);
    
    return this.parseIntervals(intervals);
  }

  /**
   * Detect WPM from timing intervals
   * @param {Array} intervals - Array of [duration, state]
   * @returns {number} Estimated WPM
   */
  detectWpm(intervals) {
    if (!intervals || intervals.length === 0) return 15;
    
    const onDurations = intervals
      .filter(([_, state]) => state === 1)
      .map(([duration]) => duration);
    
    if (onDurations.length === 0) return 15;
    
    // Find dots (shortest durations)
    const sorted = [...onDurations].sort((a, b) => a - b);
    
    // Assume the shortest group are dots
    const dots = sorted.slice(0, Math.ceil(sorted.length / 2));
    const avgDot = dots.reduce((a, b) => a + b, 0) / dots.length;
    
    // Calculate WPM (1 unit = 1.2 / wpm seconds)
    const wpm = 1.2 / avgDot;
    
    return Math.round(wpm);
  }
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Quick encode text to Morse code
 * @param {string} text - Text to encode
 * @param {Object} [options] - Encoder options
 * @returns {string} Morse code
 */
function encode(text, options = {}) {
  const encoder = new MorseEncoder(options);
  return encoder.encode(text);
}

/**
 * Quick decode Morse code to text
 * @param {string} morse - Morse code to decode
 * @param {Object} [options] - Decoder options
 * @returns {string} Decoded text
 */
function decode(morse, options = {}) {
  const decoder = new MorseDecoder(options);
  return decoder.decode(morse);
}

/**
 * Check if text contains only encodable characters
 * @param {string} text - Text to check
 * @returns {boolean} True if all characters can be encoded
 */
function isValidText(text) {
  if (!text) return true;
  const encoder = new MorseEncoder();
  return [...text].every(char => {
    if (/\s/.test(char)) return true;
    return encoder.canEncode(char);
  });
}

/**
 * Check if string is valid Morse code
 * @param {string} morse - Morse code to check
 * @returns {boolean} True if valid Morse code
 */
function isValidMorse(morse) {
  if (!morse) return true;
  const decoder = new MorseDecoder();
  const codes = morse.split(/\s+/);
  return codes.every(code => {
    if (!code) return true;
    return decoder.canDecode(code);
  });
}

/**
 * Get Morse code for a single character
 * @param {string} char - Character to look up
 * @returns {string|null} Morse code or null if not found
 */
function getMorseCode(char) {
  if (!char || char.length !== 1) return null;
  return MORSE_CODE[char.toUpperCase()] || null;
}

/**
 * Get character for a Morse code
 * @param {string} code - Morse code to look up
 * @returns {string|null} Character or null if not found
 */
function getCharFromMorse(code) {
  if (!code) return null;
  return MORSE_DECODE[code] || null;
}

/**
 * Calculate statistics for Morse code
 * @param {string} text - Text to analyze
 * @returns {Object} Statistics object
 */
function getStats(text) {
  const encoder = new MorseEncoder();
  const morse = encoder.encode(text);
  
  const dots = (morse.match(/\./g) || []).length;
  const dashes = (morse.match(/-/g) || []).length;
  const words = text.split(/\s+/).filter(w => w).length;
  const chars = text.replace(/\s/g, '').length;
  
  // Calculate total units
  const totalUnits = dots * TIMING.DOT + dashes * TIMING.DASH;
  // Add inter-character gaps (3 units each, minus 1 for already counted)
  const charGaps = Math.max(0, chars - words) * (TIMING.INTER_CHAR - 1);
  // Add word gaps (7 units each, minus inter-char)
  const wordGaps = Math.max(0, words - 1) * (TIMING.WORD_SPACE - TIMING.INTER_CHAR);
  
  return {
    text: text,
    morse: morse,
    dots: dots,
    dashes: dashes,
    characters: chars,
    words: words,
    totalUnits: totalUnits + charGaps + wordGaps,
    ratio: dashes > 0 ? (dots / dashes).toFixed(2) : dots.toString(),
  };
}

/**
 * Convert text to visual representation
 * @param {string} text - Text to convert
 * @param {Object} [options] - Options
 * @param {string} [options.on='█'] - On symbol
 * @param {string} [options.off='░'] - Off symbol
 * @param {number} [options.unitWidth=3] - Width per unit time
 * @returns {string} Visual representation
 */
function toVisual(text, options = {}) {
  const on = options.on || '█';
  const off = options.off || '░';
  const unitWidth = options.unitWidth || 3;
  
  const encoder = new MorseEncoder();
  const morse = encoder.encode(text);
  
  let visual = '';
  
  for (const char of morse) {
    if (char === encoder.dotSymbol) {
      visual += on.repeat(unitWidth);
      visual += off.repeat(unitWidth); // Intra-char gap
    } else if (char === encoder.dashSymbol) {
      visual += on.repeat(unitWidth * 3);
      visual += off.repeat(unitWidth); // Intra-char gap
    } else if (char === encoder.charSeparator) {
      // Remove last intra-char gap, add inter-char gap
      visual = visual.slice(0, -unitWidth);
      visual += off.repeat(unitWidth * 3);
    } else if (char === ' ') {
      // Remove last gap, add word space
      visual = visual.slice(0, -unitWidth);
      visual += off.repeat(unitWidth * 7);
    }
  }
  
  return visual;
}

/**
 * Estimate transmission time
 * @param {string} text - Text to transmit
 * @param {number} [wpm=15] - Words per minute
 * @returns {number} Time in seconds
 */
function estimateTime(text, wpm = 15) {
  const generator = new MorseSignalGenerator({ wpm });
  return generator.calculateDuration(text);
}

/**
 * Generate a practice sequence
 * @param {Object} [options] - Options
 * @param {string[]} [options.chars] - Characters to practice
 * @param {number} [options.count=10] - Number of items
 * @param {boolean} [options.includeWords=false] - Include common words
 * @returns {Object[]} Array of {char, morse} objects
 */
function generatePractice(options = {}) {
  const chars = options.chars || 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'.split('');
  const count = options.count || 10;
  const includeWords = options.includeWords || false;
  
  const commonWords = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER'];
  const encoder = new MorseEncoder();
  const result = [];
  
  for (let i = 0; i < count; i++) {
    let item;
    
    if (includeWords && Math.random() > 0.5) {
      item = commonWords[Math.floor(Math.random() * commonWords.length)];
    } else {
      item = chars[Math.floor(Math.random() * chars.length)];
    }
    
    result.push({
      char: item,
      morse: encoder.encode(item),
    });
  }
  
  return result;
}

// ============================================================================
// Exports
// ============================================================================

module.exports = {
  // Constants
  TIMING,
  MORSE_CODE,
  MORSE_DECODE,
  PROSIGNS,
  PROSIGN_DECODE,
  
  // Classes
  MorseEncoder,
  MorseDecoder,
  MorseSignalGenerator,
  MorseSignalParser,
  
  // Utility functions
  encode,
  decode,
  isValidText,
  isValidMorse,
  getMorseCode,
  getCharFromMorse,
  getStats,
  toVisual,
  estimateTime,
  generatePractice,
};