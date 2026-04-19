# BloomFilter Utils - C# 布隆过滤器工具

## 概述

布隆过滤器（Bloom Filter）是一种空间高效的概率型数据结构，用于快速判断一个元素是否"可能存在"或"绝对不存在"于集合中。

**核心特性：**
- ✅ 空间效率极高：相比 HashSet 可节省 90%+ 内存
- ✅ 查询速度极快：O(k) 时间复杂度（k 为哈希函数数量）
- ✅ 零假阴性：如果元素存在，必定返回 true
- ⚠️ 存在假阳性：可能误报不存在的元素为存在
- ⚠️ 标准版本不支持删除（使用 CountingBloomFilter 可解决）

## 安装使用

无需任何外部依赖，仅需 .NET 标准库。直接复制 `BloomFilter.cs` 文件到项目中即可使用。

## 快速开始

### 基础用法

```csharp
using AllToolkit.BloomFilter;

// 创建布隆过滤器（预期1000个元素，假阳性率1%）
var filter = new BloomFilter<string>(1000, 0.01);

// 添加元素
filter.Add("hello");
filter.Add("world");
filter.AddRange(new[] { "one", "two", "three" });

// 检查元素是否存在
bool mightExist = filter.MightContain("hello");  // true
bool notExist = filter.MightContain("notexist"); // false（或假阳性）

// 获取统计信息
var stats = filter.GetStats();
Console.WriteLine(stats);
// 输出: BloomFilter[Bits=9586, Hashes=7, Items=5, Fill=0.36%, Est.FalsePositive=0.00%]

// 清空过滤器
filter.Clear();
```

### 计数布隆过滤器（支持删除）

```csharp
// 创建计数布隆过滤器
var countingFilter = new CountingBloomFilter<string>(1000, 0.01);

// 添加元素
countingFilter.Add("item1");
countingFilter.Add("item2");

// 删除元素
bool removed = countingFilter.Remove("item1"); // true

// 检查存在
bool exists = countingFilter.MightContain("item2"); // true
```

### 可缩放布隆过滤器（自动扩容）

```csharp
// 创建可缩放布隆过滤器（初始容量100，会自动增长）
var scalableFilter = new ScalableBloomFilter<int>(100, 0.01);

// 添加大量元素（超过初始容量时会自动创建新层）
for (int i = 0; i < 10000; i++)
{
    scalableFilter.Add(i);
}

Console.WriteLine($"Filters created: {scalableFilter.FilterCount}");
Console.WriteLine($"Total items: {scalableFilter.Count}");

// 查询
bool exists = scalableFilter.MightContain(5000); // true
```

## API 文档

### BloomFilter<T>

| 属性 | 类型 | 说明 |
|------|------|------|
| ExpectedItems | int | 预期元素数量 |
| BitSize | int | 位数组大小 |
| HashFunctionCount | int | 哈希函数数量 |
| Count | int | 已添加元素数量 |
| BitsSet | int | 设置为1的位数 |
| EstimatedFalsePositiveProbability | double | 估计的假阳性概率 |

| 方法 | 说明 |
|------|------|
| Add(T item) | 添加元素 |
| AddRange(IEnumerable<T> items) | 批量添加 |
| MightContain(T item) | 检查元素是否可能存在 |
| Contains(T item) | MightContain 的别名 |
| Clear() | 清空过滤器 |
| Clone() | 克隆过滤器 |
| UnionWith(BloomFilter<T> other) | 合并另一个过滤器 |
| IntersectWith(BloomFilter<T> other) | 与另一个过滤器求交集 |
| ToByteArray() | 序列化为字节数组 |
| FromByteArray(...) | 从字节数组恢复 |
| GetStats() | 获取统计信息 |

### CountingBloomFilter<T>

| 方法 | 说明 |
|------|------|
| Add(T item) | 添加元素 |
| Remove(T item) | 删除元素（返回是否成功） |
| MightContain(T item) | 检查元素是否可能存在 |
| Clear() | 清空过滤器 |

### ScalableBloomFilter<T>

| 属性 | 类型 | 说明 |
|------|------|------|
| Count | long | 总元素数量 |
| FilterCount | int | 过滤器层数 |

| 方法 | 说明 |
|------|------|
| Add(T item) | 添加元素（自动扩容） |
| AddRange(IEnumerable<T> items) | 批量添加 |
| MightContain(T item) | 检查元素是否可能存在 |
| GetAllStats() | 获取所有层的统计信息 |

## 数学原理

### 最优参数计算

```csharp
// 计算最优位数组大小
int bits = BloomFilter<string>.OptimalBitSize(expectedItems, falsePositiveProbability);
// 公式: m = -n * ln(p) / (ln(2))^2

// 计算最优哈希函数数量
int hashes = BloomFilter<string>.OptimalHashFunctionCount(bits, expectedItems);
// 公式: k = (m/n) * ln(2)
```

### 常见配置参考

| 预期元素数 | 假阳性率 | 位数组大小 | 哈希函数数 | 内存占用 |
|------------|----------|------------|------------|----------|
| 1000 | 1% | ~9586 | 7 | ~1.2KB |
| 10000 | 1% | ~95851 | 7 | ~12KB |
| 100000 | 1% | ~958506 | 7 | ~120KB |
| 1000000 | 0.1% | ~19170118 | 10 | ~2.4MB |

## 应用场景

### 1. 缓存穿透防护

```csharp
// 在查询缓存前先检查布隆过滤器
var cacheFilter = new BloomFilter<string>(1000000, 0.01);

// 预加载所有可能的数据key
foreach (var key in allPossibleKeys)
{
    cacheFilter.Add(key);
}

// 查询前检查
if (!cacheFilter.MightContain(key))
{
    // 绝对不存在，直接返回，避免缓存穿透
    return null;
}
// 可能存在，继续查询缓存/数据库
```

### 2. URL 去重（爬虫）

```csharp
var urlFilter = new BloomFilter<string>(10000000, 0.001);
var visitedUrls = new HashSet<string>(); // 用于精确去重

bool IsUrlVisited(string url)
{
    if (!urlFilter.MightContain(url))
    {
        // 绝对未访问
        urlFilter.Add(url);
        visitedUrls.Add(url);
        return false;
    }
    
    // 可能已访问，用 HashSet 精确判断
    if (visitedUrls.Contains(url))
    {
        return true;
    }
    
    // 假阳性，实际未访问
    urlFilter.Add(url);
    visitedUrls.Add(url);
    return false;
}
```

### 3. 邮件地址过滤

```csharp
var emailFilter = new BloomFilter<string>(1000000, 0.01);

// 预加载黑名单邮箱
foreach (var blockedEmail in blockedList)
{
    emailFilter.Add(blockedEmail);
}

bool IsEmailBlocked(string email)
{
    return emailFilter.MightContain(email);
}
```

### 4. 分布式系统数据同步

```csharp
// 节点A: 创建布隆过滤器并发送给节点B
var syncFilter = new BloomFilter<int>(100000, 0.01);
foreach (var id in localIds)
{
    syncFilter.Add(id);
}
byte[] filterData = syncFilter.ToByteArray();

// 发送 filterData 到节点B...

// 节点B: 接收并检查
var receivedFilter = BloomFilter<int>.FromByteArray(filterData, 100000, 0.01);
var missingIds = remoteIds.Where(id => !receivedFilter.MightContain(id)).ToList();
// 只同步缺失的数据
```

## 性能对比

| 数据结构 | 插入时间 | 查询时间 | 内存占用 | 支持删除 |
|----------|----------|----------|----------|----------|
| HashSet<T> | O(1) | O(1) | 高（100%+） | ✅ |
| BloomFilter<T> | O(k) | O(k) | 极低（~10%） | ❌ |
| CountingBloomFilter<T> | O(k) | O(k) | 低（~20%） | ✅ |

对于 1 百万元素：
- HashSet: ~40MB
- BloomFilter: ~2MB（假阳性率 0.1%）

## 运行测试

```bash
cd C#/bloom_filter_utils
dotnet run BloomFilterTest.cs
# 或使用传统方式
csc BloomFilter.cs BloomFilterTest.cs && BloomFilterTest.exe
```

## 注意事项

1. **假阳性不可逆**：一旦误报，无法修正，只能重建过滤器
2. **假阴性不可能**：如果返回 false，元素绝对不存在
3. **参数选择**：实际元素数不应超过预期值，否则假阳性率会上升
4. **不支持删除**：标准布隆过滤器不支持删除，使用 CountingBloomFilter

## 版本历史

- v1.0.0 (2026-04-20): 初始版本
  - 标准 BloomFilter<T>
  - CountingBloomFilter<T>（支持删除）
  - ScalableBloomFilter<T>（自动扩容）
  - 序列化/反序列化支持
  - 合并/交集操作
  - 完整测试套件

## License

MIT License - 自由使用、修改和分发。