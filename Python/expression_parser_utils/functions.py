"""
Math Functions - 内置数学函数定义

提供表达式解析器使用的内置函数
"""

from typing import Any, Callable, Dict

# 三角函数
def sin(x: float) -> float:
    """正弦函数"""
    import math
    return math.sin(x)

def cos(x: float) -> float:
    """余弦函数"""
    import math
    return math.cos(x)

def tan(x: float) -> float:
    """正切函数"""
    import math
    return math.tan(x)

def asin(x: float) -> float:
    """反正弦函数"""
    import math
    return math.asin(x)

def acos(x: float) -> float:
    """反余弦函数"""
    import math
    return math.acos(x)

def atan(x: float) -> float:
    """反正切函数"""
    import math
    return math.atan(x)

def atan2(y: float, x: float) -> float:
    """双参数反正切函数"""
    import math
    return math.atan2(y, x)

# 双曲函数
def sinh(x: float) -> float:
    """双曲正弦函数"""
    import math
    return math.sinh(x)

def cosh(x: float) -> float:
    """双曲余弦函数"""
    import math
    return math.cosh(x)

def tanh(x: float) -> float:
    """双曲正切函数"""
    import math
    return math.tanh(x)

# 指数和对数
def exp(x: float) -> float:
    """e 的 x 次幂"""
    import math
    return math.exp(x)

def log(x: float, base: float = 2.718281828459045) -> float:
    """对数函数"""
    import math
    return math.log(x, base)

def log10(x: float) -> float:
    """常用对数"""
    import math
    return math.log10(x)

def log2(x: float) -> float:
    """二进制对数"""
    import math
    return math.log2(x)

def sqrt(x: float) -> float:
    """平方根"""
    import math
    return math.sqrt(x)

def pow_(x: float, y: float) -> float:
    """幂运算"""
    return x ** y

# 取整函数
def floor(x: float) -> int:
    """向下取整"""
    import math
    return math.floor(x)

def ceil(x: float) -> int:
    """向上取整"""
    import math
    return math.ceil(x)

def round_(x: float, ndigits: int = 0) -> float:
    """四舍五入"""
    return round(x, ndigits)

def trunc(x: float) -> int:
    """截断取整"""
    import math
    return math.trunc(x)

# 数学工具
def abs_(x) -> Any:
    """绝对值"""
    return abs(x)

def min_(*args) -> Any:
    """最小值"""
    return min(args)

def max_(*args) -> Any:
    """最大值"""
    return max(args)

def sum_(*args) -> Any:
    """求和"""
    return sum(args)

def avg(*args) -> float:
    """平均值"""
    if not args:
        raise ValueError("Cannot calculate average of empty set")
    return sum(args) / len(args)

def mod(x: float, y: float) -> float:
    """取模"""
    if y == 0:
        raise ValueError("Modulo by zero")
    return x % y

def factorial(n: int) -> int:
    """阶乘"""
    import math
    return math.factorial(n)

# 检查函数
def isnan(x) -> bool:
    """检查是否为 NaN"""
    import math
    return math.isnan(x) if isinstance(x, float) else False

def isinf(x) -> bool:
    """检查是否为无穷"""
    import math
    return math.isinf(x) if isinstance(x, float) else False

# 角度转换
def degrees(x: float) -> float:
    """弧度转角度"""
    import math
    return math.degrees(x)

def radians(x: float) -> float:
    """角度转弧度"""
    import math
    return math.radians(x)

# 工具函数
def sign(x) -> int:
    """符号函数"""
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0

def clamp(x: float, min_val: float, max_val: float) -> float:
    """限制值在范围内"""
    return max(min_val, min(max_val, x))

def lerp(a: float, b: float, t: float) -> float:
    """线性插值"""
    return a + (b - a) * t

def len_(x) -> int:
    """长度"""
    return len(x)


# 内置函数字典
BUILTIN_FUNCTIONS: Dict[str, Callable] = {
    # 三角函数
    'sin': sin, 'cos': cos, 'tan': tan,
    'asin': asin, 'acos': acos, 'atan': atan, 'atan2': atan2,
    # 双曲函数
    'sinh': sinh, 'cosh': cosh, 'tanh': tanh,
    # 指数和对数
    'exp': exp, 'log': log, 'log10': log10, 'log2': log2,
    'sqrt': sqrt, 'pow': pow_,
    # 取整
    'floor': floor, 'ceil': ceil, 'round': round_, 'trunc': trunc,
    # 数学工具
    'abs': abs_, 'min': min_, 'max': max_, 'sum': sum_,
    'avg': avg, 'mod': mod, 'factorial': factorial,
    # 检查函数
    'isnan': isnan, 'isinf': isinf,
    # 角度转换
    'degrees': degrees, 'radians': radians,
    # 工具函数
    'sign': sign, 'clamp': clamp, 'lerp': lerp, 'len': len_,
}


__all__ = [
    'BUILTIN_FUNCTIONS',
    # 三角函数
    'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2',
    # 双曲函数
    'sinh', 'cosh', 'tanh',
    # 指数对数
    'exp', 'log', 'log10', 'log2', 'sqrt', 'pow_',
    # 取整
    'floor', 'ceil', 'round_', 'trunc',
    # 数学工具
    'abs_', 'min_', 'max_', 'sum_', 'avg', 'mod', 'factorial',
    # 检查函数
    'isnan', 'isinf',
    # 角度转换
    'degrees', 'radians',
    # 工具函数
    'sign', 'clamp', 'lerp', 'len_',
]