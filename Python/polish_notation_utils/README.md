# Polish Notation Utils


AllToolkit - Polish Notation Utilities Module
==============================================
A comprehensive Polish notation (prefix/reverse Polish notation) utilities module
for Python with zero external dependencies.

Features:
    - Infix to Prefix (Polish) notation conversion
    - Infix to Postfix (Reverse Polish) notation conversion
    - Prefix expression evaluation
    - Postfix expression evaluation
    - All notation types interconversion
    - Support for mathematical operators and functions
    - Custom operator support
    - Expression validation and tokenization

Time Complexity:
    - Conversion: O(n)
    - Evaluation: O(n)

Author: AllToolkit Contributors
License: MIT


## 功能

### 类

- **TokenType**: Token类型枚举
- **Token**: Token类
- **Operator**: 运算符定义
- **Tokenizer**: 词法分析器
  方法: tokenize
- **NotationConverter**: 表达式转换器
  方法: infix_to_postfix, infix_to_prefix, postfix_to_infix
- **ExpressionEvaluator**: 表达式求值器
  方法: evaluate_postfix, evaluate_prefix
- **PolishNotation**: 波兰表达式工具类
  方法: tokenize, infix_to_postfix, infix_to_postfix_tokens, infix_to_prefix, infix_to_prefix_tokens ... (13 个方法)

### 函数

- **infix_to_postfix(expression**) - 中缀表达式转后缀表达式（便捷函数）
- **infix_to_prefix(expression**) - 中缀表达式转前缀表达式（便捷函数）
- **evaluate_postfix(expression, variables**) - 求值后缀表达式（便捷函数）
- **evaluate_prefix(expression, variables**) - 求值前缀表达式（便捷函数）
- **evaluate_infix(expression, variables**) - 求值中缀表达式（便捷函数）
- **tokenize(self, expression**) - 将表达式转换为token列表
- **infix_to_postfix(self, tokens**) - 中缀转后缀（逆波兰表达式）
- **infix_to_prefix(self, tokens**) - 中缀转前缀（波兰表达式）
- **postfix_to_infix(self, tokens**) - 后缀转中缀
- **evaluate_postfix(self, tokens, variables**) - 求值后缀表达式

... 共 24 个函数

## 使用示例

```python
from mod import infix_to_postfix

# 使用 infix_to_postfix
result = infix_to_postfix()
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
