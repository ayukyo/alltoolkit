/**
 * String Utilities Example for ArkTS
 * 
 * Demonstrates usage of the string_utils module.
 */

import {
  isBlank, isNotBlank,
  trim, capitalize, toCamelCase, toSnakeCase, toKebabCase,
  truncate, substringBetween, substringAfter, substringBefore,
  startsWith, endsWith, removePrefix, removeSuffix,
  isValidEmail, isValidUrl, isNumeric,
  padLeft, padRight, center,
  contains, replaceAll, split, join,
  base64Encode, base64Decode, urlEncode, urlDecode,
  randomString, randomPassword,
  reverse, slugify,
  StringUtils
} from '../string_utils/mod';

// Example 1: Empty/Blank Checks
console.log('=== Example 1: Empty/Blank Checks ===');
console.log('isBlank("hello"):', isBlank('hello'));           // false
console.log('isBlank("  "):', isBlank('  '));                 // true
console.log('isBlank(null):', isBlank(null));                 // true
console.log('isNotBlank("hello"):', isNotBlank('hello'));     // true

// Example 2: Trimming and Whitespace
console.log('\n=== Example 2: Trimming ===');
const padded = '  hello world  ';
console.log('Original:', `"${padded}"`);
console.log('trim():', `"${trim(padded)}"`);
console.log('trimLeft():', `"${trimLeft(padded)}"`);
console.log('trimRight():', `"${trimRight(padded)}"`);

// Example 3: Case Conversion
console.log('\n=== Example 3: Case Conversion ===');
const input = 'hello_world';
console.log('Original:', input);
console.log('toCamelCase:', toCamelCase(input));      // helloWorld
console.log('toPascalCase:', toPascalCase(input));    // HelloWorld
console.log('toSnakeCase:', toSnakeCase('HelloWorld')); // hello_world
console.log('toKebabCase:', toKebabCase('HelloWorld')); // hello-world
console.log('capitalize:', capitalize('hello'));       // Hello
console.log('toTitleCase:', toTitleCase('hello world')); // Hello World

// Example 4: Substring Operations
console.log('\n=== Example 4: Substring Operations ===');
const path = '/home/user/documents/file.txt';
console.log('Path:', path);
console.log('substringAfterLast("/"):', substringAfterLast(path, '/'));     // file.txt
console.log('substringBeforeLast("/"):', substringBeforeLast(path, '/'));   // /home/user/documents
console.log('substringBetween("<", ">"):', substringBetween('<tag>content</tag>', '<', '>')); // tag
console.log('truncate:', truncate('This is a very long text', 15)); // This is a ve...

// Example 5: Prefix/Suffix Operations
console.log('\n=== Example 5: Prefix/Suffix ===');
const filename = 'document.pdf';
console.log('Filename:', filename);
console.log('startsWith("doc"):', startsWith(filename, 'doc'));           // true
console.log('endsWith(".pdf"):', endsWith(filename, '.pdf'));             // true
console.log('removeSuffix(".pdf"):', removeSuffix(filename, '.pdf'));     // document
console.log('removePrefix("doc"):', removePrefix(filename, 'doc'));       // ument.pdf

// Example 6: Validation
console.log('\n=== Example 6: Validation ===');
console.log('isValidEmail("test@example.com"):', isValidEmail('test@example.com')); // true
console.log('isValidEmail("invalid"):', isValidEmail('invalid'));                   // false
console.log('isValidUrl("https://example.com"):', isValidUrl('https://example.com')); // true
console.log('isNumeric("123.45"):', isNumeric('123.45'));                           // true
console.log('isInteger("-42"):', isInteger('-42'));                                 // true
console.log('isAlpha("Hello"):', isAlpha('Hello'));                                 // true

// Example 7: Padding and Alignment
console.log('\n=== Example 7: Padding ===');
console.log('padLeft("5", 3, "0"):', `"${padLeft('5', 3, '0')}"`);     // "005"
console.log('padRight("5", 3, "0"):', `"${padRight('5', 3, '0')}"`);   // "500"
console.log('center("hi", 6):', `"${center('hi', 6)}"`);               // "  hi  "

// Example 8: Search and Replace
console.log('\n=== Example 8: Search and Replace ===');
const text = 'The quick brown fox jumps over the lazy dog';
console.log('Text:', text);
console.log('contains("fox"):', contains(text, 'fox'));               // true
console.log('countMatches("the"):', countMatches(text.toLowerCase(), 'the')); // 2
console.log('replaceAll("o", "0"):', replaceAll(text, 'o', '0'));     // The quick br0wn f0x jumps 0ver the lazy d0g

// Example 9: Split and Join
console.log('\n=== Example 9: Split and Join ===');
const csv = 'apple,banana,cherry';
console.log('CSV:', csv);
const fruits = split(csv, ',');
console.log('split():', JSON.stringify(fruits));                      // ["apple","banana","cherry"]
console.log('join(" | "):', join(fruits, ' | '));                     // apple | banana | cherry

// Example 10: Encoding
console.log('\n=== Example 10: Encoding ===');
const message = 'Hello, World!';
console.log('Message:', message);
const encoded = base64Encode(message);
console.log('base64Encode:', encoded);                                // SGVsbG8sIFdvcmxkIQ==
console.log('base64Decode:', base64Decode(encoded));                  // Hello, World!
console.log('urlEncode:', urlEncode('hello world'));                  // hello%20world
console.log('urlDecode:', urlDecode('hello%20world'));                // hello world

// Example 11: Random Generation
console.log('\n=== Example 11: Random Generation ===');
console.log('randomString(10):', randomString(10));
console.log('randomPassword(16):', randomPassword(16));

// Example 12: Utility Functions
console.log('\n=== Example 12: Utilities ===');
console.log('reverse("hello"):', reverse('hello'));                   // olleh
console.log('slugify("Hello World!"):', slugify('Hello World!'));     // hello-world

// Example 13: Using StringUtils Class
console.log('\n=== Example 13: StringUtils Class ===');
console.log('StringUtils.trim():', StringUtils.trim('  hello  '));
console.log('StringUtils.toCamelCase():', StringUtils.toCamelCase('hello_world'));

console.log('\n=== All Examples Completed ===');
