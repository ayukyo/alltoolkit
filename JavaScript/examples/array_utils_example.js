/**
 * ArrayUtils Example
 * JavaScript 数组工具模块使用示例
 */

const ArrayUtils = require('../array_utils/mod.js');

console.log('ArrayUtils 使用示例\n');
console.log('='.repeat(50));

// ==================== 基础操作 ====================
console.log('\n## 基础操作');
console.log('-'.repeat(30));

const numbers = [1, 2, 3, 4, 5];
console.log('原始数组:', numbers);

console.log('第一个元素:', ArrayUtils.first(numbers));
console.log('最后一个元素:', ArrayUtils.last(numbers));
console.log('前 3 个:', ArrayUtils.take(numbers, 3));
console.log('跳过前 2 个:', ArrayUtils.skip(numbers, 2));

// ==================== 去重操作 ====================
console.log('\n## 去重操作');
console.log('-'.repeat(30));

const duplicates = [1, 2, 2, 3, 3, 3, 4];
console.log('原始数组:', duplicates);
console.log('去重后:', ArrayUtils.unique(duplicates));

// 根据条件去重
const users = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' },
  { id: 1, name: 'Charlie' }
];
console.log('\n用户列表:', users);
const uniqueUsers = ArrayUtils.uniqueBy(users, u => u.id);
console.log('按 ID 去重:', uniqueUsers);

// ==================== 分组操作 ====================
console.log('\n## 分组操作');
console.log('-'.repeat(30));

const people = [
  { name: 'Alice', age: 25, city: 'Beijing' },
  { name: 'Bob', age: 30, city: 'Shanghai' },
  { name: 'Charlie', age: 25, city: 'Beijing' },
  { name: 'David', age: 30, city: 'Shanghai' }
];

console.log('按城市分组:', ArrayUtils.groupBy(people, 'city'));
console.log('按年龄段分组:', ArrayUtils.groupBy(people, p => p.age >= 30 ? 'adult' : 'young'));

// ==================== 分块与扁平化 ====================
console.log('\n## 分块与扁平化');
console.log('-'.repeat(30));

const data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
console.log('原始数组:', data);
console.log('每 3 个分块:', ArrayUtils.chunk(data, 3));

const nested = [[1, 2], [3, 4], [5, [6, 7]]];
console.log('\n嵌套数组:', nested);
console.log('一级扁平化:', ArrayUtils.flatten(nested));
console.log('深度扁平化:', ArrayUtils.flattenDeep(nested));

// ==================== 集合运算 ====================
console.log('\n## 集合运算');
console.log('-'.repeat(30));

const setA = [1, 2, 3, 4];
const setB = [3, 4, 5, 6];

console.log('集合 A:', setA);
console.log('集合 B:', setB);
console.log('交集:', ArrayUtils.intersection(setA, setB));
console.log('并集:', ArrayUtils.union(setA, setB));
console.log('差集 (A-B):', ArrayUtils.difference(setA, setB));
console.log('对称差集:', ArrayUtils.symmetricDifference(setA, setB));

// ==================== 排序操作 ====================
console.log('\n## 排序操作');
console.log('-'.repeat(30));

const products = [
  { name: 'Apple', price: 5 },
  { name: 'Banana', price: 3 },
  { name: 'Cherry', price: 8 }
];

console.log('按价格升序:', ArrayUtils.sortBy(products, 'price'));
console.log('按价格降序:', ArrayUtils.sortBy(products, 'price', 'desc'));

// 多字段排序
const items = [
  { category: 'A', price: 10 },
  { category: 'B', price: 5 },
  { category: 'A', price: 5 }
];
console.log('\n多字段排序:', ArrayUtils.multiSort(items, 
  { key: 'category', order: 'asc' },
  { key: 'price', order: 'asc' }
));

// ==================== 随机操作 ====================
console.log('\n## 随机操作');
console.log('-'.repeat(30));

const cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'];
console.log('原始牌组:', cards);
console.log('打乱后:', ArrayUtils.shuffle(cards));
console.log('随机抽 3 张:', ArrayUtils.sample(cards, 3));

// ==================== 查找与过滤 ====================
console.log('\n## 查找与过滤');
console.log('-'.repeat(30));

const scores = [85, 92, 78, 95, 88, 76, 90];
console.log('分数列表:', scores);
console.log('及格分数 (>80):', ArrayUtils.filter(scores, s => s > 80));
console.log('第一个优秀 (>90):', ArrayUtils.find(scores, s => s > 90));
console.log('最高分索引:', ArrayUtils.findIndex(scores, s => s === 95));

// ==================== 统计操作 ====================
console.log('\n## 统计操作');
console.log('-'.repeat(30));

const stats = [2, 4, 4, 4, 5, 5, 7, 9];
console.log('数据:', stats);
console.log('最小值:', ArrayUtils.min(stats));
console.log('最大值:', ArrayUtils.max(stats));
console.log('总和:', ArrayUtils.sum(stats));
console.log('平均值:', ArrayUtils.average(stats));
console.log('中位数:', ArrayUtils.median(stats));
console.log('标准差:', ArrayUtils.stdDev(stats).toFixed(2));

// 出现次数统计
const colors = ['red', 'blue', 'red', 'green', 'blue', 'red'];
console.log('\n颜色统计:', ArrayUtils.countBy(colors));
console.log('最频繁的颜色:', ArrayUtils.mostFrequent(colors));

// ==================== 分区操作 ====================
console.log('\n## 分区操作');
console.log('-'.repeat(30));

const ages = [15, 22, 35, 42, 18, 55, 28];
const [adults, minors] = ArrayUtils.partition(ages, a => a >= 18);
console.log('年龄列表:', ages);
console.log('成年人:', adults);
console.log('未成年人:', minors);

// ==================== 转换操作 ====================
console.log('\n## 转换操作');
console.log('-'.repeat(30));

// 数组转对象
const usersList = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' },
  { id: 3, name: 'Charlie' }
];
const usersMap = ArrayUtils.toObject(usersList, 'id', 'name');
console.log('用户映射:', usersMap);

// 范围生成
console.log('0-9:', ArrayUtils.range(0, 10));
console.log('0-10 步长 2:', ArrayUtils.range(0, 11, 2));

// 压缩与解压
const names = ['Alice', 'Bob', 'Charlie'];
const ages2 = [25, 30, 35];
const zipped = ArrayUtils.zip(names, ages2);
console.log('\n压缩:', zipped);
console.log('解压:', ArrayUtils.unzip(zipped));

// ==================== 数组操作 ====================
console.log('\n## 数组操作');
console.log('-'.repeat(30));

let arr = [1, 2, 3, 4, 5];
console.log('原始数组:', arr);
console.log('移除值为 3:', ArrayUtils.remove(arr, 3));
console.log('移除索引 2:', ArrayUtils.removeAt(arr, 2));
console.log('在索引 2 插入 99:', ArrayUtils.insertAt(arr, 2, 99));
console.log('移动元素 (0->3):', ArrayUtils.move(arr, 0, 3));
console.log('交换元素 (0<->4):', ArrayUtils.swap(arr, 0, 4));

// ==================== 高级操作 ====================
console.log('\n## 高级操作');
console.log('-'.repeat(30));

// 滑动窗口
const prices = [10, 12, 11, 13, 15, 14, 16];
console.log('价格数据:', prices);
console.log('3 日滑动窗口:', ArrayUtils.window(prices, 3));
console.log('3 日滑动平均:', ArrayUtils.movingAverage(prices, 3).map(v => v.toFixed(2)));

// 累积和
console.log('累积和:', ArrayUtils.cumulativeSum(prices));

// 成对处理
console.log('相邻差值:', ArrayUtils.pairwise(prices, (a, b) => b - a));

// 最长递增子序列
const sequence = [10, 9, 2, 5, 3, 7, 101, 18];
console.log('\n序列:', sequence);
console.log('最长递增子序列:', ArrayUtils.longestIncreasingSubsequence(sequence));

// ==================== 分页操作 ====================
console.log('\n## 分页操作');
console.log('-'.repeat(30));

const allData = ArrayUtils.range(1, 26); // 1-25
const page1 = ArrayUtils.paginate(allData, 1, 10);
const page2 = ArrayUtils.paginate(allData, 2, 10);
const page3 = ArrayUtils.paginate(allData, 3, 10);

console.log('总数据:', allData.length);
console.log('第 1 页:', page1.data);
console.log('第 2 页:', page2.data);
console.log('第 3 页:', page3.data);
console.log('总页数:', page1.pages);

// ==================== 集合转换 ====================
console.log('\n## 集合转换');
console.log('-'.repeat(30));

const arr2 = [1, 2, 2, 3, 3, 3];
const set = ArrayUtils.toSet(arr2);
console.log('数组转 Set:', set);
console.log('Set 转数组:', ArrayUtils.fromSet(set));

// Map 转换
const keyValuePairs = [['a', 1], ['b', 2], ['c', 3]];
const map = new Map(keyValuePairs);
console.log('\nMap 转数组:', ArrayUtils.fromMap(map));

// ==================== 搜索操作 ====================
console.log('\n## 搜索操作');
console.log('-'.repeat(30));

const sorted = [1, 3, 5, 7, 9, 11, 13, 15];
console.log('已排序数组:', sorted);
console.log('查找 7:', ArrayUtils.binarySearch(sorted, 7));
console.log('查找 6 (不存在):', ArrayUtils.binarySearch(sorted, 6));
console.log('下界位置 (6):', ArrayUtils.binarySearchLowerBound(sorted, 6));
console.log('上界位置 (6):', ArrayUtils.binarySearchUpperBound(sorted, 6));

// ==================== 比较操作 ====================
console.log('\n## 比较操作');
console.log('-'.repeat(30));

const arrA = [1, 2, [3, 4]];
const arrB = [1, 2, [3, 4]];
const arrC = [1, 2, [3, 5]];

console.log('数组 A:', arrA);
console.log('数组 B:', arrB);
console.log('数组 C:', arrC);
console.log('A 等于 B:', ArrayUtils.deepEquals(arrA, arrB));
console.log('A 等于 C:', ArrayUtils.deepEquals(arrA, arrC));

console.log('忽略顺序比较 [1,2,3] 和 [3,2,1]:', 
  ArrayUtils.equalsIgnoreOrder([1, 2, 3], [3, 2, 1]));

// 相似度
const sim1 = [1, 2, 3, 4];
const sim2 = [2, 3, 4, 5];
console.log('\n相似度计算:');
console.log('数组 1:', sim1);
console.log('数组 2:', sim2);
console.log('Jaccard 相似度:', ArrayUtils.similarity(sim1, sim2).toFixed(2));

// 编辑距离
console.log('\n编辑距离:');
console.log('[1,2,3] -> [1,3,2]:', ArrayUtils.editDistance([1, 2, 3], [1, 3, 2]));

// ==================== 旋转与反转 ====================
console.log('\n## 旋转与反转');
console.log('-'.repeat(30));

const rotateArr = [1, 2, 3, 4, 5];
console.log('原始数组:', rotateArr);
console.log('向右旋转 2:', ArrayUtils.rotate(rotateArr, 2));
console.log('向左旋转 2:', ArrayUtils.rotate(rotateArr, -2));
console.log('反转:', ArrayUtils.reverse(rotateArr));

// ==================== 压缩与清理 ====================
console.log('\n## 压缩与清理');
console.log('-'.repeat(30));

const messy = [0, 1, false, 2, '', 3, null, 4, undefined, 5];
console.log('原始数组:', messy);
console.log('compact (移除 falsy):', ArrayUtils.compact(messy));
console.log('compactStrict (仅 null/undefined):', ArrayUtils.compactStrict(messy));

// ==================== 克隆操作 ====================
console.log('\n## 克隆操作');
console.log('-'.repeat(30));

const original = [{ a: 1 }, { b: 2 }];
const cloned = ArrayUtils.clone(original);
const deepCloned = ArrayUtils.deepClone(original);

cloned[0].a = 999;
console.log('修改克隆后:');
console.log('原始数组[0].a:', original[0].a);
console.log('深克隆[0].a:', deepCloned[0].a);

// ==================== 实用工具 ====================
console.log('\n## 实用工具');
console.log('-'.repeat(30));

// head/tail
const ht = [1, 2, 3, 4, 5];
console.log('headTail([1,2,3,4,5], 2):', ArrayUtils.headTail(ht, 2));
console.log('initLast([1,2,3,4,5], 2):', ArrayUtils.initLast(ht, 2));

// interleave
console.log('interleave([1,2], ["a","b"], [true,false]):', 
  ArrayUtils.interleave([1, 2], ['a', 'b'], [true, false]));

// 分桶
const bucketData = [1, 5, 10, 15, 20, 25, 30];
console.log('\n分桶 ([1,5,10,15,20,25,30] 分 3 桶):', 
  ArrayUtils.bucketize(bucketData, 3));

// 水塘抽样
console.log('水塘抽样 (取 3 个):', ArrayUtils.reservoirSample(bucketData, 3));

// ==================== 链式操作 ====================
console.log('\n## 链式操作 (Pipeline)');
console.log('-'.repeat(30));

const pipelineResult = ArrayUtils.pipeline(
  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  arr => ArrayUtils.filter(arr, x => x > 2),
  arr => ArrayUtils.filter(arr, x => x < 8),
  arr => ArrayUtils.map(arr, x => x * 2)
);
console.log('Pipeline 结果:', pipelineResult);

// ==================== 漏斗筛选 ====================
console.log('\n## 漏斗筛选');
console.log('-'.repeat(30));

const funnelResult = ArrayUtils.funnel(
  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  x => x > 2,
  x => x < 8,
  x => x % 2 === 0
);
console.log('漏斗筛选结果:', funnelResult);

// ==================== 拓扑排序 ====================
console.log('\n## 拓扑排序');
console.log('-'.repeat(30));

const tasks = [
  { name: 'A', deps: [] },
  { name: 'B', deps: ['A'] },
  { name: 'C', deps: ['A'] },
  { name: 'D', deps: ['B', 'C'] }
];
const sorted = ArrayUtils.topologicalSort(tasks, t => 
  t.deps.map(dep => tasks.find(task => task.name === dep))
);
console.log('任务依赖:', tasks.map(t => `${t.name}: [${t.deps.join(', ')}]`));
console.log('拓扑排序:', sorted?.map(t => t.name));

console.log('\n' + '='.repeat(50));
console.log('示例运行完成！');
