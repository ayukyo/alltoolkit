/**
 * Base64 Utilities - 单元测试
 * 
 * 运行方式:
 * - Node.js: node base64_utils_test.js
 * - 浏览器: 在控制台加载 mod.js 后运行 testAll()
 */

// 加载模块（Node.js 环境）
const Base64Utils = (typeof require !== 'undefined') 
  ? require('./mod.js') 
  : { encode, decode, toUrlSafe, fromUrlSafe, isValid, toUint8Array, fromUint8Array, encodedLength };

const { encode, decode, toUrlSafe, fromUrlSafe, isValid, toUint8Array, fromUint8Array, encodedLength } = Base64Utils;

// 测试结果统计
let passed = 0;
let failed = 0;

/**
 * 断言函数
 */
function assert(condition, message) {
  if (condition) {
    passed++;
    console.log(`✓ ${message}`);
  } else {
    failed++;
    console.error(`✗ ${message}`);
  }
}

/**
 * 测试 encode 函数
 */
function testEncode() {
  console.log('\n=== Testing encode() ===');
  
  // 基本编码测试
  assert(encode('Hello World') === 'SGVsbG8gV29ybGQ=', 'Basic encoding');
  assert(encode('') === '', 'Empty string encoding');
  assert(encode('A') === 'QQ==', 'Single character encoding');
  assert(encode('AB') === 'QUI=', 'Two characters encoding');
  assert(encode('ABC') === 'QUJD', 'Three characters encoding');
  
  // URL 安全编码
  assert(encode('Hello World', { urlSafe: true, pad: false }) === 'SGVsbG8gV29ybGQ', 'URL-safe encoding without padding');
  assert(encode('>>>???', { urlSafe: true }) === 'Pj4-Pz8_', 'URL-safe encoding with special chars');
  
  // 无填充编码
  assert(encode('A', { pad: false }) === 'QQ', 'Encoding without padding');
  
  // Unicode 测试
  assert(encode('你好') === '5L2g5aW9', 'Chinese encoding');
  assert(encode('🎉') === '8J+OiQ==', 'Emoji encoding');
  assert(encode('日本語') === '5pel5pys6Kqe', 'Japanese encoding');
  
  // 错误处理
  try {
    encode(123);
    assert(false, 'Should throw TypeError for non-string input');
  } catch (e) {
    assert(e instanceof TypeError, 'Throws TypeError for non-string input');
  }
}

/**
 * 测试 decode 函数
 */
function testDecode() {
  console.log('\n=== Testing decode() ===');
  
  // 基本解码测试
  assert(decode('SGVsbG8gV29ybGQ=') === 'Hello World', 'Basic decoding');
  assert(decode('') === '', 'Empty string decoding');
  assert(decode('QQ==') === 'A', 'Single character decoding');
  assert(decode('QUI=') === 'AB', 'Two characters decoding');
  assert(decode('QUJD') === 'ABC', 'Three characters decoding');
  
  // URL 安全解码
  assert(decode('SGVsbG8gV29ybGQ', { urlSafe: true }) === 'Hello World', 'URL-safe decoding');
  assert(decode('Pj4-Pz8_', { urlSafe: true }) === '>>>???', 'URL-safe decoding with special chars');
  
  // Unicode 解码
  assert(decode('5L2g5aW9') === '你好', 'Chinese decoding');
  assert(decode('8J+OiQ==') === '🎉', 'Emoji decoding');
  assert(decode('5pel5pys6Kqe') === '日本語', 'Japanese decoding');
  
  // 错误处理
  try {
    decode(123);
    assert(false, 'Should throw TypeError for non-string input');
  } catch (e) {
    assert(e instanceof TypeError, 'Throws TypeError for non-string input');
  }
  
  try {
    decode('Invalid!!!');
    assert(false, 'Should throw Error for invalid Base64');
  } catch (e) {
    assert(e instanceof Error, 'Throws Error for invalid Base64');
  }
}

/**
 * 测试 toUrlSafe 函数
 */
function testToUrlSafe() {
  console.log('\n=== Testing toUrlSafe() ===');
  
  assert(toUrlSafe('SGVsbG8gV29ybGQ=') === 'SGVsbG8gV29ybGQ', 'Convert to URL-safe (no padding)');
  assert(toUrlSafe('SGVsbG8gV29ybGQ=', true) === 'SGVsbG8gV29ybGQ=', 'Convert to URL-safe (with padding)');
  assert(toUrlSafe('a+b/c=') === 'a-b_c', 'Replace + and /');
  
  // 错误处理
  try {
    toUrlSafe(123);
    assert(false, 'Should throw TypeError for non-string input');
  } catch (e) {
    assert(e instanceof TypeError, 'Throws TypeError for non-string input');
  }
}

/**
 * 测试 fromUrlSafe 函数
 */
function testFromUrlSafe() {
  console.log('\n=== Testing fromUrlSafe() ===');
  
  assert(fromUrlSafe('SGVsbG8gV29ybGQ') === 'SGVsbG8gV29ybGQ=', 'Convert from URL-safe');
  assert(fromUrlSafe('a-b_c') === 'a+b/c===', 'Replace - and _');
  assert(fromUrlSafe('QQ') === 'QQ==', 'Add padding for 2 chars');
  assert(fromUrlSafe('QUI') === 'QUI=', 'Add padding for 3 chars');
  
  // 错误处理
  try {
    fromUrlSafe(123);
    assert(false, 'Should throw TypeError for non-string input');
  } catch (e) {
    assert(e instanceof TypeError, 'Throws TypeError for non-string input');
  }
}

/**
 * 测试 isValid 函数
 */
function testIsValid() {
  console.log('\n=== Testing isValid() ===');
  
  // 有效 Base64
  assert(isValid('SGVsbG8gV29ybGQ=') === true, 'Valid Base64 with padding');
  assert(isValid('SGVsbG8gV29ybGQ') === true, 'Valid Base64 without padding');
  assert(isValid('') === false, 'Empty string is invalid');
  
  // 无效 Base64
  assert(isValid('Invalid!!!') === false, 'Invalid characters');
  assert(isValid('QQQQ') === true, 'Valid length (mod 4 = 0)');
  
  // URL 安全验证
  assert(isValid('SGVsbG8gV29ybGQ', { urlSafe: true }) === true, 'Valid URL-safe Base64');
  assert(isValid('a+b/c=', { urlSafe: true }) === false, 'Standard Base64 is invalid for URL-safe check');
  assert(isValid('a-b_cA', { urlSafe: true }) === true, 'Valid URL-safe with - and _');
  
  // 填充选项
  assert(isValid('SGVsbG8gV29ybGQ=', { allowPadding: false }) === false, 'Padding not allowed');
  assert(isValid('SGVsbG8gV29ybGQ', { allowPadding: false }) === true, 'No padding with allowPadding: false');
}

/**
 * 测试 toUint8Array 函数
 */
function testToUint8Array() {
  console.log('\n=== Testing toUint8Array() ===');
  
  const arr1 = toUint8Array('SGVsbG8gV29ybGQ=');
  assert(arr1 instanceof Uint8Array, 'Returns Uint8Array');
  assert(arr1.length === 11, 'Correct length');
  assert(arr1[0] === 72 && arr1[1] === 101, 'Correct values');
  
  const arr2 = toUint8Array('');
  assert(arr2.length === 0, 'Empty string returns empty array');
  
  // 错误处理
  try {
    toUint8Array(123);
    assert(false, 'Should throw TypeError for non-string input');
  } catch (e) {
    assert(e instanceof TypeError, 'Throws TypeError for non-string input');
  }
}

/**
 * 测试 fromUint8Array 函数
 */
function testFromUint8Array() {
  console.log('\n=== Testing fromUint8Array() ===');
  
  const bytes = new Uint8Array([72, 101, 108, 108, 111]);
  assert(fromUint8Array(bytes) === 'SGVsbG8=', 'Basic encoding from Uint8Array');
  
  const empty = new Uint8Array([]);
  assert(fromUint8Array(empty) === '', 'Empty array returns empty string');
  
  // URL 安全编码
  const special = new Uint8Array([62, 62, 62, 63, 63, 63]);
  assert(fromUint8Array(special, { urlSafe: true }) === 'Pj4-Pz8_', 'URL-safe encoding from Uint8Array');
  
  // 错误处理
  try {
    fromUint8Array('not an array');
    assert(false, 'Should throw TypeError for non-Uint8Array input');
  } catch (e) {
    assert(e instanceof TypeError, 'Throws TypeError for non-Uint8Array input');
  }
}

/**
 * 测试 encodedLength 函数
 */
function testEncodedLength() {
  console.log('\n=== Testing encodedLength() ===');
  
  assert(encodedLength('Hello') === 8, 'Length with padding');
  assert(encodedLength('Hello', { pad: false }) === 7, 'Length without padding');
  assert(encodedLength('A') === 4, 'Single char length');
  assert(encodedLength('AB') === 4, 'Two chars length');
  assert(encodedLength('ABC') === 4, 'Three chars length');
  assert(encodedLength('') === 0, 'Empty string length');
  assert(encodedLength(123) === 0, 'Non-string returns 0');
}

/**
 * 测试编解码一致性
 */
function testRoundTrip() {
  console.log('\n=== Testing Round-trip Consistency ===');
  
  const testCases = [
    'Hello World',
    'The quick brown fox jumps over the lazy dog',
    '你好，世界！',
    '🎉🎊🎁',
    '日本語テキスト',
    'Special chars: !@#$%^&*()',
    '',
    'A',
    'AB',
    'ABC'
  ];
  
  for (const testCase of testCases) {
    const encoded = encode(testCase);
    const decoded = decode(encoded);
    assert(decoded === testCase, `Round-trip: "${testCase.substring(0, 20)}`);
  }
}

/**
 * 运行所有测试
 */
function testAll() {
  console.log('Starting Base64 Utils Tests...\n');
  
  testEncode();
  testDecode();
  testToUrlSafe();
  testFromUrlSafe();
  testIsValid();
  testToUint8Array();
  testFromUint8Array();
  testEncodedLength();
  testRoundTrip();
  
  console.log('\n=== Test Summary ===');
  console.log(`Passed: ${passed}`);
  console.log(`Failed: ${failed}`);
  console.log(`Total: ${passed + failed}`);
  
  if (failed === 0) {
    console.log('\n✓ All tests passed!');
    return true;
  } else {
    console.log(`\n✗ ${failed} test(s) failed`);
    return false;
  }
}

// Node.js 环境自动运行测试
if (typeof module !== 'undefined' && require.main === module) {
  const success = testAll();
  process.exit(success ? 0 : 1);
}
