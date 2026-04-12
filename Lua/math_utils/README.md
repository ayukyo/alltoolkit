# Math Utils - Lua 数学工具库

提供全面的数学计算功能，包括统计、数论、格式化、随机数、向量和矩阵操作等。

## 特性

- ✅ **零依赖** - 仅使用 Lua 标准库
- ✅ **功能全面** - 50+ 数学函数
- ✅ **类型安全** - 完善的 nil 处理
- ✅ **详细文档** - 每个函数都有注释和示例
- ✅ **完整测试** - 覆盖所有主要功能

## 安装

```bash
# 复制 math_utils 文件夹到您的项目
cp -r math_utils /your/project/path/
```

## 快速开始

```lua
-- 加载模块
local MathUtils = dofile("math_utils/mod.lua")

-- 基础计算
print(MathUtils.round(3.14159, 2))        -- 3.14
print(MathUtils.clamp(15, 0, 10))         -- 10
print(MathUtils.lerp(0, 100, 0.5))        -- 50

-- 统计函数
local nums = {1, 2, 3, 4, 5}
print(MathUtils.average(nums))            -- 3
print(MathUtils.median(nums))             -- 3
print(MathUtils.stddev(nums))             -- 1.414...

-- 数论
print(MathUtils.gcd(48, 18))              -- 6
print(MathUtils.is_prime(17))             -- true
print(MathUtils.factorial(5))             -- 120

-- 格式化
print(MathUtils.format_bytes(1048576))    -- 1.00 MB
print(MathUtils.format_currency(1234.56)) -- $1,234.56
```

## API 参考

### 基础数学工具

| 函数 | 描述 | 示例 |
|------|------|------|
| `is_number(n)` | 检查是否为数字 | `is_number(42) → true` |
| `is_integer(n)` | 检查是否为整数 | `is_integer(3.14) → false` |
| `safe_divide(a, b, default)` | 安全除法 | `safe_divide(10, 0, -1) → -1` |
| `percentage(part, total)` | 计算百分比 | `percentage(25, 100) → 25` |
| `growth_rate(old, new)` | 计算增长率 | `growth_rate(100, 150) → 50` |
| `round(n, decimals)` | 四舍五入 | `round(3.14159, 2) → 3.14` |
| `floor_decimal(n, decimals)` | 向下取整 | `floor_decimal(3.999, 2) → 3.99` |
| `ceil_decimal(n, decimals)` | 向上取整 | `ceil_decimal(3.001, 2) → 3.01` |
| `clamp(n, min, max)` | 限制范围 | `clamp(15, 0, 10) → 10` |
| `lerp(a, b, t)` | 线性插值 | `lerp(0, 100, 0.5) → 50` |

### 统计函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `sum(numbers)` | 求和 | `sum({1,2,3}) → 6` |
| `average(numbers)` | 平均值 | `average({1,2,3}) → 2` |
| `median(numbers)` | 中位数 | `median({1,2,3,4,5}) → 3` |
| `mode(numbers)` | 众数 | `mode({1,2,2,3}) → 2` |
| `variance(numbers)` | 方差 | `variance({2,4,4,4,5,5,7,9}) → 4` |
| `stddev(numbers)` | 标准差 | `stddev({2,4,4,4,5,5,7,9}) → 2` |
| `min(numbers)` | 最小值 | `min({1,2,3}) → 1` |
| `max(numbers)` | 最大值 | `max({1,2,3}) → 3` |
| `range(numbers)` | 范围 | `range({1,2,3,4,5}) → 4` |

### 数论函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `gcd(a, b)` | 最大公约数 | `gcd(48, 18) → 6` |
| `lcm(a, b)` | 最小公倍数 | `lcm(4, 6) → 12` |
| `is_prime(n)` | 判断质数 | `is_prime(17) → true` |
| `prev_prime(n)` | 前一个质数 | `prev_prime(20) → 19` |
| `next_prime(n)` | 下一个质数 | `next_prime(10) → 11` |
| `factorial(n)` | 阶乘 | `factorial(5) → 120` |
| `combinations(n, k)` | 组合数 C(n,k) | `combinations(5, 2) → 10` |
| `permutations(n, k)` | 排列数 P(n,k) | `permutations(5, 2) → 20` |
| `divisors(n)` | 所有因数 | `divisors(12) → {1,2,3,4,6,12}` |
| `prime_factorization(n)` | 质因数分解 | `prime_factorization(60) → {2=2, 3=1, 5=1}` |

### 三角函数（角度版）

| 函数 | 描述 | 示例 |
|------|------|------|
| `deg_to_rad(degrees)` | 角度转弧度 | `deg_to_rad(180) → π` |
| `rad_to_deg(radians)` | 弧度转角度 | `rad_to_deg(π) → 180` |
| `sin_deg(degrees)` | 正弦（角度） | `sin_deg(30) → 0.5` |
| `cos_deg(degrees)` | 余弦（角度） | `cos_deg(60) → 0.5` |
| `tan_deg(degrees)` | 正切（角度） | `tan_deg(45) → 1` |
| `asin_deg(value)` | 反正弦 | `asin_deg(0.5) → 30` |
| `acos_deg(value)` | 反余弦 | `acos_deg(0.5) → 60` |
| `atan_deg(value)` | 反正切 | `atan_deg(1) → 45` |

### 数值格式化

| 函数 | 描述 | 示例 |
|------|------|------|
| `format_thousands(n, sep)` | 千分位格式化 | `format_thousands(1234567) → "1,234,567"` |
| `format_bytes(bytes, precision)` | 字节格式化 | `format_bytes(1048576) → "1.00 MB"` |
| `format_scientific(n, precision)` | 科学计数法 | `format_scientific(123456, 2) → "1.23e+05"` |
| `format_currency(amount, symbol, precision)` | 货币格式化 | `format_currency(1234.56, "$") → "$1,234.56"` |

### 随机数工具

| 函数 | 描述 | 示例 |
|------|------|------|
| `random_int(min, max)` | 随机整数 | `random_int(1, 10) → 7` |
| `random_float(min, max)` | 随机浮点数 | `random_float(0, 1) → 0.543...` |
| `random_choice(array)` | 随机选择 | `random_choice({1,2,3}) → 2` |
| `shuffle(array)` | 打乱数组 | `shuffle({1,2,3,4,5}) → {3,1,5,2,4}` |
| `uuid()` | 生成 UUID v4 | `uuid() → "550e8400-e29b-41d4-a716-446655440000"` |

### 向量操作

| 函数 | 描述 | 示例 |
|------|------|------|
| `vector_add(a, b)` | 向量加法 | `vector_add({1,2}, {3,4}) → {4,6}` |
| `vector_sub(a, b)` | 向量减法 | `vector_sub({5,6}, {1,2}) → {4,4}` |
| `dot_product(a, b)` | 点积 | `dot_product({1,2,3}, {4,5,6}) → 32` |
| `vector_length(v)` | 向量长度 | `vector_length({3,4}) → 5` |
| `normalize(v)` | 向量归一化 | `normalize({3,4}) → {0.6,0.8}` |
| `distance(a, b)` | 欧几里得距离 | `distance({0,0}, {3,4}) → 5` |

### 序列生成

| 函数 | 描述 | 示例 |
|------|------|------|
| `range_seq(start, stop, step)` | 等差数列 | `range_seq(0, 5) → {0,1,2,3,4}` |
| `fibonacci(count)` | 斐波那契数列 | `fibonacci(10) → {0,1,1,2,3,5,8,13,21,34}` |
| `fib(n)` | 第 n 个斐波那契数 | `fib(10) → 55` |

### 矩阵操作

| 函数 | 描述 | 示例 |
|------|------|------|
| `zeros(rows, cols)` | 零矩阵 | `zeros(2, 3) → {{0,0,0}, {0,0,0}}` |
| `identity(size)` | 单位矩阵 | `identity(3) → {{1,0,0}, {0,1,0}, {0,0,1}}` |
| `transpose(matrix)` | 矩阵转置 | `transpose({{1,2}, {3,4}}) → {{1,3}, {2,4}}` |
| `matrix_multiply(a, b)` | 矩阵乘法 | `matrix_multiply(a, b) → result` |
| `matrix_vector_multiply(matrix, vector)` | 矩阵向量乘法 | `matrix_vector_multiply(m, v) → result` |

### 特殊函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `ln(n)` | 自然对数 | `ln(e) → 1` |
| `log10(n)` | 常用对数 | `log10(100) → 2` |
| `log2(n)` | 二进制对数 | `log2(8) → 3` |
| `log_base(n, base)` | 任意底数对数 | `log_base(8, 2) → 3` |
| `sqrt(n)` | 平方根 | `sqrt(16) → 4` |
| `cbrt(n)` | 立方根 | `cbrt(27) → 3` |
| `power(base, exp)` | 幂运算 | `power(2, 10) → 1024` |
| `abs(n)` | 绝对值 | `abs(-5) → 5` |
| `sign(n)` | 符号函数 | `sign(-10) → -1` |
| `is_even(n)` | 判断偶数 | `is_even(4) → true` |
| `is_odd(n)` | 判断奇数 | `is_odd(7) → true` |
| `almost_equal(a, b, epsilon)` | 浮点数近似比较 | `almost_equal(0.1+0.2, 0.3) → true` |
| `digit_count(n)` | 数字位数 | `digit_count(12345) → 5` |
| `reverse_number(n)` | 反转数字 | `reverse_number(12345) → 54321` |
| `digit_sum(n)` | 各位数字之和 | `digit_sum(12345) → 15` |
| `is_perfect_square(n)` | 判断完全平方数 | `is_perfect_square(16) → true` |
| `is_perfect_cube(n)` | 判断完全立方数 | `is_perfect_cube(27) → true` |

## 运行测试

```bash
cd Lua/math_utils
lua math_utils_test.lua
```

## 示例

查看 `examples/` 目录获取更多使用示例。

## 常量

```lua
MathUtils.PI      -- π (3.14159...)
MathUtils.E       -- e (2.71828...)
MathUtils.PHI     -- 黄金比例 (1.618...)
MathUtils.SQRT2   -- √2 (1.414...)
```

## 错误处理

模块定义了标准错误类型：

```lua
MathUtils.Error.InvalidArgument   -- 无效参数
MathUtils.Error.DivisionByZero    -- 除零错误
MathUtils.Error.OutOfRange        -- 超出范围
MathUtils.Error.EmptyTable        -- 空表
```

## 许可证

MIT License - 详见 AllToolkit 主项目许可证。

## 贡献

欢迎提交 Issue 和 Pull Request！
