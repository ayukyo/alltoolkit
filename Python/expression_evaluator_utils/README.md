# Expression Evaluator Utils


expression_evaluator_utils - 表达式求值器工具

一个零外部依赖的表达式求值器，支持：
- 数学运算（加减乘除、幂、模）
- 比较运算（==, !=, <, >, <=, >=）
- 逻辑运算（and, or, not）
- 三元条件表达式（条件 ? 真值 : 假值）
- 内置数学函数（sin, cos, tan, sqrt, abs, log, exp, floor, ceil, round）
- 自定义变量和函数
- 嵌套函数调用
- 安全执行（禁止危险操作）

使用示例：
    from expression_evaluator_utils import ExpressionEvaluator
    
    # 基础数学运算
    evaluator = ExpressionEvaluator()
    result = evaluator.evaluate("2 + 3 * 4")  # 14
    
    # 使用变量
    evaluator.set_variable("x", 10)
    result = evaluator.evaluate("x * 2 + 5")  # 25
    
    # 使用函数
    result = evaluator.evaluate("sin(pi / 2)")  # 1.0
    
    # 条件表达式
    result = evaluator.evaluate("x > 5 ? 'large' : 'small'")  # 'large'
    
    # 自定义函数
    evaluator.set_function("double", lambda x: x * 2)
    result = evaluator.evaluate("double(5)")  # 10


## 功能

### 类

- **TokenType**: Token类型枚举
- **Token**: Token类
- **Lexer**: 词法分析器
  方法: advance, peek, skip_whitespace, read_number, read_string ... (9 个方法)
- **Parser**: 语法分析器
  方法: advance, parse, parse_ternary, parse_logical_or, parse_logical_and ... (12 个方法)
- **ASTNode**: AST节点基类
- **NumberNode**: 数字节点
- **StringNode**: 字符串节点
- **VariableNode**: 变量节点
- **BinaryOpNode**: 二元运算节点
- **UnaryOpNode**: 一元运算节点
- **FunctionCallNode**: 函数调用节点
- **TernaryNode**: 三元表达式节点
- **ExpressionEvaluator**: 表达式求值器
  方法: set_variable, get_variable, set_function, get_function, evaluate ... (8 个方法)

### 函数

- **evaluate(expression**) - 便捷函数：创建求值器并计算表达式
- **validate(expression**) - 便捷函数：验证表达式语法
- **get_variables(expression**) - 便捷函数：获取表达式中的变量名
- **advance(self**) - 前进一步
- **peek(self, offset**) - 预览字符
- **skip_whitespace(self**) - 跳过空白字符
- **read_number(self**) - 读取数字
- **read_string(self**) - 读取字符串
- **read_identifier(self**) - 读取标识符
- **read_operator(self**) - 读取运算符

... 共 32 个函数

## 使用示例

```python
from mod import evaluate

# 使用 evaluate
result = evaluate()
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
