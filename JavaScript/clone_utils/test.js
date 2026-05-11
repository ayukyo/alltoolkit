/**
 * Clone Utils Tests
 */

const assert = require('assert');
const {
  getType,
  shallowClone,
  deepClone,
  deepCompare,
  deepMerge,
  cloneJSON,
  cloneWithCustomizer,
  isDeepEqual,
  structuralClone,
  cloneWithDeps,
  clonePick,
  cloneOmit
} = require('./mod.js');

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (e) {
    console.log(`✗ ${name}`);
    console.log(`  Error: ${e.message}`);
    failed++;
  }
}

// ==================== getType Tests ====================

test('getType: null', () => {
  assert.strictEqual(getType(null), 'null');
});

test('getType: undefined', () => {
  assert.strictEqual(getType(undefined), 'undefined');
});

test('getType: number', () => {
  assert.strictEqual(getType(42), 'number');
});

test('getType: string', () => {
  assert.strictEqual(getType('hello'), 'string');
});

test('getType: boolean', () => {
  assert.strictEqual(getType(true), 'boolean');
});

test('getType: bigint', () => {
  assert.strictEqual(getType(123n), 'bigint');
});

test('getType: symbol', () => {
  assert.strictEqual(getType(Symbol('test')), 'symbol');
});

test('getType: function', () => {
  assert.strictEqual(getType(() => {}), 'function');
});

test('getType: array', () => {
  assert.strictEqual(getType([1, 2, 3]), 'array');
});

test('getType: object', () => {
  assert.strictEqual(getType({ a: 1 }), 'object');
});

test('getType: date', () => {
  assert.strictEqual(getType(new Date()), 'date');
});

test('getType: regexp', () => {
  assert.strictEqual(getType(/test/), 'regexp');
});

test('getType: map', () => {
  assert.strictEqual(getType(new Map()), 'map');
});

test('getType: set', () => {
  assert.strictEqual(getType(new Set()), 'set');
});

test('getType: error', () => {
  assert.strictEqual(getType(new Error()), 'error');
});

test('getType: arraybuffer', () => {
  assert.strictEqual(getType(new ArrayBuffer(8)), 'arraybuffer');
});

test('getType: typedarray', () => {
  assert.strictEqual(getType(new Uint8Array(8)), 'typedarray');
});

test('getType: dataview', () => {
  assert.strictEqual(getType(new DataView(new ArrayBuffer(8))), 'dataview');
});

// ==================== shallowClone Tests ====================

test('shallowClone: primitive values', () => {
  assert.strictEqual(shallowClone(42), 42);
  assert.strictEqual(shallowClone('hello'), 'hello');
  assert.strictEqual(shallowClone(true), true);
  assert.strictEqual(shallowClone(null), null);
  assert.strictEqual(shallowClone(undefined), undefined);
});

test('shallowClone: array', () => {
  const arr = [1, 2, 3];
  const cloned = shallowClone(arr);
  assert.notStrictEqual(cloned, arr);
  assert.deepStrictEqual(cloned, arr);
  arr[0] = 99;
  assert.strictEqual(cloned[0], 1); // 浅克隆，不影响原数组
});

test('shallowClone: object', () => {
  const obj = { a: 1, b: 2 };
  const cloned = shallowClone(obj);
  assert.notStrictEqual(cloned, obj);
  assert.deepStrictEqual(cloned, obj);
});

test('shallowClone: date', () => {
  const date = new Date('2024-01-01');
  const cloned = shallowClone(date);
  assert.notStrictEqual(cloned, date);
  assert.strictEqual(cloned.getTime(), date.getTime());
});

test('shallowClone: regexp', () => {
  const re = /test/gi;
  const cloned = shallowClone(re);
  assert.notStrictEqual(cloned, re);
  assert.strictEqual(cloned.source, re.source);
  assert.strictEqual(cloned.flags, re.flags);
});

test('shallowClone: map', () => {
  const map = new Map([['a', 1], ['b', 2]]);
  const cloned = shallowClone(map);
  assert.notStrictEqual(cloned, map);
  assert.strictEqual(cloned.size, map.size);
  assert.strictEqual(cloned.get('a'), 1);
});

test('shallowClone: set', () => {
  const set = new Set([1, 2, 3]);
  const cloned = shallowClone(set);
  assert.notStrictEqual(cloned, set);
  assert.strictEqual(cloned.size, set.size);
});

test('shallowClone: error', () => {
  const err = new Error('test error');
  err.name = 'TestError';
  const cloned = shallowClone(err);
  assert.notStrictEqual(cloned, err);
  assert.strictEqual(cloned.message, 'test error');
  assert.strictEqual(cloned.name, 'TestError');
});

test('shallowClone: arraybuffer', () => {
  const buf = new ArrayBuffer(8);
  const cloned = shallowClone(buf);
  assert.notStrictEqual(cloned, buf);
  assert.strictEqual(cloned.byteLength, buf.byteLength);
});

test('shallowClone: typedarray', () => {
  const arr = new Uint8Array([1, 2, 3]);
  const cloned = shallowClone(arr);
  assert.notStrictEqual(cloned, arr);
  assert.strictEqual(cloned[0], 1);
});

// ==================== deepClone Tests ====================

test('deepClone: nested object', () => {
  const obj = { a: { b: { c: 1 } } };
  const cloned = deepClone(obj);
  assert.notStrictEqual(cloned, obj);
  assert.notStrictEqual(cloned.a, obj.a);
  assert.strictEqual(cloned.a.b.c, 1);
  obj.a.b.c = 99;
  assert.strictEqual(cloned.a.b.c, 1);
});

test('deepClone: nested array', () => {
  const arr = [[1, 2], [3, 4]];
  const cloned = deepClone(arr);
  assert.notStrictEqual(cloned, arr);
  assert.notStrictEqual(cloned[0], arr[0]);
  arr[0][0] = 99;
  assert.strictEqual(cloned[0][0], 1);
});

test('deepClone: circular reference', () => {
  const obj = { a: 1 };
  obj.self = obj;
  const cloned = deepClone(obj);
  assert.notStrictEqual(cloned, obj);
  assert.strictEqual(cloned.self, cloned);
});

test('deepClone: complex circular', () => {
  const a = { name: 'a' };
  const b = { name: 'b', ref: a };
  a.ref = b;
  const cloned = deepClone(a);
  assert.notStrictEqual(cloned, a);
  assert.strictEqual(cloned.ref.name, 'b');
  assert.strictEqual(cloned.ref.ref, cloned);
});

test('deepClone: date deep clone', () => {
  const obj = { date: new Date('2024-01-01') };
  const cloned = deepClone(obj);
  obj.date.setFullYear(2020);
  assert.strictEqual(cloned.date.getFullYear(), 2024);
});

test('deepClone: regexp with lastIndex', () => {
  const re = /test/g;
  re.lastIndex = 2;
  const cloned = deepClone(re);
  assert.strictEqual(cloned.lastIndex, 2);
});

test('deepClone: map with objects', () => {
  const key = { id: 1 };
  const map = new Map();
  map.set(key, { value: 'test' });
  const cloned = deepClone(map);
  assert.notStrictEqual(cloned, map);
  // 克隆后 key 是新的对象
  for (const [k, v] of cloned) {
    assert.notStrictEqual(k, key);
    assert.strictEqual(v.value, 'test');
  }
});

test('deepClone: set with objects', () => {
  const item = { id: 1 };
  const set = new Set([item]);
  const cloned = deepClone(set);
  assert.notStrictEqual(cloned, set);
  for (const v of cloned) {
    assert.notStrictEqual(v, item);
    assert.strictEqual(v.id, 1);
  }
});

test('deepClone: symbol properties', () => {
  const sym = Symbol('test');
  const obj = { [sym]: 'symbol value', a: 1 };
  const cloned = deepClone(obj);
  assert.strictEqual(cloned[sym], 'symbol value');
});

test('deepClone: depth limit', () => {
  const obj = { a: { b: { c: { d: 1 } } } };
  const cloned = deepClone(obj, { depth: 2 });
  // depth=2 时：
  // - obj (depth 0) 深克隆
  // - a (depth 1) 深克隆  
  // - b (depth 2) 到达限制，返回 shallowClone
  // shallowClone 创建新对象，但内部属性引用不变
  assert.notStrictEqual(cloned, obj);
  assert.notStrictEqual(cloned.a, obj.a);
  assert.notStrictEqual(cloned.a.b, obj.a.b);
  // b.c 是浅克隆的结果对象中的属性，保持原引用
  assert.strictEqual(cloned.a.b.c, obj.a.b.c);
});

test('deepClone: customizer', () => {
  const obj = { date: new Date('2024-01-01') };
  const cloned = deepClone(obj, {
    customizer: (val, type) => {
      if (type === 'date') return 'custom-date';
      return undefined;
    }
  });
  assert.strictEqual(cloned.date, 'custom-date');
});

test('deepClone: prototype preservation', () => {
  function Person(name) { this.name = name; }
  Person.prototype.greet = function() { return `Hi, ${this.name}`; };
  const obj = new Person('Alice');
  const cloned = deepClone(obj);
  assert.strictEqual(cloned.greet(), 'Hi, Alice');
});

// ==================== deepCompare Tests ====================

test('deepCompare: equal primitives', () => {
  const result = deepCompare(1, 1);
  assert.strictEqual(result.equal, true);
  assert.deepStrictEqual(result.differences, []);
});

test('deepCompare: different primitives', () => {
  const result = deepCompare(1, 2);
  assert.strictEqual(result.equal, false);
  assert.strictEqual(result.differences.length, 1);
});

test('deepCompare: NaN (non-strict)', () => {
  const result = deepCompare(NaN, NaN, { strict: false });
  assert.strictEqual(result.equal, true);
});

test('deepCompare: NaN (strict)', () => {
  const result = deepCompare(NaN, NaN, { strict: true });
  assert.strictEqual(result.equal, true); // Object.is(NaN, NaN) = true
});

test('deepCompare: -0 vs 0 (non-strict)', () => {
  const result = deepCompare(-0, 0, { strict: false });
  assert.strictEqual(result.equal, true);
});

test('deepCompare: -0 vs 0 (strict)', () => {
  const result = deepCompare(-0, 0, { strict: true });
  assert.strictEqual(result.equal, false); // Object.is(-0, 0) = false
});

test('deepCompare: equal objects', () => {
  const result = deepCompare({ a: 1, b: 2 }, { a: 1, b: 2 });
  assert.strictEqual(result.equal, true);
});

test('deepCompare: different objects', () => {
  const result = deepCompare({ a: 1, b: 2 }, { a: 1, b: 3 });
  assert.strictEqual(result.equal, false);
  assert.ok(result.differences[0].path.includes('b'));
});

test('deepCompare: missing key', () => {
  const result = deepCompare({ a: 1 }, { a: 1, b: 2 });
  assert.strictEqual(result.equal, false);
});

test('deepCompare: equal arrays', () => {
  const result = deepCompare([1, 2, 3], [1, 2, 3]);
  assert.strictEqual(result.equal, true);
});

test('deepCompare: different arrays', () => {
  const result = deepCompare([1, 2, 3], [1, 2, 4]);
  assert.strictEqual(result.equal, false);
});

test('deepCompare: array length difference', () => {
  const result = deepCompare([1, 2], [1, 2, 3]);
  assert.strictEqual(result.equal, false);
  assert.ok(result.differences.some(d => d.path.includes('length')));
});

test('deepCompare: equal dates', () => {
  const result = deepCompare(new Date('2024-01-01'), new Date('2024-01-01'));
  assert.strictEqual(result.equal, true);
});

test('deepCompare: different dates', () => {
  const result = deepCompare(new Date('2024-01-01'), new Date('2024-01-02'));
  assert.strictEqual(result.equal, false);
});

test('deepCompare: equal regexps', () => {
  const result = deepCompare(/test/gi, /test/gi);
  assert.strictEqual(result.equal, true);
});

test('deepCompare: different regexps', () => {
  const result = deepCompare(/test/gi, /test/g);
  assert.strictEqual(result.equal, false);
});

test('deepCompare: equal maps', () => {
  const map1 = new Map([['a', 1], ['b', 2]]);
  const map2 = new Map([['a', 1], ['b', 2]]);
  const result = deepCompare(map1, map2);
  assert.strictEqual(result.equal, true);
});

test('deepCompare: different maps', () => {
  const map1 = new Map([['a', 1]]);
  const map2 = new Map([['a', 2]]);
  const result = deepCompare(map1, map2);
  assert.strictEqual(result.equal, false);
});

test('deepCompare: equal sets', () => {
  const set1 = new Set([1, 2, 3]);
  const set2 = new Set([1, 2, 3]);
  const result = deepCompare(set1, set2);
  assert.strictEqual(result.equal, true);
});

test('deepCompare: different sets', () => {
  const set1 = new Set([1, 2]);
  const set2 = new Set([1, 3]);
  const result = deepCompare(set1, set2);
  assert.strictEqual(result.equal, false);
});

test('deepCompare: ignore functions', () => {
  const result = deepCompare({ a: () => 1 }, { a: () => 2 }, { ignoreFunctions: true });
  assert.strictEqual(result.equal, true);
});

test('deepCompare: symbol properties', () => {
  const sym = Symbol('test');
  const result = deepCompare({ [sym]: 1 }, { [sym]: 1 });
  assert.strictEqual(result.equal, true);
});

test('deepCompare: depth limit', () => {
  const obj = { a: { b: { c: 1 } } };
  const result = deepCompare(obj, { a: { b: { c: 2 } } }, { depth: 2 });
  assert.strictEqual(result.equal, true);
});

test('deepCompare: arraybuffer', () => {
  const buf1 = new Uint8Array([1, 2, 3]).buffer;
  const buf2 = new Uint8Array([1, 2, 3]).buffer;
  const result = deepCompare(buf1, buf2);
  assert.strictEqual(result.equal, true);
});

test('deepCompare: typedarray', () => {
  const arr1 = new Uint8Array([1, 2, 3]);
  const arr2 = new Uint8Array([1, 2, 3]);
  const result = deepCompare(arr1, arr2);
  assert.strictEqual(result.equal, true);
});

// ==================== deepMerge Tests ====================

test('deepMerge: basic merge', () => {
  const result = deepMerge({ a: 1 }, { b: 2 });
  assert.deepStrictEqual(result, { a: 1, b: 2 });
});

test('deepMerge: nested merge', () => {
  const result = deepMerge(
    { a: { x: 1, y: 2 } },
    { a: { y: 3, z: 4 } }
  );
  assert.deepStrictEqual(result, { a: { x: 1, y: 3, z: 4 } });
});

test('deepMerge: multiple sources', () => {
  const result = deepMerge({ a: 1 }, { b: 2 }, { c: 3 });
  assert.deepStrictEqual(result, { a: 1, b: 2, c: 3 });
});

test('deepMerge: array merge', () => {
  const result = deepMerge([1, 2, 3], [4, 5]);
  assert.deepStrictEqual(result, [4, 5, 3]);
});

test('deepMerge: null source', () => {
  const result = deepMerge({ a: 1 }, null);
  assert.deepStrictEqual(result, { a: 1 });
});

test('deepMerge: null target', () => {
  const result = deepMerge(null, { a: 1 });
  assert.deepStrictEqual(result, { a: 1 });
});

test('deepMerge: different types override', () => {
  const result = deepMerge({ a: 1 }, { a: 'string' });
  assert.strictEqual(result.a, 'string');
});

test('deepMerge: map merge', () => {
  const map1 = new Map([['a', 1]]);
  const map2 = new Map([['b', 2]]);
  const result = deepMerge(map1, map2);
  assert.strictEqual(result.size, 2);
  assert.strictEqual(result.get('a'), 1);
  assert.strictEqual(result.get('b'), 2);
});

test('deepMerge: set merge', () => {
  const set1 = new Set([1, 2]);
  const set2 = new Set([3, 4]);
  const result = deepMerge(set1, set2);
  assert.strictEqual(result.size, 2);
  assert.ok(result.has(3));
});

// ==================== cloneJSON Tests ====================

test('cloneJSON: basic object', () => {
  const obj = { a: 1, b: 'hello' };
  const cloned = cloneJSON(obj);
  assert.deepStrictEqual(cloned, obj);
  assert.notStrictEqual(cloned, obj);
});

test('cloneJSON: array', () => {
  const arr = [1, 2, 3];
  const cloned = cloneJSON(arr);
  assert.deepStrictEqual(cloned, arr);
  assert.notStrictEqual(cloned, arr);
});

test('cloneJSON: nested', () => {
  const obj = { a: { b: { c: 1 } } };
  const cloned = cloneJSON(obj);
  obj.a.b.c = 99;
  assert.strictEqual(cloned.a.b.c, 1);
});

test('cloneJSON: ignores undefined', () => {
  const obj = { a: 1, b: undefined };
  const cloned = cloneJSON(obj);
  assert.strictEqual(cloned.a, 1);
  assert.strictEqual('b' in cloned, false);
});

test('cloneJSON: ignores functions', () => {
  const obj = { a: 1, fn: () => {} };
  const cloned = cloneJSON(obj);
  assert.strictEqual(cloned.a, 1);
  assert.strictEqual('fn' in cloned, false);
});

test('cloneJSON: converts Date to string', () => {
  const obj = { date: new Date('2024-01-01') };
  const cloned = cloneJSON(obj);
  assert.strictEqual(typeof cloned.date, 'string');
});

// ==================== cloneWithCustomizer Tests ====================

test('cloneWithCustomizer: custom date handling', () => {
  const obj = { date: new Date('2024-01-01'), num: 42 };
  const cloned = cloneWithCustomizer(obj, {
    date: (d) => d.getTime()
  });
  assert.strictEqual(typeof cloned.date, 'number');
  assert.strictEqual(cloned.num, 42);
});

test('cloneWithCustomizer: custom error handling', () => {
  const obj = { err: new Error('test') };
  const cloned = cloneWithCustomizer(obj, {
    error: (e) => ({ message: e.message, name: e.name })
  });
  assert.strictEqual(cloned.err.message, 'test');
  assert.strictEqual(cloned.err.name, 'Error');
});

// ==================== isDeepEqual Tests ====================

test('isDeepEqual: equal objects', () => {
  assert.strictEqual(isDeepEqual({ a: 1 }, { a: 1 }), true);
});

test('isDeepEqual: different objects', () => {
  assert.strictEqual(isDeepEqual({ a: 1 }, { a: 2 }), false);
});

test('isDeepEqual: nested equality', () => {
  assert.strictEqual(
    isDeepEqual({ a: { b: [1, 2, 3] } }, { a: { b: [1, 2, 3] } }),
    true
  );
});

test('isDeepEqual: arrays', () => {
  assert.strictEqual(isDeepEqual([1, 2, 3], [1, 2, 3]), true);
  assert.strictEqual(isDeepEqual([1, 2], [1, 2, 3]), false);
});

// ==================== structuralClone Tests ====================

test('structuralClone: basic types', () => {
  const obj = { a: 1, b: 'hello' };
  const cloned = structuralClone(obj);
  assert.deepStrictEqual(cloned, obj);
  assert.notStrictEqual(cloned, obj);
});

test('structuralClone: date', () => {
  const date = new Date('2024-01-01');
  const cloned = structuralClone(date);
  assert.strictEqual(cloned.getTime(), date.getTime());
  assert.notStrictEqual(cloned, date);
});

test('structuralClone: map', () => {
  const map = new Map([['a', 1]]);
  const cloned = structuralClone(map);
  assert.strictEqual(cloned.size, 1);
  assert.strictEqual(cloned.get('a'), 1);
});

test('structuralClone: set', () => {
  const set = new Set([1, 2, 3]);
  const cloned = structuralClone(set);
  assert.strictEqual(cloned.size, 3);
});

// ==================== cloneWithDeps Tests ====================

test('cloneWithDeps: replace dependency', () => {
  const dep = { id: 1 };
  const obj = { a: dep, b: dep };
  const newDep = { id: 2 };
  const deps = new Map();
  deps.set(dep, newDep);
  
  const cloned = cloneWithDeps(obj, deps);
  assert.strictEqual(cloned.a, newDep);
  assert.strictEqual(cloned.b, newDep);
});

test('cloneWithDeps: no dependency', () => {
  const obj = { a: { id: 1 } };
  const cloned = cloneWithDeps(obj, new Map());
  assert.deepStrictEqual(cloned, obj);
  assert.notStrictEqual(cloned.a, obj.a);
});

// ==================== clonePick Tests ====================

test('clonePick: basic pick', () => {
  const obj = { a: 1, b: 2, c: 3 };
  const cloned = clonePick(obj, ['a', 'c']);
  assert.deepStrictEqual(cloned, { a: 1, c: 3 });
});

test('clonePick: non-existent keys', () => {
  const obj = { a: 1 };
  const cloned = clonePick(obj, ['a', 'b']);
  assert.deepStrictEqual(cloned, { a: 1 });
});

test('clonePick: deep clone picked values', () => {
  const obj = { a: { nested: 1 }, b: 2 };
  const cloned = clonePick(obj, ['a']);
  obj.a.nested = 99;
  assert.strictEqual(cloned.a.nested, 1);
});

test('clonePick: empty keys', () => {
  const obj = { a: 1 };
  const cloned = clonePick(obj, []);
  assert.deepStrictEqual(cloned, {});
});

// ==================== cloneOmit Tests ====================

test('cloneOmit: basic omit', () => {
  const obj = { a: 1, b: 2, c: 3 };
  const cloned = cloneOmit(obj, ['b']);
  assert.deepStrictEqual(cloned, { a: 1, c: 3 });
});

test('cloneOmit: non-existent keys', () => {
  const obj = { a: 1 };
  const cloned = cloneOmit(obj, ['b']);
  assert.deepStrictEqual(cloned, { a: 1 });
});

test('cloneOmit: deep clone remaining values', () => {
  const obj = { a: { nested: 1 }, b: 2 };
  const cloned = cloneOmit(obj, ['b']);
  obj.a.nested = 99;
  assert.strictEqual(cloned.a.nested, 1);
});

test('cloneOmit: empty keys', () => {
  const obj = { a: 1 };
  const cloned = cloneOmit(obj, []);
  assert.deepStrictEqual(cloned, { a: 1 });
});

test('cloneOmit: symbol properties', () => {
  const sym = Symbol('test');
  const obj = { a: 1, [sym]: 'sym' };
  const cloned = cloneOmit(obj, [sym]);
  assert.strictEqual(cloned.a, 1);
  assert.strictEqual(sym in cloned, false);
});

// ==================== Summary ====================

console.log('\n' + '='.repeat(50));
console.log(`Tests: ${passed} passed, ${failed} failed`);
console.log('='.repeat(50));

if (failed > 0) {
  process.exit(1);
}