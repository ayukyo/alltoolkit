# math_utils

C++ 数学工具库 - 零依赖、现代 C++17 实现

## 概述

提供 40+ 个常用数学函数，涵盖基础数学运算、统计计算、几何计算、数论函数等。

## 核心功能

### 常量
- `PI` - 圆周率
- `E` - 自然常数
- `PHI` - 黄金比例
- `SQRT2`, `SQRT3` - 常用平方根
- `DEG_TO_RAD`, `RAD_TO_DEG` - 角度弧度转换因子

### 基础数学运算
- `abs()` - 绝对值
- `max()`, `min()` - 最大/最小值
- `clamp()` - 数值范围限制
- `lerp()` - 线性插值
- `smoothstep()` - 平滑插值
- `square()`, `cube()` - 平方/立方
- `power()` - 整数幂运算
- `sign()` - 符号函数
- `distance()` - 2D/3D 点距离计算

### 统计计算
- `mean()` - 平均值
- `median()` - 中位数
- `variance()`, `sampleVariance()` - 方差
- `stdDev()`, `sampleStdDev()` - 标准差
- `covariance()` - 协方差
- `correlation()` - 皮尔逊相关系数
- `mode()` - 众数
- `range()` - 极差
- `sum()`, `product()` - 总和/乘积

### 几何计算
- `circleArea()`, `circleCircumference()` - 圆形面积/周长
- `rectangleArea()`, `rectanglePerimeter()` - 矩形面积/周长
- `triangleArea()` - 三角形面积（海伦公式/底高公式）
- `sphereVolume()`, `sphereSurfaceArea()` - 球体体积/表面积
- `cylinderVolume()` - 圆柱体体积
- `pointInCircle()`, `pointInRect()` - 点包含判断

### 数论函数
- `gcd()`, `lcm()` - 最大公约数/最小公倍数
- `isPrime()` - 素数判断
- `sieveOfEratosthenes()` - 埃拉托斯特尼筛法
- `factorial()` - 阶乘
- `permutation()`, `combination()` - 排列/组合数
- `fibonacci()` - 斐波那契数列

### 三角函数扩展
- `degToRad()`, `radToDeg()` - 角度弧度转换
- `safeAsin()`, `safeAcos()` - 安全反三角函数
- `sec()`, `csc()`, `cot()` - 正割/余割/余切

### 数值计算
- `sqrtNewton()` - 牛顿法平方根
- `bisectionMethod()` - 二分法求根
- `trapezoidalIntegration()` - 梯形法数值积分
- `simpsonIntegration()` - 辛普森法数值积分

### 向量操作
- `vectorAdd()`, `vectorSub()` - 向量加减
- `vectorScale()` - 向量缩放
- `dotProduct()` - 向量点积
- `vectorMagnitude()` - 向量模长
- `vectorNormalize()` - 向量归一化
- `crossProduct3D()` - 3D向量叉积
- `vectorAngle()` - 向量夹角

### 比较与映射
- `approxEqual()` - 浮点数近似相等
- `isZero()` - 浮点数零判断
- `inRange()` - 范围判断
- `mapRange()` - 范围映射
- `normalize()` - 归一化到 [0, 1]

## 使用方法

```cpp
#include "math_utils.hpp"
using namespace alltoolkit::math_utils;

// 基础运算
double value = clamp(150, 0, 100);  // 100
double interp = lerp(0.0, 100.0, 0.5);  // 50.0

// 统计
std::vector<double> data = {85, 90, 78, 92};
double avg = mean(data);
double std = stdDev(data);

// 数论
int g = gcd(48, 18);  // 6
bool prime = isPrime(17);  // true
unsigned long long fact = factorial(10);  // 3628800

// 几何
double area = circleArea(5.0);  // 25π
double vol = sphereVolume(3.0);  // 36π

// 向量
std::vector<double> a = {1, 2, 3};
std::vector<double> b = {4, 5, 6};
double dot = dotProduct(a, b);  // 32
```

## 编译与测试

```bash
# 编译测试
cd C++/math_utils
g++ -std=c++17 -o math_utils_test math_utils_test.cpp

# 运行测试
./math_utils_test

# 编译示例
g++ -std=c++17 -I.. -o math_utils_example examples/math_utils_example.cpp

# 运行示例
./math_utils_example
```

## 设计特点

- **Header-only**: 仅需包含 `math_utils.hpp`，无需额外编译
- **零依赖**: 仅使用 C++17 标准库
- **类型安全**: 支持泛型，自动推导类型
- **现代 C++**: 使用 `constexpr`, `nodiscard`, 模板等特性
- **异常安全**: 边界检查和异常处理

## 文件结构

```
math_utils/
├── math_utils.hpp      # 主头文件（header-only）
├── math_utils_test.cpp # 测试文件
├── README.md           # 本文档
└── examples/
    └── math_utils_example.cpp # 使用示例
```

## 版本信息

- 版本: 1.0.0
- 日期: 2026-04-24
- 作者: AllToolkit
- 标准: C++17