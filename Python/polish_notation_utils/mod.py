#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
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
"""

import re
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    """Token类型枚举"""
    NUMBER = auto()
    IDENTIFIER = auto()
    OPERATOR = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    FUNCTION = auto()


@dataclass
class Token:
    """Token类"""
    type: TokenType
    value: Any
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r})"


class Operator:
    """运算符定义"""
    
    def __init__(self, symbol: str, precedence: int, associativity: str, 
                 func: Callable, is_unary: bool = False):
        """
        Args:
            symbol: 运算符符号
            precedence: 优先级（越大越高）
            associativity: 结合性 ('left' 或 'right')
            func: 计算函数
            is_unary: 是否为一元运算符
        """
        self.symbol = symbol
        self.precedence = precedence
        self.associativity = associativity
        self.func = func
        self.is_unary = is_unary
    
    def __repr__(self):
        return f"Operator({self.symbol})"


# 默认运算符
DEFAULT_OPERATORS: Dict[str, Operator] = {
    '+': Operator('+', 2, 'left', lambda a, b: a + b),
    '-': Operator('-', 2, 'left', lambda a, b: a - b),
    '*': Operator('*', 3, 'left', lambda a, b: a * b),
    '/': Operator('/', 3, 'left', lambda a, b: a / b),
    '%': Operator('%', 3, 'left', lambda a, b: a % b),
    '^': Operator('^', 4, 'right', lambda a, b: a ** b),
    # 一元运算符
    'u+': Operator('u+', 5, 'right', lambda a: +a, is_unary=True),
    'u-': Operator('u-', 5, 'right', lambda a: -a, is_unary=True),
}

# 常用数学函数
DEFAULT_FUNCTIONS: Dict[str, Callable] = {
    'sin': lambda x: __import__('math').sin(x),
    'cos': lambda x: __import__('math').cos(x),
    'tan': lambda x: __import__('math').tan(x),
    'sqrt': lambda x: __import__('math').sqrt(x),
    'abs': abs,
    'log': lambda x: __import__('math').log(x),
    'log10': lambda x: __import__('math').log10(x),
    'exp': lambda x: __import__('math').exp(x),
    'floor': lambda x: __import__('math').floor(x),
    'ceil': lambda x: __import__('math').ceil(x),
    'round': round,
    'min': min,
    'max': max,
}

# 数学常量
DEFAULT_CONSTANTS: Dict[str, Union[int, float]] = {
    'pi': 3.141592653589793,
    'e': 2.718281828459045,
}


class Tokenizer:
    """词法分析器"""
    
    def __init__(self, operators: Optional[Dict[str, Operator]] = None):
        self.operators = operators or DEFAULT_OPERATORS
    
    def tokenize(self, expression: str) -> List[Token]:
        """
        将表达式转换为token列表
        
        Args:
            expression: 中缀表达式字符串
            
        Returns:
            Token列表
        """
        tokens = []
        i = 0
        expr = expression.replace(' ', '')
        
        while i < len(expr):
            char = expr[i]
            
            # 数字（包括小数）
            if char.isdigit() or (char == '.' and i + 1 < len(expr) and expr[i + 1].isdigit()):
                j = i
                while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                    j += 1
                # 科学计数法
                if j < len(expr) and expr[j].lower() == 'e':
                    j += 1
                    if j < len(expr) and expr[j] in '+-':
                        j += 1
                    while j < len(expr) and expr[j].isdigit():
                        j += 1
                num_str = expr[i:j]
                tokens.append(Token(TokenType.NUMBER, float(num_str) if '.' in num_str or 'e' in num_str.lower() else int(num_str)))
                i = j
            
            # 标识符（变量或函数）
            elif char.isalpha() or char == '_':
                j = i
                while j < len(expr) and (expr[j].isalnum() or expr[j] == '_'):
                    j += 1
                name = expr[i:j]
                # 检查是否为函数（后面跟括号）
                if j < len(expr) and expr[j] == '(':
                    tokens.append(Token(TokenType.FUNCTION, name))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, name))
                i = j
            
            # 左括号
            elif char == '(':
                tokens.append(Token(TokenType.LPAREN, '('))
                i += 1
            
            # 右括号
            elif char == ')':
                tokens.append(Token(TokenType.RPAREN, ')'))
                i += 1
            
            # 逗号
            elif char == ',':
                tokens.append(Token(TokenType.COMMA, ','))
                i += 1
            
            # 运算符
            elif char in '+-*/%^':
                tokens.append(Token(TokenType.OPERATOR, char))
                i += 1
            
            else:
                raise ValueError(f"未知字符: {char} 在位置 {i}")
        
        return tokens


class NotationConverter:
    """表达式转换器"""
    
    def __init__(self, operators: Optional[Dict[str, Operator]] = None):
        self.operators = operators or DEFAULT_OPERATORS
    
    def _get_precedence(self, op: str) -> int:
        """获取运算符优先级"""
        if op in self.operators:
            return self.operators[op].precedence
        return 0
    
    def _get_associativity(self, op: str) -> str:
        """获取运算符结合性"""
        if op in self.operators:
            return self.operators[op].associativity
        return 'left'
    
    def infix_to_postfix(self, tokens: List[Token]) -> List[Token]:
        """
        中缀转后缀（逆波兰表达式）
        
        使用Shunting-yard算法
        
        Args:
            tokens: 中缀token列表
            
        Returns:
            后缀token列表
        """
        output = []
        operator_stack = []
        
        for i, token in enumerate(tokens):
            if token.type in (TokenType.NUMBER, TokenType.IDENTIFIER):
                output.append(token)
            
            elif token.type == TokenType.FUNCTION:
                operator_stack.append(token)
            
            elif token.type == TokenType.COMMA:
                # 弹出直到遇到左括号
                while operator_stack and operator_stack[-1].type != TokenType.LPAREN:
                    output.append(operator_stack.pop())
            
            elif token.type == TokenType.OPERATOR:
                op = token.value
                
                # 处理一元运算符（正负号）
                prev_token = tokens[i - 1] if i > 0 else None
                is_unary = (i == 0 or 
                           (prev_token and prev_token.type in (TokenType.OPERATOR, TokenType.LPAREN)))
                
                if is_unary and op in '+-':
                    # 用特殊标记区分一元运算符
                    unary_op = 'u' + op
                    operator_stack.append(Token(TokenType.OPERATOR, unary_op))
                else:
                    # 处理二元运算符
                    while (operator_stack and 
                           operator_stack[-1].type == TokenType.OPERATOR and
                           (self._get_precedence(operator_stack[-1].value) > self._get_precedence(op) or
                            (self._get_precedence(operator_stack[-1].value) == self._get_precedence(op) and
                             self._get_associativity(op) == 'left'))):
                        output.append(operator_stack.pop())
                    operator_stack.append(token)
            
            elif token.type == TokenType.LPAREN:
                operator_stack.append(token)
            
            elif token.type == TokenType.RPAREN:
                # 弹出直到遇到左括号
                while operator_stack and operator_stack[-1].type != TokenType.LPAREN:
                    output.append(operator_stack.pop())
                
                if operator_stack:
                    operator_stack.pop()  # 弹出左括号
                
                # 如果栈顶是函数，也弹出
                if operator_stack and operator_stack[-1].type == TokenType.FUNCTION:
                    output.append(operator_stack.pop())
        
        # 弹出剩余运算符
        while operator_stack:
            output.append(operator_stack.pop())
        
        return output
    
    def infix_to_prefix(self, tokens: List[Token]) -> List[Token]:
        """
        中缀转前缀（波兰表达式）
        
        算法：反转表达式，转后缀，再反转
        
        Args:
            tokens: 中缀token列表
            
        Returns:
            前缀token列表
        """
        # 反转token列表并交换括号
        reversed_tokens = []
        for token in reversed(tokens):
            if token.type == TokenType.LPAREN:
                reversed_tokens.append(Token(TokenType.RPAREN, ')'))
            elif token.type == TokenType.RPAREN:
                reversed_tokens.append(Token(TokenType.LPAREN, '('))
            else:
                reversed_tokens.append(token)
        
        # 转后缀
        postfix = self.infix_to_postfix(reversed_tokens)
        
        # 反转结果
        return list(reversed(postfix))
    
    def postfix_to_infix(self, tokens: List[Token]) -> List[Token]:
        """
        后缀转中缀
        
        Args:
            tokens: 后缀token列表
            
        Returns:
            中缀token列表
        """
        stack = []
        
        for token in tokens:
            if token.type in (TokenType.NUMBER, TokenType.IDENTIFIER):
                stack.append([token])
            
            elif token.type == TokenType.FUNCTION:
                # 函数需要特殊处理
                if stack:
                    args = stack.pop()
                    result = [token, Token(TokenType.LPAREN, '(')]
                    result.extend(args)
                    result.append(Token(TokenType.RPAREN, ')'))
                    stack.append(result)
            
            elif token.type == TokenType.OPERATOR:
                op = token.value
                if len(stack) >= 2:
                    right = stack.pop()
                    left = stack.pop()
                    result = [Token(TokenType.LPAREN, '(')]
                    result.extend(left)
                    result.append(token)
                    result.extend(right)
                    result.append(Token(TokenType.RPAREN, ')'))
                    stack.append(result)
                elif len(stack) == 1 and op in ('u+', 'u-'):
                    # 一元运算符
                    operand = stack.pop()
                    result = [token]
                    result.extend(operand)
                    stack.append(result)
        
        if stack:
            # 移除多余的外层括号
            result = stack[0]
            if (len(result) >= 2 and 
                result[0].type == TokenType.LPAREN and 
                result[-1].type == TokenType.RPAREN):
                return result[1:-1]
            return result
        return []


class ExpressionEvaluator:
    """表达式求值器"""
    
    def __init__(self, operators: Optional[Dict[str, Operator]] = None,
                 functions: Optional[Dict[str, Callable]] = None,
                 constants: Optional[Dict[str, Union[int, float]]] = None):
        self.operators = operators or DEFAULT_OPERATORS
        self.functions = functions or DEFAULT_FUNCTIONS.copy()
        self.constants = constants or DEFAULT_CONSTANTS.copy()
        self.converter = NotationConverter(operators)
    
    def evaluate_postfix(self, tokens: List[Token], 
                        variables: Optional[Dict[str, Any]] = None) -> Any:
        """
        求值后缀表达式
        
        Args:
            tokens: 后缀token列表
            variables: 变量字典
            
        Returns:
            计算结果
        """
        variables = variables or {}
        stack = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                stack.append(token.value)
            
            elif token.type == TokenType.IDENTIFIER:
                name = token.value
                if name in variables:
                    stack.append(variables[name])
                elif name in self.constants:
                    stack.append(self.constants[name])
                else:
                    raise ValueError(f"未定义的变量: {name}")
            
            elif token.type == TokenType.FUNCTION:
                func_name = token.value
                if func_name not in self.functions:
                    raise ValueError(f"未定义的函数: {func_name}")
                
                # 从栈中获取参数（简化处理，假设单参数）
                if stack:
                    arg = stack.pop()
                    result = self.functions[func_name](arg)
                    stack.append(result)
            
            elif token.type == TokenType.OPERATOR:
                op = token.value
                
                if op in ('u+', 'u-'):
                    # 一元运算符
                    if stack:
                        a = stack.pop()
                        result = self.operators[op].func(a)
                        stack.append(result)
                else:
                    # 二元运算符
                    if len(stack) >= 2:
                        b = stack.pop()
                        a = stack.pop()
                        result = self.operators[op].func(a, b)
                        stack.append(result)
        
        return stack[0] if stack else None
    
    def evaluate_prefix(self, tokens: List[Token],
                       variables: Optional[Dict[str, Any]] = None) -> Any:
        """
        求值前缀表达式
        
        Args:
            tokens: 前缀token列表
            variables: 变量字典
            
        Returns:
            计算结果
        """
        variables = variables or {}
        stack = []
        
        # 从右到左扫描
        for token in reversed(tokens):
            if token.type == TokenType.NUMBER:
                stack.append(token.value)
            
            elif token.type == TokenType.IDENTIFIER:
                name = token.value
                if name in variables:
                    stack.append(variables[name])
                elif name in self.constants:
                    stack.append(self.constants[name])
                else:
                    raise ValueError(f"未定义的变量: {name}")
            
            elif token.type == TokenType.OPERATOR:
                op = token.value
                
                if op in ('u+', 'u-'):
                    # 一元运算符
                    if stack:
                        a = stack.pop()
                        result = self.operators[op].func(a)
                        stack.append(result)
                else:
                    # 二元运算符（注意顺序）
                    if len(stack) >= 2:
                        a = stack.pop()
                        b = stack.pop()
                        result = self.operators[op].func(a, b)
                        stack.append(result)
            
            elif token.type == TokenType.FUNCTION:
                func_name = token.value
                if func_name not in self.functions:
                    raise ValueError(f"未定义的函数: {func_name}")
                
                if stack:
                    arg = stack.pop()
                    result = self.functions[func_name](arg)
                    stack.append(result)
        
        return stack[0] if stack else None


class PolishNotation:
    """波兰表达式工具类"""
    
    def __init__(self, operators: Optional[Dict[str, Operator]] = None,
                 functions: Optional[Dict[str, Callable]] = None,
                 constants: Optional[Dict[str, Union[int, float]]] = None):
        # 复制默认值以避免修改全局变量
        self.operators = operators if operators is not None else dict(DEFAULT_OPERATORS)
        self.functions = functions if functions is not None else dict(DEFAULT_FUNCTIONS)
        self.constants = constants if constants is not None else dict(DEFAULT_CONSTANTS)
        self.tokenizer = Tokenizer(self.operators)
        self.converter = NotationConverter(self.operators)
        self.evaluator = ExpressionEvaluator(self.operators, self.functions, self.constants)
    
    def tokenize(self, expression: str) -> List[Token]:
        """
        将表达式字符串转换为token列表
        
        Args:
            expression: 表达式字符串
            
        Returns:
            Token列表
            
        Example:
            >>> pn = PolishNotation()
            >>> tokens = pn.tokenize("3 + 4 * 2")
            >>> print([t.value for t in tokens])
            [3, '+', 4, '*', 2]
        """
        return self.tokenizer.tokenize(expression)
    
    def infix_to_postfix(self, expression: str) -> str:
        """
        中缀表达式转后缀表达式（逆波兰表达式）
        
        Args:
            expression: 中缀表达式字符串
            
        Returns:
            后缀表达式字符串
            
        Example:
            >>> pn = PolishNotation()
            >>> result = pn.infix_to_postfix("3 + 4 * 2")
            >>> print(result)
            "3 4 2 * +"
        """
        tokens = self.tokenizer.tokenize(expression)
        postfix_tokens = self.converter.infix_to_postfix(tokens)
        return ' '.join(str(t.value) for t in postfix_tokens)
    
    def infix_to_postfix_tokens(self, expression: str) -> List[Token]:
        """
        中缀表达式转后缀表达式（返回token列表）
        
        Args:
            expression: 中缀表达式字符串
            
        Returns:
            后缀token列表
        """
        tokens = self.tokenizer.tokenize(expression)
        return self.converter.infix_to_postfix(tokens)
    
    def infix_to_prefix(self, expression: str) -> str:
        """
        中缀表达式转前缀表达式（波兰表达式）
        
        Args:
            expression: 中缀表达式字符串
            
        Returns:
            前缀表达式字符串
            
        Example:
            >>> pn = PolishNotation()
            >>> result = pn.infix_to_prefix("3 + 4 * 2")
            >>> print(result)
            "+ 3 * 4 2"
        """
        tokens = self.tokenizer.tokenize(expression)
        prefix_tokens = self.converter.infix_to_prefix(tokens)
        return ' '.join(str(t.value) for t in prefix_tokens)
    
    def infix_to_prefix_tokens(self, expression: str) -> List[Token]:
        """
        中缀表达式转前缀表达式（返回token列表）
        
        Args:
            expression: 中缀表达式字符串
            
        Returns:
            前缀token列表
        """
        tokens = self.tokenizer.tokenize(expression)
        return self.converter.infix_to_prefix(tokens)
    
    def evaluate_postfix(self, expression: str,
                        variables: Optional[Dict[str, Any]] = None) -> Any:
        """
        求值后缀表达式
        
        Args:
            expression: 后缀表达式字符串（空格分隔）
            variables: 变量字典
            
        Returns:
            计算结果
            
        Example:
            >>> pn = PolishNotation()
            >>> result = pn.evaluate_postfix("3 4 + 2 *")
            >>> print(result)
            14
        """
        # 解析后缀表达式字符串
        tokens = []
        for part in expression.split():
            if part in self.operators:
                tokens.append(Token(TokenType.OPERATOR, part))
            elif part.replace('.', '').replace('-', '').isdigit():
                tokens.append(Token(TokenType.NUMBER, 
                                   float(part) if '.' in part else int(part)))
            else:
                tokens.append(Token(TokenType.IDENTIFIER, part))
        
        return self.evaluator.evaluate_postfix(tokens, variables)
    
    def evaluate_prefix(self, expression: str,
                       variables: Optional[Dict[str, Any]] = None) -> Any:
        """
        求值前缀表达式
        
        Args:
            expression: 前缀表达式字符串（空格分隔）
            variables: 变量字典
            
        Returns:
            计算结果
            
        Example:
            >>> pn = PolishNotation()
            >>> result = pn.evaluate_prefix("+ 3 * 4 2")
            >>> print(result)
            11
        """
        # 解析前缀表达式字符串
        tokens = []
        for part in expression.split():
            if part in self.operators:
                tokens.append(Token(TokenType.OPERATOR, part))
            elif part.replace('.', '').replace('-', '').isdigit():
                tokens.append(Token(TokenType.NUMBER,
                                   float(part) if '.' in part else int(part)))
            else:
                tokens.append(Token(TokenType.IDENTIFIER, part))
        
        return self.evaluator.evaluate_prefix(tokens, variables)
    
    def evaluate_infix(self, expression: str,
                      variables: Optional[Dict[str, Any]] = None) -> Any:
        """
        求值中缀表达式（先转后缀再求值）
        
        Args:
            expression: 中缀表达式字符串
            variables: 变量字典
            
        Returns:
            计算结果
            
        Example:
            >>> pn = PolishNotation()
            >>> result = pn.evaluate_infix("3 + 4 * 2")
            >>> print(result)
            11
        """
        tokens = self.tokenizer.tokenize(expression)
        postfix_tokens = self.converter.infix_to_postfix(tokens)
        return self.evaluator.evaluate_postfix(postfix_tokens, variables)
    
    def postfix_to_infix(self, expression: str) -> str:
        """
        后缀表达式转中缀表达式
        
        Args:
            expression: 后缀表达式字符串
            
        Returns:
            中缀表达式字符串
            
        Example:
            >>> pn = PolishNotation()
            >>> result = pn.postfix_to_infix("3 4 2 * +")
            >>> print(result)
            "(3 + (4 * 2))"
        """
        tokens = []
        for part in expression.split():
            if part in self.operators:
                tokens.append(Token(TokenType.OPERATOR, part))
            elif part.replace('.', '').replace('-', '').isdigit():
                tokens.append(Token(TokenType.NUMBER,
                                   float(part) if '.' in part else int(part)))
            else:
                tokens.append(Token(TokenType.IDENTIFIER, part))
        
        infix_tokens = self.converter.postfix_to_infix(tokens)
        return ''.join(str(t.value) for t in infix_tokens)
    
    def add_operator(self, symbol: str, precedence: int, associativity: str,
                    func: Callable, is_unary: bool = False):
        """
        添加自定义运算符
        
        Args:
            symbol: 运算符符号
            precedence: 优先级
            associativity: 结合性 ('left' 或 'right')
            func: 计算函数
            is_unary: 是否为一元运算符
        """
        op = Operator(symbol, precedence, associativity, func, is_unary)
        self.operators[symbol] = op
        self.tokenizer = Tokenizer(self.operators)
        self.converter = NotationConverter(self.operators)
        self.evaluator = ExpressionEvaluator(self.operators, self.functions, self.constants)
    
    def add_function(self, name: str, func: Callable):
        """
        添加自定义函数
        
        Args:
            name: 函数名
            func: 函数实现
        """
        self.functions[name] = func
        self.evaluator = ExpressionEvaluator(self.operators, self.functions, self.constants)
    
    def add_constant(self, name: str, value: Union[int, float]):
        """
        添加自定义常量
        
        Args:
            name: 常量名
            value: 常量值
        """
        self.constants[name] = value
        self.evaluator = ExpressionEvaluator(self.operators, self.functions, self.constants)
    
    def validate_expression(self, expression: str) -> Tuple[bool, Optional[str]]:
        """
        验证表达式语法
        
        Args:
            expression: 表达式字符串
            
        Returns:
            (是否有效, 错误信息)
        """
        try:
            tokens = self.tokenizer.tokenize(expression)
            self.converter.infix_to_postfix(tokens)
            return True, None
        except Exception as e:
            return False, str(e)


# 便捷函数
def infix_to_postfix(expression: str) -> str:
    """
    中缀表达式转后缀表达式（便捷函数）
    
    Args:
        expression: 中缀表达式字符串
        
    Returns:
        后缀表达式字符串
        
    Example:
        >>> infix_to_postfix("3 + 4 * 2")
        "3 4 2 * +"
    """
    pn = PolishNotation()
    return pn.infix_to_postfix(expression)


def infix_to_prefix(expression: str) -> str:
    """
    中缀表达式转前缀表达式（便捷函数）
    
    Args:
        expression: 中缀表达式字符串
        
    Returns:
        前缀表达式字符串
        
    Example:
        >>> infix_to_prefix("3 + 4 * 2")
        "+ 3 * 4 2"
    """
    pn = PolishNotation()
    return pn.infix_to_prefix(expression)


def evaluate_postfix(expression: str, variables: Optional[Dict[str, Any]] = None) -> Any:
    """
    求值后缀表达式（便捷函数）
    
    Args:
        expression: 后缀表达式字符串
        variables: 变量字典
        
    Returns:
        计算结果
        
    Example:
        >>> evaluate_postfix("3 4 + 2 *")
        14
    """
    pn = PolishNotation()
    return pn.evaluate_postfix(expression, variables)


def evaluate_prefix(expression: str, variables: Optional[Dict[str, Any]] = None) -> Any:
    """
    求值前缀表达式（便捷函数）
    
    Args:
        expression: 前缀表达式字符串
        variables: 变量字典
        
    Returns:
        计算结果
        
    Example:
        >>> evaluate_prefix("+ 3 * 4 2")
        11
    """
    pn = PolishNotation()
    return pn.evaluate_prefix(expression, variables)


def evaluate_infix(expression: str, variables: Optional[Dict[str, Any]] = None) -> Any:
    """
    求值中缀表达式（便捷函数）
    
    Args:
        expression: 中缀表达式字符串
        variables: 变量字典
        
    Returns:
        计算结果
        
    Example:
        >>> evaluate_infix("3 + 4 * 2")
        11
    """
    pn = PolishNotation()
    return pn.evaluate_infix(expression, variables)


# 导出公共API
__all__ = [
    'PolishNotation',
    'Tokenizer',
    'NotationConverter',
    'ExpressionEvaluator',
    'Token',
    'TokenType',
    'Operator',
    'DEFAULT_OPERATORS',
    'DEFAULT_FUNCTIONS',
    'DEFAULT_CONSTANTS',
    'infix_to_postfix',
    'infix_to_prefix',
    'evaluate_postfix',
    'evaluate_prefix',
    'evaluate_infix',
]