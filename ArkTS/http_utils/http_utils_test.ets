/**
 * HTTP Utils Test Suite for ArkTS
 * 
 * Unit tests for the HTTP utilities module.
 * Run with HarmonyOS test framework or manually in development environment.
 * 
 * @module http_utils_test
 * @version 1.0.0
 */

import {
  buildUrl,
  buildQueryString,
  urlEncode,
  urlDecode,
  parseUrl,
  getDomain,
  getPath,
  isValidUrl,
  parseQueryString,
  addQueryParams,
  removeQueryParams
} from './mod';

/**
 * Test result interface
 */
interface TestResult {
  name: string;
  passed: boolean;
  message?: string;
}

/**
 * Test runner
 */
class TestRunner {
  private results: TestResult[] = [];
  private currentSuite: string = '';

  suite(name: string): void {
    this.currentSuite = name;
    console.info(`\n=== ${name} ===`);
  }

  test(name: string, fn: () => void): void {
    try {
      fn();
      this.results.push({ name: `${this.currentSuite}: ${name}`, passed: true });
      console.info(`  ✓ ${name}`);
    } catch (error) {
      this.results.push({ 
        name: `${this.currentSuite}: ${name}`, 
        passed: false, 
        message: error.message 
      });
      console.error(`  ✗ ${name}: ${error.message}`);
    }
  }

  assertEqual(actual: unknown, expected: unknown, message?: string): void {
    if (actual !== expected) {
      throw new Error(message || `Expected ${expected}, got ${actual}`);
    }
  }

  assertTrue(value: boolean, message?: string): void {
    if (!value) {
      throw new Error(message || 'Expected true, got false');
    }
  }

  assertFalse(value: boolean, message?: string): void {
    if (value) {
      throw new Error(message || 'Expected false, got true');
    }
  }

  assertObjectEqual(actual: Record<string, unknown>, expected: Record<string, unknown>): void {
    const actualStr = JSON.stringify(actual);
    const expectedStr = JSON.stringify(expected);
    if (actualStr !== expectedStr) {
      throw new Error(`Expected ${expectedStr}, got ${actualStr}`);
    }
  }

  summary(): void {
    const passed = this.results.filter(r => r.passed).length;
    const failed = this.results.filter(r => !r.passed).length;
    
    console.info('\n=== Test Summary ===');
    console.info(`Total: ${this.results.length}`);
    console.info(`Passed: ${passed}`);
    console.info(`Failed: ${failed}`);
    
    if (failed > 0) {
      console.error('\nFailed tests:');
      this.results
        .filter(r => !r.passed)
        .forEach(r => console.error(`  - ${r.name}: ${r.message}`));
    }
  }
}

export function runTests(): void {
  const runner = new TestRunner();

  runner.suite('buildUrl');
  runner.test('builds URL with no params', () => {
    runner.assertEqual(buildUrl('https://example.com'), 'https://example.com');
  });
  runner.test('builds URL with params', () => {
    const result = buildUrl('https://example.com/users', { page: 1, limit: 10 });
    runner.assertTrue(result.includes('page=1'));
    runner.assertTrue(result.includes('limit=10'));
    runner.assertTrue(result.startsWith('https://example.com/users?'));
  });
  runner.test('appends to existing query string', () => {
    const result = buildUrl('https://example.com/users?sort=desc', { page: 1 });
    runner.assertTrue(result.includes('sort=desc'));
    runner.assertTrue(result.includes('page=1'));
    runner.assertTrue(result.includes('&'));
  });
  runner.test('handles empty params', () => {
    runner.assertEqual(buildUrl('https://example.com', {}), 'https://example.com');
  });
  runner.test('encodes special characters', () => {
    const result = buildUrl('https://example.com/search', { q: 'hello world' });
    runner.assertTrue(result.includes('hello%20world'));
  });

  runner.suite('buildQueryString');
  runner.test('builds query string from object', () => {
    const result = buildQueryString({ name: 'John', age: 30 });
    runner.assertTrue(result.includes('name=John'));
    runner.assertTrue(result.includes('age=30'));
  });
  runner.test('encodes values', () => {
    const result = buildQueryString({ key: 'value with spaces' });
    runner.assertEqual(result, 'key=value%20with%20spaces');
  });
  runner.test('handles boolean values', () => {
    const result = buildQueryString({ active: true, deleted: false });
    runner.assertTrue(result.includes('active=true'));
    runner.assertTrue(result.includes('deleted=false'));
  });

  runner.suite('urlEncode');
  runner.test('encodes spaces', () => {
    runner.assertEqual(urlEncode('hello world'), 'hello%20world');
  });
  runner.test('encodes special characters', () => {
    runner.assertEqual(urlEncode('a+b=c'), 'a%2Bb%3Dc');
  });
  runner.test('encodes unicode', () => {
    runner.assertEqual(urlEncode('你好'), '%E4%BD%A0%E5%A5%BD');
  });

  runner.suite('urlDecode');
  runner.test('decodes spaces', () => {
    runner.assertEqual(urlDecode('hello%20world'), 'hello world');
  });
  runner.test('decodes special characters', () => {
    runner.assertEqual(urlDecode('a%2Bb%3Dc'), 'a+b=c');
  });
  runner.test('decodes unicode', () => {
    runner.assertEqual(urlDecode('%E4%BD%A0%E5%A5%BD'), '你好');
  });

  runner.suite('parseUrl');
  runner.test('parses simple URL', () => {
    const result = parseUrl('https://example.com');
    runner.assertEqual(result.protocol, 'https');
    runner.assertEqual(result.hostname, 'example.com');
  });
  runner.test('parses URL with port', () => {
    const result = parseUrl('https://example.com:8080/path');
    runner.assertEqual(result.port, '8080');
    runner.assertEqual(result.pathname, '/path');
  });
  runner.test('parses URL with query', () => {
    const result = parseUrl('https://example.com?foo=bar');
    runner.assertEqual(result.search, 'foo=bar');
  });
  runner.test('parses URL with hash', () => {
    const result = parseUrl('https://example.com#section');
    runner.assertEqual(result.hash, 'section');
  });
  runner.test('defaults http port', () => {
    const result = parseUrl('http://example.com');
    runner.assertEqual(result.port, '80');
  });
  runner.test('defaults https port', () => {
    const result = parseUrl('https://example.com');
    runner.assertEqual(result.port, '443');
  });

  runner.suite('getDomain');
  runner.test('extracts domain from URL', () => {
    runner.assertEqual(getDomain('https://api.example.com/users'), 'api.example.com');
  });
  runner.test('extracts domain without path', () => {
    runner.assertEqual(getDomain('https://example.com'), 'example.com');
  });

  runner.suite('getPath');
  runner.test('extracts path from URL', () => {
    runner.assertEqual(getPath('https://example.com/users/123'), '/users/123');
  });
  runner.test('returns root for no path', () => {
    runner.assertEqual(getPath('https://example.com'), '/');
  });

  runner.suite('isValidUrl');
  runner.test('validates HTTPS URL', () => {
    runner.assertTrue(isValidUrl('https://example.com'));
  });
  runner.test('validates HTTP URL', () => {
    runner.assertTrue(isValidUrl('http://example.com'));
  });
  runner.test('validates URL with path', () => {
    runner.assertTrue(isValidUrl('https://example.com/path/to/resource'));
  });
  runner.test('validates URL with query', () => {
    runner.assertTrue(isValidUrl('https://example.com?key=value'));
  });
  runner.test('validates URL with port', () => {
    runner.assertTrue(isValidUrl('https://example.com:8080'));
  });
  runner.test('rejects invalid URL', () => {
    runner.assertFalse(isValidUrl('not a url'));
  });
  runner.test('rejects empty string', () => {
    runner.assertFalse(isValidUrl(''));
  });
  runner.test('rejects null-like values', () => {
    runner.assertFalse(isValidUrl('null'));
  });

  runner.suite('parseQueryString');
  runner.test('parses simple query', () => {
    const result = parseQueryString('name=John&age=30');
    runner.assertObjectEqual(result, { name: 'John', age: '30' });
  });
  runner.test('parses query with leading ?', () => {
    const result = parseQueryString('?name=John');
    runner.assertObjectEqual(result, { name: 'John' });
  });
  runner.test('decodes values', () => {
    const result = parseQueryString('key=hello%20world');
    runner.assertEqual(result.key, 'hello world');
  });
  runner.test('handles empty query', () => {
    const result = parseQueryString('');
    runner.assertObjectEqual(result, {});
  });
  runner.test('handles value without key', () => {
    const result = parseQueryString('=value');
    runner.assertEqual(result[''], 'value');
  });

  runner.suite('addQueryParams');
  runner.test('adds params to URL without query', () => {
    const result = addQueryParams('https://example.com', { page: 1 });
    runner.assertEqual(result, 'https://example.com?page=1');
  });
  runner.test('adds params to URL with existing query', () => {
    const result = addQueryParams('https://example.com?sort=desc', { page: 1 });
    runner.assertTrue(result.includes('sort=desc'));
    runner.assertTrue(result.includes('page=1'));
  });

  runner.suite('removeQueryParams');
  runner.test('removes single param', () => {
    const result = removeQueryParams('https://example.com?page=1&sort=desc', ['page']);
    runner.assertFalse(result.includes('page=1'));
    runner.assertTrue(result.includes('sort=desc'));
  });
  runner.test('removes multiple params', () => {
    const result = removeQueryParams('https://example.com?page=1&sort=desc&limit=10', ['page', 'sort']);
    runner.assertFalse(result.includes('page'));
    runner.assertFalse(result.includes('sort'));
    runner.assertTrue(result.includes('limit=10'));
  });
  runner.test('returns unchanged if no params', () => {
    const result = removeQueryParams('https://example.com', ['page']);
    runner.assertEqual(result, 'https://example.com');
  });

  runner.summary();
}
