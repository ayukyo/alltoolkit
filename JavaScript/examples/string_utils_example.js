/**
 * String Utils Example
 * 
 * Demonstrates usage of the StringUtils module.
 * 
 * Run with: node string_utils_example.js
 */

const StringUtils = require('../string_utils/mod.js');

console.log('========================================');
console.log('StringUtils Examples');
console.log('========================================\n');

// Empty/Blank Checks
console.log('--- Empty/Blank Checks ---');
console.log('isBlank("hello"):', StringUtils.isBlank('hello'));
console.log('isBlank("  "):', StringUtils.isBlank('  '));
console.log('isBlank(null):', StringUtils.isBlank(null));
console.log('isNotBlank("hello"):', StringUtils.isNotBlank('hello'));
console.log();

// Trimming and Whitespace
console.log('--- Trimming and Whitespace ---');
console.log('trim("  hello  "):', StringUtils.trim('  hello  '));
console.log('trimLeft("  hello  "):', StringUtils.trimLeft('  hello  '));
console.log('trimRight("  hello  "):', StringUtils.trimRight('  hello  '));
console.log('removeWhitespace("h e l l o"):', StringUtils.removeWhitespace('h e l l o'));
console.log('normalizeWhitespace("hello   world"):', StringUtils.normalizeWhitespace('hello   world'));
console.log();

// Case Conversion
console.log('--- Case Conversion ---');
console.log('toLowerCase("HELLO"):', StringUtils.toLowerCase('HELLO'));
console.log('toUpperCase("hello"):', StringUtils.toUpperCase('hello'));
console.log('capitalize("hello"):', StringUtils.capitalize('hello'));
console.log('uncapitalize("Hello"):', StringUtils.uncapitalize('Hello'));
console.log('toTitleCase("hello world"):', StringUtils.toTitleCase('hello world'));
console.log('swapCase("Hello"):', StringUtils.swapCase('Hello'));
console.log();

// Substring Operations
console.log('--- Substring Operations ---');
console.log('truncate("hello world", 8):', StringUtils.truncate('hello world', 8));
console.log('truncate("hello world", 8, " >>"):', StringUtils.truncate('hello world', 8, ' >>'));
console.log('substringBetween("hello [world] there", "[", "]"):', StringUtils.substringBetween('hello [world] there', '[', ']'));
console.log('substringAfter("hello-world", "-"):', StringUtils.substringAfter('hello-world', '-'));
console.log('substringBefore("hello-world", "-"):', StringUtils.substringBefore('hello-world', '-'));
console.log('substringAfterLast("a-b-c", "-"):', StringUtils.substringAfterLast('a-b-c', '-'));
console.log('substringBeforeLast("a-b-c", "-"):', StringUtils.substringBeforeLast('a-b-c', '-'));
console.log();

// Prefix/Suffix Operations
console.log('--- Prefix/Suffix Operations ---');
console.log('startsWith("hello world", "hello"):', StringUtils.startsWith('hello world', 'hello'));
console.log('startsWith("Hello world", "hello", true):', StringUtils.startsWith('Hello world', 'hello', true));
console.log('endsWith("hello world", "world"):', StringUtils.endsWith('hello world', 'world'));
console.log('removePrefix("hello world", "hello "):', StringUtils.removePrefix('hello world', 'hello '));
console.log('removeSuffix("hello world", " world"):', StringUtils.removeSuffix('hello world', ' world'));
console.log();

// Counting and Searching
console.log('--- Counting and Searching ---');
console.log('countMatches("hello hello", "hello"):', StringUtils.countMatches('hello hello', 'hello'));
console.log('contains("hello world", "world"):', StringUtils.contains('hello world', 'world'));
console.log('contains("Hello World", "world", true):', StringUtils.contains('Hello World', 'world', true));
console.log('indexOf("hello world", "world"):', StringUtils.indexOf('hello world', 'world'));
console.log('lastIndexOf("hello hello", "hello"):', StringUtils.lastIndexOf('hello hello', 'hello'));
console.log();

// Replacement
console.log('--- Replacement ---');
console.log('replaceAll("hello hello", "hello", "hi"):', StringUtils.replaceAll('hello hello', 'hello', 'hi'));
console.log('replaceFirst("hello hello", "hello", "hi"):', StringUtils.replaceFirst('hello hello', 'hello', 'hi'));
console.log('replaceLast("hello hello", "hello", "hi"):', StringUtils.replaceLast('hello hello', 'hello', 'hi'));
console.log();

// Padding
console.log('--- Padding ---');
console.log('padLeft("5", 3, "0"):', StringUtils.padLeft('5', 3, '0'));
console.log('padRight("5", 3, "0"):', StringUtils.padRight('5', 3, '0'));
console.log('center("hi", 6, "-"):', StringUtils.center('hi', 6, '-'));
console.log();

// Reversal and Repetition
console.log('--- Reversal and Repetition ---');
console.log('reverse("hello"):', StringUtils.reverse('hello'));
console.log('repeat("ab", 3):', StringUtils.repeat('ab', 3));
console.log();

// Splitting and Joining
console.log('--- Splitting and Joining ---');
console.log('split("a,b,c", ","):', JSON.stringify(StringUtils.split('a,b,c', ',')));
console.log('lines("line1\\nline2\\nline3"):', JSON.stringify(StringUtils.lines('line1\nline2\nline3')));
console.log('join(["a", "b", "c"], "-"):', StringUtils.join(['a', 'b', 'c'], '-'));
console.log();

// Validation
console.log('--- Validation ---');
console.log('isValidEmail("test@example.com"):', StringUtils.isValidEmail('test@example.com'));
console.log('isValidEmail("invalid"):', StringUtils.isValidEmail('invalid'));
console.log('isValidUrl("https://example.com"):', StringUtils.isValidUrl('https://example.com'));
console.log('isValidIPv4("192.168.1.1"):', StringUtils.isValidIPv4('192.168.1.1'));
console.log('isNumeric("123.45"):', StringUtils.isNumeric('123.45'));
console.log('isInteger("123"):', StringUtils.isInteger('123'));
console.log('isAlpha("abc"):', StringUtils.isAlpha('abc'));
console.log('isAlphanumeric("abc123"):', StringUtils.isAlphanumeric('abc123'));
console.log();

// Naming Conventions
console.log('--- Naming Conventions ---');
console.log('toCamelCase("hello-world"):', StringUtils.toCamelCase('hello-world'));
console.log('toCamelCase("hello_world"):', StringUtils.toCamelCase('hello_world'));
console.log('toPascalCase("hello-world"):', StringUtils.toPascalCase('hello-world'));
console.log('toSnakeCase("helloWorld"):', StringUtils.toSnakeCase('helloWorld'));
console.log('toKebabCase("helloWorld"):', StringUtils.toKebabCase('helloWorld'));
console.log();

// Random Generation
console.log('--- Random Generation ---');
console.log('random(10):', StringUtils.random(10));
console.log('randomAlphanumeric(10):', StringUtils.randomAlphanumeric(10));
console.log('randomNumeric(10):', StringUtils.randomNumeric(10));
console.log('randomAlphabetic(10):', StringUtils.randomAlphabetic(10));
console.log('randomPassword(16):', StringUtils.randomPassword(16));
console.log();

// URL Encoding
console.log('--- URL Encoding ---');
console.log('urlEncode("hello world"):', StringUtils.urlEncode('hello world'));
console.log('urlDecode("hello%20world"):', StringUtils.urlDecode('hello%20world'));
console.log();

// Slug Generation
console.log('--- Slug Generation ---');
console.log('slugify("Hello World!"):', StringUtils.slugify('Hello World!'));
console.log('slugify("My Blog Post Title"):', StringUtils.slugify('My Blog Post Title'));
console.log();

// HTML Operations
console.log('--- HTML Operations ---');
console.log('stripHtml("<p>hello</p>"):', StringUtils.stripHtml('<p>hello</p>'));
console.log('escapeHtml("<script>alert(1)</script>"):', StringUtils.escapeHtml('<script>alert(1)</script>'));
console.log('unescapeHtml("&lt;script&gt;"):', StringUtils.unescapeHtml('&lt;script&gt;'));
console.log();

// Comparison
console.log('--- Comparison ---');
console.log('equals("hello", "hello"):', StringUtils.equals('hello', 'hello'));
console.log('equals("Hello", "hello", true):', StringUtils.equals('Hello', 'hello', true));
console.log('compare("a", "b"):', StringUtils.compare('a', 'b'));
console.log();

// Default Values
console.log('--- Default Values ---');
console.log('defaultString("", "default"):', StringUtils.defaultString('', 'default'));
console.log('defaultString("hello", "default"):', StringUtils.defaultString('hello', 'default'));
console.log('defaultIfEmpty("", "default"):', StringUtils.defaultIfEmpty('', 'default'));
console.log('defaultIfEmpty("  ", "default"):', StringUtils.defaultIfEmpty('  ', 'default'));
console.log();

console.log('========================================');
console.log('Examples completed!');
console.log('========================================');