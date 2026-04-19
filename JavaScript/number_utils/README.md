# Number Utilities - JavaScript 数字工具模块

提供全面的数字操作函数库，包括类型判断、解析转换、格式化、数学运算、数论函数等。

## 功能特性

- ✅ **类型判断**: 整数、浮点数、质数、斐波那契数等判断
- ✅ **解析转换**: 二进制、十六进制、八进制转换
- ✅ **格式化**: 千分位、货币、百分比、文件大小、中文数字
- ✅ **数学运算**: 高精度加减乘除，统计函数（平均值、中位数、标准差）
- ✅ **范围操作**: clamp、线性插值、范围生成
- ✅ **随机数**: 随机整数、浮点数、唯一随机数组
- ✅ **数论函数**: GCD、LCM、阶乘、排列组合、质因数分解
- ✅ **数值处理**: 舍入、三角函数、对数、指数

## 零依赖

纯 JavaScript 实现，无需任何外部依赖。

## 快速开始

```javascript
const NumberUtils = require('./mod.js');

// 类型判断
NumberUtils.isNumber(42);        // true
NumberUtils.isPrime(7);          // true
NumberUtils.isFibonacci(5);      // true

// 格式化
NumberUtils.format(1234567.89, 2);     // "1,234,567.89"
NumberUtils.formatCurrency(1234.56);   // "¥1,234.56"
NumberUtils.formatFileSize(1048576);   // "1.00 MB"
NumberUtils.formatChinese(123);        // "一百二十三"

// 数学运算
NumberUtils.add(0.1, 0.2);       // 0.3 (避免精度问题)
NumberUtils.average([1,2,3,4,5]); // 3
NumberUtils.gcd(12, 8);         // 4
NumberUtils.factorial(5);       // 120

// 范围操作
NumberUtils.clamp(15, 1, 10);   // 10
NumberUtils.range(1, 5);        // [1, 2, 3, 4]

// 随机数
NumberUtils.randomInt(1, 10);   // 1-10之间的随机整数
NumberUtils.randomArray(5, 1, 10, true); // 5个唯一随机数
```

## 运行测试

```bash
node number_utils_test.js
```

## API 文档

### 类型判断

| 函数 | 说明 |
|------|------|
| `isNumber(value)` | 检查是否为数字 |
| `isInteger(value)` | 检查是否为整数 |
| `isFloat(value)` | 检查是否为浮点数 |
| `isPositive(value)` | 检查是否为正数 |
| `isNegative(value)` | 检查是否为负数 |
| `isZero(value, epsilon)` | 检查是否为零 |
| `isEven(value)` | 检查是否为偶数 |
| `isOdd(value)` | 检查是否为奇数 |
| `isPrime(value)` | 检查是否为质数 |
| `isPerfectSquare(value)` | 检查是否为完全平方数 |
| `isFibonacci(value)` | 检查是否为斐波那契数 |
| `inRange(value, min, max, inclusive)` | 检查是否在范围内 |

### 解析转换

| 函数 | 说明 |
|------|------|
| `parse(value, defaultValue)` | 安全解析数字 |
| `fromString(str, defaultValue)` | 从字符串解析（支持千分位） |
| `fromBinary(binaryStr)` | 从二进制解析 |
| `fromHex(hexStr)` | 从十六进制解析 |
| `toBinary(value)` | 转换为二进制字符串 |
| `toHex(value)` | 转换为十六进制字符串 |

### 格式化

| 函数 | 说明 |
|------|------|
| `format(value, decimals)` | 格式化（千分位） |
| `formatCurrency(value)` | 格式化为货币 |
| `formatPercent(value)` | 格式化为百分比 |
| `formatFileSize(bytes)` | 格式化文件大小 |
| `formatDuration(ms)` | 格式化持续时间 |
| `formatChinese(value)` | 中文数字格式化 |

### 数学运算

| 函数 | 说明 |
|------|------|
| `add(a, b)` | 高精度加法 |
| `subtract(a, b)` | 高精度减法 |
| `multiply(a, b)` | 高精度乘法 |
| `divide(a, b)` | 高精度除法 |
| `average(numbers)` | 求平均值 |
| `median(numbers)` | 求中位数 |
| `mode(numbers)` | 求众数 |
| `standardDeviation(numbers)` | 求标准差 |

### 数论函数

| 函数 | 说明 |
|------|------|
| `gcd(a, b)` | 最大公约数 |
| `lcm(a, b)` | 最小公倍数 |
| `factorial(n)` | 阶乘 |
| `permutation(n, r)` | 排列数 |
| `combination(n, r)` | 组合数 |
| `fibonacci(n)` | 斐波那契数 |
| `factors(n)` | 获取所有因数 |
| `primeFactors(n)` | 质因数分解 |
| `generatePrimes(n)` | 生成质数序列 |
| `sieveOfEratosthenes(max)` | 埃拉托斯特尼筛法 |

### 数值处理

| 函数 | 说明 |
|------|------|
| `round(value, decimals)` | 四舍五入 |
| `ceil(value, decimals)` | 向上取整 |
| `floor(value, decimals)` | 向下取整 |
| `truncate(value, decimals)` | 截断 |
| `sqrt(value)` | 平方根 |
| `pow(base, exponent)` | 幂运算 |
| `sin/cos/tan(radians)` | 三角函数 |
| `toDegrees/toRadians(value)` | 弧度角度转换 |

## 版本

- 1.0.0 - 初始版本

## 作者

AllToolkit