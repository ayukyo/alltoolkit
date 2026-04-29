"""
Expression Evaluator - 简化的求值接口

提供便捷的高级接口函数
"""

import re
from typing import Dict, Any, Optional, Callable, List, Set
from .parser import ExpressionParser, ExpressionError, ASTNode
from .functions import BUILTIN_FUNCTIONS


class MathFunctions:
    """
    数学函数集合类
    
    提供所有内置数学函数的访问，支持添加自定义函数
    
    使用示例:
    >>> funcs = MathFunctions()
    >>> funcs.add('double', lambda x: x * 2)
    >>> funcs['sin'](0)  # 0.0
    """
    
    def __init__(self, include_builtins: bool = True):
        """
        初始化
        
        Args:
            include_builtins: 是否包含内置数学函数
        """
        self._functions: Dict[str, Callable] = {}
        if include_builtins:
            self._functions.update(BUILTIN_FUNCTIONS)
    
    def add(self, name: str, func: Callable) -> None:
        """添加或覆盖函数"""
        self._functions[name] = func
    
    def remove(self, name: str) -> bool:
        """移除函数"""
        if name in self._functions:
            del self._functions[name]
            return True
        return False
    
    def get(self, name: str, default: Optional[Callable] = None) -> Optional[Callable]:
        """获取函数"""
        return self._functions.get(name, default)
    
    def has(self, name: str) -> bool:
        """检查函数是否存在"""
        return name in self._functions
    
    def names(self) -> List[str]:
        """获取所有函数名"""
        return list(self._functions.keys())
    
    def to_dict(self) -> Dict[str, Callable]:
        """导出为字典"""
        return dict(self._functions)
    
    def __getitem__(self, name: str) -> Callable:
        """通过 [] 访问函数"""
        return self._functions[name]
    
    def __setitem__(self, name: str, func: Callable):
        """通过 [] 设置函数"""
        self._functions[name] = func
    
    def __contains__(self, name: str) -> bool:
        """支持 in 操作符"""
        return name in self._functions
    
    def __len__(self) -> int:
        """函数数量"""
        return len(self._functions)
    
    def __repr__(self) -> str:
        return f"MathFunctions({len(self)} functions)"


def safe_eval(expression: str, variables: Optional[Dict[str, Any]] = None,
              functions: Optional[Dict[str, Callable]] = None) -> Any:
    """
    安全地计算表达式
    
    这是最高级别的便捷接口，自动解析并计算表达式
    
    Args:
        expression: 表达式字符串
        variables: 变量字典，如 {'x': 10, 'y': 20}
        functions: 自定义函数字典，会与内置函数合并
    
    Returns:
        计算结果
    
    Raises:
        ExpressionError: 表达式语法错误或运行时错误
    
    示例:
    >>> safe_eval("2 + 3 * 4")
    14
    >>> safe_eval("x * y + z", variables={'x': 2, 'y': 3, 'z': 1})
    7
    >>> safe_eval("sqrt(16) + abs(-5)")
    9.0
    >>> safe_eval("a > b and c < d", variables={'a': 5, 'b': 3, 'c': 1, 'd': 2})
    True
    """
    # 合并函数
    all_functions = dict(BUILTIN_FUNCTIONS)
    if functions:
        all_functions.update(functions)
    
    parser = ExpressionParser(variables=variables or {}, functions=all_functions)
    ast = parser.parse(expression)
    return parser.evaluate(ast)


def validate_expression(expression: str) -> tuple:
    """
    验证表达式语法
    
    Args:
        expression: 表达式字符串
    
    Returns:
        (is_valid, error_message) 元组
        - is_valid: 是否有效
        - error_message: 错误信息（有效时为 None）
    
    示例:
    >>> validate_expression("2 + 3")
    (True, None)
    >>> validate_expression("2 + ")
    (False, "Position 4: Unexpected token: None")
    """
    try:
        parser = ExpressionParser()
        parser.parse(expression)
        return (True, None)
    except ExpressionError as e:
        return (False, str(e))


def extract_variables(expression: str) -> Set[str]:
    """
    提取表达式中的变量名
    
    Args:
        expression: 表达式字符串
    
    Returns:
        变量名集合
    
    示例:
    >>> extract_variables("x + y * z")
    {'x', 'y', 'z'}
    >>> extract_variables("sin(a) + cos(b)")
    {'a', 'b'}
    """
    parser = ExpressionParser()
    ast = parser.parse(expression)
    return _extract_variables_from_ast(ast)


def _extract_variables_from_ast(node: ASTNode) -> Set[str]:
    """从 AST 中提取变量名"""
    from .parser import VariableNode, BinaryOpNode, UnaryOpNode, FunctionCallNode
    
    variables = set()
    
    if isinstance(node, VariableNode):
        variables.add(node.name)
    elif isinstance(node, BinaryOpNode):
        variables.update(_extract_variables_from_ast(node.left))
        variables.update(_extract_variables_from_ast(node.right))
    elif isinstance(node, UnaryOpNode):
        variables.update(_extract_variables_from_ast(node.operand))
    elif isinstance(node, FunctionCallNode):
        for arg in node.args:
            variables.update(_extract_variables_from_ast(arg))
    
    return variables