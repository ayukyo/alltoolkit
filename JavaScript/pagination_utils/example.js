/**
 * Pagination Utilities 使用示例
 */

const {
  OffsetPaginator,
  CursorPaginator,
  KeysetPaginator,
  InfiniteScrollPaginator,
  Pagination,
  paginateOffset,
  paginateCursor,
  paginateInfinite,
  pageRange
} = require('./mod.js');

// 创建测试数据
const createItems = (count = 100) => 
  Array.from({ length: count }, (_, i) => ({ id: i + 1, name: `Item-${i + 1}`, value: Math.random() }));

const simpleItems = Array.from({ length: 100 }, (_, i) => `Item-${i + 1}`);

console.log('=== Pagination Utilities 使用示例 ===\n');

// ==================== 1. 基于偏移量的分页 ====================

console.log('--- 1. 基于偏移量的分页 (Offset Pagination) ---\n');

// 创建分页器
const offsetPaginator = new OffsetPaginator({ itemsPerPage: 10 });

// 对数据进行分页
const items = createItems(100);
const page3 = offsetPaginator.paginate(items, 3, 10);

console.log('第 3 页数据:');
console.log(page3.items.map(item => item.name).join(', '));

console.log('\n分页元数据:');
console.log(JSON.stringify(page3.metadata.toJSON(), null, 2));

// 计算总页数
const totalPages = offsetPaginator.calculatePages(1000, 10);
console.log(`\n1000 条数据，每页 10 条，共 ${totalPages} 页`);

// 获取 SQL 查询用的 OFFSET 和 LIMIT
const { offset, limit } = offsetPaginator.getOffsetLimit(5, 20);
console.log(`\n第 5 页的 SQL: OFFSET ${offset}, LIMIT ${limit}`);

// ==================== 2. 基于游标的分页 ====================

console.log('\n--- 2. 基于游标的分页 (Cursor Pagination) ---\n');

const cursorPaginator = new CursorPaginator({ limit: 10 });

// 获取第一页
let cursorResult = cursorPaginator.getFirstPage(simpleItems, 10);

console.log('第一页数据:');
console.log(cursorResult.items.slice(0, 3).join(', ') + ' ...');
console.log(`游标: ${cursorResult.metadata.nextCursor}`);

// 使用游标获取下一页
const nextCursor = cursorResult.metadata.nextCursor;
cursorResult = cursorPaginator.paginate(simpleItems, nextCursor, 10);

console.log('\n第二页数据:');
console.log(cursorResult.items.slice(0, 3).join(', ') + ' ...');
console.log(`还有更多: ${cursorResult.metadata.hasMore}`);

// 继续翻页直到结束
let iterations = 0;
let currentCursor = null;
cursorResult = cursorPaginator.paginate(simpleItems, currentCursor, 20);

while (cursorResult.metadata.hasMore && iterations < 5) {
  console.log(`\n批次 ${iterations + 1}: ${cursorResult.items[0]} - ${cursorResult.items[cursorResult.items.length - 1]}`);
  currentCursor = cursorResult.metadata.nextCursor;
  cursorResult = cursorPaginator.paginate(simpleItems, currentCursor, 20);
  iterations++;
}

// ==================== 3. 基于键集的分页 ====================

console.log('\n--- 3. 基于键集的分页 (Keyset Pagination) ---\n');

const keysetItems = createItems(100);
const keysetPaginator = new KeysetPaginator({ keyField: 'id', limit: 15 });

// 第一页
const keysetResult1 = keysetPaginator.paginate(keysetItems, null, 15);

console.log('第一页数据 (按 id 排序):');
console.log(`ID 范围: ${keysetResult1.items[0].id} - ${keysetResult1.items[keysetResult1.items.length - 1].id}`);
console.log(`下一页游标: ${keysetResult1.metadata.nextCursor}`);

// 使用游标获取下一页
const keysetResult2 = keysetPaginator.paginate(keysetItems, keysetResult1.metadata.nextCursor, 15);

console.log('\n第二页数据:');
console.log(`ID 范围: ${keysetResult2.items[0].id} - ${keysetResult2.items[keysetResult2.items.length - 1].id}`);

// ==================== 4. 无限滚动分页 ====================

console.log('\n--- 4. 无限滚动分页 (Infinite Scroll) ---\n');

const infinitePaginator = new InfiniteScrollPaginator({
  batchSize: 10,
  preloadThreshold: 5
});

// 模拟无限滚动加载
let loadedCount = 0;
let batchCount = 0;

console.log('模拟无限滚动加载:');

while (loadedCount < 100 && batchCount < 15) {
  const batch = infinitePaginator.paginate(simpleItems, loadedCount, 10);
  
  console.log(`批次 ${batchCount + 1}: 加载 ${batch.items.length} 条 (已加载 ${loadedCount} + ${batch.items.length})`);
  
  // 检查是否需要预加载
  const loadState = infinitePaginator.getLoadState(100, loadedCount + batch.items.length);
  if (loadState.shouldPreload) {
    console.log('  ⚠️ 触发预加载条件!');
  }
  
  loadedCount += batch.items.length;
  batchCount++;
  
  if (!batch.metadata.hasMore) {
    console.log('  ✓ 加载完成!');
    break;
  }
}

// ==================== 5. Pagination 静态方法 ====================

console.log('\n--- 5. Pagination 静态方法 ---\n');

// 快速分页
const quickPage = Pagination.offset(simpleItems, 4, 15);
console.log(`快速分页: 第 4 页，共 ${quickPage.items.length} 条`);

// 页码范围计算
const displayPages = Pagination.calculatePageRange(10, 50, 9);
console.log(`\n页码范围 (当前第 10 页，共 50 页，显示 9 页): ${displayPages.join(', ')}`);

// 分页链接生成
const links = Pagination.generateLinks('/api/products', 5, 20);
console.log('\n分页链接:');
console.log(`  第一页: ${links.first}`);
console.log(`  上一页: ${links.prev}`);
console.log(`  当前页: ${links.self}`);
console.log(`  下一页: ${links.next}`);
console.log(`  最后一页: ${links.last}`);

// HTTP Link Header
const headerLink = Pagination.generateHeaderLinks('/api/products', 5, 20);
console.log('\nHTTP Link Header:');
console.log(headerLink);

// ==================== 6. 便捷函数 ====================

console.log('\n--- 6. 便捷函数 ---\n');

// 偏移量分页
const offsetResult = paginateOffset(simpleItems, 2, 10);
console.log(`paginateOffset: 第 2 页，从 ${offsetResult.items[0]} 开始`);

// 游标分页
const cursorResultQuick = paginateCursor(simpleItems, null, 10);
console.log(`paginateCursor: 第一页，共 ${cursorResultQuick.items.length} 条`);

// 无限滚动
const infiniteResult = paginateInfinite(simpleItems, 0, 10);
console.log(`paginateInfinite: 首批，共 ${infiniteResult.items.length} 条`);

// 页码范围
const range = pageRange(15, 30, 7);
console.log(`pageRange: ${range.join(', ')}`);

// ==================== 7. 实际应用场景 ====================

console.log('\n--- 7. 实际应用场景 ---\n');

// 场景 1: REST API 响应
console.log('场景 1: REST API 响应格式');
const apiResponse = Pagination.offset(createItems(500), 1, 25);
console.log(JSON.stringify({
  success: true,
  data: apiResponse.items.slice(0, 3).map(i => ({ id: i.id, name: i.name })),
  pagination: apiResponse.metadata.toJSON()
}, null, 2));

// 场景 2: GraphQL 分页响应
console.log('\n场景 2: GraphQL 分页响应格式');
const graphqlResponse = Pagination.cursor(createItems(200), null, 20);
console.log(JSON.stringify({
  edges: graphqlResponse.items.slice(0, 3).map(item => ({
    node: { id: item.id, name: item.name },
    cursor: Buffer.from(String(item.id)).toString('base64')
  })),
  pageInfo: {
    hasNextPage: graphqlResponse.metadata.hasMore,
    endCursor: graphqlResponse.metadata.nextCursor
  }
}, null, 2));

// 场景 3: 前端分页组件数据
console.log('\n场景 3: 前端分页组件数据');
const frontendData = Pagination.offset(simpleItems, 7, 15);
const pageButtons = Pagination.calculatePageRange(7, 20, 5);
const navLinks = Pagination.generateLinks('/products', 7, 20);

console.log(JSON.stringify({
  items: frontendData.items.slice(0, 3),
  currentPage: frontendData.metadata.currentPage,
  totalPages: frontendData.metadata.totalPages,
  pageButtons,
  navigation: navLinks
}, null, 2));

// 场景 4: 移动端无限滚动
console.log('\n场景 4: 移动端无限滚动状态');
const mobileState = infinitePaginator.getLoadState(1000, 850);
console.log(JSON.stringify({
  ...mobileState,
  message: mobileState.isComplete 
    ? '已加载全部内容' 
    : mobileState.shouldPreload 
      ? '建议预加载下一批' 
      : `还有 ${mobileState.remaining} 条未加载`
}, null, 2));

console.log('\n=== 示例完成 ===\n');