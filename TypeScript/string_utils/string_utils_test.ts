/**
 * String Utilities Test Suite
 * 
 * Comprehensive tests for all string utility functions.
 * Run with: deno test string_utils_test.ts
 * Or: bun test string_utils_test.ts
 * Or: node --test string_utils_test.ts (Node 20+)
 */

import {
  // Case conversion
  splitWords,
  toCamelCase,
  toPascalCase,
  toSnakeCase,
  toScreamingSnake,
  toKebabCase,
  toScreamingKebab,
  toDotCase,
  toSpaceCase,
  toTitleCase,
  toCase,
  
  // Trimming and padding
  trim,
  trimLeft,
  trimRight,
  trimChars,
  pad,
  padLeft,
  padRight,
  padBoth,
  zeroPad,
  
  // Truncation
  truncate,
  truncateWords,
  
  // Template interpolation
  interpolate,
  format,
  
  // Escaping
  escapeHtml,
  unescapeHtml,
  escapeJson,
  unescapeJson,
  escapeXml,
  escapeSql,
  escapeRegExp,
  
  // Pattern matching
  extractUrls,
  extractEmails,
  extractPhoneNumbers,
  extractHashtags,
  extractMentions,
  extractNumbers,
  extractBetween,
  
  // Character analysis
  analyzeChars,
  countOccurrences,
  isAlpha,
  isAlphanumeric,
  isNumeric,
  isInteger,
  isFloat,
  
  // String manipulation
  reverse,
  removeWhitespace,
  removeDigits,
  removeSpecialChars,
  replaceAll,
  insertAt,
  removeAt,
  repeat,
  
  // Splitting and joining
  split,
  chunk,
  joinGrammar,
  
  // Encoding
  toBase64,
  fromBase64,
  toBase64Url,
  fromBase64Url,
  encodeUrl,
  decodeUrl,
  
  // Comparison
  equals,
  startsWith,
  endsWith,
  contains,
  levenshtein,
  similarity,
  longestCommonSubstring,
  
  // Utilities
  randomString,
  slugify,
  isEmpty,
  isNotEmpty,
  capitalize,
  capitalizeWords,
  decapitalize,
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
  const condition = JSON.stringify(actual) === JSON.stringify(expected);
  if (!condition) {
    console.error(`    Expected: ${JSON.stringify(expected)}`);
    console.error(`    Got: ${JSON.stringify(actual)}`);
  }
  assert(condition, message);
}

function assertClose(actual: number, expected: number, tolerance: number, message: string): void {
  const condition = Math.abs(actual - expected) <= tolerance;
  if (!condition) {
    console.error(`    Expected: ${expected} (±${tolerance})`);
    console.error(`    Got: ${actual}`);
  }
  assert(condition, message);
}

// =============================================================================
// Case Conversion Tests
// =============================================================================

console.log('\n📝 Case Conversion Tests');
console.log('=' .repeat(50));

// splitWords
console.log('\n  splitWords:');
assertEquals(splitWords('helloWorld'), ['hello', 'World'], 'Split camelCase');
assertEquals(splitWords('hello_world'), ['hello', 'world'], 'Split snake_case');
assertEquals(splitWords('hello-world'), ['hello', 'world'], 'Split kebab-case');
assertEquals(splitWords('hello.world'), ['hello', 'world'], 'Split dot.case');
assertEquals(splitWords('Hello World'), ['Hello', 'World'], 'Split space separated');
assertEquals(splitWords('HTTPServer'), ['HTTP', 'Server'], 'Split consecutive caps');

// toCamelCase
console.log('\n  toCamelCase:');
assertEquals(toCamelCase('hello_world'), 'helloWorld', 'snake_case to camelCase');
assertEquals(toCamelCase('Hello-World'), 'helloWorld', 'kebab-case to camelCase');
assertEquals(toCamelCase('hello world'), 'helloWorld', 'space case to camelCase');
assertEquals(toCamelCase('HelloWorld'), 'helloWorld', 'PascalCase to camelCase');

// toPascalCase
console.log('\n  toPascalCase:');
assertEquals(toPascalCase('hello_world'), 'HelloWorld', 'snake_case to PascalCase');
assertEquals(toPascalCase('hello-world'), 'HelloWorld', 'kebab-case to PascalCase');
assertEquals(toPascalCase('helloWorld'), 'HelloWorld', 'camelCase to PascalCase');

// toSnakeCase
console.log('\n  toSnakeCase:');
assertEquals(toSnakeCase('helloWorld'), 'hello_world', 'camelCase to snake_case');
assertEquals(toSnakeCase('HelloWorld'), 'hello_world', 'PascalCase to snake_case');
assertEquals(toSnakeCase('hello-world'), 'hello_world', 'kebab-case to snake_case');

// toScreamingSnake
console.log('\n  toScreamingSnake:');
assertEquals(toScreamingSnake('helloWorld'), 'HELLO_WORLD', 'camelCase to SCREAMING_SNAKE');
assertEquals(toScreamingSnake('hello_world'), 'HELLO_WORLD', 'snake_case to SCREAMING_SNAKE');

// toKebabCase
console.log('\n  toKebabCase:');
assertEquals(toKebabCase('helloWorld'), 'hello-world', 'camelCase to kebab-case');
assertEquals(toKebabCase('hello_world'), 'hello-world', 'snake_case to kebab-case');
assertEquals(toKebabCase('HelloWorld'), 'hello-world', 'PascalCase to kebab-case');

// toScreamingKebab
console.log('\n  toScreamingKebab:');
assertEquals(toScreamingKebab('helloWorld'), 'HELLO-WORLD', 'camelCase to SCREAMING-KEBAB');

// toDotCase
console.log('\n  toDotCase:');
assertEquals(toDotCase('helloWorld'), 'hello.world', 'camelCase to dot.case');
assertEquals(toDotCase('hello_world'), 'hello.world', 'snake_case to dot.case');

// toSpaceCase
console.log('\n  toSpaceCase:');
assertEquals(toSpaceCase('helloWorld'), 'hello world', 'camelCase to space case');
assertEquals(toSpaceCase('hello_world'), 'hello world', 'snake_case to space case');

// toTitleCase
console.log('\n  toTitleCase:');
assertEquals(toTitleCase('hello world'), 'Hello World', 'lowercase to Title Case');
assertEquals(toTitleCase('HELLO WORLD'), 'Hello World', 'UPPERCASE to Title Case');

// toCase
console.log('\n  toCase:');
assertEquals(toCase('hello_world', 'camelCase'), 'helloWorld', 'toCase camelCase');
assertEquals(toCase('helloWorld', 'snake_case'), 'hello_world', 'toCase snake_case');
assertEquals(toCase('helloWorld', 'kebab-case'), 'hello-world', 'toCase kebab-case');

// =============================================================================
// Trimming and Padding Tests
// =============================================================================

console.log('\n✂️  Trimming and Padding Tests');
console.log('=' .repeat(50));

// trim
console.log('\n  trim:');
assertEquals(trim('  hello  '), 'hello', 'Trim both sides');
assertEquals(trim('\t\nhello\t\n'), 'hello', 'Trim whitespace chars');

// trimLeft
console.log('\n  trimLeft:');
assertEquals(trimLeft('  hello  '), 'hello  ', 'Trim left only');

// trimRight
console.log('\n  trimRight:');
assertEquals(trimRight('  hello  '), '  hello', 'Trim right only');

// trimChars
console.log('\n  trimChars:');
assertEquals(trimChars('###hello###', '#'), 'hello', 'Trim specific chars');
assertEquals(trimChars('---hello---', '-'), 'hello', 'Trim dashes');

// pad
console.log('\n  pad:');
assertEquals(pad('5', { length: 3, char: '0', position: 'left' }), '005', 'Pad left');
assertEquals(pad('5', { length: 3, char: '0', position: 'right' }), '500', 'Pad right');
assertEquals(pad('x', { length: 5, char: '*', position: 'both' }), '**x**', 'Pad both');
assertEquals(pad('hello', { length: 3 }), 'hello', 'No pad if already long enough');

// padLeft
console.log('\n  padLeft:');
assertEquals(padLeft('5', 3, '0'), '005', 'padLeft with zero');

// padRight
console.log('\n  padRight:');
assertEquals(padRight('5', 3, '0'), '500', 'padRight with zero');

// padBoth
console.log('\n  padBoth:');
assertEquals(padBoth('x', 5, '*'), '**x**', 'padBoth');
assertEquals(padBoth('x', 4, '*'), '*x**', 'padBoth even length');

// zeroPad
console.log('\n  zeroPad:');
assertEquals(zeroPad(5, 3), '005', 'zeroPad number');
assertEquals(zeroPad('42', 4), '0042', 'zeroPad string');
assertEquals(zeroPad(123, 2), '123', 'zeroPad no change if long enough');

// =============================================================================
// Truncation Tests
// =============================================================================

console.log('\n📏 Truncation Tests');
console.log('=' .repeat(50));

// truncate
console.log('\n  truncate:');
assertEquals(truncate('Hello World', { length: 8 }), 'Hello...', 'Basic truncate');
assertEquals(truncate('Hello', { length: 10 }), 'Hello', 'No truncate if short enough');
assertEquals(truncate('Hello World Test', { length: 12, suffix: ' [more]' }), 'Hello [more]', 'Custom suffix');
assertEquals(truncate('Hello World', { length: 8, preserveWords: true }), 'Hello...', 'Preserve words');
assertEquals(truncate('Hi', { length: 2, suffix: '...' }), 'Hi', 'No truncate if fits');

// truncateWords
console.log('\n  truncateWords:');
assertEquals(truncateWords('Hello world this is a test', 3), 'Hello world this...', 'Truncate by words');
assertEquals(truncateWords('Hello world', 5), 'Hello world', 'No truncate if few words');
assertEquals(truncateWords('Hello world', 1, ' [cont]'), 'Hello [cont]', 'Custom suffix');

// =============================================================================
// Template Interpolation Tests
// =============================================================================

console.log('\n📝 Template Interpolation Tests');
console.log('=' .repeat(50));

// interpolate
console.log('\n  interpolate:');
assertEquals(interpolate('Hello, {{name}}!', { name: 'World' }), 'Hello, World!', 'Basic interpolation');
assertEquals(interpolate('{{greeting}}, {{name}}!', { greeting: 'Hi', name: 'Alice' }), 'Hi, Alice!', 'Multiple variables');
assertEquals(interpolate('Hello, {{missing}}!', {}), 'Hello, !', 'Missing variable');
assertEquals(interpolate('Hello, {name}!', { name: 'World' }, { prefix: '{', suffix: '}' }), 'Hello, World!', 'Custom delimiters');

// format
console.log('\n  format:');
assertEquals(format('Hello {0}', 'World'), 'Hello World', 'Single argument');
assertEquals(format('{0} is {1} years old', 'Alice', 25), 'Alice is 25 years old', 'Multiple arguments');
assertEquals(format('No placeholders'), 'No placeholders', 'No placeholders');
assertEquals(format('Missing {5}', 'a', 'b'), 'Missing ', 'Missing argument');

// =============================================================================
// Escaping Tests
// =============================================================================

console.log('\n🔒 Escaping Tests');
console.log('=' .repeat(50));

// escapeHtml
console.log('\n  escapeHtml:');
assertEquals(escapeHtml('<script>alert("XSS")</script>'), '&lt;script&gt;alert(&quot;XSS&quot;)&lt;&#x2F;script&gt;', 'Escape HTML tags');
assertEquals(escapeHtml('Tom & Jerry'), 'Tom &amp; Jerry', 'Escape ampersand');
assertEquals(escapeHtml('Safe text'), 'Safe text', 'No escaping needed');

// unescapeHtml
console.log('\n  unescapeHtml:');
assertEquals(unescapeHtml('&lt;div&gt;'), '<div>', 'Unescape HTML tags');
assertEquals(unescapeHtml('Tom &amp; Jerry'), 'Tom & Jerry', 'Unescape ampersand');

// escapeJson
console.log('\n  escapeJson:');
assertEquals(escapeJson('Hello\nWorld'), 'Hello\\nWorld', 'Escape newline');
assertEquals(escapeJson('Say "Hi"'), 'Say \\"Hi\\"', 'Escape quotes');
assertEquals(escapeJson('Tab\there'), 'Tab\\there', 'Escape tab');

// unescapeJson
console.log('\n  unescapeJson:');
assertEquals(unescapeJson('Hello\\nWorld'), 'Hello\nWorld', 'Unescape newline');
assertEquals(unescapeJson('Say \\"Hi\\"'), 'Say "Hi"', 'Unescape quotes');

// escapeXml
console.log('\n  escapeXml:');
assertEquals(escapeXml('<tag>content</tag>'), '&lt;tag&gt;content&lt;/tag&gt;', 'Escape XML tags');
assertEquals(escapeXml("Tom & Jerry's"), 'Tom &amp; Jerry&apos;s', 'Escape XML special chars');

// escapeSql
console.log('\n  escapeSql:');
assertEquals(escapeSql("O'Reilly"), "O''Reilly", 'Escape SQL quote');
assertEquals(escapeSql("SELECT * FROM users WHERE name='test'"), "SELECT * FROM users WHERE name=''test''", 'Escape SQL in query');

// escapeRegExp
console.log('\n  escapeRegExp:');
assertEquals(escapeRegExp('hello.world'), 'hello\\.world', 'Escape dot');
assertEquals(escapeRegExp('a+b*c?'), 'a\\+b\\*c\\?', 'Escape special chars');
assertEquals(escapeRegExp('[abc]'), '\\[abc\\]', 'Escape brackets');

// =============================================================================
// Pattern Matching Tests
// =============================================================================

console.log('\n🔍 Pattern Matching Tests');
console.log('=' .repeat(50));

// extractUrls
console.log('\n  extractUrls:');
assertEquals(extractUrls('Visit https://example.com and http://test.org'), ['https://example.com', 'http://test.org'], 'Extract URLs');
assertEquals(extractUrls('No URLs here'), [], 'No URLs');

// extractEmails
console.log('\n  extractEmails:');
assertEquals(extractEmails('Contact: test@example.com or support@test.org'), ['test@example.com', 'support@test.org'], 'Extract emails');
assertEquals(extractEmails('No emails'), [], 'No emails');

// extractPhoneNumbers
console.log('\n  extractPhoneNumbers:');
assertEquals(extractPhoneNumbers('Call 123-456-7890 or (555) 123-4567'), ['123-456-7890', '(555) 123-4567'], 'Extract phone numbers');

// extractHashtags
console.log('\n  extractHashtags:');
assertEquals(extractHashtags('Love #typescript and #coding!'), ['typescript', 'coding'], 'Extract hashtags');
assertEquals(extractHashtags('No hashtags'), [], 'No hashtags');

// extractMentions
console.log('\n  extractMentions:');
assertEquals(extractMentions('Hey @alice and @bob!'), ['alice', 'bob'], 'Extract mentions');
assertEquals(extractMentions('No mentions'), [], 'No mentions');

// extractNumbers
console.log('\n  extractNumbers:');
assertEquals(extractNumbers('I have 3 apples and 5 oranges'), [3, 5], 'Extract integers');
assertEquals(extractNumbers('Price: 19.99 and 29.50', true), [19.99, 29.5], 'Extract floats');
assertEquals(extractNumbers('No numbers'), [], 'No numbers');

// extractBetween
console.log('\n  extractBetween:');
assertEquals(extractBetween('Hello [World] and [Universe]', '[', ']'), ['World', 'Universe'], 'Extract between delimiters');
assertEquals(extractBetween('<tag>content</tag>', '<tag>', '</tag>'), ['content'], 'Extract between HTML tags');
assertEquals(extractBetween('Hello [World]', '[', ']', true), ['[World]'], 'Include delimiters');

// =============================================================================
// Character Analysis Tests
// =============================================================================

console.log('\n📊 Character Analysis Tests');
console.log('=' .repeat(50));

// analyzeChars
console.log('\n  analyzeChars:');
const analysis = analyzeChars('Hello 123!');
assertEquals(analysis.total, 10, 'Total characters');
assertEquals(analysis.letters, 5, 'Letter count');
assertEquals(analysis.digits, 3, 'Digit count');
assertEquals(analysis.spaces, 1, 'Space count');
assertEquals(analysis.punctuation, 1, 'Punctuation count');

// countOccurrences
console.log('\n  countOccurrences:');
assertEquals(countOccurrences('hello hello hello', 'hello'), 3, 'Count occurrences');
assertEquals(countOccurrences('Hello HELLO hello', 'hello', false), 3, 'Case insensitive count');
assertEquals(countOccurrences('aaa', 'aa'), 1, 'Non-overlapping count');

// isAlpha
console.log('\n  isAlpha:');
assertEquals(isAlpha('Hello'), true, 'All letters');
assertEquals(isAlpha('Hello123'), false, 'Letters and digits');
assertEquals(isAlpha(''), false, 'Empty string');

// isAlphanumeric
console.log('\n  isAlphanumeric:');
assertEquals(isAlphanumeric('Hello123'), true, 'All alphanumeric');
assertEquals(isAlphanumeric('Hello 123'), false, 'With space');
assertEquals(isAlphanumeric('Hello!'), false, 'With special char');

// isNumeric
console.log('\n  isNumeric:');
assertEquals(isNumeric('123'), true, 'All digits');
assertEquals(isNumeric('12.3'), false, 'With decimal');
assertEquals(isNumeric('123abc'), false, 'With letters');

// isInteger
console.log('\n  isInteger:');
assertEquals(isInteger('123'), true, 'Positive integer');
assertEquals(isInteger('-123'), true, 'Negative integer');
assertEquals(isInteger('12.3'), false, 'Float');
assertEquals(isInteger('abc'), false, 'Not a number');

// isFloat
console.log('\n  isFloat:');
assertEquals(isFloat('12.34'), true, 'Float');
assertEquals(isInteger('123'), true, 'Integer is also float-compatible');
assertEquals(isFloat('-12.34'), true, 'Negative float');
assertEquals(isFloat('abc'), false, 'Not a number');

// =============================================================================
// String Manipulation Tests
// =============================================================================

console.log('\n🔧 String Manipulation Tests');
console.log('=' .repeat(50));

// reverse
console.log('\n  reverse:');
assertEquals(reverse('hello'), 'olleh', 'Reverse ASCII');
assertEquals(reverse('你好'), '好你', 'Reverse Unicode');
assertEquals(reverse(''), '', 'Reverse empty');

// removeWhitespace
console.log('\n  removeWhitespace:');
assertEquals(removeWhitespace('hello world'), 'helloworld', 'Remove spaces');
assertEquals(removeWhitespace('a\nb\tc'), 'abc', 'Remove all whitespace');

// removeDigits
console.log('\n  removeDigits:');
assertEquals(removeDigits('abc123def'), 'abcdef', 'Remove digits');
assertEquals(removeDigits('no digits'), 'no digits', 'No digits to remove');

// removeSpecialChars
console.log('\n  removeSpecialChars:');
assertEquals(removeSpecialChars('Hello! World@123'), 'HelloWorld123', 'Remove special chars');
assertEquals(removeSpecialChars('abc123'), 'abc123', 'No special chars');

// replaceAll
console.log('\n  replaceAll:');
assertEquals(replaceAll('hello hello', 'hello', 'hi'), 'hi hi', 'Replace all');
assertEquals(replaceAll('Hello HELLO', 'hello', 'hi', false), 'hi hi', 'Case insensitive replace');

// insertAt
console.log('\n  insertAt:');
assertEquals(insertAt('Helo', 'l', 2), 'Hello', 'Insert in middle');
assertEquals(insertAt('abc', 'X', 0), 'Xabc', 'Insert at start');
assertEquals(insertAt('abc', 'X', 3), 'abcX', 'Insert at end');

// removeAt
console.log('\n  removeAt:');
assertEquals(removeAt('Hello', 1, 1), 'Hllo', 'Remove one char');
assertEquals(removeAt('Hello', 1, 2), 'Hlo', 'Remove multiple chars');
assertEquals(removeAt('Hello', 0), 'ello', 'Remove from start');

// repeat
console.log('\n  repeat:');
assertEquals(repeat('ab', 3), 'ababab', 'Repeat string');
assertEquals(repeat('ab', 3, '-'), 'ab-ab-ab', 'Repeat with separator');
assertEquals(repeat('x', 0), '', 'Repeat zero times');

// =============================================================================
// Splitting and Joining Tests
// =============================================================================

console.log('\n🔗 Splitting and Joining Tests');
console.log('=' .repeat(50));

// split
console.log('\n  split:');
assertEquals(split('a,b,c', { separator: ',' }), ['a', 'b', 'c'], 'Basic split');
assertEquals(split('a, b, c', { separator: ',', trim: true }), ['a', 'b', 'c'], 'Split with trim');
assertEquals(split('a,,b,,c', { separator: ',', removeEmpty: true }), ['a', 'b', 'c'], 'Remove empty');

// chunk
console.log('\n  chunk:');
assertEquals(chunk('abcdefgh', 3), ['abc', 'def', 'gh'], 'Chunk string');
assertEquals(chunk('abc', 5), ['abc'], 'Chunk larger than string');
assertEquals(chunk('', 3), [], 'Chunk empty string');

// joinGrammar
console.log('\n  joinGrammar:');
assertEquals(joinGrammar(['apple']), 'apple', 'Single item');
assertEquals(joinGrammar(['apple', 'banana']), 'apple and banana', 'Two items');
assertEquals(joinGrammar(['apple', 'banana', 'cherry']), 'apple, banana, and cherry', 'Three items with Oxford comma');
assertEquals(joinGrammar(['apple', 'banana', 'cherry'], { oxfordComma: false }), 'apple, banana and cherry', 'Without Oxford comma');
assertEquals(joinGrammar(['apple', 'banana', 'cherry'], { conjunction: 'or' }), 'apple, banana, or cherry', 'Custom conjunction');

// =============================================================================
// Encoding Tests
// =============================================================================

console.log('\n🔐 Encoding Tests');
console.log('=' .repeat(50));

// toBase64 / fromBase64
console.log('\n  toBase64 / fromBase64:');
const base64Hello = toBase64('Hello, World!');
assertEquals(fromBase64(base64Hello), 'Hello, World!', 'Base64 round-trip');
assertEquals(base64Hello, 'SGVsbG8sIFdvcmxkIQ==', 'Known Base64 value');

// toBase64Url / fromBase64Url
console.log('\n  toBase64Url / fromBase64Url:');
const base64Url = toBase64Url('Hello+World/Test');
assertEquals(fromBase64Url(base64Url), 'Hello+World/Test', 'Base64URL round-trip');
assert(!base64Url.includes('+') && !base64Url.includes('/'), 'Base64URL has no + or /');

// encodeUrl / decodeUrl
console.log('\n  encodeUrl / decodeUrl:');
const encoded = encodeUrl('Hello World!');
assertEquals(decodeUrl(encoded), 'Hello World!', 'URL encode round-trip');
assertEquals(encoded, 'Hello%20World!', 'Known URL encoded value');

// =============================================================================
// Comparison Tests
// =============================================================================

console.log('\n⚖️  Comparison Tests');
console.log('=' .repeat(50));

// equals
console.log('\n  equals:');
assertEquals(equals('Hello', 'Hello'), true, 'Equal strings');
assertEquals(equals('Hello', 'hello'), true, 'Case insensitive equal');
assertEquals(equals('Hello', 'hello', true), false, 'Case sensitive not equal');
assertEquals(equals('abc', 'def'), false, 'Different strings');

// startsWith
console.log('\n  startsWith:');
assertEquals(startsWith('Hello World', 'Hello'), true, 'Starts with');
assertEquals(startsWith('Hello World', 'hello', false), true, 'Case insensitive starts with');
assertEquals(startsWith('Hello World', 'World'), false, 'Does not start with');

// endsWith
console.log('\n  endsWith:');
assertEquals(endsWith('Hello World', 'World'), true, 'Ends with');
assertEquals(endsWith('Hello World', 'world', false), true, 'Case insensitive ends with');
assertEquals(endsWith('Hello World', 'Hello'), false, 'Does not end with');

// contains
console.log('\n  contains:');
assertEquals(contains('Hello World', 'lo Wo'), true, 'Contains substring');
assertEquals(contains('Hello World', 'hello', false), true, 'Case insensitive contains');
assertEquals(contains('Hello World', 'xyz'), false, 'Does not contain');

// levenshtein
console.log('\n  levenshtein:');
assertEquals(levenshtein('kitten', 'sitting'), 3, 'Levenshtein distance');
assertEquals(levenshtein('abc', 'abc'), 0, 'Same string');
assertEquals(levenshtein('', 'abc'), 3, 'Empty to string');
assertEquals(levenshtein('abc', ''), 3, 'String to empty');

// similarity
console.log('\n  similarity:');
assertClose(similarity('abc', 'abc'), 1, 0.01, 'Same string similarity');
assertClose(similarity('abc', 'def'), 0, 0.01, 'Different string similarity');
assertClose(similarity('kitten', 'sitting'), 0.57, 0.01, 'Partial similarity');

// longestCommonSubstring
console.log('\n  longestCommonSubstring:');
assertEquals(longestCommonSubstring('abcdef', 'zcdgh'), 'cd', 'Common substring');
assertEquals(longestCommonSubstring('abc', 'xyz'), '', 'No common substring');
assertEquals(longestCommonSubstring('hello', 'hello'), 'hello', 'Same string');

// =============================================================================
// Utility Tests
// =============================================================================

console.log('\n🛠️  Utility Tests');
console.log('=' .repeat(50));

// randomString
console.log('\n  randomString:');
const random10 = randomString(10);
assertEquals(random10.length, 10, 'Random string length');
const random10Digits = randomString(10, '0123456789');
assertEquals(random10Digits.length, 10, 'Random digits length');
assert(/^\d+$/.test(random10Digits), 'Random string contains only digits');

// slugify
console.log('\n  slugify:');
assertEquals(slugify('Hello World!'), 'hello-world', 'Basic slugify');
assertEquals(slugify('Café & Restaurant'), 'cafe-restaurant', 'Slugify with accents');
assertEquals(slugify('Hello_World', { separator: '_' }), 'hello_world', 'Custom separator');
assertEquals(slugify('Hello   World'), 'hello-world', 'Multiple spaces');

// isEmpty
console.log('\n  isEmpty:');
assertEquals(isEmpty(''), true, 'Empty string');
assertEquals(isEmpty('   '), true, 'Whitespace only');
assertEquals(isEmpty('hello'), false, 'Non-empty string');
assertEquals(isEmpty(null as any), true, 'Null');
assertEquals(isEmpty(undefined as any), true, 'Undefined');

// isNotEmpty
console.log('\n  isNotEmpty:');
assertEquals(isNotEmpty('hello'), true, 'Non-empty string');
assertEquals(isNotEmpty(''), false, 'Empty string');

// capitalize
console.log('\n  capitalize:');
assertEquals(capitalize('hello'), 'Hello', 'Capitalize first letter');
assertEquals(capitalize('HELLO'), 'HELLO', 'Already capitalized');
assertEquals(capitalize(''), '', 'Empty string');

// capitalizeWords
console.log('\n  capitalizeWords:');
assertEquals(capitalizeWords('hello world'), 'Hello World', 'Capitalize all words');
assertEquals(capitalizeWords('HELLO WORLD'), 'HELLO WORLD', 'Already capitalized');

// decapitalize
console.log('\n  decapitalize:');
assertEquals(decapitalize('Hello'), 'hello', 'Decapitalize first letter');
assertEquals(decapitalize('hello'), 'hello', 'Already decapitalized');

// =============================================================================
// Summary
// =============================================================================

console.log('\n' + '='.repeat(50));
console.log(`\n📊 Test Results: ${passed} passed, ${failed} failed\n`);

if (failed > 0) {
  console.error('❌ Some tests failed!');
  // In a real test runner, this would exit with error code
} else {
  console.log('✅ All tests passed!');
}
