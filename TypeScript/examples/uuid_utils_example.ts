/**
 * UUID Utilities Example
 * 
 * Demonstrates usage of the UUID utilities module for TypeScript.
 * 
 * Run with: npx ts-node uuid_utils_example.ts
 */

import {
  v4,
  v1,
  compact,
  uppercase,
  isValid,
  parse,
  getVersion,
  getVariant,
  toCompact,
  toStandard,
  equals,
  nanoId,
  shortId,
  randomString,
  randomPassword,
  UuidUtils,
  CHARSETS,
  UUID_NAMESPACES,
} from '../uuid_utils/mod';

console.log('========================================');
console.log('UUID Utilities Examples');
console.log('========================================\n');

// ==================== UUID Generation ====================

console.log('--- UUID v4 (Random-based) ---');
const uuid4 = v4();
console.log(`Generated UUID v4: ${uuid4}`);
console.log(`Is valid: ${isValid(uuid4)}`);
console.log(`Version: ${getVersion(uuid4)}`);
console.log(`Variant: ${getVariant(uuid4)}`);
console.log();

console.log('--- UUID v1 (Timestamp-based) ---');
const uuid1 = v1();
console.log(`Generated UUID v1: ${uuid1}`);
console.log(`Is valid: ${isValid(uuid1)}`);
console.log(`Version: ${getVersion(uuid1)}`);
console.log();

// ==================== Format Variations ====================

console.log('--- Format Variations ---');
const standard = v4();
console.log(`Standard format:  ${standard}`);
console.log(`Compact format:   ${compact()}`);
console.log(`Uppercase format: ${uppercase()}`);
console.log();

// ==================== Parsing UUIDs ====================

console.log('--- Parsing UUIDs ---');
const parsedV4 = parse(standard);
console.log(`Parsed UUID v4:`, parsedV4);

const parsedV1 = parse(uuid1);
console.log(`Parsed UUID v1:`, parsedV1);
console.log(`  Timestamp: ${parsedV1?.timestamp?.toISOString()}`);
console.log(`  Clock Seq: ${parsedV1?.clockSeq}`);
console.log(`  Node: ${parsedV1?.node}`);
console.log();

// ==================== Validation ====================

console.log('--- Validation ---');
console.log(`Is '550e8400-e29b-41d4-a716-446655440000' valid? ${isValid('550e8400-e29b-41d4-a716-446655440000')}`);
console.log(`Is 'invalid-uuid' valid? ${isValid('invalid-uuid')}`);
console.log(`Is '${standard}' a v4? ${isValid(standard, 4)}`);
console.log(`Is '${uuid1}' a v1? ${isValid(uuid1, 1)}`);
console.log();

// ==================== Format Conversion ====================

console.log('--- Format Conversion ---');
const testUuid = '550e8400-e29b-41d4-a716-446655440000';
const compactUuid = toCompact(testUuid);
const backToStandard = toStandard(compactUuid || '');

console.log(`Original:      ${testUuid}`);
console.log(`To compact:    ${compactUuid}`);
console.log(`Back to standard: ${backToStandard}`);
console.log();

// ==================== UUID Comparison ====================

console.log('--- UUID Comparison ---');
const uuidA = '550e8400-e29b-41d4-a716-446655440000';
const uuidB = '550E8400-E29B-41D4-A716-446655440000';
const uuidC = '6ba7b810-9dad-11d1-80b4-00c04fd430c8';

console.log(`UUID A: ${uuidA}`);
console.log(`UUID B: ${uuidB}`);
console.log(`UUID C: ${uuidC}`);
console.log(`A equals B (case insensitive): ${equals(uuidA, uuidB)}`);
console.log(`A equals C: ${equals(uuidA, uuidC)}`);
console.log();

// ==================== Alternative IDs ====================

console.log('--- Nano ID (URL-safe) ---');
console.log(`Default (21 chars): ${nanoId()}`);
console.log(`Custom (10 chars):  ${nanoId(10)}`);
console.log(`Custom (32 chars):  ${nanoId(32)}`);
console.log();

console.log('--- Short ID (Base62) ---');
console.log(`Default (8 chars):  ${shortId()}`);
console.log(`Custom (16 chars):  ${shortId(16)}`);
console.log();

// ==================== Random String Generation ====================

console.log('--- Random String Generation ---');
console.log(`Alphanumeric (16): ${randomString(16)}`);
console.log(`Digits only (6):   ${randomString(6, CHARSETS.DIGITS)}`);
console.log(`Hex only (16):     ${randomString(16, CHARSETS.HEX)}`);
console.log(`Uppercase (8):     ${randomString(8, CHARSETS.UPPERCASE)}`);
console.log();

// ==================== Secure Password Generation ====================

console.log('--- Secure Password Generation ---');
console.log(`Default (16 chars): ${randomPassword()}`);
console.log(`Short (8 chars):    ${randomPassword(8)}`);
console.log(`Long (32 chars):    ${randomPassword(32)}`);
console.log();

// ==================== Using UuidUtils Namespace ====================

console.log('--- Using UuidUtils Namespace ---');
const nsUuid = UuidUtils.v4();
console.log(`Via namespace: ${nsUuid}`);
console.log(`Is valid: ${UuidUtils.isValid(nsUuid)}`);
console.log();

// ==================== Predefined Namespaces ====================

console.log('--- Predefined Namespaces ---');
console.log(`DNS:  ${UUID_NAMESPACES.DNS}`);
console.log(`URL:  ${UUID_NAMESPACES.URL}`);
console.log(`OID:  ${UUID_NAMESPACES.OID}`);
console.log(`X500: ${UUID_NAMESPACES.X500}`);
console.log();

// ==================== Practical Use Cases ====================

console.log('--- Practical Use Cases ---');

// Generate multiple UUIDs for database records
console.log('\n1. Database Record IDs:');
const records = Array.from({ length: 5 }, (_, i) => ({
  id: v4(),
  name: `Record ${i + 1}`,
}));
records.forEach(record => console.log(`   ${record.name}: ${record.id}`));

// Generate session tokens
console.log('\n2. Session Tokens (Nano ID):');
const sessions = Array.from({ length: 3 }, () => nanoId(32));
sessions.forEach((token, i) => console.log(`   Session ${i + 1}: ${token}`));

// Generate API keys
console.log('\n3. API Keys (Short ID):');
const apiKeys = Array.from({ length: 3 }, () => shortId(24));
apiKeys.forEach((key, i) => console.log(`   Key ${i + 1}: ${key}`));

// Generate temporary passwords
console.log('\n4. Temporary Passwords:');
const passwords = Array.from({ length: 3 }, () => randomPassword(12));
passwords.forEach((pwd, i) => console.log(`   Password ${i + 1}: ${pwd}`));

console.log('\n========================================');
console.log('Examples completed successfully!');
console.log('========================================');