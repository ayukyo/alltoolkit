/**
 * String Utilities Test Suite for ArkTS
 * 
 * Comprehensive tests for the string_utils module.
 */

import {
  isBlank, isNotBlank, isEmpty,
  trim, trimLeft, trimRight, removeWhitespace, normalizeWhitespace,
  toLowerCase, toUpperCase, capitalize, uncapitalize, toTitleCase,
  toCamelCase, toPascalCase, toSnakeCase, toKebabCase,
  truncate, substringBetween, substringAfter, substringBefore,
  substringAfterLast, substringBeforeLast,
  startsWith, endsWith, removePrefix, removeSuffix,
  isValidEmail, isValidUrl, isNumeric, isInteger, isAlpha, isAlphanumeric,
  padLeft, padRight, center,
  contains, countMatches, replaceAll,
  split, lines, join,
  base64Encode, base64Decode, urlEncode, urlDecode,
  randomString, randomAlphanumeric, randomNumeric, randomPassword,
  reverse, repeat, defaultIfBlank, defaultIfEmpty, equals, slugify,
  StringUtils
} from './mod';

// ============================================
// Test Results
// ============================================

let passed = 0;
let failed = 0;

function test(name: string, fn: () => void): void {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (e) {
    console.error(`✗ ${name}: ${e}`);
    failed++;
  }
}

function assertEqual(actual: unknown, expected: unknown, msg?: string): void {
  if (actual !== expected) {
    throw new Error(`${msg || 'Assertion failed'}: expected ${expected}, got ${actual}`);
  }
}

function assertTrue(value: boolean, msg?: string): void {
  if (!value) {
    throw new Error(msg || 'Expected true, got false');
  }
}

function assertFalse(value: boolean, msg?: string): void {
  if (value) {
    throw new Error(msg || 'Expected false, got true');
  }
}

// ============================================
// Empty/Blank Tests
// ============================================

export function runTests(): void {
  console.log('Running StringUtils Tests...\n');

  // Empty/Blank Tests
  test('isBlank with null', () => assertTrue(isBlank(null)));
  test('isBlank with undefined', () => assertTrue(isBlank(undefined)));
  test('isBlank with empty string', () => assertTrue(isBlank('')));
  test('isBlank with whitespace', () => assertTrue(isBlank('   ')));
  test('isBlank with content', () => assertFalse(isBlank('hello')));
  
  test('isNotBlank with content', () => assertTrue(isNotBlank('hello')));
  test('isNotBlank with null', () => assertFalse(isNotBlank(null)));
  
  test('isEmpty with empty string', () => assertTrue(isEmpty('')));
  test('isEmpty with whitespace', () => assertFalse(isEmpty('   ')));

  // Trimming Tests
  test('trim removes whitespace', () => assertEqual(trim('  hello  '), 'hello'));
  test('trimLeft removes left whitespace', () => assertEqual(trimLeft('  hello  '), 'hello  '));
  test('trimRight removes right whitespace', () => assertEqual(trimRight('  hello  '), '  hello'));
  test('removeWhitespace removes all whitespace', () => assertEqual(removeWhitespace('h e l l o'), 'hello'));
  test('normalizeWhitespace collapses spaces', () => assertEqual(normalizeWhitespace('hello   world'), 'hello world'));

  // Case Conversion Tests
  test('toLowerCase converts to lowercase', () => assertEqual(toLowerCase('HELLO'), 'hello'));
  test('toUpperCase converts to uppercase', () => assertEqual(toUpperCase('hello'), 'HELLO'));
  test('capitalizes first character', () => assertEqual(capitalize('hello'), 'Hello'));
  test('uncapitalize lowercases first character', () => assertEqual(uncapitalize('Hello'), 'hello'));
  test('toTitleCase converts to title case', () => assertEqual(toTitleCase('hello world'), 'Hello World'));
  
  test('toCamelCase converts to camelCase', () => assertEqual(toCamelCase('hello_world'), 'helloWorld'));
  test('toPascalCase converts to PascalCase', () => assertEqual(toPascalCase('hello_world'), 'HelloWorld'));
  test('toSnakeCase converts to snake_case', () => assertEqual(toSnakeCase('HelloWorld'), 'hello_world'));
  test('toKebabCase converts to kebab-case', () => assertEqual(toKebabCase('HelloWorld'), 'hello-world'));

  // Substring Tests
  test('truncate with ellipsis', () => assertEqual(truncate('hello world', 8), 'hello...'));
  test('truncate when shorter', () => assertEqual(truncate('hi', 10), 'hi'));
  test('substringBetween extracts between markers', () => assertEqual(substringBetween('hello[world]test', '[', ']'), 'world'));
  test('substringAfter extracts after separator', () => assertEqual(substringAfter('hello/world', '/'), 'world'));
  test('substringBefore extracts before separator', () => assertEqual(substringBefore('hello/world', '/'), 'hello'));
  test('substringAfterLast extracts after last separator', () => assertEqual(substringAfterLast('/a/b/c', '/'), 'c'));
  test('substringBeforeLast extracts before last separator', () => assertEqual(substringBeforeLast('/a/b/c', '/'), '/a/b'));

  // Prefix/Suffix Tests
  test('startsWith checks prefix', () => assertTrue(startsWith('hello world', 'hello')));
  test('startsWith with ignoreCase', () => assertTrue(startsWith('Hello world', 'hello', true)));
  test('endsWith checks suffix', () => assertTrue(endsWith('hello world', 'world')));
  test('removePrefix removes prefix', () => assertEqual(removePrefix('prefix_text', 'prefix_'), 'text')));
  test('removeSuffix removes suffix', () => assertEqual(removeSuffix('text_suffix', '_suffix'), 'text'));

  // Validation Tests
  test('isValidEmail validates email', () => assertTrue(isValidEmail('test@example.com')));
  test('isValidEmail rejects invalid', () => assertFalse(isValidEmail('invalid')));
  test('isValidUrl validates URL', () => assertTrue(isValidUrl('https://example.com')));
  test('isNumeric validates number', () => assertTrue(isNumeric('123.45')));
  test('isInteger validates integer', () => assertTrue(isInteger('-42')));
  test('isAlpha validates letters', () => assertTrue(isAlpha('Hello')));
  test('isAlphanumeric validates alphanumeric', () => assertTrue(isAlphanumeric('Hello123')));

  // Padding Tests
  test('padLeft pads on left', () => assertEqual(padLeft('5', 3, '0'), '005'));
  test('padRight pads on right', () => assertEqual(padRight('5', 3, '0'), '500'));
  test('center centers string', () => assertEqual(center('hi', 4, ' '), ' hi '));

  // Search Tests
  test('contains finds substring', () => assertTrue(contains('hello world', 'world')));
  test('countMatches counts occurrences', () => assertEqual(countMatches('hello hello', 'hello'), 2));
  test('replaceAll replaces all', () => assertEqual(replaceAll('hello world', 'o', '0'), 'hell0 w0rld'));

  // Split/Join Tests
  test('split divides string', () => assertEqual(split('a,b,c', ',').length, 3));
  test('lines splits by newline', () => assertEqual(lines('a\nb').length, 2));
  test('join combines array', () => assertEqual(join(['a', 'b', 'c'], '-'), 'a-b-c'));

  // Encoding Tests
  test('base64Encode encodes', () => assertEqual(base64Encode('Hello'), 'SGVsbG8='));
  test('base64Decode decodes', () => assertEqual(base64Decode('SGVsbG8='), 'Hello'));
  test('urlEncode encodes URL', () => assertEqual(urlEncode('hello world'), 'hello%20world'));
  test('urlDecode decodes URL', () => assertEqual(urlDecode('hello%20world'), 'hello world'));

  // Random Tests (just check length and type)
  test('randomString generates correct length', () => assertEqual(randomString(10).length, 10));
  test('randomPassword generates password', () => assertTrue(randomPassword().length >= 4));

  // Utility Tests
  test('reverse reverses string', () => assertEqual(reverse('hello'), 'olleh'));
  test('repeat repeats string', () => assertEqual(repeat('ab', 3), 'ababab'));
  test('defaultIfBlank returns default', () => assertEqual(defaultIfBlank(null, 'default'), 'default'));
  test('equals compares strings', () => assertTrue(equals('hello', 'hello')));
  test('slugify creates slug', () => assertEqual(slugify('Hello World!'), 'hello
-world'));

  // Class API Tests
  test('StringUtils class API works', () => assertEqual(StringUtils.trim('  hello  '), 'hello'));

  // Summary
  console.log(`\n========================================`);
  console.log(`Test Results: ${passed} passed, ${failed} failed`);
  console.log(`========================================`);
}

// Run tests if executed directly
runTests();
