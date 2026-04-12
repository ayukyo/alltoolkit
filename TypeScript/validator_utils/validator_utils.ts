/**
 * Validator Utilities Module for TypeScript
 * 
 * A comprehensive data validation utility module with zero dependencies.
 * Provides common validation functions for emails, phones, URLs, IDs, and more.
 * 
 * Features:
 * - Email validation
 * - Phone number validation (international)
 * - URL validation
 * - IP address validation (IPv4/IPv6)
 * - ID card validation (Chinese, US SSN)
 * - Credit card validation (Luhn algorithm)
 * - Date/time validation
 * - String length validation
 * - Pattern matching validation
 * - Zero dependencies, uses only TypeScript/JavaScript standard library
 * 
 * @module validator_utils
 * @version 1.0.0
 * @license MIT
 */

// =============================================================================
// Type Definitions
// =============================================================================

/**
 * Validation result interface
 */
export interface ValidationResult {
  /** Whether the validation passed */
  valid: boolean;
  /** Error message if validation failed */
  error?: string;
  /** Additional data extracted during validation */
  data?: Record<string, unknown>;
}

/**
 * Email validation options
 */
export interface EmailOptions {
  /** Allow IP addresses as domain (e.g., user@[192.168.1.1]) */
  allowIpDomain?: boolean;
  /** Require TLD (top-level domain) */
  requireTld?: boolean;
  /** Maximum length for email */
  maxLength?: number;
}

/**
 * Phone validation options
 */
export interface PhoneOptions {
  /** Country code (e.g., 'CN', 'US', 'UK') */
  countryCode?: string;
  /** Allow international format with country code */
  allowInternational?: boolean;
  /** Strict mode - enforce exact format */
  strict?: boolean;
}

/**
 * URL validation options
 */
export interface UrlOptions {
  /** Allowed protocols */
  protocols?: string[];
  /** Require protocol */
  requireProtocol?: boolean;
  /** Allow IP addresses as host */
  allowIp?: boolean;
  /** Require TLD */
  requireTld?: boolean;
}

/**
 * Date validation options
 */
export interface DateOptions {
  /** Expected date format */
  format?: string;
  /** Minimum date */
  min?: Date;
  /** Maximum date */
  max?: Date;
}

/**
 * String validation options
 */
export interface StringOptions {
  /** Minimum length */
  minLength?: number;
  /** Maximum length */
  maxLength?: number;
  /** Exact length */
  exactLength?: number;
  /** Allow empty string */
  allowEmpty?: boolean;
  /** Trim before validation */
  trim?: boolean;
}

// =============================================================================
// Email Validation
// =============================================================================

/**
 * RFC 5322 compliant email regex (simplified for practical use)
 */
const EMAIL_REGEX = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

/**
 * Email with IP domain regex
 */
const EMAIL_IP_REGEX = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@\[(?:\d{1,3}\.){3}\d{1,3}\]$/;

/**
 * Validate an email address
 * 
 * @param email - The email address to validate
 * @param options - Validation options
 * @returns ValidationResult with validation status
 * 
 * @example
 * ```typescript
 * validateEmail('user@example.com')
 * // { valid: true }
 * 
 * validateEmail('invalid-email')
 * // { valid: false, error: 'Invalid email format' }
 * ```
 */
export function validateEmail(email: string, options: EmailOptions = {}): ValidationResult {
  const {
    allowIpDomain = false,
    requireTld = true,
    maxLength = 254
  } = options;

  // Check if null or undefined
  if (email == null) {
    return { valid: false, error: 'Email is required' };
  }

  // Convert to string and trim
  const str = String(email).trim();

  // Check length
  if (str.length === 0) {
    return { valid: false, error: 'Email cannot be empty' };
  }

  if (str.length > maxLength) {
    return { valid: false, error: `Email exceeds maximum length of ${maxLength}` };
  }

  // Check for @ symbol
  if (!str.includes('@')) {
    return { valid: false, error: 'Email must contain @ symbol' };
  }

  // Split into local and domain parts
  const parts = str.split('@');
  if (parts.length !== 2) {
    return { valid: false, error: 'Email must contain exactly one @ symbol' };
  }

  const [local, domain] = parts;

  // Validate local part
  if (local.length === 0 || local.length > 64) {
    return { valid: false, error: 'Invalid email local part' };
  }

  // Check for consecutive dots
  if (local.includes('..')) {
    return { valid: false, error: 'Email cannot contain consecutive dots' };
  }

  // Validate domain part
  if (domain.length === 0) {
    return { valid: false, error: 'Email domain cannot be empty' };
  }

  // Check for IP domain
  if (domain.startsWith('[') && domain.endsWith(']')) {
    if (!allowIpDomain) {
      return { valid: false, error: 'IP domain not allowed' };
    }
    const ip = domain.slice(1, -1);
    const ipResult = validateIPv4(ip);
    if (!ipResult.valid) {
      return { valid: false, error: 'Invalid IP address in domain' };
    }
    return { valid: true, data: { local, domain: ip, type: 'ip' } };
  }

  // Validate domain format
  if (domain.startsWith('.') || domain.endsWith('.')) {
    return { valid: false, error: 'Domain cannot start or end with a dot' };
  }

  if (domain.includes('..')) {
    return { valid: false, error: 'Domain cannot contain consecutive dots' };
  }

  // Check TLD requirement
  if (requireTld) {
    const tldParts = domain.split('.');
    if (tldParts.length < 2 || tldParts[tldParts.length - 1].length < 2) {
      return { valid: false, error: 'Email must have a valid TLD' };
    }
  }

  // Final regex validation
  const regex = allowIpDomain ? EMAIL_REGEX : EMAIL_REGEX;
  if (!regex.test(str)) {
    return { valid: false, error: 'Invalid email format' };
  }

  return { valid: true, data: { local, domain, type: 'standard' } };
}

// =============================================================================
// Phone Number Validation
// =============================================================================

/**
 * Country-specific phone regex patterns
 */
const PHONE_PATTERNS: Record<string, RegExp> = {
  // China: 11 digits starting with 1
  CN: /^(\+86)?1[3-9]\d{9}$/,
  // US/Canada: 10 digits with optional country code
  US: /^(\+1)?[2-9]\d{2}[2-9]\d{6}$/,
  // UK: Various formats
  UK: /^(\+44)?[1-9]\d{9,10}$/,
  // Japan: Various formats
  JP: /^(\+81)?[1-9]\d{9,10}$/,
  // Germany: Various formats
  DE: /^(\+49)?[1-9]\d{9,11}$/,
  // France: Various formats
  FR: /^(\+33)?[1-9]\d{8}$/,
  // Australia: Various formats
  AU: /^(\+61)?[1-9]\d{8,9}$/,
  // India: 10 digits starting with 6-9
  IN: /^(\+91)?[6-9]\d{9}$/,
  // Brazil: Various formats
  BR: /^(\+55)?[1-9]\d{10}$/,
  // Russia: 11 digits starting with 7 or 8
  RU: /^(\+7)?[789]\d{10}$/,
};

/**
 * International phone regex (flexible)
 */
const INTERNATIONAL_PHONE_REGEX = /^\+?[1-9]\d{6,14}$/;

/**
 * Validate a phone number
 * 
 * @param phone - The phone number to validate
 * @param options - Validation options
 * @returns ValidationResult with validation status
 * 
 * @example
 * ```typescript
 * validatePhone('13800138000', { countryCode: 'CN' })
 * // { valid: true }
 * 
 * validatePhone('+1-555-123-4567', { allowInternational: true })
 * // { valid: true }
 * ```
 */
export function validatePhone(phone: string, options: PhoneOptions = {}): ValidationResult {
  const {
    countryCode,
    allowInternational = true,
    strict = false
  } = options;

  // Check if null or undefined
  if (phone == null) {
    return { valid: false, error: 'Phone number is required' };
  }

  // Convert to string and remove common separators
  const str = String(phone).replace(/[\s\-\.\(\)]/g, '');

  // Check if empty
  if (str.length === 0) {
    return { valid: false, error: 'Phone number cannot be empty' };
  }

  // Remove leading + for length check
  const digitsOnly = str.replace(/\+/g, '');
  
  // Check if all digits
  if (!/^\+?\d+$/.test(str)) {
    return { valid: false, error: 'Phone number must contain only digits and optional +' };
  }

  // Country-specific validation
  if (countryCode) {
    const code = countryCode.toUpperCase();
    const pattern = PHONE_PATTERNS[code];
    
    if (pattern) {
      if (!pattern.test(str)) {
        return { 
          valid: false, 
          error: `Invalid phone number format for country ${code}` 
        };
      }
      return { valid: true, data: { countryCode: code, original: str } };
    }
  }

  // International format validation
  if (allowInternational) {
    if (!INTERNATIONAL_PHONE_REGEX.test(str)) {
      return { valid: false, error: 'Invalid international phone number format' };
    }
    
    // E.164 standard: max 15 digits
    if (digitsOnly.length > 15) {
      return { valid: false, error: 'Phone number exceeds maximum length (15 digits)' };
    }
    
    if (digitsOnly.length < 7) {
      return { valid: false, error: 'Phone number too short' };
    }

    return { 
      valid: true, 
      data: { 
        international: str.startsWith('+'),
        digits: digitsOnly,
        length: digitsOnly.length
      } 
    };
  }

  // Strict mode: require exact 10-11 digits
  if (strict) {
    if (digitsOnly.length < 10 || digitsOnly.length > 11) {
      return { valid: false, error: 'Phone number must be 10-11 digits' };
    }
  }

  return { valid: true, data: { digits: digitsOnly } };
}

// =============================================================================
// URL Validation
// =============================================================================

/**
 * URL regex pattern
 */
const URL_REGEX = /^(?:https?:\/\/)?(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)$/;

/**
 * Validate a URL
 * 
 * @param url - The URL to validate
 * @param options - Validation options
 * @returns ValidationResult with validation status
 * 
 * @example
 * ```typescript
 * validateUrl('https://example.com/path')
 * // { valid: true }
 * 
 * validateUrl('ftp://files.example.com', { protocols: ['http', 'https'] })
 * // { valid: false, error: 'Protocol not allowed' }
 * ```
 */
export function validateUrl(url: string, options: UrlOptions = {}): ValidationResult {
  const {
    protocols = ['http', 'https'],
    requireProtocol = true,
    allowIp = true,
    requireTld = true
  } = options;

  // Check if null or undefined
  if (url == null) {
    return { valid: false, error: 'URL is required' };
  }

  const str = String(url).trim();

  // Check if empty
  if (str.length === 0) {
    return { valid: false, error: 'URL cannot be empty' };
  }

  // Check max length
  if (str.length > 2048) {
    return { valid: false, error: 'URL exceeds maximum length (2048 characters)' };
  }

  // Parse URL components
  let protocol = '';
  let host = '';
  let pathname = '';
  let search = '';
  let hash = '';

  try {
    // Try using URL constructor if available
    const urlObj = new URL(str.startsWith('http') || str.startsWith('ftp') ? str : `http://${str}`);
    protocol = urlObj.protocol.replace(':', '');
    host = urlObj.hostname;
    pathname = urlObj.pathname;
    search = urlObj.search;
    hash = urlObj.hash;
  } catch {
    // Fallback to regex parsing
    const match = str.match(URL_REGEX);
    if (!match) {
      return { valid: false, error: 'Invalid URL format' };
    }
  }

  // Validate protocol
  if (requireProtocol && !protocol) {
    return { valid: false, error: 'URL must include protocol (http:// or https://)' };
  }

  if (protocol && !protocols.includes(protocol.toLowerCase())) {
    return { valid: false, error: `Protocol '${protocol}' not allowed. Allowed: ${protocols.join(', ')}` };
  }

  // Validate host
  if (!host) {
    return { valid: false, error: 'URL must have a host' };
  }

  // Check if IP address
  const isIp = /^(\d{1,3}\.){3}\d{1,3}$/.test(host) || host.includes(':');
  
  if (isIp && !allowIp) {
    return { valid: false, error: 'IP addresses are not allowed as URL host' };
  }

  // Validate TLD
  if (requireTld && !isIp) {
    const tldParts = host.split('.');
    if (tldParts.length < 2 || tldParts[tldParts.length - 1].length < 2) {
      return { valid: false, error: 'URL must have a valid TLD' };
    }
  }

  return {
    valid: true,
    data: {
      protocol,
      host,
      pathname,
      search,
      hash,
      isIp,
      full: str
    }
  };
}

// =============================================================================
// IP Address Validation
// =============================================================================

/**
 * IPv4 regex pattern
 */
const IPV4_REGEX = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;

/**
 * IPv6 regex pattern (simplified)
 */
const IPV6_REGEX = /^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^([0-9a-fA-F]{1,4}:){1,7}:$|^([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}$|^([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}$|^([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}$|^([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}$|^([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}$|^[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6}|:)$|^:((:[0-9a-fA-F]{1,4}){1,7}|:)$/;

/**
 * Validate an IPv4 address
 * 
 * @param ip - The IPv4 address to validate
 * @returns ValidationResult with validation status
 * 
 * @example
 * ```typescript
 * validateIPv4('192.168.1.1')
 * // { valid: true }
 * 
 * validateIPv4('256.1.1.1')
 * // { valid: false, error: 'Invalid IPv4 octet' }
 * ```
 */
export function validateIPv4(ip: string): ValidationResult {
  if (ip == null || typeof ip !== 'string') {
    return { valid: false, error: 'IP address is required' };
  }

  const str = ip.trim();
  const match = str.match(IPV4_REGEX);

  if (!match) {
    return { valid: false, error: 'Invalid IPv4 format' };
  }

  // Validate each octet
  for (let i = 1; i <= 4; i++) {
    const octet = parseInt(match[i], 10);
    if (octet < 0 || octet > 255) {
      return { valid: false, error: `Invalid IPv4 octet: ${match[i]}` };
    }
  }

  // Check for leading zeros (optional strict validation)
  for (let i = 1; i <= 4; i++) {
    if (match[i].length > 1 && match[i].startsWith('0')) {
      return { valid: false, error: 'IPv4 octets should not have leading zeros' };
    }
  }

  return {
    valid: true,
    data: {
      version: 4,
      octets: [parseInt(match[1]), parseInt(match[2]), parseInt(match[3]), parseInt(match[4])],
      isPrivate: isPrivateIPv4(str)
    }
  };
}

/**
 * Check if an IPv4 address is private
 */
function isPrivateIPv4(ip: string): boolean {
  const octets = ip.split('.').map(Number);
  
  // 10.0.0.0/8
  if (octets[0] === 10) return true;
  
  // 172.16.0.0/12
  if (octets[0] === 172 && octets[1] >= 16 && octets[1] <= 31) return true;
  
  // 192.168.0.0/16
  if (octets[0] === 192 && octets[1] === 168) return true;
  
  // 127.0.0.0/8 (loopback)
  if (octets[0] === 127) return true;

  return false;
}

/**
 * Validate an IPv6 address
 * 
 * @param ip - The IPv6 address to validate
 * @returns ValidationResult with validation status
 * 
 * @example
 * ```typescript
 * validateIPv6('2001:0db8:85a3:0000:0000:8a2e:0370:7334')
 * // { valid: true }
 * ```
 */
export function validateIPv6(ip: string): ValidationResult {
  if (ip == null || typeof ip !== 'string') {
    return { valid: false, error: 'IP address is required' };
  }

  const str = ip.trim();

  if (!IPV6_REGEX.test(str)) {
    // Try with :: compression
    const compressedRegex = /^::1$|^::$/;
    if (!compressedRegex.test(str)) {
      return { valid: false, error: 'Invalid IPv6 format' };
    }
  }

  return {
    valid: true,
    data: {
      version: 6,
      compressed: str.includes('::'),
      full: str
    }
  };
}

/**
 * Validate an IP address (IPv4 or IPv6)
 * 
 * @param ip - The IP address to validate
 * @param version - IP version (4, 6, or 'any')
 * @returns ValidationResult with validation status
 */
export function validateIP(ip: string, version: 4 | 6 | 'any' = 'any'): ValidationResult {
  if (version === 4 || version === 'any') {
    const result = validateIPv4(ip);
    if (result.valid && (version === 4 || version === 'any')) {
      return result;
    }
  }

  if (version === 6 || version === 'any') {
    const result = validateIPv6(ip);
    if (result.valid) {
      return result;
    }
  }

  return { valid: false, error: `Invalid IP address${version !== 'any' ? ` (v${version})` : ''}` };
}

// =============================================================================
// ID Card Validation
// =============================================================================

/**
 * Validate Chinese ID card (18 digits)
 * 
 * @param idCard - The ID card number to validate
 * @returns ValidationResult with validation status
 * 
 * @example
 * ```typescript
 * validateChineseIdCard('110101199001011234')
 * // { valid: true }
 * ```
 */
export function validateChineseIdCard(idCard: string): ValidationResult {
  if (idCard == null || typeof idCard !== 'string') {
    return { valid: false, error: 'ID card number is required' };
  }

  const str = idCard.trim().toUpperCase();

  // Check length
  if (str.length !== 18) {
    return { valid: false, error: 'Chinese ID card must be 18 characters' };
  }

  // Check format: 17 digits + 1 check digit (0-9 or X)
  const formatRegex = /^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dX]$/;
  
  if (!formatRegex.test(str)) {
    return { valid: false, error: 'Invalid Chinese ID card format' };
  }

  // Validate check digit using Luhn-like algorithm
  const weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];
  const checkCodes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'];

  let sum = 0;
  for (let i = 0; i < 17; i++) {
    sum += parseInt(str[i], 10) * weights[i];
  }

  const expectedCheck = checkCodes[sum % 11];
  const actualCheck = str[17];

  if (expectedCheck !== actualCheck) {
    return { valid: false, error: 'Invalid Chinese ID card check digit' };
  }

  // Extract birthdate
  const year = parseInt(str.substring(6, 10), 10);
  const month = parseInt(str.substring(10, 12), 10);
  const day = parseInt(str.substring(12, 14), 10);

  // Validate birthdate
  const birthdate = new Date(year, month - 1, day);
  if (birthdate.getFullYear() !== year || 
      birthdate.getMonth() !== month - 1 || 
      birthdate.getDate() !== day) {
    return { valid: false, error: 'Invalid birthdate in ID card' };
  }

  // Extract region code (first 6 digits)
  const regionCode = str.substring(0, 6);

  return {
    valid: true,
    data: {
      type: 'chinese',
      regionCode,
      birthdate: `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`,
      gender: parseInt(str[16], 10) % 2 === 1 ? 'male' : 'female'
    }
  };
}

/**
 * Validate US Social Security Number (SSN)
 * 
 * @param ssn - The SSN to validate
 * @returns ValidationResult with validation status
 */
export function validateUSSSN(ssn: string): ValidationResult {
  if (ssn == null || typeof ssn !== 'string') {
    return { valid: false, error: 'SSN is required' };
  }

  // Remove dashes and spaces
  const str = ssn.replace(/[-\s]/g, '');

  // Check length
  if (str.length !== 9) {
    return { valid: false, error: 'SSN must be 9 digits' };
  }

  // Check format
  if (!/^\d{9}$/.test(str)) {
    return { valid: false, error: 'SSN must contain only digits' };
  }

  // Validate area number (first 3 digits)
  const area = parseInt(str.substring(0, 3), 10);
  if (area === 0 || area === 666 || area > 899) {
    return { valid: false, error: 'Invalid SSN area number' };
  }

  // Validate group number (middle 2 digits)
  const group = parseInt(str.substring(3, 5), 10);
  if (group === 0) {
    return { valid: false, error: 'Invalid SSN group number' };
  }

  // Validate serial number (last 4 digits)
  const serial = parseInt(str.substring(5, 9), 10);
  if (serial === 0) {
    return { valid: false, error: 'Invalid SSN serial number' };
  }

  // Check for known invalid patterns
  const invalidPatterns = ['000', '666', '900', '901', '902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924', '925', '926', '927', '928', '929', '930', '931', '932', '933', '934', '935', '936', '937', '938', '939', '940', '941', '942', '943', '944', '945', '946', '947', '948', '949', '950', '951', '952', '953', '954', '955', '956', '957', '958', '959', '960', '961', '962', '963', '964', '965', '966', '967', '968', '969', '970', '971', '972', '973', '974', '975', '976', '977', '978', '979', '980', '981', '982', '983', '984', '985', '986', '987', '988', '989', '990', '991', '992', '993', '994', '995', '996', '997', '998', '999'];
  if (invalidPatterns.includes(str.substring(0, 3))) {
    return { valid: false, error: 'Invalid SSN area number' };
  }

  return {
    valid: true,
    data: {
      type: 'us-ssn',
      area: str.substring(0, 3),
      group: str.substring(3, 5),
      serial: str.substring(5, 9)
    }
  };
}

// =============================================================================
// Credit Card Validation
// =============================================================================

/**
 * Credit card number patterns by issuer
 */
const CARD_PATTERNS: Record<string, { pattern: RegExp; lengths: number[] }> = {
  visa: { pattern: /^4/, lengths: [13, 16, 19] },
  mastercard: { pattern: /^5[1-5]|^2[2-7]/, lengths: [16] },
  amex: { pattern: /^3[47]/, lengths: [15] },
  discover: { pattern: /^6(?:011|5)/, lengths: [16] },
  jcb: { pattern: /^35/, lengths: [16] },
  diners: { pattern: /^3(?:0[0-5]|[68])/, lengths: [14] },
};

/**
 * Validate a credit card number using Luhn algorithm
 * 
 * @param cardNumber - The card number to validate
 * @param issuer - Optional specific issuer to validate against
 * @returns ValidationResult with validation status
 * 
 * @example
 * ```typescript
 * validateCreditCard('4532015112830366')
 * // { valid: true, data: { issuer: 'visa', ... } }
 * ```
 */
export function validateCreditCard(cardNumber: string, issuer?: string): ValidationResult {
  if (cardNumber == null || typeof cardNumber !== 'string') {
    return { valid: false, error: 'Card number is required' };
  }

  // Remove spaces and dashes
  const str = cardNumber.replace(/[\s\-]/g, '');

  // Check if all digits
  if (!/^\d+$/.test(str)) {
    return { valid: false, error: 'Card number must contain only digits' };
  }

  // Check length
  if (str.length < 12 || str.length > 19) {
    return { valid: false, error: 'Card number length must be between 12 and 19 digits' };
  }

  // Detect issuer
  let detectedIssuer = 'unknown';
  let validLength = false;

  for (const [name, config] of Object.entries(CARD_PATTERNS)) {
    if (config.pattern.test(str)) {
      detectedIssuer = name;
      validLength = config.lengths.includes(str.length);
      break;
    }
  }

  // If specific issuer requested, validate against it
  if (issuer) {
    const issuerLower = issuer.toLowerCase();
    if (!CARD_PATTERNS[issuerLower]) {
      return { valid: false, error: `Unknown card issuer: ${issuer}` };
    }
    if (!CARD_PATTERNS[issuerLower].pattern.test(str)) {
      return { valid: false, error: `Card number does not match ${issuer} pattern` };
    }
    validLength = CARD_PATTERNS[issuerLower].lengths.includes(str.length);
    detectedIssuer = issuerLower;
  }

  if (!validLength) {
    return { valid: false, error: `Invalid card number length for ${detectedIssuer}` };
  }

  // Luhn algorithm validation
  let sum = 0;
  let isEven = false;

  // Loop through digits from right to left
  for (let i = str.length - 1; i >= 0; i--) {
    let digit = parseInt(str[i], 10);

    // Double every second digit
    if (isEven) {
      digit *= 2;
      if (digit > 9) {
        digit -= 9;
      }
    }

    sum += digit;
    isEven = !isEven;
  }

  if (sum % 10 !== 0) {
    return { valid: false, error: 'Invalid card number (failed Luhn check)' };
  }

  return {
    valid: true,
    data: {
      issuer: detectedIssuer,
      length: str.length,
      lastFour: str.slice(-4),
      bin: str.slice(0, 6)
    }
  };
}

// =============================================================================
// Date/Time Validation
// =============================================================================

/**
 * Common date format patterns
 */
const DATE_PATTERNS: Record<string, RegExp> = {
  'YYYY-MM-DD': /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/,
  'DD/MM/YYYY': /^(0[1-9]|[12]\d|3[01])\/(0[1-9]|1[0-2])\/\d{4}$/,
  'MM/DD/YYYY': /^(0[1-9]|1[0-2])\/(0[1-9]|[12]\d|3[01])\/\d{4}$/,
  'YYYY/MM/DD': /^\d{4}\/(0[1-9]|1[0-2])\/(0[1-9]|[12]\d|3[01])$/,
  'DD-MM-YYYY': /^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-\d{4}$/,
  'MM-DD-YYYY': /^(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])-\d{4}$/,
  'YYYYMMDD': /^\d{4}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])$/,
};

/**
 * Validate a date string
 * 
 * @param dateStr - The date string to validate
 * @param options - Validation options
 * @returns ValidationResult with validation status
 * 
 * @example
 * ```typescript
 * validateDate('2024-01-15', { format: 'YYYY-MM-DD' })
 * // { valid: true }
 * 
 * validateDate('2024-02-30', { format: 'YYYY-MM-DD' })
 * // { valid: false, error: 'Invalid date' }
 * ```
 */
export function validateDate(dateStr: string, options: DateOptions = {}): ValidationResult {
  const {
    format = 'YYYY-MM-DD',
    min,
    max
  } = options;

  if (dateStr == null || typeof dateStr !== 'string') {
    return { valid: false, error: 'Date is required' };
  }

  const str = dateStr.trim();

  // Check format pattern
  const pattern = DATE_PATTERNS[format];
  if (!pattern) {
    return { valid: false, error: `Unsupported date format: ${format}` };
  }

  if (!pattern.test(str)) {
    return { valid: false, error: `Date does not match format ${format}` };
  }

  // Parse date based on format
  let year: number, month: number, day: number;

  switch (format) {
    case 'YYYY-MM-DD':
      year = parseInt(str.substring(0, 4), 10);
      month = parseInt(str.substring(5, 7), 10);
      day = parseInt(str.substring(8, 10), 10);
      break;
    case 'YYYY/MM/DD':
      year = parseInt(str.substring(0, 4), 10);
      month = parseInt(str.substring(5, 7), 10);
      day = parseInt(str.substring(8, 10), 10);
      break;
    case 'YYYYMMDD':
      year = parseInt(str.substring(0, 4), 10);
      month = parseInt(str.substring(4, 6), 10);
      day = parseInt(str.substring(6, 8), 10);
      break;
    case 'DD/MM/YYYY':
      day = parseInt(str.substring(0, 2), 10);
      month = parseInt(str.substring(3, 5), 10);
      year = parseInt(str.substring(6, 10), 10);
      break;
    case 'DD-MM-YYYY':
      day = parseInt(str.substring(0, 2), 10);
      month = parseInt(str.substring(3, 5), 10);
      year = parseInt(str.substring(6, 10), 10);
      break;
    case 'MM/DD/YYYY':
      month = parseInt(str.substring(0, 2), 10);
      day = parseInt(str.substring(3, 5), 10);
      year = parseInt(str.substring(6, 10), 10);
      break;
    case 'MM-DD-YYYY':
      month = parseInt(str.substring(0, 2), 10);
      day = parseInt(str.substring(3, 5), 10);
      year = parseInt(str.substring(6, 10), 10);
      break;
    default:
      return { valid: false, error: `Unsupported date format: ${format}` };
  }

  // Validate date components
  if (month < 1 || month > 12) {
    return { valid: false, error: 'Invalid month' };
  }

  // Check days in month
  const daysInMonth = new Date(year, month, 0).getDate();
  if (day < 1 || day > daysInMonth) {
    return { valid: false, error: `Invalid day for month ${month}` };
  }

  // Create date object for min/max comparison
  const date = new Date(year, month - 1, day);

  // Validate min
  if (min && date < min) {
    return { valid: false, error: `Date must be on or after ${min.toISOString().split('T')[0]}` };
  }

  // Validate max
  if (max && date > max) {
    return { valid: false, error: `Date must be on or before ${max.toISOString().split('T')[0]}` };
  }

  return {
    valid: true,
    data: {
      year,
      month,
      day,
      date: date.toISOString().split('T')[0],
      dayOfWeek: date.toLocaleDateString('en-US', { weekday: 'long' })
    }
  };
}

/**
 * Validate a time string
 * 
 * @param timeStr - The time string to validate
 * @param format - Time format ('HH:mm:ss', 'HH:mm', '12h')
 * @returns ValidationResult with validation status
 */
export function validateTime(timeStr: string, format: 'HH:mm:ss' | 'HH:mm' | '12h' = 'HH:mm:ss'): ValidationResult {
  if (timeStr == null || typeof timeStr !== 'string') {
    return { valid: false, error: 'Time is required' };
  }

  const str = timeStr.trim();
  let pattern: RegExp;
  let is12Hour = false;

  switch (format) {
    case 'HH:mm:ss':
      pattern = /^([01]?\d|2[0-3]):([0-5]\d):([0-5]\d)$/;
      break;
    case 'HH:mm':
      pattern = /^([01]?\d|2[0-3]):([0-5]\d)$/;
      break;
    case '12h':
      pattern = /^(0?[1-9]|1[0-2]):([0-5]\d)(?::([0-5]\d))?\s*(AM|PM|am|pm)$/;
      is12Hour = true;
      break;
    default:
      return { valid: false, error: `Unsupported time format: ${format}` };
  }

  if (!pattern.test(str)) {
    return { valid: false, error: `Time does not match format ${format}` };
  }

  const match = str.match(pattern);
  if (!match) {
    return { valid: false, error: 'Invalid time format' };
  }

  let hour = parseInt(match[1], 10);
  const minute = parseInt(match[2], 10);
  const second = match[3] ? parseInt(match[3], 10) : 0;
  let ampm = match[4]?.toUpperCase();

  // Convert 12-hour to 24-hour
  if (is12Hour) {
    if (ampm === 'PM' && hour !== 12) {
      hour += 12;
    } else if (ampm === 'AM' && hour === 12) {
      hour = 0;
    }
  }

  return {
    valid: true,
    data: {
      hour,
      minute,
      second,
      hour12: is12Hour ? hour : (hour > 12 ? hour - 12 : (hour === 0 ? 12 : hour)),
      ampm: is12Hour ? ampm : (hour >= 12 ? 'PM' : 'AM'),
      seconds: hour * 3600 + minute * 60 + second
    }
  };
}

// =============================================================================
// String Validation
// =============================================================================

/**
 * Validate string length and content
 * 
 * @param str - The string to validate
 * @param options - Validation options
 * @returns ValidationResult with validation status
 * 
 * @example
 * ```typescript
 * validateString('hello', { minLength: 3, maxLength: 10 })
 * // { valid: true }
 * ```
 */
export function validateString(str: string, options: StringOptions = {}): ValidationResult {
  const {
    minLength,
    maxLength,
    exactLength,
    allowEmpty = false,
    trim = true
  } = options;

  if (str == null) {
    return { valid: false, error: 'String is required' };
  }

  let value = String(str);

  // Trim if requested
  if (trim) {
    value = value.trim();
  }

  // Check empty
  if (value.length === 0) {
    if (allowEmpty) {
      return { valid: true, data: { length: 0, trimmed: trim } };
    }
    return { valid: false, error: 'String cannot be empty' };
  }

  // Check exact length
  if (exactLength !== undefined && value.length !== exactLength) {
    return { valid: false, error: `String must be exactly ${exactLength} characters` };
  }

  // Check minimum length
  if (minLength !== undefined && value.length < minLength) {
    return { valid: false, error: `String must be at least ${minLength} characters` };
  }

  // Check maximum length
  if (maxLength !== undefined && value.length > maxLength) {
    return { valid: false, error: `String must be at most ${maxLength} characters` };
  }

  return {
    valid: true,
    data: {
      length: value.length,
      trimmed: trim,
      isEmpty: value.length === 0
    }
  };
}

/**
 * Validate string matches a pattern
 * 
 * @param str - The string to validate
 * @param pattern - RegExp pattern or string pattern
 * @param flags - Optional regex flags
 * @returns ValidationResult with validation status
 */
export function validatePattern(str: string, pattern: string | RegExp, flags?: string): ValidationResult {
  if (str == null) {
    return { valid: false, error: 'String is required' };
  }

  const value = String(str);
  let regex: RegExp;

  if (pattern instanceof RegExp) {
    regex = pattern;
  } else {
    regex = new RegExp(pattern, flags);
  }

  if (!regex.test(value)) {
    return { valid: false, error: `String does not match pattern: ${pattern}` };
  }

  const match = value.match(regex);

  return {
    valid: true,
    data: {
      pattern: pattern.toString(),
      match: match ? match[0] : null,
      groups: match?.groups
    }
  };
}

// =============================================================================
// Utility Functions
// =============================================================================

/**
 * Validate multiple fields at once
 * 
 * @param fields - Object with field names and their validation functions
 * @returns Object with validation results for each field
 * 
 * @example
 * ```typescript
 * validateFields({
 *   email: () => validateEmail('user@example.com'),
 *   phone: () => validatePhone('13800138000', { countryCode: 'CN' })
 * })
 * // { email: { valid: true }, phone: { valid: true } }
 * ```
 */
export function validateFields<T extends Record<string, () => ValidationResult>>(
  fields: T
): { [K in keyof T]: ReturnType<T[K]> } {
  const results = {} as { [K in keyof T]: ReturnType<T[K]> };

  for (const [key, validator] of Object.entries(fields)) {
    results[key as keyof T] = validator() as ReturnType<T[typeof key]>;
  }

  return results;
}

/**
 * Check if all validations passed
 * 
 * @param results - Array of validation results
 * @returns true if all passed, false otherwise
 */
export function allValid(results: ValidationResult[]): boolean {
  return results.every(r => r.valid);
}

/**
 * Get first error message from validation results
 * 
 * @param results - Array of validation results
 * @returns First error message or null if all passed
 */
export function getFirstError(results: ValidationResult[]): string | null {
  for (const result of results) {
    if (!result.valid && result.error) {
      return result.error;
    }
  }
  return null;
}

// =============================================================================
// Exports
// =============================================================================

export default {
  // Email
  validateEmail,
  
  // Phone
  validatePhone,
  
  // URL
  validateUrl,
  
  // IP
  validateIP,
  validateIPv4,
  validateIPv6,
  
  // ID Cards
  validateChineseIdCard,
  validateUSSSN,
  
  // Credit Cards
  validateCreditCard,
  
  // Date/Time
  validateDate,
  validateTime,
  
  // String
  validateString,
  validatePattern,
  
  // Utilities
  validateFields,
  allValid,
  getFirstError,
};

// Re-export types for convenience
export type {
  ValidationResult,
  EmailOptions,
  PhoneOptions,
  UrlOptions,
  DateOptions,
  StringOptions,
};
