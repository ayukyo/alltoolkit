# JavaScript 工具模块

AllToolkit 的 JavaScript 语言实现，提供零依赖、生产级的常用工具函数。

## 模块列表

| 模块 | 文件 | 功能描述 | 测试 |
|------|------|----------|------|
| **array_utils** | `array_utils/mod.js` | 数组操作工具（去重、分组、排序、统计等） | ✅ 55 测试 |
| **string_utils** | `string_utils/mod.js` | 字符串处理工具 | ✅ 82 测试 |
| **base64_utils** | `base64_utils/mod.js` | Base64 编码解码 | ✅ 29 测试 |

## 快速开始

### 使用数组工具

```javascript
const ArrayUtils = require('./array_utils/mod.js');

// 去重
const unique = ArrayUtils.unique([1, 2, 2, 3]); // [1, 2, 3]

// 分组
const grouped = ArrayUtils.groupBy([
  { type: 'a', val: 1 },
  { type: 'b', val: 2 },
  { type: 'a', val: 3 }
], 'type');
// { a: [{...}, {...}], b: [{...}] }

// 分块
const chunks = ArrayUtils.chunk([1, 2, 3, 4, 5], 2); // [[1, 2], [3, 4], [5]]

// 排序
const sorted = ArrayUtils.sortBy([{ age: 30 }, { age: 20 }], 'age');

// 统计
const stats = ArrayUtils.countBy(['a', 'b', 'a', 'c', 'a']);
// { a: 3, b: 1, c: 1 }
```

### 使用字符串工具

```javascript
const StringUtils = require('./string_utils/mod.js');

// 空值检查
StringUtils.isBlank(''); // true
StringUtils.isNotBlank('hello'); // true

// 命名转换
StringUtils.toCamelCase('hello-world'); // 'helloWorld'
StringUtils.toSnakeCase('HelloWorld'); // 'hello_world'

// 验证
StringUtils.isValidEmail('test@example.com'); // true
StringUtils.isValidUrl('https://example.com'); // true

// 随机生成
StringUtils.randomPassword(16); // 生成 16 位密码
```

### 使用 Base64 工具

```javascript
const Base64Utils = require('./base64_utils/mod.js');

// 编码解码
const encoded = Base64Utils.encode('Hello, World!');
const decoded = Base64Utils.decode(encoded);

// URL 安全编码
const urlSafe = Base64Utils.toUrlSafe(encoded);
```

## 运行测试

```bash
# 数组工具测试
cd array_utils
node array_utils_test.js

# 字符串工具测试
cd string_utils
node string_utils_test.js

# Base64 工具测试
cd base64_utils
node base64_utils_test.js
```

## 运行示例

```bash
# 数组工具示例
node examples/array_utils_example.js

# 字符串工具示例
node examples/string_utils_example.js

# Base64 工具示例
node examples/base64_utils_example.js
```

## 特性

- ✅ **零依赖** - 仅使用 JavaScript 标准库
- ✅ **Node.js & 浏览器兼容** - 支持两种环境
- ✅ **完整测试覆盖** - 每个模块都有全面的测试用例
- ✅ **详细文档** - JSDoc 注释，包含参数和返回值说明
- ✅ **类型安全** - 所有方法都有参数验证
- ✅ **高性能** - 使用最优算法实现

## ArrayUtils 功能概览

### 基础操作
- `isEmpty/isNotEmpty` - 空值检查
- `first/last` - 首尾元素
- `take/skip` - 取/跳元素

### 去重与分组
- `unique` - 数组去重
- `uniqueBy` - 按条件去重
- `groupBy` - 数组分组

### 扁平化与分块
- `flatten/flattenDeep` - 扁平化
- `chunk` - 分块

### 集合运算
- `intersection` - 交集
- `union` - 并集
- `difference` - 差集
- `symmetricDifference` - 对称差集

### 排序与随机
- `sortBy` - 按条件排序
- `multiSort` - 多字段排序
- `shuffle` - 随机打乱
- `sample` - 随机取样

### 查找与过滤
- `find/filter` - 查找/过滤
- `findIndex` - 查找索引
- `partition` - 分区

### 统计计算
- `countBy` - 统计次数
- `mostFrequent` - 最频繁元素
- `min/max` - 最值
- `sum/average` - 求和/平均
- `median` - 中位数
- `stdDev/variance` - 标准差/方差

### 数组操作
- `remove/removeAt` - 移除元素
- `insertAt` - 插入元素
- `move/swap` - 移动/交换
- `rotate/reverse` - 旋转/反转

### 转换
- `toObject` - 转对象
- `toSet/fromSet` - Set 转换
- `toMap/fromMap` - Map 转换
- `range` - 范围生成
- `zip/unzip` - 压缩解压

### 高级功能
- `window` - 滑动窗口
- `pairwise` - 成对处理
- `longestIncreasingSubsequence` - 最长递增子序列
- `binarySearch` - 二分查找
- `paginate` - 分页
- `pipeline` - 流水线
- `topologicalSort` - 拓扑排序
- `asyncFilter/asyncMap` - 异步操作

## 许可证

MIT License
