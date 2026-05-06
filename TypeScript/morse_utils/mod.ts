/**
 * Morse Code Utilities Module for TypeScript
 * 
 * A comprehensive Morse code encoding and decoding utility module
 * with zero dependencies.
 * 
 * Features:
 * - Text to Morse code encoding
 * - Morse code to text decoding
 * - Timing configuration for audio generation
 * - Prosigns (special operator signals) support
 * - Audio signal generation helpers
 * - Validation and utility functions
 * - Zero dependencies, uses only TypeScript/JavaScript standard library
 * 
 * @module morse_utils
 * @version 1.0.0
 * @license MIT
 */

/**
 * Morse code timing configuration
 */
export interface MorseTimingConfig {
  /** Duration of a dot in milliseconds (1 unit) */
  dotDurationMs: number;
  /** Duration of a dash in milliseconds (3 units) */
  dashDurationMs: number;
  /** Gap between symbols within a character (1 unit) */
  symbolGapMs: number;
  /** Gap between characters (3 units) */
  charGapMs: number;
  /** Gap between words (7 units) */
  wordGapMs: number;
  /** Audio frequency in Hz (default: 700) */
  frequencyHz: number;
}

/**
 * Signal element for audio generation
 */
export interface MorseSignal {
  /** true = signal on (tone), false = signal off (silence) */
  on: boolean;
  /** Duration in milliseconds */
  durationMs: number;
}

/**
 * Prosign (special operator signal)
 */
export interface Prosign {
  /** Prosign name/abbreviation */
  name: string;
  /** Morse code representation */
  code: string;
  /** Description/meaning */
  description: string;
}

/**
 * Morse code analysis result
 */
export interface MorseAnalysis {
  /** Total count of dots */
  dotCount: number;
  /** Total count of dashes */
  dashCount: number;
  /** Total count of space characters */
  spaceCount: number;
  /** Total signal count (dots + dashes) */
  signalCount: number;
  /** Estimated character count */
  characterCount: number;
  /** Estimated word count */
  wordCount: number;
}

/**
 * Standard Morse code lookup table
 */
const MORSE_CODE_MAP: Record<string, string> = {
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
  '×': '-..-.', // Same as /
};

/**
 * Reverse lookup map for decoding
 */
const MORSE_DECODE_MAP: Record<string, string> = {};

// Initialize reverse map
for (const [char, code] of Object.entries(MORSE_CODE_MAP)) {
  MORSE_DECODE_MAP[code] = char;
}

/**
 * Common prosigns (special operator signals)
 */
export const PROSIGNS: Prosign[] = [
  { name: 'AR', code: '.-.-.', description: 'End of message' },
  { name: 'BT', code: '-...-', description: 'Break / pause' },
  { name: 'SK', code: '...-.-', description: 'End of work' },
  { name: 'SN', code: '...-.', description: 'Understood' },
  { name: 'KN', code: '-.--.', description: 'Invite a specific station to transmit' },
  { name: 'AS', code: '.-...', description: 'Wait' },
  { name: 'K', code: '-.-', description: 'Invitation to transmit' },
  { name: 'VE', code: '...-', description: 'Verified' },
  { name: 'HH', code: '........', description: 'Error' },
  { name: 'SOS', code: '...---...', description: 'Distress signal' },
  { name: 'CQ', code: '-.-.--.-', description: 'Calling any station' },
];

/**
 * Default timing configuration (standard Morse timing)
 * @returns Default timing config with 60ms dot duration
 */
export function defaultTiming(): MorseTimingConfig {
  const dotDurationMs = 60;
  return {
    dotDurationMs,
    dashDurationMs: dotDurationMs * 3,
    symbolGapMs: dotDurationMs,
    charGapMs: dotDurationMs * 3,
    wordGapMs: dotDurationMs * 7,
    frequencyHz: 700,
  };
}

/**
 * Fast timing configuration for quick transmission
 * @returns Fast timing config with 40ms dot duration
 */
export function fastTiming(): MorseTimingConfig {
  const dotDurationMs = 40;
  return {
    dotDurationMs,
    dashDurationMs: dotDurationMs * 3,
    symbolGapMs: dotDurationMs,
    charGapMs: dotDurationMs * 3,
    wordGapMs: dotDurationMs * 7,
    frequencyHz: 700,
  };
}

/**
 * Slow timing configuration for learning/beginners
 * @returns Slow timing config with 120ms dot duration
 */
export function slowTiming(): MorseTimingConfig {
  const dotDurationMs = 120;
  return {
    dotDurationMs,
    dashDurationMs: dotDurationMs * 3,
    symbolGapMs: dotDurationMs,
    charGapMs: dotDurationMs * 3,
    wordGapMs: dotDurationMs * 7,
    frequencyHz: 600,
  };
}

/**
 * Custom timing configuration
 * @param dotDurationMs - Duration of a dot in milliseconds
 * @param frequencyHz - Audio frequency in Hz (default: 700)
 * @returns Custom timing configuration
 */
export function customTiming(dotDurationMs: number, frequencyHz: number = 700): MorseTimingConfig {
  return {
    dotDurationMs,
    dashDurationMs: dotDurationMs * 3,
    symbolGapMs: dotDurationMs,
    charGapMs: dotDurationMs * 3,
    wordGapMs: dotDurationMs * 7,
    frequencyHz,
  };
}

/**
 * Convert WPM (words per minute) to dot duration
 * Standard word "PARIS" = 50 units
 * @param wpm - Words per minute
 * @returns Dot duration in milliseconds
 */
export function wpmToDotDuration(wpm: number): number {
  // WPM = 1200 / (dot duration in ms)
  return 1200 / wpm;
}

/**
 * Convert dot duration to WPM (words per minute)
 * @param dotDurationMs - Dot duration in milliseconds
 * @returns Words per minute
 */
export function dotDurationToWpm(dotDurationMs: number): number {
  return 1200 / dotDurationMs;
}

/**
 * Encode text to Morse code
 * @param text - Text to encode
 * @param options - Optional encoding options
 * @returns Morse code string
 * @throws Error if text contains invalid characters
 * @example
 * ```typescript
 * const morse = encode('SOS');
 * // "... --- ..."
 * const morseWithSep = encode('HELLO WORLD', { separator: '/' });
 * // ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
 * ```
 */
export function encode(text: string, options?: { separator?: string }): string {
  if (!text) {
    return '';
  }
  
  const separator = options?.separator ?? ' '; // Space between characters
  const wordSeparator = ' / '; // Standard word separator
  
  const result: string[] = [];
  const words = text.split(/\s+/);
  
  for (let wordIdx = 0; wordIdx < words.length; wordIdx++) {
    const word = words[wordIdx];
    if (!word) continue;
    
    if (wordIdx > 0) {
      result.push(wordSeparator);
    }
    
    for (let charIdx = 0; charIdx < word.length; charIdx++) {
      const char = word[charIdx].toUpperCase();
      const morse = MORSE_CODE_MAP[char];
      
      if (!morse) {
        // Skip unknown characters or throw error
        continue;
      }
      
      if (charIdx > 0) {
        result.push(separator);
      }
      result.push(morse);
    }
  }
  
  return result.join('');
}

/**
 * Encode text to Morse code, throws on invalid character
 * @param text - Text to encode
 * @returns Morse code string
 * @throws Error if text contains invalid characters
 */
export function encodeStrict(text: string): string {
  if (!text) {
    return '';
  }
  
  const result: string[] = [];
  const words = text.split(/\s+/);
  
  for (let wordIdx = 0; wordIdx < words.length; wordIdx++) {
    const word = words[wordIdx];
    if (!word) continue;
    
    if (wordIdx > 0) {
      result.push(' / ');
    }
    
    for (let charIdx = 0; charIdx < word.length; charIdx++) {
      const char = word[charIdx].toUpperCase();
      const morse = MORSE_CODE_MAP[char];
      
      if (!morse) {
        throw new Error(`Invalid character for Morse encoding: '${word[charIdx]}'`);
      }
      
      if (charIdx > 0) {
        result.push(' ');
      }
      result.push(morse);
    }
  }
  
  return result.join('');
}

/**
 * Decode Morse code to text
 * @param morse - Morse code string
 * @returns Decoded text
 * @throws Error if Morse code contains invalid symbols
 * @example
 * ```typescript
 * const text = decode('... --- ...');
 * // "SOS"
 * ```
 */
export function decode(morse: string): string {
  if (!morse) {
    return '';
  }
  
  const result: string[] = [];
  
  // Split by word separator (7 spaces or '/')
  const words = morse.split(/\s{7}|\/|\s*\/\s*/);
  
  for (let wordIdx = 0; wordIdx < words.length; wordIdx++) {
    const word = words[wordIdx];
    if (!word.trim()) continue;
    
    if (wordIdx > 0) {
      result.push(' ');
    }
    
    // Split by character separator (3 spaces)
    const chars = word.trim().split(/\s{3}|\s+/);
    
    for (const symbol of chars) {
      const trimmed = symbol.trim();
      if (!trimmed) continue;
      
      const char = MORSE_DECODE_MAP[trimmed];
      if (!char) {
        throw new Error(`Invalid Morse symbol: '${trimmed}'`);
      }
      result.push(char);
    }
  }
  
  return result.join('');
}

/**
 * Decode Morse code, skipping invalid symbols
 * @param morse - Morse code string
 * @returns Decoded text (invalid symbols skipped)
 */
export function decodeLenient(morse: string): string {
  if (!morse) {
    return '';
  }
  
  const result: string[] = [];
  const words = morse.split(/\s{7}|\/|\s*\/\s*/);
  
  for (let wordIdx = 0; wordIdx < words.length; wordIdx++) {
    const word = words[wordIdx];
    if (!word.trim()) continue;
    
    if (wordIdx > 0) {
      result.push(' ');
    }
    
    const chars = word.trim().split(/\s{3}|\s+/);
    
    for (const symbol of chars) {
      const trimmed = symbol.trim();
      if (!trimmed) continue;
      
      const char = MORSE_DECODE_MAP[trimmed];
      if (char) {
        result.push(char);
      }
    }
  }
  
  return result.join('');
}

/**
 * Get Morse code for a single character
 * @param char - Character to encode
 * @returns Morse code or null if invalid
 */
export function getMorseCode(char: string): string | null {
  const upper = char.toUpperCase();
  return MORSE_CODE_MAP[upper] ?? null;
}

/**
 * Get character for a Morse code symbol
 * @param morse - Morse code symbol
 * @returns Character or null if invalid
 */
export function getCharacter(morse: string): string | null {
  return MORSE_DECODE_MAP[morse] ?? null;
}

/**
 * Check if a character can be encoded to Morse
 * @param char - Character to check
 * @returns True if character is encodable
 */
export function isValidCharacter(char: string): boolean {
  return MORSE_CODE_MAP[char.toUpperCase()] !== undefined;
}

/**
 * Check if a string is valid Morse code
 * @param morse - String to check
 * @returns True if string contains only valid Morse symbols
 */
export function isValidMorse(morse: string): boolean {
  for (const char of morse) {
    if (char !== '.' && char !== '-' && char !== ' ' && char !== '/') {
      return false;
    }
  }
  return true;
}

/**
 * Check if text can be encoded to Morse
 * @param text - Text to check
 * @returns True if all characters are encodable
 */
export function canEncode(text: string): boolean {
  for (const char of text) {
    if (char === ' ') continue;
    if (!isValidCharacter(char)) {
      return false;
    }
  }
  return true;
}

/**
 * Convert Morse code to signal sequence
 * @param morse - Morse code string
 * @param config - Timing configuration (default: standard timing)
 * @returns Array of signal elements
 */
export function toSignals(morse: string, config?: MorseTimingConfig): MorseSignal[] {
  const timing = config ?? defaultTiming();
  const signals: MorseSignal[] = [];
  
  // Track if we just added a word gap (to skip spaces after slash)
  let lastWasWordGap = false;
  
  for (let i = 0; i < morse.length; i++) {
    const char = morse[i];
    
    switch (char) {
      case '.':
        signals.push({ on: true, durationMs: timing.dotDurationMs });
        signals.push({ on: false, durationMs: timing.symbolGapMs });
        lastWasWordGap = false;
        break;
      case '-':
        signals.push({ on: true, durationMs: timing.dashDurationMs });
        signals.push({ on: false, durationMs: timing.symbolGapMs });
        lastWasWordGap = false;
        break;
      case ' ':
        // Skip space if we just added a word gap
        if (lastWasWordGap) {
          continue;
        }
        
        // Remove trailing symbol gap and add appropriate gap
        if (signals.length > 0 && !signals[signals.length - 1].on) {
          signals.pop();
        }
        
        // Check for consecutive spaces to determine gap type
        let spaceCount = 0;
        for (let j = i; j < morse.length && morse[j] === ' '; j++) {
          spaceCount++;
        }
        
        if (spaceCount >= 7) {
          signals.push({ on: false, durationMs: timing.wordGapMs });
          i += spaceCount - 1; // Skip extra spaces
          lastWasWordGap = true;
        } else if (spaceCount >= 3) {
          signals.push({ on: false, durationMs: timing.charGapMs });
          i += spaceCount - 1; // Skip extra spaces
          lastWasWordGap = false;
        } else {
          signals.push({ on: false, durationMs: timing.symbolGapMs });
          lastWasWordGap = false;
        }
        break;
      case '/':
        // Word separator
        if (signals.length > 0 && !signals[signals.length - 1].on) {
          signals.pop();
        }
        signals.push({ on: false, durationMs: timing.wordGapMs });
        lastWasWordGap = true;
        break;
    }
  }
  
  // Remove trailing silence if present
  if (signals.length > 0 && !signals[signals.length - 1].on) {
    signals.pop();
  }
  
  return signals;
}

/**
 * Calculate total transmission duration
 * @param morse - Morse code string
 * @param config - Timing configuration (default: standard timing)
 * @returns Total duration in milliseconds
 */
export function getTotalDuration(morse: string, config?: MorseTimingConfig): number {
  const signals = toSignals(morse, config);
  return signals.reduce((total, signal) => total + signal.durationMs, 0);
}

/**
 * Convert Morse code to binary representation
 * (1 = signal on, 0 = signal off)
 * Each symbol has an implicit gap after it (represented as 0)
 * @param morse - Morse code string
 * @returns Binary string representation
 */
export function toBinary(morse: string): string {
  let result = '';
  let lastWasSymbol = false;
  
  for (const char of morse) {
    switch (char) {
      case '.':
        if (lastWasSymbol) {
          result += '0'; // Gap between symbols within a character
        }
        result += '1';
        lastWasSymbol = true;
        break;
      case '-':
        if (lastWasSymbol) {
          result += '0'; // Gap between symbols
        }
        result += '111';
        lastWasSymbol = true;
        break;
      case ' ':
        result += '0'; // Represents silence/gap
        lastWasSymbol = false;
        break;
      case '/':
        result += '0000000'; // Word separator
        lastWasSymbol = false;
        break;
    }
  }
  return result;
}

/**
 * Convert binary representation to Morse code
 * @param binary - Binary string
 * @returns Morse code string
 */
export function fromBinary(binary: string): string {
  let result = '';
  let i = 0;
  
  while (i < binary.length) {
    if (binary[i] === '1') {
      // Count consecutive 1s
      let count = 0;
      while (i < binary.length && binary[i] === '1') {
        count++;
        i++;
      }
      if (count === 1) {
        result += '.';
      } else if (count === 3) {
        result += '-';
      }
    } else {
      // Count consecutive 0s
      let count = 0;
      while (i < binary.length && binary[i] === '0') {
        count++;
        i++;
      }
      if (count >= 7) {
        result += '       ';
      } else if (count >= 3) {
        result += '   ';
      } else if (count > 0) {
        result += ' ';
      }
    }
  }
  
  return result;
}

/**
 * Analyze Morse code and return statistics
 * @param morse - Morse code string
 * @returns Analysis result
 */
export function analyze(morse: string): MorseAnalysis {
  let dotCount = 0;
  let dashCount = 0;
  let spaceCount = 0;
  
  for (const char of morse) {
    switch (char) {
      case '.':
        dotCount++;
        break;
      case '-':
        dashCount++;
        break;
      case ' ':
        spaceCount++;
        break;
    }
  }
  
  const words = morse.split(/\s{7}|\/|\s*\/\s*/).filter(w => w.trim());
  const characterCount = words.reduce((total, word) => {
    const chars = word.trim().split(/\s{3}|\s+/).filter(c => c.trim());
    return total + chars.length;
  }, 0);
  
  return {
    dotCount,
    dashCount,
    spaceCount,
    signalCount: dotCount + dashCount,
    characterCount,
    wordCount: words.length,
  };
}

/**
 * Normalize Morse code spacing
 * @param morse - Morse code string
 * @returns Normalized Morse code with standard spacing
 */
export function normalize(morse: string): string {
  const words = morse.split(/\s{7}|\/|\s*\/\s*/);
  const result: string[] = [];
  
  for (let wordIdx = 0; wordIdx < words.length; wordIdx++) {
    const word = words[wordIdx];
    if (!word.trim()) continue;
    
    if (wordIdx > 0) {
      result.push('       ');
    }
    
    const chars = word.trim().split(/\s{3}|\s+/);
    for (let charIdx = 0; charIdx < chars.length; charIdx++) {
      const charCode = chars[charIdx].trim();
      if (!charCode) continue;
      
      if (charIdx > 0) {
        result.push('   ');
      }
      result.push(charCode);
    }
  }
  
  return result.join('');
}

/**
 * Transpose Morse code (swap dots and dashes)
 * @param morse - Morse code string
 * @returns Transposed Morse code
 */
export function transpose(morse: string): string {
  let result = '';
  for (const char of morse) {
    switch (char) {
      case '.':
        result += '-';
        break;
      case '-':
        result += '.';
        break;
      default:
        result += char;
    }
  }
  return result;
}

/**
 * Get prosign by name
 * @param name - Prosign name
 * @returns Prosign or null if not found
 */
export function getProsign(name: string): Prosign | null {
  return PROSIGNS.find(p => p.name === name) ?? null;
}

/**
 * Check if Morse code is a prosign
 * @param code - Morse code to check
 * @returns True if code is a prosign
 */
export function isProsign(code: string): boolean {
  return PROSIGNS.some(p => p.code === code);
}

/**
 * Encode prosign by name
 * @param name - Prosign name
 * @returns Morse code or null if not found
 */
export function encodeProsign(name: string): string | null {
  const prosign = getProsign(name);
  return prosign?.code ?? null;
}

/**
 * Get all supported characters and their Morse codes
 * @returns Map of characters to Morse codes
 */
export function getAllCodes(): Record<string, string> {
  return { ...MORSE_CODE_MAP };
}

/**
 * Generate audio waveform samples for Morse code
 * @param morse - Morse code string
 * @param config - Timing configuration
 * @param sampleRate - Audio sample rate in Hz (default: 44100)
 * @returns Array of amplitude samples (values between -1 and 1)
 */
export function generateAudioWaveform(
  morse: string,
  config?: MorseTimingConfig,
  sampleRate: number = 44100
): number[] {
  const timing = config ?? defaultTiming();
  const signals = toSignals(morse, timing);
  const samples: number[] = [];
  
  for (const signal of signals) {
    const numSamples = Math.floor(signal.durationMs * sampleRate / 1000);
    
    if (signal.on) {
      // Generate sine wave
      for (let i = 0; i < numSamples; i++) {
        const t = i / sampleRate;
        // Apply simple envelope (fade out at end)
        const envelope = Math.min(1, Math.min(i / 100, (numSamples - i) / 100));
        const sample = envelope * Math.sin(2 * Math.PI * timing.frequencyHz * t);
        samples.push(sample);
      }
    } else {
      // Generate silence
      for (let i = 0; i < numSamples; i++) {
        samples.push(0);
      }
    }
  }
  
  return samples;
}

// ==================== Default Export ====================

/**
 * Morse Utilities namespace
 */
export const MorseUtils = {
  // Encoding
  encode,
  encodeStrict,
  getMorseCode,
  isValidCharacter,
  canEncode,
  
  // Decoding
  decode,
  decodeLenient,
  getCharacter,
  isValidMorse,
  
  // Timing
  defaultTiming,
  fastTiming,
  slowTiming,
  customTiming,
  wpmToDotDuration,
  dotDurationToWpm,
  
  // Signals & Audio
  toSignals,
  getTotalDuration,
  generateAudioWaveform,
  toBinary,
  fromBinary,
  
  // Analysis & Utilities
  analyze,
  normalize,
  transpose,
  getAllCodes,
  
  // Prosigns
  PROSIGNS,
  getProsign,
  isProsign,
  encodeProsign,
};

export default MorseUtils;