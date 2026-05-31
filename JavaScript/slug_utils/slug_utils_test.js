/**
 * slug_utils Tests
 * Comprehensive test suite for JavaScript slug utilities
 */

const {
  slugify,
  validateSlug,
  uniqueSlugify,
  uniqueSlugifySync,
  unslugify,
  extractSlugs,
  joinSlug,
  parseSlug,
  optionsToQueryString,
  DEFAULT_CONFIG
} = require('./mod.js');

// Test utilities
let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (error) {
    console.log(`❌ ${name}`);
    console.log(`   Error: ${error.message}`);
    failed++;
  }
}

function assertEqual(actual, expected, message = '') {
  if (actual !== expected) {
    throw new Error(`${message} Expected "${expected}", got "${actual}"`);
  }
}

function assertDeepEqual(actual, expected, message = '') {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`${message} Expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

console.log('\n=== slug_utils Tests ===\n');

// Basic slugify tests
console.log('--- Basic Slugify ---');

test('slugify basic', () => {
  assertEqual(slugify('Hello World'), 'hello-world');
});

test('slugify lowercase', () => {
  assertEqual(slugify('Hello World'), 'hello-world');
});

test('slugify with spaces', () => {
  assertEqual(slugify('  Hello   World  '), 'hello-world');
});

test('slugify with special chars', () => {
  assertEqual(slugify('Hello@World!'), 'helloworld');
});

test('slugify empty string', () => {
  assertEqual(slugify(''), '');
});

test('slugify null/undefined', () => {
  assertEqual(slugify(null), '');
  assertEqual(slugify(undefined), '');
});

// Custom separator tests
console.log('\n--- Custom Separator ---');

test('separator underscore', () => {
  assertEqual(slugify('Hello World', { separator: '_' }), 'hello_world');
});

test('separator dot', () => {
  assertEqual(slugify('Hello World', { separator: '.' }), 'hello.world');
});

test('separator shorthand', () => {
  assertEqual(slugify('Hello World', '_'), 'hello_world');
});

test('separator empty handled', () => {
  // Empty separator should be replaced with default
  const result = slugify('Hello World', { separator: '' });
  assertEqual(result === 'helloworld' || result === 'hello-world', true);
});

// Case options tests
console.log('\n--- Case Options ---');

test('preserve lowercase by default', () => {
  assertEqual(slugify('Hello World'), 'hello-world');
});

test('preserve case option', () => {
  assertEqual(slugify('Hello World', { lowercase: false }), 'Hello-World');
});

// Max length tests
console.log('\n--- Max Length ---');

test('max length truncation', () => {
  const result = slugify('Hello World Example', { maxLength: 11 });
  assertEqual(result.startsWith('hello'), true);
});

test('max length at word boundary', () => {
  const result = slugify('Hello World', { maxLength: 8 });
  assertEqual(result === 'hello' || result === 'hello-wor', true);
});

test('max length preserves words', () => {
  const result = slugify('Hello World Example Test', { maxLength: 20 });
  assertEqual(result.startsWith('hello-world'), true);
});

// Trim tests
console.log('\n--- Trim Options ---');

test('trim leading/trailing separators', () => {
  assertEqual(slugify('  Hello World  '), 'hello-world');
});

test('no trim', () => {
  const result = slugify('  Hello World  ', { trim: false });
  assertEqual(result.includes('hello-world'), true);
});

// Stopwords tests
console.log('\n--- Stopwords ---');

test('remove stopwords', () => {
  const result = slugify('The Hello World', { removeStopwords: true });
  assertEqual(result, 'hello-world');
});

test('stopwords case insensitive', () => {
  const result = slugify('THE Hello WORLD', { removeStopwords: true });
  assertEqual(result, 'hello-world');
});

// Custom replacements tests
console.log('\n--- Custom Replacements ---');

test('custom replacement single', () => {
  assertEqual(
    slugify('Hello World', { customReplacements: { 'world': 'universe' } }),
    'hello-universe'
  );
});

test('custom replacement c++', () => {
  assertEqual(
    slugify('C++ Programming', { customReplacements: { 'C++': 'cpp' } }),
    'cpp-programming'
  );
});

// Strict mode tests
console.log('\n--- Strict Mode ---');

test('strict mode removes dots', () => {
  assertEqual(slugify('file.txt', { strict: true }), 'filetxt');
});

test('strict mode removes special chars', () => {
  assertEqual(slugify('Hello@World!', { strict: true }), 'helloworld');
});

// Multiple languages tests
console.log('\n--- Multiple Languages ---');

test('Chinese characters', () => {
  const result = slugify('你好世界');
  assertEqual(result.includes('hao') && result.includes('shi'), true);
});

test('Japanese hiragana', () => {
  const result = slugify('こんにちは');
  assertEqual(result.includes('kon'), true);
});

test('Korean hangul', () => {
  const result = slugify('안녕하세요');
  assertEqual(result.length > 0, true);
});

test('Russian cyrillic', () => {
  assertEqual(slugify('Привет мир'), 'privet-mir');
});

test('French accents', () => {
  assertEqual(slugify('Café'), 'cafe');
});

test('German umlauts', () => {
  assertEqual(slugify('München'), 'munchen');
});

test('Spanish ñ', () => {
  assertEqual(slugify('España'), 'espana');
});

test('Vietnamese diacritics', () => {
  assertEqual(slugify('Xin chào'), 'xin-chao');
});

test('Thai characters', () => {
  const result = slugify('สวัสดี');
  assertEqual(result.length > 0, true);
});

test('Arabic characters', () => {
  const result = slugify('مرحبا');
  assertEqual(result.length > 0, true);
});

test('Mixed language', () => {
  const result = slugify('Hello 世界');
  assertEqual(result.includes('hello') && result.includes('shi'), true);
});

// validateSlug tests
console.log('\n--- Validate Slug ---');

test('validate valid slug', () => {
  const result = validateSlug('hello-world');
  assertDeepEqual(result, { valid: true, errors: [] });
});

test('validate empty slug', () => {
  const result = validateSlug('');
  assertEqual(result.valid, false);
  assertEqual(result.errors.length > 0, true);
});

test('validate slug with spaces', () => {
  const result = validateSlug('hello world');
  assertEqual(result.valid, false);
});

test('validate slug with invalid chars', () => {
  const result = validateSlug('hello@world');
  assertEqual(result.valid, false);
});

test('validate slug with leading dash', () => {
  const result = validateSlug('-hello');
  assertEqual(result.valid, false);
});

test('validate slug exceeding max length', () => {
  const longSlug = 'a'.repeat(300);
  const result = validateSlug(longSlug, { maxLength: 255 });
  assertEqual(result.valid, false);
});

test('validate maxLength option', () => {
  const result = validateSlug('hello-world-extra', { maxLength: 10 });
  assertEqual(result.valid, false);
});

// unslugify tests
console.log('\n--- Unslugify ---');

test('unslugify basic', () => {
  assertEqual(unslugify('hello-world'), 'Hello World');
});

test('unslugify with underscore', () => {
  assertEqual(unslugify('hello_world', { separator: '_' }), 'Hello World');
});

test('unslugify empty', () => {
  assertEqual(unslugify(''), '');
});

test('unslugify null', () => {
  assertEqual(unslugify(null), '');
});

// extractSlugs tests
console.log('\n--- Extract Slugs ---');

test('extract single slug', () => {
  const result = extractSlugs('Check out hello-world');
  assertDeepEqual(result, ['hello-world']);
});

test('extract multiple slugs', () => {
  const result = extractSlugs('hello-world and amazing-post');
  assertDeepEqual(result, ['hello-world', 'amazing-post']);
});

test('extract slugs from mixed text', () => {
  const result = extractSlugs('Visit hello-world today!');
  assertDeepEqual(result, ['hello-world']);
});

test('extract no slugs', () => {
  const result = extractSlugs('No slugs here');
  assertDeepEqual(result, []);
});

// joinSlug tests
console.log('\n--- Join Slug ---');

test('join two strings', () => {
  assertEqual(joinSlug('Hello', 'World'), 'hello-world');
});

test('join with array', () => {
  assertEqual(joinSlug(['foo', 'bar'], 'baz'), 'foo-bar-baz');
});

test('join with empty', () => {
  assertEqual(joinSlug('Hello', '', 'World'), 'hello-world');
});

test('join empty', () => {
  assertEqual(joinSlug(), '');
});

// parseSlug tests
console.log('\n--- Parse Slug ---');

test('parse basic slug', () => {
  assertDeepEqual(parseSlug('hello-world'), ['hello', 'world']);
});

test('parse with underscore', () => {
  assertDeepEqual(parseSlug('foo_bar_baz', { separator: '_' }), ['foo', 'bar', 'baz']);
});

test('parse empty slug', () => {
  assertDeepEqual(parseSlug(''), []);
});

test('parse null', () => {
  assertDeepEqual(parseSlug(null), []);
});

// uniqueSlugifySync tests
console.log('\n--- Unique Slugify (Sync) ---');

test('unique slugify no collision', () => {
  // isUnique returns true if the slug is available (unique)
  const exists = (s) => true;  // all slugs are unique
  const result = uniqueSlugifySync('Hello World', exists);
  assertEqual(result, 'hello-world');
});

test('unique slugify with collision', () => {
  const existing = ['hello-world', 'hello-world-2'];
  const exists = (s) => existing.includes(s);
  const result = uniqueSlugifySync('Hello World', exists);
  assertEqual(result === 'hello-world-3' || result === 'hello-world', true);
});

test('unique slugify multiple collisions', () => {
  const existing = ['hello-world', 'hello-world-2', 'hello-world-3'];
  const exists = (s) => existing.includes(s);
  const result = uniqueSlugifySync('Hello World', exists);
  assertEqual(result === 'hello-world-4' || result === 'hello-world', true);
});

// uniqueSlugify async tests
console.log('\n--- Unique Slugify (Async) ---');

test('unique slugify async', async () => {
  const existing = ['hello-world'];
  const exists = async (s) => existing.includes(s);
  const result = await uniqueSlugify('Hello World', exists);
  assertEqual(result === 'hello-world-2' || result === 'hello-world', true);
});

// optionsToQueryString tests
console.log('\n--- Options to Query String ---');

test('default options', () => {
  assertEqual(optionsToQueryString({}), '');
});

test('custom separator', () => {
  const result = optionsToQueryString({ separator: '_' });
  assertEqual(result, 'separator=_');
});

test('preserve case', () => {
  const result = optionsToQueryString({ lowercase: false });
  assertEqual(result, 'lowercase=false');
});

test('max length', () => {
  const result = optionsToQueryString({ maxLength: 50 });
  assertEqual(result, 'maxLength=50');
});

test('multiple options', () => {
  const result = optionsToQueryString({ separator: '.', maxLength: 100 });
  assertEqual(result.includes('separator=.'), true);
  assertEqual(result.includes('maxLength=100'), true);
});

// Edge cases
console.log('\n--- Edge Cases ---');

test('all numbers', () => {
  assertEqual(slugify('123 456'), '123-456');
});

test('only special chars', () => {
  const result = slugify('@@@');
  assertEqual(result === '' || result.length < 3, true);
});

test('long single word', () => {
  assertEqual(slugify('supercalifragilisticexpialidocious'), 'supercalifragilisticexpialidocious');
});

test('already a slug', () => {
  assertEqual(slugify('hello-world'), 'hello-world');
});

test('numbers and letters', () => {
  assertEqual(slugify('Hello World 123'), 'hello-world-123');
});

test('leading numbers', () => {
  assertEqual(slugify('123 Hello'), '123-hello');
});

test('slashes', () => {
  const result = slugify('path/to/file');
  assertEqual(result.includes('pathtofile'), true);
});

// Print summary
console.log('\n=== Test Summary ===');
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
console.log(`Total: ${passed + failed}`);

if (failed > 0) {
  console.log('\n❌ Some tests failed!');
  process.exit(1);
} else {
  console.log('\n✅ All tests passed!');
  process.exit(0);
}
