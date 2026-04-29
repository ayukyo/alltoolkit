# Expression Parser Utils

安全的数学表达式解析和求值工具，无需使用 `eval()` 函数。

## 功能特性

- ✅ **安全解析** - 不使用 `eval()`，完全自实现词法分析和语法分析
- ✅ **四则运算** - 加减乘除、幂运算、取模、整除
- ✅ **比较运算** - ==, !=, <, <=, >, >=
- ✅ **逻辑运算** - and, or, not（支持 &&, ||, ! 别名）
- ✅ **变量支持** - 表达式中使用变量
- ✅ **函数调用** - 内置 30+ 数学函数，支持自定义函数
- ✅ **字符串支持** - 字符串字面量和拼接
- ✅ **表达式验证** - 语法检查
- ✅ **变量提取** - 从表达式中提取变量名

## 快速开始

```python
from expression_parser_utils import safe_eval

# 基本运算
result = safe_eval("2 + 3 * 4")  # 14
result = safe_eval("(2 + 3) * 4")  # 20
result = safe_eval("2 ** 10")  # 1024

# 使用变量
result = safe_eval("x + y * z", variables={'x': 1, 'y': 2, 'z': 3})  # 7

# 内置数学函数
result = safe_eval("sqrt(16)")  # 4.0
result = safe_eval("sin(pi/2)", variables={'pi': 3.14159})  # 1.0
result = safe_eval("max(1, 2, 3, 4, 5)")  # 5

# 复杂表达式
result = safe_eval(
    "sqrt(x**2 + y**2) + abs(z)",
    variables={'x': 3, 'y': 4, 'z': -5}
)  # 10.0

# 逻辑表达式
result = safe_eval("x > 0 and y < 10", variables={'x': 5, 'y': 3})  # True

# 自定义函数
result = safe_eval(
    "double(x) + triple(y)",
    variables={'x': 2, 'y': 3},
    functions={
        'double': lambda x: x * 2,
        'triple': lambda x: x * 3
    }
)  # 13
```

## 支持的运算符

| 运算符 | 说明 | 优先级 |
|--------|------|--------|
| `**` | 幂运算 | 最高 |
| `*`, `/`, `//`, `%` | 乘、除、整除、取模 | 高 |
| `+`, `-` | 加、减 | 中 |
| `<`, `<=`, `>`, `>=` | 比较 | 低 |
| `==`, `!=` | 相等比较 | 低 |
| `not`, `!` | 逻辑非 | 低 |
| `and`, `&&` | 逻辑与 | 最低 |
| `or`, `\|\|` | 逻辑或 | 最低 |

## 内置函数

### 三角函数
`sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`

### 双曲函数
`sinh`, `cosh`, `tanh`

### 指数对数
`exp`, `log`, `log10`, `log2`, `sqrt`, `pow`

### 取整函数
`floor`, `ceil`, `round`, `trunc`

### 数学工具
`abs`, `min`, `max`, `sum`, `avg`, `mod`, `factorial`

### 检查函数
`isnan`, `isinf`

### 角度转换
`degrees`, `radians`

### 工具函数
`sign`, `clamp`, `lerp`, `len`

## 高级用法

### 使用 ExpressionParser 类

```python
from expression_parser_utils import ExpressionParser

# 创建解析器（可预置变量和函数）
parser = ExpressionParser(
    variables={'pi': 3.14159},
    functions={'cube': lambda x: x ** 3}
)

# 解析表达式
ast = parser.parse("sin(pi/2) + cube(2)")

# 计算结果
result = parser.evaluate(ast)  # 9.0

# 可以在计算时覆盖变量
result = parser.evaluate(ast, variables={'pi': 3.14})
```

### 表达式验证

```python
from expression_parser_utils import validate_expression

is_valid, error = validate_expression("1 + 2 * 3")
# (True, None)

is_valid, error = validate_expression("1 + ")
# (False, "Position 3: Unexpected token: None")
```

### 提取变量

```python
from expression_parser_utils import extract_variables

variables = extract_variables("sqrt(x*x + y*y) + z")
# {'x', 'y', 'z'}
```

### MathFunctions 类

```python
from expression_parser_utils import MathFunctions

# 创建函数集合
funcs = MathFunctions()  # 默认包含所有内置函数

# 添加自定义函数
funcs.add('double', lambda x: x * 2)

# 检查函数是否存在
funcs.has('sin')  # True

# 获取函数列表
funcs.names()  # ['sin', 'cos', 'sqrt', ...]

# 仅使用自定义函数
custom_funcs = MathFunctions(include_builtins=False)
custom_funcs.add('my_func', lambda x: x + 1)
```

## 测试

```bash
# 运行测试
python -m unittest expression_parser_utils_test.py

# 或直接运行
python expression_parser_utils_test.py
```

## 安全性

本模块**不使用** Python 的 `eval()` 函数，而是实现了完整的词法分析器和递归下降解析器，确保表达式求值的安全性。

## 作者

AllToolkit Auto-Generator

## 日期

2026-04-29