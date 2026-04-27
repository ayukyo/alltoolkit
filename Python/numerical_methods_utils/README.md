# Numerical Methods Utils


AllToolkit - Python Numerical Methods Utilities

A comprehensive numerical methods library providing root finding, 
numerical integration, differentiation, interpolation, and optimization.
Zero external dependencies - pure Python standard library implementation.

Author: AllToolkit
License: MIT


## 功能

### 类

- **RootResult**: Result of root finding algorithm
- **IntegrationResult**: Result of numerical integration
- **InterpolationResult**: Result of interpolation

### 函数

- **bisection(f, a, b**, ...) - Find root of function f in interval [a, b] using bisection method.
- **newton_raphson(f, df, x0**, ...) - Find root of function f using Newton-Raphson method.
- **secant_method(f, x0, x1**, ...) - Find root of function f using the secant method.
- **brent_method(f, a, b**, ...) - Find root using Brent's method (combines bisection, secant, and inverse quadratic).
- **trapezoidal_rule(f, a, b**, ...) - Numerical integration using the trapezoidal rule.
- **trapezoidal_rule_simple(f, a, b**, ...) - Simple trapezoidal rule without error estimate.
- **simpsons_rule(f, a, b**, ...) - Numerical integration using Simpson's rule.
- **simpsons_rule_simple(f, a, b**, ...) - Simple Simpson's rule without error estimate.
- **adaptive_simpson(f, a, b**, ...) - Adaptive Simpson's rule with automatic interval subdivision.
- **gaussian_quadrature(f, a, b**, ...) - Numerical integration using Gaussian quadrature.

... 共 27 个函数

## 使用示例

```python
from mod import bisection

# 使用 bisection
result = bisection()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
