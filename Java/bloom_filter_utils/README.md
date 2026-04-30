# Bloom Filter Utils (Java)

零外部依赖的布隆过滤器工具库，提供高效的概率性集合成员检测。

## 功能特性

- ✅ **零外部依赖** - 仅使用 Java 标准库
- ✅ **可配置误判率** - 支持自定义预期元素数和误判率
- ✅ **泛型支持** - 通过序列化器支持任意类型
- ✅ **可扩展布隆过滤器** - 自动增长容量
- ✅ **线程安全** - 提供并发访问支持
- ✅ **序列化** - 支持持久化存储

## 快速开始

### 基本用法

```java
import com.alltoolkit.bloomfilter.*;

// 创建 String 类型的布隆过滤器（默认 10000 元素，1% 误判率）
BloomFilter<String> filter = new BloomFilter<>(BloomFilter.stringSerializer());

// 添加元素
filter.insert("hello");
filter.insert("world");

// 检查成员
filter.contains("hello");  // true - 可能存在
filter.contains("missing"); // false - 确定不存在
```

### 自定义配置

```java
// 创建优化的配置：100000 元素，0.1% 误判率
BloomFilter.BloomConfig config = BloomFilter.BloomConfig.optimal(100000, 0.001);
BloomFilter<Integer> filter = new BloomFilter<>(config, BloomFilter.intSerializer());

// 或直接指定参数
BloomFilter<Integer> filter = new BloomFilter<>(100000, 0.001, BloomFilter.intSerializer());
```

### 内置序列化器

```java
// String
BloomFilter<String> stringFilter = new BloomFilter<>(BloomFilter.stringSerializer());

// Integer
BloomFilter<Integer> intFilter = new BloomFilter<>(BloomFilter.intSerializer());

// Long
BloomFilter<Long> longFilter = new BloomFilter<>(BloomFilter.longSerializer());

// byte[]
BloomFilter<byte[]> bytesFilter = new BloomFilter<>(BloomFilter.bytesSerializer());
```

### 自定义类型

```java
// 定义自定义序列化器
BloomFilter.ElementSerializer<User> userSerializer = user -> {
    ByteArrayOutputStream baos = new ByteArrayOutputStream();
    DataOutputStream dos = new DataOutputStream(baos);
    dos.writeLong(user.getId());
    dos.writeUTF(user.getName());
    return baos.toByteArray();
};

BloomFilter<User> userFilter = new BloomFilter<>(userSerializer);
```

### 可扩展布隆过滤器

```java
// 自动增长的布隆过滤器
ScalableBloomFilter<String> filter = new ScalableBloomFilter<>(
    100,    // 初始容量
    0.01,   // 误判率
    BloomFilter.stringSerializer()
);

// 插入任意数量的元素，过滤器自动扩展
for (int i = 0; i < 1000000; i++) {
    filter.insert("item_" + i);
}

System.out.println("Filters created: " + filter.filterCount());
```

### 线程安全访问

```java
// 创建线程安全的布隆过滤器
ConcurrentBloomFilter<String> filter = new ConcurrentBloomFilter<>(
    BloomFilter.stringSerializer()
);

// 多线程安全使用
filter.insert("item1");
filter.contains("item1");  // 线程安全

// 或包装现有过滤器
BloomFilter<String> unsafeFilter = new BloomFilter<>(BloomFilter.stringSerializer());
ConcurrentBloomFilter<String> safeFilter = new ConcurrentBloomFilter<>(unsafeFilter);
```

### 序列化与持久化

```java
// 序列化到字节数组
byte[] bytes = filter.toBytes();

// 从字节数组恢复
BloomFilter<String> restored = BloomFilter.fromBytes(bytes, BloomFilter.stringSerializer());

// 可保存到文件
Files.write(Paths.get("filter.dat"), bytes);
```

## 核心 API

### BloomFilter

| 方法 | 说明 |
|------|------|
| `insert(T item)` | 添加元素 |
| `contains(T item)` | 检查元素是否存在（可能误判） |
| `checkAndInsert(T item)` | 检查并添加（原子操作） |
| `clear()` | 清空过滤器 |
| `size()` | 已添加元素数量 |
| `isEmpty()` | 是否为空 |
| `fillRatio()` | 位填充率 |
| `currentFalsePositiveRate()` | 当前预估误判率 |
| `merge(BloomFilter<T>)` | 合并另一个过滤器 |
| `toBytes()` | 序列化 |
| `fromBytes(byte[], serializer)` | 反序列化 |

### ScalableBloomFilter

| 方法 | 说明 |
|------|------|
| `insert(T item)` | 添加元素（自动扩展） |
| `contains(T item)` | 检查元素是否存在 |
| `filterCount()` | 内部过滤器数量 |
| `estimatedFalsePositiveRate()` | 预估误判率 |

### ConcurrentBloomFilter

线程安全的包装器，API 与 BloomFilter 相同。

## 性能特性

- **空间效率**：每个元素约需 10-20 位（取决于误判率）
- **时间复杂度**：O(k)，k 为哈希函数数量（通常 3-10）
- **误判率**：可配置，通常 0.1% - 5%

### 配置选择指南

| 元素数 | 误判率 | 推荐配置 |
|--------|--------|----------|
| 1,000 | 1% | `optimal(1000, 0.01)` |
| 10,000 | 0.1% | `optimal(10000, 0.001)` |
| 100,000 | 1% | `optimal(100000, 0.01)` |
| 1,000,000 | 0.01% | `optimal(1000000, 0.0001)` |

## 典型应用场景

1. **URL 去重**：爬虫已访问 URL 检测
2. **用户名检查**：快速判断用户名是否已注册
3. **缓存预热**：判断数据是否需要加载
4. **垃圾邮件过滤**：快速判断发件人是否在黑名单
5. **推荐系统**：排除已推荐内容

## 编译与测试

```bash
# 编译
javac -d target/classes src/main/java/com/alltoolkit/bloomfilter/*.java

# 运行示例
java -cp target/classes com.alltoolkit.bloomfilter.examples.BloomFilterExample

# 运行测试 (需要 JUnit)
javac -d target/test-classes -cp target/classes:junit-4.13.2.jar \
    src/test/java/com/alltoolkit/bloomfilter/*.java
java -cp target/classes:target/test-classes:junit-4.13.2.jar:hamcrest-core-1.3.jar \
    org.junit.runner.JUnitCore com.alltoolkit.bloomfilter.BloomFilterTest
```

## 文件结构

```
bloom_filter_utils/
├── README.md
├── src/
│   ├── main/java/com/alltoolkit/bloomfilter/
│   │   ├── BloomFilter.java          # 核心实现
│   │   ├── ScalableBloomFilter.java  # 可扩展版本
│   │   └── ConcurrentBloomFilter.java # 线程安全版本
│   └── test/java/com/alltoolkit/bloomfilter/
│       ├── BloomFilterTest.java
│       ├── ScalableBloomFilterTest.java
│       └── ConcurrentBloomFilterTest.java
└── examples/
    └── BloomFilterExample.java       # 使用示例
```

## 许可证

MIT License