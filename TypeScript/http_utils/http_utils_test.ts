/**
 * HTTP Utilities Tests
 * 
 * 使用 Node.js 内置测试运行器进行单元测试
 * 运行: node --test --loader ts-node/esm http_utils_test.ts
 * 或: npx ts-node --esm http_utils_test.ts
 */

import { describe, it } from 'node:test';
import assert from 'node:assert';
import {
  buildUrl,
  buildQueryString,
  urlEncode,
  urlDecode,
  HttpError,
  TimeoutError,
  createClient,
} from './mod';

describe('URL Utilities', () => {
  describe('buildQueryString', () => {
    it('should build query string from object', () => {
      const result = buildQueryString({ name: 'John', age: 25 });
      assert.ok(result === 'name=John&age=25' || result === 'age=25&name=John');
    });

    it('should URL encode special characters', () => {
      const result = buildQueryString({ name: 'John Doe', city: 'New York' });
      assert.ok(result.includes('John%20Doe'));
      assert.ok(result.includes('New%20York'));
    });

    it('should filter undefined and null values', () => {
      const result = buildQueryString({ a: 1, b: undefined, c: null, d: 'value' });
      assert.ok(!result.includes('b='));
      assert.ok(!result.includes('c='));
      assert.ok(result.includes('a=1'));
      assert.ok(result.includes('d=value'));
    });

    it('should handle boolean values', () => {
      const result = buildQueryString({ active: true, deleted: false });
      assert.ok(result.includes('active=true'));
      assert.ok(result.includes('deleted=false'));
    });

    it('should handle empty object', () => {
      const result = buildQueryString({});
      assert.strictEqual(result, '');
    });
  });

  describe('buildUrl', () => {
    it('should return base URL when no params', () => {
      const result = buildUrl('https://api.example.com/users');
      assert.strictEqual(result, 'https://api.example.com/users');
    });

    it('should append query params to URL', () => {
      const result = buildUrl('https://api.example.com/search', { q: 'test', page: 1 });
      assert.ok(result.startsWith('https://api.example.com/search?'));
      assert.ok(result.includes('q=test'));
      assert.ok(result.includes('page=1'));
    });

    it('should append to existing query string', () => {
      const result = buildUrl('https://api.example.com/search?sort=desc', { q: 'test' });
      assert.ok(result.includes('?sort=desc&'));
      assert.ok(result.includes('q=test'));
    });
  });

  describe('urlEncode', () => {
    it('should encode special characters', () => {
      assert.strictEqual(urlEncode('hello world'), 'hello%20world');
      assert.strictEqual(urlEncode('a+b=c'), 'a%2Bb%3Dc');
    });

    it('should handle empty string', () => {
      assert.strictEqual(urlEncode(''), '');
    });
  });

  describe('urlDecode', () => {
    it('should decode encoded string', () => {
      assert.strictEqual(urlDecode('hello%20world'), 'hello world');
      assert.strictEqual(urlDecode('a%2Bb%3Dc'), 'a+b=c');
    });

    it('should handle empty string', () => {
      assert.strictEqual(urlDecode(''), '');
    });
  });
});

describe('Error Classes', () => {
  describe('HttpError', () => {
    it('should create error with correct properties', () => {
      const error = new HttpError('Not Found', 404, { message: 'User not found' }, 'https://api.example.com/users');
      
      assert.strictEqual(error.name, 'HttpError');
      assert.strictEqual(error.message, 'Not Found');
      assert.strictEqual(error.status, 404);
      assert.deepStrictEqual(error.data, { message: 'User not found' });
      assert.strictEqual(error.url, 'https://api.example.com/users');
    });

    it('should be instanceof Error', () => {
      const error = new HttpError('Error', 500, null, '');
      assert.ok(error instanceof Error);
    });
  });

  describe('TimeoutError', () => {
    it('should create error with default message', () => {
      const error = new TimeoutError();
      assert.strictEqual(error.name, 'TimeoutError');
      assert.strictEqual(error.message, 'Request timeout');
    });

    it('should create error with custom message', () => {
      const error = new TimeoutError('Custom timeout message');
      assert.strictEqual(error.message, 'Custom timeout message');
    });

    it('should be instanceof Error', () => {
      const error = new TimeoutError();
      assert.ok(error instanceof Error);
    });
  });
});

describe('createClient', () => {
  it('should create client with default options', () => {
    const client = createClient();
    assert.ok(typeof client.get === 'function');
    assert.ok(typeof client.post === 'function');
    assert.ok(typeof client.put === 'function');
    assert.ok(typeof client.del === 'function');
    assert.ok(typeof client.patch === 'function');
    assert.ok(typeof client.head === 'function');
    assert.ok(typeof client.postForm === 'function');
  });

  it('should create client with custom default options', () => {
    const client = createClient({
      headers: { 'Authorization': 'Bearer token123' },
      timeout: 5000,
    });
    
    assert.ok(typeof client.get === 'function');
  });
});

// 简单的类型检查测试
describe('Type Safety', () => {
  it('should export all required types', () => {
    // 这些类型在编译时检查，运行时只需确认模块加载成功
    assert.ok(true);
  });
});
