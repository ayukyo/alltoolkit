/**
 * Cache Utilities - 使用示例
 * 
 * 展示各种缓存的使用场景和方法
 */

const cacheUtils = require('./mod.js');

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

console.log('=== Cache Utilities Examples ===\n');

// ============================================================================
// 1. LRU Cache 示例 - 适合作为数据缓存
// ============================================================================

console.log('1. LRU Cache Example (图片缓存场景)');

const imageCache = new LRUCache(100); // 最多缓存 100 张图片

// 模拟缓存图片路径
imageCache.set('image1.jpg', '/path/to/image1.jpg');
imageCache.set('image2.jpg', '/path/to/image2.jpg');
imageCache.set('image3.jpg', '/path/to/image3.jpg');

console.log('缓存大小:', imageCache.size);
console.log('获取 image1.jpg:', imageCache.get('image1.jpg'));

// 当缓存超过容量时，最久未使用的会被淘汰
for (let i = 4; i <= 105; i++) {
  imageCache.set(`image${i}.jpg`, `/path/to/image${i}.jpg`);
}
console.log('添加更多后缓存大小:', imageCache.size); // 仍然是 100

console.log('缓存统计:', imageCache.getStats());

// ============================================================================
// 2. LFU Cache 示例 - 适合热门内容缓存
// ============================================================================

console.log('\n2. LFU Cache Example (热门文章缓存)');

const articleCache = new LFUCache(50); // 最多缓存 50 篇文章

// 缓存文章
articleCache.set('article-001', { title: '热门文章 A', views: 1000 });
articleCache.set('article-002', { title: '普通文章 B', views: 100 });
articleCache.set('article-003', { title: '冷门文章 C', views: 10 });

// 用户频繁访问热门文章
for (let i = 0; i < 10; i++) {
  articleCache.get('article-001'); // 热门文章频率增加到 11
}

// 用户偶尔访问普通文章
articleCache.get('article-002'); // 频率增加到 2

// 冷门文章没有被访问，频率保持 1

console.log('热门文章频率:', articleCache.get('article-001') ? '高' : '被淘汰');
console.log('普通文章频率:', articleCache.get('article-002') ? '中' : '被淘汰');

// 当需要淘汰时，冷门文章（频率最低）会被优先淘汰
console.log('缓存统计:', articleCache.getStats());

// ============================================================================
// 3. TTL Cache 示例 - 适合临时数据和 API 缓存
// ============================================================================

console.log('\n3. TTL Cache Example (API 响应缓存)');

const apiCache = new TTLCache({
  defaultTTL: 5000, // 默认 5 秒过期
  maxSize: 200,
  cleanupInterval: 1000 // 每秒清理过期条目
});

// 缓存 API 响应
apiCache.set('api/users', { users: ['Alice', 'Bob', 'Charlie'] });
apiCache.set('api/products', { products: ['Apple', 'Banana'] }, 10000); // 10 秒过期

console.log('用户 API 数据:', apiCache.get('api/users'));
console.log('剩余时间:', apiCache.getRemainingTTL('api/users'), 'ms');

// 检查过期情况
setTimeout(() => {
  console.log('5 秒后用户 API 是否存在:', apiCache.has('api/users') ? '存在' : '已过期');
  console.log('产品 API 是否存在:', apiCache.has('api/products') ? '存在' : '已过期');
  apiCache.stopCleanup(); // 停止自动清理
}, 5000);

// ============================================================================
// 4. Memory Cache 示例 - 通用内存缓存
// ============================================================================

console.log('\n4. Memory Cache Example (通用缓存)');

const generalCache = new MemoryCache({
  maxSize: 500,
  defaultTTL: 60000 // 默认 1 分钟过期
});

// 基本操作
generalCache.set('config', { theme: 'dark', language: 'zh-CN' });
generalCache.set('session', { userId: 123, token: 'abc123' }, 30000); // 30 秒过期

console.log('获取配置:', generalCache.get('config'));
console.log('获取不存在:', generalCache.get('nonexistent', 'default_value'));

// setNX - 如果不存在才设置
console.log('setNX 成功:', generalCache.setNX('new_key', 'new_value'));
console.log('setNX 失败:', generalCache.setNX('config', 'new_config')); // 已存在

// take - 获取并删除
console.log('take new_key:', generalCache.take('new_key'));
console.log('take 后还存在:', generalCache.has('new_key'));

// ============================================================================
// 5. Two-Level Cache 示例 - 高性能多级缓存
// ============================================================================

console.log('\n5. Two-Level Cache Example');

const twoLevelCache = new TwoLevelCache({
  l1Capacity: 50, // L1 快速缓存
  l2Capacity: 500, // L2 大容量缓存
  l2TTL: 300000 // L2 5 分钟过期
});

// 设置数据
twoLevelCache.set('key1', 'value1');
twoLevelCache.set('key2', 'value2');

// 第一次获取 - 从 L2 回填到 L1
console.log('第一次获取 key1:', twoLevelCache.get('key1'));

// 第二次获取 - 直接从 L1 获取
console.log('第二次获取 key1:', twoLevelCache.get('key1'));

console.log('两级缓存统计:', twoLevelCache.getStats());

// ============================================================================
// 6. Memoize 示例 - 函数结果缓存
// ============================================================================

console.log('\n6. Memoize Example (计算缓存)');

// 计算斐波那契数列（带缓存）
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

// 创建带缓存的版本
let fibCallCount = 0;
const cachedFib = memoize((n) => {
  fibCallCount++;
  if (n <= 1) return n;
  return cachedFib(n - 1) + cachedFib(n - 2);
}, { maxSize: 100 });

console.log('fib(10) =', cachedFib(10));
console.log('fib(20) =', cachedFib(20));
console.log('计算次数:', fibCallCount); // 远少于递归次数

// 缓存统计
console.log('Fib 缓存统计:', cachedFib.getStats());

// ============================================================================
// 7. Async Memoize 示例 - 异步函数缓存
// ============================================================================

console.log('\n7. Async Memoize Example (API 请求缓存)');

// 模拟 API 请求
async function fetchUserData(userId) {
  // 模拟网络延迟
  await new Promise(resolve => setTimeout(resolve, 1000));
  return { userId, name: `User ${userId}`, timestamp: Date.now() };
}

const cachedFetch = memoizeAsync(fetchUserData, {
  ttl: 10000, // 10 秒缓存
  maxSize: 50
});

// 测试异步缓存
(async () => {
  console.log('第一次请求...');
  const user1 = await cachedFetch(1);
  console.log('用户数据:', user1);
  
  console.log('第二次请求（应该立即返回）...');
  const user1Cached = await cachedFetch(1);
  console.log('缓存数据:', user1Cached);
  console.log('是否相同:', user1.timestamp === user1Cached.timestamp);
  
  console.log('缓存统计:', cachedFetch.getStats());
})();

// ============================================================================
// 8. Utility Functions 示例
// ============================================================================

console.log('\n8. Utility Functions Example');

const utilCache = new LRUCache(10);

// 批量设置
multiSet(utilCache, {
  'item1': { value: 100 },
  'item2': { value: 200 },
  'item3': { value: 300 }
});
console.log('批量设置后大小:', utilCache.size);

// 批量获取
const items = multiGet(utilCache, ['item1', 'item2', 'item4']);
console.log('批量获取:', items);

// 创建缓存键
const key1 = createCacheKey('user', 123, 'profile');
const key2 = createCacheKey({ type: 'config', id: 1 });
console.log('缓存键示例:', key1, key2);

// ============================================================================
// 等待异步示例完成
// ============================================================================

setTimeout(() => {
  console.log('\n=== 所有示例完成 ===');
}, 6000);