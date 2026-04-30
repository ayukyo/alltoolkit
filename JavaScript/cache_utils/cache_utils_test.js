/**
 * Cache Utilities Test Suite
 * 
 * 全面测试缓存工具模块的所有功能
 */

// 引入模块
const path = require('path');
const cacheUtils = require(path.join(__dirname, 'mod.js'));

const {
  LRUCache,
  LFUCache,
  TTLCache,
  MemoryCache,
  TwoLevelCache,
  memoize,
  memoizeAsync,
  createCacheKey,
  multiGet,
  multiSet
} = cacheUtils;

// 测试计数器
let passed = 0;
let failed = 0;

// 测试辅助函数
function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (error) {
    console.log(`✗ ${name}`);
    console.log(`  Error: ${error.message}`);
    failed++;
  }
}

function assertEqual(actual, expected, message = '') {
  if (actual !== expected) {
    throw new Error(`${message} Expected ${expected}, got ${actual}`);
  }
}

function assertDeepEqual(actual, expected, message = '') {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`${message} Expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

function assertTrue(value, message = '') {
  if (!value) {
    throw new Error(`${message} Expected true, got ${value}`);
  }
}

function assertFalse(value, message = '') {
  if (value) {
    throw new Error(`${message} Expected false, got ${value}`);
  }
}

function assertUndefined(value, message = '') {
  if (value !== undefined) {
    throw new Error(`${message} Expected undefined, got ${value}`);
  }
}

// ============================================================================
// LRU Cache Tests
// ============================================================================

console.log('\n=== LRU Cache Tests ===\n');

test('LRUCache: 创建实例', () => {
  const cache = new LRUCache(100);
  assertEqual(cache.size, 0);
  assertEqual(cache.capacity, 100);
});

test('LRUCache: 设置和获取', () => {
  const cache = new LRUCache(3);
  cache.set('a', 1);
  cache.set('b', 2);
  cache.set('c', 3);
  
  assertEqual(cache.size, 3);
  assertEqual(cache.get('a'), 1);
  assertEqual(cache.get('b'), 2);
  assertEqual(cache.get('c'), 3);
});

test('LRUCache: 容量淘汰', () => {
  const cache = new LRUCache(2);
  cache.set('a', 1);
  cache.set('b', 2);
  cache.set('c', 3); // 'a' 应该被淘汰
  
  assertEqual(cache.size, 2);
  assertUndefined(cache.get('a'));
  assertEqual(cache.get('b'), 2);
  assertEqual(cache.get('c'), 3);
});

test('LRUCache: 最近使用更新', () => {
  const cache = new LRUCache(3);
  cache.set('a', 1);
  cache.set('b', 2);
  cache.set('c', 3);
  
  // 访问 'a'，使其变为最新
  cache.get('a');
  
  // 添加新条目，'b' 应该被淘汰（因为它是最久未使用的）
  cache.set('d', 4);
  
  assertEqual(cache.size, 3);
  assertEqual(cache.get('a'), 1);
  assertUndefined(cache.get('b'));
  assertEqual(cache.get('c'), 3);
  assertEqual(cache.get('d'), 4);
});

test('LRUCache: 更新已存在的键', () => {
  const cache = new LRUCache(2);
  cache.set('a', 1);
  cache.set('b', 2);
  cache.set('a', 10); // 更新 'a'
  
  assertEqual(cache.size, 2);
  assertEqual(cache.get('a'), 10);
  assertEqual(cache.get('b'), 2);
});

test('LRUCache: has 方法', () => {
  const cache = new LRUCache(10);
  cache.set('a', 1);
  
  assertTrue(cache.has('a'));
  assertFalse(cache.has('b'));
});

test('LRUCache: delete 方法', () => {
  const cache = new LRUCache(10);
  cache.set('a', 1);
  
  assertTrue(cache.delete('a'));
  assertFalse(cache.has('a'));
  assertEqual(cache.size, 0);
});

test('LRUCache: clear 方法', () => {
  const cache = new LRUCache(10);
  cache.set('a', 1);
  cache.set('b', 2);
  cache.clear();
  
  assertEqual(cache.size, 0);
});

test('LRUCache: keys 和 values 方法', () => {
  const cache = new LRUCache(10);
  cache.set('a', 1);
  cache.set('b', 2);
  cache.set('c', 3);
  
  assertDeepEqual(cache.keys().sort(), ['a', 'b', 'c']);
  assertDeepEqual(cache.values().sort(), [1, 2, 3]);
});

test('LRUCache: 命中率统计', () => {
  const cache = new LRUCache(10);
  cache.set('a', 1);
  
  cache.get('a'); // hit
  cache.get('a'); // hit
  cache.get('b'); // miss
  
  const stats = cache.getStats();
  assertEqual(stats.hits, 2);
  assertEqual(stats.misses, 1);
  assertEqual(stats.hitRate, 2/3);
});

// ============================================================================
// LFU Cache Tests
// ============================================================================

console.log('\n=== LFU Cache Tests ===\n');

test('LFUCache: 创建实例', () => {
  const cache = new LFUCache(100);
  assertEqual(cache.size, 0);
  assertEqual(cache.capacity, 100);
});

test('LFUCache: 设置和获取', () => {
  const cache = new LFUCache(3);
  cache.set('a', 1);
  cache.set('b', 2);
  cache.set('c', 3);
  
  assertEqual(cache.size, 3);
  assertEqual(cache.get('a'), 1);
  assertEqual(cache.get('b'), 2);
  assertEqual(cache.get('c'), 3);
});

test('LFUCache: 频率淘汰', () => {
  const cache = new LFUCache(3);
  
  cache.set('a', 1);
  cache.set('b', 2);
  cache.set('c', 3);
  
  // 增加频率
  cache.get('a');
  cache.get('a');
  cache.get('b');
  
  // 'c' 频率最低（1），应该被淘汰
  cache.set('d', 4);
  
  assertEqual(cache.size, 3);
  assertEqual(cache.get('a'), 1);
  assertEqual(cache.get('b'), 2);
  assertUndefined(cache.get('c'));
  assertEqual(cache.get('d'), 4);
});

test('LFUCache: 频率相同时按时间淘汰', () => {
  const cache = new LFUCache(3);
  
  cache.set('a', 1);
  cache.set('b', 2);
  cache.set('c', 3);
  
  // 所有条目频率都是 1
  // 淘汰最早插入的 'a'
  cache.set('d', 4);
  
  assertUndefined(cache.get('a'));
});

test('LFUCache: 更新已存在的键', () => {
  const cache = new LFUCache(2);
  cache.set('a', 1);
  cache.set('b', 2);
  cache.set('a', 10);
  
  assertEqual(cache.get('a'), 10);
  assertEqual(cache.get('b'), 2);
});

test('LFUCache: has 方法', () => {
  const cache = new LFUCache(10);
  cache.set('a', 1);
  
  assertTrue(cache.has('a'));
  assertFalse(cache.has('b'));
});

test('LFUCache: delete 方法', () => {
  const cache = new LFUCache(10);
  cache.set('a', 1);
  
  assertTrue(cache.delete('a'));
  assertFalse(cache.has('a'));
});

test('LFUCache: clear 方法', () => {
  const cache = new LFUCache(10);
  cache.set('a', 1);
  cache.set('b', 2);
  cache.clear();
  
  assertEqual(cache.size, 0);
});

test('LFUCache: 命中率统计', () => {
  const cache = new LFUCache(10);
  cache.set('a', 1);
  
  cache.get('a'); // hit
  cache.get('b'); // miss
  
  const stats = cache.getStats();
  assertEqual(stats.hits, 1);
  assertEqual(stats.misses, 1);
  assertEqual(stats.hitRate, 0.5);
});

// ============================================================================
// TTL Cache Tests
// ============================================================================

console.log('\n=== TTL Cache Tests ===\n');

test('TTLCache: 创建实例', () => {
  const cache = new TTLCache({ defaultTTL: 1000 });
  assertEqual(cache.size, 0);
});

test('TTLCache: 设置和获取', () => {
  const cache = new TTLCache({ defaultTTL: 1000 });
  cache.set('a', 1);
  
  assertEqual(cache.get('a'), 1);
});

test('TTLCache: 过期时间', async () => {
  const cache = new TTLCache({ defaultTTL: 50 });
  cache.set('a', 1);
  
  assertEqual(cache.get('a'), 1);
  
  // 等待过期
  await new Promise(resolve => setTimeout(resolve, 100));
  
  assertUndefined(cache.get('a'));
});

test('TTLCache: 自定义 TTL', async () => {
  const cache = new TTLCache({ defaultTTL: 1000 });
  cache.set('a', 1, 50);
  
  assertEqual(cache.get('a'), 1);
  
  await new Promise(resolve => setTimeout(resolve, 100));
  
  assertUndefined(cache.get('a'));
});

test('TTLCache: 获取剩余时间', async () => {
  const cache = new TTLCache({ defaultTTL: 100 });
  cache.set('a', 1);
  
  const ttl1 = cache.getRemainingTTL('a');
  assertTrue(ttl1 > 0 && ttl1 <= 100);
  
  await new Promise(resolve => setTimeout(resolve, 50));
  
  const ttl2 = cache.getRemainingTTL('a');
  assertTrue(ttl2 < ttl1);
  
  await new Promise(resolve => setTimeout(resolve, 100));
  
  assertEqual(cache.getRemainingTTL('a'), 0);
});

test('TTLCache: 刷新过期时间', async () => {
  const cache = new TTLCache({ defaultTTL: 50 });
  cache.set('a', 1);
  
  await new Promise(resolve => setTimeout(resolve, 30));
  cache.refresh('a', 100);
  
  await new Promise(resolve => setTimeout(resolve, 50));
  
  // 应该还存在，因为刷新了 TTL
  assertEqual(cache.get('a'), 1);
});

test('TTLCache: has 方法检查过期', async () => {
  const cache = new TTLCache({ defaultTTL: 50 });
  cache.set('a', 1);
  
  assertTrue(cache.has('a'));
  
  await new Promise(resolve => setTimeout(resolve, 100));
  
  assertFalse(cache.has('a'));
});

test('TTLCache: 手动清理', async () => {
  const cache = new TTLCache({ defaultTTL: 50 });
  cache.set('a', 1);
  cache.set('b', 2);
  
  await new Promise(resolve => setTimeout(resolve, 100));
  
  // 在过期后手动清理
  const cleaned = cache.cleanup();
  
  assertEqual(cleaned, 2);
  assertEqual(cache.size, 0);
});

test('TTLCache: 最大容量限制', () => {
  const cache = new TTLCache({ maxSize: 2 });
  cache.set('a', 1);
  cache.set('b', 2);
  cache.set('c', 3); // 应该淘汰一个
  
  assertEqual(cache.size, 2);
});

test('TTLCache: 命中率统计', () => {
  const cache = new TTLCache({ defaultTTL: 1000 });
  cache.set('a', 1);
  
  cache.get('a'); // hit
  cache.get('b'); // miss
  
  const stats = cache.getStats();
  assertEqual(stats.hits, 1);
  assertEqual(stats.misses, 1);
});

// ============================================================================
// Memory Cache Tests
// ============================================================================

console.log('\n=== Memory Cache Tests ===\n');

test('MemoryCache: 创建实例', () => {
  const cache = new MemoryCache();
  assertEqual(cache.size, 0);
});

test('MemoryCache: 设置和获取', () => {
  const cache = new MemoryCache();
  cache.set('a', 1);
  
  assertEqual(cache.get('a'), 1);
});

test('MemoryCache: 默认值', () => {
  const cache = new MemoryCache();
  
  assertEqual(cache.get('a', 'default'), 'default');
});

test('MemoryCache: 过期时间', async () => {
  const cache = new MemoryCache({ defaultTTL: 50 });
  cache.set('a', 1);
  
  assertEqual(cache.get('a'), 1);
  
  await new Promise(resolve => setTimeout(resolve, 100));
  
  assertUndefined(cache.get('a'));
});

test('MemoryCache: setNX', () => {
  const cache = new MemoryCache();
  
  assertTrue(cache.setNX('a', 1));
  assertEqual(cache.get('a'), 1);
  assertFalse(cache.setNX('a', 2)); // 已存在
  assertEqual(cache.get('a'), 1);
});

test('MemoryCache: take', () => {
  const cache = new MemoryCache();
  cache.set('a', 1);
  
  assertEqual(cache.take('a'), 1);
  assertUndefined(cache.get('a'));
});

test('MemoryCache: has 方法', () => {
  const cache = new MemoryCache();
  cache.set('a', 1);
  
  assertTrue(cache.has('a'));
  assertFalse(cache.has('b'));
});

test('MemoryCache: forEach', () => {
  const cache = new MemoryCache();
  cache.set('a', 1);
  cache.set('b', 2);
  
  const result = [];
  cache.forEach((value, key) => {
    result.push({ key, value });
  });
  
  assertEqual(result.length, 2);
});

test('MemoryCache: 容量限制', () => {
  const cache = new MemoryCache({ maxSize: 2 });
  cache.set('a', 1);
  cache.set('b', 2);
  cache.set('c', 3);
  
  assertEqual(cache.size, 2);
  assertFalse(cache.has('a')); // 最老的被淘汰
});

// ============================================================================
// Two-Level Cache Tests
// ============================================================================

console.log('\n=== Two-Level Cache Tests ===\n');

test('TwoLevelCache: 创建实例', () => {
  const cache = new TwoLevelCache();
  assertEqual(cache.l1.size, 0);
  assertEqual(cache.l2.size, 0);
});

test('TwoLevelCache: L1 命中', () => {
  const cache = new TwoLevelCache();
  cache.set('a', 1);
  
  // 第一次获取会存入 L1
  cache.get('a');
  
  const stats = cache.getStats();
  assertEqual(stats.l1Hits, 1);
  assertEqual(stats.l2Hits, 0);
});

test('TwoLevelCache: L2 命中并回填', () => {
  const cache = new TwoLevelCache({ l1Capacity: 1 });
  cache.set('a', 1);
  cache.set('b', 2); // 淘汰 L1 中的 'a'
  
  // 从 L2 获取，应该回填到 L1
  const value = cache.get('a');
  
  assertEqual(value, 1);
  assertTrue(cache.l1.has('a'));
});

test('TwoLevelCache: delete 从两级删除', () => {
  const cache = new TwoLevelCache();
  cache.set('a', 1);
  
  cache.delete('a');
  
  assertFalse(cache.l1.has('a'));
  assertFalse(cache.l2.has('a'));
});

test('TwoLevelCache: clear 清空两级', () => {
  const cache = new TwoLevelCache();
  cache.set('a', 1);
  cache.set('b', 2);
  
  cache.clear();
  
  assertEqual(cache.l1.size, 0);
  assertEqual(cache.l2.size, 0);
});

// ============================================================================
// Memoize Tests
// ============================================================================

console.log('\n=== Memoize Tests ===\n');

test('memoize: 缓存函数结果', () => {
  let callCount = 0;
  const fn = (x) => {
    callCount++;
    return x * 2;
  };
  
  const memoized = memoize(fn);
  
  assertEqual(memoized(5), 10);
  assertEqual(callCount, 1);
  
  // 再次调用，应该使用缓存
  assertEqual(memoized(5), 10);
  assertEqual(callCount, 1); // 没有增加
});

test('memoize: 不同参数不同缓存', () => {
  let callCount = 0;
  const fn = (x) => {
    callCount++;
    return x * 2;
  };
  
  const memoized = memoize(fn);
  
  memoized(5);
  memoized(10);
  
  assertEqual(callCount, 2); // 两个不同的参数
});

test('memoize: 自定义键函数', () => {
  let callCount = 0;
  const fn = (a, b) => {
    callCount++;
    return a + b;
  };
  
  const memoized = memoize(fn, {
    keyFn: (a, b) => `${a}:${b}`
  });
  
  memoized(1, 2);
  memoized(1, 2);
  
  assertEqual(callCount, 1);
});

test('memoize: clear 方法', () => {
  let callCount = 0;
  const fn = (x) => {
    callCount++;
    return x;
  };
  
  const memoized = memoize(fn);
  
  memoized(1);
  assertEqual(callCount, 1);
  
  memoized.clear();
  memoized(1);
  assertEqual(callCount, 2); // 清除后重新计算
});

test('memoizeAsync: 缓存异步结果', async () => {
  let callCount = 0;
  const fn = async (x) => {
    callCount++;
    return x * 2;
  };
  
  const memoized = memoizeAsync(fn);
  
  const result1 = await memoized(5);
  const result2 = await memoized(5);
  
  assertEqual(result1, 10);
  assertEqual(result2, 10);
  assertEqual(callCount, 1);
});

test('memoizeAsync: 防止重复请求', async () => {
  let callCount = 0;
  const fn = async (x) => {
    callCount++;
    await new Promise(resolve => setTimeout(resolve, 50));
    return x * 2;
  };
  
  const memoized = memoizeAsync(fn);
  
  // 同时发起多个请求
  const [r1, r2, r3] = await Promise.all([
    memoized(5),
    memoized(5),
    memoized(5)
  ]);
  
  assertEqual(r1, 10);
  assertEqual(r2, 10);
  assertEqual(r3, 10);
  assertEqual(callCount, 1); // 只调用一次
});

// ============================================================================
// Utility Functions Tests
// ============================================================================

console.log('\n=== Utility Functions Tests ===\n');

test('createCacheKey: 基本类型', () => {
  assertEqual(createCacheKey('a', 'b'), 'a:b');
  assertEqual(createCacheKey(1, 2), '1:2');
  assertEqual(createCacheKey(null), 'null');
  assertEqual(createCacheKey(undefined), 'undefined');
});

test('createCacheKey: 对象类型', () => {
  const key = createCacheKey({ a: 1 });
  assertTrue(key.includes('a'));
  assertTrue(key.includes('1'));
});

test('multiGet: 批量获取', () => {
  const cache = new LRUCache(10);
  cache.set('a', 1);
  cache.set('b', 2);
  cache.set('c', 3);
  
  const result = multiGet(cache, ['a', 'b', 'd']);
  
  assertEqual(result.a, 1);
  assertEqual(result.b, 2);
  assertUndefined(result.d);
});

test('multiSet: 批量设置', () => {
  const cache = new LRUCache(10);
  
  multiSet(cache, { a: 1, b: 2, c: 3 });
  
  assertEqual(cache.get('a'), 1);
  assertEqual(cache.get('b'), 2);
  assertEqual(cache.get('c'), 3);
});

test('multiSet: 带 TTL', async () => {
  const cache = new TTLCache({ defaultTTL: 1000 });
  
  multiSet(cache, { a: 1, b: 2 }, 50);
  
  assertEqual(cache.get('a'), 1);
  
  await new Promise(resolve => setTimeout(resolve, 100));
  
  assertUndefined(cache.get('a'));
});

// ============================================================================
// 边界情况测试
// ============================================================================

console.log('\n=== Edge Cases Tests ===\n');

test('LRUCache: 容量为 1', () => {
  const cache = new LRUCache(1);
  cache.set('a', 1);
  cache.set('b', 2);
  
  assertUndefined(cache.get('a'));
  assertEqual(cache.get('b'), 2);
});

test('LRUCache: 更新不增加大小', () => {
  const cache = new LRUCache(2);
  cache.set('a', 1);
  cache.set('a', 10);
  cache.set('b', 2);
  
  assertEqual(cache.size, 2);
});

test('LFUCache: 容量为 1', () => {
  const cache = new LFUCache(1);
  cache.set('a', 1);
  cache.set('b', 2);
  
  assertUndefined(cache.get('a'));
  assertEqual(cache.get('b'), 2);
});

test('TTLCache: TTL 为 0 表示永不过期', async () => {
  const cache = new TTLCache({ defaultTTL: 0 });
  cache.set('a', 1);
  
  await new Promise(resolve => setTimeout(resolve, 50));
  
  assertEqual(cache.get('a'), 1);
});

test('MemoryCache: 空缓存操作', () => {
  const cache = new MemoryCache();
  
  assertUndefined(cache.get('a'));
  assertFalse(cache.has('a'));
  assertFalse(cache.delete('a'));
});

// ============================================================================
// 输出结果
// ============================================================================

console.log('\n========================================');
console.log(`Total Tests: ${passed + failed}`);
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
console.log('========================================\n');

if (failed > 0) {
  process.exit(1);
}