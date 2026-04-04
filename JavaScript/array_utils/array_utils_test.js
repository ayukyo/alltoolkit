/**
 * Array Utilities Test Suite
 * JavaScript 数组工具模块测试
 */

const ArrayUtils = require('./mod.js');

// 测试工具函数
function assert(condition, message) {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
}

function assertEqual(actual, expected, message) {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`${message}\nExpected: ${JSON.stringify(expected)}\nActual: ${JSON.stringify(actual)}`);
  }
}

function assertDeepEqual(actual, expected, message) {
  if (!ArrayUtils.deepEquals(actual, expected)) {
    throw new Error(`${message}\nExpected: ${JSON.stringify(expected)}\nActual: ${JSON.stringify(actual)}`);
  }
}

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (e) {
    console.error(`✗ ${name}`);
    console.error(`  ${e.message}`);
    failed++;
  }
}

console.log('Running ArrayUtils tests...\n');

// ==================== 基础检查测试 ====================
test('isEmpty - 空数组', () => {
  assert(ArrayUtils.isEmpty([]), '空数组应该返回 true');
  assert(ArrayUtils.isEmpty(null), 'null 应该返回 true');
  assert(ArrayUtils.isEmpty(undefined), 'undefined 应该返回 true');
  assert(!ArrayUtils.isEmpty([1]), '非空数组应该返回 false');
});

test('isNotEmpty - 非空检查', () => {
  assert(ArrayUtils.isNotEmpty([1]), '非空数组应该返回 true');
  assert(!ArrayUtils.isNotEmpty([]), '空数组应该返回 false');
  assert(!ArrayUtils.isNotEmpty(null), 'null 应该返回 false');
});

// ==================== 去重测试 ====================
test('unique - 基本去重', () => {
  assertDeepEqual(ArrayUtils.unique([1, 2, 2, 3, 3, 3]), [1, 2, 3], '应该去除重复元素');
  assertDeepEqual(ArrayUtils.unique(['a', 'b', 'a']), ['a', 'b'], '字符串去重');
});

test('uniqueBy - 根据条件去重', () => {
  const arr = [{ id: 1, name: 'a' }, { id: 2, name: 'b' }, { id: 1, name: 'c' }];
  const result = ArrayUtils.uniqueBy(arr, x => x.id);
  assertEqual(result.length, 2, '应该根据 id 去重');
  assertEqual(result[0].name, 'a', '保留第一个');
});

// ==================== 分组测试 ====================
test('groupBy - 基本分组', () => {
  const arr = [1, 2, 3, 4, 5, 6];
  const result = ArrayUtils.groupBy(arr, x => x % 2 === 0 ? 'even' : 'odd');
  assertDeepEqual(result.odd, [1, 3, 5], '奇数分组');
  assertDeepEqual(result.even, [2, 4, 6], '偶数分组');
});

test('groupBy - 按属性分组', () => {
  const arr = [{ type: 'a', val: 1 }, { type: 'b', val: 2 }, { type: 'a', val: 3 }];
  const result = ArrayUtils.groupBy(arr, 'type');
  assertEqual(result.a.length, 2, 'a 类型应该有 2 个');
  assertEqual(result.b.length, 1, 'b 类型应该有 1 个');
});

// ==================== 分块测试 ====================
test('chunk - 基本分块', () => {
  assertDeepEqual(ArrayUtils.chunk([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]], '应该正确分块');
  assertDeepEqual(ArrayUtils.chunk([1, 2, 3], 5), [[1, 2, 3]], '块大小大于数组长度');
});

// ==================== 扁平化测试 ====================
test('flatten - 一级扁平化', () => {
  assertDeepEqual(ArrayUtils.flatten([[1, 2], [3, 4]]), [1, 2, 3, 4], '应该扁平化一级');
});

test('flattenDeep - 深度扁平化', () => {
  assertDeepEqual(ArrayUtils.flattenDeep([[1, [2, 3]], [[4]]]), [1, 2, 3, 4], '应该深度扁平化');
});

// ==================== 集合运算测试 ====================
test('intersection - 交集', () => {
  assertDeepEqual(ArrayUtils.intersection([1, 2, 3], [2, 3, 4]), [2, 3], '应该返回交集');
  assertDeepEqual(ArrayUtils.intersection([1, 2], [3, 4]), [], '无交集应该返回空数组');
});

test('union - 并集', () => {
  assertDeepEqual(ArrayUtils.union([1, 2], [2, 3]), [1, 2, 3], '应该返回并集');
});

test('difference - 差集', () => {
  assertDeepEqual(ArrayUtils.difference([1, 2, 3], [2, 3]), [1], '应该返回差集');
});

test('symmetricDifference - 对称差集', () => {
  assertDeepEqual(ArrayUtils.symmetricDifference([1, 2], [2, 3]), [1, 3], '应该返回对称差集');
});

// ==================== 排序测试 ====================
test('sortBy - 基本排序', () => {
  const arr = [{ age: 30 }, { age: 20 }, { age: 25 }];
  const result = ArrayUtils.sortBy(arr, 'age');
  assertEqual(result[0].age, 20, '应该按年龄升序');
  assertEqual(result[2].age, 30, '最后一个应该是 30');
});

test('sortBy - 降序排序', () => {
  const result = ArrayUtils.sortBy([3, 1, 2], x => x, 'desc');
  assertDeepEqual(result, [3, 2, 1], '应该降序排序');
});

// ==================== 随机测试 ====================
test('shuffle - 打乱数组', () => {
  const arr = [1, 2, 3, 4, 5];
  const shuffled = ArrayUtils.shuffle(arr);
  assertEqual(shuffled.length, 5, '长度应该保持不变');
  assertEqual(shuffled.sort().join(','), '1,2,3,4,5', '元素应该相同');
});

test('sample - 随机取样', () => {
  const arr = [1, 2, 3, 4, 5];
  const sample = ArrayUtils.sample(arr, 3);
  assertEqual(sample.length, 3, '应该取 3 个');
});

// ==================== 查找测试 ====================
test('find - 查找元素', () => {
  const arr = [{ id: 1, name: 'a' }, { id: 2, name: 'b' }];
  const result = ArrayUtils.find(arr, x => x.id === 2);
  assertEqual(result.name, 'b', '应该找到 id 为 2 的元素');
});

test('filter - 过滤元素', () => {
  const result = ArrayUtils.filter([1, 2, 3, 4], x => x > 2);
  assertDeepEqual(result, [3, 4], '应该过滤出大于 2 的元素');
});

test('findIndex - 查找索引', () => {
  assertEqual(ArrayUtils.findIndex([1, 2, 3], x => x === 2), 1, '应该返回索引 1');
  assertEqual(ArrayUtils.findIndex([1, 2, 3], x => x === 5), -1, '未找到应该返回 -1');
});

// ==================== 统计测试 ====================
test('countBy - 统计次数', () => {
  const result = ArrayUtils.countBy(['a', 'b', 'a', 'c', 'a']);
  assertEqual(result.a, 3, 'a 应该出现 3 次');
  assertEqual(result.b, 1, 'b 应该出现 1 次');
});

test('mostFrequent - 最频繁元素', () => {
  assertEqual(ArrayUtils.mostFrequent([1, 2, 2, 3, 2]), 2, '2 应该是最频繁的');
});

// ==================== 分区测试 ====================
test('partition - 数组分区', () => {
  const [evens, odds] = ArrayUtils.partition([1, 2, 3, 4, 5], x => x % 2 === 0);
  assertDeepEqual(evens, [2, 4], '偶数分区');
  assertDeepEqual(odds, [1, 3, 5], '奇数分区');
});

// ==================== 数学运算测试 ====================
test('min/max - 最值', () => {
  assertEqual(ArrayUtils.min([3, 1, 4, 1, 5]), 1, '最小值应该是 1');
  assertEqual(ArrayUtils.max([3, 1, 4, 1, 5]), 5, '最大值应该是 5');
});

test('min/max - 按键', () => {
  const arr = [{ val: 3 }, { val: 1 }, { val: 4 }];
  assertEqual(ArrayUtils.min(arr, x => x.val).val, 1, '应该按 val 取最小');
});

test('sum - 求和', () => {
  assertEqual(ArrayUtils.sum([1, 2, 3, 4]), 10, '总和应该是 10');
});

test('average - 平均值', () => {
  assertEqual(ArrayUtils.average([1, 2, 3, 4]), 2.5, '平均值应该是 2.5');
});

test('median - 中位数', () => {
  assertEqual(ArrayUtils.median([1, 2, 3, 4, 5]), 3, '中位数应该是 3');
  assertEqual(ArrayUtils.median([1, 2, 3, 4]), 2.5, '偶数个应该是中间两个的平均');
});

test('stdDev/variance - 标准差和方差', () => {
  const arr = [2, 4, 4, 4, 5, 5, 7, 9];
  const variance = ArrayUtils.variance(arr);
  const stdDev = ArrayUtils.stdDev(arr);
  // 样本方差: 4.57, 标准差: 2.14
  assert(Math.abs(variance - 4.57) < 0.1, `方差应该接近 4.57, 实际是 ${variance}`);
  assert(Math.abs(stdDev - 2.14) < 0.1, `标准差应该接近 2.14, 实际是 ${stdDev}`);
});

// ==================== 数组操作测试 ====================
test('first/last - 首尾元素', () => {
  assertEqual(ArrayUtils.first([1, 2, 3]), 1, '第一个应该是 1');
  assertEqual(ArrayUtils.last([1, 2, 3]), 3, '最后一个应该是 3');
});

test('take/skip - 取/跳', () => {
  assertDeepEqual(ArrayUtils.take([1, 2, 3, 4], 2), [1, 2], '应该取前 2 个');
  assertDeepEqual(ArrayUtils.skip([1, 2, 3, 4], 2), [3, 4], '应该跳过前 2 个');
});

test('remove/removeAt - 移除', () => {
  assertDeepEqual(ArrayUtils.remove([1, 2, 3], 2), [1, 3], '应该移除值为 2 的元素');
  assertDeepEqual(ArrayUtils.removeAt([1, 2, 3], 1), [1, 3], '应该移除索引 1');
});

test('insertAt - 插入', () => {
  assertDeepEqual(ArrayUtils.insertAt([1, 3], 1, 2), [1, 2, 3], '应该在索引 1 插入 2');
});

test('move - 移动', () => {
  assertDeepEqual(ArrayUtils.move([1, 2, 3], 0, 2), [2, 3, 1], '应该将元素从 0 移到 2');
});

test('swap - 交换', () => {
  assertDeepEqual(ArrayUtils.swap([1, 2, 3], 0, 2), [3, 2, 1], '应该交换 0 和 2');
});

// ==================== 转换测试 ====================
test('toObject/fromObject - 对象转换', () => {
  const arr = [{ id: 1, name: 'a' }, { id: 2, name: 'b' }];
  const obj = ArrayUtils.toObject(arr, 'id', 'name');
  assertEqual(obj[1], 'a', 'id 1 对应 name a');
  assertEqual(obj[2], 'b', 'id 2 对应 name b');
});

test('range - 范围', () => {
  assertDeepEqual(ArrayUtils.range(0, 5), [0, 1, 2, 3, 4], '应该生成 0-4');
  assertDeepEqual(ArrayUtils.range(0, 10, 2), [0, 2, 4, 6, 8], '应该生成步长为 2');
});

test('zip/unzip - 压缩解压', () => {
  const zipped = ArrayUtils.zip([1, 2], ['a', 'b'], [true, false]);
  assertDeepEqual(zipped, [[1, 'a', true], [2, 'b', false]], '应该正确压缩');
  const unzipped = ArrayUtils.unzip(zipped);
  assertDeepEqual(unzipped[0], [1, 2], '应该正确解压');
});

// ==================== 比较测试 ====================
test('deepEquals - 深度比较', () => {
  assert(ArrayUtils.deepEquals([1, 2, [3, 4]], [1, 2, [3, 4]]), '应该相等');
  assert(!ArrayUtils.deepEquals([1, 2], [1, 3]), '应该不相等');
});

test('equalsIgnoreOrder - 忽略顺序比较', () => {
  assert(ArrayUtils.equalsIgnoreOrder([1, 2, 3], [3, 2, 1]), '应该相等');
  assert(!ArrayUtils.equalsIgnoreOrder([1, 2], [1, 2, 3]), '长度不同应该不相等');
});

// ==================== 分页测试 ====================
test('paginate - 分页', () => {
  const result = ArrayUtils.paginate([1, 2, 3, 4, 5], 1, 2);
  assertEqual(result.data.length, 2, '每页 2 个');
  assertEqual(result.total, 5, '总共 5 个');
  assertEqual(result.pages, 3, '共 3 页');
  assert(result.hasMore, '应该有更多');
});

// ==================== 集合测试 ====================
test('toSet/fromSet - Set 转换', () => {
  const set = ArrayUtils.toSet([1, 2, 2, 3]);
  assertEqual(set.size, 3, 'Set 大小应该是 3');
  assertDeepEqual(ArrayUtils.fromSet(set), [1, 2, 3], '应该正确转换回数组');
});

test('toMap/fromMap - Map 转换', () => {
  const arr = [{ id: 1, name: 'a' }, { id: 2, name: 'b' }];
  const map = ArrayUtils.toMap(arr, x => x.id, x => x.name);
  assertEqual(map.get(1), 'a', 'id 1 对应 a');
});

// ==================== 搜索测试 ====================
test('binarySearch - 二分查找', () => {
  const arr = [1, 3, 5, 7, 9];
  assertEqual(ArrayUtils.binarySearch(arr, 5), 2, '应该找到索引 2');
  assertEqual(ArrayUtils.binarySearch(arr, 4), -1, '未找到应该返回 -1');
});

// ==================== 工具测试 ====================
test('compact - 压缩', () => {
  assertDeepEqual(ArrayUtils.compact([0, 1, false, 2, '', 3]), [1, 2, 3], '应该移除 falsy 值');
});

test('rotate - 旋转', () => {
  assertDeepEqual(ArrayUtils.rotate([1, 2, 3, 4], 1), [4, 1, 2, 3], '应该向右旋转 1');
  assertDeepEqual(ArrayUtils.rotate([1, 2, 3, 4], -1), [2, 3, 4, 1], '应该向左旋转 1');
});

test('reverse - 反转', () => {
  assertDeepEqual(ArrayUtils.reverse([1, 2, 3]), [3, 2, 1], '应该反转');
});

test('clone/deepClone - 克隆', () => {
  const arr = [{ a: 1 }];
  const cloned = ArrayUtils.clone(arr);
  const deepCloned = ArrayUtils.deepClone(arr);
  cloned[0].a = 2;
  assertEqual(arr[0].a, 2, '浅克隆应该影响原数组');
  assertEqual(deepCloned[0].a, 1, '深克隆不应该影响');
});

// ==================== 高级测试 ====================
test('window - 滑动窗口', () => {
  const result = ArrayUtils.window([1, 2, 3, 4, 5], 3);
  assertDeepEqual(result, [[1, 2, 3], [2, 3, 4], [3, 4, 5]], '应该正确生成窗口');
});

test('pairwise - 成对处理', () => {
  const result = ArrayUtils.pairwise([1, 2, 3, 4], (a, b) => a + b);
  assertDeepEqual(result, [3, 5, 7], '应该成对相加');
});

test('longestIncreasingSubsequence - 最长递增子序列', () => {
  const result = ArrayUtils.longestIncreasingSubsequence([10, 9, 2, 5, 3, 7, 101, 18]);
  assertDeepEqual(result, [2, 3, 7, 18], '应该找到最长递增子序列');
});

test('editDistance - 编辑距离', () => {
  assertEqual(ArrayUtils.editDistance([1, 2, 3], [1, 2, 3]), 0, '相同数组距离为 0');
  assertEqual(ArrayUtils.editDistance([1, 2, 3], [1, 3, 2]), 2, '交换需要 2 步');
});

test('similarity - 相似度', () => {
  const sim = ArrayUtils.similarity([1, 2, 3], [2, 3, 4]);
  assert(sim > 0 && sim < 1, '相似度应该在 0-1 之间');
});

// ==================== 异步测试 ====================
async function runAsyncTests() {
  console.log('\nRunning async tests...\n');
  
  await (async () => {
    try {
      const arr = [1, 2, 3, 4, 5];
      const result = await ArrayUtils.asyncFilter(arr, async x => x > 2);
      assertDeepEqual(result, [3, 4, 5], '异步过滤应该正确');
      console.log('✓ asyncFilter - 异步过滤');
      passed++;
    } catch (e) {
      console.error('✗ asyncFilter - 异步过滤');
      console.error(`  ${e.message}`);
      failed++;
    }
  })();
  
  await (async () => {
    try {
      const arr = [1, 2, 3];
      const result = await ArrayUtils.asyncMap(arr, async x => x * 2);
      assertDeepEqual(result, [2, 4, 6], '异步映射应该正确');
      console.log('✓ asyncMap - 异步映射');
      passed++;
    } catch (e) {
      console.error('✗ asyncMap - 异步映射');
      console.error(`  ${e.message}`);
      failed++;
    }
  })();
}

// 运行测试
(async () => {
  await runAsyncTests();
  
  console.log(`\n========================================`);
  console.log(`Results: ${passed} passed, ${failed} failed`);
  console.log(`========================================`);
  
  process.exit(failed > 0 ? 1 : 0);
})();
