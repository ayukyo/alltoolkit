# Polynomial Utils


多项式运算工具模块

提供完整的多项式运算功能，包括：
- 多项式创建与解析
- 四则运算（加减乘除）
- 求值、求导、积分
- 求根（牛顿法、二分法）
- 因式分解（简单情况）
- 多项式插值

零外部依赖，纯 Python 实现。


## 功能

### 类

- **Polynomial**: 多项式类，支持完整的数学运算。

多项式以系数列表形式存储，从低次到高次。
例如：[1, 2, 3] 表示 1 + 2x + 3x²

用法：
    p = Polynomial([1, 2, 3])  # 1 + 2x + 3x²
    p(2)  # 求值：1 + 2*2 + 3*4 = 17
    p
  方法: coefficients, degree, is_zero, divmod, derivative ... (17 个方法)

### 函数

- **from_roots(roots**) - 根据根构造多项式。
- **lagrange_interpolation(points**) - 拉格朗日插值：构造通过给定点的多项式。
- **newton_interpolation(points**) - 牛顿插值：构造通过给定点的多项式（牛顿形式）。
- **chebyshev_polynomial(n**) - 生成 n 阶切比雪夫多项式（第一类）。
- **legendre_polynomial(n**) - 生成 n 阶勒让德多项式。
- **hermite_polynomial(n**) - 生成 n 阶埃尔米特多项式（物理学家版本）。
- **bernstein_polynomial(n, k**) - 生成伯恩斯坦基多项式 B_{n,k}(x) = C(n,k) * x^k * (1-x)^{n-k}。
- **parse(s**) - 解析字符串形式的多项式。
- **horner(coefficients, x**) - 使用霍纳法则计算多项式值。
- **synthetic_division(coefficients, root**) - 综合除法：多项式除以 (x - root)。

... 共 28 个函数

## 使用示例

```python
from mod import from_roots

# 使用 from_roots
result = from_roots()
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
