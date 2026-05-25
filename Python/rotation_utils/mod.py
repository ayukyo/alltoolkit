"""
Rotation Utils - 旋转操作工具集

提供各种旋转操作的实现，包括：
- 数组/列表旋转（左旋、右旋）
- 位旋转（循环移位）
- 矩阵旋转（90°、180°、270°）
- 字符串旋转
- 旋转检测（判断是否为旋转关系）

算法特点：
- 多种高效算法实现（Juggling、Block Swap、Reversal）
- 零外部依赖
- 支持原地操作和返回新对象
"""

from typing import TypeVar, List, Sequence, Any, Optional, Tuple
import math

T = TypeVar('T')


def rotate_left_simple(arr: List[T], k: int) -> List[T]:
    """左旋数组（简单实现）"""
    if not arr or k == 0:
        return arr.copy()
    n = len(arr)
    k = k % n
    if k == 0:
        return arr.copy()
    return arr[k:] + arr[:k]


def rotate_right_simple(arr: List[T], k: int) -> List[T]:
    """右旋数组（简单实现）"""
    if not arr or k == 0:
        return arr.copy()
    n = len(arr)
    k = k % n
    if k == 0:
        return arr.copy()
    return arr[-k:] + arr[:-k]


def rotate_left_inplace(arr: List[T], k: int) -> None:
    """原地左旋数组（Reversal 算法）"""
    if not arr or k == 0:
        return
    n = len(arr)
    k = k % n
    if k == 0:
        return
    _reverse(arr, 0, k - 1)
    _reverse(arr, k, n - 1)
    _reverse(arr, 0, n - 1)


def rotate_right_inplace(arr: List[T], k: int) -> None:
    """原地右旋数组"""
    if not arr or k == 0:
        return
    n = len(arr)
    k = k % n
    if k == 0:
        return
    rotate_left_inplace(arr, n - k)


def _reverse(arr: List[T], start: int, end: int) -> None:
    while start < end:
        arr[start], arr[end] = arr[end], arr[start]
        start += 1
        end -= 1


def rotate_left_juggling(arr: List[T], k: int) -> List[T]:
    """左旋数组（Juggling 算法）"""
    if not arr or k == 0:
        return arr.copy()
    n = len(arr)
    k = k % n
    if k == 0:
        return arr.copy()
    result = arr.copy()
    gcd = math.gcd(n, k)
    for i in range(gcd):
        temp = result[i]
        j = i
        while True:
            d = (j + k) % n
            if d == i:
                break
            result[j] = result[d]
            j = d
        result[j] = temp
    return result


def rotate_left_block_swap(arr: List[T], k: int) -> List[T]:
    """左旋数组（Block Swap 算法）"""
    if not arr or k == 0:
        return arr.copy()
    n = len(arr)
    k = k % n
    if k == 0:
        return arr.copy()
    result = arr.copy()
    _block_swap_recursive(result, 0, k, n)
    return result


def _block_swap_recursive(arr: List[T], start: int, d: int, n: int) -> None:
    if d == 0 or d == n:
        return
    i, j = start, start + d
    if d == n - d:
        for x in range(d):
            arr[i + x], arr[j + x] = arr[j + x], arr[i + x]
        return
    if d < n - d:
        for x in range(d):
            arr[i + x], arr[j + x] = arr[j + x], arr[i + x]
        _block_swap_recursive(arr, start + d, d, n - d)
    else:
        ar_start = start + d - (n - d)
        b_start = start + d
        for x in range(n - d):
            arr[ar_start + x], arr[b_start + x] = arr[b_start + x], arr[ar_start + x]
        _block_swap_recursive(arr, start, d - (n - d), d)


def rotate_left_bits(value: int, shift: int, bits: int = 32) -> int:
    """左旋位（循环左移）"""
    if bits <= 0:
        raise ValueError("bits must be positive")
    shift = shift % bits
    if shift == 0:
        return value
    mask = (1 << bits) - 1
    value = value & mask
    return ((value << shift) | (value >> (bits - shift))) & mask


def rotate_right_bits(value: int, shift: int, bits: int = 32) -> int:
    """右旋位（循环右移）"""
    if bits <= 0:
        raise ValueError("bits must be positive")
    shift = shift % bits
    if shift == 0:
        return value
    mask = (1 << bits) - 1
    value = value & mask
    return ((value >> shift) | (value << (bits - shift))) & mask


def rotate_bits(value: int, shift: int, bits: int = 32) -> int:
    """位旋转（正数左旋，负数右旋）"""
    return rotate_left_bits(value, shift, bits) if shift >= 0 else rotate_right_bits(value, -shift, bits)


def rotate_matrix_90_clockwise(matrix: List[List[T]]) -> List[List[T]]:
    """矩阵顺时针旋转 90°"""
    if not matrix or not matrix[0]:
        return []
    n, m = len(matrix), len(matrix[0])
    return [[matrix[n - 1 - i][j] for i in range(n)] for j in range(m)]


def rotate_matrix_90_counterclockwise(matrix: List[List[T]]) -> List[List[T]]:
    """矩阵逆时针旋转 90°"""
    if not matrix or not matrix[0]:
        return []
    n, m = len(matrix), len(matrix[0])
    return [[matrix[i][m - 1 - j] for i in range(n)] for j in range(m)]


def rotate_matrix_180(matrix: List[List[T]]) -> List[List[T]]:
    """矩阵旋转 180°"""
    if not matrix or not matrix[0]:
        return []
    return [row[::-1] for row in matrix[::-1]]


def rotate_matrix(matrix: List[List[T]], degrees: int) -> List[List[T]]:
    """矩阵旋转指定角度"""
    degrees = degrees % 360
    if degrees == 0:
        return [row.copy() for row in matrix]
    elif degrees == 90:
        return rotate_matrix_90_clockwise(matrix)
    elif degrees == 180:
        return rotate_matrix_180(matrix)
    elif degrees == 270:
        return rotate_matrix_90_counterclockwise(matrix)
    raise ValueError(f"Invalid rotation angle: {degrees}")


def rotate_matrix_inplace(matrix: List[List[T]], degrees: int = 90) -> None:
    """原地旋转方阵"""
    if not matrix:
        return
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("In-place rotation only supports square matrices")
    degrees = degrees % 360
    if degrees == 0:
        return
    elif degrees == 90:
        _rotate_square_90_cw(matrix, n)
    elif degrees == 180:
        _rotate_square_180(matrix, n)
    elif degrees == 270:
        _rotate_square_90_ccw(matrix, n)
    else:
        raise ValueError(f"Invalid rotation angle: {degrees}")


def _rotate_square_90_cw(matrix, n):
    for i in range(n // 2):
        for j in range(i, n - i - 1):
            temp = matrix[i][j]
            matrix[i][j] = matrix[n - 1 - j][i]
            matrix[n - 1 - j][i] = matrix[n - 1 - i][n - 1 - j]
            matrix[n - 1 - i][n - 1 - j] = matrix[j][n - 1 - i]
            matrix[j][n - 1 - i] = temp


def _rotate_square_90_ccw(matrix, n):
    for i in range(n // 2):
        for j in range(i, n - i - 1):
            temp = matrix[i][j]
            matrix[i][j] = matrix[j][n - 1 - i]
            matrix[j][n - 1 - i] = matrix[n - 1 - i][n - 1 - j]
            matrix[n - 1 - i][n - 1 - j] = matrix[n - 1 - j][i]
            matrix[n - 1 - j][i] = temp


def _rotate_square_180(matrix, n):
    for i in range(n // 2):
        for j in range(n):
            matrix[i][j], matrix[n - 1 - i][n - 1 - j] = matrix[n - 1 - i][n - 1 - j], matrix[i][j]
    if n % 2 == 1:
        matrix[n // 2] = matrix[n // 2][::-1]


def rotate_string_left(s: str, k: int) -> str:
    """左旋字符串"""
    if not s or k == 0:
        return s
    n = len(s)
    k = k % n
    return s if k == 0 else s[k:] + s[:k]


def rotate_string_right(s: str, k: int) -> str:
    """右旋字符串"""
    if not s or k == 0:
        return s
    n = len(s)
    k = k % n
    return s if k == 0 else s[-k:] + s[:-k]


def is_rotation(s1: str, s2: str) -> bool:
    """判断 s2 是否是 s1 的旋转"""
    return len(s1) == len(s2) and (s1 == s2 or s2 in (s1 + s1))


def find_rotation_distance(s1: str, s2: str) -> Optional[int]:
    """找出 s2 相对于 s1 的左旋距离"""
    return None if not is_rotation(s1, s2) else (0 if s1 == s2 else (s1 + s1).find(s2))


def get_all_rotations(s: str) -> List[str]:
    """获取字符串的所有旋转形式"""
    return [] if not s else [rotate_string_left(s, i) for i in range(len(s))]


def rotate_2d_point(x: float, y: float, angle_degrees: float, center: Tuple[float, float] = (0, 0)) -> Tuple[float, float]:
    """围绕中心点旋转二维点"""
    angle_rad = math.radians(angle_degrees)
    cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
    dx, dy = x - center[0], y - center[1]
    new_x = dx * cos_a - dy * sin_a
    new_y = dx * sin_a + dy * cos_a
    return (new_x + center[0], new_y + center[1])


def rotate_points(points: List[Tuple[float, float]], angle_degrees: float, center: Tuple[float, float] = (0, 0)) -> List[Tuple[float, float]]:
    """批量旋转二维点"""
    return [rotate_2d_point(x, y, angle_degrees, center) for x, y in points]


class Rotator:
    """旋转器类 - 链式调用风格"""
    def __init__(self, data: Sequence[T]):
        self._data = list(data)
    
    def left(self, k: int) -> 'Rotator':
        if self._data and k != 0:
            n = len(self._data)
            k = k % n
            if k != 0:
                self._data = self._data[k:] + self._data[:k]
        return self
    
    def right(self, k: int) -> 'Rotator':
        if self._data and k != 0:
            n = len(self._data)
            k = k % n
            if k != 0:
                self._data = self._data[-k:] + self._data[:-k]
        return self
    
    def rotate_bits(self, shift: int, bits: int = 32) -> 'Rotator':
        self._data = [rotate_bits(x, shift, bits) for x in self._data]
        return self
    
    def result(self) -> List[T]:
        return self._data
    
    def __str__(self) -> str:
        return str(self._data)
    
    def __repr__(self) -> str:
        return f"Rotator({self._data})"


class BitRotator:
    """位旋转器"""
    def __init__(self, value: int, bits: int = 32):
        self._value, self._bits, self._mask = value, bits, (1 << bits) - 1
    
    def left(self, shift: int) -> 'BitRotator':
        shift = shift % self._bits
        if shift != 0:
            self._value = ((self._value << shift) | (self._value >> (self._bits - shift))) & self._mask
        return self
    
    def right(self, shift: int) -> 'BitRotator':
        shift = shift % self._bits
        if shift != 0:
            self._value = ((self._value >> shift) | (self._value << (self._bits - shift))) & self._mask
        return self
    
    def value(self) -> int:
        return self._value
    
    def binary(self) -> str:
        return bin(self._value)[2:].zfill(self._bits)
    
    def __str__(self) -> str:
        return f"BitRotator({self.binary()})"
    
    def __repr__(self) -> str:
        return f"BitRotator(value={self._value}, bits={self._bits})"


def rotate(data: Any, k: int, direction: str = 'left') -> Any:
    """通用旋转函数"""
    if isinstance(data, str):
        return rotate_string_left(data, k) if direction == 'left' else rotate_string_right(data, k)
    elif isinstance(data, (list, tuple)):
        return rotate_left_simple(list(data), k) if direction == 'left' else rotate_right_simple(list(data), k)
    elif isinstance(data, int):
        return rotate_left_bits(data, k) if direction == 'left' else rotate_right_bits(data, k)
    raise TypeError(f"Unsupported type for rotation: {type(data)}")


__all__ = [
    'rotate_left_simple', 'rotate_right_simple', 'rotate_left_inplace', 'rotate_right_inplace',
    'rotate_left_juggling', 'rotate_left_block_swap', 'rotate_left_bits', 'rotate_right_bits', 'rotate_bits',
    'rotate_matrix_90_clockwise', 'rotate_matrix_90_counterclockwise', 'rotate_matrix_180', 'rotate_matrix', 'rotate_matrix_inplace',
    'rotate_string_left', 'rotate_string_right', 'is_rotation', 'find_rotation_distance', 'get_all_rotations',
    'rotate_2d_point', 'rotate_points', 'Rotator', 'BitRotator', 'rotate',
]
