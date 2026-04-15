# Safe Expression Evaluator - 安全表达式求值工具

提供安全的数学和逻辑表达式求值功能，无需使用 Python 内置的 `eval()`。

## 特点

- ✅ **零外部依赖** - 纯 Python 标准库实现
- ✅ **AST 解析** - 不使用 eval/exec，安全性高
- ✅ **可配置的安全选项** - 灵活控制允许的操作
- ✅ **详细的错误信息** - 精准定位问题
- ✅ **支持数学函数** - 三角函数、对数、指数等
- ✅ **支持布尔运算** - and、or、not、比较运算符
- ✅ **支持变量替换** - 动态变量和常量
- ✅ **支持自定义函数** - 扩展能力强

## 快速开始

### 基础使用

```python
from safe_eval_utils import safe_eval

# 简单数学运算
result = safe_eval("2 + 3 * 4")  # 14

# 使用变量
result = safe_eval("x + y", variables={"x": 10, "y": 5})  # 15

# 使用函数
result = safe_eval("max(1, 2, 3)")  # 3
result = safe_eval("sqrt(16)")  # 4.0
```

### 创建求值器

```python
from safe_eval_utils import SafeEvaluator

# 创建求值器
evaluator = SafeEvaluator()

# 设置变量
evaluator.set_variable("x", 10)
evaluator.set_variable("y", 5)

# 求值表达式
result = evaluator.eval("x + y * 2")  # 20

# 自定义函数
evaluator.set_function("square", lambda x: x**2)
result = evaluator.eval("square(5)")  # 25
```

### 安全求值

```python
from safe_eval_utils import safe_eval_with_result

# 返回结果对象，不抛出异常
result = safe_eval_with_result("2 + 3")
if result.success:
    print(f"结果: {result.value}")  # 结果: 5
else:
    print(f"错误: {result.error}")

# 错误处理示例
result = safe_eval_with_result("unknown_var")
print(result.success)  # False
print(result.error)    # "Unknown variable: 'unknown_var'"
```

## 核心功能

### 支持的运算符

| 类型 | 运算符 |
|------|--------|
| 算术 | `+`, `-`, `*`, `/`, `//`, `%`, `**` |
| 比较 | `==`, `!=`, `<`, `<=`, `>`, `>=`, `is`, `is not`, `in`, `not in` |
| 布尔 | `and`, `or`, `not` |
| 位运算 | `&`, `|`, `^`, `~`, `<<`, `>>` |
| 一元 | `-`, `+`, `not`, `~` |

### 支持的函数

**数学函数**:
- `abs`, `round`, `min`, `max`, `sum`
- `sqrt`, `pow`, `log`, `log10`, `log2`, `exp`
- `sin`, `cos`, `tan`, `asin`, `acos`, `atan`
- `sinh`, `cosh`, `tanh`
- `floor`, `ceil`, `trunc`
- `factorial`, `gcd`, `lcm`

**类型转换**:
- `int`, `float`, `str`, `bool`
- `len`, `type`, `isinstance`

**字符串函数**:
- `upper`, `lower`, `strip`, `capitalize`, `title`
- `replace`, `split`, `join`
- `startswith`, `endswith`, `find`, `count`
- `center`, `ljust`, `rjust`, `zfill`

### 支持的常量

- `pi`, `e`, `tau`, `inf`, `nan`
- `True`, `False`, `None`

### 数据结构

支持列表、元组、字典、集合：

```python
safe_eval("[1, 2, 3]")  # [1, 2, 3]
safe_eval("(1, 2, 3)")  # (1, 2, 3)
safe_eval("{'a': 1}")   # {'a': 1}
safe_eval("{1, 2, 3}")  # {1, 2, 3}
```

支持下标和切片：

```python
safe_eval("[1, 2, 3][0]")      # 1
safe_eval("[1, 2, 3][1:2]")    # [2]
safe_eval("'hello'[0]")        # 'h'
safe_eval("'hello'[1:4]")      # 'ell'
```

## 专用求值器

### MathEvaluator - 数学专用

```python
from safe_eval_utils import MathEvaluator

evaluator = MathEvaluator()
result = evaluator.eval("sin(pi/2)")  # 1.0
result = evaluator.eval("sqrt(16) + log(e)")  # 5.0
```

### StringEvaluator - 字符串专用

```python
from safe_eval_utils import StringEvaluator

evaluator = StringEvaluator()
result = evaluator.eval("upper('hello')")  # 'HELLO'
result = evaluator.eval("replace('hello world', 'world', 'python')")  # 'hello python'
```

### ConditionEvaluator - 条件专用

```python
from safe_eval_utils import ConditionEvaluator

evaluator = ConditionEvaluator()
result = evaluator.eval("age >= 18 and score > 60", 
                       variables={"age": 20, "score": 85})  # True

# 过滤列表
items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
filtered = evaluator.filter_list(items, "item > 5")  # [6, 7, 8, 9, 10]
```

### TemplateEvaluator - 模板求值

```python
from safe_eval_utils import TemplateEvaluator

evaluator = TemplateEvaluator()
result = evaluator.eval("Result: ${2 + 3}")  # 'Result: 5'
result = evaluator.eval("${x} + ${y} = ${x + y}", 
                       variables={"x": 2, "y": 3})  # '2 + 3 = 5'
```

### BatchEvaluator - 批量求值

```python
from safe_eval_utils import BatchEvaluator

evaluator = BatchEvaluator()
evaluator.set("x", 10)

# 批量求值
results = evaluator.eval_all(["x + 1", "x * 2", "x - 5"])  # [11, 20, 5]

# 安全批量求值
results = evaluator.eval_all_safe(["2 + 3", "unknown", "4 * 5"])
for r in results:
    if r.success:
        print(r.value)
```

## 表达式分析

```python
from safe_eval_utils import ExpressionParser

parser = ExpressionParser()

# 获取表达式中引用的变量
variables = parser.get_variables("x + y * z")  # {'x', 'y', 'z'}

# 获取调用的函数
functions = parser.get_functions("sin(x) + cos(y)")  # {'sin', 'cos'}

# 获取使用的运算符
operators = parser.get_operators("1 + 2 * 3")  # {'+', '*'}

# 完整分析
analysis = parser.analyze("sin(x) + cos(y)")
print(analysis)
# {
#     'expression': 'sin(x) + cos(y)',
#     'valid': True,
#     'variables': ['x', 'y'],
#     'functions': ['sin', 'cos'],
#     'operators': ['+'],
#     'node_types': [...]
# }
```

## 安全配置

```python
from safe_eval_utils import SafeEvaluator

# 禁用属性访问（默认）
evaluator = SafeEvaluator(allow_attributes=False)
evaluator.eval("'hello'.upper()")  # SecurityError

# 启用属性访问
evaluator = SafeEvaluator(allow_attributes=True)
evaluator.eval("'hello'.upper()")  # 'HELLO'

# 配置限制
evaluator = SafeEvaluator(
    max_string_length=1000,      # 最大字符串长度
    max_list_length=100,         # 最大列表长度
    max_recursion_depth=50,      # 最大递归深度
    allow_subscript=True,        # 允许下标访问
)
```

## 错误类型

- `EvalError` - 求值错误基类
- `SyntaxError` - 语法错误
- `NameError` - 未知变量或函数
- `TypeError_` - 类型错误
- `SecurityError` - 安全错误（不允许的操作）
- `DivisionByZeroError` - 除零错误

## 与 Python eval 的对比

| 特性 | Python eval | safe_eval_utils |
|------|-------------|-----------------|
| 安全性 | ❌ 可执行任意代码 | ✅ AST解析，无代码执行 |
| 错误处理 | ❌ 异常可能崩溃 | ✅ 详细错误信息 |
| 自定义函数 | ❌ 需要传入整个环境 | ✅ 简单配置 |
| 变量控制 | ❌ 需要字典传参 | ✅ 链式设置 |
| 配置灵活 | ❌ 固定 | ✅ 多选项配置 |

## API 参考

### SafeEvaluator

```python
class SafeEvaluator:
    def __init__(variables=None, functions=None, constants=None,
                 allow_attributes=False, allow_subscript=True,
                 max_string_length=1000000, max_list_length=10000,
                 max_recursion_depth=100)
    
    def eval(expression: str, variables=None) -> Any
    def eval_safe(expression: str, variables=None) -> EvalResult
    def set_variable(name: str, value: Any) -> SafeEvaluator
    def set_function(name: str, func: Callable) -> SafeEvaluator
    def set_constant(name: str, value: Any) -> SafeEvaluator
    def validate(expression: str) -> Tuple[bool, Optional[str]]
    def reset() -> SafeEvaluator
```

### 便捷函数

```python
def safe_eval(expression: str, variables=None, functions=None,
              allow_attributes=False) -> Any

def safe_eval_with_result(expression: str, variables=None,
                          functions=None, allow_attributes=False) -> EvalResult

def validate_expression(expression: str) -> Tuple[bool, Optional[str]]

def create_evaluator(variables=None, functions=None, **kwargs) -> SafeEvaluator
```

## 使用场景

1. **配置文件解析** - 安全解析配置中的表达式
2. **规则引擎** - 业务规则的动态求值
3. **计算器应用** - 数学表达式计算
4. **数据验证** - 条件表达式验证
5. **模板引擎** - 字符串模板填充
6. **条件过滤** - 数据过滤和筛选

## 作者

AllToolkit 自动生成

## 日期

2026-04-16