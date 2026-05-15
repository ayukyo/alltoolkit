/**
 * Pagination Utilities 测试
 */

const assert = require('assert');
const {
  PaginationType,
  OffsetPaginator,
  CursorPaginator,
  KeysetPaginator,
  InfiniteScrollPaginator,
  Pagination,
  paginateOffset,
  paginateCursor,
  paginateInfinite,
  pageRange,
  createPageMetadata,
  createCursorMetadata,
  createPaginatedResult
} = require('./mod.js');

// 测试数据
const createTestItems = (count = 100) => 
  Array.from({ length: count }, (_, i) => ({ id: i + 1, name: `Item-${i + 1}` }));

const createSimpleItems = (count = 100) => 
  Array.from({ length: count }, (_, i) => `Item-${i + 1}`);

// 颜色输出
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  reset: '\x1b[0m'
};

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`${colors.green}✓${colors.reset} ${name}`);
    passed++;
  } catch (error) {
    console.log(`${colors.red}✗${colors.reset} ${name}`);
    console.log(`  ${error.message}`);
    failed++;
  }
}

// ==================== OffsetPaginator 测试 ====================

console.log('\n=== OffsetPaginator 测试 ===\n');

test('OffsetPaginator: 基本分页', () => {
  const items = createSimpleItems(100);
  const paginator = new OffsetPaginator();
  const result = paginator.paginate(items, 1, 10);
  
  assert.strictEqual(result.paginationType, PaginationType.OFFSET);
  assert.strictEqual(result.items.length, 10);
  assert.strictEqual(result.items[0], 'Item-1');
  assert.strictEqual(result.metadata.currentPage, 1);
  assert.strictEqual(result.metadata.totalPages, 10);
  assert.strictEqual(result.metadata.totalItems, 100);
  assert.strictEqual(result.metadata.hasPrevious, false);
  assert.strictEqual(result.metadata.hasNext, true);
});

test('OffsetPaginator: 中间页', () => {
  const items = createSimpleItems(100);
  const paginator = new OffsetPaginator();
  const result = paginator.paginate(items, 5, 10);
  
  assert.strictEqual(result.items[0], 'Item-41');
  assert.strictEqual(result.items[9], 'Item-50');
  assert.strictEqual(result.metadata.currentPage, 5);
  assert.strictEqual(result.metadata.hasPrevious, true);
  assert.strictEqual(result.metadata.hasNext, true);
  assert.strictEqual(result.metadata.previousPage, 4);
  assert.strictEqual(result.metadata.nextPage, 6);
});

test('OffsetPaginator: 最后一页', () => {
  const items = createSimpleItems(100);
  const paginator = new OffsetPaginator();
  const result = paginator.paginate(items, 10, 10);
  
  assert.strictEqual(result.items[0], 'Item-91');
  assert.strictEqual(result.items[9], 'Item-100');
  assert.strictEqual(result.metadata.currentPage, 10);
  assert.strictEqual(result.metadata.hasNext, false);
});

test('OffsetPaginator: 空数组', () => {
  const paginator = new OffsetPaginator();
  const result = paginator.paginate([], 1, 10);
  
  assert.strictEqual(result.items.length, 0);
  assert.strictEqual(result.metadata.totalPages, 1);
  assert.strictEqual(result.metadata.totalItems, 0);
});

test('OffsetPaginator: 单页数据', () => {
  const items = createSimpleItems(5);
  const paginator = new OffsetPaginator();
  const result = paginator.paginate(items, 1, 10);
  
  assert.strictEqual(result.items.length, 5);
  assert.strictEqual(result.metadata.totalPages, 1);
  assert.strictEqual(result.metadata.hasPrevious, false);
  assert.strictEqual(result.metadata.hasNext, false);
});

test('OffsetPaginator: 边界页码处理', () => {
  const items = createSimpleItems(100);
  const paginator = new OffsetPaginator();
  
  // 页码小于 1
  const result1 = paginator.paginate(items, 0, 10);
  assert.strictEqual(result1.metadata.currentPage, 1);
  
  // 页码大于总页数
  const result2 = paginator.paginate(items, 100, 10);
  assert.strictEqual(result2.metadata.currentPage, 10);
});

test('OffsetPaginator: getOffsetLimit', () => {
  const paginator = new OffsetPaginator();
  const { offset, limit } = paginator.getOffsetLimit(3, 10);
  
  assert.strictEqual(offset, 20);
  assert.strictEqual(limit, 10);
});

test('OffsetPaginator: calculatePages', () => {
  const paginator = new OffsetPaginator();
  
  assert.strictEqual(paginator.calculatePages(100, 10), 10);
  assert.strictEqual(paginator.calculatePages(95, 10), 10);
  assert.strictEqual(paginator.calculatePages(0, 10), 1);
  assert.strictEqual(paginator.calculatePages(5, 10), 1);
});

test('OffsetPaginator: 自定义配置', () => {
  const paginator = new OffsetPaginator({ 
    itemsPerPage: 5,
    maxItemsPerPage: 10,
    minItemsPerPage: 2
  });
  
  const items = createSimpleItems(100);
  
  // 使用默认值
  const result1 = paginator.paginate(items, 1);
  assert.strictEqual(result1.items.length, 5);
  
  // 超过最大值
  const result2 = paginator.paginate(items, 1, 20);
  assert.strictEqual(result2.items.length, 10);
  
  // 低于最小值
  const result3 = paginator.paginate(items, 1, 1);
  assert.strictEqual(result3.items.length, 2);
});

test('OffsetPaginator: startIndex 和 endIndex', () => {
  const items = createSimpleItems(100);
  const paginator = new OffsetPaginator();
  const result = paginator.paginate(items, 3, 10);
  
  assert.strictEqual(result.metadata.startIndex, 21);
  assert.strictEqual(result.metadata.endIndex, 30);
});

// ==================== CursorPaginator 测试 ====================

console.log('\n=== CursorPaginator 测试 ===\n');

test('CursorPaginator: 第一页', () => {
  const items = createSimpleItems(100);
  const paginator = new CursorPaginator();
  const result = paginator.getFirstPage(items, 10);
  
  assert.strictEqual(result.paginationType, PaginationType.CURSOR);
  assert.strictEqual(result.items.length, 10);
  assert.strictEqual(result.items[0], 'Item-1');
  assert.strictEqual(result.metadata.hasMore, true);
  assert.strictEqual(result.metadata.cursor, null);
  assert.ok(result.metadata.nextCursor);
});

test('CursorPaginator: 下一页', () => {
  const items = createSimpleItems(100);
  const paginator = new CursorPaginator();
  
  // 获取第一页
  const result1 = paginator.getFirstPage(items, 10);
  assert.strictEqual(result1.items[0], 'Item-1');
  
  // 使用游标获取下一页
  const result2 = paginator.paginate(items, result1.metadata.nextCursor, 10);
  assert.strictEqual(result2.items[0], 'Item-11');
  assert.strictEqual(result2.items[9], 'Item-20');
});

test('CursorPaginator: 最后一页', () => {
  const items = createSimpleItems(95);
  const paginator = new CursorPaginator({ limit: 10 });
  
  // 一直翻到最后一页
  let cursor = null;
  let result;
  let iterations = 0;
  
  do {
    result = paginator.paginate(items, cursor, 10);
    cursor = result.metadata.nextCursor;
    iterations++;
  } while (result.metadata.hasMore);
  
  assert.ok(iterations >= 9);
  assert.strictEqual(result.metadata.hasMore, false);
  assert.strictEqual(result.metadata.nextCursor, null);
});

test('CursorPaginator: 游标编码解码', () => {
  const paginator = new CursorPaginator();
  
  const encoded = paginator.encodeCursor(50, 'next');
  assert.ok(typeof encoded === 'string');
  
  const decoded = paginator.decodeCursor(encoded);
  assert.strictEqual(decoded.index, 50);
  assert.strictEqual(decoded.direction, 'next');
});

test('CursorPaginator: 向后翻页', () => {
  const items = createSimpleItems(100);
  const paginator = new CursorPaginator();
  
  // 先前进两页
  const result1 = paginator.paginate(items, null, 10, 'next');
  const result2 = paginator.paginate(items, result1.metadata.nextCursor, 10, 'next');
  
  assert.strictEqual(result2.items[0], 'Item-11');
  
  // 然后向后翻页
  const result3 = paginator.paginate(items, result2.metadata.previousCursor, 10, 'previous');
  assert.strictEqual(result3.items[0], 'Item-1');
});

test('CursorPaginator: 空数组', () => {
  const paginator = new CursorPaginator();
  const result = paginator.paginate([], null, 10);
  
  assert.strictEqual(result.items.length, 0);
  assert.strictEqual(result.metadata.hasMore, false);
});

// ==================== KeysetPaginator 测试 ====================

console.log('\n=== KeysetPaginator 测试 ===\n');

test('KeysetPaginator: 基本分页', () => {
  const items = createTestItems(100);
  const paginator = new KeysetPaginator({ keyField: 'id' });
  const result = paginator.paginate(items, null, 10);
  
  assert.strictEqual(result.paginationType, PaginationType.KEYSET);
  assert.strictEqual(result.items.length, 10);
  assert.strictEqual(result.items[0].id, 1);
  assert.strictEqual(result.items[9].id, 10);
  assert.strictEqual(result.metadata.hasMore, true);
});

test('KeysetPaginator: 使用游标', () => {
  const items = createTestItems(100);
  const paginator = new KeysetPaginator({ keyField: 'id' });
  
  // 第一页
  const result1 = paginator.paginate(items, null, 10);
  
  // 使用游标获取下一页
  const result2 = paginator.paginate(items, result1.metadata.nextCursor, 10);
  assert.strictEqual(result2.items[0].id, 11);
  assert.strictEqual(result2.items[9].id, 20);
});

test('KeysetPaginator: 自定义键提取器', () => {
  const items = [
    { code: 'A', value: 1 },
    { code: 'B', value: 2 },
    { code: 'C', value: 3 }
  ];
  
  const paginator = new KeysetPaginator({
    keyExtractor: (item) => item.code
  });
  
  const result = paginator.paginate(items, null, 2);
  assert.strictEqual(result.items.length, 2);
  assert.strictEqual(result.items[0].code, 'A');
  assert.strictEqual(result.items[1].code, 'B');
});

test('KeysetPaginator: 降序排序', () => {
  const items = createTestItems(100).reverse(); // 降序
  const paginator = new KeysetPaginator({ keyField: 'id' });
  
  const result1 = paginator.paginate(items, null, 10, true);
  assert.strictEqual(result1.items[0].id, 100);
  
  const result2 = paginator.paginate(items, result1.metadata.nextCursor, 10, true);
  assert.strictEqual(result2.items[0].id, 90);
});

test('KeysetPaginator: 游标编码解码', () => {
  const paginator = new KeysetPaginator();
  
  const cursor = paginator.encodeCursor(42);
  const decoded = paginator.decodeCursor(cursor);
  
  assert.strictEqual(decoded, 42);
});

// ==================== InfiniteScrollPaginator 测试 ====================

console.log('\n=== InfiniteScrollPaginator 测试 ===\n');

test('InfiniteScrollPaginator: 基本分页', () => {
  const items = createSimpleItems(100);
  const paginator = new InfiniteScrollPaginator();
  const result = paginator.paginate(items, 0, 10);
  
  assert.strictEqual(result.paginationType, PaginationType.INFINITE);
  assert.strictEqual(result.items.length, 10);
  assert.strictEqual(result.items[0], 'Item-1');
  assert.strictEqual(result.metadata.hasMore, true);
});

test('InfiniteScrollPaginator: 连续加载', () => {
  const items = createSimpleItems(100);
  const paginator = new InfiniteScrollPaginator();
  
  // 首批
  const result1 = paginator.paginate(items, 0, 20);
  assert.strictEqual(result1.items[0], 'Item-1');
  assert.strictEqual(result1.items[19], 'Item-20');
  
  // 第二批
  const result2 = paginator.paginate(items, 20, 20);
  assert.strictEqual(result2.items[0], 'Item-21');
  assert.strictEqual(result2.items[19], 'Item-40');
  
  // 第三批
  const result3 = paginator.paginate(items, 40, 20);
  assert.strictEqual(result3.items[0], 'Item-41');
});

test('InfiniteScrollPaginator: 加载状态', () => {
  const paginator = new InfiniteScrollPaginator({ preloadThreshold: 10 });
  
  const state1 = paginator.getLoadState(100, 80);
  assert.strictEqual(state1.total, 100);
  assert.strictEqual(state1.loaded, 80);
  assert.strictEqual(state1.remaining, 20);
  assert.strictEqual(state1.progress, 0.8);
  assert.strictEqual(state1.shouldPreload, false);
  assert.strictEqual(state1.isComplete, false);
  
  const state2 = paginator.getLoadState(100, 95);
  assert.strictEqual(state2.shouldPreload, true);
  
  const state3 = paginator.getLoadState(100, 100);
  assert.strictEqual(state3.isComplete, true);
});

test('InfiniteScrollPaginator: 自定义配置', () => {
  const items = createSimpleItems(50);
  const paginator = new InfiniteScrollPaginator({
    batchSize: 5,
    maxBatchSize: 10,
    preloadThreshold: 3
  });
  
  const result = paginator.paginate(items, 0);
  assert.strictEqual(result.items.length, 5);
  assert.strictEqual(result.metadata.limit, 5);
});

// ==================== Pagination 静态方法测试 ====================

console.log('\n=== Pagination 静态方法测试 ===\n');

test('Pagination.offset: 便捷方法', () => {
  const items = createSimpleItems(100);
  const result = Pagination.offset(items, 3, 15);
  
  assert.strictEqual(result.items.length, 15);
  assert.strictEqual(result.metadata.currentPage, 3);
  assert.strictEqual(result.paginationType, PaginationType.OFFSET);
});

test('Pagination.cursor: 便捷方法', () => {
  const items = createSimpleItems(100);
  const result = Pagination.cursor(items, null, 15);
  
  assert.strictEqual(result.items.length, 15);
  assert.strictEqual(result.paginationType, PaginationType.CURSOR);
});

test('Pagination.keyset: 便捷方法', () => {
  const items = createTestItems(100);
  const result = Pagination.keyset(items, null, 15, 'id');
  
  assert.strictEqual(result.items.length, 15);
  assert.strictEqual(result.paginationType, PaginationType.KEYSET);
});

test('Pagination.infinite: 便捷方法', () => {
  const items = createSimpleItems(100);
  const result = Pagination.infinite(items, 0, 15);
  
  assert.strictEqual(result.items.length, 15);
  assert.strictEqual(result.paginationType, PaginationType.INFINITE);
});

test('Pagination.calculatePageRange: 基本计算', () => {
  // 中间页
  assert.deepStrictEqual(
    Pagination.calculatePageRange(5, 20, 7),
    [2, 3, 4, 5, 6, 7, 8]
  );
  
  // 开头
  assert.deepStrictEqual(
    Pagination.calculatePageRange(1, 20, 7),
    [1, 2, 3, 4, 5, 6, 7]
  );
  
  // 结尾
  assert.deepStrictEqual(
    Pagination.calculatePageRange(20, 20, 7),
    [14, 15, 16, 17, 18, 19, 20]
  );
});

test('Pagination.calculatePageRange: 边界情况', () => {
  // 总页数小于显示数
  assert.deepStrictEqual(
    Pagination.calculatePageRange(2, 5, 7),
    [1, 2, 3, 4, 5]
  );
  
  // 单页
  assert.deepStrictEqual(
    Pagination.calculatePageRange(1, 1, 7),
    [1]
  );
  
  // 无效输入
  assert.deepStrictEqual(
    Pagination.calculatePageRange(0, 10, 7),
    []
  );
});

test('Pagination.generateLinks: 生成链接', () => {
  const links = Pagination.generateLinks('/api/items', 5, 10);
  
  assert.strictEqual(links.first, '/api/items?page=1');
  assert.strictEqual(links.last, '/api/items?page=10');
  assert.strictEqual(links.prev, '/api/items?page=4');
  assert.strictEqual(links.next, '/api/items?page=6');
  assert.strictEqual(links.self, '/api/items?page=5');
});

test('Pagination.generateLinks: 边界情况', () => {
  // 第一页
  const links1 = Pagination.generateLinks('/api/items', 1, 10);
  assert.strictEqual(links1.prev, undefined);
  assert.ok(links1.next);
  
  // 最后一页
  const links2 = Pagination.generateLinks('/api/items', 10, 10);
  assert.ok(links2.prev);
  assert.strictEqual(links2.next, undefined);
  
  // 无效输入
  const links3 = Pagination.generateLinks('/api/items', 0, 10);
  assert.deepStrictEqual(links3, {});
});

test('Pagination.generateHeaderLinks: HTTP Link Header', () => {
  const header = Pagination.generateHeaderLinks('/api/items', 5, 10);
  
  assert.ok(header.includes('rel="first"'));
  assert.ok(header.includes('rel="last"'));
  assert.ok(header.includes('rel="prev"'));
  assert.ok(header.includes('rel="next"'));
  assert.ok(header.includes('rel="self"'));
});

// ==================== 便捷函数测试 ====================

console.log('\n=== 便捷函数测试 ===\n');

test('paginateOffset: 便捷函数', () => {
  const items = createSimpleItems(50);
  const result = paginateOffset(items, 2, 10);
  
  assert.strictEqual(result.items[0], 'Item-11');
  assert.strictEqual(result.metadata.currentPage, 2);
});

test('paginateCursor: 便捷函数', () => {
  const items = createSimpleItems(50);
  const result = paginateCursor(items, null, 10);
  
  assert.strictEqual(result.items[0], 'Item-1');
  assert.strictEqual(result.metadata.limit, 10);
});

test('paginateInfinite: 便捷函数', () => {
  const items = createSimpleItems(50);
  const result = paginateInfinite(items, 0, 10);
  
  assert.strictEqual(result.items[0], 'Item-1');
  assert.strictEqual(result.metadata.limit, 10);
});

test('pageRange: 便捷函数', () => {
  const range = pageRange(5, 20, 7);
  
  assert.deepStrictEqual(range, [2, 3, 4, 5, 6, 7, 8]);
});

// ==================== 元数据工厂函数测试 ====================

console.log('\n=== 元数据工厂函数测试 ===\n');

test('createPageMetadata: 创建分页元数据', () => {
  const metadata = createPageMetadata({
    currentPage: 3,
    totalPages: 10,
    totalItems: 100,
    itemsPerPage: 10,
    hasPrevious: true,
    hasNext: true
  });
  
  assert.strictEqual(metadata.currentPage, 3);
  assert.strictEqual(metadata.totalPages, 10);
  assert.ok(typeof metadata.toJSON === 'function');
});

test('createCursorMetadata: 创建游标元数据', () => {
  const metadata = createCursorMetadata({
    cursor: 'abc123',
    nextCursor: 'def456',
    hasMore: true,
    limit: 20
  });
  
  assert.strictEqual(metadata.cursor, 'abc123');
  assert.strictEqual(metadata.nextCursor, 'def456');
  assert.strictEqual(metadata.hasMore, true);
  assert.ok(typeof metadata.toJSON === 'function');
});

test('createPaginatedResult: 创建分页结果', () => {
  const items = [1, 2, 3];
  const metadata = createPageMetadata({ currentPage: 1 });
  const result = createPaginatedResult(items, metadata, PaginationType.OFFSET);
  
  assert.deepStrictEqual(result.items, items);
  assert.strictEqual(result.paginationType, PaginationType.OFFSET);
  assert.ok(typeof result.toJSON === 'function');
  
  const json = result.toJSON();
  assert.ok(json.items);
  assert.ok(json.pagination);
  assert.strictEqual(json.type, 'offset');
});

// ==================== 输出结果 ====================

console.log('\n' + '='.repeat(50));
console.log(`测试结果: ${colors.green}${passed} 通过${colors.reset}, ${colors.red}${failed} 失败${colors.reset}`);
console.log('='.repeat(50) + '\n');

process.exit(failed > 0 ? 1 : 0);