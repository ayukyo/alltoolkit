# Credit Card Utilities

A comprehensive TypeScript utility module for credit card validation and processing, with **zero external dependencies**.

## Features

- ✅ **Card Number Validation** - Luhn algorithm implementation
- ✅ **Card Type Detection** - Visa, MasterCard, Amex, Discover, JCB, Diners Club, UnionPay, Mir, Maestro
- ✅ **Number Formatting** - Standard 4-digit groups, Amex 4-6-5 format
- ✅ **Number Masking** - Secure display with configurable visibility
- ✅ **CVV Validation** - Type-specific CVV length validation
- ✅ **Expiry Date Validation** - Parse and validate MM/YY, MM/YYYY formats
- ✅ **BIN/IIN Extraction** - Bank Identification Number helpers
- ✅ **Test Number Generation** - Generate valid test numbers for each card type
- ✅ **Zero Dependencies** - Uses only TypeScript/JavaScript standard library

## Installation

No external dependencies required. Just import the module:

```typescript
import CreditCardUtils, { validate, CardType } from './mod';
```

## Quick Start

### Basic Validation

```typescript
import { validate, isValid } from './mod';

// Comprehensive validation
const result = validate('4111111111111111');
console.log(result.valid); // true
console.log(result.cardType); // CardType.VISA

// Quick check
if (isValid('4111111111111111')) {
  console.log('Card is valid!');
}
```

### Card Type Detection

```typescript
import { detectCardType, getCardTypeName, CardType } from './mod';

const type = detectCardType('378282246310005');
console.log(type); // CardType.AMEX
console.log(getCardTypeName('378282246310005')); // 'American Express'
```

### Formatting & Masking

```typescript
import { format, mask, maskFormatted } from './mod';

// Format with spaces
console.log(format('4111111111111111')); // '4111 1111 1111 1111'
console.log(format('378282246310005'));  // '3782 822463 10005' (Amex)

// Mask for display
console.log(mask('4111111111111111')); // '4111********1111'
console.log(mask('4111111111111111', 6, 4)); // '411111******1111'

// Masked with formatting
console.log(maskFormatted('4111111111111111')); // '4111 **** **** 1111'
```

### Luhn Algorithm

```typescript
import { luhnCheck, calculateLuhnCheckDigit } from './mod';

// Check validity
console.log(luhnCheck('4111111111111111')); // true

// Calculate check digit for partial number
const checkDigit = calculateLuhnCheckDigit('411111111111111');
console.log(checkDigit); // 1
console.log('411111111111111' + checkDigit); // '4111111111111111' (valid)
```

### CVV Validation

```typescript
import { isValidCVV, CardType } from './mod';

// Generic validation (3-4 digits)
console.log(isValidCVV('123')); // true
console.log(isValidCVV('1234')); // true

// Type-specific validation
console.log(isValidCVV('123', CardType.VISA)); // true (Visa uses 3 digits)
console.log(isValidCVV('1234', CardType.AMEX)); // true (Amex uses 4 digits)
console.log(isValidCVV('123', CardType.AMEX)); // false (wrong length)
```

### Expiry Date Validation

```typescript
import { validateExpiry, validateExpiryString } from './mod';

// String parsing
const result1 = validateExpiryString('12/30');
console.log(result1.valid); // true
console.log(result1.year); // 2030

// Numeric input
const result2 = validateExpiry(12, 2025);
console.log(result2.expired); // false
console.log(result2.expiresSoon); // warns if < 30 days
```

### BIN/IIN Extraction

```typescript
import { getBIN, isValidBIN } from './mod';

console.log(getBIN('4111111111111111', 6)); // '411111'
console.log(getBIN('4111111111111111', 8)); // '41111111'
console.log(isValidBIN('411111')); // true
```

### Test Number Generation

```typescript
import { generateTestNumber, CardType } from './mod';

const visaTest = generateTestNumber(CardType.VISA);
console.log(visaTest); // e.g., '4111111111111111'
console.log(luhnCheck(visaTest)); // true

const amexTest = generateTestNumber(CardType.AMEX);
console.log(amexTest.length); // 15
```

### Complete Validation Workflow

```typescript
import { validate, isValidCVV, validateExpiryString } from './mod';

function validatePayment(card: string, cvv: string, expiry: string) {
  const cardResult = validate(card);
  if (!cardResult.valid) return { error: cardResult.error };
  
  if (!isValidCVV(cvv, cardResult.cardType!)) {
    return { error: 'Invalid CVV' };
  }
  
  const expiryResult = validateExpiryString(expiry);
  if (!expiryResult.valid) return { error: expiryResult.error };
  if (expiryResult.expired) return { error: 'Card expired' };
  
  return { valid: true, cardType: cardResult.cardType };
}
```

## API Reference

### Validation Functions

| Function | Description |
|----------|-------------|
| `validate(cardNumber)` | Comprehensive validation with full result |
| `isValid(cardNumber)` | Quick boolean check |
| `isValidFormat(cardNumber)` | Check if format is correct (12-19 digits) |
| `isValidLength(cardNumber)` | Check if length matches card type |
| `luhnCheck(cardNumber)` | Luhn algorithm validation |
| `calculateLuhnCheckDigit(partial)` | Calculate check digit |

### Card Type Functions

| Function | Description |
|----------|-------------|
| `detectCardType(cardNumber)` | Detect card type from number |
| `getCardTypeName(cardNumber)` | Get display name |
| `getCardInfo(cardType)` | Get detailed card type info |
| `getAllCardTypes()` | List all supported card types |
| `isCardTypeSupported(type)` | Check if type is supported |

### Formatting Functions

| Function | Description |
|----------|-------------|
| `sanitize(cardNumber)` | Remove non-digit characters |
| `format(cardNumber)` | Format with spaces |
| `mask(cardNumber, start, end, char)` | Mask for display |
| `maskFormatted(cardNumber, ...)` | Masked with formatting |

### Expiry Functions

| Function | Description |
|----------|-------------|
| `validateExpiry(month, year)` | Validate numeric expiry |
| `validateExpiryString(expiry)` | Parse MM/YY or MM/YYYY |

### Other Functions

| Function | Description |
|----------|-------------|
| `isValidCVV(cvv, cardType)` | Validate CVV |
| `getBIN(cardNumber, length)` | Extract BIN/IIN |
| `isValidBIN(bin)` | Validate BIN format |
| `generateTestNumber(cardType)` | Generate valid test number |

## Supported Card Types

| Card Type | Prefixes | Length | CVV |
|-----------|----------|--------|-----|
| Visa | 4 | 13, 16, 19 | 3 |
| MasterCard | 51-55, 2221-2720 | 16 | 3 |
| American Express | 34, 37 | 15 | 4 |
| Discover | 6011, 65, 644-649 | 16, 19 | 3 |
| JCB | 3528-3589 | 16-19 | 3 |
| Diners Club | 36, 38, 39, 300-305 | 14, 16, 19 | 3 |
| UnionPay | 62 | 16-19 | 3 |
| Mir | 2200-2204 | 16 | 3 |
| Maestro | 50, 56-69 | 12-19 | 3 |

## Test Numbers

Valid test numbers for development (these pass Luhn check):

- Visa: `4111111111111111`, `4012888888881881`
- MasterCard: `5555555555554444`, `5105105105105100`
- Amex: `378282246310005`, `371449635398431`
- Discover: `6011111111111117`, `6011000990139424`
- JCB: `3530111333300000`, `3566002020360505`

## Running Tests

```bash
npx ts-node credit_card_utils_test.ts
```

## Running Examples

```bash
npx ts-node examples/credit_card_example.ts
```

## License

MIT

## Version

1.0.0