/**
 * UUID Utilities Test Suite
 * 
 * Comprehensive tests for the UUID utilities module.
 * Run with: npx ts-node uuid_utils_test.ts
 * Or compile: tsc uuid_utils_test.ts && node uuid_utils_test.js
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

// ==================== UUID v4 Tests ====================

test('v4() generates valid UUID', () => {
  const uuid = v4();
  assertTrue(isValid(uuid), 'Generated UUID should be valid');
  assertEqual(getVersion(uuid), 4, 'Should be version 4');
});

test('v4() generates unique UUIDs', () => {
  const uuids = new Set<string>();
  for (let i = 0; i < 100; i++) {
    uuids.add(v4());
  }
  assertEqual(uuids.size, 100, 'All 100 UUIDs should be unique');
});

test('v4() generates correct format', () => {
  const uuid = v4();
  assertMatch(uuid, /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/, 
    'Should match UUID v4 pattern');
});

// ==================== UUID v1 Tests ====================

test('v1() generates valid UUID', () => {
  const uuid = v1();
  assertTrue(isValid(uuid), 'Generated UUID should be valid');
  assertEqual(getVersion(uuid), 1, 'Should be version 1');
});

test('v1() generates unique UUIDs', () => {
  const uuids = new Set<string>();
  for (let i = 0; i < 100; i++) {
    uuids.add(v1());
  }
  assertEqual(uuids.size, 100, 'All 100 UUIDs should be unique');
});

test('v1() generates correct format', () => {
  const uuid = v1();
  assertMatch(uuid, /^[0-9a-f]{8}-[0-9a-f]{4}-1[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/, 
    'Should match UUID v1 pattern');
});

// ==================== Compact UUID Tests ====================

test('compact() generates valid compact UUID', () => {
  const compactUuid = compact();
  assertEqual(compactUuid.length, 32, 'Compact UUID should be 32 characters');
  assertMatch(compactUuid, /^[0-9a-f]{32}$/, 'Should be lowercase hex');
});

test('compact() with version 1', () => {
  const compactUuid = compact(1);
  assertEqual(compactUuid.length, 32, 'Compact UUID should be 32 characters');
});

test('compact() generates unique values', () => {
  const uuids = new Set<string>();
  for (let i = 0; i < 100; i++) {
    uuids.add(compact());
  }
  assertEqual(uuids.size, 100, 'All 100 compact UUIDs should be unique');
});

// ==================== Uppercase UUID Tests ====================

test('uppercase() generates uppercase UUID', () => {
  const upper = uppercase();
  assertMatch(upper, /^[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}$/, 
    'Should be uppercase');
});

// ==================== Validation Tests ====================

test('isValid() returns true for valid UUID v4', () => {
  assertTrue(isValid('550e8400-e29b-41d4-a716-446655440000'), 'Should be valid');
});

test('isValid() returns true for valid UUID v1', () => {
  assertTrue(isValid('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'), 'Should be valid');
});

test('isValid() returns false for invalid UUID', () => {
  assertFalse(isValid('invalid'), 'Should be invalid');
  assertFalse(isValid(''), 'Empty string should be invalid');
  assertFalse(isValid('550e8400-e29b-41d4-a716-44665544'), 'Too short');
  assertFalse(isValid('550e8400-e29b-41d4-a716-44665544000g'), 'Invalid character');
});

test('isValid() with version check', () => {
  assertTrue(isValid('550e8400-e29b-41d4-a716-446655440000', 4), 'Should be valid v4');
  assertFalse(isValid('550e8400-e29b-41d4-a716-446655440000', 1), 'Should not be v1');
});

test('isValid() handles null and undefined', () => {
  assertFalse(isValid(null as any), 'null should be invalid');
  assertFalse(isValid(undefined as any), 'undefined should be invalid');
});

// ==================== Parsing Tests ====================

test('parse() returns correct version and variant', () => {
  const parsed = parse('550e8400-e29b-41d4-a716-446655440000');
  assertTrue(parsed !== null, 'Should parse successfully');
  assertEqual(parsed!.version, 4, 'Should be version 4');
  assertEqual(parsed!.variant, 1, 'Should be RFC 4122 variant');
});

test('parse() returns null for invalid UUID', () => {
  const parsed = parse('invalid');
  assertEqual(parsed, null, 'Should return null for invalid UUID');
});

test('parse() extracts timestamp for v1', () => {
  const uuid = v1();
  const parsed = parse(uuid);
  assertTrue(parsed !== null, 'Should parse successfully');
  assertTrue(parsed!.timestamp instanceof Date, 'Should have timestamp');
});

// ==================== Version and Variant Tests ====================

test('getVersion() returns correct version', () => {
  assertEqual(getVersion('550e8400-e29b-41d4-a716-446655440000'), 4, 'Should be version 4');
  assertEqual(getVersion('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'), 1, 'Should be version 1');
  assertEqual(getVersion('invalid'), -1, 'Invalid UUID returns -1');
});

test('getVariant() returns correct variant', () => {
  assertEqual(getVariant('550e8400-e29b-41d4-a716-446655440000'), 1, 'Should be RFC 4122');
  assertEqual(getVariant('invalid'), -1, 'Invalid UUID returns -1');
});

// ==================== Format Conversion Tests ====================

test('toCompact() converts standard to compact', () => {
  const compact = toCompact('550e8400-e29b-41d4-a716-446655440000');
  assertEqual(compact, '550e8400e29b41d4a716446655440000', 'Should remove hyphens');
});

test('toCompact() returns null for invalid UUID', () => {
  assertEqual(toCompact('invalid'), null, 'Should return null');
});

test('toStandard() converts compact to standard', () => {
  const standard = toStandard('550e8400e29b41d4a716446655440000');
  assertEqual(standard, '550e8400-e29b-41d4-a716-446655440000', 'Should add hyphens');
});

test('toStandard() returns null for invalid compact', () => {
  assertEqual(toStandard('invalid'), null, 'Should return null');
  assertEqual(toStandard('550e8400'), null, 'Too short');
});

test('equals() compares UUIDs case-insensitively', () => {
  assertTrue(
    equals('550e8400-e29b-41d4-a716-446655440000', '550E8400-E29B-41D4-A716-446655440000'),
    'Should be equal (case insensitive)'
  );
  assertFalse(
    equals('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440001'),
    'Different UUIDs should not be equal'
  );
  assertFalse(equals('invalid', '550e8400-e29b-41d4-a716-446655440000'), 'Invalid UUIDs not equal');
});

// ==================== Nano ID Tests ====================

test('nanoId() generates correct length', () => {
  assertEqual(nanoId().length, 21, 'Default length should be 21');
  assertEqual(nanoId(10).length, 10, 'Custom length should work');
  assertEqual(nanoId(0).length, 0, 'Zero length should work');
});

test('nanoId() generates unique values', () => {
  const ids = new Set<string>();
  for (let i = 0; i < 100; i++) {
    ids.add(nanoId());
  }
  assertEqual(ids.size, 100, 'All 100 Nano IDs should be unique');
});

test('nanoId() uses URL-safe characters', () => {
  const id = nanoId(100);
  assertMatch(id, /^[A-Za-z0-9_-]+$/, 'Should only contain URL-safe characters');
});

// ==================== Short ID Tests ====================

test('shortId() generates correct length', () => {
  assertEqual(shortId().length, 8, 'Default length should be 8');
  assertEqual(shortId(16).length, 16, 'Custom length should work');
});

test('shortId() generates unique values', () => {
  const ids = new Set<string>();
  for (let i = 0; i < 100; i++) {
    ids.add(shortId());
  }
  assertEqual(ids.size, 100, 'All 100 short IDs should be unique');
});

test('shortId() uses alphanumeric characters', () => {
  const id = shortId(100);
  assertMatch(id, /^[A-Za-z0-9]+$/, 'Should only contain alphanumeric characters');
});

// ==================== Random String Tests ====================

test('randomString() generates correct length', () => {
  assertEqual(randomString(10).length, 10, 'Should generate correct length');
  assertEqual(randomString(0).length, 0, 'Zero length should work');
});

test('randomString() uses specified charset', () => {
  const str = randomString(100, CHARSETS.DIGITS);
  assertMatch(str, /^[0-9]+$/, 'Should only contain digits');
});

test('randomString() generates unique values', () => {
  const strs = new Set<string>();
  for (let i = 0; i < 100; i++) {
    strs.add(randomString(16));
  }
  assertEqual(strs.size, 100, 'All 100 strings should be unique');
});

// ==================== Random Password Tests ====================

test('randomPassword() generates correct length', () => {
  assertEqual(randomPassword().length, 16, 'Default length should be 16');
  assertEqual(randomPassword(8).length, 8, 'Minimum length should be 8');
  assertEqual(randomPassword(32).length, 32, 'Custom length should work');
});

test('randomPassword() enforces minimum length', () => {
  assertEqual(randomPassword(4).length, 8, 'Should enforce minimum length of 8');
});

test('randomPassword() contains required character types', () => {
  const password = randomPassword(16);
  assertMatch(password, /[A-Z]/, 'Should contain uppercase');
  assertMatch(password, /[a-z]/, 'Should contain lowercase');
  assertMatch(password, /[0-9]/, 'Should contain digits');
  assertMatch(password, /[!@#$%^&*()\-_=+\[\]{}|;:,.<>?]/, 'Should contain special characters');
});

test('randomPassword() generates unique passwords', () => {
  const passwords = new Set<string>();
  for (let i = 0; i < 100; i++) {
    passwords.add(randomPassword());
  }
  assertEqual(passwords.size, 100, 'All 100 passwords should be unique');
});

// ==================== Constants Tests ====================

test('CHARSETS constants are defined', () => {
  assertTrue(CHARSETS.LOWERCASE.length > 0, 'LOWERCASE should be defined');
  assertTrue(CHARSETS.UPPERCASE.length > 0, 'UPPERCASE should be defined');
  assertTrue(CHARSETS.DIGITS.length > 0, 'DIGITS should be defined');
  assertTrue(CHARSETS.SPECIAL.length > 0, 'SPECIAL should be defined');
  assertTrue(CHARSETS.HEX.length > 0, 'HEX should be defined');
  assertTrue(CHARSETS.ALPHANUMERIC.length > 0, 'ALPHANUMERIC should be defined');
  assertTrue(CHARSETS.URL_SAFE.length > 0, 'URL_SAFE should be defined');
});

// ==================== Namespace Tests ====================

test('UuidUtils namespace exports all functions', () => {
  assertTrue(typeof UuidUtils.v4 === 'function', 'v4 should be exported');
  assertTrue(typeof UuidUtils.v1 === 'function', 'v1 should be exported');
  assertTrue(typeof UuidUtils.compact === 'function', 'compact should be exported');
  assertTrue(typeof UuidUtils.uppercase === 'function', 'uppercase should be exported');
  assertTrue(typeof UuidUtils.isValid === 'function', 'isValid should be exported');
  assertTrue(typeof UuidUtils.parse === 'function', 'parse should be exported');
  assertTrue(typeof UuidUtils.getVersion === 'function', 'getVersion should be exported');
  assertTrue(typeof UuidUtils.getVariant === 'function', 'getVariant should be exported');
  assertTrue(typeof UuidUtils.toCompact === 'function', 'toCompact should be exported');
  assertTrue(typeof UuidUtils.toStandard === 'function', 'toStandard should be exported');
  assertTrue(typeof UuidUtils.equals === 'function', 'equals should be exported');
  assertTrue(typeof UuidUtils.nanoId === 'function', 'nanoId should be exported');
  assertTrue(typeof UuidUtils.shortId === 'function', 'shortId should be exported');
  assertTrue(typeof UuidUtils.randomString === 'function', 'randomString should be exported');
  assertTrue(typeof UuidUtils.randomPassword === 'function', 'randomPassword should be exported');
});

// ==================== Run Tests ====================

console.log('Running UUID Utils Test Suite...\n');

// Run all tests
// (Tests are executed as they are defined above)

console.log('\n=========================');
console.log(`Total: ${passed + failed} tests`);
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
console.log('=========================');

if (failed > 0) {
  process.exit(1);
}