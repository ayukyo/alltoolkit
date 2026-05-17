# Fortran Interpolation Utils

数值插值工具模块，提供多种插值算法实现，零外部依赖。

## 功能特性

- **线性插值** (Linear Interpolation)
  - 单点插值
  - 批量数组插值
  - 自动外推处理

- **拉格朗日插值** (Lagrange Interpolation)
  - 多项式插值
  - 适合任意分布数据点

- **牛顿插值** (Newton Interpolation)
  - 差商系数计算
  - 高效的多项式插值

- **三次样条插值** (Cubic Spline Interpolation)
  - 自然样条边界条件
  - 平滑曲线拟合
  - 面向对象接口

- **双线性插值** (Bilinear Interpolation)
  - 2D 网格插值
  - 图像处理应用

## 编译

```bash
# 编译模块和测试
gfortran -c interpolation_utils.f90
gfortran -o test_interpolation interpolation_utils.o test_interpolation_utils.f90

# 编译示例
gfortran -o example_interpolation interpolation_utils.o example_interpolation.f90
```

## 使用示例

### 线性插值

```fortran
use interpolation_utils

! 单点插值
y = linear_interp(0.0d0, 0.0d0, 10.0d0, 100.0d0, 5.0d0)
! 结果: y = 50.0

! 数组插值
real(8) :: x_data(5), y_data(5), x_vals(3), y_results(3)
x_data = [0.0d0, 1.0d0, 2.0d0, 3.0d0, 4.0d0]
y_data = [0.0d0, 1.0d0, 4.0d0, 9.0d0, 16.0d0]
x_vals = [0.5d0, 1.5d0, 2.5d0]
y_results = linear_interp_array(x_data, y_data, x_vals)
```

### 三次样条插值

```fortran
use interpolation_utils

type(cubic_spline) :: spline
real(8) :: x_data(5), y_data(5)

x_data = [0.0d0, 1.0d0, 2.0d0, 3.0d0, 4.0d0]
y_data = [0.0d0, 1.0d0, 4.0d0, 9.0d0, 16.0d0]

! 初始化样条
call spline%init(x_data, y_data)

! 插值
y = spline%interp(2.5d0)

! 释放内存
call spline%free()
```

### 拉格朗日插值

```fortran
use interpolation_utils

real(8) :: x_data(4), y_data(4)

x_data = [0.0d0, 1.0d0, 2.0d0, 3.0d0]
y_data = [0.0d0, 1.0d0, 8.0d0, 27.0d0]  ! y = x^3

y = lagrange_interp(x_data, y_data, 1.5d0)
! 结果接近 3.375
```

### 牛顿插值

```fortran
use interpolation_utils

real(8) :: x_data(4), y_data(4), coeffs(4)

x_data = [0.0d0, 1.0d0, 2.0d0, 3.0d0]
y_data = [1.0d0, 2.718d0, 7.389d0, 20.086d0]  ! e^x 近似

! 获取差商系数
coeffs = newton_coefficients(x_data, y_data)

! 插值
y = newton_interp(x_data, y_data, 1.5d0)
```

### 双线性插值

```fortran
use interpolation_utils

! 2D 网格插值
! z11 = f(x1, y1), z12 = f(x1, y2)
! z21 = f(x2, y1), z22 = f(x2, y2)

z = bilinear_interp(x1, x2, y1, y2, z11, z12, z21, z22, x, y)
```

## API 参考

### linear_interp(x0, y0, x1, y1, x) → y

单点线性插值。

| 参数 | 类型 | 描述 |
|------|------|------|
| x0, y0 | real(8) | 第一个数据点 |
| x1, y1 | real(8) | 第二个数据点 |
| x | real(8) | 目标 x 值 |

### linear_interp_array(x_data, y_data, x) → y

批量线性插值。

### lagrange_interp(x_data, y_data, x) → y

拉格朗日多项式插值。

### newton_coefficients(x_data, y_data) → coeffs

计算牛顿差商系数。

### newton_interp(x_data, y_data, x) → y

牛顿多项式插值。

### cubic_spline 类型

| 方法 | 描述 |
|------|------|
| init(x_data, y_data) | 初始化样条 |
| interp(x) → y | 插值计算 |
| free() | 释放内存 |

### bilinear_interp(x1, x2, y1, y2, z11, z12, z21, z22, x, y) → z

双线性 2D 插值。

## 精度说明

- 所有计算使用双精度 `real(8)`
- 样条插值使用 Thomas 算法求解三对角系统
- 比较阈值: `1.0d-15`

## 测试

运行测试程序：

```bash
./test_interpolation
```

测试覆盖：
- 线性插值（中点、偏移点、外推）
- 数组插值
- 拉格朗日插值
- 牛顿插值
- 三次样条插值
- 双线性插值

## 作者

AllToolkit

## 日期

2026-05-18