/**
 * URL Utilities Test Suite
 * Comprehensive tests for all url_utils functions
 */

const assert = require('assert');
const urlUtils = require('./mod.js');

let passCount = 0;
let failCount = 0;

function test(name, fn) {
    try {
        fn();
        console.log(`✓ ${name}`);
        passCount++;
    } catch (e) {
        console.log(`✗ ${name}: ${e.message}`);
        failCount++;
    }
}

console.log('\n=== URL Utilities Test Suite ===\n');

// Test parse()
console.log('\n--- parse() ---');

test('parse basic URL', () => {
    const result = urlUtils.parse('https://example.com/path');
    assert.strictEqual(result.protocol, 'https');
    assert.strictEqual(result.hostname, 'example.com');
    assert.strictEqual(result.path, '/path');
});

test('parse URL with port', () => {
    const result = urlUtils.parse('https://example.com:8080/path');
    assert.strictEqual(result.port, '8080');
});

test('parse URL with query', () => {
    const result = urlUtils.parse('https://example.com?key=value&foo=bar');
    assert.deepStrictEqual(result.query, { key: 'value', foo: 'bar' });
});

test('parse URL with hash', () => {
    const result = urlUtils.parse('https://example.com#section');
    assert.strictEqual(result.hash, 'section');
});

test('parse URL with authentication', () => {
    const result = urlUtils.parse('https://user:pass@example.com');
    assert.strictEqual(result.username, 'user');
    assert.strictEqual(result.password, 'pass');
});

test('parse invalid URL returns null', () => {
    assert.strictEqual(urlUtils.parse(''), null);
    assert.strictEqual(urlUtils.parse(null), null);
    assert.strictEqual(urlUtils.parse(undefined), null);
    assert.strictEqual(urlUtils.parse(123), null);
});

// Test parseQuery()
console.log('\n--- parseQuery() ---');

test('parse basic query string', () => {
    const result = urlUtils.parseQuery('?key=value');
    assert.deepStrictEqual(result, { key: 'value' });
});

test('parse query string without leading ?', () => {
    const result = urlUtils.parseQuery('key=value');
    assert.deepStrictEqual(result, { key: 'value' });
});

test('parse multiple parameters', () => {
    const result = urlUtils.parseQuery('a=1&b=2&c=3');
    assert.deepStrictEqual(result, { a: '1', b: '2', c: '3' });
});

test('parse encoded values', () => {
    const result = urlUtils.parseQuery('name=John%20Doe&email=test%40example.com');
    assert.strictEqual(result.name, 'John Doe');
    assert.strictEqual(result.email, 'test@example.com');
});

test('parse duplicate keys to array', () => {
    const result = urlUtils.parseQuery('tag=a&tag=b&tag=c');
    assert.deepStrictEqual(result.tag, ['a', 'b', 'c']);
});

test('parse array notation', () => {
    const result = urlUtils.parseQuery('items[]=1&items[]=2');
    assert.deepStrictEqual(result.items, ['1', '2']);
});

test('parse empty query string', () => {
    const result = urlUtils.parseQuery('');
    assert.deepStrictEqual(result, {});
});

test('parse parameter without value', () => {
    const result = urlUtils.parseQuery('flag');
    assert.strictEqual(result.flag, '');
});

// Test buildQuery()
console.log('\n--- buildQuery() ---');

test('build basic query string', () => {
    const result = urlUtils.buildQuery({ key: 'value' });
    assert.strictEqual(result, '?key=value');
});

test('build query without prefix', () => {
    const result = urlUtils.buildQuery({ key: 'value' }, { prefix: '' });
    assert.strictEqual(result, 'key=value');
});

test('build query with multiple parameters', () => {
    const result = urlUtils.buildQuery({ a: '1', b: '2' });
    assert.strictEqual(result, '?a=1&b=2');
});

test('build query with sorted keys', () => {
    const result = urlUtils.buildQuery({ z: '1', a: '2' }, { sort: true });
    assert.strictEqual(result, '?a=2&z=1');
});

test('build query with array values', () => {
    const result = urlUtils.buildQuery({ tags: ['a', 'b'] });
    assert.ok(result.includes('tags=a'));
    assert.ok(result.includes('tags=b'));
});

test('build query skips null/undefined values', () => {
    const result = urlUtils.buildQuery({ a: '1', b: null, c: undefined });
    assert.strictEqual(result, '?a=1');
});

test('build empty object returns empty string', () => {
    assert.strictEqual(urlUtils.buildQuery({}), '');
    assert.strictEqual(urlUtils.buildQuery(null), '');
});

// Test build()
console.log('\n--- build() ---');

test('build basic URL', () => {
    const result = urlUtils.build({ protocol: 'https', hostname: 'example.com' });
    assert.strictEqual(result, 'https://example.com/');
});

test('build URL with port', () => {
    const result = urlUtils.build({ protocol: 'https', hostname: 'example.com', port: '8080' });
    assert.strictEqual(result, 'https://example.com:8080/');
});

test('build URL with path', () => {
    const result = urlUtils.build({ protocol: 'https', hostname: 'example.com', path: '/api/users' });
    assert.strictEqual(result, 'https://example.com/api/users');
});

test('build URL with query', () => {
    const result = urlUtils.build({ protocol: 'https', hostname: 'example.com', query: { key: 'value' } });
    assert.strictEqual(result, 'https://example.com/?key=value');
});

test('build URL with authentication', () => {
    const result = urlUtils.build({ protocol: 'https', hostname: 'example.com', username: 'user', password: 'pass' });
    assert.strictEqual(result, 'https://user:pass@example.com/');
});

test('build URL with hash', () => {
    const result = urlUtils.build({ protocol: 'https', hostname: 'example.com', hash: 'section' });
    assert.strictEqual(result, 'https://example.com/#section');
});

test('build throws without hostname', () => {
    assert.throws(() => urlUtils.build({}), /Hostname is required/);
});

// Test isValid()
console.log('\n--- isValid() ---');

test('valid HTTP URL', () => {
    assert.strictEqual(urlUtils.isValid('http://example.com'), true);
});

test('valid HTTPS URL', () => {
    assert.strictEqual(urlUtils.isValid('https://example.com'), true);
});

test('invalid URL returns false', () => {
    assert.strictEqual(urlUtils.isValid('not a url'), false);
    assert.strictEqual(urlUtils.isValid(''), false);
});

test('disallowed protocol returns false', () => {
    assert.strictEqual(urlUtils.isValid('ftp://example.com'), false);
});

test('allow custom protocols', () => {
    assert.strictEqual(urlUtils.isValid('ftp://example.com', { protocols: ['ftp'] }), true);
});

test('URL without protocol when requireProtocol=false', () => {
    assert.strictEqual(urlUtils.isValid('example.com/path', { requireProtocol: false }), true);
});

// Test joinPaths()
console.log('\n--- joinPaths() ---');

test('join simple paths', () => {
    assert.strictEqual(urlUtils.joinPaths('a', 'b', 'c'), 'a/b/c');
});

test('join with leading slashes', () => {
    assert.strictEqual(urlUtils.joinPaths('/a', '/b', '/c'), '/a/b/c');
});

test('join empty parts', () => {
    assert.strictEqual(urlUtils.joinPaths('a', '', 'b'), 'a/b');
});

test('join with full URL', () => {
    const result = urlUtils.joinPaths('https://example.com/', 'path');
    assert.strictEqual(result, 'https://example.com/path');
});

test('join no arguments returns root', () => {
    assert.strictEqual(urlUtils.joinPaths(), '/');
});

// Test resolve()
console.log('\n--- resolve() ---');

test('resolve relative path', () => {
    assert.strictEqual(
        urlUtils.resolve('https://example.com/page', '/api/data'),
        'https://example.com/api/data'
    );
});

test('resolve relative path without leading slash', () => {
    assert.strictEqual(
        urlUtils.resolve('https://example.com/', 'api/data'),
        'https://example.com/api/data'
    );
});

test('resolve with query parameters', () => {
    const result = urlUtils.resolve('https://example.com', '?key=value');
    assert.strictEqual(result, 'https://example.com/?key=value');
});

test('resolve with null base returns null', () => {
    assert.strictEqual(urlUtils.resolve(null, '/path'), null);
});

// Test normalize()
console.log('\n--- normalize() ---');

test('normalize removes default HTTP port', () => {
    const result = urlUtils.normalize('http://example.com:80/path');
    assert.strictEqual(result, 'http://example.com/path');
});

test('normalize removes default HTTPS port', () => {
    const result = urlUtils.normalize('https://example.com:443/path');
    assert.strictEqual(result, 'https://example.com/path');
});

test('normalize lowercases hostname', () => {
    const result = urlUtils.normalize('https://EXAMPLE.COM/path');
    assert.strictEqual(result, 'https://example.com/path');
});

test('normalize removes trailing slash', () => {
    const result = urlUtils.normalize('https://example.com/path/');
    assert.strictEqual(result, 'https://example.com/path');
});

test('normalize keeps root slash', () => {
    const result = urlUtils.normalize('https://example.com/');
    assert.strictEqual(result, 'https://example.com/');
});

test('normalize sorts query parameters', () => {
    const result = urlUtils.normalize('https://example.com?z=1&a=2');
    assert.strictEqual(result, 'https://example.com/?a=2&z=1');
});

test('normalize returns null for invalid URL', () => {
    assert.strictEqual(urlUtils.normalize('not a url'), null);
});

// Test getDomain()
console.log('\n--- getDomain() ---');

test('get domain from URL', () => {
    assert.strictEqual(urlUtils.getDomain('https://www.example.com/path'), 'www.example.com');
});

test('get domain with port', () => {
    assert.strictEqual(urlUtils.getDomain('https://example.com:8080'), 'example.com');
});

test('get domain returns null for invalid URL', () => {
    assert.strictEqual(urlUtils.getDomain('not a url'), null);
});

// Test getTLD()
console.log('\n--- getTLD() ---');

test('get TLD from URL', () => {
    assert.strictEqual(urlUtils.getTLD('https://example.com'), 'com');
});

test('get TLD from subdomain URL', () => {
    assert.strictEqual(urlUtils.getTLD('https://blog.example.co.uk'), 'uk');
});

test('get TLD returns null for IP address', () => {
    assert.strictEqual(urlUtils.getTLD('https://192.168.1.1'), null);
});

test('get TLD returns null for localhost', () => {
    assert.strictEqual(urlUtils.getTLD('https://localhost'), null);
});

// Test getSubdomain()
console.log('\n--- getSubdomain() ---');

test('get subdomain from URL', () => {
    assert.strictEqual(urlUtils.getSubdomain('https://blog.example.com'), 'blog');
});

test('get subdomain from multi-level subdomain', () => {
    assert.strictEqual(urlUtils.getSubdomain('https://api.v1.example.com'), 'api.v1');
});

test('get subdomain returns null for no subdomain', () => {
    assert.strictEqual(urlUtils.getSubdomain('https://example.com'), null);
});

test('get subdomain returns null for localhost', () => {
    assert.strictEqual(urlUtils.getSubdomain('https://localhost'), null);
});

// Test isAbsolute() and isRelative()
console.log('\n--- isAbsolute() / isRelative() ---');

test('isAbsolute for full URL', () => {
    assert.strictEqual(urlUtils.isAbsolute('https://example.com'), true);
});

test('isAbsolute for protocol-relative URL', () => {
    assert.strictEqual(urlUtils.isAbsolute('//example.com'), true);
});

test('isAbsolute for relative path returns false', () => {
    assert.strictEqual(urlUtils.isAbsolute('/path'), false);
});

test('isRelative for relative path', () => {
    assert.strictEqual(urlUtils.isRelative('/path'), true);
});

test('isRelative for full URL returns false', () => {
    assert.strictEqual(urlUtils.isRelative('https://example.com'), false);
});

// Test addQuery() and removeQuery()
console.log('\n--- addQuery() / removeQuery() ---');

test('add query parameter', () => {
    const result = urlUtils.addQuery('https://example.com', { key: 'value' });
    assert.strictEqual(result, 'https://example.com/?key=value');
});

test('add query to existing query', () => {
    const result = urlUtils.addQuery('https://example.com?a=1', { b: '2' });
    assert.strictEqual(result, 'https://example.com/?a=1&b=2');
});

test('update existing query parameter', () => {
    const result = urlUtils.addQuery('https://example.com?key=old', { key: 'new' });
    assert.strictEqual(result, 'https://example.com/?key=new');
});

test('remove query parameter', () => {
    const result = urlUtils.removeQuery('https://example.com?a=1&b=2', ['a']);
    assert.strictEqual(result, 'https://example.com/?b=2');
});

test('remove multiple query parameters', () => {
    const result = urlUtils.removeQuery('https://example.com?a=1&b=2&c=3', ['a', 'c']);
    assert.strictEqual(result, 'https://example.com/?b=2');
});

test('addQuery returns null for invalid URL', () => {
    assert.strictEqual(urlUtils.addQuery('not a url', { key: 'value' }), null);
});

// Test getExtension() and getFilename()
console.log('\n--- getExtension() / getFilename() ---');

test('get extension from URL', () => {
    assert.strictEqual(urlUtils.getExtension('https://example.com/file.txt'), 'txt');
});

test('get extension from URL with query', () => {
    assert.strictEqual(urlUtils.getExtension('https://example.com/file.jpg?size=large'), 'jpg');
});

test('get extension returns null for no extension', () => {
    assert.strictEqual(urlUtils.getExtension('https://example.com/path/'), null);
});

test('get filename from URL', () => {
    assert.strictEqual(urlUtils.getFilename('https://example.com/path/to/file.txt'), 'file.txt');
});

test('get filename from URL with query', () => {
    assert.strictEqual(urlUtils.getFilename('https://example.com/document.pdf?v=1'), 'document.pdf');
});

test('get filename returns null for root path', () => {
    assert.strictEqual(urlUtils.getFilename('https://example.com/'), null);
});

// Test toAbsolute()
console.log('\n--- toAbsolute() ---');

test('toAbsolute converts relative to absolute', () => {
    assert.strictEqual(
        urlUtils.toAbsolute('/path', 'https://example.com'),
        'https://example.com/path'
    );
});

test('toAbsolute keeps absolute URL unchanged', () => {
    assert.strictEqual(
        urlUtils.toAbsolute('https://other.com/path', 'https://example.com'),
        'https://other.com/path'
    );
});

// Test areEquivalent()
console.log('\n--- areEquivalent() ---');

test('equivalent URLs', () => {
    assert.strictEqual(
        urlUtils.areEquivalent('https://EXAMPLE.COM/path/', 'https://example.com/path'),
        true
    );
});

test('equivalent URLs with different query order', () => {
    assert.strictEqual(
        urlUtils.areEquivalent('https://example.com?a=1&b=2', 'https://example.com?b=2&a=1'),
        true
    );
});

test('non-equivalent URLs', () => {
    assert.strictEqual(
        urlUtils.areEquivalent('https://example.com/a', 'https://example.com/b'),
        false
    );
});

// Test getPathSegments()
console.log('\n--- getPathSegments() ---');

test('get path segments', () => {
    assert.deepStrictEqual(
        urlUtils.getPathSegments('https://example.com/a/b/c'),
        ['a', 'b', 'c']
    );
});

test('get path segments from root', () => {
    assert.deepStrictEqual(
        urlUtils.getPathSegments('https://example.com/'),
        []
    );
});

test('get path segments handles extra slashes', () => {
    assert.deepStrictEqual(
        urlUtils.getPathSegments('https://example.com//a//b//'),
        ['a', 'b']
    );
});

// Test fromTemplate() and parseTemplate()
console.log('\n--- fromTemplate() / parseTemplate() ---');

test('build URL from template', () => {
    const result = urlUtils.fromTemplate('/users/:id/posts/:postId', { id: '123', postId: '456' });
    assert.strictEqual(result, '/users/123/posts/456');
});

test('build URL from template encodes values', () => {
    const result = urlUtils.fromTemplate('/search/:query', { query: 'hello world' });
    assert.strictEqual(result, '/search/hello%20world');
});

test('parse template parameters', () => {
    const result = urlUtils.parseTemplate('/users/:id/posts/:postId');
    assert.deepStrictEqual(result, ['id', 'postId']);
});

test('parse template with no parameters', () => {
    const result = urlUtils.parseTemplate('/static/path');
    assert.deepStrictEqual(result, []);
});

// Test roundtrip: parse -> build
console.log('\n--- Roundtrip Tests ---');

test('roundtrip: parse then build', () => {
    const original = 'https://user:pass@example.com:8080/path?key=value#hash';
    const parsed = urlUtils.parse(original);
    const built = urlUtils.build(parsed);
    assert.strictEqual(built, original);
});

test('roundtrip: parseQuery then buildQuery', () => {
    const original = 'key1=value1&key2=value2';
    const parsed = urlUtils.parseQuery(original);
    const built = urlUtils.buildQuery(parsed, { prefix: '' });
    assert.strictEqual(built, original);
});

// Print summary
console.log('\n=== Test Summary ===');
console.log(`Passed: ${passCount}`);
console.log(`Failed: ${failCount}`);
console.log(`Total: ${passCount + failCount}`);
console.log(failCount === 0 ? '\n✓ All tests passed!' : `\n✗ ${failCount} test(s) failed.`);

process.exit(failCount === 0 ? 0 : 1);