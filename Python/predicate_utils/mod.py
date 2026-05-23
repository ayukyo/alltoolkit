# -*- coding: utf-8 -*-
"""
Predicate Utilities - 谓词构建与组合工具

提供类型安全的谓词构建器，支持 AND、OR、NOT 等逻辑组合，
以及等于、大于、包含、匹配等各种比较操作。
零外部依赖，仅使用 Python 标准库。

Author: AllToolkit
Version: 1.0.0
"""

from typing import (
    TypeVar, Generic, Callable, Any, Optional, 
    List, Dict, Set, Tuple, Union, Iterable, Pattern
)
from functools import wraps
import re
from datetime import datetime, date, time, timedelta
from dataclasses import dataclass
from abc import ABC, abstractmethod
import operator

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


# ============================================================================
# 核心谓词类
# ============================================================================

class Predicate(ABC, Generic[T]):
    """
    谓词抽象基类
    
    所有谓词都实现 __call__ 方法，可以像函数一样调用。
    支持使用 & (AND), | (OR), ~ (NOT) 操作符进行组合。
    """
    
    @abstractmethod
    def __call__(self, value: T) -> bool:
        """评估谓词"""
        pass
    
    def __and__(self, other: 'Predicate[T]') -> 'AndPredicate[T]':
        """使用 & 操作符组合 AND"""
        return AndPredicate([self, other])
    
    def __or__(self, other: 'Predicate[T]') -> 'OrPredicate[T]':
        """使用 | 操作符组合 OR"""
        return OrPredicate([self, other])
    
    def __invert__(self) -> 'NotPredicate[T]':
        """使用 ~ 操作符取反"""
        return NotPredicate(self)
    
    def __xor__(self, other: 'Predicate[T]') -> 'XorPredicate[T]':
        """使用 ^ 操作符组合 XOR"""
        return XorPredicate(self, other)
    
    def and_(self, *others: 'Predicate[T]') -> 'AndPredicate[T]':
        """链式 AND 组合"""
        return AndPredicate([self] + list(others))
    
    def or_(self, *others: 'Predicate[T]') -> 'OrPredicate[T]':
        """链式 OR 组合"""
        return OrPredicate([self] + list(others))
    
    def not_(self) -> 'NotPredicate[T]':
        """返回 NOT 谓词"""
        return NotPredicate(self)
    
    def filter(self, iterable: Iterable[T]) -> List[T]:
        """过滤可迭代对象"""
        return [item for item in iterable if self(item)]
    
    def any(self, iterable: Iterable[T]) -> bool:
        """检查是否有任何元素满足"""
        return any(self(item) for item in iterable)
    
    def all(self, iterable: Iterable[T]) -> bool:
        """检查是否所有元素都满足"""
        return all(self(item) for item in iterable)
    
    def count(self, iterable: Iterable[T]) -> int:
        """统计满足条件的元素数"""
        return sum(1 for item in iterable if self(item))
    
    def first(self, iterable: Iterable[T], default: Optional[T] = None) -> Optional[T]:
        """查找第一个满足条件的元素"""
        for item in iterable:
            if self(item):
                return item
        return default
    
    def reject(self, iterable: Iterable[T]) -> List[T]:
        """返回不满足条件的元素（反向过滤）"""
        return [item for item in iterable if not self(item)]


# ============================================================================
# 复合谓词
# ============================================================================

class AndPredicate(Predicate[T]):
    """AND 谓词 - 所有条件都必须满足"""
    
    def __init__(self, predicates: List[Predicate[T]]):
        self._predicates = predicates
    
    def __call__(self, value: T) -> bool:
        return all(p(value) for p in self._predicates)
    
    def __repr__(self) -> str:
        inner = " AND ".join(repr(p) for p in self._predicates)
        return f"({inner})"


class OrPredicate(Predicate[T]):
    """OR 谓词 - 至少一个条件满足"""
    
    def __init__(self, predicates: List[Predicate[T]]):
        self._predicates = predicates
    
    def __call__(self, value: T) -> bool:
        return any(p(value) for p in self._predicates)
    
    def __repr__(self) -> str:
        inner = " OR ".join(repr(p) for p in self._predicates)
        return f"({inner})"


class NotPredicate(Predicate[T]):
    """NOT 谓词 - 取反"""
    
    def __init__(self, predicate: Predicate[T]):
        self._predicate = predicate
    
    def __call__(self, value: T) -> bool:
        return not self._predicate(value)
    
    def __repr__(self) -> str:
        return f"NOT {self._predicate!r}"


class XorPredicate(Predicate[T]):
    """XOR 谓词 - 异或（恰好一个满足）"""
    
    def __init__(self, left: Predicate[T], right: Predicate[T]):
        self._left = left
        self._right = right
    
    def __call__(self, value: T) -> bool:
        return self._left(value) != self._right(value)
    
    def __repr__(self) -> str:
        return f"({self._left!r} XOR {self._right!r})"


class NandPredicate(Predicate[T]):
    """NAND 谓词 - NOT AND"""
    
    def __init__(self, predicates: List[Predicate[T]]):
        self._and = AndPredicate(predicates)
    
    def __call__(self, value: T) -> bool:
        return not self._and(value)
    
    def __repr__(self) -> str:
        return f"NOT ({self._and!r})"


class NorPredicate(Predicate[T]):
    """NOR 谓词 - NOT OR"""
    
    def __init__(self, predicates: List[Predicate[T]]):
        self._or = OrPredicate(predicates)
    
    def __call__(self, value: T) -> bool:
        return not self._or(value)
    
    def __repr__(self) -> str:
        return f"NOT ({self._or!r})"


class ImplicationPredicate(Predicate[T]):
    """蕴涵谓词 - A => B 等价于 NOT A OR B"""
    
    def __init__(self, antecedent: Predicate[T], consequent: Predicate[T]):
        self._antecedent = antecedent
        self._consequent = consequent
    
    def __call__(self, value: T) -> bool:
        return not self._antecedent(value) or self._consequent(value)
    
    def __repr__(self) -> str:
        return f"({self._antecedent!r} => {self._consequent!r})"


class ExactlyPredicate(Predicate[T]):
    """恰好 N 个条件满足"""
    
    def __init__(self, predicates: List[Predicate[T]], count: int):
        self._predicates = predicates
        self._count = count
    
    def __call__(self, value: T) -> bool:
        matches = sum(1 for p in self._predicates if p(value))
        return matches == self._count
    
    def __repr__(self) -> str:
        return f"(exactly {self._count} of {len(self._predicates)})"


class AtLeastPredicate(Predicate[T]):
    """至少 N 个条件满足"""
    
    def __init__(self, predicates: List[Predicate[T]], count: int):
        self._predicates = predicates
        self._count = count
    
    def __call__(self, value: T) -> bool:
        matches = 0
        for p in self._predicates:
            if p(value):
                matches += 1
                if matches >= self._count:
                    return True
        return False
    
    def __repr__(self) -> str:
        return f"(at least {self._count} of {len(self._predicates)})"


class AtMostPredicate(Predicate[T]):
    """最多 N 个条件满足"""
    
    def __init__(self, predicates: List[Predicate[T]], count: int):
        self._predicates = predicates
        self._count = count
    
    def __call__(self, value: T) -> bool:
        matches = 0
        for p in self._predicates:
            if p(value):
                matches += 1
                if matches > self._count:
                    return False
        return True
    
    def __repr__(self) -> str:
        return f"(at most {self._count} of {len(self._predicates)})"


# ============================================================================
# 比较谓词
# ============================================================================

class EqualsPredicate(Predicate[T]):
    """等于谓词"""
    
    def __init__(self, expected: T):
        self._expected = expected
    
    def __call__(self, value: T) -> bool:
        return value == self._expected
    
    def __repr__(self) -> str:
        return f"=={self._expected!r}"


class NotEqualsPredicate(Predicate[T]):
    """不等于谓词"""
    
    def __init__(self, expected: T):
        self._expected = expected
    
    def __call__(self, value: T) -> bool:
        return value != self._expected
    
    def __repr__(self) -> str:
        return f"!={self._expected!r}"


class LessThanPredicate(Predicate[T]):
    """小于谓词"""
    
    def __init__(self, threshold: T):
        self._threshold = threshold
    
    def __call__(self, value: T) -> bool:
        return value < self._threshold
    
    def __repr__(self) -> str:
        return f"<{self._threshold!r}"


class LessThanOrEqualPredicate(Predicate[T]):
    """小于等于谓词"""
    
    def __init__(self, threshold: T):
        self._threshold = threshold
    
    def __call__(self, value: T) -> bool:
        return value <= self._threshold
    
    def __repr__(self) -> str:
        return f"<={self._threshold!r}"


class GreaterThanPredicate(Predicate[T]):
    """大于谓词"""
    
    def __init__(self, threshold: T):
        self._threshold = threshold
    
    def __call__(self, value: T) -> bool:
        return value > self._threshold
    
    def __repr__(self) -> str:
        return f">{self._threshold!r}"


class GreaterThanOrEqualPredicate(Predicate[T]):
    """大于等于谓词"""
    
    def __init__(self, threshold: T):
        self._threshold = threshold
    
    def __call__(self, value: T) -> bool:
        return value >= self._threshold
    
    def __repr__(self) -> str:
        return f">={self._threshold!r}"


class BetweenPredicate(Predicate[T]):
    """区间谓词 - 在两个值之间（闭区间）"""
    
    def __init__(self, low: T, high: T, inclusive: bool = True):
        self._low = low
        self._high = high
        self._inclusive = inclusive
    
    def __call__(self, value: T) -> bool:
        if self._inclusive:
            return self._low <= value <= self._high
        return self._low < value < self._high
    
    def __repr__(self) -> str:
        brackets = "[]" if self._inclusive else "()"
        return f"{brackets[0]}{self._low!r}, {self._high!r}{brackets[1]}"


class InPredicate(Predicate[T]):
    """包含于谓词 - 值在集合中"""
    
    def __init__(self, collection: Iterable[T]):
        self._collection = set(collection) if not isinstance(collection, (set, frozenset)) else collection
    
    def __call__(self, value: T) -> bool:
        return value in self._collection
    
    def __repr__(self) -> str:
        items = list(self._collection)[:5]
        suffix = "..." if len(self._collection) > 5 else ""
        return f"in {{{items!r}{suffix}}}"


class NotInPredicate(Predicate[T]):
    """不包含于谓词 - 值不在集合中"""
    
    def __init__(self, collection: Iterable[T]):
        self._collection = set(collection) if not isinstance(collection, (set, frozenset)) else collection
    
    def __call__(self, value: T) -> bool:
        return value not in self._collection
    
    def __repr__(self) -> str:
        items = list(self._collection)[:5]
        suffix = "..." if len(self._collection) > 5 else ""
        return f"not in {{{items!r}{suffix}}}"


# ============================================================================
# 类型谓词
# ============================================================================

class IsNonePredicate(Predicate[T]):
    """是 None 谓词"""
    
    def __call__(self, value: T) -> bool:
        return value is None
    
    def __repr__(self) -> str:
        return "is None"


class IsNotNonePredicate(Predicate[T]):
    """不是 None 谓词"""
    
    def __call__(self, value: T) -> bool:
        return value is not None
    
    def __repr__(self) -> str:
        return "is not None"


class IsInstancePredicate(Predicate[Any]):
    """是某类型实例谓词"""
    
    def __init__(self, types: Union[type, Tuple[type, ...]]):
        self._types = types if isinstance(types, tuple) else (types,)
    
    def __call__(self, value: Any) -> bool:
        return isinstance(value, self._types)
    
    def __repr__(self) -> str:
        type_names = [t.__name__ for t in self._types]
        return f"isinstance({', '.join(type_names)})"


class IsSubclassPredicate(Predicate[type]):
    """是某类型子类谓词"""
    
    def __init__(self, types: Union[type, Tuple[type, ...]]):
        self._types = types if isinstance(types, tuple) else (types,)
    
    def __call__(self, value: type) -> bool:
        return issubclass(value, self._types)
    
    def __repr__(self) -> str:
        type_names = [t.__name__ for t in self._types]
        return f"issubclass({', '.join(type_names)})"


# ============================================================================
# 字符串谓词
# ============================================================================

class StringPredicate(Predicate[str]):
    """字符串谓词基类"""
    pass


class StartsWithPredicate(StringPredicate):
    """以...开头谓词"""
    
    def __init__(self, prefix: str, case_sensitive: bool = True):
        self._prefix = prefix
        self._case_sensitive = case_sensitive
    
    def __call__(self, value: str) -> bool:
        if self._case_sensitive:
            return value.startswith(self._prefix)
        return value.lower().startswith(self._prefix.lower())
    
    def __repr__(self) -> str:
        case = "" if self._case_sensitive else "(ignore case)"
        return f"starts_with({self._prefix!r}{case})"


class EndsWithPredicate(StringPredicate):
    """以...结尾谓词"""
    
    def __init__(self, suffix: str, case_sensitive: bool = True):
        self._suffix = suffix
        self._case_sensitive = case_sensitive
    
    def __call__(self, value: str) -> bool:
        if self._case_sensitive:
            return value.endswith(self._suffix)
        return value.lower().endswith(self._suffix.lower())
    
    def __repr__(self) -> str:
        case = "" if self._case_sensitive else "(ignore case)"
        return f"ends_with({self._suffix!r}{case})"


class ContainsPredicate(StringPredicate):
    """包含子串谓词"""
    
    def __init__(self, substring: str, case_sensitive: bool = True):
        self._substring = substring
        self._case_sensitive = case_sensitive
    
    def __call__(self, value: str) -> bool:
        if self._case_sensitive:
            return self._substring in value
        return self._substring.lower() in value.lower()
    
    def __repr__(self) -> str:
        case = "" if self._case_sensitive else "(ignore case)"
        return f"contains({self._substring!r}{case})"


class MatchesPredicate(StringPredicate):
    """正则匹配谓词"""
    
    def __init__(self, pattern: Union[str, Pattern], flags: int = 0):
        if isinstance(pattern, str):
            self._pattern = re.compile(pattern, flags)
        else:
            self._pattern = pattern
        self._flags = flags
    
    def __call__(self, value: str) -> bool:
        return bool(self._pattern.search(value))
    
    def __repr__(self) -> str:
        return f"matches(/{self._pattern.pattern}/)"


class LengthPredicate(Predicate[Any]):
    """长度谓词"""
    
    def __init__(self, min_len: Optional[int] = None, max_len: Optional[int] = None):
        self._min_len = min_len
        self._max_len = max_len
    
    def __call__(self, value: Any) -> bool:
        try:
            length = len(value)
            if self._min_len is not None and length < self._min_len:
                return False
            if self._max_len is not None and length > self._max_len:
                return False
            return True
        except TypeError:
            return False
    
    def __repr__(self) -> str:
        if self._min_len is not None and self._max_len is not None:
            return f"length[{self._min_len}, {self._max_len}]"
        elif self._min_len is not None:
            return f"length>={self._min_len}"
        elif self._max_len is not None:
            return f"length<={self._max_len}"
        return "length(*)"


class IsEmptyPredicate(Predicate[Any]):
    """为空谓词"""
    
    def __call__(self, value: Any) -> bool:
        if value is None:
            return True
        try:
            return len(value) == 0
        except TypeError:
            return False
    
    def __repr__(self) -> str:
        return "is_empty"


class IsNotEmptyPredicate(Predicate[Any]):
    """不为空谓词"""
    
    def __call__(self, value: Any) -> bool:
        if value is None:
            return False
        try:
            return len(value) > 0
        except TypeError:
            return True
    
    def __repr__(self) -> str:
        return "is_not_empty"


class IsAlnumPredicate(StringPredicate):
    """只包含字母数字谓词"""
    
    def __call__(self, value: str) -> bool:
        return value.isalnum()
    
    def __repr__(self) -> str:
        return "is_alnum"


class IsAlphaPredicate(StringPredicate):
    """只包含字母谓词"""
    
    def __call__(self, value: str) -> bool:
        return value.isalpha()
    
    def __repr__(self) -> str:
        return "is_alpha"


class IsDigitPredicate(StringPredicate):
    """只包含数字谓词"""
    
    def __call__(self, value: str) -> bool:
        return value.isdigit()
    
    def __repr__(self) -> str:
        return "is_digit"


class IsNumericPredicate(StringPredicate):
    """是数字谓词（包括 Unicode 数字）"""
    
    def __call__(self, value: str) -> bool:
        return value.isnumeric()
    
    def __repr__(self) -> str:
        return "is_numeric"


class IsLowerPredicate(StringPredicate):
    """是小写谓词"""
    
    def __call__(self, value: str) -> bool:
        return value.islower()
    
    def __repr__(self) -> str:
        return "is_lower"


class IsUpperPredicate(StringPredicate):
    """是大写谓词"""
    
    def __call__(self, value: str) -> bool:
        return value.isupper()
    
    def __repr__(self) -> str:
        return "is_upper"


class IsSpacePredicate(StringPredicate):
    """只包含空白字符谓词"""
    
    def __call__(self, value: str) -> bool:
        return value.isspace()
    
    def __repr__(self) -> str:
        return "is_space"


class IsTitlePredicate(StringPredicate):
    """是标题格式谓词"""
    
    def __call__(self, value: str) -> bool:
        return value.istitle()
    
    def __repr__(self) -> str:
        return "is_title"


# ============================================================================
# 数值谓词
# ============================================================================

class NumberPredicate(Predicate[Union[int, float]]):
    """数值谓词基类"""
    pass


class IsPositivePredicate(NumberPredicate):
    """是正数谓词"""
    
    def __call__(self, value: Union[int, float]) -> bool:
        return value > 0
    
    def __repr__(self) -> str:
        return "is_positive"


class IsNegativePredicate(NumberPredicate):
    """是负数谓词"""
    
    def __call__(self, value: Union[int, float]) -> bool:
        return value < 0
    
    def __repr__(self) -> str:
        return "is_negative"


class IsZeroPredicate(NumberPredicate):
    """是零谓词"""
    
    def __call__(self, value: Union[int, float]) -> bool:
        return value == 0
    
    def __repr__(self) -> str:
        return "is_zero"


class IsEvenPredicate(Predicate[int]):
    """是偶数谓词"""
    
    def __call__(self, value: int) -> bool:
        return value % 2 == 0
    
    def __repr__(self) -> str:
        return "is_even"


class IsOddPredicate(Predicate[int]):
    """是奇数谓词"""
    
    def __call__(self, value: int) -> bool:
        return value % 2 != 0
    
    def __repr__(self) -> str:
        return "is_odd"


class IsIntegerPredicate(Predicate[Union[int, float]]):
    """是整数谓词（包括浮点数表示的整数）"""
    
    def __call__(self, value: Union[int, float]) -> bool:
        if isinstance(value, int):
            return True
        return float(value).is_integer()
    
    def __repr__(self) -> str:
        return "is_integer"


class IsFloatPredicate(Predicate[Union[int, float]]):
    """是浮点数谓词"""
    
    def __call__(self, value: Union[int, float]) -> bool:
        return isinstance(value, float)
    
    def __repr__(self) -> str:
        return "is_float"


class IsFinitePredicate(Predicate[float]):
    """是有限数谓词"""
    
    def __call__(self, value: float) -> bool:
        import math
        return math.isfinite(value)
    
    def __repr__(self) -> str:
        return "is_finite"


class IsInfinitePredicate(Predicate[float]):
    """是无穷大谓词"""
    
    def __call__(self, value: float) -> bool:
        import math
        return math.isinf(value)
    
    def __repr__(self) -> str:
        return "is_infinite"


class IsNaNPredicate(Predicate[float]):
    """是 NaN 谓词"""
    
    def __call__(self, value: float) -> bool:
        import math
        return math.isnan(value)
    
    def __repr__(self) -> str:
        return "is_nan"


class DivisibleByPredicate(Predicate[int]):
    """能被...整除谓词"""
    
    def __init__(self, divisor: int):
        if divisor == 0:
            raise ValueError("Divisor cannot be zero")
        self._divisor = divisor
    
    def __call__(self, value: int) -> bool:
        return value % self._divisor == 0
    
    def __repr__(self) -> str:
        return f"divisible_by({self._divisor})"


class MultipleOfPredicate(Predicate[int]):
    """是...的倍数谓词"""
    
    def __init__(self, base: int):
        if base == 0:
            raise ValueError("Base cannot be zero")
        self._base = base
    
    def __call__(self, value: int) -> bool:
        return value % self._base == 0
    
    def __repr__(self) -> str:
        return f"multiple_of({self._base})"


# ============================================================================
# 集合谓词
# ============================================================================

class ContainsAllPredicate(Predicate[Iterable[T]]):
    """包含所有元素谓词"""
    
    def __init__(self, items: Iterable[T]):
        self._items = set(items)
    
    def __call__(self, value: Iterable[T]) -> bool:
        return self._items.issubset(set(value))
    
    def __repr__(self) -> str:
        return f"contains_all({self._items!r})"


class ContainsAnyPredicate(Predicate[Iterable[T]]):
    """包含任一元素谓词"""
    
    def __init__(self, items: Iterable[T]):
        self._items = set(items)
    
    def __call__(self, value: Iterable[T]) -> bool:
        return bool(self._items.intersection(set(value)))
    
    def __repr__(self) -> str:
        return f"contains_any({self._items!r})"


class ContainsNonePredicate(Predicate[Iterable[T]]):
    """不包含任何元素谓词"""
    
    def __init__(self, items: Iterable[T]):
        self._items = set(items)
    
    def __call__(self, value: Iterable[T]) -> bool:
        return not self._items.intersection(set(value))
    
    def __repr__(self) -> str:
        return f"contains_none({self._items!r})"


class HasSizePredicate(Predicate[Any]):
    """大小谓词"""
    
    def __init__(self, size: int):
        self._size = size
    
    def __call__(self, value: Any) -> bool:
        try:
            return len(value) == self._size
        except TypeError:
            return False
    
    def __repr__(self) -> str:
        return f"has_size({self._size})"


# ============================================================================
# 字典谓词
# ============================================================================

class HasKeyPredicate(Predicate[Dict]):
    """包含键谓词"""
    
    def __init__(self, key: Any):
        self._key = key
    
    def __call__(self, value: Dict) -> bool:
        return self._key in value
    
    def __repr__(self) -> str:
        return f"has_key({self._key!r})"


class HasValuePredicate(Predicate[Dict]):
    """包含值谓词"""
    
    def __init__(self, value: Any):
        self._value = value
    
    def __call__(self, d: Dict) -> bool:
        return self._value in d.values()
    
    def __repr__(self) -> str:
        return f"has_value({self._value!r})"


class KeyValuePredicate(Predicate[Dict]):
    """键值匹配谓词"""
    
    def __init__(self, key: Any, value_predicate: Predicate):
        self._key = key
        self._value_predicate = value_predicate
    
    def __call__(self, d: Dict) -> bool:
        if self._key not in d:
            return False
        return self._value_predicate(d[self._key])
    
    def __repr__(self) -> str:
        return f"key[{self._key!r}]={self._value_predicate!r}"


# ============================================================================
# 属性/项谓词
# ============================================================================

class AttrPredicate(Predicate[Any]):
    """属性谓词 - 检查对象属性"""
    
    def __init__(self, attr: str, predicate: Predicate):
        self._attr = attr
        self._predicate = predicate
    
    def __call__(self, obj: Any) -> bool:
        try:
            value = getattr(obj, self._attr)
            return self._predicate(value)
        except AttributeError:
            return False
    
    def __repr__(self) -> str:
        return f".{self._attr}{self._predicate!r}"


class ItemPredicate(Predicate[Any]):
    """项谓词 - 检查容器项"""
    
    def __init__(self, key: Any, predicate: Predicate):
        self._key = key
        self._predicate = predicate
    
    def __call__(self, container: Any) -> bool:
        try:
            value = container[self._key]
            return self._predicate(value)
        except (KeyError, IndexError, TypeError):
            return False
    
    def __repr__(self) -> str:
        return f"[{self._key!r}]{self._predicate!r}"


# ============================================================================
# 函数包装谓词
# ============================================================================

class FunctionPredicate(Predicate[T]):
    """函数包装谓词"""
    
    def __init__(self, func: Callable[[T], bool], description: str = ""):
        self._func = func
        self._description = description or func.__name__ or "lambda"
    
    def __call__(self, value: T) -> bool:
        return self._func(value)
    
    def __repr__(self) -> str:
        return f"Predicate({self._description})"


# ============================================================================
# 常用谓词实例
# ============================================================================

# 类型检查谓词
is_none = IsNonePredicate()
is_not_none = IsNotNonePredicate()
is_empty = IsEmptyPredicate()
is_not_empty = IsNotEmptyPredicate()

# 数值谓词
is_positive = IsPositivePredicate()
is_negative = IsNegativePredicate()
is_zero = IsZeroPredicate()
is_even = IsEvenPredicate()
is_odd = IsOddPredicate()
is_integer = IsIntegerPredicate()
is_float = IsFloatPredicate()
is_finite = IsFinitePredicate()
is_infinite = IsInfinitePredicate()
is_nan = IsNaNPredicate()

# 字符串谓词
is_alnum = IsAlnumPredicate()
is_alpha = IsAlphaPredicate()
is_digit = IsDigitPredicate()
is_numeric = IsNumericPredicate()
is_lower = IsLowerPredicate()
is_upper = IsUpperPredicate()
is_space = IsSpacePredicate()
is_title = IsTitlePredicate()


# ============================================================================
# 谓词构建器函数
# ============================================================================

def eq(expected: T) -> EqualsPredicate[T]:
    """等于谓词"""
    return EqualsPredicate(expected)


def ne(expected: T) -> NotEqualsPredicate[T]:
    """不等于谓词"""
    return NotEqualsPredicate(expected)


def lt(threshold: T) -> LessThanPredicate[T]:
    """小于谓词"""
    return LessThanPredicate(threshold)


def le(threshold: T) -> LessThanOrEqualPredicate[T]:
    """小于等于谓词"""
    return LessThanOrEqualPredicate(threshold)


def gt(threshold: T) -> GreaterThanPredicate[T]:
    """大于谓词"""
    return GreaterThanPredicate(threshold)


def ge(threshold: T) -> GreaterThanOrEqualPredicate[T]:
    """大于等于谓词"""
    return GreaterThanOrEqualPredicate(threshold)


def between(low: T, high: T, inclusive: bool = True) -> BetweenPredicate[T]:
    """区间谓词"""
    return BetweenPredicate(low, high, inclusive)


def in_(collection: Iterable[T]) -> InPredicate[T]:
    """包含于谓词"""
    return InPredicate(collection)


def not_in(collection: Iterable[T]) -> NotInPredicate[T]:
    """不包含于谓词"""
    return NotInPredicate(collection)


def isinstance_of(types: Union[type, Tuple[type, ...]]) -> IsInstancePredicate:
    """是某类型实例谓词"""
    return IsInstancePredicate(types)


def issubclass_of(types: Union[type, Tuple[type, ...]]) -> IsSubclassPredicate:
    """是某类型子类谓词"""
    return IsSubclassPredicate(types)


def starts_with(prefix: str, case_sensitive: bool = True) -> StartsWithPredicate:
    """以...开头谓词"""
    return StartsWithPredicate(prefix, case_sensitive)


def ends_with(suffix: str, case_sensitive: bool = True) -> EndsWithPredicate:
    """以...结尾谓词"""
    return EndsWithPredicate(suffix, case_sensitive)


def contains(substring: str, case_sensitive: bool = True) -> ContainsPredicate:
    """包含子串谓词"""
    return ContainsPredicate(substring, case_sensitive)


def matches(pattern: Union[str, Pattern], flags: int = 0) -> MatchesPredicate:
    """正则匹配谓词"""
    return MatchesPredicate(pattern, flags)


def length(min_len: Optional[int] = None, max_len: Optional[int] = None) -> LengthPredicate:
    """长度谓词"""
    return LengthPredicate(min_len, max_len)


def has_size(size: int) -> HasSizePredicate:
    """大小谓词"""
    return HasSizePredicate(size)


def divisible_by(divisor: int) -> DivisibleByPredicate:
    """能被...整除谓词"""
    return DivisibleByPredicate(divisor)


def multiple_of(base: int) -> MultipleOfPredicate:
    """是...的倍数谓词"""
    return MultipleOfPredicate(base)


def contains_all(items: Iterable[T]) -> ContainsAllPredicate[T]:
    """包含所有元素谓词"""
    return ContainsAllPredicate(items)


def contains_any(items: Iterable[T]) -> ContainsAnyPredicate[T]:
    """包含任一元素谓词"""
    return ContainsAnyPredicate(items)


def contains_none(items: Iterable[T]) -> ContainsNonePredicate[T]:
    """不包含任何元素谓词"""
    return ContainsNonePredicate(items)


def has_key(key: Any) -> HasKeyPredicate:
    """包含键谓词"""
    return HasKeyPredicate(key)


def has_value(value: Any) -> HasValuePredicate:
    """包含值谓词"""
    return HasValuePredicate(value)


def key_value(key: Any, predicate: Predicate) -> KeyValuePredicate:
    """键值匹配谓词"""
    return KeyValuePredicate(key, predicate)


def attr(name: str, predicate: Predicate) -> AttrPredicate:
    """属性谓词"""
    return AttrPredicate(name, predicate)


def item(key: Any, predicate: Predicate) -> ItemPredicate:
    """项谓词"""
    return ItemPredicate(key, predicate)


def predicate(func: Callable[[T], bool], description: str = "") -> FunctionPredicate[T]:
    """函数包装谓词"""
    return FunctionPredicate(func, description)


def all_of(*predicates: Predicate[T]) -> AndPredicate[T]:
    """所有条件都满足（AND）"""
    return AndPredicate(list(predicates))


def any_of(*predicates: Predicate[T]) -> OrPredicate[T]:
    """任一条件满足（OR）"""
    return OrPredicate(list(predicates))


def none_of(*predicates: Predicate[T]) -> NorPredicate[T]:
    """所有条件都不满足（NOR）"""
    return NorPredicate(list(predicates))


def exactly(count: int, *predicates: Predicate[T]) -> ExactlyPredicate[T]:
    """恰好 N 个条件满足"""
    return ExactlyPredicate(list(predicates), count)


def at_least(count: int, *predicates: Predicate[T]) -> AtLeastPredicate[T]:
    """至少 N 个条件满足"""
    return AtLeastPredicate(list(predicates), count)


def at_most(count: int, *predicates: Predicate[T]) -> AtMostPredicate[T]:
    """最多 N 个条件满足"""
    return AtMostPredicate(list(predicates), count)


def implies(antecedent: Predicate[T], consequent: Predicate[T]) -> ImplicationPredicate[T]:
    """蕴涵谓词（A => B）"""
    return ImplicationPredicate(antecedent, consequent)


# ============================================================================
# 模块元数据
# ============================================================================

__version__ = "1.0.0"
__author__ = "AllToolkit"
__all__ = [
    # 核心类
    'Predicate',
    
    # 复合谓词
    'AndPredicate',
    'OrPredicate',
    'NotPredicate',
    'XorPredicate',
    'NandPredicate',
    'NorPredicate',
    'ImplicationPredicate',
    'ExactlyPredicate',
    'AtLeastPredicate',
    'AtMostPredicate',
    
    # 比较谓词
    'EqualsPredicate',
    'NotEqualsPredicate',
    'LessThanPredicate',
    'LessThanOrEqualPredicate',
    'GreaterThanPredicate',
    'GreaterThanOrEqualPredicate',
    'BetweenPredicate',
    'InPredicate',
    'NotInPredicate',
    
    # 类型谓词
    'IsNonePredicate',
    'IsNotNonePredicate',
    'IsInstancePredicate',
    'IsSubclassPredicate',
    
    # 字符串谓词
    'StartsWithPredicate',
    'EndsWithPredicate',
    'ContainsPredicate',
    'MatchesPredicate',
    'LengthPredicate',
    'IsEmptyPredicate',
    'IsNotEmptyPredicate',
    'IsAlnumPredicate',
    'IsAlphaPredicate',
    'IsDigitPredicate',
    'IsNumericPredicate',
    'IsLowerPredicate',
    'IsUpperPredicate',
    'IsSpacePredicate',
    'IsTitlePredicate',
    
    # 数值谓词
    'IsPositivePredicate',
    'IsNegativePredicate',
    'IsZeroPredicate',
    'IsEvenPredicate',
    'IsOddPredicate',
    'IsIntegerPredicate',
    'IsFloatPredicate',
    'IsFinitePredicate',
    'IsInfinitePredicate',
    'IsNaNPredicate',
    'DivisibleByPredicate',
    'MultipleOfPredicate',
    
    # 集合谓词
    'ContainsAllPredicate',
    'ContainsAnyPredicate',
    'ContainsNonePredicate',
    'HasSizePredicate',
    
    # 字典谓词
    'HasKeyPredicate',
    'HasValuePredicate',
    'KeyValuePredicate',
    
    # 属性/项谓词
    'AttrPredicate',
    'ItemPredicate',
    
    # 函数谓词
    'FunctionPredicate',
    
    # 常用谓词实例
    'is_none',
    'is_not_none',
    'is_empty',
    'is_not_empty',
    'is_positive',
    'is_negative',
    'is_zero',
    'is_even',
    'is_odd',
    'is_integer',
    'is_float',
    'is_finite',
    'is_infinite',
    'is_nan',
    'is_alnum',
    'is_alpha',
    'is_digit',
    'is_numeric',
    'is_lower',
    'is_upper',
    'is_space',
    'is_title',
    
    # 构建器函数
    'eq',
    'ne',
    'lt',
    'le',
    'gt',
    'ge',
    'between',
    'in_',
    'not_in',
    'isinstance_of',
    'issubclass_of',
    'starts_with',
    'ends_with',
    'contains',
    'matches',
    'length',
    'has_size',
    'divisible_by',
    'multiple_of',
    'contains_all',
    'contains_any',
    'contains_none',
    'has_key',
    'has_value',
    'key_value',
    'attr',
    'item',
    'predicate',
    'all_of',
    'any_of',
    'none_of',
    'exactly',
    'at_least',
    'at_most',
    'implies',
]