# Interpolation Utils - 插值工具模块

多种插值算法的 Python 实现，零外部依赖，生产就绪。

## 功能特性

- ✅ **零依赖** - 仅使用 Python 标准库
- ✅ **多方法支持** - 10+ 种插值算法
- ✅ **1D/2D/3D** - 支持一维、二维、三维插值
- ✅ **类封装** - Interpolator 类支持批量插值
- ✅ **边界处理** - 自动处理超出范围的数据
- ✅ **完整测试** - 150+ 测试用例，100% 通过

## 支持的插值方法

| 方法 | 说明 | 适用场景 |
|------|------|----------|
| `linear` | 线性插值 | 简单快速，适合平滑数据 |
| `nearest` | 最近邻插值 | 分类数据、离散值 |
| `lagrange` | 拉格朗日多项式 | 理论分析、精确拟合 |
| `newton` | 牛顿多项式 | 可动态添加点 |
| `cubic_spline` | 三次样条 | 平滑曲线，避免 Runge 现象 |
| `akima` | Akima 插值 | 局部平滑，适合有噪声数据 |
| `idw` | 反距离加权 | 空间插值，地质数据 |
| `piecewise_linear` | 分段线性 | 可控外推 |
| `bilinear` | 双线性插值 | 2D 网格数据 |
| `trilinear` | 三线性插值 | 3D 体积数据 |

## 快速开始

### 线性插值

```python
from interpolation_utils import linear_interpolate

points = [(0, 0), (1, 1), (2, 4)]
result = linear_interpolate(points, 0.5)  # 0.5
result = linear_interpolate(points, 1.5)  # 2.5
```

### 多项式插值

```python
from interpolation_utils import lagrange_interpolate, newton_interpolate

points = [(0, 0), (1, 1), (2, 4), (3, 9)]
result = lagrange_interpolate(points, 1.5)  # 2.25
result = newton_interpolate(points, 1.5)    # 2.25
```

### 样条插值

```python
from interpolation_utils import cubic_spline_interpolate

points = [(0, 0), (1, 1), (2, 0), (3, 1)]
result = cubic_spline_interpolate(points, 1.5)  # 平滑曲线上的点
```

### 2D 插值

```python
from interpolation_utils import bilinear_interpolate

# 四个角点 (x, y, value)
points = [(0, 0, 1), (1, 0, 2), (0, 1, 3), (1, 1, 4)]
result = bilinear_interpolate(points, 0.5, 0.5)  # 2.5
```

### Interpolator 类

```python
from interpolation_utils import Interpolator

points = [(0, 0), (1, 1), (2, 4), (3, 9)]

# 创建插值器
interp = Interpolator(points, method='cubic_spline')

# 单次插值
result = interp.interpolate(1.5)

# 批量插值
results = interp.interpolate_batch([0.5, 1.0, 1.5, 2.0])
```

### 多项式拟合

```python
from interpolation_utils import polynomial_fit, evaluate_polynomial

# 数据点
points = [(0, 0), (1, 1), (2, 4)]

# 二次多项式拟合
coeffs = polynomial_fit(points, 2)

# 计算多项式值
value = evaluate_polynomial(coeffs, 1.5)
```

## API 参考

### 一维插值函数

#### `linear_interpolate(points, x)`
线性插值，自动处理外推。

#### `lagrange_interpolate(points, x)`
拉格朗日多项式插值，通过所有点。

#### `newton_interpolate(points, x)`
牛顿多项式插值，便于添加新点。

#### `cubic_spline_interpolate(points, x, natural=True)`
三次样条插值，自然边界条件。

#### `akima_interpolate(points, x)`
Akima 插值，局部平滑算法。

#### `idw_interpolate(points, x, power=2.0, k=None)`
反距离加权插值。
- `power`: 距离权重幂次（默认 2）
- `k`: 只使用最近的 k 个点

#### `nearest_neighbor_interpolate(points, x)`
最近邻插值，返回最近点的值。

#### `piecewise_linear_interpolate(points, x, extrapolate=True)`
分段线性插值，可控制外推行为。

### 多维插值函数

#### `bilinear_interpolate(points, x, y)`
双线性插值，需要 4 个 2D 网格点。

#### `trilinear_interpolate(points, x, y, z)`
三线性插值，需要 8 个 3D 网格点。

### 多项式拟合

#### `polynomial_fit(points, degree)`
最小二乘法多项式拟合，返回系数。

#### `evaluate_polynomial(coeffs, x)`
计算多项式值，使用 Horner 方法。

### 类

#### `Interpolator(points, method='linear', **kwargs)`
通用插值器类。

**方法:**
- `interpolate(x)`: 单次插值
- `interpolate_batch(xs)`: 批量插值
- 支持直接调用: `interp(x)`

#### `BilinearInterpolator(grid_x, grid_y, values)`
2D 网格插值器。

### 辅助函数

#### `validate_points(points)`
验证点数据格式。

#### `sort_points(points)`
按 x 值排序。

#### `find_interpolation_bounds(points, x)`
找到包含 x 的区间索引。

#### `interpolate_2d_grid(x_coords, y_coords, values, method='bilinear')`
创建 2D 网格插值函数。

## 使用场景

1. **时间序列插值** - 填充缺失的时间点数据
2. **图像处理** - 图像缩放、像素插值
3. **科学计算** - 实验数据处理、曲线拟合
4. **地理信息** - GPS轨迹平滑、位置估计
5. **3D 渲染** - 体积数据插值
6. **金融分析** - 股票价格插值、预测
7. **温度场** - 空间温度分布计算

## 测试

```bash
python interpolation_utils_test.py
```

测试覆盖：
- 基本功能测试
- 边界值测试
- 数值稳定性测试
- 一致性测试（不同方法结果一致）
- 异常处理测试

## 性能特点

| 方法 | 时间复杂度 | 空间复杂度 | 稳定性 |
|------|------------|------------|--------|
| linear | O(n) | O(1) | ✅ 高 |
| nearest | O(n) | O(1) | ✅ 高 |
| lagrange | O(n²) | O(1) | ⚠️ 中 |
| newton | O(n²) | O(n²) | ⚠️ 中 |
| cubic_spline | O(n) | O(n) | ✅ 高 |
| akima | O(n) | O(n) | ✅ 高 |
| idw | O(n) | O(1) | ✅ 高 |

## 限制

- 拉格朗日和牛顿多项式在高阶时可能出现 Runge 现象
- 三次样条需要至少 3 个点
- 双线性插值需要恰好 4 个网格点
- 三线性插值需要恰好 8 个网格点

## License

MIT License

## 版本

- v1.0.0 - 初始版本（2026-05-03）