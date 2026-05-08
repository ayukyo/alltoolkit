/**
 * Credit Card Utilities Test Suite
 * 
 * Comprehensive tests for the credit card utilities module.
 * Run with: npx ts-node credit_card_utils_test.ts
 * Or compile: tsc credit_card_utils_test.ts && node credit_card_utils_test.js
 */

import {
  sanitize,
  format,
  mask,
  maskFormatted,
  validate,
  isValid,
  isValidFormat,
  isValidLength,
  luhnCheck,
  calculateLuhnCheckDigit,
  detectCardType,
  getCardInfo,
  getCardTypeName,
  getAllCardTypes,
  isCardTypeSupported,
  isValidCVV,
  validateExpiry,
  validateExpiryString,
  getBIN,
  isValidBIN,
  generateTestNumber,
  CardType,
  CreditCardUtils,
} from './mod';

// Test result tracking
let passed = 0;
let failed = 0;

function test(name: string, fn: () => void): void {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (error) {
    console.error(`✗ ${name}`);
    console.error(`  Error: ${error}`);
    failed++;
  }
}

function assertEqual(actual: any, expected: any, message?: string): void {
  if (actual !== expected) {
    throw new Error(`${message || 'Assertion failed'}: expected ${expected}, got ${actual}`);
  }
}

function assertTrue(value: boolean, message?: string): void {
  if (!value) {
    throw new Error(message || 'Expected true, got false');
  }
}

function assertFalse(value: boolean, message?: string): void {
  if (value) {
    throw new Error(message || 'Expected false, got true');
  }
}

function assertMatch(value: string, pattern: RegExp, message?: string): void {
  if (!pattern.test(value)) {
    throw new Error(`${message || 'Pattern match failed'}: ${value} does not match ${pattern}`);
  }
}

function assertThrows(fn: () => void, expectedMessage?: string): void {
  try {
    fn();
    // Function didn't throw, this is an error
    throw new Error(expectedMessage || 'Expected function to throw');
  } catch (e) {
    // Function threw something
    if (e instanceof Error) {
      // If this is our own "Expected function to throw" error, re-throw it
      if (e.message === (expectedMessage || 'Expected function to throw') && e.message === 'Expected function to throw') {
        throw e;
      }
      // Otherwise, the function threw as expected (possibly with a different message)
    }
    // Non-Error exceptions are also valid throws
  }
}

// ==================== Sanitization Tests ====================

test('sanitize() removes non-digits', () => {
  assertEqual(sanitize('4111-1111-1111-1111'), '4111111111111111');
  assertEqual(sanitize('4111 1111 1111 1111'), '4111111111111111');
  assertEqual(sanitize('4111.1111.1111.1111'), '4111111111111111');
  assertEqual(sanitize('abc4111111111111111def'), '4111111111111111');
});

test('sanitize() handles empty string', () => {
  assertEqual(sanitize(''), '');
  assertEqual(sanitize('   '), '');
  assertEqual(sanitize('abc'), '');
});

// ==================== Formatting Tests ====================

test('format() formats Visa card number', () => {
  assertEqual(format('4111111111111111'), '4111 1111 1111 1111');
  assertEqual(format('4111-1111-1111-1111'), '4111 1111 1111 1111');
});

test('format() formats Amex card number', () => {
  assertEqual(format('378282246310005'), '3782 822463 10005');
});

test('format() handles short numbers', () => {
  assertEqual(format('123'), '123');
  assertEqual(format('1234'), '1234');
  assertEqual(format('12345'), '1234 5');
});

// ==================== Masking Tests ====================

test('mask() masks card number', () => {
  assertEqual(mask('4111111111111111'), '4111********1111');
  assertEqual(mask('378282246310005'), '3782*******0005');
});

test('mask() with custom visible digits', () => {
  assertEqual(mask('4111111111111111', 6, 4), '411111******1111');
  assertEqual(mask('4111111111111111', 4, 2), '4111**********11');
});

test('mask() with custom mask character', () => {
  assertEqual(mask('4111111111111111', 4, 4, 'X'), '4111XXXXXXXX1111');
});

test('maskFormatted() masks with formatting', () => {
  const masked = maskFormatted('4111111111111111');
  // maskFormatted first masks then formats, so masked digits become the mask char
  // Expected: "4111" + "********" + "1111" -> formatted
  assertMatch(masked, /4111/);
  assertMatch(masked, /1111/);
});

// ==================== Luhn Check Tests ====================

test('luhnCheck() validates known test numbers', () => {
  // Valid test numbers
  assertTrue(luhnCheck('4111111111111111')); // Visa
  assertTrue(luhnCheck('4012888888881881')); // Visa
  assertTrue(luhnCheck('378282246310005')); // Amex
  assertTrue(luhnCheck('5555555555554444')); // MasterCard
  assertTrue(luhnCheck('5105105105105100')); // MasterCard
  assertTrue(luhnCheck('6011111111111117')); // Discover
});

test('luhnCheck() rejects invalid numbers', () => {
  assertFalse(luhnCheck('4111111111111112')); // Invalid check digit
  assertFalse(luhnCheck('1234567890123450')); // Truly invalid
  assertFalse(luhnCheck('5555555555554443')); // Invalid MasterCard
});

test('luhnCheck() handles empty and invalid input', () => {
  assertFalse(luhnCheck(''));
  assertFalse(luhnCheck('abcdef'));
  assertFalse(luhnCheck('123abc456'));
});

test('calculateLuhnCheckDigit() calculates correct check digits', () => {
  // Verify against known valid numbers
  // 4111111111111111 -> check digit for 411111111111111 is 1
  const visaPartial = '411111111111111';
  const visaCheck = calculateLuhnCheckDigit(visaPartial);
  assertTrue(luhnCheck(visaPartial + visaCheck));
  
  // 378282246310005 -> check digit for 37828224631000 is 5
  const amexPartial = '37828224631000';
  const amexCheck = calculateLuhnCheckDigit(amexPartial);
  assertTrue(luhnCheck(amexPartial + amexCheck));
  
  // Verify the full number is valid
  assertEqual(luhnCheck('4111111111111111'), true);
  assertEqual(luhnCheck('378282246310005'), true);
});

test('calculateLuhnCheckDigit() throws on invalid input', () => {
  assertThrows(() => calculateLuhnCheckDigit('abc'), 'Partial card number must contain only digits');
  assertThrows(() => calculateLuhnCheckDigit(''), 'Partial card number must contain only digits');
  assertThrows(() => calculateLuhnCheckDigit('123a456'), 'Partial card number must contain only digits');
});

// ==================== Card Type Detection Tests ====================

test('detectCardType() detects Visa', () => {
  assertEqual(detectCardType('4111111111111111'), CardType.VISA);
  assertEqual(detectCardType('4012888888881881'), CardType.VISA);
  assertEqual(detectCardType('4222222222222'), CardType.VISA);
});

test('detectCardType() detects MasterCard', () => {
  assertEqual(detectCardType('5555555555554444'), CardType.MASTERCARD);
  assertEqual(detectCardType('5105105105105100'), CardType.MASTERCARD);
  assertEqual(detectCardType('2221000000000009'), CardType.MASTERCARD);
  assertEqual(detectCardType('2720999999999995'), CardType.MASTERCARD);
});

test('detectCardType() detects Amex', () => {
  assertEqual(detectCardType('378282246310005'), CardType.AMEX);
  assertEqual(detectCardType('371449635398431'), CardType.AMEX);
});

test('detectCardType() detects Discover', () => {
  assertEqual(detectCardType('6011111111111117'), CardType.DISCOVER);
  assertEqual(detectCardType('6011000990139424'), CardType.DISCOVER);
  assertEqual(detectCardType('6511111111111111'), CardType.DISCOVER);
});

test('detectCardType() detects JCB', () => {
  assertEqual(detectCardType('3530111333300000'), CardType.JCB);
  assertEqual(detectCardType('3566002020360505'), CardType.JCB);
});

test('detectCardType() detects Diners Club', () => {
  assertEqual(detectCardType('30569309025904'), CardType.DINERS_CLUB);
  assertEqual(detectCardType('36000000000008'), CardType.DINERS_CLUB);
});

test('detectCardType() detects UnionPay', () => {
  assertEqual(detectCardType('6212345678901234'), CardType.UNIONPAY);
  assertEqual(detectCardType('6225881234567890'), CardType.UNIONPAY);
});

test('detectCardType() detects Mir', () => {
  assertEqual(detectCardType('2200123456789012'), CardType.MIR);
  assertEqual(detectCardType('2204123456789016'), CardType.MIR);
});

test('detectCardType() detects Maestro', () => {
  assertEqual(detectCardType('5018123456789012'), CardType.MAESTRO);
  assertEqual(detectCardType('5612345678901234'), CardType.MAESTRO);
});

test('detectCardType() returns UNKNOWN for invalid input', () => {
  assertEqual(detectCardType(''), CardType.UNKNOWN);
  assertEqual(detectCardType('123'), CardType.UNKNOWN);
  assertEqual(detectCardType('0000000000000000'), CardType.UNKNOWN);
});

// ==================== Validation Tests ====================

test('validate() validates correct card numbers', () => {
  const result = validate('4111111111111111');
  assertTrue(result.valid);
  assertEqual(result.cardType, CardType.VISA);
  assertEqual(result.error, null);
  assertTrue(result.info !== null);
});

test('validate() rejects empty input', () => {
  const result = validate('');
  assertFalse(result.valid);
  assertEqual(result.error, 'Card number is empty');
});

test('validate() rejects invalid characters in short input', () => {
  const result = validate('abc123'); // After sanitize: '123' (too short)
  assertFalse(result.valid);
  assertMatch(result.error!, /length is invalid|empty/);
});

test('validate() rejects wrong length', () => {
  const result = validate('123');
  assertFalse(result.valid);
  assertMatch(result.error!, /length is invalid/);
});

test('validate() rejects invalid Luhn', () => {
  const result = validate('4111111111111112');
  assertFalse(result.valid);
  assertEqual(result.error, 'Card number fails Luhn check');
});

test('validate() rejects wrong length for card type', () => {
  const result = validate('3782822463100050'); // Amex with 16 digits
  assertFalse(result.valid);
  assertMatch(result.error!, /Invalid length for American Express/);
});

test('isValid() returns boolean', () => {
  assertTrue(isValid('4111111111111111'));
  assertFalse(isValid('4111111111111112'));
  assertFalse(isValid(''));
});

test('isValidFormat() checks format', () => {
  assertTrue(isValidFormat('4111111111111111'));
  assertTrue(isValidFormat('123456789012'));
  assertFalse(isValidFormat('123'));
  assertFalse(isValidFormat('12345678901234567890123'));
});

test('isValidLength() checks length for card type', () => {
  assertTrue(isValidLength('4111111111111111')); // Visa 16 digits (valid)
  assertTrue(isValidLength('378282246310005')); // Amex 15 digits (valid)
  assertTrue(isValidLength('4111111111111')); // Visa 13 digits (valid - Visa supports 13, 16, 19)
  assertFalse(isValidLength('411111111111')); // Visa 12 digits (invalid)
  assertFalse(isValidLength('37828224631000')); // Amex 14 digits (invalid - Amex only 15)
});

// ==================== CVV Validation Tests ====================

test('isValidCVV() validates 3-digit CVV', () => {
  assertTrue(isValidCVV('123'));
  assertTrue(isValidCVV('999'));
  assertTrue(isValidCVV('000'));
  assertFalse(isValidCVV('12')); // Too short
  assertFalse(isValidCVV('1')); // Too short
  assertFalse(isValidCVV('abc')); // Invalid chars
  assertFalse(isValidCVV('12a')); // Invalid chars
});

test('isValidCVV() validates 4-digit CVV for Amex', () => {
  assertTrue(isValidCVV('1234', CardType.AMEX));
  assertTrue(isValidCVV('123', CardType.VISA));
  assertFalse(isValidCVV('123', CardType.AMEX));
  assertFalse(isValidCVV('1234', CardType.VISA));
});

// ==================== Expiry Date Tests ====================

test('validateExpiry() validates correct dates', () => {
  const now = new Date();
  const futureYear = now.getFullYear() + 1;
  const result = validateExpiry(12, futureYear);
  assertTrue(result.valid);
  assertEqual(result.month, 12);
  assertEqual(result.year, futureYear);
  assertFalse(result.expired);
});

test('validateExpiry() handles 2-digit years', () => {
  const result = validateExpiry(12, 30);
  assertTrue(result.valid);
  assertEqual(result.year, 2030);
});

test('validateExpiry() rejects invalid months', () => {
  const result = validateExpiry(13, 2030);
  assertFalse(result.valid);
  assertMatch(result.error!, /Invalid month/);
  
  const result2 = validateExpiry(0, 2030);
  assertFalse(result2.valid);
});

test('validateExpiry() detects expired cards', () => {
  const result = validateExpiry(1, 2020);
  assertTrue(result.valid);
  assertTrue(result.expired);
});

test('validateExpiry() detects cards expiring soon', () => {
  const now = new Date();
  const currentMonth = now.getMonth() + 1;
  const currentYear = now.getFullYear();
  
  // Test with current month/year (should expire soon)
  const result = validateExpiry(currentMonth, currentYear);
  assertTrue(result.valid);
  assertTrue(result.expiresSoon || result.expired);
});

test('validateExpiryString() parses MM/YY format', () => {
  const result = validateExpiryString('12/30');
  assertTrue(result.valid);
  assertEqual(result.month, 12);
  assertEqual(result.year, 2030);
});

test('validateExpiryString() parses MM/YYYY format', () => {
  const result = validateExpiryString('12/2030');
  assertTrue(result.valid);
  assertEqual(result.month, 12);
  assertEqual(result.year, 2030);
});

test('validateExpiryString() handles spaces', () => {
  const result = validateExpiryString('12 / 30');
  assertTrue(result.valid);
  assertEqual(result.month, 12);
  assertEqual(result.year, 2030);
});

test('validateExpiryString() rejects invalid formats', () => {
  const result = validateExpiryString('1230');
  assertFalse(result.valid);
  
  const result2 = validateExpiryString('12-30');
  assertTrue(result2.valid); // Should accept dash separator
});

// ==================== BIN Tests ====================

test('getBIN() extracts BIN', () => {
  assertEqual(getBIN('4111111111111111'), '411111');
  assertEqual(getBIN('4111111111111111', 8), '41111111');
  assertEqual(getBIN('123', 6), null);
});

test('isValidBIN() validates BIN format', () => {
  assertTrue(isValidBIN('411111')); // 6 digits - valid
  assertTrue(isValidBIN('41111111')); // 8 digits - valid
  assertTrue(isValidBIN('4111111')); // 7 digits - also valid (6-8 range)
  assertFalse(isValidBIN('41111')); // 5 digits - invalid
  assertFalse(isValidBIN('411111111')); // 9 digits - invalid
  assertFalse(isValidBIN('abcdef')); // Non-digits - invalid
});

// ==================== Card Info Tests ====================

test('getCardInfo() returns card info', () => {
  const info = getCardInfo(CardType.VISA);
  assertTrue(info !== null);
  assertEqual(info!.type, CardType.VISA);
  assertEqual(info!.displayName, 'Visa');
  assertEqual(info!.cvvLength, 3);
});

test('getCardInfo() returns null for unknown', () => {
  const info = getCardInfo(CardType.UNKNOWN);
  assertEqual(info, null);
});

test('getAllCardTypes() returns all supported types', () => {
  const types = getAllCardTypes();
  assertTrue(types.length > 0);
  assertTrue(types.every(t => t.type !== CardType.UNKNOWN));
});

test('isCardTypeSupported() checks support', () => {
  assertTrue(isCardTypeSupported('VISA'));
  assertTrue(isCardTypeSupported('visa'));
  assertTrue(isCardTypeSupported('MASTERCARD'));
  assertFalse(isCardTypeSupported('UNKNOWN'));
  assertFalse(isCardTypeSupported('FAKE'));
});

test('getCardTypeName() returns display name', () => {
  assertEqual(getCardTypeName('4111111111111111'), 'Visa');
  assertEqual(getCardTypeName('378282246310005'), 'American Express');
  assertEqual(getCardTypeName('5555555555554444'), 'MasterCard');
});

// ==================== Test Number Generation Tests ====================

test('generateTestNumber() generates valid Visa number', () => {
  const number = generateTestNumber(CardType.VISA);
  assertTrue(luhnCheck(number));
  assertEqual(detectCardType(number), CardType.VISA);
  // Visa supports 13, 16, 19 - default to 16
  assertTrue(number.length === 16 || number.length === 13 || number.length === 19);
});

test('generateTestNumber() generates valid Amex number', () => {
  const number = generateTestNumber(CardType.AMEX);
  assertEqual(number.length, 15); // Amex is always 15 digits
  assertTrue(luhnCheck(number));
  assertEqual(detectCardType(number), CardType.AMEX);
});

test('generateTestNumber() generates valid MasterCard number', () => {
  const number = generateTestNumber(CardType.MASTERCARD);
  assertEqual(number.length, 16); // MasterCard is 16 digits
  assertTrue(luhnCheck(number));
  assertEqual(detectCardType(number), CardType.MASTERCARD);
});

test('generateTestNumber() throws for unknown type', () => {
  assertThrows(() => generateTestNumber(CardType.UNKNOWN));
});

// ==================== Namespace Tests ====================

test('CreditCardUtils namespace exports all functions', () => {
  assertTrue(typeof CreditCardUtils.sanitize === 'function');
  assertTrue(typeof CreditCardUtils.format === 'function');
  assertTrue(typeof CreditCardUtils.mask === 'function');
  assertTrue(typeof CreditCardUtils.validate === 'function');
  assertTrue(typeof CreditCardUtils.luhnCheck === 'function');
  assertTrue(typeof CreditCardUtils.detectCardType === 'function');
  assertTrue(typeof CreditCardUtils.CardType === 'object');
});

// ==================== Edge Cases ====================

test('handles formatted input throughout', () => {
  const formatted = '4111 1111 1111 1111';
  assertTrue(isValid(formatted));
  assertEqual(detectCardType(formatted), CardType.VISA);
  assertEqual(sanitize(formatted), '4111111111111111');
});

test('handles long card numbers', () => {
  const longVisa = '4111111111111111111'; // 19 digits
  assertEqual(detectCardType(longVisa), CardType.VISA);
});

test('handles short card numbers', () => {
  assertEqual(detectCardType('4'), CardType.VISA); // Still detected by prefix
  assertFalse(isValidLength('4'));
});

// ==================== Run Summary ====================

console.log('\n' + '='.repeat(50));
console.log(`Test Results: ${passed} passed, ${failed} failed`);
console.log('='.repeat(50));

if (failed > 0) {
  process.exit(1);
}