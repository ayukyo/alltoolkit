# Math Utils - 数学工具模块

零外部依赖的 Python 数学工具库，提供常用数学运算功能。

## 功能特性

### 基础运算
- `factorial(n)` - 阶乘计算
- `fibonacci(n)` - 斐波那契数列
- `fibonacci_sequence(n)` - 生成前 n 个斐波那契数
- `gcd(*numbers)` - 最大公约数
- `lcm(*numbers)` - 最小公倍数
- `power(base, exponent)` - 幂运算
- `sqrt(n)` - 平方根
- `cbrt(n)` - 立方根
- `root(n, index)` - n 次方根
- `abs(n)` - 绝对值
- `sign(n)` - 符号函数

### 数论工具
- `is_prime(n)` - 素数检测
- `primes_up_to(n)` - 生成素数列表（埃拉托斯特尼筛法）
- `prime_factors(n)` - 质因数分解
- `divisors(n)` - 获取所有因数
- `count_divisors(n)` - 因数个数
- `euler_totient(n)` - 欧拉函数
- `is_perfect_number(n)` - 完全数检测

### 几何计算
- `distance_2d(p1, p2)` - 二维距离
- `distance_3d(p1, p2)` - 三维距离
- `circle_area(radius)` - 圆面积
- `circle_circumference(radius)` - 圆周长
- `sphere_volume(radius)` - 球体积
- `sphere_surface_area(radius)` - 球表面积
- `rectangle_area(width, height)` - 矩形面积
- `triangle_area(base, height)` - 三角形面积（底高法）
- `triangle_area_heron(a, b, c)` - 三角形面积（海伦公式）
- `cylinder_volume(radius, height)` - 圆柱体体积
- `cone_volume(radius, height)` - 圆锥体体积
- `angle_between_vectors(v1, v2)` - 向量夹角

### 统计扩展
- `mean(values)` - 平均值
- `median(values)` - 中位数
- `mode(values)` - 众数
- `variance(values, population)` - 方差
- `standard_deviation(values, population)` - 标准差
- `range_value(values)` - 极差
- `percentile(values, p)` - 百分位数
- `quartiles(values)` - 四分位数
- `iqr(values)` - 四分位距
- `covariance(x, y, population)` - 协方差
- `correlation(x, y)` - 皮尔逊相关系数

### 数值处理
- `round_to(value, decimals)` - 四舍五入
- `round_up(value, decimals)` - 向上取整
- `round_down(value, decimals)` - 向下取整
- `truncate(value, decimals)` - 截断
- `clamp(value, min_val, max_val)` - 限制范围
- `percentage(value, total)` - 计算百分比
- `percentage_change(old, new)` - 百分比变化
- `ratio_to_percentage(ratio)` - 比率转百分比

### 向量运算
- `vector_add(v1, v2)` - 向量加法
- `vector_subtract(v1, v2)` - 向量减法
- `vector_scale(v, scalar)` - 向量数乘
- `vector_dot(v1, v2)` - 向量点积
- `vector_cross_3d(v1, v2)` - 三维向量叉积
- `vector_magnitude(v)` - 向量模长
- `vector_normalize(v)` - 向量归一化

### 序列生成
- `arithmetic_sequence(start, diff, n)` - 等差数列
- `arithmetic_sum(start, diff, n)` - 等差数列求和
- `geometric_sequence(start, ratio, n)` - 等比数列
- `geometric_sum(start, ratio, n)` - 等比数列求和
- `range_float(start, stop, step)` - 浮点数范围
- `linspace(start, stop, num)` - 等间距数列

### 数值检查
- `is_even(n)` - 偶数判断
- `is_odd(n)` - 奇数判断
- `is_integer(n)` - 整数判断
- `is_power_of(n, base)` - 幂次判断
- `is_perfect_square(n)` - 完全平方数
- `is_perfect_cube(n)` - 完全立方数
- `is_armstrong(n)` - 阿姆斯特朗数
- `is_palindrome_number(n)` - 回文数

### 随机函数
- `random_int(min_val, max_val)` - 随机整数
- `random_float(min_val, max_val)` - 随机浮点数
- `random_choice(values)` - 随机选择
- `random_sample(values, k)` - 随机抽样
- `shuffle(values)` - 打乱列表

## 安装

无需安装，直接复制 `math_utils.py` 文件到项目中即可使用。

## 使用示例

```python
from math_utils import MathUtils

# 基础运算
print(MathUtils.factorial(5))        # 120
print(MathUtils.fibonacci(10))       # 55
print(MathUtils.gcd(48, 18))         # 6
print(MathUtils.lcm(4, 6))           # 12

# 数论
print(MathUtils.is_prime(17))        # True
print(MathUtils.primes_up_to(20))    # [2, 3, 5, 7, 11, 13, 17, 19]
print(MathUtils.prime_factors(60))   # [2, 2, 3, 5]

# 几何
print(MathUtils.distance_2d((0, 0), (3, 4)))  # 5.0
print(MathUtils.circle_area(1))                # 3.14159...
print(MathUtils.triangle_area_heron(3, 4, 5)) # 6.0

# 统计
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(MathUtils.mean(data))                    # 5.5
print(MathUtils.median(data))                   # 5.5
print(MathUtils.standard_deviation(data))      # 2.87228...
print(MathUtils.correlation([1, 2, 3], [2, 4, 6]))  # 1.0

# 数值处理
print(MathUtils.percentage(25, 200))     # 12.5
print(MathUtils.clamp(10, 0, 5))         # 5
print(MathUtils.round_to(3.14159, 2))   # 3.14

# 向量
v1 = (1, 2, 3)
v2 = (4, 5, 6)
print(MathUtils.vector_add(v1, v2))      # (5, 7, 9)
print(MathUtils.vector_dot(v1, v2))      # 32
print(MathUtils.vector_magnitude((3, 4))) # 5.0

# 序列生成
print(MathUtils.arithmetic_sequence(1, 2, 5))  # [1, 3, 5, 7, 9]
print(MathUtils.geometric_sequence(1, 2, 5))   # [1, 2, 4, 8, 16]
print(MathUtils.linspace(0, 10, 5))             # [0.0, 2.5, 5.0, 7.5, 10.0]

# 数值检查
print(MathUtils.is_prime(97))              # True
print(MathUtils.is_perfect_number(28))     # True
print(MathUtils.is_palindrome_number(12321))  # True
```

## 测试

运行测试：
```bash
python math_utils_test.py
```

## 特性

- ✅ 零外部依赖（仅使用 Python 标准库）
- ✅ 类型注解支持
- ✅ 完整的错误处理
- ✅ 100+ 单元测试覆盖
- ✅ 详细文档字符串

## 许可证

MIT License