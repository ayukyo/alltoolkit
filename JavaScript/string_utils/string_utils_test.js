/**
 * String Utils Test Suite
 * 
 * Run with: node string_utils_test.js
 */

const StringUtils = require('./mod.js');

let passed = 0;
let failed = 0;

function test(name, fn) {
    try {
        fn();
        console.log('✓ ' + name);
        passed++;
    } catch (e) {
        console.log('✗ ' + name + ': ' + e.message);
        failed++;
    }
}

function assertEqual(actual, expected, msg) {
    if (actual !== expected) {
        throw new Error((msg || 'Assertion failed') + ': expected ' + JSON.stringify(expected) + ', got ' + JSON.stringify(actual));
    }
}

function assertTrue(value, msg) {
    if (value !== true) {
        throw new Error(msg || 'Expected true');
    }
}

function assertFalse(value, msg) {
    if (value !== false) {
        throw new Error(msg || 'Expected false');
    }
}

console.log('Running StringUtils Tests...\n');

// Empty/Blank Checks
test('isBlank with empty string', () => assertTrue(StringUtils.isBlank('')));
test('isBlank with whitespace', () => assertTrue(StringUtils.isBlank('   ')));
test('isBlank with null', () => assertTrue(StringUtils.isBlank(null)));
test('isBlank with undefined', () => assertTrue(StringUtils.isBlank(undefined)));
test('isBlank with content', () => assertFalse(StringUtils.isBlank('hello')));

test('isNotBlank with content', () => assertTrue(StringUtils.isNotBlank('hello')));
test('isNotBlank with empty', () => assertFalse(StringUtils.isNotBlank('')));

test('isEmpty with empty string', () => assertTrue(StringUtils.isEmpty('')));
test('isEmpty with whitespace', () => assertFalse(StringUtils.isEmpty('  ')));

// Trimming
test('trim removes whitespace', () => assertEqual(StringUtils.trim('  hello  '), 'hello'));
test('trimLeft removes leading whitespace', () => assertEqual(StringUtils.trimLeft('  hello  '), 'hello  '));
test('trimRight removes trailing whitespace', () => assertEqual(StringUtils.trimRight('  hello  '), '  hello'));
test('removeWhitespace removes all whitespace', () => assertEqual(StringUtils.removeWhitespace('h e l l o'), 'hello'));
test('normalizeWhitespace normalizes spaces', () => assertEqual(StringUtils.normalizeWhitespace('hello   world'), 'hello world'));

// Case Conversion
test('toLowerCase converts to lowercase', () => assertEqual(StringUtils.toLowerCase('HELLO'), 'hello'));
test('toUpperCase converts to uppercase', () => assertEqual(StringUtils.toUpperCase('hello'), 'HELLO'));
test('capitalize capitalizes first letter', () => assertEqual(StringUtils.capitalize('hello'), 'Hello'));
test('uncapitalize uncapitalizes first letter', () => assertEqual(StringUtils.uncapitalize('Hello'), 'hello'));
test('toTitleCase converts to title case', () => assertEqual(StringUtils.toTitleCase('hello world'), 'Hello World'));
test('swapCase swaps case', () => assertEqual(StringUtils.swapCase('Hello'), 'hELLO'));

// Substring Operations
test('truncate truncates string', () => assertEqual(StringUtils.truncate('hello world', 8), 'hello...'));
test('truncate with custom suffix', () => assertEqual(StringUtils.truncate('hello world', 8, '>>'), 'hello >>'));
test('truncate returns original if shorter than maxLength', () => assertEqual(StringUtils.truncate('hi', 10), 'hi'));
test('truncate handles empty string', () => assertEqual(StringUtils.truncate('', 10), ''));
test('truncate handles null', () => assertEqual(StringUtils.truncate(null, 10), ''));
test('truncate handles undefined', () => assertEqual(StringUtils.truncate(undefined, 10), ''));
test('truncate handles exact length', () => assertEqual(StringUtils.truncate('hello', 5), 'hello'));
test('truncate with long suffix', () => assertEqual(StringUtils.truncate('hello', 4, '...'), 'h...'));
test('substringBetween extracts between markers', () => assertEqual(StringUtils.substringBetween('hello [world] there', '[', ']'), 'world'));
test('substringAfter extracts after separator', () => assertEqual(StringUtils.substringAfter('hello-world', '-'), 'world'));
test('substringBefore extracts before separator', () => assertEqual(StringUtils.substringBefore('hello-world', '-'), 'hello'));
test('substringAfterLast extracts after last separator', () => assertEqual(StringUtils.substringAfterLast('a-b-c', '-'), 'c'));
test('substringBeforeLast extracts before last separator', () => assertEqual(StringUtils.substringBeforeLast('a-b-c', '-'), 'a-b'));

// Prefix/Suffix Operations
test('startsWith checks prefix', () => assertTrue(StringUtils.startsWith('hello world', 'hello')));
test('startsWith with ignoreCase', () => assertTrue(StringUtils.startsWith('Hello world', 'hello', true)));
test('endsWith checks suffix', () => assertTrue(StringUtils.endsWith('hello world', 'world')));
test('endsWith with ignoreCase', () => assertTrue(StringUtils.endsWith('hello World', 'world', true)));
test('removePrefix removes prefix', () => assertEqual(StringUtils.removePrefix('hello world', 'hello '), 'world'));
test('removeSuffix removes suffix', () => assertEqual(StringUtils.removeSuffix('hello world', ' world'), 'hello'));

// Counting and Searching
test('countMatches counts occurrences', () => assertEqual(StringUtils.countMatches('hello hello', 'hello'), 2));
test('contains finds substring', () => assertTrue(StringUtils.contains('hello world', 'world')));
test('contains with ignoreCase', () => assertTrue(StringUtils.contains('Hello World', 'world', true)));
test('indexOf finds index', () => assertEqual(StringUtils.indexOf('hello world', 'world'), 6));
test('lastIndexOf finds last index', () => assertEqual(StringUtils.lastIndexOf('hello hello', 'hello'), 6));

// Replacement
test('replaceAll replaces all occurrences', () => assertEqual(StringUtils.replaceAll('hello hello', 'hello', 'hi'), 'hi hi'));
test('replaceFirst replaces first occurrence', () => assertEqual(StringUtils.replaceFirst('hello hello', 'hello', 'hi'), 'hi hello'));
test('replaceLast replaces last occurrence', () => assertEqual(StringUtils.replaceLast('hello hello', 'hello', 'hi'), 'hello hi'));

// Padding
test('padLeft pads on left', () => assertEqual(StringUtils.padLeft('5', 3, '0'), '005'));
test('padRight pads on right', () => assertEqual(StringUtils.padRight('5', 3, '0'), '500'));
test('center centers string', () => assertEqual(StringUtils.center('hi', 6, '-'), '--hi--'));

// Reversal and Repetition
test('reverse reverses string', () => assertEqual(StringUtils.reverse('hello'), 'olleh'));
test('repeat repeats string', () => assertEqual(StringUtils.repeat('ab', 3), 'ababab'));

// Splitting and Joining
test('split splits string', () => {
    const result = StringUtils.split('a,b,c', ',');
    assertEqual(result.length, 3);
    assertEqual(result[0], 'a');
});
test('lines splits by newlines', () => {
    const result = StringUtils.lines('line1\nline2\nline3');
    assertEqual(result.length, 3);
});
test('join joins array', () => assertEqual(StringUtils.join(['a', 'b', 'c'], '-'), 'a-b-c'));

// Validation
test('isValidEmail validates email', () => assertTrue(StringUtils.isValidEmail('test@example.com')));
test('isValidEmail rejects invalid email', () => assertFalse(StringUtils.isValidEmail('invalid')));
test('isValidUrl validates URL', () => assertTrue(StringUtils.isValidUrl('https://example.com')));
test('isValidIPv4 validates IPv4', () => assertTrue(StringUtils.isValidIPv4('192.168.1.1')));
test('isNumeric validates numeric', () => assertTrue(StringUtils.isNumeric('123.45')));
test('isInteger validates integer', () => assertTrue(StringUtils.isInteger('123')));
test('isAlpha validates alphabetic', () => assertTrue(StringUtils.isAlpha('abc')));
test('isAlphanumeric validates alphanumeric', () => assertTrue(StringUtils.isAlphanumeric('abc123')));

// Naming Conventions
test('toCamelCase converts to camelCase', () => assertEqual(StringUtils.toCamelCase('hello-world'), 'helloWorld'));
test('toPascalCase converts to PascalCase', () => assertEqual(StringUtils.toPascalCase('hello-world'), 'HelloWorld'));
test('toSnakeCase converts to snake_case', () => assertEqual(StringUtils.toSnakeCase('helloWorld'), 'hello_world'));
test('toKebabCase converts to kebab-case', () => assertEqual(StringUtils.toKebabCase('helloWorld'), 'hello-world'));

// Random Generation
test('random generates string of correct length', () => {
    const result = StringUtils.random(10);
    assertEqual(result.length, 10);
});
test('randomAlphanumeric generates alphanumeric', () => assertTrue(StringUtils.isAlphanumeric(StringUtils.randomAlphanumeric(10))));
test('randomNumeric generates numeric', () => assertTrue(StringUtils.isNumeric(StringUtils.randomNumeric(10))));
test('randomPassword generates password of correct length', () => assertEqual(StringUtils.randomPassword(16).length, 16));
test('randomPassword generates password with minimum length', () => {
    const result = StringUtils.randomPassword(2); // Should use minimum 4
    assertEqual(result.length, 4);
});
test('randomPassword generates password with maximum length cap', () => {
    const result = StringUtils.randomPassword(2000); // Should cap at 1024
    assertEqual(result.length, 1024);
});
test('randomPassword contains all required character types', () => {
    const password = StringUtils.randomPassword(16);
    const hasLower = /[a-z]/.test(password);
    const hasUpper = /[A-Z]/.test(password);
    const hasDigit = /[0-9]/.test(password);
    const hasSpecial = /[!@#$%^&*()\-_=+\[\]{}|;:,.<>?]/.test(password);
    assertTrue(hasLower, 'Password should contain lowercase letter');
    assertTrue(hasUpper, 'Password should contain uppercase letter');
    assertTrue(hasDigit, 'Password should contain digit');
    assertTrue(hasSpecial, 'Password should contain special character');
});
test('randomPassword handles invalid length input', () => {
    const result1 = StringUtils.randomPassword('invalid');
    assertEqual(result1.length, 16); // Should use default
    const result2 = StringUtils.randomPassword(null);
    assertEqual(result2.length, 16); // Should use default
    const result3 = StringUtils.randomPassword(undefined);
    assertEqual(result3.length, 16); // Should use default
});
test('randomPassword generates different passwords each time', () => {
    const p1 = StringUtils.randomPassword(16);
    const p2 = StringUtils.randomPassword(16);
    const p3 = StringUtils.randomPassword(16);
    // Very unlikely to get same password 3 times
    assertTrue(p1 !== p2 || p2 !== p3, 'Passwords should be random');
});

// URL Encoding
test('urlEncode encodes URL', () => assertEqual(StringUtils.urlEncode('hello world'), 'hello%20world'));
test('urlDecode decodes URL', () => assertEqual(StringUtils.urlDecode('hello%20world'), 'hello world'));

// Slug Generation
test('slugify creates slug', () => assertEqual(StringUtils.slugify('Hello World!'), 'hello-world'));

// HTML Operations
test('stripHtml removes HTML tags', () => assertEqual(StringUtils.stripHtml('<p>hello</p>'), 'hello'));
test('escapeHtml escapes HTML', () => assertEqual(StringUtils.escapeHtml('<script>'), '&lt;script&gt;'));
test('unescapeHtml unescapes HTML', () => assertEqual(StringUtils.unescapeHtml('&lt;script&gt;'), '<script>'));

// Comparison
test('equals compares strings', () => assertTrue(StringUtils.equals('hello', 'hello')));
test('equals with ignoreCase', () => assertTrue(StringUtils.equals('Hello', 'hello', true)));
test('compare returns correct order', () => assertEqual(StringUtils.compare('a', 'b'), -1));

// Default Values
test('defaultString returns default for blank', () => assertEqual(StringUtils.defaultString('', 'default'), 'default'));
test('defaultString returns string if not blank', () => assertEqual(StringUtils.defaultString('hello', 'default'), 'hello'));
test('defaultIfEmpty returns default for empty', () => assertEqual(StringUtils.defaultIfEmpty('', 'default'), 'default'));
test('defaultIfEmpty returns string with whitespace', () => assertEqual(StringUtils.defaultIfEmpty('  ', 'default'), '  '));

// Null/Undefined Safety
test('handles null input gracefully', () => assertEqual(StringUtils.trim(null), ''));
test('handles undefined input gracefully', () => assertEqual(StringUtils.trim(undefined), ''));
test('isBlank handles null', () => assertTrue(StringUtils.isBlank(null)));
test('isBlank handles undefined', () => assertTrue(StringUtils.isBlank(undefined)));

console.log('\n========================================');
console.log('Test Results: ' + passed + ' passed, ' + failed + ' failed');
console.log('========================================');

process.exit(failed > 0 ? 1 : 0);