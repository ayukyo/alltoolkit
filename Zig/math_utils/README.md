# Zig Math Utils

一个全面的 Zig 数学工具库，提供丰富的数学运算功能，零外部依赖。

## 功能特性

### 基本运算
- `abs` / `absInt` - 绝对值（浮点/整数）
- `min` / `max` - 最小值/最大值（泛型）
- `clamp` - 将值限制在范围内
- `sign` - 符号函数（-1, 0, 1）
- `approxEquals` - 近似相等比较
- `isNearZero` - 检查是否接近零

### 常量
- `PI` - 圆周率
- `E` - 自然常数
- `PHI` - 黄金比例
- `SQRT2` - 根号二
- `LN2` / `LN10` - 对数常量

### 舍入函数
- `floor` - 向下取整
- `ceil` - 向上取整
- `round` - 四舍五入
- `trunc` - 截断（取整数部分）
- `roundTo` - 指定小数位舍入

### 幂和根
- `pow` / `powInt` - 幂运算（浮点/整数）
- `sqrt` - 平方根（Newton-Raphson 算法）
- `cbrt` - 立方根
- `nthRoot` - n 次方根
- `isPerfectSquare` - 检查是否为完全平方数
- `inverseSquare` - 平方倒数（1/x²）

### 三角函数
- `degToRad` / `radToDeg` - 角度弧度转换
- `normalizeAngle` - 将角度归一化到 [0, 2π)
- `sin` / `cos` / `tan` - 三角函数（Taylor 级数）
- `arcsin` / `arccos` / `arctan` - 反三角函数
- `arctan2` - 四象限反正切

### 对数和指数
- `ln` - 自然对数（Newton-Raphson）
- `log10` / `log2` - 常用对数/二进制对数
- `log` - 任意底对数
- `expNatural` - 自然指数（Taylor 级数）
- `exp` - 通用指数函数

### 数论
- `isPrime` - 素数检测（确定性算法）
- `gcd` - 最大公约数（欧几里得算法）
- `lcm` - 最小公倍数
- `factorial` / `factorialF` - 阶乘（整数/浮点）
- `fibonacci` - 斐波那契数
- `binomial` - 二项式系数（n choose k）
- `isEven` / `isOdd` - 奇偶检测
- `modPositive` - 正模运算

### 统计
- `mean` - 平均值
- `median` - 中位数（需要 allocator）
- `variance` / `sampleVariance` - 方差（总体/样本）
- `stdDev` / `sampleStdDev` - 标准差（总体/样本）
- `sum` - 求和
- `minVal` / `maxVal` - 最小/最大值
- `range` - 极差

### 插值
- `lerp` - 线性插值
- `inverseLerp` - 逆线性插值
- `remap` / `map` - 范围映射
- `smoothstep` - 平滑插值（三次 Hermite）
- `smootherstep` - 更平滑插值（五次）
- `hermite` - Hermite 插值
- `quintic` - 五次插值
- `step` - 阶跃函数

### 工具函数
- `percentage` - 计算百分比
- `percentOf` - 计算百分比对应的值
- `wrap` - 循环范围
- `pingPong` - 来回往复
- `distance2D` / `distance3D` - 两点距离
- `between` / `betweenExclusive` - 范围检测
- `linearToDb` / `dbToLinear` - 线性/分贝转换

## 使用方法

### 添加依赖

在 `build.zig.zon` 中添加：

```zig
.{
    .dependencies = .{
        .math_utils = .{
            .path = "../math_utils",
        },
    },
}
```

### 在 build.zig 中导入

```zig
const math_utils_dep = b.dependency("math_utils", .{
    .target = target,
    .optimize = optimize,
});

exe.root_module.addImport("math_utils", math_utils_dep.module("math_utils"));
```

### 代码示例

```zig
const std = @import("std");
const math_utils = @import("math_utils");

pub fn main() !void {
    // 基本运算
    const abs_val = math_utils.abs(-5.0); // 5.0
    const clamped = math_utils.clamp(i32, 100, 0, 50); // 50
    
    // 幂运算
    const power = math_utils.pow(2.0, 8.0); // 256.0
    const root = math_utils.sqrt(144.0); // 12.0
    
    // 三角函数
    const angle = math_utils.degToRad(45.0);
    const sin_val = math_utils.sin(angle); // ~0.707
    const cos_val = math_utils.cos(angle); // ~0.707
    
    // 数论
    if (math_utils.isPrime(17)) {
        std.debug.print("17 is prime!\n", .{}); 
    }
    const gcd_val = math_utils.gcd(48, 18); // 6
    const fact = math_utils.factorial(6); // 720
    
    // 统计
    const data = [_]f64{ 1.0, 2.0, 3.0, 4.0, 5.0 };
    const avg = math_utils.mean(&data); // 3.0
    const dev = math_utils.stdDev(&data); // ~1.41
    
    // 插值
    const interp = math_utils.lerp(0.0, 100.0, 0.5); // 50.0
    const mapped = math_utils.remap(5.0, 0.0, 10.0, 0.0, 100.0); // 50.0
    
    // 工具函数
    const dist = math_utils.distance2D(0.0, 0.0, 3.0, 4.0); // 5.0
    const db = math_utils.linearToDb(0.1); // -20 dB
}
```

## 运行测试

```bash
cd Zig/math_utils
zig build test
```

## 运行示例

```bash
zig build example
```

## 特性说明

- **零依赖**: 仅使用 Zig 标准库，无外部依赖
- **纯算法实现**: 所有数学函数使用经典算法（Newton-Raphson、Taylor 级数等）
- **类型安全**: 泛型设计，支持多种数值类型
- **精度可控**: 提供自定义精度常量（`EPSILON`）
- **性能优化**: 迭代算法有合理的收敛上限，避免无限循环

## 性能说明

| 函数 | 算法 | 收敛特性 |
|------|------|----------|
| `sqrt` | Newton-Raphson | 二次收敛，最多 100 次迭代 |
| `sin/cos` | Taylor 级数 | 精度 EPSILON（1e-10） |
| `ln` | Newton-Raphson | 二次收敛，最多 100 次迭代 |
| `exp` | Taylor 级数 | 精度 EPSILON |

## 许可证

MIT License

## 版本历史

- v1.0.0 (2026-05-16) - 初始版本，包含 60+ 数学函数