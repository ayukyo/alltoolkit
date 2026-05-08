/**
 * Credit Card Utilities Module for TypeScript
 * 
 * A comprehensive credit card validation and utility module
 * with zero external dependencies.
 * 
 * Features:
 * - Credit card number validation (Luhn algorithm)
 * - Card type detection (Visa, MasterCard, Amex, etc.)
 * - Card number formatting and masking
 * - CVV validation
 * - Expiry date validation
 * - BIN/IIN lookup helpers
 * - Zero dependencies, uses only TypeScript/JavaScript standard library
 * 
 * @module credit_card_utils
 * @version 1.0.0
 * @license MIT
 */

/**
 * Supported credit card types
 */
export enum CardType {
  VISA = 'VISA',
  MASTERCARD = 'MASTERCARD',
  AMEX = 'AMEX',
  DISCOVER = 'DISCOVER',
  DINERS_CLUB = 'DINERS_CLUB',
  JCB = 'JCB',
  UNIONPAY = 'UNIONPAY',
  MAESTRO = 'MAESTRO',
  MIR = 'MIR',
  UNKNOWN = 'UNKNOWN',
}

/**
 * Credit card information
 */
export interface CardInfo {
  /** Card type */
  type: CardType;
  /** Card type display name */
  displayName: string;
  /** Expected card number length(s) */
  lengths: number[];
  /** CVV length */
  cvvLength: number;
  /** Card number pattern (regex) */
  pattern: RegExp;
  /** BIN/IIN prefix range(s) */
  prefixes: string[];
}

/**
 * Card validation result
 */
export interface ValidationResult {
  /** Whether the card number is valid */
  valid: boolean;
  /** Card type if valid */
  cardType: CardType | null;
  /** Error message if invalid */
  error: string | null;
  /** Card info if valid */
  info: CardInfo | null;
}

/**
 * Expiry date validation result
 */
export interface ExpiryResult {
  /** Whether the expiry date is valid */
  valid: boolean;
  /** Error message if invalid */
  error: string | null;
  /** Parsed month (1-12) */
  month: number | null;
  /** Parsed year (4 digits) */
  year: number | null;
  /** Whether the card is expired */
  expired: boolean;
  /** Whether the card expires soon (within 30 days) */
  expiresSoon: boolean;
}

/**
 * Card type configurations
 */
const CARD_TYPES: Record<CardType, CardInfo> = {
  [CardType.VISA]: {
    type: CardType.VISA,
    displayName: 'Visa',
    lengths: [13, 16, 19],
    cvvLength: 3,
    pattern: /^4/,
    prefixes: ['4'],
  },
  [CardType.MASTERCARD]: {
    type: CardType.MASTERCARD,
    displayName: 'MasterCard',
    lengths: [16],
    cvvLength: 3,
    pattern: /^(5[1-5]|2[2-7])/,
    prefixes: ['51', '52', '53', '54', '55', '2221', '2222', '2223', '2224', '2225', '2226', '2227', '2228', '2229', '223', '224', '225', '226', '227', '228', '229', '23', '24', '25', '26', '270', '271', '2720'],
  },
  [CardType.AMEX]: {
    type: CardType.AMEX,
    displayName: 'American Express',
    lengths: [15],
    cvvLength: 4,
    pattern: /^3[47]/,
    prefixes: ['34', '37'],
  },
  [CardType.DISCOVER]: {
    type: CardType.DISCOVER,
    displayName: 'Discover',
    lengths: [16, 19],
    cvvLength: 3,
    pattern: /^(6011|65|64[4-9])/,
    prefixes: ['6011', '65', '644', '645', '646', '647', '648', '649'],
  },
  [CardType.DINERS_CLUB]: {
    type: CardType.DINERS_CLUB,
    displayName: 'Diners Club',
    lengths: [14, 16, 19],
    cvvLength: 3,
    pattern: /^(36|38|39|30[0-5])/,
    prefixes: ['36', '38', '39', '300', '301', '302', '303', '304', '305'],
  },
  [CardType.JCB]: {
    type: CardType.JCB,
    displayName: 'JCB',
    lengths: [16, 17, 18, 19],
    cvvLength: 3,
    pattern: /^35(2[89]|[3-8][0-9])/,
    prefixes: ['3528', '3529', '353', '354', '355', '356', '357', '358', '359'],
  },
  [CardType.UNIONPAY]: {
    type: CardType.UNIONPAY,
    displayName: 'UnionPay',
    lengths: [16, 17, 18, 19],
    cvvLength: 3,
    pattern: /^62/,
    prefixes: ['62'],
  },
  [CardType.MAESTRO]: {
    type: CardType.MAESTRO,
    displayName: 'Maestro',
    lengths: [12, 13, 14, 15, 16, 17, 18, 19],
    cvvLength: 3,
    pattern: /^(50|5[6-9]|6[0-9])/,
    prefixes: ['50', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69'],
  },
  [CardType.MIR]: {
    type: CardType.MIR,
    displayName: 'Mir',
    lengths: [16],
    cvvLength: 3,
    pattern: /^220[0-4]/,
    prefixes: ['2200', '2201', '2202', '2203', '2204'],
  },
  [CardType.UNKNOWN]: {
    type: CardType.UNKNOWN,
    displayName: 'Unknown',
    lengths: [],
    cvvLength: 3,
    pattern: /^/,
    prefixes: [],
  },
};

/**
 * Order of card type detection (most specific first)
 */
const DETECTION_ORDER: CardType[] = [
  CardType.AMEX,
  CardType.DINERS_CLUB,
  CardType.JCB,
  CardType.DISCOVER,
  CardType.MIR,
  CardType.UNIONPAY,
  CardType.MASTERCARD,
  CardType.MAESTRO,
  CardType.VISA,
];

// ==================== Utility Functions ====================

/**
 * Remove non-digit characters from card number
 * @param cardNumber - Card number string
 * @returns Digits only
 */
export function sanitize(cardNumber: string): string {
  return cardNumber.replace(/\D/g, '');
}

/**
 * Format card number with spaces
 * @param cardNumber - Card number (digits only or formatted)
 * @param format - Format pattern (default: standard 4-digit groups)
 * @returns Formatted card number
 */
export function format(cardNumber: string, format?: string): string {
  const digits = sanitize(cardNumber);
  const cardType = detectCardType(digits);
  const info = CARD_TYPES[cardType];
  
  // Amex has different formatting (4-6-5)
  if (cardType === CardType.AMEX) {
    return digits.replace(/(\d{4})(\d{6})(\d{5})/, '$1 $2 $3').trim();
  }
  
  // Standard 4-digit groups
  return digits.replace(/(\d{4})(?=\d)/g, '$1 ').trim();
}

/**
 * Mask card number for display
 * @param cardNumber - Card number (digits only or formatted)
 * @param visibleStart - Number of digits visible at start (default: 4)
 * @param visibleEnd - Number of digits visible at end (default: 4)
 * @param maskChar - Character to use for masking (default: '*')
 * @returns Masked card number
 */
export function mask(
  cardNumber: string,
  visibleStart: number = 4,
  visibleEnd: number = 4,
  maskChar: string = '*'
): string {
  const digits = sanitize(cardNumber);
  if (digits.length <= visibleStart + visibleEnd) {
    return digits;
  }
  
  const start = digits.slice(0, visibleStart);
  const end = digits.slice(-visibleEnd);
  const maskedLength = digits.length - visibleStart - visibleEnd;
  const masked = maskChar.repeat(maskedLength);
  
  return `${start}${masked}${end}`;
}

/**
 * Mask card number with format (includes spaces)
 * @param cardNumber - Card number
 * @param visibleStart - Digits visible at start
 * @param visibleEnd - Digits visible at end
 * @param maskChar - Masking character
 * @returns Formatted and masked card number
 */
export function maskFormatted(
  cardNumber: string,
  visibleStart: number = 4,
  visibleEnd: number = 4,
  maskChar: string = '*'
): string {
  const masked = mask(cardNumber, visibleStart, visibleEnd, maskChar);
  return format(masked);
}

// ==================== Validation Functions ====================

/**
 * Implement the Luhn algorithm to validate card number
 * @param cardNumber - Card number (digits only)
 * @returns True if valid according to Luhn algorithm
 */
export function luhnCheck(cardNumber: string): boolean {
  const digits = sanitize(cardNumber);
  if (!digits || !/^\d+$/.test(digits)) {
    return false;
  }
  
  let sum = 0;
  let isEven = false;
  
  // Iterate from right to left
  for (let i = digits.length - 1; i >= 0; i--) {
    let digit = parseInt(digits[i], 10);
    
    if (isEven) {
      digit *= 2;
      if (digit > 9) {
        digit -= 9;
      }
    }
    
    sum += digit;
    isEven = !isEven;
  }
  
  return sum % 10 === 0;
}

/**
 * Calculate the Luhn check digit
 * @param partialCardNumber - Card number without check digit
 * @returns Check digit (0-9)
 */
export function calculateLuhnCheckDigit(partialCardNumber: string): number {
  const digits = sanitize(partialCardNumber);
  if (!/^\d+$/.test(digits)) {
    throw new Error('Partial card number must contain only digits');
  }
  
  // In Luhn algorithm:
  // - We process from right to left
  // - The check digit (position 0) is NOT doubled
  // - Position 1 (second from right) IS doubled
  // - Positions alternate: odd positions doubled, even positions not doubled
  // 
  // For a partial number (without check digit), all digits are at positions 1, 2, 3, ...
  // So position 1 (rightmost of partial) should be doubled, position 2 not doubled, etc.
  // This means: from right to left, first digit (of partial) is doubled, second not, third doubled, etc.
  
  let sum = 0;
  const n = digits.length;
  
  // Process from right to left (positions 1, 2, 3, ... relative to full number)
  // Position 1 (rightmost of partial) should be doubled (odd position)
  // Position 2 should not be doubled (even position)
  // Position 3 should be doubled (odd position)
  // etc.
  
  for (let i = n - 1; i >= 0; i--) {
    let digit = parseInt(digits[i], 10);
    // Position relative to full number (with check digit at position 0)
    const position = (n - i); // position from right, starting at 1
    
    // Odd positions (1, 3, 5...) are doubled
    if (position % 2 === 1) {
      digit *= 2;
      if (digit > 9) {
        digit -= 9;
      }
    }
    
    sum += digit;
  }
  
  const checkDigit = (10 - (sum % 10)) % 10;
  return checkDigit;
}

/**
 * Generate a valid test card number for a given card type
 * @param cardType - Card type to generate
 * @param preferLength - Preferred length (default: 16 for most cards, or first available)
 * @returns Valid test card number
 */
export function generateTestNumber(cardType: CardType, preferLength?: number): string {
  const info = CARD_TYPES[cardType];
  if (cardType === CardType.UNKNOWN || info.prefixes.length === 0) {
    throw new Error('Cannot generate test number for unknown card type');
  }
  
  const prefix = info.prefixes[0];
  
  // Choose target length: prefer 16 if available, otherwise first available, or preferLength if specified
  let targetLength = info.lengths.includes(16) ? 16 : info.lengths[0];
  if (preferLength && info.lengths.includes(preferLength)) {
    targetLength = preferLength;
  }
  
  // For Amex, always use 15
  if (cardType === CardType.AMEX) {
    targetLength = 15;
  }
  
  const remainingLength = targetLength - prefix.length - 1; // -1 for check digit
  
  // Generate random digits for remaining positions
  let number = prefix;
  for (let i = 0; i < remainingLength; i++) {
    number += Math.floor(Math.random() * 10).toString();
  }
  
  // Calculate and append check digit
  const checkDigit = calculateLuhnCheckDigit(number);
  return number + checkDigit.toString();
}

/**
 * Detect card type from card number
 * @param cardNumber - Card number (digits only or formatted)
 * @returns Detected card type
 */
export function detectCardType(cardNumber: string): CardType {
  const digits = sanitize(cardNumber);
  if (!digits) {
    return CardType.UNKNOWN;
  }
  
  for (const cardType of DETECTION_ORDER) {
    const info = CARD_TYPES[cardType];
    if (info.pattern.test(digits)) {
      return cardType;
    }
  }
  
  return CardType.UNKNOWN;
}

/**
 * Check if card number length is valid for detected card type
 * @param cardNumber - Card number (digits only)
 * @returns True if length is valid
 */
export function isValidLength(cardNumber: string): boolean {
  const digits = sanitize(cardNumber);
  const cardType = detectCardType(digits);
  const info = CARD_TYPES[cardType];
  
  return info.lengths.includes(digits.length);
}

/**
 * Validate card number format (digits only, proper length)
 * @param cardNumber - Card number
 * @returns True if format is valid
 */
export function isValidFormat(cardNumber: string): boolean {
  const digits = sanitize(cardNumber);
  return /^\d+$/.test(digits) && digits.length >= 12 && digits.length <= 19;
}

/**
 * Comprehensive card number validation
 * @param cardNumber - Card number (digits only or formatted)
 * @returns Validation result
 */
export function validate(cardNumber: string): ValidationResult {
  const digits = sanitize(cardNumber);
  
  // Check for empty
  if (!digits) {
    return {
      valid: false,
      cardType: null,
      error: 'Card number is empty',
      info: null,
    };
  }
  
  // Check for non-digits
  if (!/^\d+$/.test(digits)) {
    return {
      valid: false,
      cardType: null,
      error: 'Card number contains invalid characters',
      info: null,
    };
  }
  
  // Check length
  if (digits.length < 12 || digits.length > 19) {
    return {
      valid: false,
      cardType: null,
      error: 'Card number length is invalid (must be 12-19 digits)',
      info: null,
    };
  }
  
  // Detect card type
  const cardType = detectCardType(digits);
  const info = CARD_TYPES[cardType];
  
  // Check specific length for card type
  if (cardType !== CardType.UNKNOWN && !info.lengths.includes(digits.length)) {
    return {
      valid: false,
      cardType,
      error: `Invalid length for ${info.displayName} (expected ${info.lengths.join(' or ')} digits, got ${digits.length})`,
      info: null,
    };
  }
  
  // Check Luhn algorithm
  if (!luhnCheck(digits)) {
    return {
      valid: false,
      cardType,
      error: 'Card number fails Luhn check',
      info: null,
    };
  }
  
  return {
    valid: true,
    cardType,
    error: null,
    info,
  };
}

/**
 * Validate CVV (Card Verification Value)
 * @param cvv - CVV code
 * @param cardType - Optional card type for specific validation
 * @returns True if CVV is valid
 */
export function isValidCVV(cvv: string, cardType?: CardType): boolean {
  const sanitized = cvv.replace(/\D/g, '');
  if (!/^\d{3,4}$/.test(sanitized)) {
    return false;
  }
  
  if (cardType) {
    const expectedLength = CARD_TYPES[cardType].cvvLength;
    return sanitized.length === expectedLength;
  }
  
  return true;
}

/**
 * Validate expiry date
 * @param month - Month (1-12 or '01'-'12')
 * @param year - Year (2 or 4 digits)
 * @returns Expiry validation result
 */
export function validateExpiry(month: string | number, year: string | number): ExpiryResult {
  // Parse month
  const monthNum = typeof month === 'string' ? parseInt(month, 10) : month;
  const yearNum = typeof year === 'string' ? parseInt(year, 10) : year;
  
  // Validate month
  if (isNaN(monthNum) || monthNum < 1 || monthNum > 12) {
    return {
      valid: false,
      error: 'Invalid month (must be 1-12)',
      month: null,
      year: null,
      expired: false,
      expiresSoon: false,
    };
  }
  
  // Validate year
  if (isNaN(yearNum) || yearNum < 0) {
    return {
      valid: false,
      error: 'Invalid year',
      month: null,
      year: null,
      expired: false,
      expiresSoon: false,
    };
  }
  
  // Normalize year to 4 digits
  const fullYear = yearNum < 100 ? 2000 + yearNum : yearNum;
  
  // Get current date
  const now = new Date();
  const currentYear = now.getFullYear();
  const currentMonth = now.getMonth() + 1; // 0-indexed
  
  // Check if expired (last day of expiry month)
  const isExpired = fullYear < currentYear || 
    (fullYear === currentYear && monthNum < currentMonth);
  
  // Check if expires soon (within 30 days)
  const expiryDate = new Date(fullYear, monthNum, 0); // Last day of month
  const daysUntilExpiry = Math.floor((expiryDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
  const expiresSoon = !isExpired && daysUntilExpiry <= 30 && daysUntilExpiry >= 0;
  
  return {
    valid: true,
    error: null,
    month: monthNum,
    year: fullYear,
    expired: isExpired,
    expiresSoon,
  };
}

/**
 * Validate expiry date from string (MM/YY or MM/YYYY format)
 * @param expiry - Expiry date string
 * @returns Expiry validation result
 */
export function validateExpiryString(expiry: string): ExpiryResult {
  const cleaned = expiry.replace(/\s+/g, '');
  const match = cleaned.match(/^(\d{1,2})[\/\-](\d{2,4})$/);
  
  if (!match) {
    return {
      valid: false,
      error: 'Invalid expiry format (expected MM/YY or MM/YYYY)',
      month: null,
      year: null,
      expired: false,
      expiresSoon: false,
    };
  }
  
  return validateExpiry(match[1], match[2]);
}

// ==================== BIN/IIN Functions ====================

/**
 * Get BIN (Bank Identification Number) from card number
 * @param cardNumber - Card number
 * @param length - BIN length (default: 6)
 * @returns BIN or null if card number is too short
 */
export function getBIN(cardNumber: string, length: number = 6): string | null {
  const digits = sanitize(cardNumber);
  if (digits.length < length) {
    return null;
  }
  return digits.slice(0, length);
}

/**
 * Check if a BIN is in a valid range
 * @param bin - BIN to check
 * @returns True if BIN is valid (6-8 digits)
 */
export function isValidBIN(bin: string): boolean {
  const digits = sanitize(bin);
  return /^\d{6,8}$/.test(digits);
}

// ==================== Card Info Functions ====================

/**
 * Get card info for a card type
 * @param cardType - Card type
 * @returns Card info or null if unknown
 */
export function getCardInfo(cardType: CardType): CardInfo | null {
  const info = CARD_TYPES[cardType];
  return info.type === CardType.UNKNOWN ? null : { ...info };
}

/**
 * Get all supported card types
 * @returns Array of card type info
 */
export function getAllCardTypes(): CardInfo[] {
  return Object.values(CARD_TYPES).filter(info => info.type !== CardType.UNKNOWN);
}

/**
 * Check if a card type is supported
 * @param cardType - Card type to check
 * @returns True if card type is supported
 */
export function isCardTypeSupported(cardType: string): boolean {
  return cardType.toUpperCase() in CardType && cardType.toUpperCase() !== 'UNKNOWN';
}

// ==================== Convenience Functions ====================

/**
 * Quick check if card number is valid
 * @param cardNumber - Card number
 * @returns True if valid
 */
export function isValid(cardNumber: string): boolean {
  return validate(cardNumber).valid;
}

/**
 * Get card type name from card number
 * @param cardNumber - Card number
 * @returns Card type display name
 */
export function getCardTypeName(cardNumber: string): string {
  const cardType = detectCardType(cardNumber);
  return CARD_TYPES[cardType].displayName;
}

// ==================== Default Export ====================

/**
 * Credit Card Utilities namespace
 */
export const CreditCardUtils = {
  // Sanitization & Formatting
  sanitize,
  format,
  mask,
  maskFormatted,
  
  // Validation
  validate,
  isValid,
  isValidFormat,
  isValidLength,
  luhnCheck,
  calculateLuhnCheckDigit,
  
  // Card Type Detection
  detectCardType,
  getCardInfo,
  getCardTypeName,
  getAllCardTypes,
  isCardTypeSupported,
  
  // CVV Validation
  isValidCVV,
  
  // Expiry Validation
  validateExpiry,
  validateExpiryString,
  
  // BIN/IIN
  getBIN,
  isValidBIN,
  
  // Test Data
  generateTestNumber,
  
  // Types
  CardType,
};

export default CreditCardUtils;