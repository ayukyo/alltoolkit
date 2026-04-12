/**
 * Crypto Utilities Test Suite
 * 
 * Comprehensive tests for all crypto utility functions.
 * Run with: deno test crypto_utils_test.ts
 * Or: bun test crypto_utils_test.ts
 * Or: npx tsx crypto_utils_test.ts
 */

import {
  // Hash functions
  md5,
  sha1,
  sha256,
  sha384,
  sha512,
  hash,
  
  // HMAC functions
  hmacSha256,
  hmacSha384,
  hmacSha512,
  verifyHmac,
  
  // Base64
  base64Encode,
  base64Decode,
  base64UrlEncode,
  base64UrlDecode,
  isValidBase64,
  
  // Hex
  hexEncode,
  hexDecode,
  isValidHex,
  
  // Random generation
  randomString,
  randomHex,
  uuidv4,
} from './mod.ts';

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
    console.error(`  ✗ ${message}`);
  }
}

function assertEquals<T>(actual: T, expected: T, message: string): void {
  const condition = actual === expected;
  if (!condition) {
    console.error(`    Expected: ${expected}`);
    console.error(`    Got: ${actual}`);
  }
  assert(condition, message);
}

function assertLength(actual: string, expectedLength: number, message: string): void {
  const condition = actual.length === expectedLength;
  if (!condition) {
    console.error(`    Expected length: ${expectedLength}`);
    console.error(`    Got length: ${actual.length}`);
  }
  assert(condition, message);
}

function assertThrows(fn: () => void, message: string): void {
  try {
    fn();
    assert(false, `${message} (should have thrown)`);
  } catch {
    assert(true, message);
  }
}

async function runAsyncTests(): Promise<void> {
  // =============================================================================
  // MD5 Tests
  // =============================================================================
  
  console.log('\n📝 MD5 Hash Tests');
  console.log('=' .repeat(50));
  
  assertEquals(md5(''), 'd41d8cd98f00b204e9800998ecf8427e', 'MD5 empty string');
  assertEquals(md5('hello'), '5d41402abc4b2a76b9719d911017c592', 'MD5 "hello"');
  assertEquals(md5('Hello World'), 'b10a8db164e0754105b7a99be72e3fe5', 'MD5 "Hello World"');
  assertEquals(md5('The quick brown fox jumps over the lazy dog'), '9e107d9d372bb6826bd81d3542a419d6', 'MD5 famous test');
  assertLength(md5('test'), 32, 'MD5 hash length is 32 chars');
  
  // =============================================================================
  // SHA-1 Tests
  // =============================================================================
  
  console.log('\n📝 SHA-1 Hash Tests');
  console.log('=' .repeat(50));
  
  assertEquals(sha1(''), 'da39a3ee5e6b4b0d3255bfef95601890afd80709', 'SHA-1 empty string');
  assertEquals(sha1('hello'), 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d', 'SHA-1 "hello"');
  assertEquals(sha1('Hello World'), '0a4d55a8d778e5022fab701977c5d840bbc486d0', 'SHA-1 "Hello World"');
  assertLength(sha1('test'), 40, 'SHA-1 hash length is 40 chars');
  
  // =============================================================================
  // SHA-256 Tests
  // =============================================================================
  
  console.log('\n📝 SHA-256 Hash Tests');
  console.log('=' .repeat(50));
  
  assertEquals(sha256(''), 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'SHA-256 empty string');
  assertEquals(sha256('hello'), '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', 'SHA-256 "hello"');
  assertEquals(sha256('Hello World'), 'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e', 'SHA-256 "Hello World"');
  assertLength(sha256('hello'), 64, 'SHA-256 hash length is 64 chars');
  
  // =============================================================================
  // SHA-384 Tests
  // =============================================================================
  
  console.log('\n📝 SHA-384 Hash Tests');
  console.log('=' .repeat(50));
  
  assertEquals(sha384(''), '38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95b', 'SHA-384 empty string');
  assertLength(sha384('hello'), 96, 'SHA-384 hash length is 96 chars');
  
  // =============================================================================
  // SHA-512 Tests
  // =============================================================================
  
  console.log('\n📝 SHA-512 Hash Tests');
  console.log('=' .repeat(50));
  
  assertEquals(sha512(''), 'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e', 'SHA-512 empty string');
  assertLength(sha512('hello'), 128, 'SHA-512 hash length is 128 chars');
  
  // =============================================================================
  // Generic Hash Tests
  // =============================================================================
  
  console.log('\n📝 Generic Hash Tests');
  console.log('=' .repeat(50));
  
  assertEquals(hash('hello', 'MD5'), md5('hello'), 'hash() with MD5');
  assertEquals(hash('hello', 'SHA-1'), sha1('hello'), 'hash() with SHA-1');
  assertEquals(hash('hello', 'SHA-256'), sha256('hello'), 'hash() with SHA-256');
  
  try {
    hash('test', 'UNKNOWN' as any);
    assert(false, 'hash() should throw for unknown algorithm');
  } catch {
    assert(true, 'hash() throws for unknown algorithm');
  }
  
  // =============================================================================
  // HMAC Tests
  // =============================================================================
  
  console.log('\n📝 HMAC Tests');
  console.log('=' .repeat(50));
  
  const hmac256 = hmacSha256('message', 'secret');
  assertLength(hmac256, 64, 'HMAC-SHA256 length is 64 chars');
  
  const hmac384 = hmacSha384('message', 'secret');
  assertLength(hmac384, 96, 'HMAC-SHA384 length is 96 chars');
  
  const hmac512 = hmacSha512('message', 'secret');
  assertLength(hmac512, 128, 'HMAC-SHA512 length is 128 chars');
  
  // Verify HMAC
  const validSig = hmacSha256('test message', 'my secret');
  const isValid = verifyHmac('test message', 'my secret', validSig);
  assert(isValid, 'verifyHmac returns true for valid signature');
  
  const isInvalid = verifyHmac('test message', 'wrong secret', validSig);
  assert(!isInvalid, 'verifyHmac returns false for invalid signature');
  
  const isInvalid2 = verifyHmac('wrong message', 'my secret', validSig);
  assert(!isInvalid2, 'verifyHmac returns false for wrong message');
  
  // =============================================================================
  // Base64 Tests
  // =============================================================================
  
  console.log('\n📝 Base64 Encoding/Decoding Tests');
  console.log('=' .repeat(50));
  
  // Basic encoding
  assertEquals(base64Encode('Hello'), 'SGVsbG8=', 'Base64 encode "Hello"');
  assertEquals(base64Encode('Hello World!'), 'SGVsbG8gV29ybGQh', 'Base64 encode "Hello World!"');
  assertEquals(base64Encode(''), '', 'Base64 encode empty string');
  assertEquals(base64Encode('Man'), 'TWFu', 'Base64 encode "Man"');
  assertEquals(base64Encode('Ma'), 'TWE=', 'Base64 encode "Ma" (with padding)');
  assertEquals(base64Encode('M'), 'TQ==', 'Base64 encode "M" (double padding)');
  
  // Basic decoding
  assertEquals(base64Decode('SGVsbG8='), 'Hello', 'Base64 decode "Hello"');
  assertEquals(base64Decode('SGVsbG8gV29ybGQh'), 'Hello World!', 'Base64 decode "Hello World!"');
  assertEquals(base64Decode(''), '', 'Base64 decode empty string');
  
  // Round-trip
  const testStrings = ['Hello', 'World', 'Test 123', 'Special chars: !@#$%^&*()'];
  for (const str of testStrings) {
    assertEquals(base64Decode(base64Encode(str)), str, `Base64 round-trip: "${str}"`);
  }
  
  // URL-safe encoding
  assertEquals(base64UrlEncode('Hello+World/Test'), 'SGVsbG8rV29ybGQvVGVzdA==', 'Base64URL encode');
  const noPad = base64UrlEncode('Hello+World/Test', false);
  assert(!noPad.includes('='), 'Base64URL without padding');
  assert(!noPad.includes('+'), 'Base64URL has no +');
  assert(!noPad.includes('/'), 'Base64URL has no /');
  
  // URL-safe decoding
  assertEquals(base64UrlDecode('SGVsbG8rV29ybGQvVGVzdA'), 'Hello+World/Test', 'Base64URL decode');
  
  // Validation
  assert(isValidBase64('SGVsbG8='), 'isValidBase64 true for valid Base64');
  assert(!isValidBase64('SGVsbG8'), 'isValidBase64 false for no-padding (length check)');
  assert(!isValidBase64('Invalid!'), 'isValidBase64 false for invalid chars');
  assert(!isValidBase64('SGVsbG8==='), 'isValidBase64 false for invalid padding');
  assert(!isValidBase64('abc'), 'isValidBase64 false for invalid length');
  
  // =============================================================================
  // Hex Tests
  // =============================================================================
  
  console.log('\n📝 Hex Encoding/Decoding Tests');
  console.log('=' .repeat(50));
  
  // Basic encoding
  assertEquals(hexEncode('Hello'), '48656c6c6f', 'Hex encode "Hello"');
  assertEquals(hexEncode(''), '', 'Hex encode empty string');
  assertEquals(hexEncode('ABC'), '414243', 'Hex encode "ABC"');
  assertEquals(hexEncode('\x00\x01'), '0001', 'Hex encode binary chars');
  
  // Basic decoding
  assertEquals(hexDecode('48656c6c6f'), 'Hello', 'Hex decode "Hello"');
  assertEquals(hexDecode(''), '', 'Hex decode empty string');
  assertEquals(hexDecode('414243'), 'ABC', 'Hex decode "ABC"');
  assertEquals(hexDecode('414243'), 'ABC', 'Hex decode uppercase');
  assertEquals(hexDecode('414243'), 'ABC', 'Hex decode lowercase');
  
  // Round-trip
  for (const str of ['Test', '123', 'ABC']) {
    assertEquals(hexDecode(hexEncode(str)), str, `Hex round-trip: "${str}"`);
  }
  
  // Validation
  assert(isValidHex('48656c6c6f'), 'isValidHex true for valid hex');
  assert(isValidHex(''), 'isValidHex true for empty string');
  assert(isValidHex('ABCDEF'), 'isValidHex true for uppercase');
  assert(isValidHex('abcdef'), 'isValidHex true for lowercase');
  assert(!isValidHex('ghijkl'), 'isValidHex false for invalid chars');
  assert(!isValidHex('123gh'), 'isValidHex false for mixed invalid');
  
  // Error cases
  assertThrows(() => hexDecode('abc'), 'Hex decode throws for odd length');
  
  // =============================================================================
  // Random Generation Tests
  // =============================================================================
  
  console.log('\n📝 Random Generation Tests');
  console.log('=' .repeat(50));
  
  // randomString
  const random10 = randomString(10);
  assertLength(random10, 10, 'randomString length is correct');
  assert(random10 !== randomString(10), 'randomString produces different values');
  
  const randomDigits = randomString(20, '0123456789');
  assertLength(randomDigits, 20, 'randomString with custom charset length');
  assert(/^\d+$/.test(randomDigits), 'randomString digits only');
  
  const randomAlpha = randomString(15, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ');
  assertLength(randomAlpha, 15, 'randomString uppercase length');
  assert(/[A-Z]+$/.test(randomAlpha), 'randomString uppercase only');
  
  // randomHex
  const hex20 = randomHex(20);
  assertLength(hex20, 20, 'randomHex length is correct');
  assert(/^[0-9a-f]+$/.test(hex20), 'randomHex contains only hex chars');
  
  // uuidv4
  const uuid1 = uuidv4();
  assertLength(uuid1, 36, 'UUID length is 36 chars');
  assert(/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(uuid1), 'UUID v4 format is valid');
  assert(uuid1 !== uuidv4(), 'UUID produces different values');
  
  // UUID components
  const uuidParts = uuid1.split('-');
  assertEquals(uuidParts.length, 5, 'UUID has 5 parts');
  assertEquals(uuidParts[0].length, 8, 'UUID part 1 length');
  assertEquals(uuidParts[1].length, 4, 'UUID part 2 length');
  assertEquals(uuidParts[2].length, 4, 'UUID part 3 length');
  assertEquals(uuidParts[3].length, 4, 'UUID part 4 length');
  assertEquals(uuidParts[4].length, 12, 'UUID part 5 length');
}

// =============================================================================
// Run Tests
// =============================================================================

console.log('\n🔐 Crypto Utilities Test Suite');
console.log('=' .repeat(50));

runAsyncTests().then(() => {
  console.log('\n' + '='.repeat(50));
  console.log(`\n📊 Test Results: ${passed} passed, ${failed} failed\n`);
  
  if (failed > 0) {
    console.error('❌ Some tests failed!');
  } else {
    console.log('✅ All tests passed!');
  }
}).catch(err => {
  console.error('Error running tests:', err);
});