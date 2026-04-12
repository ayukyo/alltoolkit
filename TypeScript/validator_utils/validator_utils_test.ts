/**
 * Validator Utilities Test Suite
 * 
 * Comprehensive tests for all validation functions.
 * Run with: deno test validator_utils_test.ts
 * Or: bun test validator_utils_test.ts
 * Or: node --test validator_utils_test.ts (Node 20+)
 */

import {
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
  
  type ValidationResult,
} from './validator_utils.ts';

// =============================================================================
// Test Helper
// =============================================================================

let passed = 0;
let failed = 0;

function assert(condition: boolean, message: string): void {
  if (condition) {
    passed++;
    console.log(`  ✓ ${message}`);
  } else {
    failed++;
    console.log(`  ✗ ${message}`);
  }
}

function assertEquals<T>(actual: T, expected: T, message: string): void {
  if (actual === expected) {
    passed++;
    console.log(`  ✓ ${message}`);
  } else {
    failed++;
    console.log(`  ✗ ${message} (expected: ${expected}, got: ${actual})`);
  }
}

function assertValid(result: ValidationResult, message: string): void {
  if (result.valid) {
    passed++;
    console.log(`  ✓ ${message}`);
  } else {
    failed++;
    console.log(`  ✗ ${message} (error: ${result.error})`);
  }
}

function assertInvalid(result: ValidationResult, message: string): void {
  if (!result.valid) {
    passed++;
    console.log(`  ✓ ${message}`);
  } else {
    failed++;
    console.log(`  ✗ ${message} (expected invalid, got valid)`);
  }
}

// =============================================================================
// Email Validation Tests
// =============================================================================

console.log('\n=== Email Validation Tests ===\n');

// Valid emails
assertValid(validateEmail('user@example.com'), 'Valid standard email');
assertValid(validateEmail('test.user@domain.co.uk'), 'Valid email with subdomain');
assertValid(validateEmail('user+tag@example.com'), 'Valid email with plus sign');
assertValid(validateEmail('user_name@example.com'), 'Valid email with underscore');
assertValid(validateEmail('user123@example.com'), 'Valid email with numbers');
assertValid(validateEmail('a@b.co'), 'Valid minimal email');

// Invalid emails
assertInvalid(validateEmail(''), 'Empty email');
assertInvalid(validateEmail('invalid'), 'No @ symbol');
assertInvalid(validateEmail('user@'), 'No domain');
assertInvalid(validateEmail('@example.com'), 'No local part');
assertInvalid(validateEmail('user..name@example.com'), 'Consecutive dots');
assertInvalid(validateEmail('user@example'), 'No TLD (default requireTld)');
assertInvalid(validateEmail('user@example.c'), 'Single char TLD');

// Email with IP domain
assertInvalid(validateEmail('user@[192.168.1.1]'), 'IP domain not allowed by default');
assertValid(validateEmail('user@[192.168.1.1]', { allowIpDomain: true }), 'IP domain allowed when enabled');
assertInvalid(validateEmail('user@[256.1.1.1]', { allowIpDomain: true }), 'Invalid IP in domain');

// Email options
assertInvalid(validateEmail('user@example.com', { maxLength: 10 }), 'Email exceeds maxLength');

// Email data extraction
const emailResult = validateEmail('test.user@example.com');
assert(emailResult.valid && emailResult.data?.local === 'test.user', 'Extract local part');
assert(emailResult.valid && emailResult.data?.domain === 'example.com', 'Extract domain');

// =============================================================================
// Phone Validation Tests
// =============================================================================

console.log('\n=== Phone Validation Tests ===\n');

// Valid Chinese phones
assertValid(validatePhone('13800138000', { countryCode: 'CN' }), 'Valid CN phone');
assertValid(validatePhone('+8613800138000', { countryCode: 'CN' }), 'Valid CN phone with country code');
assertValid(validatePhone('19812345678', { countryCode: 'CN' }), 'Valid CN phone (198 prefix)');

// Invalid Chinese phones
assertInvalid(validatePhone('12345678901', { countryCode: 'CN' }), 'Invalid CN phone (wrong prefix)');
assertInvalid(validatePhone('1380013800', { countryCode: 'CN' }), 'Invalid CN phone (too short)');

// Valid US phones
assertValid(validatePhone('2125551234', { countryCode: 'US' }), 'Valid US phone');
assertValid(validatePhone('+12125551234', { countryCode: 'US' }), 'Valid US phone with country code');

// International format
assertValid(validatePhone('+12125551234', { allowInternational: true }), 'Valid international phone');
assertValid(validatePhone('+447911123456', { allowInternational: true }), 'Valid UK international phone');
assertValid(validatePhone('+8613800138000', { allowInternational: true }), 'Valid CN international phone');

// Invalid international
assertInvalid(validatePhone('12345', { allowInternational: true }), 'Phone too short');
assertInvalid(validatePhone('+12345678901234567', { allowInternational: true }), 'Phone too long (>15 digits)');
assertInvalid(validatePhone('abc123', { allowInternational: true }), 'Non-numeric phone');

// Phone with separators
assertValid(validatePhone('138-0013-8000', { countryCode: 'CN' }), 'CN phone with dashes');
assertValid(validatePhone('138 0013 8000', { countryCode: 'CN' }), 'CN phone with spaces');
assertValid(validatePhone('(138)0013-8000', { countryCode: 'CN' }), 'CN phone with parentheses');

// =============================================================================
// URL Validation Tests
// =============================================================================

console.log('\n=== URL Validation Tests ===\n');

// Valid URLs
assertValid(validateUrl('https://example.com'), 'Valid HTTPS URL');
assertValid(validateUrl('http://example.com'), 'Valid HTTP URL');
assertValid(validateUrl('https://www.example.com'), 'Valid URL with www');
assertValid(validateUrl('https://example.com/path/to/page'), 'Valid URL with path');
assertValid(validateUrl('https://example.com?query=value'), 'Valid URL with query');
assertValid(validateUrl('https://example.com#anchor'), 'Valid URL with hash');
assertValid(validateUrl('example.com'), 'Valid URL without protocol (requireProtocol=false)');

// Invalid URLs
assertInvalid(validateUrl(''), 'Empty URL');
assertInvalid(validateUrl('not-a-url'), 'Invalid URL format');
assertInvalid(validateUrl('ftp://files.example.com', { protocols: ['http', 'https'] }), 'Disallowed protocol');

// URL with IP
assertValid(validateUrl('http://192.168.1.1'), 'Valid URL with IP');
assertInvalid(validateUrl('http://192.168.1.1', { allowIp: false }), 'IP not allowed when disabled');

// URL data extraction
const urlResult = validateUrl('https://example.com/path?query=1#anchor');
assert(urlResult.valid && urlResult.data?.protocol === 'https', 'Extract protocol');
assert(urlResult.valid && urlResult.data?.host === 'example.com', 'Extract host');
assert(urlResult.valid && urlResult.data?.pathname === '/path', 'Extract pathname');

// =============================================================================
// IP Address Validation Tests
// =============================================================================

console.log('\n=== IP Address Validation Tests ===\n');

// Valid IPv4
assertValid(validateIPv4('192.168.1.1'), 'Valid IPv4');
assertValid(validateIPv4('0.0.0.0'), 'Valid IPv4 (all zeros)');
assertValid(validateIPv4('255.255.255.255'), 'Valid IPv4 (all 255s)');
assertValid(validateIPv4('127.0.0.1'), 'Valid IPv4 (localhost)');

// Invalid IPv4
assertInvalid(validateIPv4('256.1.1.1'), 'Invalid IPv4 (octet > 255)');
assertInvalid(validateIPv4('1.1.1'), 'Invalid IPv4 (too few octets)');
assertInvalid(validateIPv4('1.1.1.1.1'), 'Invalid IPv4 (too many octets)');
assertInvalid(validateIPv4('01.01.01.01'), 'Invalid IPv4 (leading zeros)');
assertInvalid(validateIPv4('abc.def.ghi.jkl'), 'Invalid IPv4 (non-numeric)');

// Private IP detection
const privateIp = validateIPv4('192.168.1.1');
assert(privateIp.valid && privateIp.data?.isPrivate === true, 'Detect private IP (192.168.x.x)');

const publicIp = validateIPv4('8.8.8.8');
assert(publicIp.valid && publicIp.data?.isPrivate === false, 'Detect public IP');

const loopback = validateIPv4('127.0.0.1');
assert(loopback.valid && loopback.data?.isPrivate === true, 'Detect loopback IP');

// Valid IPv6
assertValid(validateIPv6('2001:0db8:85a3:0000:0000:8a2e:0370:7334'), 'Valid IPv6 full');
assertValid(validateIPv6('2001:db8:85a3::8a2e:370:7334'), 'Valid IPv6 compressed');
assertValid(validateIPv6('::1'), 'Valid IPv6 loopback');
assertValid(validateIPv6('::'), 'Valid IPv6 all zeros');

// Invalid IPv6
assertInvalid(validateIPv6('2001:db8:::85a3'), 'Invalid IPv6 (triple colon)');
assertInvalid(validateIPv6('gggg::1'), 'Invalid IPv6 (invalid hex)');

// Generic IP validation
assertValid(validateIP('192.168.1.1'), 'Valid IP (auto-detect IPv4)');
assertValid(validateIP('::1', 6), 'Valid IPv6 (explicit version)');
assertInvalid(validateIP('192.168.1.1', 6), 'IPv4 rejected when IPv6 required');

// =============================================================================
// Chinese ID Card Validation Tests
// =============================================================================

console.log('\n=== Chinese ID Card Validation Tests ===\n');

// Valid ID cards (test data with correct check digit)
// For 11010119900101123: check digit calculation gives 7
assertValid(validateChineseIdCard('110101199001011237'), 'Valid ID card format');

// Invalid ID cards
assertInvalid(validateChineseIdCard(''), 'Empty ID card');
assertInvalid(validateChineseIdCard('123456789012345678'), 'Invalid ID card (wrong region)');
assertInvalid(validateChineseIdCard('110101199001011234'), 'Invalid ID card (wrong check digit)');
assertInvalid(validateChineseIdCard('110101199002301234'), 'Invalid ID card (invalid date)');
assertInvalid(validateChineseIdCard('11010119900101123'), 'Invalid ID card (too short)');
assertInvalid(validateChineseIdCard('1101011990010112345'), 'Invalid ID card (too long)');

// ID card data extraction
const idResult = validateChineseIdCard('110101199001011237');
if (idResult.valid && idResult.data) {
  assert(idResult.data.birthdate === '1990-01-01', 'Extract birthdate');
  assert(idResult.data.regionCode === '110101', 'Extract region code');
}

// =============================================================================
// US SSN Validation Tests
// =============================================================================

console.log('\n=== US SSN Validation Tests ===\n');

// Valid SSNs (test data)
assertValid(validateUSSSN('123-45-6789'), 'Valid SSN with dashes');
assertValid(validateUSSSN('123456789'), 'Valid SSN without dashes');

// Invalid SSNs
assertInvalid(validateUSSSN(''), 'Empty SSN');
assertInvalid(validateUSSSN('000-45-6789'), 'Invalid SSN (area 000)');
assertInvalid(validateUSSSN('666-45-6789'), 'Invalid SSN (area 666)');
assertInvalid(validateUSSSN('123-00-6789'), 'Invalid SSN (group 00)');
assertInvalid(validateUSSSN('123-45-0000'), 'Invalid SSN (serial 0000)');
assertInvalid(validateUSSSN('12345678'), 'Invalid SSN (too short)');
assertInvalid(validateUSSSN('123-45-67890'), 'Invalid SSN (too long)');

// =============================================================================
// Credit Card Validation Tests
// =============================================================================

console.log('\n=== Credit Card Validation Tests ===\n');

// Valid card numbers (test data using Luhn-valid numbers)
assertValid(validateCreditCard('4532015112830366'), 'Valid Visa card');
assertValid(validateCreditCard('5425233430109903'), 'Valid Mastercard');
assertValid(validateCreditCard('374245455400126'), 'Valid Amex card');
assertValid(validateCreditCard('6011000990139424'), 'Valid Discover card');

// Invalid card numbers
assertInvalid(validateCreditCard(''), 'Empty card number');
assertInvalid(validateCreditCard('1234567890123456'), 'Invalid card (fails Luhn)');
assertInvalid(validateCreditCard('4532015112830367'), 'Invalid Visa (wrong check digit)');
assertInvalid(validateCreditCard('abcd123456789012'), 'Invalid card (non-numeric)');

// Card with spaces
assertValid(validateCreditCard('4532 0151 1283 0366'), 'Valid card with spaces');
assertValid(validateCreditCard('4532-0151-1283-0366'), 'Valid card with dashes');

// Issuer detection
const cardResult = validateCreditCard('4532015112830366');
if (cardResult.valid && cardResult.data) {
  assert(cardResult.data.issuer === 'visa', 'Detect Visa issuer');
  assert(cardResult.data.lastFour === '0366', 'Extract last four digits');
}

// Specific issuer validation
assertValid(validateCreditCard('4532015112830366', 'visa'), 'Valid Visa (explicit)');
assertInvalid(validateCreditCard('4532015112830366', 'mastercard'), 'Visa rejected as Mastercard');

// =============================================================================
// Date Validation Tests
// =============================================================================

console.log('\n=== Date Validation Tests ===\n');

// Valid dates
assertValid(validateDate('2024-01-15', { format: 'YYYY-MM-DD' }), 'Valid date (YYYY-MM-DD)');
assertValid(validateDate('15/01/2024', { format: 'DD/MM/YYYY' }), 'Valid date (DD/MM/YYYY)');
assertValid(validateDate('01/15/2024', { format: 'MM/DD/YYYY' }), 'Valid date (MM/DD/YYYY)');
assertValid(validateDate('20240115', { format: 'YYYYMMDD' }), 'Valid date (YYYYMMDD)');

// Invalid dates
assertInvalid(validateDate('2024-13-01', { format: 'YYYY-MM-DD' }), 'Invalid date (month > 12)');
assertInvalid(validateDate('2024-02-30', { format: 'YYYY-MM-DD' }), 'Invalid date (Feb 30)');
assertInvalid(validateDate('2024-04-31', { format: 'YYYY-MM-DD' }), 'Invalid date (Apr 31)');
assertInvalid(validateDate('2023-02-29', { format: 'YYYY-MM-DD' }), 'Invalid date (Feb 29 non-leap)');
assertValid(validateDate('2024-02-29', { format: 'YYYY-MM-DD' }), 'Valid date (Feb 29 leap year)');

// Leap year validation
const leapResult = validateDate('2024-02-29', { format: 'YYYY-MM-DD' });
assert(leapResult.valid, '2024 is leap year, Feb 29 valid');

const nonLeapResult = validateDate('2023-02-29', { format: 'YYYY-MM-DD' });
assert(!nonLeapResult.valid, '2023 is not leap year, Feb 29 invalid');

// Min/Max validation
const minDate = new Date(2024, 0, 1);
const maxDate = new Date(2024, 11, 31);

assertValid(validateDate('2024-06-15', { format: 'YYYY-MM-DD', min: minDate, max: maxDate }), 'Date within range');
assertInvalid(validateDate('2023-06-15', { format: 'YYYY-MM-DD', min: minDate, max: maxDate }), 'Date before min');
assertInvalid(validateDate('2025-06-15', { format: 'YYYY-MM-DD', min: minDate, max: maxDate }), 'Date after max');

// Date data extraction
const dateResult = validateDate('2024-01-15', { format: 'YYYY-MM-DD' });
if (dateResult.valid && dateResult.data) {
  assertEquals(dateResult.data.year, 2024, 'Extract year');
  assertEquals(dateResult.data.month, 1, 'Extract month');
  assertEquals(dateResult.data.day, 15, 'Extract day');
}

// =============================================================================
// Time Validation Tests
// =============================================================================

console.log('\n=== Time Validation Tests ===\n');

// Valid times
assertValid(validateTime('14:30:45', 'HH:mm:ss'), 'Valid time (HH:mm:ss)');
assertValid(validateTime('00:00:00', 'HH:mm:ss'), 'Valid time (midnight)');
assertValid(validateTime('23:59:59', 'HH:mm:ss'), 'Valid time (end of day)');
assertValid(validateTime('14:30', 'HH:mm'), 'Valid time (HH:mm)');
assertValid(validateTime('2:30 PM', '12h'), 'Valid time (12h format)');
assertValid(validateTime('12:00 AM', '12h'), 'Valid time (midnight 12h)');
assertValid(validateTime('12:00 PM', '12h'), 'Valid time (noon 12h)');

// Invalid times
assertInvalid(validateTime('25:00:00', 'HH:mm:ss'), 'Invalid time (hour > 23)');
assertInvalid(validateTime('14:60:00', 'HH:mm:ss'), 'Invalid time (minute > 59)');
assertInvalid(validateTime('14:30:60', 'HH:mm:ss'), 'Invalid time (second > 59)');
assertInvalid(validateTime('13:00 PM', '12h'), 'Invalid time (12h format hour > 12)');
assertInvalid(validateTime('0:00 AM', '12h'), 'Invalid time (12h format hour 0)');

// Time data extraction
const timeResult = validateTime('14:30:45', 'HH:mm:ss');
if (timeResult.valid && timeResult.data) {
  assertEquals(timeResult.data.hour, 14, 'Extract hour');
  assertEquals(timeResult.data.minute, 30, 'Extract minute');
  assertEquals(timeResult.data.second, 45, 'Extract second');
}

// 12h to 24h conversion
const amResult = validateTime('02:30 AM', '12h');
if (amResult.valid && amResult.data) {
  assertEquals(amResult.data.hour, 2, '2 AM = hour 2');
}

const pmResult = validateTime('02:30 PM', '12h');
if (pmResult.valid && pmResult.data) {
  assertEquals(pmResult.data.hour, 14, '2 PM = hour 14');
}

const midnightResult = validateTime('12:00 AM', '12h');
if (midnightResult.valid && midnightResult.data) {
  assertEquals(midnightResult.data.hour, 0, '12 AM = hour 0');
}

const noonResult = validateTime('12:00 PM', '12h');
if (noonResult.valid && noonResult.data) {
  assertEquals(noonResult.data.hour, 12, '12 PM = hour 12');
}

// =============================================================================
// String Validation Tests
// =============================================================================

console.log('\n=== String Validation Tests ===\n');

// Valid strings
assertValid(validateString('hello'), 'Valid string (no options)');
assertValid(validateString('hello', { minLength: 3 }), 'Valid string (minLength)');
assertValid(validateString('hello', { maxLength: 10 }), 'Valid string (maxLength)');
assertValid(validateString('hello', { exactLength: 5 }), 'Valid string (exactLength)');
assertValid(validateString('', { allowEmpty: true }), 'Empty string allowed');

// Invalid strings
assertInvalid(validateString(''), 'Empty string not allowed');
assertInvalid(validateString('hi', { minLength: 5 }), 'String too short');
assertInvalid(validateString('hello world', { maxLength: 5 }), 'String too long');
assertInvalid(validateString('hello', { exactLength: 10 }), 'String wrong exact length');

// Trim option
const trimResult = validateString('  hello  ', { trim: true });
assert(trimResult.valid && trimResult.data?.length === 5, 'Trim removes whitespace');

const noTrimResult = validateString('  hello  ', { trim: false });
assert(noTrimResult.valid && noTrimResult.data?.length === 9, 'No trim keeps whitespace');

// =============================================================================
// Pattern Validation Tests
// =============================================================================

console.log('\n=== Pattern Validation Tests ===\n');

// Valid patterns
assertValid(validatePattern('hello123', /^[a-z]+\d+$/i), 'Valid pattern (regex)');
assertValid(validatePattern('hello123', '^[a-z]+\\d+$', 'i'), 'Valid pattern (string)');
assertValid(validatePattern('user@example.com', /^[a-z]+@[a-z]+\.[a-z]+$/i), 'Valid email pattern');

// Invalid patterns
assertInvalid(validatePattern('hello', /^[0-9]+$/), 'Invalid pattern (letters vs digits)');
assertInvalid(validatePattern('123', /^[a-z]+$/), 'Invalid pattern (digits vs letters)');

// Pattern data extraction
const patternResult = validatePattern('hello123', /^([a-z]+)(\d+)$/);
if (patternResult.valid && patternResult.data) {
  assert(patternResult.data.match === 'hello123', 'Extract full match');
}

// =============================================================================
// Utility Functions Tests
// =============================================================================

console.log('\n=== Utility Functions Tests ===\n');

// validateFields
const fieldResults = validateFields({
  email: () => validateEmail('user@example.com'),
  phone: () => validatePhone('13800138000', { countryCode: 'CN' }),
  invalid: () => validateEmail('invalid')
});

assert(fieldResults.email.valid === true, 'validateFields: valid email');
assert(fieldResults.phone.valid === true, 'validateFields: valid phone');
assert(fieldResults.invalid.valid === false, 'validateFields: invalid email');

// allValid
const allValidResult = allValid([
  { valid: true },
  { valid: true },
  { valid: true }
]);
assert(allValidResult === true, 'allValid: all true');

const notAllValidResult = allValid([
  { valid: true },
  { valid: false, error: 'test' },
  { valid: true }
]);
assert(notAllValidResult === false, 'allValid: one false');

// getFirstError
const noError = getFirstError([
  { valid: true },
  { valid: true }
]);
assert(noError === null, 'getFirstError: no errors');

const firstError = getFirstError([
  { valid: true },
  { valid: false, error: 'First error' },
  { valid: false, error: 'Second error' }
]);
assertEquals(firstError, 'First error', 'getFirstError: returns first error');

// =============================================================================
// Summary
// =============================================================================

console.log('\n=== Test Summary ===\n');
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
console.log(`Total:  ${passed + failed}`);

if (failed > 0) {
  console.log('\n⚠️  Some tests failed!');
  // Compatible with both Deno and Node.js
  if (typeof Deno !== 'undefined') {
    Deno.exit(1);
  } else if (typeof process !== 'undefined') {
    process.exit(1);
  }
} else {
  console.log('\n✅ All tests passed!');
}
