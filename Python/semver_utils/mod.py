"""
语义化版本工具 (SemVer Utils)

遵循 Semantic Versioning 2.0.0 规范
https://semver.org/

功能:
- 版本解析与验证
- 版本比较
- 版本递增（major/minor/patch）
- 预发布版本处理
- 版本范围匹配
- 版本排序
- 版本约束解析（^、~、>、<、>=、<=、=）
"""

import re
from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Union, Callable
from functools import total_ordering


@dataclass
@total_ordering
class SemVer:
    """语义化版本对象"""
    major: int
    minor: int
    patch: int
    prerelease: Optional[str] = None
    build: Optional[str] = None
    
    def __str__(self) -> str:
        """转换为版本字符串"""
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version += f"-{self.prerelease}"
        if self.build:
            version += f"+{self.build}"
        return version
    
    def __repr__(self) -> str:
        return f"SemVer({self})"
    
    def __hash__(self) -> int:
        # 根据 SemVer 规范，build 元数据不参与比较
        return hash((self.major, self.minor, self.patch, self.prerelease))
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, SemVer):
            return NotImplemented
        # 根据 SemVer 规范，build 元数据不参与比较
        return (
            self.major == other.major and
            self.minor == other.minor and
            self.patch == other.patch and
            self._normalize_prerelease() == other._normalize_prerelease()
        )
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, SemVer):
            return NotImplemented
        return self._compare(other) < 0
    
    def _normalize_prerelease(self) -> Tuple:
        """将预发布标识规范化为可比较的元组"""
        if not self.prerelease:
            return ()  # 无预发布标识 > 有预发布标识
        
        parts = []
        for part in self.prerelease.split('.'):
            if part.isdigit():
                parts.append((0, int(part)))  # 数字标识符
            else:
                parts.append((1, part))  # 字母标识符
        return tuple(parts)
    
    def _compare(self, other: 'SemVer') -> int:
        """比较两个版本，返回 -1, 0, 1"""
        # 比较 major
        if self.major != other.major:
            return -1 if self.major < other.major else 1
        
        # 比较 minor
        if self.minor != other.minor:
            return -1 if self.minor < other.minor else 1
        
        # 比较 patch
        if self.patch != other.patch:
            return -1 if self.patch < other.patch else 1
        
        # 比较预发布标识
        # 无预发布 > 有预发布
        self_pre = self.prerelease
        other_pre = other.prerelease
        
        if self_pre is None and other_pre is None:
            return 0
        if self_pre is None:
            return 1  # self > other (无预发布更大)
        if other_pre is None:
            return -1  # self < other (有预发布更小)
        
        # 比较预发布标识部分
        self_parts = self_pre.split('.')
        other_parts = other_pre.split('.')
        
        for i in range(max(len(self_parts), len(other_parts))):
            if i >= len(self_parts):
                return -1  # self 较短，更小
            if i >= len(other_parts):
                return 1  # other 较短，self 更大
            
            s_part = self_parts[i]
            o_part = other_parts[i]
            
            s_is_num = s_part.isdigit()
            o_is_num = o_part.isdigit()
            
            if s_is_num and o_is_num:
                # 两个都是数字
                if int(s_part) != int(o_part):
                    return -1 if int(s_part) < int(o_part) else 1
            elif s_is_num:
                # 数字 < 字母
                return -1
            elif o_is_num:
                # 字母 > 数字
                return 1
            else:
                # 两个都是字母
                if s_part != o_part:
                    return -1 if s_part < o_part else 1
        
        return 0
    
    def bump_major(self, reset_prerelease: bool = True) -> 'SemVer':
        """递增主版本号"""
        prerelease = None if reset_prerelease else self.prerelease
        return SemVer(self.major + 1, 0, 0, prerelease, self.build)
    
    def bump_minor(self, reset_prerelease: bool = True) -> 'SemVer':
        """递增次版本号"""
        prerelease = None if reset_prerelease else self.prerelease
        return SemVer(self.major, self.minor + 1, 0, prerelease, self.build)
    
    def bump_patch(self, reset_prerelease: bool = True) -> 'SemVer':
        """递增修订版本号"""
        prerelease = None if reset_prerelease else self.prerelease
        return SemVer(self.major, self.minor, self.patch + 1, prerelease, self.build)
    
    def bump_prerelease(self, identifier: str = "alpha") -> 'SemVer':
        """
        递增预发布版本
        - 如果无预发布，创建 {identifier}.1
        - 如果有预发布且匹配标识符，递增数字
        - 如果有预发布但不匹配，创建新的 {identifier}.1
        """
        if not self.prerelease:
            return SemVer(self.major, self.minor, self.patch, f"{identifier}.1", self.build)
        
        parts = self.prerelease.split('.')
        
        # 检查是否匹配标识符模式
        if len(parts) >= 2 and parts[0] == identifier and parts[-1].isdigit():
            # 递增数字
            num = int(parts[-1])
            parts[-1] = str(num + 1)
            return SemVer(self.major, self.minor, self.patch, '.'.join(parts), self.build)
        
        # 创建新的预发布版本
        return SemVer(self.major, self.minor, self.patch, f"{identifier}.1", self.build)
    
    def with_prerelease(self, identifier: str) -> 'SemVer':
        """设置预发布标识"""
        return SemVer(self.major, self.minor, self.patch, identifier, self.build)
    
    def with_build(self, build: str) -> 'SemVer':
        """设置构建元数据"""
        return SemVer(self.major, self.minor, self.patch, self.prerelease, build)
    
    def release(self) -> 'SemVer':
        """返回正式版本（移除预发布标识）"""
        return SemVer(self.major, self.minor, self.patch, None, self.build)
    
    @property
    def is_prerelease(self) -> bool:
        """是否为预发布版本"""
        return self.prerelease is not None
    
    @property
    def is_stable(self) -> bool:
        """是否为稳定版本（非预发布且主版本号 > 0）"""
        return not self.is_prerelease and self.major > 0


# 版本字符串正则表达式
SEMVER_PATTERN = re.compile(
    r'^(?P<major>0|[1-9]\d*)'
    r'\.(?P<minor>0|[1-9]\d*)'
    r'\.(?P<patch>0|[1-9]\d*)'
    r'(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
    r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?'
    r'(?:\+(?P<build>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
)


def parse(version: str) -> SemVer:
    """
    解析版本字符串
    
    Args:
        version: 版本字符串，如 "1.2.3", "1.0.0-alpha.1", "2.0.0+build.123"
    
    Returns:
        SemVer 对象
    
    Raises:
        ValueError: 无效的版本字符串
    """
    match = SEMVER_PATTERN.match(version.strip())
    if not match:
        raise ValueError(f"Invalid semantic version: '{version}'")
    
    return SemVer(
        major=int(match.group('major')),
        minor=int(match.group('minor')),
        patch=int(match.group('patch')),
        prerelease=match.group('prerelease'),
        build=match.group('build')
    )


def try_parse(version: str) -> Optional[SemVer]:
    """
    尝试解析版本字符串，失败返回 None
    
    Args:
        version: 版本字符串
    
    Returns:
        SemVer 对象或 None
    """
    try:
        return parse(version)
    except ValueError:
        return None


def is_valid(version: str) -> bool:
    """
    验证版本字符串是否有效
    
    Args:
        version: 版本字符串
    
    Returns:
        是否有效
    """
    return try_parse(version) is not None


def compare(v1: Union[str, SemVer], v2: Union[str, SemVer]) -> int:
    """
    比较两个版本
    
    Args:
        v1: 版本1
        v2: 版本2
    
    Returns:
        -1 if v1 < v2, 0 if v1 == v2, 1 if v1 > v2
    """
    if isinstance(v1, str):
        v1 = parse(v1)
    if isinstance(v2, str):
        v2 = parse(v2)
    return v1._compare(v2)


def equals(v1: Union[str, SemVer], v2: Union[str, SemVer]) -> bool:
    """判断两个版本是否相等"""
    return compare(v1, v2) == 0


def greater_than(v1: Union[str, SemVer], v2: Union[str, SemVer]) -> bool:
    """判断 v1 > v2"""
    return compare(v1, v2) > 0


def less_than(v1: Union[str, SemVer], v2: Union[str, SemVer]) -> bool:
    """判断 v1 < v2"""
    return compare(v1, v2) < 0


def gte(v1: Union[str, SemVer], v2: Union[str, SemVer]) -> bool:
    """判断 v1 >= v2"""
    return compare(v1, v2) >= 0


def lte(v1: Union[str, SemVer], v2: Union[str, SemVer]) -> bool:
    """判断 v1 <= v2"""
    return compare(v1, v2) <= 0


def sort(versions: List[Union[str, SemVer]], reverse: bool = False) -> List[SemVer]:
    """
    排序版本列表
    
    Args:
        versions: 版本列表
        reverse: 是否降序
    
    Returns:
        排序后的 SemVer 列表
    """
    parsed = [parse(v) if isinstance(v, str) else v for v in versions]
    return sorted(parsed, reverse=reverse)


def rsort(versions: List[Union[str, SemVer]]) -> List[SemVer]:
    """降序排序版本列表"""
    return sort(versions, reverse=True)


def min_version(versions: List[Union[str, SemVer]]) -> Optional[SemVer]:
    """获取最小版本"""
    if not versions:
        return None
    return sort(versions)[0]


def max_version(versions: List[Union[str, SemVer]]) -> Optional[SemVer]:
    """获取最大版本"""
    if not versions:
        return None
    return sort(versions, reverse=True)[0]


# ============ 版本范围匹配 ============

@dataclass
class VersionRange:
    """版本范围"""
    min_version: Optional[SemVer] = None
    max_version: Optional[SemVer] = None
    min_inclusive: bool = True
    max_inclusive: bool = False
    
    def contains(self, version: Union[str, SemVer]) -> bool:
        """检查版本是否在范围内"""
        if isinstance(version, str):
            version = parse(version)
        
        # 检查最小版本
        if self.min_version:
            cmp = version._compare(self.min_version)
            if self.min_inclusive:
                if cmp < 0:
                    return False
            else:
                if cmp <= 0:
                    return False
        
        # 检查最大版本
        if self.max_version:
            cmp = version._compare(self.max_version)
            if self.max_inclusive:
                if cmp > 0:
                    return False
            else:
                if cmp >= 0:
                    return False
        
        return True
    
    def __str__(self) -> str:
        parts = []
        if self.min_version:
            op = ">=" if self.min_inclusive else ">"
            parts.append(f"{op}{self.min_version}")
        if self.max_version:
            op = "<=" if self.max_inclusive else "<"
            parts.append(f"{op}{self.max_version}")
        return " ".join(parts) if parts else "*"


def parse_range(range_str: str) -> VersionRange:
    """
    解析版本范围字符串
    
    支持格式:
    - "*" - 所有版本
    - "1.2.3" - 精确版本
    - ">=1.2.3" - 大于等于
    - ">1.2.3" - 大于
    - "<=1.2.3" - 小于等于
    - "<1.2.3" - 小于
    - ">=1.0.0 <2.0.0" - 范围
    - "^1.2.3" - 兼容版本 (>=1.2.3 <2.0.0)
    - "~1.2.3" - 补丁版本范围 (>=1.2.3 <1.3.0)
    - "~1.2" - 次版本范围 (>=1.2.0 <1.3.0)
    - "1.2.x" 或 "1.2.*" - 通配符范围
    
    Args:
        range_str: 范围字符串
    
    Returns:
        VersionRange 对象
    """
    range_str = range_str.strip()
    
    # 所有版本
    if range_str == "*":
        return VersionRange()
    
    # 通配符范围 (1.2.x 或 1.2.*)
    if 'x' in range_str or '*' in range_str:
        original_parts = range_str.replace('x', '').replace('*', '').rstrip('.').split('.')
        original_parts = [p for p in original_parts if p]  # 移除空字符串
        
        # 构建最小版本
        min_parts = []
        for p in original_parts:
            min_parts.append(int(p) if p.isdigit() else 0)
        while len(min_parts) < 3:
            min_parts.append(0)
        min_v = SemVer(min_parts[0], min_parts[1], min_parts[2])
        
        # 计算最大版本（基于原始通配符位置）
        # "x" 或 "*" -> 所有版本
        if original_parts[0] == '' or len(original_parts) == 0:
            return VersionRange()
        # "1.x" 或 "1.*" -> >=1.0.0 <2.0.0
        if len(original_parts) == 1:
            max_v = SemVer(min_v.major + 1, 0, 0)
        # "1.2.x" 或 "1.2.*" -> >=1.2.0 <1.3.0
        elif len(original_parts) == 2:
            max_v = SemVer(min_v.major, min_v.minor + 1, 0)
        # "1.2.3.x" -> 不常见，但支持 >=1.2.3 <1.2.4
        else:
            max_v = SemVer(min_v.major, min_v.minor, min_v.patch + 1)
        return VersionRange(min_v, max_v, True, False)
    
    # 插入符范围 (^1.2.3)
    if range_str.startswith('^'):
        version = parse(range_str[1:])
        min_v = version
        
        # ^0.0.3 := >=0.0.3 <0.0.4
        # ^0.2.3 := >=0.2.3 <0.3.0
        # ^1.2.3 := >=1.2.3 <2.0.0
        if version.major == 0:
            if version.minor == 0:
                max_v = SemVer(0, 0, version.patch + 1)
            else:
                max_v = SemVer(0, version.minor + 1, 0)
        else:
            max_v = SemVer(version.major + 1, 0, 0)
        
        return VersionRange(min_v, max_v, True, False)
    
    # 波浪号范围 (~1.2.3)
    if range_str.startswith('~'):
        version_str = range_str[1:]
        parts = version_str.split('.')
        
        if len(parts) == 1:
            # ~1 := >=1.0.0 <2.0.0
            min_v = parse(f"{parts[0]}.0.0")
            max_v = SemVer(min_v.major + 1, 0, 0)
        elif len(parts) == 2:
            # ~1.2 := >=1.2.0 <1.3.0
            min_v = parse(f"{parts[0]}.{parts[1]}.0")
            max_v = SemVer(min_v.major, min_v.minor + 1, 0)
        else:
            # ~1.2.3 := >=1.2.3 <1.3.0
            min_v = parse(version_str)
            max_v = SemVer(min_v.major, min_v.minor + 1, 0)
        
        return VersionRange(min_v, max_v, True, False)
    
    # 精确版本
    if re.match(r'^\d+\.\d+\.\d+', range_str):
        version = parse(range_str)
        return VersionRange(version, version, True, True)
    
    # 比较运算符范围
    # 支持组合: ">=1.0.0 <2.0.0"
    constraints = range_str.split()
    
    result = VersionRange()
    
    for constraint in constraints:
        constraint = constraint.strip()
        if not constraint:
            continue
        
        # 解析单个约束
        match = re.match(r'^(>=|<=|>|<|=)?(.+)$', constraint)
        if not match:
            raise ValueError(f"Invalid version range: '{range_str}'")
        
        op = match.group(1) or '='
        version_str = match.group(2)
        version = parse(version_str)
        
        if op == '>=':
            result.min_version = version
            result.min_inclusive = True
        elif op == '>':
            result.min_version = version
            result.min_inclusive = False
        elif op == '<=':
            result.max_version = version
            result.max_inclusive = True
        elif op == '<':
            result.max_version = version
            result.max_inclusive = False
        elif op == '=':
            result.min_version = version
            result.max_version = version
            result.min_inclusive = True
            result.max_inclusive = True
    
    return result


def satisfies(version: Union[str, SemVer], range_str: str) -> bool:
    """
    检查版本是否满足范围约束
    
    Args:
        version: 版本
        range_str: 范围字符串
    
    Returns:
        是否满足
    """
    return parse_range(range_str).contains(version)


def filter_versions(versions: List[Union[str, SemVer]], 
                   range_str: str) -> List[SemVer]:
    """
    过滤满足范围的版本
    
    Args:
        versions: 版本列表
        range_str: 范围字符串
    
    Returns:
        满足条件的版本列表
    """
    vr = parse_range(range_str)
    return [parse(v) if isinstance(v, str) else v 
            for v in versions if vr.contains(v)]


def find_best_match(versions: List[Union[str, SemVer]], 
                   range_str: str,
                   prefer_prerelease: bool = False) -> Optional[SemVer]:
    """
    在版本列表中查找最佳匹配（最高版本）
    
    Args:
        versions: 版本列表
        range_str: 范围字符串
        prefer_prerelease: 是否优先选择预发布版本
    
    Returns:
        最佳匹配版本或 None
    """
    matched = filter_versions(versions, range_str)
    if not matched:
        return None
    
    # 默认排除预发布版本
    if not prefer_prerelease:
        stable = [v for v in matched if not v.is_prerelease]
        if stable:
            matched = stable
    
    return max_version(matched)


# ============ 版本差异分析 ============

@dataclass
class VersionDiff:
    """版本差异"""
    major_diff: int
    minor_diff: int
    patch_diff: int
    prerelease_change: Optional[Tuple[Optional[str], Optional[str]]] = None
    build_change: Optional[Tuple[Optional[str], Optional[str]]] = None
    
    @property
    def is_upgrade(self) -> bool:
        """是否为升级"""
        return (self.major_diff > 0 or 
                (self.major_diff == 0 and self.minor_diff > 0) or
                (self.major_diff == 0 and self.minor_diff == 0 and self.patch_diff > 0))
    
    @property
    def is_downgrade(self) -> bool:
        """是否为降级"""
        return (self.major_diff < 0 or 
                (self.major_diff == 0 and self.minor_diff < 0) or
                (self.major_diff == 0 and self.minor_diff == 0 and self.patch_diff < 0))
    
    @property
    def is_major_change(self) -> bool:
        """是否为主版本变更"""
        return self.major_diff != 0
    
    @property
    def is_minor_change(self) -> bool:
        """是否为次版本变更"""
        return self.minor_diff != 0
    
    @property
    def is_patch_change(self) -> bool:
        """是否为修订版本变更"""
        return self.patch_diff != 0
    
    def __str__(self) -> str:
        changes = []
        if self.major_diff != 0:
            changes.append(f"major:{self.major_diff:+d}")
        if self.minor_diff != 0:
            changes.append(f"minor:{self.minor_diff:+d}")
        if self.patch_diff != 0:
            changes.append(f"patch:{self.patch_diff:+d}")
        if self.prerelease_change:
            changes.append(f"prerelease:{self.prerelease_change[0]}→{self.prerelease_change[1]}")
        if self.build_change:
            changes.append(f"build:{self.build_change[0]}→{self.build_change[1]}")
        return ", ".join(changes) if changes else "no change"


def diff(v1: Union[str, SemVer], v2: Union[str, SemVer]) -> VersionDiff:
    """
    计算两个版本的差异
    
    Args:
        v1: 旧版本
        v2: 新版本
    
    Returns:
        VersionDiff 对象
    """
    if isinstance(v1, str):
        v1 = parse(v1)
    if isinstance(v2, str):
        v2 = parse(v2)
    
    prerelease_change = None
    if v1.prerelease != v2.prerelease:
        prerelease_change = (v1.prerelease, v2.prerelease)
    
    build_change = None
    if v1.build != v2.build:
        build_change = (v1.build, v2.build)
    
    return VersionDiff(
        major_diff=v2.major - v1.major,
        minor_diff=v2.minor - v1.minor,
        patch_diff=v2.patch - v1.patch,
        prerelease_change=prerelease_change,
        build_change=build_change
    )


# ============ 版本格式化 ============

def format(version: Union[str, SemVer], 
         include_prerelease: bool = True,
         include_build: bool = True) -> str:
    """
    格式化版本字符串
    
    Args:
        version: 版本
        include_prerelease: 是否包含预发布标识
        include_build: 是否包含构建元数据
    
    Returns:
        格式化后的版本字符串
    """
    if isinstance(version, str):
        version = parse(version)
    
    result = f"{version.major}.{version.minor}.{version.patch}"
    
    if include_prerelease and version.prerelease:
        result += f"-{version.prerelease}"
    
    if include_build and version.build:
        result += f"+{version.build}"
    
    return result


def to_tuple(version: Union[str, SemVer]) -> Tuple[int, int, int]:
    """将版本转换为元组 (major, minor, patch)"""
    if isinstance(version, str):
        version = parse(version)
    return (version.major, version.minor, version.patch)


def from_tuple(t: Tuple[int, int, int], 
              prerelease: Optional[str] = None,
              build: Optional[str] = None) -> SemVer:
    """从元组创建版本"""
    return SemVer(t[0], t[1], t[2], prerelease, build)


# ============ 版本集合操作 ============

def unique(versions: List[Union[str, SemVer]]) -> List[SemVer]:
    """去重版本列表"""
    seen = set()
    result = []
    for v in versions:
        parsed = parse(v) if isinstance(v, str) else v
        key = (parsed.major, parsed.minor, parsed.patch, parsed.prerelease)
        if key not in seen:
            seen.add(key)
            result.append(parsed)
    return result


def next_versions(version: Union[str, SemVer], 
                 include_prerelease: bool = False) -> List[SemVer]:
    """
    获取可能的下一个版本列表
    
    Args:
        version: 当前版本
        include_prerelease: 是否包含预发布版本
    
    Returns:
        下一个版本列表
    """
    if isinstance(version, str):
        version = parse(version)
    
    versions = [
        version.bump_patch(),
        version.bump_minor(),
        version.bump_major(),
    ]
    
    if include_prerelease:
        versions.extend([
            version.bump_prerelease("alpha"),
            version.bump_prerelease("beta"),
            version.bump_prerelease("rc"),
        ])
    
    return versions


# ============ 常用版本常量 ============

ZERO = SemVer(0, 0, 0)
ONE = SemVer(1, 0, 0)


# ============ 便捷函数 ============

def major(version: Union[str, SemVer]) -> int:
    """获取主版本号"""
    return parse(version).major if isinstance(version, str) else version.major


def minor(version: Union[str, SemVer]) -> int:
    """获取次版本号"""
    return parse(version).minor if isinstance(version, str) else version.minor


def patch(version: Union[str, SemVer]) -> int:
    """获取修订版本号"""
    return parse(version).patch if isinstance(version, str) else version.patch


def prerelease(version: Union[str, SemVer]) -> Optional[str]:
    """获取预发布标识"""
    return parse(version).prerelease if isinstance(version, str) else version.prerelease


def build(version: Union[str, SemVer]) -> Optional[str]:
    """获取构建元数据"""
    return parse(version).build if isinstance(version, str) else version.build