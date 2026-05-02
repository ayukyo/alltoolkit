"""
AllToolkit - Python License Plate Utilities

中国车牌号工具模块，支持车牌验证、生成、解析等功能。
零依赖，仅使用 Python 标准库。

@author AllToolkit
@version 1.0.0
"""

import random
import re
from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict


# ============================================================================
# 数据定义
# ============================================================================

# 省份简称映射
PROVINCE_MAP: Dict[str, str] = {
    '京': '北京市',
    '津': '天津市',
    '沪': '上海市',
    '渝': '重庆市',
    '冀': '河北省',
    '晋': '山西省',
    '蒙': '内蒙古自治区',
    '辽': '辽宁省',
    '吉': '吉林省',
    '黑': '黑龙江省',
    '苏': '江苏省',
    '浙': '浙江省',
    '皖': '安徽省',
    '闽': '福建省',
    '赣': '江西省',
    '鲁': '山东省',
    '豫': '河南省',
    '鄂': '湖北省',
    '湘': '湖南省',
    '粤': '广东省',
    '桂': '广西壮族自治区',
    '琼': '海南省',
    '川': '四川省',
    '贵': '贵州省',
    '云': '云南省',
    '藏': '西藏自治区',
    '陕': '陕西省',
    '甘': '甘肃省',
    '青': '青海省',
    '宁': '宁夏回族自治区',
    '新': '新疆维吾尔自治区',
    '港': '香港特别行政区',
    '澳': '澳门特别行政区',
    '台': '台湾省',
}

# 省份简称列表
PROVINCES: List[str] = list(PROVINCE_MAP.keys())

# 字母表（不含 I 和 O，避免与数字混淆）
VALID_LETTERS: str = 'ABCDEFGHJKLMNPQRSTUVWXYZ'

# 字母映射到数字（用于编码计算）
LETTER_TO_NUMBER: Dict[str, int] = {
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14,
    'F': 15, 'G': 16, 'H': 17, 'J': 18, 'K': 19,
    'L': 20, 'M': 21, 'N': 22, 'P': 23, 'Q': 24,
    'R': 25, 'S': 26, 'T': 27, 'U': 28, 'V': 29,
    'W': 30, 'X': 31, 'Y': 32, 'Z': 33,
}

# 特殊车牌类型
SPECIAL_TYPES: Dict[str, str] = {
    '警': '警用车辆',
    '学': '教练车辆',
    '使': '使馆车辆',
    '领': '领馆车辆',
    '港': '香港入境车辆',
    '澳': '澳门入境车辆',
    '临': '临时车牌',
    '挂': '挂车',
    '电': '电动车辆',
    'F': '非纯电动车',
    'D': '纯电动车',
}

# ============================================================================
# 数据类定义
# ============================================================================

@dataclass
class LicensePlate:
    """车牌信息类"""
    province: str           # 省份简称
    province_name: str      # 省份名称
    city_code: str          # 城市/地区代码
    number: str             # 号码部分
    special_type: Optional[str] = None  # 特殊类型（警、学等）
    full_plate: str = ''    # 完整车牌号
    
    def __post_init__(self):
        if self.special_type:
            self.full_plate = f"{self.province}{self.city_code}{self.number}{self.special_type}"
        else:
            self.full_plate = f"{self.province}{self.city_code}{self.number}"
    
    def is_special(self) -> bool:
        """是否为特殊车牌"""
        return self.special_type is not None
    
    def get_type_description(self) -> str:
        """获取类型描述"""
        if self.special_type:
            return SPECIAL_TYPES.get(self.special_type, '未知类型')
        return '普通车牌'
    
    def __str__(self) -> str:
        return self.full_plate
    
    def __repr__(self) -> str:
        return f"LicensePlate('{self.full_plate}', province='{self.province_name}', type='{self.get_type_description()}')"


# ============================================================================
# 验证函数
# ============================================================================

def validate(plate: str) -> bool:
    """
    验证车牌号是否有效
    
    Args:
        plate: 车牌号字符串
        
    Returns:
        bool: 是否有效
    """
    return parse(plate) is not None


def parse(plate: str) -> Optional[LicensePlate]:
    """
    解析车牌号，返回详细信息
    
    Args:
        plate: 车牌号字符串
        
    Returns:
        LicensePlate: 车牌信息对象，无效时返回 None
    """
    if not plate:
        return None
    
    # 清理输入 - 移除空格、点号等分隔符
    plate = plate.strip().upper()
    plate = re.sub(r'[·\.\s\-_]', '', plate)
    
    # 标准车牌格式：省份简称 + 字母 + 5位字母/数字
    # 特殊车牌可能有后缀（警、学等）
    # 新能源车牌：省份 + 字母 + D/F + 4位字母/数字
    
    # 先尝试新能源车牌格式
    ev_pattern = r'^([京津冀沪渝晋蒙辽吉黑苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云藏陕甘青宁新港澳台台])([A-Z])([DF])([A-HJ-NP-Z0-9]{4})$'
    ev_match = re.match(ev_pattern, plate)
    if ev_match:
        province, city_code, ev_type, number = ev_match.groups()
        if province in PROVINCE_MAP:
            return LicensePlate(
                province=province,
                province_name=PROVINCE_MAP[province],
                city_code=city_code,
                number=ev_type + number,
                special_type=ev_type,  # D 或 F 作为特殊类型
            )
    
    # 标准车牌格式
    pattern = r'^([京津冀沪渝晋蒙辽吉黑苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云藏陕甘青宁新港澳台台])([A-Z])([A-HJ-NP-Z0-9]{4,5})([警学使领港澳临挂电DF]?)$'
    
    match = re.match(pattern, plate)
    if not match:
        return None
    
    province, city_code, number, special = match.groups()
    
    # 验证省份简称
    if province not in PROVINCE_MAP:
        return None
    
    # 验证城市代码（不能包含 I 和 O）
    if city_code in ('I', 'O'):
        return None
    
    # 验证号码部分不包含 I 和 O
    if 'I' in number or 'O' in number:
        return None
    
    return LicensePlate(
        province=province,
        province_name=PROVINCE_MAP[province],
        city_code=city_code,
        number=number,
        special_type=special if special else None
    )


def validate_format(plate: str) -> Tuple[bool, str]:
    """
    验证车牌格式并返回详细错误信息
    
    Args:
        plate: 车牌号字符串
        
    Returns:
        Tuple[bool, str]: (是否有效, 错误信息或成功消息)
    """
    if not plate:
        return (False, "车牌号为空")
    
    plate = plate.strip().upper()
    
    if len(plate) < 7:
        return (False, "车牌号长度不足，标准车牌至少7位")
    
    if len(plate) > 8:
        return (False, "车牌号长度超出，标准车牌最多8位")
    
    # 检查省份简称
    province = plate[0]
    if province not in PROVINCE_MAP:
        return (False, f"无效的省份简称: '{province}'")
    
    # 检查城市代码
    city_code = plate[1]
    if city_code not in VALID_LETTERS and city_code not in '0123456789':
        return (False, f"无效的城市代码: '{city_code}'，不能使用 I 或 O")
    
    # 检查号码部分
    number_part = plate[2:7]
    for char in number_part:
        if char in ('I', 'O'):
            return (False, f"号码部分包含无效字符: '{char}'，不能使用 I 或 O")
        if char not in VALID_LETTERS and char not in '0123456789':
            return (False, f"号码部分包含无效字符: '{char}'")
    
    # 检查特殊类型标识（如果有）
    if len(plate) == 8:
        special = plate[7]
        if special not in SPECIAL_TYPES:
            return (False, f"无效的特殊类型标识: '{special}'")
    
    return (True, "车牌格式有效")


# ============================================================================
# 生成函数
# ============================================================================

def generate(province: Optional[str] = None, 
             city_code: Optional[str] = None,
             special_type: Optional[str] = None) -> str:
    """
    生成随机车牌号
    
    Args:
        province: 省份简称，随机生成时为 None
        city_code: 城市代码，随机生成时为 None
        special_type: 特殊类型标识（警、学等）
        
    Returns:
        str: 生成的车牌号
    """
    # 选择省份
    if province and province in PROVINCES:
        selected_province = province
    else:
        selected_province = random.choice(PROVINCES)
    
    # 选择城市代码
    if city_code and city_code in VALID_LETTERS:
        selected_city = city_code
    else:
        selected_city = random.choice(VALID_LETTERS)
    
    # 生成号码部分（5位）
    chars = VALID_LETTERS + '0123456789'
    number = ''.join(random.choice(chars) for _ in range(5))
    
    # 添加特殊类型标识
    suffix = ''
    if special_type and special_type in SPECIAL_TYPES:
        suffix = special_type
    
    return f"{selected_province}{selected_city}{number}{suffix}"


def generate_batch(count: int, 
                   province: Optional[str] = None,
                   city_code: Optional[str] = None,
                   special_type: Optional[str] = None) -> List[str]:
    """
    批量生成车牌号
    
    Args:
        count: 生成数量
        province: 省份简称
        city_code: 城市代码
        special_type: 特殊类型
        
    Returns:
        List[str]: 车牌号列表
    """
    return [generate(province, city_code, special_type) for _ in range(count)]


def generate_nice_number(province: Optional[str] = None,
                         city_code: Optional[str] = None,
                         pattern: str = 'sequential') -> str:
    """
    生成靓号车牌（连号、重复号等）
    
    Args:
        province: 省份简称
        city_code: 城市代码
        pattern: 号码模式 ('sequential' 连号, 'repeat' 重复号, 'palindrome' 回文)
        
    Returns:
        str: 靓号车牌
    """
    # 选择省份和城市
    if province and province in PROVINCES:
        selected_province = province
    else:
        selected_province = random.choice(PROVINCES)
    
    if city_code and city_code in VALID_LETTERS:
        selected_city = city_code
    else:
        selected_city = random.choice(VALID_LETTERS)
    
    # 根据模式生成号码
    if pattern == 'sequential':
        # 连号：如 12345, 56789
        start = random.randint(1, 5)
        number = ''.join(str(start + i) for i in range(5))
    elif pattern == 'repeat':
        # 重复号：如 88888, 66666
        digit = random.choice('0123456789')
        number = digit * 5
    elif pattern == 'palindrome':
        # 回文号：如 12321, 56665
        prefix = ''.join(random.choice('0123456789') for _ in range(2))
        middle = random.choice('0123456789')
        number = prefix + middle + prefix[::-1]
    elif pattern == 'mixed_repeat':
        # 混合重复：如 AA888, BB123
        letters = random.choice(VALID_LETTERS) * 2
        digits = ''.join(random.choice('0123456789') for _ in range(3))
        number = letters + digits
    else:
        number = ''.join(random.choice('0123456789') for _ in range(5))
    
    return f"{selected_province}{selected_city}{number}"


# ============================================================================
# 解析与分析函数
# ============================================================================

def get_province(plate: str) -> Optional[str]:
    """
    获取车牌所属省份名称
    
    Args:
        plate: 轳牌号
        
    Returns:
        str: 省份名称，无效车牌返回 None
    """
    info = parse(plate)
    return info.province_name if info else None


def get_province_short(plate: str) -> Optional[str]:
    """
    获取车牌省份简称
    
    Args:
        plate: 轳牌号
        
    Returns:
        str: 省份简称，无效车牌返回 None
    """
    info = parse(plate)
    return info.province if info else None


def get_city_code(plate: str) -> Optional[str]:
    """
    获取车牌城市代码
    
    Args:
        plate: 轳牌号
        
    Returns:
        str: 城市代码，无效车牌返回 None
    """
    info = parse(plate)
    return info.city_code if info else None


def get_number(plate: str) -> Optional[str]:
    """
    获取车牌号码部分
    
    Args:
        plate: 轳牌号
        
    Returns:
        str: 号码部分，无效车牌返回 None
    """
    info = parse(plate)
    return info.number if info else None


def get_type(plate: str) -> Optional[str]:
    """
    获取车牌类型描述
    
    Args:
        plate: 轳牌号
        
    Returns:
        str: 类型描述，无效车牌返回 None
    """
    info = parse(plate)
    return info.get_type_description() if info else None


def is_special(plate: str) -> bool:
    """
    判断是否为特殊车牌
    
    Args:
        plate: 轳牌号
        
    Returns:
        bool: 是否为特殊车牌
    """
    info = parse(plate)
    return info.is_special() if info else False


def is_police(plate: str) -> bool:
    """是否为警用车牌"""
    info = parse(plate)
    return info.special_type == '警' if info else False


def is_learner(plate: str) -> bool:
    """是否为教练车车牌"""
    info = parse(plate)
    return info.special_type == '学' if info else False


def is_embassy(plate: str) -> bool:
    """是否为使馆车车牌"""
    info = parse(plate)
    return info.special_type in ('使', '领') if info else False


def is_temporary(plate: str) -> bool:
    """是否为临时车牌"""
    info = parse(plate)
    return info.special_type == '临' if info else False


def is_electric(plate: str) -> bool:
    """是否为电动车车牌"""
    info = parse(plate)
    return info.special_type in ('电', 'D', 'F') if info else False


# ============================================================================
# 编码计算（用于车牌识别算法）
# ============================================================================

def encode_number(plate: str) -> Optional[int]:
    """
    将车牌号码部分编码为数值（用于算法计算）
    
    编码规则：
    - 数字直接使用其值（0-9）
    - 字母使用映射值（A=10, B=11, ..., Z=33）
    - 按位加权计算
    
    Args:
        plate: 轳牌号
        
    Returns:
        int: 编码值，无效车牌返回 None
    """
    info = parse(plate)
    if not info:
        return None
    
    result = 0
    for char in info.number:
        if char.isdigit():
            value = int(char)
        elif char in LETTER_TO_NUMBER:
            value = LETTER_TO_NUMBER[char]
        else:
            return None
        result = result * 34 + value
    
    return result


def decode_number(code: int, length: int = 5) -> str:
    """
    将编码值解码为车牌号码
    
    Args:
        code: 编码值
        length: 号码长度
        
    Returns:
        str: 解码后的号码
    """
    chars = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'
    result = []
    
    temp = code
    while temp > 0 and len(result) < length:
        result.append(chars[temp % 34])
        temp //= 34
    
    # 补齐长度
    while len(result) < length:
        result.append('0')
    
    return ''.join(reversed(result))


# ============================================================================
# 车牌比较与匹配
# ============================================================================

def compare(plate1: str, plate2: str) -> Tuple[bool, str]:
    """
    比较两个车牌（忽略大小写和空格）
    
    Args:
        plate1: 第一个车牌
        plate2: 第二个车牌
        
    Returns:
        Tuple[bool, str]: (是否相同, 差异描述)
    """
    p1 = plate1.strip().upper()
    p2 = plate2.strip().upper()
    
    if p1 == p2:
        return (True, "完全相同")
    
    # 分析差异
    if len(p1) != len(p2):
        return (False, f"长度不同: {len(p1)} vs {len(p2)}")
    
    diffs = []
    for i, (c1, c2) in enumerate(zip(p1, p2)):
        if c1 != c2:
            diffs.append(f"位置{i}: '{c1}' vs '{c2}'")
    
    return (False, ", ".join(diffs))


def match_pattern(plate: str, pattern: str) -> bool:
    """
    检查车牌是否匹配指定模式
    
    模式语法：
    - ? 匹配任意单个字符
    - * 匹配任意多个字符
    - [ABC] 匹配 A、B 或 C
    - [!ABC] 不匹配 A、B 或 C
    
    Args:
        plate: 轳牌号
        pattern: 匹配模式
        
    Returns:
        bool: 是否匹配
    """
    plate = plate.strip().upper()
    pattern = pattern.strip().upper()
    
    # 转换为正则表达式
    regex_pattern = ''
    i = 0
    while i < len(pattern):
        c = pattern[i]
        if c == '?':
            # ? 匹配任意单个字符（包括中文）
            regex_pattern += '.'
        elif c == '*':
            # * 匹配任意多个字符（包括中文）
            regex_pattern += '.*'
        elif c == '[':
            # 处理字符集（支持中文）
            j = i + 1
            if j < len(pattern) and pattern[j] == '!':
                regex_pattern += '[^'
                j += 1
            else:
                regex_pattern += '['
            
            while j < len(pattern) and pattern[j] != ']':
                regex_pattern += pattern[j]
                j += 1
            regex_pattern += ']'
            i = j
        else:
            regex_pattern += re.escape(c)
        i += 1
    
    try:
        # 允许匹配中文字符
        regex_pattern = '^' + regex_pattern + '$'
        return bool(re.match(regex_pattern, plate))
    except re.error:
        return False


# ============================================================================
# 统计函数
# ============================================================================

def analyze_batch(plates: List[str]) -> Dict[str, any]:
    """
    批量分析车牌
    
    Args:
        plates: 轳牌号列表
        
    Returns:
        Dict: 分析结果统计
    """
    valid_count = 0
    invalid_count = 0
    province_stats: Dict[str, int] = {}
    special_stats: Dict[str, int] = {}
    
    for plate in plates:
        info = parse(plate)
        if info:
            valid_count += 1
            province_stats[info.province] = province_stats.get(info.province, 0) + 1
            if info.special_type:
                special_stats[info.special_type] = special_stats.get(info.special_type, 0) + 1
        else:
            invalid_count += 1
    
    return {
        'total': len(plates),
        'valid': valid_count,
        'invalid': invalid_count,
        'valid_rate': valid_count / len(plates) if plates else 0,
        'province_distribution': province_stats,
        'special_type_distribution': special_stats,
    }


# ============================================================================
# 格式化函数
# ============================================================================

def format_plate(plate: str, separator: str = '') -> str:
    """
    格式化车牌输出
    
    Args:
        plate: 轳牌号
        separator: 分隔符（如空格或点）
        
    Returns:
        str: 格式化后的车牌
    """
    info = parse(plate)
    if not info:
        return plate
    
    if separator:
        return f"{info.province}{separator}{info.city_code}{separator}{info.number}{separator}{info.special_type or ''}".rstrip(separator)
    return info.full_plate


def format_with_province(plate: str) -> str:
    """
    格式化车牌并显示省份名称
    
    Args:
        plate: 轳牌号
        
    Returns:
        str: 格式化字符串
    """
    info = parse(plate)
    if not info:
        return f"{plate} (无效)"
    return f"{info.full_plate} ({info.province_name})"


# ============================================================================
# 辅助函数
# ============================================================================

def list_provinces() -> List[str]:
    """列出所有省份简称"""
    return PROVINCES.copy()


def list_province_names() -> Dict[str, str]:
    """列出省份简称与名称映射"""
    return PROVINCE_MAP.copy()


def list_special_types() -> Dict[str, str]:
    """列出所有特殊车牌类型"""
    return SPECIAL_TYPES.copy()


def is_valid_char(char: str) -> bool:
    """检查字符是否可用于车牌"""
    char = char.upper()
    return char in VALID_LETTERS or char in '0123456789'


def get_char_type(char: str) -> str:
    """获取字符类型（数字/字母/无效）"""
    char = char.upper()
    if char.isdigit():
        return 'digit'
    elif char in VALID_LETTERS:
        return 'letter'
    else:
        return 'invalid'


# ============================================================================
# 类定义：车牌集合
# ============================================================================

class LicensePlateSet:
    """车牌集合管理类"""
    
    def __init__(self, plates: Optional[List[str]] = None):
        self._plates: Dict[str, LicensePlate] = {}
        if plates:
            for plate in plates:
                self.add(plate)
    
    def add(self, plate: str) -> bool:
        """添加车牌"""
        info = parse(plate)
        if info:
            self._plates[info.full_plate] = info
            return True
        return False
    
    def remove(self, plate: str) -> bool:
        """移除车牌"""
        plate = plate.strip().upper()
        return self._plates.pop(plate, None) is not None
    
    def contains(self, plate: str) -> bool:
        """检查是否包含车牌"""
        plate = plate.strip().upper()
        return plate in self._plates
    
    def get(self, plate: str) -> Optional[LicensePlate]:
        """获取车牌信息"""
        plate = plate.strip().upper()
        return self._plates.get(plate)
    
    def list_all(self) -> List[str]:
        """列出所有车牌"""
        return list(self._plates.keys())
    
    def filter_by_province(self, province: str) -> List[str]:
        """按省份筛选"""
        province = province.strip()
        return [p for p, info in self._plates.items() if info.province == province]
    
    def filter_by_special_type(self, special_type: str) -> List[str]:
        """按特殊类型筛选"""
        return [p for p, info in self._plates.items() if info.special_type == special_type]
    
    def count(self) -> int:
        """获取数量"""
        return len(self._plates)
    
    def clear(self) -> None:
        """清空集合"""
        self._plates.clear()
    
    def analyze(self) -> Dict[str, any]:
        """分析集合"""
        return analyze_batch(self.list_all())
    
    def __len__(self) -> int:
        return len(self._plates)
    
    def __contains__(self, plate: str) -> bool:
        return self.contains(plate)
    
    def __iter__(self):
        return iter(self._plates.values())
    
    def __str__(self) -> str:
        return f"LicensePlateSet({len(self._plates)} plates)"


# ============================================================================
# 模块信息
# ============================================================================

__all__ = [
    # 数据类
    'LicensePlate',
    'LicensePlateSet',
    
    # 验证函数
    'validate',
    'parse',
    'validate_format',
    
    # 生成函数
    'generate',
    'generate_batch',
    'generate_nice_number',
    
    # 解析函数
    'get_province',
    'get_province_short',
    'get_city_code',
    'get_number',
    'get_type',
    
    # 类型判断
    'is_special',
    'is_police',
    'is_learner',
    'is_embassy',
    'is_temporary',
    'is_electric',
    
    # 编码函数
    'encode_number',
    'decode_number',
    
    # 比较函数
    'compare',
    'match_pattern',
    
    # 统计函数
    'analyze_batch',
    
    # 格式化函数
    'format_plate',
    'format_with_province',
    
    # 辅助函数
    'list_provinces',
    'list_province_names',
    'list_special_types',
    'is_valid_char',
    'get_char_type',
    
    # 常量
    'PROVINCES',
    'PROVINCE_MAP',
    'VALID_LETTERS',
    'SPECIAL_TYPES',
]

__version__ = '1.0.0'
__author__ = 'AllToolkit'