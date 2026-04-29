"""
语义版本工具 (Semantic Versioning Utils)

提供语义版本号的解析、比较、验证、递增等功能。
遵循 Semantic Versioning 2.0.0 规范 (https://semver.org/)

功能:
- 版本解析：解析语义版本字符串，提取主版本、次版本、修订版本等
- 版本比较：支持 >, <, >=, <=, ==, != 等比较操作
- 版本验证：验证字符串是否符合语义版本规范
- 版本递增：支持 major, minor, patch 递增
- 范围匹配：检查版本是否满足版本范围约束
- 预发布处理：解析和比较预发布版本标识符
- 构建元数据：解析和处理构建元数据

零依赖，仅使用 Python 标准库
"""

import re
from dataclasses import dataclass
from typing import Optional, Tuple, List, Union


@dataclass
class SemanticVersion:
    """
    语义版本数据类
    
    属性:
        major: 主版本号
        minor: 次版本号
        patch: 修订版本号
        prerelease: 预发布标识符列表（如 ['alpha', '1']）
        build_metadata: 构建元数据字符串
    """
    major: int
    minor: int
    patch: int
    prerelease: Optional[List[Union[str, int]]] = None
    build_metadata: Optional[str] = None
    
    def __str__(self) -> str:
        """转换为语义版本字符串"""
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version += "-" + ".".join(str(p) for p in self.prerelease)
        if self.build_metadata:
            version += "+" + self.build_metadata
        return version
    
    def __repr__(self) -> str:
        return f"SemanticVersion({self})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        # 比较时忽略 build_metadata
        return (
            self.major == other.major and
            self.minor == other.minor and
            self.patch == other.patch and
            self.prerelease == other.prerelease
        )
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return self._compare(other) < 0
    
    def __le__(self, other) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return self._compare(other) <= 0
    
    def __gt__(self, other) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return self._compare(other) > 0
    
    def __ge__(self, other) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return self._compare(other) >= 0
    
    def __hash__(self) -> int:
        prerelease_tuple = tuple(self.prerelease) if self.prerelease else None
        return hash((self.major, self.minor, self.patch, prerelease_tuple))
    
    def _compare(self, other: 'SemanticVersion') -> int:
        """
        比较两个语义版本
        
        返回:
            -1: self < other
             0: self == other
             1: self > other
        """
        # 比较 major.minor.patch
        if self.major != other.major:
            return -1 if self.major < other.major else 1
        if self.minor != other.minor:
            return -1 if self.minor < other.minor else 1
        if self.patch != other.patch:
            return -1 if self.patch < other.patch else 1
        
        # 预发布版本比较规则：
        # 1. 没有预发布标识符的版本 > 有预发布标识符的版本
        # 2. 预发布标识符从左到右比较
        if self.prerelease is None and other.prerelease is None:
            return 0
        if self.prerelease is None:
            return 1  # 正式版本 > 预发布版本
        if other.prerelease is None:
            return -1  # 预发布版本 < 正式版本
        
        # 比较预发布标识符
        return self._compare_prerelease(self.prerelease, other.prerelease)
    
    @staticmethod
    def _compare_prerelease(pr1: List[Union[str, int]], pr2: List[Union[str, int]]) -> int:
        """比较两个预发布标识符列表"""
        for i in range(max(len(pr1), len(pr2))):
            if i >= len(pr1):
                return -1  # pr1 较短，pr1 < pr2
            if i >= len(pr2):
                return 1   # pr2 较短，pr1 > pr2
            
            id1, id2 = pr1[i], pr2[i]
            
            # 数值标识符 < 字符串标识符
            if isinstance(id1, int) and isinstance(id2, str):
                return -1
            if isinstance(id1, str) and isinstance(id2, int):
                return 1
            
            if id1 < id2:
                return -1
            if id1 > id2:
                return 1
        
        return 0
    
    def to_tuple(self) -> Tuple[int, int, int]:
        """返回 (major, minor, patch) 元组"""
        return (self.major, self.minor, self.patch)
    
    def is_prerelease(self) -> bool:
        """是否为预发布版本"""
        return self.prerelease is not None and len(self.prerelease) > 0
    
    def is_stable(self) -> bool:
        """是否为稳定版本（major > 0 且非预发布）"""
        return self.major > 0 and not self.is_prerelease()


# 语义版本正则表达式（符合 SemVer 2.0.0 规范）
SEMVER_PATTERN = re.compile(
    r'^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)'
    r'(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
    r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?'
    r'(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
)


def parse(version_string: str) -> SemanticVersion:
    """
    解析语义版本字符串
    
    参数:
        version_string: 版本字符串（如 "1.2.3", "1.0.0-alpha.1", "2.0.0+build.123"）
    
    返回:
        SemanticVersion 对象
    
    异常:
        ValueError: 版本字符串格式无效
    
    示例:
        >>> v = parse("1.2.3")
        >>> v.major, v.minor, v.patch
        (1, 2, 3)
        >>> v = parse("1.0.0-alpha.1+build.123")
        >>> v.prerelease
        ['alpha', 1]
        >>> v.build_metadata
        'build.123'
    """
    match = SEMVER_PATTERN.match(version_string.strip())
    if not match:
        raise ValueError(f"Invalid semantic version: {version_string}")
    
    major = int(match.group('major'))
    minor = int(match.group('minor'))
    patch = int(match.group('patch'))
    
    prerelease = None
    if match.group('prerelease'):
        prerelease = _parse_prerelease(match.group('prerelease'))
    
    build_metadata = match.group('buildmetadata')
    
    return SemanticVersion(
        major=major,
        minor=minor,
        patch=patch,
        prerelease=prerelease,
        build_metadata=build_metadata
    )


def _parse_prerelease(prerelease_str: str) -> List[Union[str, int]]:
    """解析预发布标识符"""
    identifiers = []
    for identifier in prerelease_str.split('.'):
        # 尝试解析为整数
        if identifier.isdigit():
            identifiers.append(int(identifier))
        else:
            identifiers.append(identifier)
    return identifiers


def is_valid(version_string: str) -> bool:
    """
    验证字符串是否为有效的语义版本
    
    参数:
        version_string: 待验证的字符串
    
    返回:
        bool: 是否有效
    
    示例:
        >>> is_valid("1.2.3")
        True
        >>> is_valid("1.2")
        False
        >>> is_valid("1.2.3-alpha.1")
        True
    """
    try:
        parse(version_string)
        return True
    except ValueError:
        return False


def compare(v1: str, v2: str) -> int:
    """
    比较两个语义版本
    
    参数:
        v1: 第一个版本字符串
        v2: 第二个版本字符串
    
    返回:
        -1: v1 < v2
         0: v1 == v2
         1: v1 > v2
    
    示例:
        >>> compare("1.0.0", "2.0.0")
        -1
        >>> compare("2.0.0", "1.0.0")
        1
        >>> compare("1.0.0", "1.0.0")
        0
    """
    return parse(v1)._compare(parse(v2))


def gt(v1: str, v2: str) -> bool:
    """v1 > v2"""
    return parse(v1) > parse(v2)


def gte(v1: str, v2: str) -> bool:
    """v1 >= v2"""
    return parse(v1) >= parse(v2)


def lt(v1: str, v2: str) -> bool:
    """v1 < v2"""
    return parse(v1) < parse(v2)


def lte(v1: str, v2: str) -> bool:
    """v1 <= v2"""
    return parse(v1) <= parse(v2)


def eq(v1: str, v2: str) -> bool:
    """v1 == v2（忽略构建元数据）"""
    return parse(v1) == parse(v2)


def neq(v1: str, v2: str) -> bool:
    """v1 != v2"""
    return not eq(v1, v2)


def increment_major(version: str) -> str:
    """
    递增主版本号（重置 minor 和 patch 为 0，移除预发布标识）
    
    示例:
        >>> increment_major("1.2.3")
        '2.0.0'
        >>> increment_major("1.2.3-alpha")
        '2.0.0'
    """
    v = parse(version)
    return str(SemanticVersion(v.major + 1, 0, 0))


def increment_minor(version: str) -> str:
    """
    递增次版本号（重置 patch 为 0，移除预发布标识）
    
    示例:
        >>> increment_minor("1.2.3")
        '1.3.0'
    """
    v = parse(version)
    return str(SemanticVersion(v.major, v.minor + 1, 0))


def increment_patch(version: str) -> str:
    """
    递增修订版本号（移除预发布标识）
    
    示例:
        >>> increment_patch("1.2.3")
        '1.2.4'
        >>> increment_patch("1.2.3-alpha")
        '1.2.3'
    """
    v = parse(version)
    return str(SemanticVersion(v.major, v.minor, v.patch + 1))


def increment_prerelease(version: str, identifier: str = "rc") -> str:
    """
    递增预发布版本
    
    如果没有预发布标识，创建新的预发布版本
    如果已有预发布标识，递增数值部分
    
    参数:
        version: 版本字符串
        identifier: 预发布标识符（默认 "rc"）
    
    示例:
        >>> increment_prerelease("1.2.3")
        '1.2.4-rc.1'
        >>> increment_prerelease("1.2.3-rc.1")
        '1.2.3-rc.2'
        >>> increment_prerelease("1.2.3-alpha.1")
        '1.2.3-alpha.2'
    """
    v = parse(version)
    
    if v.prerelease is None:
        # 从 patch 递增后开始预发布
        return str(SemanticVersion(v.major, v.minor, v.patch + 1, [identifier, 1]))
    
    # 查找最后一个数字标识符并递增
    prerelease = list(v.prerelease)
    for i in range(len(prerelease) - 1, -1, -1):
        if isinstance(prerelease[i], int):
            prerelease[i] += 1
            break
    else:
        # 没有数字标识符，追加 .1
        prerelease.append(1)
    
    return str(SemanticVersion(v.major, v.minor, v.patch, prerelease))


def major(version: str) -> int:
    """获取主版本号"""
    return parse(version).major


def minor(version: str) -> int:
    """获取次版本号"""
    return parse(version).minor


def patch(version: str) -> int:
    """获取修订版本号"""
    return parse(version).patch


def prerelease(version: str) -> Optional[List[Union[str, int]]]:
    """获取预发布标识符"""
    return parse(version).prerelease


def build_metadata(version: str) -> Optional[str]:
    """获取构建元数据"""
    return parse(version).build_metadata


def diff(v1: str, v2: str) -> Optional[str]:
    """
    获取两个版本之间的差异类型
    
    返回:
        "major": 主版本不同
        "minor": 次版本不同
        "patch": 修订版本不同
        "prerelease": 仅预发布标识不同
        None: 版本相同
    
    示例:
        >>> diff("1.0.0", "2.0.0")
        'major'
        >>> diff("1.0.0", "1.1.0")
        'minor'
        >>> diff("1.0.0", "1.0.1")
        'patch'
    """
    ver1, ver2 = parse(v1), parse(v2)
    
    if ver1.major != ver2.major:
        return "major"
    if ver1.minor != ver2.minor:
        return "minor"
    if ver1.patch != ver2.patch:
        return "patch"
    if ver1.prerelease != ver2.prerelease:
        return "prerelease"
    return None


def satisfies(version: str, range_str: str) -> bool:
    """
    检查版本是否满足版本范围约束
    
    支持的范围格式:
        - "1.2.3": 精确匹配
        - ">1.2.3": 大于
        - ">=1.2.3": 大于等于
        - "<1.2.3": 小于
        - "<=1.2.3": 小于等于
        - "1.2.3 - 2.0.0": 范围（>=1.2.3 <=2.0.0）
        - "~1.2.3": 兼容版本（>=1.2.3 <1.3.0）
        - "^1.2.3": 主版本兼容（>=1.2.3 <2.0.0）
        - "1.2.*": 通配符（>=1.2.0 <1.3.0）
        - "1.x": 通配符（>=1.0.0 <2.0.0）
    
    示例:
        >>> satisfies("1.2.3", ">=1.0.0")
        True
        >>> satisfies("1.2.3", "^1.0.0")
        True
        >>> satisfies("2.0.0", "^1.0.0")
        False
    """
    range_str = range_str.strip()
    v = parse(version)
    
    # 精确匹配
    if SEMVER_PATTERN.match(range_str):
        return v == parse(range_str)
    
    # 范围格式 "1.2.3 - 2.0.0"
    if " - " in range_str:
        low, high = range_str.split(" - ", 1)
        return parse(low) <= v <= parse(high)
    
    # 复合条件（空格分隔）
    if " " in range_str and not any(op in range_str for op in ["~", "^", "*"]):
        parts = range_str.split()
        return all(_satisfies_single(version, part) for part in parts)
    
    # 单一条件
    return _satisfies_single(version, range_str)


def _satisfies_single(version: str, range_str: str) -> bool:
    """处理单一版本条件"""
    v = parse(version)
    
    # 通配符匹配
    if "x" in range_str.lower() or "*" in range_str:
        return _satisfies_wildcard(v, range_str)
    
    # 插入号范围 ^
    if range_str.startswith("^"):
        return _satisfies_caret(v, range_str[1:])
    
    # 波浪号范围 ~
    if range_str.startswith("~"):
        return _satisfies_tilde(v, range_str[1:])
    
    # 比较运算符
    if range_str.startswith(">="):
        return v >= parse(range_str[2:].strip())
    if range_str.startswith(">"):
        return v > parse(range_str[1:].strip())
    if range_str.startswith("<="):
        return v <= parse(range_str[2:].strip())
    if range_str.startswith("<"):
        return v < parse(range_str[1:].strip())
    if range_str.startswith("="):
        return v == parse(range_str[1:].strip())
    
    # 默认精确匹配
    return v == parse(range_str)


def _satisfies_wildcard(v: SemanticVersion, range_str: str) -> bool:
    """处理通配符匹配"""
    range_str = range_str.lower().replace("x", "*")
    parts = range_str.split(".")
    
    if len(parts) == 1:
        # "*" 匹配所有
        if parts[0] == "*":
            return True
        return v.major == int(parts[0])
    
    if len(parts) == 2:
        # "1.*" 或 "1.x"
        if parts[1] == "*":
            return v.major == int(parts[0])
        return v.major == int(parts[0]) and v.minor == int(parts[1])
    
    # "1.2.*" 匹配 1.2.0 - 1.2.x
    if parts[2] == "*":
        return v.major == int(parts[0]) and v.minor == int(parts[1])
    
    return False


def _satisfies_caret(v: SemanticVersion, base: str) -> bool:
    """
    插入号范围 ^
    ^1.2.3 := >=1.2.3 <2.0.0
    ^0.2.3 := >=0.2.3 <0.3.0
    ^0.0.3 := >=0.0.3 <0.0.4
    """
    base_v = parse(base)
    if v < base_v:
        return False
    
    if base_v.major != 0:
        # ^1.2.3 -> <2.0.0
        return v.major == base_v.major
    elif base_v.minor != 0:
        # ^0.2.3 -> <0.3.0
        return v.major == 0 and v.minor == base_v.minor
    else:
        # ^0.0.3 -> <0.0.4
        return v.major == 0 and v.minor == 0 and v.patch == base_v.patch


def _satisfies_tilde(v: SemanticVersion, base: str) -> bool:
    """
    波浪号范围 ~
    ~1.2.3 := >=1.2.3 <1.3.0
    """
    base_v = parse(base)
    if v < base_v:
        return False
    
    return v.major == base_v.major and v.minor == base_v.minor


def max_satisfying(versions: List[str], range_str: str) -> Optional[str]:
    """
    在版本列表中找到满足范围的最大版本
    
    参数:
        versions: 版本字符串列表
        range_str: 版本范围约束
    
    返回:
        满足范围的最大版本字符串，如果没有满足的则返回 None
    
    示例:
        >>> max_satisfying(["1.0.0", "1.2.3", "2.0.0"], "^1.0.0")
        '1.2.3'
    """
    satisfying_versions = [v for v in versions if satisfies(v, range_str)]
    if not satisfying_versions:
        return None
    
    # 排序并返回最大版本
    return max(satisfying_versions, key=lambda v: parse(v))


def min_satisfying(versions: List[str], range_str: str) -> Optional[str]:
    """
    在版本列表中找到满足范围的最小版本
    
    参数:
        versions: 版本字符串列表
        range_str: 版本范围约束
    
    返回:
        满足范围的最小版本字符串，如果没有满足的则返回 None
    
    示例:
        >>> min_satisfying(["1.0.0", "1.2.3", "2.0.0"], ">=1.1.0")
        '1.2.3'
    """
    satisfying_versions = [v for v in versions if satisfies(v, range_str)]
    if not satisfying_versions:
        return None
    
    return min(satisfying_versions, key=lambda v: parse(v))


def coerce(version_string: str) -> Optional[SemanticVersion]:
    """
    尝试将字符串强制转换为语义版本
    
    从可能不规范版本字符串中提取版本信息
    
    参数:
        version_string: 可能包含版本信息的字符串
    
    返回:
        SemanticVersion 对象，如果无法解析则返回 None
    
    示例:
        >>> coerce("v1.2.3")
        SemanticVersion(1.2.3)
        >>> coerce("version-2.0.0")
        SemanticVersion(2.0.0)
        >>> coerce("1.2")
        SemanticVersion(1.2.0)
    """
    # 移除常见前缀
    cleaned = re.sub(r'^(v|version|ver|release|r)[\s\-._]*', '', version_string, flags=re.IGNORECASE)
    cleaned = cleaned.strip()
    
    # 尝试直接解析
    try:
        return parse(cleaned)
    except ValueError:
        pass
    
    # 尝试提取版本号模式
    # 模式：major.minor.patch 或 major.minor
    patterns = [
        r'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:[-+]([^\s]*))?',
        r'(?P<major>\d+)\.(?P<minor>\d+)',
        r'(?P<major>\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, cleaned)
        if match:
            try:
                major = int(match.group('major'))
                minor = int(match.group('minor')) if 'minor' in match.groupdict() else 0
                patch = int(match.group('patch')) if 'patch' in match.groupdict() else 0
                
                return SemanticVersion(major, minor, patch)
            except (ValueError, IndexError):
                continue
    
    return None


def sort_versions(versions: List[str], reverse: bool = False) -> List[str]:
    """
    对版本列表排序
    
    参数:
        versions: 版本字符串列表
        reverse: 是否降序排序
    
    返回:
        排序后的版本列表
    
    示例:
        >>> sort_versions(["2.0.0", "1.0.0", "1.2.3"])
        ['1.0.0', '1.2.3', '2.0.0']
        >>> sort_versions(["2.0.0", "1.0.0", "1.2.3"], reverse=True)
        ['2.0.0', '1.2.3', '1.0.0']
    """
    return sorted(versions, key=lambda v: parse(v), reverse=reverse)


def get_change_type(from_version: str, to_version: str) -> str:
    """
    获取版本变更类型
    
    参数:
        from_version: 起始版本
        to_version: 目标版本
    
    返回:
        "major": 主版本变更
        "minor": 次版本变更
        "patch": 修订版本变更
        "prerelease": 预发布变更
        "none": 无变更
        "downgrade": 版本降级
    
    示例:
        >>> get_change_type("1.0.0", "2.0.0")
        'major'
        >>> get_change_type("2.0.0", "1.0.0")
        'downgrade'
    """
    v1, v2 = parse(from_version), parse(to_version)
    
    if v1 == v2:
        return "none"
    
    if v1 > v2:
        return "downgrade"
    
    if v1.major != v2.major:
        return "major"
    if v1.minor != v2.minor:
        return "minor"
    if v1.patch != v2.patch:
        return "patch"
    return "prerelease"


def create(major: int, minor: int, patch: int,
           prerelease: Optional[List[Union[str, int]]] = None,
           build_metadata: Optional[str] = None) -> SemanticVersion:
    """
    创建语义版本对象
    
    参数:
        major: 主版本号
        minor: 次版本号
        patch: 修订版本号
        prerelease: 预发布标识符列表
        build_metadata: 构建元数据
    
    返回:
        SemanticVersion 对象
    
    示例:
        >>> v = create(1, 2, 3)
        >>> str(v)
        '1.2.3'
        >>> v = create(1, 0, 0, ['alpha', 1])
        >>> str(v)
        '1.0.0-alpha.1'
    """
    return SemanticVersion(major, minor, patch, prerelease, build_metadata)


def validate(version_string: str) -> Tuple[bool, Optional[str]]:
    """
    验证语义版本并返回详细结果
    
    参数:
        version_string: 版本字符串
    
    返回:
        (是否有效, 错误信息或None)
    
    示例:
        >>> validate("1.2.3")
        (True, None)
        >>> validate("1.2")
        (False, "Invalid semantic version: missing patch version")
    """
    version_string = version_string.strip()
    
    if not version_string:
        return False, "Empty version string"
    
    # 检查基本格式
    parts = version_string.split('+')[0].split('-')[0].split('.')
    if len(parts) != 3:
        return False, "Semantic version must have exactly 3 parts (major.minor.patch)"
    
    # 检查每个部分是否为数字
    for i, part in enumerate(parts):
        names = ['major', 'minor', 'patch']
        if not part.isdigit():
            return False, f"Invalid {names[i]} version: {part}"
        
        # 检查前导零
        if len(part) > 1 and part[0] == '0':
            return False, f"{names[i].capitalize()} version cannot have leading zeros: {part}"
        
        value = int(part)
        if value < 0:
            return False, f"{names[i].capitalize()} version cannot be negative: {value}"
    
    # 使用正则表达式完整验证
    if not SEMVER_PATTERN.match(version_string):
        return False, f"Invalid semantic version format: {version_string}"
    
    try:
        parse(version_string)
        return True, None
    except ValueError as e:
        return False, str(e)


def next_version(version: str, release_type: str = "patch") -> str:
    """
    获取下一个版本号
    
    参数:
        version: 当前版本字符串
        release_type: 发布类型 ("major", "minor", "patch", "prerelease")
    
    返回:
        下一个版本字符串
    
    示例:
        >>> next_version("1.2.3", "major")
        '2.0.0'
        >>> next_version("1.2.3", "minor")
        '1.3.0'
        >>> next_version("1.2.3", "patch")
        '1.2.4'
    """
    if release_type == "major":
        return increment_major(version)
    elif release_type == "minor":
        return increment_minor(version)
    elif release_type == "patch":
        return increment_patch(version)
    elif release_type == "prerelease":
        return increment_prerelease(version)
    else:
        raise ValueError(f"Invalid release type: {release_type}")


if __name__ == "__main__":
    # 简单演示
    print("语义版本工具演示")
    print("=" * 50)
    
    # 解析版本
    v = parse("1.2.3-alpha.1+build.123")
    print(f"解析版本: {v}")
    print(f"  major: {v.major}")
    print(f"  minor: {v.minor}")
    print(f"  patch: {v.patch}")
    print(f"  prerelease: {v.prerelease}")
    print(f"  build_metadata: {v.build_metadata}")
    print(f"  is_prerelease: {v.is_prerelease()}")
    print(f"  is_stable: {v.is_stable()}")
    
    print()
    
    # 版本比较
    print("版本比较:")
    print(f"  compare('1.0.0', '2.0.0') = {compare('1.0.0', '2.0.0')}")
    print(f"  compare('2.0.0', '1.0.0') = {compare('2.0.0', '1.0.0')}")
    print(f"  gt('2.0.0', '1.0.0') = {gt('2.0.0', '1.0.0')}")
    
    print()
    
    # 版本递增
    print("版本递增:")
    print(f"  increment_major('1.2.3') = {increment_major('1.2.3')}")
    print(f"  increment_minor('1.2.3') = {increment_minor('1.2.3')}")
    print(f"  increment_patch('1.2.3') = {increment_patch('1.2.3')}")
    print(f"  increment_prerelease('1.2.3') = {increment_prerelease('1.2.3')}")
    
    print()
    
    # 版本范围
    print("版本范围:")
    print(f"  satisfies('1.2.3', '^1.0.0') = {satisfies('1.2.3', '^1.0.0')}")
    print(f"  satisfies('2.0.0', '^1.0.0') = {satisfies('2.0.0', '^1.0.0')}")
    print(f"  satisfies('1.2.5', '~1.2.0') = {satisfies('1.2.5', '~1.2.0')}")
    print(f"  satisfies('1.3.0', '~1.2.0') = {satisfies('1.3.0', '~1.2.0')}")
    
    print()
    
    # 版本排序
    versions = ["2.0.0", "1.0.0-alpha", "1.0.0", "1.2.3", "1.0.0-beta"]
    print(f"排序版本 {versions}:")
    print(f"  升序: {sort_versions(versions)}")
    print(f"  降序: {sort_versions(versions, reverse=True)}")