# JavaScript 随机工具模块 (random_utils)

> 完整的随机数和值生成工具库，零外部依赖

## 📦 模块信息

- **语言**: JavaScript (Node.js)
- **依赖**: 无外部依赖，纯标准库实现
- **测试**: 80+ 单元测试
- **日期**: 2026-04-15

## ✨ 功能特性

### 🎲 基础随机数
- `randomInt(min, max)` - 随机整数 [min, max]（包含边界）
- `randomFloat(min, max, precision)` - 随机浮点数，支持精度控制
- `randomBool(probability)` - 随机布尔值，支持概率控制

### 🔤 随机字符串
- `randomString(length, options)` - 自定义随机字符串
  - 支持大小写字母、数字、特殊字符
  - 支持自定义字符集
  - 支持前缀/后缀
- `randomHex(length)` - 随机十六进制字符串
- `randomNumeric(length)` - 随机数字字符串
- `randomAlpha(length, lowercaseOnly)` - 随机字母字符串
- `randomPassword(length)` - 强密码生成（包含所有字符类型）

### 🎨 随机颜色
- `randomHexColor(withHash)` - 随机 HEX 颜色
- `randomRgbColor()` / `randomRgbString()` - 随机 RGB 颜色
- `randomRgbaColor(alpha)` / `randomRgbaString(alpha)` - 随机 RGBA 颜色
- `randomHslColor()` / `randomHslString()` - 随机 HSL 颜色

### 🔑 UUID 生成
- `uuid()` - UUID v4（符合 RFC 4122）
- `shortUuid()` - 短 UUID（无连字符）
- `uuidBatch(count)` - 批量生成 UUID

### 📚 数组操作
- `randomChoice(array)` - 随机选择一个元素
- `randomChoices(array, count)` - 随机选择多个元素（可重复）
- `randomSample(array, count)` - 随机采样（不重复）
- `shuffle(array)` - Fisher-Yates 洗牌（返回新数组）
- `shuffleInPlace(array)` - 原地洗牌

### ⚖️ 加权随机
- `weightedChoice(items)` - 加权随机选择
- `weightedChoices(items, count, unique)` - 加权随机选择多个

### 📊 概率分布
- `uniform(min, max)` - 均匀分布
- `normal(mean, stdDev)` - 正态分布（Box-Muller 变换）
- `exponential(lambda)` - 指数分布
- `poisson(lambda)` - 泊松分布

### 🕐 随机日期时间
- `randomDate(start, end)` - 随机日期
- `randomTime(withSeconds)` - 随机时间
- `randomDatetime()` - 随机日期时间

### 🔐 加密安全随机
- `cryptoRandomInt(min, max)` - 加密安全随机整数
- `cryptoRandomString(length, charset)` - 加密安全随机字符串
- `cryptoRandomBytes(length)` - 加密安全随机字节

### 🛠️ 其他实用函数
- `randomEnum(enumObj)` - 随机枚举值
- `randomIPv4()` - 随机 IPv4 地址
- `randomMAC(separator)` - 随机 MAC 地址
- `randomPort(wellKnownOnly)` - 随机端口
- `randomUsername(options)` - 随机用户名
- `randomEmail(domains)` - 随机邮箱
- `randomUrl(options)` - 随机 URL
- `randomChinesePhone()` - 随机中国手机号
- `randomDelay(minMs, maxMs)` - 随机延迟（异步）

### 📝 常量
- `ALPHABET_LOWERCASE` - 小写字母 `abcdefghijklmnopqrstuvwxyz`
- `ALPHABET_UPPERCASE` - 大写字母 `ABCDEFGHIJKLMNOPQRSTUVWXYZ`
- `ALPHABET` - 全字母（大小写）
- `DIGITS` - 数字 `0123456789`
- `ALPHANUMERIC` - 字母数字
- `SPECIAL_CHARS` - 特殊字符
- `HEX_CHARS` - 十六进制字符

## 📖 使用示例

```javascript
const random = require('./mod.js');

// 基础随机数
console.log(random.randomInt(1, 100));      // 1-100 之间的整数
console.log(random.randomFloat(0, 1, 4));   // 0-1 之间，4位小数
console.log(random.randomBool(0.8));        // 80% 概率返回 true

// 随机字符串
console.log(random.randomString(16));       // 16位字母数字字符串
console.log(random.randomPassword(20));     // 20位强密码
console.log(random.randomHex(8));           // 8位十六进制

// 随机颜色
console.log(random.randomHexColor());       // #a3f2b1
console.log(random.randomRgbString());      // rgb(123, 45, 200)

// UUID
console.log(random.uuid());                 // 550e8400-e29b-41d4-a716-446655440000

// 数组操作
const arr = [1, 2, 3, 4, 5];
console.log(random.randomChoice(arr));      // 随机选择一个
console.log(random.randomSample(arr, 3));   // 随机选择3个不重复
console.log(random.shuffle(arr));           // 打乱顺序

// 加权随机
const items = [
    { item: 'gold', weight: 1 },
    { item: 'silver', weight: 10 },
    { item: 'bronze', weight: 50 }
];
console.log(random.weightedChoice(items));  // 更可能选择 bronze

// 概率分布
console.log(random.normal(100, 15));        // 正态分布，均值100，标准差15
console.log(random.poisson(5));             // 泊松分布

// 随机日期
console.log(random.randomDate('2020-01-01', '2023-12-31'));

// 实用函数
console.log(random.randomIPv4());           // 192.168.1.100
console.log(random.randomChinesePhone());   // 13812345678
console.log(random.randomEmail());          // user123@example.com
```

## 🧪 测试结果

```
========================================
随机工具模块测试
========================================

✓ ALPHABET_LOWERCASE 长度正确
✓ ALPHABET_UPPERCASE 长度正确
✓ ALPHABET 包含大小写
✓ DIGITS 长度正确
✓ ALPHANUMERIC 包含字母和数字
✓ SPECIAL_CHARS 非空
✓ HEX_CHARS 度正确

--- 基础随机数测试 ---
✓ randomInt 在范围内
✓ randomInt 包含边界值
✓ randomInt 边界相等返回该值
✓ randomInt 抛出错误：min > max
✓ randomInt 抛出错误：非数字参数
✓ randomFloat 在范围内
✓ randomFloat 精度控制
✓ randomFloat 抛出错误：min >= max
✓ randomBool 返回布尔值
✓ randomBool 概率正确
✓ randomBool 抛出错误：无效概率

... (共 80+ 测试)

========================================
测试完成: 82 通过, 0 失败
========================================
```

## 🔧 API 参考

### randomInt(min, max)
生成指定范围内的随机整数。

| 参数 | 类型 | 说明 |
|------|------|------|
| min | number | 最小值（包含） |
| max | number | 最大值（包含） |

**返回**: `number`

### randomString(length, options)
生成随机字符串。

| 参数 | 类型 | 说明 |
|------|------|------|
| length | number | 字符串长度 |
| options.lowercase | boolean | 包含小写字母（默认 true） |
| options.uppercase | boolean | 包含大写字母（默认 true） |
| options.digits | boolean | 包含数字（默认 true） |
| options.special | boolean | 包含特殊字符（默认 false） |
| options.charset | string | 自定义字符集 |
| options.prefix | string | 前缀 |
| options.suffix | string | 后缀 |

**返回**: `string`

### weightedChoice(items)
加权随机选择。

| 参数 | 类型 | 说明 |
|------|------|------|
| items | Array<{item, weight}> | 带权重的项目数组 |

**返回**: `*`（选中项目的 item 值）

### normal(mean, stdDev)
生成正态分布随机数。

| 参数 | 类型 | 说明 |
|------|------|------|
| mean | number | 均值（默认 0） |
| stdDev | number | 标准差（默认 1） |

**返回**: `number`

## 📝 注意事项

1. **加密安全**: `cryptoRandomInt`、`cryptoRandomString`、`cryptoRandomBytes` 使用 Node.js crypto 模块，适合用于密码、密钥等敏感场景
2. **性能**: 普通随机函数使用 `Math.random()`，性能更高但不适合安全场景
3. **边界**: `randomInt` 包含边界值（闭区间），`randomFloat` 不包含最大值（开区间）
4. **分布测试**: 正态分布使用 Box-Muller 变换，泊松分布使用 Knuth 算法

## 🚀 使用场景

- **游戏开发**: 随机事件、概率掉落、随机生成
- **测试数据生成**: 随机用户名、邮箱、日期等测试数据
- **密码生成**: 强密码生成器
- **模拟仿真**: 概率分布模拟
- **抽样统计**: 随机采样、洗牌
- **UI 开发**: 随机颜色生成

---

**零外部依赖 | 纯 JavaScript 标准库实现 | 80+ 单元测试**