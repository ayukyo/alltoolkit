# Math Utils - C 语言数学工具库

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![C Standard](https://img.shields.io/badge/C-C99-blue.svg)](https://en.wikipedia.org/wiki/C99)

一个轻量级、零外部依赖的 C 语言数学工具库，提供常用的数学运算、统计函数、几何计算和数论功能。

## ✨ 功能特性

### 🔢 基础运算
- **范围限制**: `clamp_int`, `clamp_double` - 将值限制在指定范围内
- **最值查找**: `max_int`, `min_int`, `max_double`, `min_double` - 支持数组和单值
- **交换**: `swap_int`, `swap_double` - 安全的值交换
- **绝对值**: `abs_int`, `abs_double` - 整数和浮点数绝对值
- **符号函数**: `sign_int`, `sign_double` - 返回 -1, 0, 1

### 📐 幂与根运算
- **整数幂**: `power_int` - 快速幂运算 (支持大指数)
- **整数平方根**: `isqrt` - 牛顿迭代法实现
- **完全平方数检查**: `is_perfect_square`

### 📏 几何计算
- **距离**: `distance_2d`, `distance_3d` - 欧几里得距离
- **圆**: `circle_area`, `circle_circumference`
- **矩形**: `rectangle_area`, `rectangle_perimeter`
- **三角形**: `triangle_area` - 海伦公式
- **球体**: `sphere_volume`, `sphere_surface_area`

### 📊 统计函数
- **求和**: `sum_int_array`, `sum_double_array`
- **均值**: `mean_int_array`, `mean_double_array`
- **中位数**: `median_int_array`, `median_double_array`
- **方差**: `variance_int_array`, `variance_double_array`
- **标准差**: `std_dev_int_array`, `std_dev_double_array`

### 🔬 数论函数
- **质数检测**: `is_prime` - 优化的试除法
- **最大公约数**: `gcd` - 欧几里得算法
- **最小公倍数**: `lcm`
- **阶乘**: `factorial` - 支持到 20!
- **斐波那契数列**: `fibonacci` - 迭代实现，避免递归栈溢出
- **模运算**: `mod` - 正确处理负数
- **模幂运算**: `mod_power` - 快速模幂，用于密码学

### ✔️ 数值检查
- **奇偶性**: `is_even`, `is_odd`
- **2的幂检查**: `is_power_of_two`
- **浮点数近似**: `is_near_zero`, `is_approx_equal`

### 🎯 范围与序列
- **范围映射**: `map_range` - 将值从一个范围映射到另一个范围
- **线性插值**: `lerp` - 平滑过渡
- **等差数列**: `range_int` - 生成整数序列

### 📐 三角函数辅助
- **角度转弧度**: `degrees_to_radians`
- **弧度转角度**: `radians_to_degrees`

## 🚀 快速开始

### 编译

```bash
# 编译测试
gcc -o math_utils_test math_utils_test.c math_utils.c -lm

# 编译示例
gcc -o example example.c math_utils.c -lm

# 运行测试
./math_utils_test

# 运行示例
./example
```

### 基本用法

```c
#include <stdio.h>
#include "math_utils.h"

int main(void) {
    // 基础运算
    printf("clamp_int(15, 0, 10) = %d\n", clamp_int(15, 0, 10));
    printf("max_int(10, 20) = %d\n", max_int(10, 20));
    
    // 数组统计
    int scores[] = {85, 92, 78, 95, 88};
    size_t n = sizeof(scores) / sizeof(scores[0]);
    printf("平均分: %.2f\n", mean_int_array(scores, n));
    printf("最高分: %d\n", max_int_array(scores, n));
    
    // 几何计算
    printf("圆面积 (r=5): %.2f\n", circle_area(5));
    printf("两点距离: %.2f\n", distance_2d(0, 0, 3, 4));
    
    // 数论函数
    printf("gcd(48, 18) = %u\n", gcd(48, 18));
    printf("5! = %llu\n", factorial(5));
    printf("fib(10) = %llu\n", fibonacci(10));
    
    // 范围映射
    double celsius = 25.0;
    double fahrenheit = map_range(celsius, 0, 100, 32, 212);
    printf("%.0f°C = %.1f°F\n", celsius, fahrenheit);
    
    return 0;
}
```

## 📋 API 参考

### 基础运算

| 函数 | 描述 |
|------|------|
| `int clamp_int(int value, int min, int max)` | 限制整数在范围内 |
| `double clamp_double(double value, double min, double max)` | 限制浮点数在范围内 |
| `int max_int(int a, int b)` | 返回两个整数的最大值 |
| `int max_int_array(const int* arr, size_t size)` | 返回数组的最大值 |
| `int min_int(int a, int b)` | 返回两个整数的最小值 |
| `int min_int_array(const int* arr, size_t size)` | 返回数组的最小值 |
| `void swap_int(int* a, int* b)` | 交换两个整数 |
| `int abs_int(int value)` | 整数绝对值 |
| `int sign_int(int value)` | 返回符号 (-1, 0, 1) |

### 数论函数

| 函数 | 描述 |
|------|------|
| `bool is_prime(unsigned int n)` | 检查是否为质数 |
| `unsigned int gcd(unsigned int a, unsigned int b)` | 最大公约数 |
| `unsigned int lcm(unsigned int a, unsigned int b)` | 最小公倍数 |
| `unsigned long long factorial(unsigned int n)` | 阶乘 (支持到 20!) |
| `unsigned long long fibonacci(unsigned int n)` | 斐波那契数列第 n 项 |
| `int mod(int a, int b)` | 模运算 (正确处理负数) |
| `long long mod_power(long long base, long long exp, long long mod)` | 模幂运算 |

### 统计函数

| 函数 | 描述 |
|------|------|
| `long long sum_int_array(const int* arr, size_t size)` | 数组求和 |
| `double mean_int_array(const int* arr, size_t size)` | 数组平均值 |
| `double median_int_array(int* arr, size_t size)` | 数组中位数 (会修改原数组) |
| `double variance_int_array(const int* arr, size_t size)` | 方差 |
| `double std_dev_int_array(const int* arr, size_t size)` | 标准差 |

## 🧪 测试

运行完整的测试套件：

```bash
gcc -o math_utils_test math_utils_test.c math_utils.c -lm
./math_utils_test
```

测试覆盖：
- ✅ 基础运算（clamp, max, min, swap, abs, sign）
- ✅ 幂与根运算（power, sqrt, perfect square）
- ✅ 几何计算（distance, area, volume）
- ✅ 统计函数（sum, mean, median, variance, std_dev）
- ✅ 数论函数（prime, gcd, lcm, factorial, fibonacci）
- ✅ 数值检查（even, odd, power of two）
- ✅ 范围映射与插值
- ✅ 角度转换
- ✅ 边界情况

## 📁 文件结构

```
math_utils/
├── math_utils.h        # 头文件（API 声明）
├── math_utils.c        # 实现文件
├── math_utils_test.c   # 测试文件
├── example.c           # 使用示例
└── README.md           # 本文档
```

## ⚡ 性能特点

- **零外部依赖**: 仅使用标准 C 库
- **内存高效**: 无动态内存分配
- **快速幂**: 使用二分幂算法，O(log n) 时间复杂度
- **优化的质数检测**: 跳过偶数，O(√n) 时间复杂度
- **迭代斐波那契**: 避免递归栈溢出，O(n) 时间复杂度

## 📝 注意事项

1. `median_int_array` 和 `median_double_array` 会修改原数组（用于排序）
2. `factorial` 函数在 n > 20 时返回 0（溢出保护）
3. 几何函数使用 `M_PI` 的近似值：`3.14159265358979323846`
4. 所有数组函数都有 NULL 和空数组检查

## 📜 许可证

MIT License - 详见 LICENSE 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**作者**: AllToolkit  
**版本**: 1.0.0  
**日期**: 2026-05-24