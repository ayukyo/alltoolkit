"""
Safe Expression Evaluator - 安全表达式求值工具集

提供安全的数学和逻辑表达式求值功能，无需使用 Python 内置的 eval()。
支持变量替换、自定义函数、布尔表达式、比较运算符等。

特点：
- 零外部依赖，纯 Python 标准库实现
- AST 解析，不使用 eval/exec
- 可配置的安全选项
- 详细的错误信息
- 支持数学函数、布尔运算、比较运算
- 支持自定义变量和函数

作者：AllToolkit 自动生成
日期：2026-04-16
"""

import ast
import math
import operator
import builtins
from typing import (
    Any, Dict, List, Optional, Callable, Union, Set, Tuple,
    TypeVar
)
# Python 3.6 compatible - Literal and Protocol not available
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import wraps
import re


# ============================================================================
# 类型定义
# ============================================================================

Number = Union[int, float]
Value = Union[int, float, str, bool, None]
T = TypeVar('T')


class TokenType(Enum):
    """表达式元素类型"""
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    NONE = auto()
    VARIABLE = auto()
    OPERATOR = auto()
    FUNCTION = auto()
    PAREN = auto()
    COMMA = auto()
    DOT = auto()
    BRACKET = auto()


class EvalError(Exception):
    """表达式求值错误基类"""
    pass


class EvalSyntaxError(EvalError):
    """语法错误"""
    pass


class EvalNameError(EvalError):
    """名称错误（未知变量或函数）"""
    pass


class EvalTypeError(EvalError):
    """类型错误"""
    pass


class EvalSecurityError(EvalError):
    """安全错误（不允许的操作）"""
    pass


class EvalDivisionByZeroError(EvalError):
    """除零错误"""
    pass


# 为了兼容性，提供别名（避免与内置异常冲突）
SyntaxError = EvalSyntaxError
NameError = EvalNameError
TypeError_ = EvalTypeError
SecurityError = EvalSecurityError
DivisionByZeroError = EvalDivisionByZeroError


# ============================================================================
# 结果类型
# ============================================================================

@dataclass
class EvalResult:
    """求值结果"""
    value: Any
    success: bool
    error: Optional[str] = None
    error_type: Optional[str] = None
    expression: str = ""
    
    def __bool__(self) -> bool:
        return self.success
    
    def __repr__(self) -> str:
        if self.success:
            return f"EvalResult(value={self.value!r}, success=True)"
        return f"EvalResult(error={self.error!r}, success=False)"


@dataclass
class TokenTypeResult:
    """词法分析结果"""
    type: TokenType
    value: Any
    position: int = 0


# ============================================================================
# 默认安全函数
# ============================================================================

def _safe_abs(x: Number) -> Number:
    """绝对值"""
    return abs(x)


def _safe_round(x: Number, ndigits: int = 0) -> Number:
    """四舍五入"""
    return round(x, ndigits)


def _safe_min(*args) -> Number:
    """最小值"""
    if not args:
        raise TypeError_("min() requires at least one argument")
    return min(args)


def _safe_max(*args) -> Number:
    """最大值"""
    if not args:
        raise TypeError_("max() requires at least one argument")
    return max(args)


def _safe_sum(*args) -> Number:
    """求和"""
    return sum(args)


def _safe_len(x) -> int:
    """长度"""
    return len(x)


def _safe_int(x) -> int:
    """转换为整数"""
    return int(x)


def _safe_float(x) -> float:
    """转换为浮点数"""
    return float(x)


def _safe_str(x) -> str:
    """转换为字符串"""
    return str(x)


def _safe_bool(x) -> bool:
    """转换为布尔值"""
    return bool(x)


def _safe_type(x) -> str:
    """获取类型名称"""
    return type(x).__name__


def _safe_isinstance(x, type_name: str) -> bool:
    """检查类型"""
    return type(x).__name__ == type_name


# 数学函数
SAFE_MATH_FUNCTIONS = {
    'abs': _safe_abs,
    'round': _safe_round,
    'min': _safe_min,
    'max': _safe_max,
    'sum': _safe_sum,
    'sqrt': lambda x: math.sqrt(x),
    'pow': lambda x, y: math.pow(x, y),
    'log': lambda x: math.log(x),
    'log10': lambda x: math.log10(x),
    'log2': lambda x: math.log2(x),
    'exp': lambda x: math.exp(x),
    'sin': lambda x: math.sin(x),
    'cos': lambda x: math.cos(x),
    'tan': lambda x: math.tan(x),
    'asin': lambda x: math.asin(x),
    'acos': lambda x: math.acos(x),
    'atan': lambda x: math.atan(x),
    'sinh': lambda x: math.sinh(x),
    'cosh': lambda x: math.cosh(x),
    'tanh': lambda x: math.tanh(x),
    'floor': lambda x: math.floor(x),
    'ceil': lambda x: math.ceil(x),
    'trunc': lambda x: math.trunc(x),
    'degrees': lambda x: math.degrees(x),
    'radians': lambda x: math.radians(x),
    'factorial': lambda x: math.factorial(int(x)),
    'gcd': lambda a, b: math.gcd(int(a), int(b)),
    # lcm not available in Python 3.6, implement manually
    'lcm': lambda a, b: abs(int(a) * int(b)) // math.gcd(int(a), int(b)) if int(a) and int(b) else 0,
}

# 类型转换函数
SAFE_TYPE_FUNCTIONS = {
    'int': _safe_int,
    'float': _safe_float,
    'str': _safe_str,
    'bool': _safe_bool,
    'len': _safe_len,
    'type': _safe_type,
    'isinstance': _safe_isinstance,
}

# 字符串函数
SAFE_STRING_FUNCTIONS = {
    'upper': lambda s: s.upper(),
    'lower': lambda s: s.lower(),
    'strip': lambda s: s.strip(),
    'lstrip': lambda s: s.lstrip(),
    'rstrip': lambda s: s.rstrip(),
    'capitalize': lambda s: s.capitalize(),
    'title': lambda s: s.title(),
    'swapcase': lambda s: s.swapcase(),
    'replace': lambda s, old, new, count=-1: s.replace(old, new, count),
    'split': lambda s, sep=None, maxsplit=-1: s.split(sep, maxsplit),
    'join': lambda sep, iterable: sep.join(iterable),
    'startswith': lambda s, prefix: s.startswith(prefix),
    'endswith': lambda s, suffix: s.endswith(suffix),
    'find': lambda s, sub, start=0, end=-1: s.find(sub, start, end if end != -1 else len(s)),
    'count': lambda s, sub: s.count(sub),
    'isdigit': lambda s: s.isdigit(),
    'isalpha': lambda s: s.isalpha(),
    'isalnum': lambda s: s.isalnum(),
    'isspace': lambda s: s.isspace(),
    'islower': lambda s: s.islower(),
    'isupper': lambda s: s.isupper(),
    'center': lambda s, width, fillchar=' ': s.center(width, fillchar),
    'ljust': lambda s, width, fillchar=' ': s.ljust(width, fillchar),
    'rjust': lambda s, width, fillchar=' ': s.rjust(width, fillchar),
    'zfill': lambda s, width: s.zfill(width),
}

# 所有默认安全函数
DEFAULT_SAFE_FUNCTIONS: Dict[str, Callable] = {}
DEFAULT_SAFE_FUNCTIONS.update(SAFE_MATH_FUNCTIONS)
DEFAULT_SAFE_FUNCTIONS.update(SAFE_TYPE_FUNCTIONS)
DEFAULT_SAFE_FUNCTIONS.update(SAFE_STRING_FUNCTIONS)

# 默认常量
DEFAULT_CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
    'tau': math.tau,
    'inf': math.inf,
    'nan': math.nan,
    'True': True,
    'False': False,
    'None': None,
    'true': True,
    'false': False,
    'null': None,
}


# ============================================================================
# AST 访问器
# ============================================================================

class SafeEvalVisitor(ast.NodeVisitor):
    """
    安全的 AST 访问器，用于计算表达式
    
    遍历 AST 并安全地计算表达式值，不执行任意代码。
    """
    
    def __init__(
        self,
        variables: Optional[Dict[str, Any]] = None,
        functions: Optional[Dict[str, Callable]] = None,
        allow_attributes: bool = False,
        allow_subscript: bool = True,
        max_string_length: int = 1000000,
        max_list_length: int = 10000,
        max_recursion_depth: int = 100,
    ):
        """
        初始化访问器
        
        Args:
            variables: 变量字典
            functions: 函数字典
            allow_attributes: 是否允许属性访问
            allow_subscript: 是否允许下标访问
            max_string_length: 最大字符串长度
            max_list_length: 最大列表长度
            max_recursion_depth: 最大递归深度
        """
        self.variables = variables or {}
        self.functions = functions or {}
        self.allow_attributes = allow_attributes
        self.allow_subscript = allow_subscript
        self.max_string_length = max_string_length
        self.max_list_length = max_list_length
        self.max_recursion_depth = max_recursion_depth
        self._depth = 0
    
    def _check_depth(self):
        """检查递归深度"""
        self._depth += 1
        if self._depth > self.max_recursion_depth:
            raise RecursionError(f"Maximum recursion depth ({self.max_recursion_depth}) exceeded")
        return self._depth
    
    def _release_depth(self):
        """释放递归深度"""
        self._depth -= 1
    
    def visit(self, node: ast.AST) -> Any:
        """访问节点"""
        self._check_depth()
        try:
            result = super().visit(node)
            return result
        finally:
            self._release_depth()
    
    def visit_Expression(self, node: ast.Expression) -> Any:
        """访问表达式节点"""
        return self.visit(node.body)
    
    def visit_Constant(self, node: ast.Constant) -> Any:
        """访问常量节点"""
        value = node.value
        
        # 检查字符串长度
        if isinstance(value, str) and len(value) > self.max_string_length:
            raise SecurityError(f"String length exceeds maximum ({self.max_string_length})")
        
        return value
    
    def visit_Num(self, node: ast.Num) -> Number:
        """访问数字节点（旧版 AST 兼容）"""
        return node.n
    
    def visit_Str(self, node: ast.Str) -> str:
        """访问字符串节点（旧版 AST 兼容）"""
        if len(node.s) > self.max_string_length:
            raise SecurityError(f"String length exceeds maximum ({self.max_string_length})")
        return node.s
    
    def visit_NameConstant(self, node: ast.NameConstant) -> Any:
        """访问命名常量节点（旧版 AST 兼容）"""
        return node.value
    
    def visit_Name(self, node: ast.Name) -> Any:
        """访问名称节点（变量引用）"""
        name = node.id
        
        # 检查常量
        if name in DEFAULT_CONSTANTS:
            return DEFAULT_CONSTANTS[name]
        
        # 检查变量
        if name in self.variables:
            return self.variables[name]
        
        raise NameError(f"Unknown variable: '{name}'")
    
    def visit_BinOp(self, node: ast.BinOp) -> Any:
        """访问二元操作节点"""
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
            ast.LShift: operator.lshift,
            ast.RShift: operator.rshift,
            ast.BitOr: operator.or_,
            ast.BitXor: operator.xor,
            ast.BitAnd: operator.and_,
            ast.MatMult: operator.matmul,
        }
        
        op_type = type(node.op)
        if op_type not in ops:
            raise SyntaxError(f"Unsupported binary operator: {op_type.__name__}")
        
        try:
            # 检查除零
            if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
                raise DivisionByZeroError("Division by zero")
            
            result = ops[op_type](left, right)
            return result
        except ZeroDivisionError:
            raise DivisionByZeroError("Division by zero")
        except TypeError as e:
            raise TypeError_(f"Type error in binary operation: {e}")
    
    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        """访问一元操作节点"""
        operand = self.visit(node.operand)
        
        ops = {
            ast.UAdd: operator.pos,
            ast.USub: operator.neg,
            ast.Not: operator.not_,
            ast.Invert: operator.invert,
        }
        
        op_type = type(node.op)
        if op_type not in ops:
            raise SyntaxError(f"Unsupported unary operator: {op_type.__name__}")
        
        return ops[op_type](operand)
    
    def visit_BoolOp(self, node: ast.BoolOp) -> Any:
        """访问布尔操作节点（带短路求值）"""
        if isinstance(node.op, ast.And):
            result = True
            for v_node in node.values:
                v = self.visit(v_node)
                if not v:
                    return False
                result = v
            return result
        elif isinstance(node.op, ast.Or):
            for v_node in node.values:
                v = self.visit(v_node)
                if v:
                    return v
            return False
        else:
            raise SyntaxError(f"Unsupported boolean operator: {type(node.op).__name__}")
    
    def visit_Compare(self, node: ast.Compare) -> bool:
        """访问比较操作节点"""
        left = self.visit(node.left)
        
        ops = {
            ast.Eq: operator.eq,
            ast.NotEq: operator.ne,
            ast.Lt: operator.lt,
            ast.LtE: operator.le,
            ast.Gt: operator.gt,
            ast.GtE: operator.ge,
            ast.Is: operator.is_,
            ast.IsNot: operator.is_not,
            ast.In: lambda a, b: a in b,
            ast.NotIn: lambda a, b: a not in b,
        }
        
        result = True
        for op, comparator in zip(node.ops, node.comparators):
            right = self.visit(comparator)
            op_type = type(op)
            
            if op_type not in ops:
                raise SyntaxError(f"Unsupported comparison operator: {op_type.__name__}")
            
            try:
                result = result and ops[op_type](left, right)
            except TypeError as e:
                raise TypeError_(f"Type error in comparison: {e}")
            
            left = right
        
        return result
    
    def visit_IfExp(self, node: ast.IfExp) -> Any:
        """访问条件表达式节点（三元运算符）"""
        test = self.visit(node.test)
        if test:
            return self.visit(node.body)
        return self.visit(node.orelse)
    
    def visit_Call(self, node: ast.Call) -> Any:
        """访问函数调用节点"""
        # 获取函数名
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute) and self.allow_attributes:
            obj = self.visit(node.func.value)
            func_name = node.func.attr
            # 属性访问的函数调用
            if hasattr(obj, func_name):
                func = getattr(obj, func_name)
                args = [self.visit(arg) for arg in node.args]
                kwargs = {kw.arg: self.visit(kw.value) for kw in node.keywords}
                return func(*args, **kwargs)
            else:
                raise NameError(f"Unknown attribute: '{func_name}'")
        else:
            raise SecurityError("Only simple function calls are allowed")
        
        # 检查函数是否存在
        if func_name not in self.functions and func_name not in DEFAULT_SAFE_FUNCTIONS:
            raise NameError(f"Unknown function: '{func_name}'")
        
        # 获取函数
        func = self.functions.get(func_name) or DEFAULT_SAFE_FUNCTIONS.get(func_name)
        
        # 计算参数
        args = [self.visit(arg) for arg in node.args]
        kwargs = {kw.arg: self.visit(kw.value) for kw in node.keywords if kw.arg}
        
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise EvalError(f"Error calling function '{func_name}': {e}")
    
    def visit_Subscript(self, node: ast.Subscript) -> Any:
        """访问下标操作节点"""
        if not self.allow_subscript:
            raise SecurityError("Subscript operations are not allowed")
        
        value = self.visit(node.value)
        
        if isinstance(node.slice, ast.Index):
            # 旧版 AST 兼容
            index = self.visit(node.slice.value)
        else:
            index = self.visit(node.slice)
        
        try:
            return value[index]
        except (KeyError, IndexError, TypeError) as e:
            raise EvalError(f"Subscript error: {e}")
    
    def visit_Slice(self, node: ast.Slice) -> slice:
        """访问切片节点"""
        lower = self.visit(node.lower) if node.lower else None
        upper = self.visit(node.upper) if node.upper else None
        step = self.visit(node.step) if node.step else None
        return slice(lower, upper, step)
    
    def visit_List(self, node: ast.List) -> List:
        """访问列表节点"""
        if len(node.elts) > self.max_list_length:
            raise SecurityError(f"List length exceeds maximum ({self.max_list_length})")
        return [self.visit(elt) for elt in node.elts]
    
    def visit_Tuple(self, node: ast.Tuple) -> Tuple:
        """访问元组节点"""
        if len(node.elts) > self.max_list_length:
            raise SecurityError(f"Tuple length exceeds maximum ({self.max_list_length})")
        return tuple(self.visit(elt) for elt in node.elts)
    
    def visit_Dict(self, node: ast.Dict) -> Dict:
        """访问字典节点"""
        if len(node.keys) > self.max_list_length:
            raise SecurityError(f"Dict length exceeds maximum ({self.max_list_length})")
        result = {}
        for key, value in zip(node.keys, node.values):
            if key is not None:
                result[self.visit(key)] = self.visit(value)
        return result
    
    def visit_Set(self, node: ast.Set) -> Set:
        """访问集合节点"""
        if len(node.elts) > self.max_list_length:
            raise SecurityError(f"Set length exceeds maximum ({self.max_list_length})")
        return {self.visit(elt) for elt in node.elts}
    
    def visit_Attribute(self, node: ast.Attribute) -> Any:
        """访问属性节点"""
        if not self.allow_attributes:
            raise SecurityError("Attribute access is not allowed")
        
        value = self.visit(node.value)
        attr = node.attr
        
        if hasattr(value, attr):
            return getattr(value, attr)
        
        raise NameError(f"Unknown attribute: '{attr}'")
    
    def visit_JoinedStr(self, node: ast.JoinedStr) -> str:
        """访问 f-string 节点"""
        parts = []
        for value in node.values:
            if isinstance(value, ast.Constant):
                parts.append(str(value.value))
            elif isinstance(value, ast.FormattedValue):
                formatted = self.visit(value.value)
                if value.conversion == ord('s'):
                    formatted = str(formatted)
                elif value.conversion == ord('r'):
                    formatted = repr(formatted)
                elif value.conversion == ord('a'):
                    formatted = ascii(formatted)
                parts.append(str(formatted))
            else:
                parts.append(str(self.visit(value)))
        return ''.join(parts)
    
    def generic_visit(self, node: ast.AST) -> Any:
        """通用访问器"""
        raise SecurityError(f"Unsupported AST node type: {type(node).__name__}")


# ============================================================================
# 主求值器类
# ============================================================================

class SafeEvaluator:
    """
    安全表达式求值器
    
    提供安全的数学和逻辑表达式求值功能。
    
    Examples:
        >>> evaluator = SafeEvaluator()
        >>> evaluator.eval("2 + 3 * 4")
        14
        >>> evaluator.eval("x + y", variables={"x": 10, "y": 5})
        15
        >>> evaluator.eval("max(1, 2, 3)")
        3
        >>> evaluator.eval("'hello'.upper()")
        SecurityError...
        >>> evaluator.eval("'hello'.upper()", allow_attributes=True)
        'HELLO'
    """
    
    def __init__(
        self,
        variables: Optional[Dict[str, Any]] = None,
        functions: Optional[Dict[str, Callable]] = None,
        constants: Optional[Dict[str, Any]] = None,
        allow_attributes: bool = False,
        allow_subscript: bool = True,
        allow_comprehensions: bool = False,
        max_string_length: int = 1000000,
        max_list_length: int = 10000,
        max_recursion_depth: int = 100,
    ):
        """
        初始化求值器
        
        Args:
            variables: 变量字典
            functions: 自定义函数字典
            constants: 常量字典
            allow_attributes: 是否允许属性访问
            allow_subscript: 是否允许下标访问
            allow_comprehensions: 是否允许列表/字典推导式
            max_string_length: 最大字符串长度
            max_list_length: 最大列表长度
            max_recursion_depth: 最大递归深度
        """
        self.variables = dict(variables) if variables else {}
        self.functions = dict(functions) if functions else {}
        self.constants = {**DEFAULT_CONSTANTS, **(constants or {})}
        self.allow_attributes = allow_attributes
        self.allow_subscript = allow_subscript
        self.allow_comprehensions = allow_comprehensions
        self.max_string_length = max_string_length
        self.max_list_length = max_list_length
        self.max_recursion_depth = max_recursion_depth
    
    def eval(self, expression: str, variables: Optional[Dict[str, Any]] = None) -> Any:
        """
        求值表达式
        
        Args:
            expression: 表达式字符串
            variables: 临时变量字典（与实例变量合并）
            
        Returns:
            表达式结果
            
        Raises:
            SyntaxError: 语法错误
            NameError: 未知变量或函数
            TypeError_: 类型错误
            SecurityError: 安全错误
            DivisionByZeroError: 除零错误
            EvalError: 其他求值错误
        """
        if not expression or not expression.strip():
            raise SyntaxError("Empty expression")
        
        # 去除首尾空白并规范化内部空白（避免 IndentationError）
        # 将连续空白替换为单个空格
        expression = re.sub(r'\s+', ' ', expression.strip())
        
        # 合并变量
        all_variables = {**self.variables, **self.constants}
        if variables:
            all_variables.update(variables)
        
        # 创建访问器
        visitor = SafeEvalVisitor(
            variables=all_variables,
            functions=self.functions,
            allow_attributes=self.allow_attributes,
            allow_subscript=self.allow_subscript,
            max_string_length=self.max_string_length,
            max_list_length=self.max_list_length,
            max_recursion_depth=self.max_recursion_depth,
        )
        
        try:
            # 解析表达式
            tree = ast.parse(expression, mode='eval')
            
            # 访问并计算
            result = visitor.visit(tree.body)
            
            return result
            
        except builtins.SyntaxError as e:
            raise EvalSyntaxError(f"Syntax error: {e}")
        except RecursionError as e:
            raise EvalError(str(e))
    
    def eval_safe(self, expression: str, variables: Optional[Dict[str, Any]] = None) -> EvalResult:
        """
        安全求值表达式（返回结果对象，不抛出异常）
        
        Args:
            expression: 表达式字符串
            variables: 临时变量字典
            
        Returns:
            EvalResult 对象，包含结果或错误信息
        """
        try:
            value = self.eval(expression, variables)
            return EvalResult(value=value, success=True, expression=expression)
        except EvalError as e:
            return EvalResult(
                value=None,
                success=False,
                error=str(e),
                error_type=type(e).__name__,
                expression=expression
            )
        except Exception as e:
            return EvalResult(
                value=None,
                success=False,
                error=f"Unexpected error: {e}",
                error_type="UnexpectedError",
                expression=expression
            )
    
    def set_variable(self, name: str, value: Any) -> 'SafeEvaluator':
        """
        设置变量
        
        Args:
            name: 变量名
            value: 变量值
            
        Returns:
            self，支持链式调用
        """
        self.variables[name] = value
        return self
    
    def set_function(self, name: str, func: Callable) -> 'SafeEvaluator':
        """
        设置函数
        
        Args:
            name: 函数名
            func: 函数对象
            
        Returns:
            self，支持链式调用
        """
        self.functions[name] = func
        return self
    
    def set_constant(self, name: str, value: Any) -> 'SafeEvaluator':
        """
        设置常量
        
        Args:
            name: 常量名
            value: 常量值
            
        Returns:
            self，支持链式调用
        """
        self.constants[name] = value
        return self
    
    def validate(self, expression: str) -> Tuple[bool, Optional[str]]:
        """
        验证表达式语法
        
        Args:
            expression: 表达式字符串
            
        Returns:
            (是否有效, 错误信息)
        """
        if not expression or not expression.strip():
            return False, "Empty expression"
        
        try:
            ast.parse(expression, mode='eval')
            return True, None
        except builtins.SyntaxError as e:
            return False, str(e)
    
    def get_variables(self) -> Dict[str, Any]:
        """获取所有变量"""
        return dict(self.variables)
    
    def get_functions(self) -> Dict[str, Callable]:
        """获取所有自定义函数"""
        return dict(self.functions)
    
    def get_constants(self) -> Dict[str, Any]:
        """获取所有常量"""
        return dict(self.constants)
    
    def clear_variables(self) -> 'SafeEvaluator':
        """清除所有变量"""
        self.variables.clear()
        return self
    
    def clear_functions(self) -> 'SafeEvaluator':
        """清除所有自定义函数"""
        self.functions.clear()
        return self
    
    def reset(self) -> 'SafeEvaluator':
        """重置求值器"""
        self.variables.clear()
        self.functions.clear()
        self.constants = dict(DEFAULT_CONSTANTS)
        return self


# ============================================================================
# 便捷函数
# ============================================================================

# 默认求值器实例
_default_evaluator = SafeEvaluator()


def safe_eval(
    expression: str,
    variables: Optional[Dict[str, Any]] = None,
    functions: Optional[Dict[str, Callable]] = None,
    allow_attributes: bool = False,
) -> Any:
    """
    安全求值表达式的便捷函数
    
    Args:
        expression: 表达式字符串
        variables: 变量字典
        functions: 自定义函数字典
        allow_attributes: 是否允许属性访问
        
    Returns:
        表达式结果
        
    Examples:
        >>> safe_eval("2 + 3")
        5
        >>> safe_eval("x * y", variables={"x": 2, "y": 3})
        6
        >>> safe_eval("square(5)", functions={"square": lambda x: x**2})
        25
    """
    evaluator = SafeEvaluator(
        variables=variables,
        functions=functions,
        allow_attributes=allow_attributes,
    )
    return evaluator.eval(expression)


def safe_eval_with_result(
    expression: str,
    variables: Optional[Dict[str, Any]] = None,
    functions: Optional[Dict[str, Callable]] = None,
    allow_attributes: bool = False,
) -> EvalResult:
    """
    安全求值表达式（返回结果对象）
    
    Args:
        expression: 表达式字符串
        variables: 变量字典
        functions: 自定义函数字典
        allow_attributes: 是否允许属性访问
        
    Returns:
        EvalResult 对象
        
    Examples:
        >>> result = safe_eval_with_result("2 + 3")
        >>> result.success
        True
        >>> result.value
        5
        >>> result = safe_eval_with_result("unknown_var")
        >>> result.success
        False
        >>> result.error
        "Unknown variable: 'unknown_var'"
    """
    evaluator = SafeEvaluator(
        variables=variables,
        functions=functions,
        allow_attributes=allow_attributes,
    )
    return evaluator.eval_safe(expression)


def validate_expression(expression: str) -> Tuple[bool, Optional[str]]:
    """
    验证表达式语法
    
    Args:
        expression: 表达式字符串
        
    Returns:
        (是否有效, 错误信息)
        
    Examples:
        >>> validate_expression("2 + 3")
        (True, None)
        >>> validate_expression("2 + ")
        (False, "...")
    """
    return _default_evaluator.validate(expression)


def create_evaluator(
    variables: Optional[Dict[str, Any]] = None,
    functions: Optional[Dict[str, Callable]] = None,
    **kwargs
) -> SafeEvaluator:
    """
    创建求值器的便捷函数
    
    Args:
        variables: 变量字典
        functions: 自定义函数字典
        **kwargs: 其他参数传递给 SafeEvaluator
        
    Returns:
        SafeEvaluator 实例
        
    Examples:
        >>> ev = create_evaluator(variables={"x": 10})
        >>> ev.eval("x + 5")
        15
    """
    return SafeEvaluator(variables=variables, functions=functions, **kwargs)


# ============================================================================
# 表达式解析器
# ============================================================================

class ExpressionParser:
    """
    表达式解析器
    
    将表达式字符串解析为 AST，并提供详细的分析信息。
    """
    
    def __init__(self):
        """初始化解析器"""
        pass
    
    def parse(self, expression: str) -> ast.Expression:
        """
        解析表达式
        
        Args:
            expression: 表达式字符串
            
        Returns:
            AST 表达式节点
        """
        return ast.parse(expression, mode='eval')
    
    def get_node_types(self, expression: str) -> List[str]:
        """
        获取表达式中所有节点类型
        
        Args:
            expression: 表达式字符串
            
        Returns:
            节点类型名称列表
        """
        tree = self.parse(expression)
        types = []
        
        for node in ast.walk(tree):
            types.append(type(node).__name__)
        
        return types
    
    def get_variables(self, expression: str) -> Set[str]:
        """
        获取表达式中引用的所有变量
        
        Args:
            expression: 表达式字符串
            
        Returns:
            变量名集合
        """
        tree = self.parse(expression)
        variables = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                if node.id not in DEFAULT_CONSTANTS:
                    variables.add(node.id)
        
        return variables
    
    def get_functions(self, expression: str) -> Set[str]:
        """
        获取表达式中调用的所有函数
        
        Args:
            expression: 表达式字符串
            
        Returns:
            函数名集合
        """
        tree = self.parse(expression)
        functions = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    functions.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    functions.add(node.func.attr)
        
        return functions
    
    def get_operators(self, expression: str) -> Set[str]:
        """
        获取表达式中使用的所有运算符
        
        Args:
            expression: 表达式字符串
            
        Returns:
            运算符名称集合
        """
        tree = self.parse(expression)
        operators = set()
        
        op_map = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: '/',
            ast.FloorDiv: '//',
            ast.Mod: '%',
            ast.Pow: '**',
            ast.LShift: '<<',
            ast.RShift: '>>',
            ast.BitOr: '|',
            ast.BitXor: '^',
            ast.BitAnd: '&',
            ast.And: 'and',
            ast.Or: 'or',
            ast.Not: 'not',
            ast.Eq: '==',
            ast.NotEq: '!=',
            ast.Lt: '<',
            ast.LtE: '<=',
            ast.Gt: '>',
            ast.GtE: '>=',
            ast.Is: 'is',
            ast.IsNot: 'is not',
            ast.In: 'in',
            ast.NotIn: 'not in',
        }
        
        for node in ast.walk(tree):
            op_type = type(node)
            if op_type in op_map:
                operators.add(op_map[op_type])
            elif isinstance(node, ast.BinOp):
                operators.add(op_map.get(type(node.op), '?'))
            elif isinstance(node, ast.UnaryOp):
                operators.add(op_map.get(type(node.op), '?'))
            elif isinstance(node, ast.BoolOp):
                operators.add(op_map.get(type(node.op), '?'))
            elif isinstance(node, ast.Compare):
                for op in node.ops:
                    operators.add(op_map.get(type(op), '?'))
        
        return operators
    
    def analyze(self, expression: str) -> Dict[str, Any]:
        """
        分析表达式
        
        Args:
            expression: 表达式字符串
            
        Returns:
            分析结果字典
        """
        try:
            return {
                'expression': expression,
                'valid': True,
                'variables': list(self.get_variables(expression)),
                'functions': list(self.get_functions(expression)),
                'operators': list(self.get_operators(expression)),
                'node_types': self.get_node_types(expression),
            }
        except SyntaxError as e:
            return {
                'expression': expression,
                'valid': False,
                'error': str(e),
            }


# ============================================================================
# 模板表达式求值器
# ============================================================================

class TemplateEvaluator:
    """
    模板表达式求值器
    
    支持在字符串中嵌入表达式，如 "${x + y}"。
    
    Examples:
        >>> te = TemplateEvaluator()
        >>> te.eval("The result is ${x + y}", variables={"x": 1, "y": 2})
        'The result is 3'
        >>> te.eval("${upper(name)}", variables={"name": "hello"}, allow_attributes=True)
        'HELLO'
    """
    
    # 匹配 ${...} 格式的表达式
    pattern = re.compile(r'\$\{([^}]+)\}')
    
    def __init__(
        self,
        variables: Optional[Dict[str, Any]] = None,
        functions: Optional[Dict[str, Callable]] = None,
        allow_attributes: bool = False,
        default_evaluator: Optional[SafeEvaluator] = None,
    ):
        """
        初始化模板求值器
        
        Args:
            variables: 变量字典
            functions: 自定义函数字典
            allow_attributes: 是否允许属性访问
            default_evaluator: 默认求值器（可选）
        """
        self.default_evaluator = default_evaluator or SafeEvaluator(
            variables=variables,
            functions=functions,
            allow_attributes=allow_attributes,
        )
    
    def eval(
        self,
        template: str,
        variables: Optional[Dict[str, Any]] = None,
        functions: Optional[Dict[str, Callable]] = None,
    ) -> str:
        """
        求值模板字符串
        
        Args:
            template: 模板字符串
            variables: 临时变量字典
            functions: 临时函数字典
            
        Returns:
            求值后的字符串
        """
        def replace_expr(match):
            expr = match.group(1).strip()
            try:
                result = self.default_evaluator.eval(expr, variables)
                return str(result)
            except EvalError as e:
                return f"[Error: {e}]"
        
        return self.pattern.sub(replace_expr, template)
    
    def eval_safe(
        self,
        template: str,
        variables: Optional[Dict[str, Any]] = None,
    ) -> EvalResult:
        """
        安全求值模板字符串
        
        Args:
            template: 模板字符串
            variables: 变量字典
            
        Returns:
            EvalResult 对象
        """
        try:
            result = self.eval(template, variables)
            return EvalResult(value=result, success=True, expression=template)
        except Exception as e:
            return EvalResult(
                value=None,
                success=False,
                error=str(e),
                error_type="TemplateError",
                expression=template
            )


# ============================================================================
# 批量求值器
# ============================================================================

class BatchEvaluator:
    """
    批量表达式求值器
    
    支持同时求值多个表达式，并管理变量状态。
    
    Examples:
        >>> be = BatchEvaluator()
        >>> be.set("a", 1)
        >>> be.set("b", 2)
        >>> results = be.eval_all(["a + b", "a * b", "a - b"])
        >>> results
        [3, 2, -1]
    """
    
    def __init__(self, **kwargs):
        """
        初始化批量求值器
        
        Args:
            **kwargs: 传递给 SafeEvaluator 的参数
        """
        self.evaluator = SafeEvaluator(**kwargs)
        self._results: Dict[str, EvalResult] = {}
    
    def set(self, name: str, value: Any) -> 'BatchEvaluator':
        """
        设置变量
        
        Args:
            name: 变量名
            value: 变量值
            
        Returns:
            self
        """
        self.evaluator.set_variable(name, value)
        return self
    
    def get(self, name: str) -> Any:
        """
        获取变量值
        
        Args:
            name: 变量名
            
        Returns:
            变量值
        """
        return self.evaluator.variables.get(name)
    
    def eval(self, expression: str, name: Optional[str] = None) -> Any:
        """
        求值表达式
        
        Args:
            expression: 表达式字符串
            name: 可选的结果名称（用于存储结果）
            
        Returns:
            表达式结果
        """
        result = self.evaluator.eval(expression)
        if name:
            self._results[name] = EvalResult(value=result, success=True, expression=expression)
        return result
    
    def eval_safe(self, expression: str, name: Optional[str] = None) -> EvalResult:
        """
        安全求值表达式
        
        Args:
            expression: 表达式字符串
            name: 可选的结果名称
            
        Returns:
            EvalResult 对象
        """
        result = self.evaluator.eval_safe(expression)
        if name:
            self._results[name] = result
        return result
    
    def eval_all(
        self,
        expressions: List[str],
        store_results: bool = True
    ) -> List[Any]:
        """
        批量求值表达式
        
        Args:
            expressions: 表达式列表
            store_results: 是否存储结果
            
        Returns:
            结果列表
        """
        results = []
        for i, expr in enumerate(expressions):
            result = self.evaluator.eval(expr)
            results.append(result)
            if store_results:
                self._results[f"expr_{i}"] = EvalResult(value=result, success=True, expression=expr)
        return results
    
    def eval_all_safe(
        self,
        expressions: List[str],
        store_results: bool = True
    ) -> List[EvalResult]:
        """
        批量安全求值表达式
        
        Args:
            expressions: 表达式列表
            store_results: 是否存储结果
            
        Returns:
            EvalResult 对象列表
        """
        results = []
        for i, expr in enumerate(expressions):
            result = self.evaluator.eval_safe(expr)
            results.append(result)
            if store_results:
                self._results[f"expr_{i}"] = result
        return results
    
    def get_result(self, name: str) -> Optional[EvalResult]:
        """
        获取存储的结果
        
        Args:
            name: 结果名称
            
        Returns:
            EvalResult 对象或 None
        """
        return self._results.get(name)
    
    def get_all_results(self) -> Dict[str, EvalResult]:
        """获取所有存储的结果"""
        return dict(self._results)
    
    def clear_results(self) -> 'BatchEvaluator':
        """清除所有结果"""
        self._results.clear()
        return self
    
    def clear_variables(self) -> 'BatchEvaluator':
        """清除所有变量"""
        self.evaluator.clear_variables()
        return self
    
    def reset(self) -> 'BatchEvaluator':
        """重置求值器"""
        self.evaluator.reset()
        self._results.clear()
        return self


# ============================================================================
# 条件表达式求值器
# ============================================================================

class ConditionEvaluator:
    """
    条件表达式求值器
    
    专门用于求值布尔条件表达式。
    
    Examples:
        >>> ce = ConditionEvaluator()
        >>> ce.eval("age >= 18 and status == 'active'", variables={"age": 20, "status": "active"})
        True
        >>> ce.eval("score > 90 or bonus == True", variables={"score": 85, "bonus": True})
        True
    """
    
    def __init__(
        self,
        variables: Optional[Dict[str, Any]] = None,
        functions: Optional[Dict[str, Callable]] = None,
    ):
        """
        初始化条件求值器
        
        Args:
            variables: 变量字典
            functions: 自定义函数字典
        """
        self.evaluator = SafeEvaluator(
            variables=variables,
            functions=functions,
            allow_attributes=False,
            allow_subscript=True,
        )
    
    def eval(self, condition: str, variables: Optional[Dict[str, Any]] = None) -> bool:
        """
        求值条件表达式
        
        Args:
            condition: 条件表达式字符串
            variables: 临时变量字典
            
        Returns:
            布尔结果
        """
        result = self.evaluator.eval(condition, variables)
        return bool(result)
    
    def eval_safe(self, condition: str, variables: Optional[Dict[str, Any]] = None) -> EvalResult:
        """
        安全求值条件表达式
        
        Args:
            condition: 条件表达式字符串
            variables: 临时变量字典
            
        Returns:
            EvalResult 对象（value 为布尔值）
        """
        result = self.evaluator.eval_safe(condition, variables)
        if result.success:
            result.value = bool(result.value)
        return result
    
    def check_all(
        self,
        conditions: List[str],
        variables: Optional[Dict[str, Any]] = None,
        mode: str = 'and'  # 'and' or 'or'
    ) -> bool:
        """
        检查多个条件
        
        Args:
            conditions: 条件列表
            variables: 变量字典
            mode: 组合模式 ('and' 或 'or')
            
        Returns:
            组合后的布尔结果
        """
        results = [self.eval(c, variables) for c in conditions]
        if mode == 'and':
            return all(results)
        else:
            return any(results)
    
    def filter_list(
        self,
        items: List[Any],
        condition: str,
        item_var: str = 'item'
    ) -> List[Any]:
        """
        根据条件过滤列表
        
        Args:
            items: 项目列表
            condition: 条件表达式（使用 item_var 引用当前项）
            item_var: 项目变量名
            
        Returns:
            过滤后的列表
        """
        result = []
        for item in items:
            try:
                if self.eval(condition, variables={item_var: item}):
                    result.append(item)
            except EvalError:
                pass
        return result


# ============================================================================
# 数学表达式求值器
# ============================================================================

class MathEvaluator(SafeEvaluator):
    """
    数学表达式专用求值器
    
    预配置了常用的数学函数和常量。
    
    Examples:
        >>> me = MathEvaluator()
        >>> me.eval("sin(pi/2)")
        1.0
        >>> me.eval("sqrt(16) + log(e)")
        5.0
        >>> me.eval("factorial(5)")
        120
    """
    
    def __init__(self, variables: Optional[Dict[str, Any]] = None):
        """
        初始化数学求值器
        
        Args:
            variables: 额外变量字典
        """
        super().__init__(
            variables=variables,
            functions=SAFE_MATH_FUNCTIONS.copy(),
            allow_attributes=False,
            allow_subscript=True,
        )


# ============================================================================
# 字符串表达式求值器
# ============================================================================

class StringEvaluator(SafeEvaluator):
    """
    字符串表达式专用求值器
    
    支持字符串操作函数。
    
    Examples:
        >>> se = StringEvaluator()
        >>> se.eval("upper('hello')", allow_attributes=True)
        'HELLO'
        >>> se.eval("replace('hello world', 'world', 'python')")
        'hello python'
    """
    
    def __init__(self, variables: Optional[Dict[str, Any]] = None):
        """
        初始化字符串求值器
        
        Args:
            variables: 额外变量字典
        """
        functions = {}
        functions.update(SAFE_STRING_FUNCTIONS)
        functions.update(SAFE_TYPE_FUNCTIONS)
        
        super().__init__(
            variables=variables,
            functions=functions,
            allow_attributes=True,
            allow_subscript=True,
        )


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    # 类型
    'EvalResult',
    'TokenTypeResult',
    'TokenType',
    # 异常
    'EvalError',
    'SyntaxError',
    'NameError',
    'TypeError_',
    'SecurityError',
    'DivisionByZeroError',
    # 类
    'SafeEvaluator',
    'SafeEvalVisitor',
    'ExpressionParser',
    'TemplateEvaluator',
    'BatchEvaluator',
    'ConditionEvaluator',
    'MathEvaluator',
    'StringEvaluator',
    # 函数
    'safe_eval',
    'safe_eval_with_result',
    'validate_expression',
    'create_evaluator',
    # 常量
    'DEFAULT_SAFE_FUNCTIONS',
    'DEFAULT_CONSTANTS',
    'SAFE_MATH_FUNCTIONS',
    'SAFE_TYPE_FUNCTIONS',
    'SAFE_STRING_FUNCTIONS',
]