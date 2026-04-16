"""
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
"""

import re
import math
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from enum import Enum, auto


class TokenType(Enum):
    """Token类型枚举"""
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    OPERATOR = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    QUESTION = auto()
    COLON = auto()
    EOF = auto()


class Token:
    """Token类"""
    def __init__(self, type_: TokenType, value: Any, position: int = 0):
        self.type = type_
        self.value = value
        self.position = position
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r})"


class Lexer:
    """词法分析器"""
    
    OPERATORS = {
        '+', '-', '*', '/', '%', '^',
        '=', '!', '<', '>',
        '&', '|',
    }
    
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None
    
    def advance(self):
        """前进一步"""
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def peek(self, offset: int = 1) -> Optional[str]:
        """预览字符"""
        peek_pos = self.pos + offset
        return self.text[peek_pos] if peek_pos < len(self.text) else None
    
    def skip_whitespace(self):
        """跳过空白字符"""
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def read_number(self) -> Token:
        """读取数字"""
        result = ''
        start_pos = self.pos
        
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        
        # 处理科学计数法
        if self.current_char and self.current_char.lower() == 'e':
            result += self.current_char
            self.advance()
            if self.current_char and self.current_char in '+-':
                result += self.current_char
                self.advance()
            while self.current_char and self.current_char.isdigit():
                result += self.current_char
                self.advance()
        
        try:
            value = float(result) if '.' in result or 'e' in result.lower() else int(result)
        except ValueError:
            value = float(result)
        
        return Token(TokenType.NUMBER, value, start_pos)
    
    def read_string(self) -> Token:
        """读取字符串"""
        quote_char = self.current_char
        start_pos = self.pos
        self.advance()  # 跳过开始引号
        
        result = ''
        while self.current_char and self.current_char != quote_char:
            if self.current_char == '\\' and self.peek() in (quote_char, '\\', 'n', 't', 'r'):
                self.advance()
                escape_map = {'n': '\n', 't': '\t', 'r': '\r'}
                result += escape_map.get(self.current_char, self.current_char)
            else:
                result += self.current_char
            self.advance()
        
        if self.current_char == quote_char:
            self.advance()  # 跳过结束引号
        
        return Token(TokenType.STRING, result, start_pos)
    
    def read_identifier(self) -> Token:
        """读取标识符"""
        start_pos = self.pos
        result = ''
        
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        return Token(TokenType.IDENTIFIER, result, start_pos)
    
    def read_operator(self) -> Token:
        """读取运算符"""
        start_pos = self.pos
        char = self.current_char
        
        # 处理多字符运算符
        if char == '=' and self.peek() == '=':
            self.advance()
            self.advance()
            return Token(TokenType.OPERATOR, '==', start_pos)
        elif char == '!' and self.peek() == '=':
            self.advance()
            self.advance()
            return Token(TokenType.OPERATOR, '!=', start_pos)
        elif char == '<' and self.peek() == '=':
            self.advance()
            self.advance()
            return Token(TokenType.OPERATOR, '<=', start_pos)
        elif char == '>' and self.peek() == '=':
            self.advance()
            self.advance()
            return Token(TokenType.OPERATOR, '>=', start_pos)
        elif char == '&' and self.peek() == '&':
            self.advance()
            self.advance()
            return Token(TokenType.OPERATOR, '&&', start_pos)
        elif char == '|' and self.peek() == '|':
            self.advance()
            self.advance()
            return Token(TokenType.OPERATOR, '||', start_pos)
        else:
            self.advance()
            return Token(TokenType.OPERATOR, char, start_pos)
    
    def get_next_token(self) -> Token:
        """获取下一个Token"""
        while self.current_char:
            # 跳过空白
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # 数字
            if self.current_char.isdigit() or (self.current_char == '.' and self.peek() and self.peek().isdigit()):
                return self.read_number()
            
            # 字符串
            if self.current_char in '"\'':
                return self.read_string()
            
            # 标识符
            if self.current_char.isalpha() or self.current_char == '_':
                return self.read_identifier()
            
            # 运算符
            if self.current_char in self.OPERATORS:
                return self.read_operator()
            
            # 括号
            if self.current_char == '(':
                token = Token(TokenType.LPAREN, '(', self.pos)
                self.advance()
                return token
            
            if self.current_char == ')':
                token = Token(TokenType.RPAREN, ')', self.pos)
                self.advance()
                return token
            
            # 逗号
            if self.current_char == ',':
                token = Token(TokenType.COMMA, ',', self.pos)
                self.advance()
                return token
            
            # 问号（三元表达式）
            if self.current_char == '?':
                token = Token(TokenType.QUESTION, '?', self.pos)
                self.advance()
                return token
            
            # 冒号（三元表达式）
            if self.current_char == ':':
                token = Token(TokenType.COLON, ':', self.pos)
                self.advance()
                return token
            
            # 未知字符
            raise SyntaxError(f"Unknown character: {self.current_char} at position {self.pos}")
        
        return Token(TokenType.EOF, None, self.pos)
    
    def tokenize(self) -> List[Token]:
        """将文本转换为Token列表"""
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens


class Parser:
    """语法分析器"""
    
    # 运算符优先级（从低到高）
    PRECEDENCE = {
        '||': 1,
        '&&': 2,
        '==': 3, '!=': 3,
        '<': 4, '>': 4, '<=': 4, '>=': 4,
        '+': 5, '-': 5,
        '*': 6, '/': 6, '%': 6,
        '^': 7,
        'unary': 8,  # 一元运算符
        'call': 9,  # 函数调用
    }
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else Token(TokenType.EOF, None)
    
    def advance(self):
        """前进一步"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(TokenType.EOF, None)
    
    def parse(self) -> 'ASTNode':
        """解析表达式"""
        return self.parse_ternary()
    
    def parse_ternary(self) -> 'ASTNode':
        """解析三元表达式"""
        condition = self.parse_logical_or()
        
        if self.current_token.type == TokenType.QUESTION:
            self.advance()  # 跳过 '?'
            true_expr = self.parse_ternary()
            
            if self.current_token.type != TokenType.COLON:
                raise SyntaxError("Expected ':' in ternary expression")
            self.advance()  # 跳过 ':'
            
            false_expr = self.parse_ternary()
            return TernaryNode(condition, true_expr, false_expr)
        
        return condition
    
    def parse_logical_or(self) -> 'ASTNode':
        """解析逻辑或"""
        left = self.parse_logical_and()
        
        while self.current_token.type == TokenType.OPERATOR and self.current_token.value == '||':
            operator = self.current_token.value
            self.advance()
            right = self.parse_logical_and()
            left = BinaryOpNode(operator, left, right)
        
        return left
    
    def parse_logical_and(self) -> 'ASTNode':
        """解析逻辑与"""
        left = self.parse_equality()
        
        while self.current_token.type == TokenType.OPERATOR and self.current_token.value == '&&':
            operator = self.current_token.value
            self.advance()
            right = self.parse_equality()
            left = BinaryOpNode(operator, left, right)
        
        return left
    
    def parse_equality(self) -> 'ASTNode':
        """解析相等性比较"""
        left = self.parse_comparison()
        
        while self.current_token.type == TokenType.OPERATOR and self.current_token.value in ('==', '!='):
            operator = self.current_token.value
            self.advance()
            right = self.parse_comparison()
            left = BinaryOpNode(operator, left, right)
        
        return left
    
    def parse_comparison(self) -> 'ASTNode':
        """解析大小比较"""
        left = self.parse_additive()
        
        while self.current_token.type == TokenType.OPERATOR and self.current_token.value in ('<', '>', '<=', '>='):
            operator = self.current_token.value
            self.advance()
            right = self.parse_additive()
            left = BinaryOpNode(operator, left, right)
        
        return left
    
    def parse_additive(self) -> 'ASTNode':
        """解析加减"""
        left = self.parse_multiplicative()
        
        while self.current_token.type == TokenType.OPERATOR and self.current_token.value in ('+', '-'):
            operator = self.current_token.value
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOpNode(operator, left, right)
        
        return left
    
    def parse_multiplicative(self) -> 'ASTNode':
        """解析乘除模"""
        left = self.parse_power()
        
        while self.current_token.type == TokenType.OPERATOR and self.current_token.value in ('*', '/', '%'):
            operator = self.current_token.value
            self.advance()
            right = self.parse_power()
            left = BinaryOpNode(operator, left, right)
        
        return left
    
    def parse_power(self) -> 'ASTNode':
        """解析幂运算（右结合）"""
        left = self.parse_unary()
        
        if self.current_token.type == TokenType.OPERATOR and self.current_token.value == '^':
            operator = self.current_token.value
            self.advance()
            right = self.parse_power()  # 右结合
            return BinaryOpNode(operator, left, right)
        
        return left
    
    def parse_unary(self) -> 'ASTNode':
        """解析一元运算符"""
        if self.current_token.type == TokenType.OPERATOR and self.current_token.value in ('-', '+', '!'):
            operator = self.current_token.value
            self.advance()
            operand = self.parse_unary()
            return UnaryOpNode(operator, operand)
        
        return self.parse_primary()
    
    def parse_primary(self) -> 'ASTNode':
        """解析基本表达式"""
        token = self.current_token
        
        # 数字
        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value)
        
        # 字符串
        if token.type == TokenType.STRING:
            self.advance()
            return StringNode(token.value)
        
        # 标识符（变量或函数调用）
        if token.type == TokenType.IDENTIFIER:
            name = token.value
            self.advance()
            
            # 函数调用
            if self.current_token.type == TokenType.LPAREN:
                self.advance()  # 跳过 '('
                args = []
                
                if self.current_token.type != TokenType.RPAREN:
                    args.append(self.parse())
                    while self.current_token.type == TokenType.COMMA:
                        self.advance()  # 跳过 ','
                        args.append(self.parse())
                
                if self.current_token.type != TokenType.RPAREN:
                    raise SyntaxError("Expected ')' in function call")
                self.advance()  # 跳过 ')'
                
                return FunctionCallNode(name, args)
            
            # 变量
            return VariableNode(name)
        
        # 括号表达式
        if token.type == TokenType.LPAREN:
            self.advance()  # 跳过 '('
            node = self.parse()
            
            if self.current_token.type != TokenType.RPAREN:
                raise SyntaxError("Expected ')'")
            self.advance()  # 跳过 ')'
            
            return node
        
        raise SyntaxError(f"Unexpected token: {token}")


# AST节点类
class ASTNode:
    """AST节点基类"""
    pass


class NumberNode(ASTNode):
    """数字节点"""
    def __init__(self, value: Union[int, float]):
        self.value = value
    
    def __repr__(self):
        return f"Number({self.value})"


class StringNode(ASTNode):
    """字符串节点"""
    def __init__(self, value: str):
        self.value = value
    
    def __repr__(self):
        return f"String({self.value!r})"


class VariableNode(ASTNode):
    """变量节点"""
    def __init__(self, name: str):
        self.name = name
    
    def __repr__(self):
        return f"Variable({self.name})"


class BinaryOpNode(ASTNode):
    """二元运算节点"""
    def __init__(self, operator: str, left: ASTNode, right: ASTNode):
        self.operator = operator
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"BinaryOp({self.operator}, {self.left}, {self.right})"


class UnaryOpNode(ASTNode):
    """一元运算节点"""
    def __init__(self, operator: str, operand: ASTNode):
        self.operator = operator
        self.operand = operand
    
    def __repr__(self):
        return f"UnaryOp({self.operator}, {self.operand})"


class FunctionCallNode(ASTNode):
    """函数调用节点"""
    def __init__(self, name: str, args: List[ASTNode]):
        self.name = name
        self.args = args
    
    def __repr__(self):
        return f"FunctionCall({self.name}, {self.args})"


class TernaryNode(ASTNode):
    """三元表达式节点"""
    def __init__(self, condition: ASTNode, true_expr: ASTNode, false_expr: ASTNode):
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr
    
    def __repr__(self):
        return f"Ternary({self.condition} ? {self.true_expr} : {self.false_expr})"


class ExpressionEvaluator:
    """表达式求值器"""
    
    # 内置数学常量
    BUILTIN_CONSTANTS = {
        'pi': math.pi,
        'e': math.e,
        'tau': math.tau,
        'inf': math.inf,
        'nan': math.nan,
        'true': True,
        'false': False,
        'null': None,
    }
    
    # 内置数学函数
    BUILTIN_FUNCTIONS = {
        # 三角函数
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'asin': math.asin,
        'acos': math.acos,
        'atan': math.atan,
        'atan2': math.atan2,
        
        # 双曲函数
        'sinh': math.sinh,
        'cosh': math.cosh,
        'tanh': math.tanh,
        
        # 指数对数
        'exp': math.exp,
        'log': math.log,
        'log10': math.log10,
        'log2': math.log2,
        
        # 幂和根
        'sqrt': math.sqrt,
        'pow': pow,
        
        # 取整
        'floor': math.floor,
        'ceil': math.ceil,
        'round': round,
        'trunc': math.trunc,
        
        # 绝对值和符号
        'abs': abs,
        'sign': lambda x: (x > 0) - (x < 0) if x != 0 else 0,
        
        # 最值
        'min': min,
        'max': max,
        
        # 其他
        'degrees': math.degrees,
        'radians': math.radians,
        'factorial': math.factorial,
        
        # 类型转换
        'int': int,
        'float': float,
        'str': str,
        'bool': bool,
        
        # 条件函数
        'if': lambda condition, true_val, false_val: true_val if condition else false_val,
        
        # 数学检验
        'isnan': math.isnan,
        'isinf': math.isinf,
        'isfinite': math.isfinite,
    }
    
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, Callable] = {}
    
    def set_variable(self, name: str, value: Any):
        """设置变量"""
        self.variables[name] = value
    
    def get_variable(self, name: str) -> Any:
        """获取变量"""
        if name in self.variables:
            return self.variables[name]
        if name in self.BUILTIN_CONSTANTS:
            return self.BUILTIN_CONSTANTS[name]
        raise NameError(f"Undefined variable: {name}")
    
    def set_function(self, name: str, func: Callable):
        """设置自定义函数"""
        self.functions[name] = func
    
    def get_function(self, name: str) -> Callable:
        """获取函数"""
        if name in self.functions:
            return self.functions[name]
        if name in self.BUILTIN_FUNCTIONS:
            return self.BUILTIN_FUNCTIONS[name]
        raise NameError(f"Undefined function: {name}")
    
    def evaluate(self, expression: str, **variables) -> Any:
        """求值表达式
        
        Args:
            expression: 要计算的表达式字符串
            **variables: 额外的变量（临时使用）
        
        Returns:
            表达式的计算结果
        
        Raises:
            SyntaxError: 语法错误
            NameError: 未定义的变量或函数
            TypeError: 类型错误
            ZeroDivisionError: 除零错误
            ValueError: 值错误
        """
        # 临时变量
        old_variables = self.variables.copy()
        self.variables.update(variables)
        
        try:
            # 词法分析
            lexer = Lexer(expression)
            tokens = lexer.tokenize()
            
            # 语法分析
            parser = Parser(tokens)
            ast = parser.parse()
            
            # 求值
            return self._evaluate_node(ast)
        finally:
            # 恢复变量
            self.variables = old_variables
    
    def _evaluate_node(self, node: ASTNode) -> Any:
        """递归求值AST节点"""
        if isinstance(node, NumberNode):
            return node.value
        
        if isinstance(node, StringNode):
            return node.value
        
        if isinstance(node, VariableNode):
            return self.get_variable(node.name)
        
        if isinstance(node, BinaryOpNode):
            return self._evaluate_binary_op(node)
        
        if isinstance(node, UnaryOpNode):
            return self._evaluate_unary_op(node)
        
        if isinstance(node, FunctionCallNode):
            return self._evaluate_function_call(node)
        
        if isinstance(node, TernaryNode):
            condition = self._evaluate_node(node.condition)
            return self._evaluate_node(node.true_expr if condition else node.false_expr)
        
        raise TypeError(f"Unknown node type: {type(node)}")
    
    def _evaluate_binary_op(self, node: BinaryOpNode) -> Any:
        """求值二元运算"""
        op = node.operator
        
        # 逻辑运算（短路求值）
        if op == '&&':
            left = self._evaluate_node(node.left)
            if not left:
                return False
            return bool(self._evaluate_node(node.right))
        if op == '||':
            left = self._evaluate_node(node.left)
            if left:
                return True
            return bool(self._evaluate_node(node.right))
        
        # 其他运算需要先求值两边
        left = self._evaluate_node(node.left)
        right = self._evaluate_node(node.right)
        
        # 算术运算
        if op == '+':
            return left + right
        if op == '-':
            return left - right
        if op == '*':
            return left * right
        if op == '/':
            return left / right
        if op == '%':
            return left % right
        if op == '^':
            return left ** right
        
        # 比较运算
        if op == '==':
            return left == right
        if op == '!=':
            return left != right
        if op == '<':
            return left < right
        if op == '>':
            return left > right
        if op == '<=':
            return left <= right
        if op == '>=':
            return left >= right
        
        raise ValueError(f"Unknown operator: {op}")
    
    def _evaluate_unary_op(self, node: UnaryOpNode) -> Any:
        """求值一元运算"""
        operand = self._evaluate_node(node.operand)
        
        if node.operator == '-':
            return -operand
        if node.operator == '+':
            return +operand
        if node.operator == '!':
            return not operand
        
        raise ValueError(f"Unknown unary operator: {node.operator}")
    
    def _evaluate_function_call(self, node: FunctionCallNode) -> Any:
        """求值函数调用"""
        func = self.get_function(node.name)
        args = [self._evaluate_node(arg) for arg in node.args]
        
        try:
            return func(*args)
        except TypeError as e:
            raise TypeError(f"Function '{node.name}' called with wrong arguments: {e}")
    
    def validate(self, expression: str) -> Tuple[bool, Optional[str]]:
        """验证表达式语法
        
        Args:
            expression: 要验证的表达式字符串
        
        Returns:
            (是否有效, 错误信息)
        """
        try:
            lexer = Lexer(expression)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            parser.parse()
            return True, None
        except SyntaxError as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)
    
    def get_variables_used(self, expression: str) -> List[str]:
        """获取表达式中使用的变量名
        
        Args:
            expression: 表达式字符串
        
        Returns:
            变量名列表
        """
        lexer = Lexer(expression)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        variables = []
        self._collect_variables(ast, variables)
        
        # 过滤掉内置常量和函数名
        all_builtins = set(self.BUILTIN_CONSTANTS.keys()) | set(self.BUILTIN_FUNCTIONS.keys())
        return [v for v in variables if v not in all_builtins]
    
    def _collect_variables(self, node: ASTNode, variables: List[str]):
        """递归收集变量名"""
        if isinstance(node, VariableNode):
            variables.append(node.name)
        elif isinstance(node, BinaryOpNode):
            self._collect_variables(node.left, variables)
            self._collect_variables(node.right, variables)
        elif isinstance(node, UnaryOpNode):
            self._collect_variables(node.operand, variables)
        elif isinstance(node, FunctionCallNode):
            for arg in node.args:
                self._collect_variables(arg, variables)
        elif isinstance(node, TernaryNode):
            self._collect_variables(node.condition, variables)
            self._collect_variables(node.true_expr, variables)
            self._collect_variables(node.false_expr, variables)
    
    def get_functions_used(self, expression: str) -> List[str]:
        """获取表达式中使用的函数名
        
        Args:
            expression: 表达式字符串
        
        Returns:
            函数名列表
        """
        lexer = Lexer(expression)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        functions = []
        self._collect_functions(ast, functions)
        
        # 过滤掉内置函数
        return [f for f in functions if f not in self.BUILTIN_FUNCTIONS]
    
    def _collect_functions(self, node: ASTNode, functions: List[str]):
        """递归收集函数名"""
        if isinstance(node, FunctionCallNode):
            functions.append(node.name)
            for arg in node.args:
                self._collect_functions(arg, functions)
        elif isinstance(node, BinaryOpNode):
            self._collect_functions(node.left, functions)
            self._collect_functions(node.right, functions)
        elif isinstance(node, UnaryOpNode):
            self._collect_functions(node.operand, functions)
        elif isinstance(node, TernaryNode):
            self._collect_functions(node.condition, functions)
            self._collect_functions(node.true_expr, functions)
            self._collect_functions(node.false_expr, functions)


# 便捷函数
def evaluate(expression: str, **variables) -> Any:
    """便捷函数：创建求值器并计算表达式
    
    Args:
        expression: 要计算的表达式字符串
        **variables: 变量
    
    Returns:
        表达式的计算结果
    
    Example:
        >>> result = evaluate("x + y * 2", x=10, y=5)
        >>> print(result)  # 20
    """
    evaluator = ExpressionEvaluator()
    return evaluator.evaluate(expression, **variables)


def validate(expression: str) -> Tuple[bool, Optional[str]]:
    """便捷函数：验证表达式语法
    
    Args:
        expression: 要验证的表达式字符串
    
    Returns:
        (是否有效, 错误信息)
    
    Example:
        >>> is_valid, error = validate("2 + 3 * 4")
        >>> print(is_valid)  # True
    """
    evaluator = ExpressionEvaluator()
    return evaluator.validate(expression)


def get_variables(expression: str) -> List[str]:
    """便捷函数：获取表达式中的变量名
    
    Args:
        expression: 表达式字符串
    
    Returns:
        变量名列表
    
    Example:
        >>> vars = get_variables("x + y * z")
        >>> print(vars)  # ['x', 'y', 'z']
    """
    evaluator = ExpressionEvaluator()
    return evaluator.get_variables_used(expression)


# 导出公共API
__all__ = [
    'ExpressionEvaluator',
    'Lexer',
    'Parser',
    'Token',
    'TokenType',
    'ASTNode',
    'NumberNode',
    'StringNode',
    'VariableNode',
    'BinaryOpNode',
    'UnaryOpNode',
    'FunctionCallNode',
    'TernaryNode',
    'evaluate',
    'validate',
    'get_variables',
]