# Fibonacci Utils


Fibonacci Utils - 斐波那契数列工具集

提供斐波那契数列的生成、计算、验证等功能。
零外部依赖，纯Python实现。

功能：
- 生成斐波那契数列
- 计算第N个斐波那契数（迭代/递归/矩阵快速幂）
- 验证数字是否为斐波那契数
- 找到最接近的斐波那契数
- 斐波那契编码（Zeckendorf表示）
- 黄金比例相关计算


## 功能

### 类

- **FibonacciUtils**: 斐波那契数列工具类
  方法: generate, nth_iterative, nth_recursive, nth_matrix, nth_binet ... (19 个方法)

### 函数

- **generate(n**) - 生成前n个斐波那契数
- **nth(n**) - 计算第n个斐波那契数（自动选择最优算法）
- **is_fibonacci(num**) - 判断是否为斐波那契数
- **zeckendorf(num**) - Zeckendorf表示
- **golden_ratio(precision**) - 计算黄金比例近似值
- **generate(n**) - 生成前n个斐波那契数
- **nth_iterative(n**) - 使用迭代法计算第n个斐波那契数
- **nth_recursive(n**) - 使用递归法计算第n个斐波那契数（带记忆化）
- **nth_matrix(n**) - 使用矩阵快速幂计算第n个斐波那契数
- **nth_binet(n**) - 使用比内公式（Binet's formula）计算第n个斐波那契数

... 共 29 个函数

## 使用示例

```python
from mod import generate

# 使用 generate
result = generate()
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
