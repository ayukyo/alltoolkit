/**
 * Credit Card Utilities Examples
 * 
 * Practical examples demonstrating all features of the credit card utilities module.
 * Run with: npx ts-node credit_card_example.ts
 */

import CreditCardUtils, {
  sanitize,
  format,
  mask,
  maskFormatted,
  validate,
  isValid,
  luhnCheck,
  calculateLuhnCheckDigit,
  detectCardType,
  getCardTypeName,
  getCardInfo,
  getAllCardTypes,
  isValidCVV,
  validateExpiry,
  validateExpiryString,
  getBIN,
  generateTestNumber,
  CardType,
} from '../mod';

console.log('Credit Card Utilities Examples');
console.log('='.repeat(50));

// ==================== Example 1: Basic Validation ====================

console.log('\n1. Basic Card Validation');
console.log('-'.repeat(30));

const cardNumbers = [
  '4111111111111111', // Valid Visa
  '4111-1111-1111-1111', // Formatted Visa
  '378282246310005', // Valid Amex
  '5555555555554444', // Valid MasterCard
  '1234567890123456', // Invalid
];

for (const card of cardNumbers) {
  const result = validate(card);
  console.log(`  Card: ${card}`);
  console.log(`  Valid: ${result.valid}`);
  if (result.cardType) {
    console.log(`  Type: ${getCardTypeName(card)}`);
  }
  if (result.error) {
    console.log(`  Error: ${result.error}`);
  }
  console.log();
}

// ==================== Example 2: Card Type Detection ====================

console.log('2. Card Type Detection');
console.log('-'.repeat(30));

const testCards = {
  'Visa': '4111111111111111',
  'MasterCard': '5555555555554444',
  'Amex': '378282246310005',
  'Discover': '6011111111111117',
  'JCB': '3530111333300000',
  'Diners Club': '30569309025904',
  'UnionPay': '6212345678901234',
  'Mir': '2200123456789012',
  'Maestro': '5018123456789012',
};

for (const [name, number] of Object.entries(testCards)) {
  const type = detectCardType(number);
  const info = getCardInfo(type);
  console.log(`  ${name}: ${number}`);
  console.log(`    Detected: ${type}`);
  console.log(`    Expected lengths: ${info?.lengths.join(', ')}`);
  console.log(`    CVV length: ${info?.cvvLength}`);
  console.log();
}

// ==================== Example 3: Formatting and Masking ====================

console.log('3. Formatting and Masking');
console.log('-'.repeat(30));

const rawNumber = '4111111111111111';
console.log(`  Raw: ${rawNumber}`);
console.log(`  Formatted: ${format(rawNumber)}`);
console.log(`  Masked (default): ${mask(rawNumber)}`);
console.log(`  Masked (show 6 start): ${mask(rawNumber, 6, 4)}`);
console.log(`  Masked (show 2 end): ${mask(rawNumber, 4, 2)}`);
console.log(`  Masked (X char): ${mask(rawNumber, 4, 4, 'X')}`);
console.log(`  Masked & Formatted: ${maskFormatted(rawNumber)}`);

console.log('\n  Amex formatting:');
const amexNumber = '378282246310005';
console.log(`    Raw: ${amexNumber}`);
console.log(`    Formatted: ${format(amexNumber)}`);
console.log(`    Masked: ${mask(amexNumber)}`);

// ==================== Example 4: Luhn Algorithm ====================

console.log('\n4. Luhn Algorithm');
console.log('-'.repeat(30));

const validNumber = '4111111111111111';
const invalidNumber = '4111111111111112';

console.log(`  Valid number: ${validNumber}`);
console.log(`    Luhn check: ${luhnCheck(validNumber)}`);

console.log(`  Invalid number: ${invalidNumber}`);
console.log(`    Luhn check: ${luhnCheck(invalidNumber)}`);

// Calculate check digit
const partial = '411111111111111';
const checkDigit = calculateLuhnCheckDigit(partial);
console.log(`\n  Partial number: ${partial}`);
console.log(`  Calculated check digit: ${checkDigit}`);
console.log(`  Full valid number: ${partial}${checkDigit}`);
console.log(`  Verification: ${luhnCheck(partial + checkDigit)}`);

// ==================== Example 5: Expiry Date Validation ====================

console.log('\n5. Expiry Date Validation');
console.log('-'.repeat(30));

const expiryTests = [
  '12/25',
  '12/2025',
  '01/2020', // Expired
  '13/30', // Invalid month
];

for (const expiry of expiryTests) {
  const result = validateExpiryString(expiry);
  console.log(`  Expiry: ${expiry}`);
  console.log(`    Valid: ${result.valid}`);
  if (result.valid) {
    console.log(`    Month: ${result.month}`);
    console.log(`    Year: ${result.year}`);
    console.log(`    Expired: ${result.expired}`);
    console.log(`    Expires soon: ${result.expiresSoon}`);
  }
  if (result.error) {
    console.log(`    Error: ${result.error}`);
  }
  console.log();
}

// Numeric expiry
console.log('  Numeric expiry (month=12, year=30):');
const numericResult = validateExpiry(12, 30);
console.log(`    Valid: ${numericResult.valid}`);
console.log(`    Month: ${numericResult.month}`);
console.log(`    Year: ${numericResult.year}`);

// ==================== Example 6: CVV Validation ====================

console.log('\n6. CVV Validation');
console.log('-'.repeat(30));

const cvvTests = [
  { cvv: '123', cardType: undefined },
  { cvv: '1234', cardType: CardType.AMEX },
  { cvv: '123', cardType: CardType.VISA },
  { cvv: '1234', cardType: CardType.VISA }, // Wrong for Visa
  { cvv: '12', cardType: undefined }, // Too short
];

for (const test of cvvTests) {
  const valid = isValidCVV(test.cvv, test.cardType);
  console.log(`  CVV: ${test.cvv}, Card Type: ${test.cardType || 'any'}`);
  console.log(`    Valid: ${valid}`);
}

// ==================== Example 7: BIN/IIN Extraction ====================

console.log('\n7. BIN/IIN Extraction');
console.log('-'.repeat(30));

const binCard = '4111111111111111';
console.log(`  Card: ${binCard}`);
console.log(`  BIN (6 digits): ${getBIN(binCard, 6)}`);
console.log(`  BIN (8 digits): ${getBIN(binCard, 8)}`);

const shortCard = '123456';
console.log(`\n  Short card: ${shortCard}`);
console.log(`  BIN (6): ${getBIN(shortCard, 6)}`);

// ==================== Example 8: Test Number Generation ====================

console.log('\n8. Test Number Generation');
console.log('-'.repeat(30));

const typesToGenerate = [
  CardType.VISA,
  CardType.MASTERCARD,
  CardType.AMEX,
  CardType.DISCOVER,
  CardType.JCB,
];

for (const cardType of typesToGenerate) {
  const number = generateTestNumber(cardType);
  const result = validate(number);
  console.log(`  ${getCardInfo(cardType)?.displayName}:`);
  console.log(`    Generated: ${number}`);
  console.log(`    Valid: ${result.valid}`);
  console.log(`    Detected type: ${result.cardType}`);
}

// ==================== Example 9: All Supported Card Types ====================

console.log('\n9. All Supported Card Types');
console.log('-'.repeat(30));

const allTypes = getAllCardTypes();
for (const type of allTypes) {
  console.log(`  ${type.displayName} (${type.type}):`);
  console.log(`    Prefixes: ${type.prefixes.slice(0, 3).join(', ')}...`);
  console.log(`    Lengths: ${type.lengths.join(', ')}`);
  console.log(`    CVV: ${type.cvvLength} digits`);
}

// ==================== Example 10: Namespace Usage ====================

console.log('\n10. Namespace Usage (CreditCardUtils)');
console.log('-'.repeat(30));

const card = '4111111111111111';
console.log(`  Card: ${card}`);
console.log(`  Sanitized: ${CreditCardUtils.sanitize(card)}`);
console.log(`  Formatted: ${CreditCardUtils.format(card)}`);
console.log(`  Valid: ${CreditCardUtils.isValid(card)}`);
console.log(`  Type: ${CreditCardUtils.getCardTypeName(card)}`);
console.log(`  Masked: ${CreditCardUtils.mask(card)}`);
console.log(`  BIN: ${CreditCardUtils.getBIN(card)}`);

// ==================== Example 11: Complete Validation Workflow ====================

console.log('\n11. Complete Validation Workflow');
console.log('-'.repeat(30));

function validatePayment(cardNumber: string, cvv: string, expiry: string): void {
  console.log(`  Validating payment:`);
  console.log(`    Card: ${maskFormatted(cardNumber)}`);
  console.log(`    CVV: ${cvv}`);
  console.log(`    Expiry: ${expiry}`);
  console.log();

  // Validate card number
  const cardResult = validate(cardNumber);
  if (!cardResult.valid) {
    console.log(`    ❌ Card invalid: ${cardResult.error}`);
    return;
  }
  console.log(`    ✓ Card valid (${cardResult.info?.displayName})`);

  // Validate CVV
  if (!isValidCVV(cvv, cardResult.cardType!)) {
    console.log(`    ❌ CVV invalid (expected ${cardResult.info?.cvvLength} digits)`);
    return;
  }
  console.log(`    ✓ CVV valid`);

  // Validate expiry
  const expiryResult = validateExpiryString(expiry);
  if (!expiryResult.valid) {
    console.log(`    ❌ Expiry invalid: ${expiryResult.error}`);
    return;
  }
  console.log(`    ✓ Expiry valid (${expiryResult.month}/${expiryResult.year})`);

  if (expiryResult.expired) {
    console.log(`    ❌ Card is expired!`);
    return;
  }

  if (expiryResult.expiresSoon) {
    console.log(`    ⚠ Card expires within 30 days`);
  }

  console.log(`    ✅ All validations passed!`);
}

// Valid payment
validatePayment('4111111111111111', '123', '12/30');

console.log();

// Invalid payment examples
validatePayment('4111111111111112', '123', '12/30'); // Invalid card
console.log();
validatePayment('378282246310005', '123', '12/30'); // Wrong CVV length for Amex
console.log();
validatePayment('4111111111111111', '123', '01/2020'); // Expired

console.log('\n' + '='.repeat(50));
console.log('Examples completed!');