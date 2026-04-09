# -*- coding: utf-8 -*-
"""
AllToolkit - Regex Utilities 🔍

零依赖正则表达式工具库，提供常用模式、验证、提取、替换等功能。

Author: AllToolkit Team
License: MIT
Version: 1.0.0
"""

import re
from typing import List, Dict, Optional, Tuple, Union, Pattern, Any, Match
from functools import lru_cache


# =============================================================================
# 常用正则表达式模式
# =============================================================================

PATTERNS = {
    # 基础类型
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'url': r'^https?://(?:www\.)?(?:[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b|localhost|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)$',
    'ip_v4': r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
    'ip_v6': r'^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$',
    'domain': r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$',
    'hostname': r'^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$',
    
    # 电话号码
    'phone_cn': r'^1[3-9]\d{9}$',
    'phone_us': r'^\+?1?\s*\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$',
    'phone_intl': r'^\+[1-9]\d{6,14}$',
    
    # 日期时间
    'date_iso': r'^\d{4}-\d{2}-\d{2}$',
    'date_cn': r'^\d{4}年\d{1,2}月\d{1,2}日$',
    'datetime_iso': r'^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}$',
    'time_24h': r'^([01]?[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?$',
    'time_12h': r'^(0?[1-9]|1[0-2]):[0-5][0-9](:[0-5][0-9])?\s*[AaPp][Mm]$',
    
    # 身份标识
    'id_card_cn': r'^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$',
    'passport': r'^[A-Z]{1,2}\d{6,9}$',
    'license_plate_cn': r'^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z][A-Z0-9]{5}$',
    
    # 编码和哈希
    'hex_color': r'^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$',
    'base64': r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$',
    'uuid': r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$',
    'md5': r'^[a-fA-F0-9]{32}$',
    'sha1': r'^[a-fA-F0-9]{40}$',
    'sha256': r'^[a-fA-F0-9]{64}$',
    
    # 文件路径
    'file_path_unix': r'^(?:/[a-zA-Z0-9._-]+)+/?$',
    'file_path_win': r'^[a-zA-Z]:\\(?:[a-zA-Z0-9._-]+\\)*[a-zA-Z0-9._-]*$',
    'file_extension': r'\.[a-zA-Z0-9]+$',
    
    # 用户名和密码
    'username': r'^[a-zA-Z][a-zA-Z0-9_-]{2,19}$',
    'password_strong': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$',
    'password_medium': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$',
    
    # 数字和货币
    'integer': r'^-?\d+$',
    'positive_integer': r'^\d+$',
    'decimal': r'^-?\d+(\.\d+)?$',
    'currency': r'^\$?\d{1,3}(,\d{3})*(\.\d{2})?$',
    'percentage': r'^\d{1,2}(\.\d{1,2})?%$|^100%$',
    
    # 特殊用途
    'html_tag': r'<([a-z]+)([^<]+)*(?:>(.*)<\/\1>|\s+\/>)',
    'markdown_link': r'\[([^\]]+)\]\(([^)]+)\)',
    'mention': r'@(\w+)',
    'hashtag': r'#(\w+)',
    'emoji': r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]',
    
    # 空白和字符
    'whitespace': r'^\s*$',
    'alphanumeric': r'^[a-zA-Z0-9]+$',
    'alphanumeric_cn': r'^[a-zA-Z0-9\u4e00-\u9fa5]+$',
    'chinese': r'^[\u4e00-\u9fa5]+$',
    'ascii': r'^[\x00-\x7F]+$',
}


# =============================================================================
# 编译后的正则表达式缓存
# =============================================================================

@lru_cache(maxsize=256)
def _get_pattern(name: str) -> Pattern:
    """获取编译后的正则表达式模式"""
    if name not in PATTERNS:
        raise ValueError(f"未知模式：{name}")
    return re.compile(PATTERNS[name])


# =============================================================================
# 验证函数
# =============================================================================

def validate_email(email: str) -> bool:
    """验证邮箱地址格式"""
    return bool(re.match(PATTERNS['email'], email))


def validate_url(url: str) -> bool:
    """验证 URL 格式"""
    return bool(re.match(PATTERNS['url'], url))


def validate_phone(phone: str, region: str = 'cn') -> bool:
    """
    验证电话号码格式
    
    Args:
        phone: 电话号码
        region: 地区代码 ('cn', 'us', 'intl')
    
    Returns:
        是否有效
    """
    pattern_key = f'phone_{region}'
    if pattern_key not in PATTERNS:
        raise ValueError(f"不支持的地区：{region}")
    return bool(re.match(PATTERNS[pattern_key], phone))


def validate_date(date_str: str, format_type: str = 'iso') -> bool:
    """
    验证日期格式
    
    Args:
        date_str: 日期字符串
        format_type: 格式类型 ('iso', 'cn')
    
    Returns:
        是否有效
    """
    pattern_key = f'date_{format_type}'
    if pattern_key not in PATTERNS:
        raise ValueError(f"不支持的日期格式：{format_type}")
    return bool(re.match(PATTERNS[pattern_key], date_str))


def validate_id_card(id_card: str) -> bool:
    """验证中国身份证号码"""
    if not re.match(PATTERNS['id_card_cn'], id_card):
        return False
    
    # 验证校验码
    if len(id_card) == 18:
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        
        try:
            total = sum(int(id_card[i]) * weights[i] for i in range(17))
            check_code = check_codes[total % 11]
            return id_card[-1].upper() == check_code
        except (ValueError, IndexError):
            return False
    
    return True


def validate_password(password: str, strength: str = 'medium') -> bool:
    """
    验证密码强度
    
    Args:
        password: 密码字符串
        strength: 强度要求 ('strong', 'medium')
    
    Returns:
        是否符合要求
    """
    pattern_key = f'password_{strength}'
    if pattern_key not in PATTERNS:
        raise ValueError(f"不支持的强度级别：{strength}")
    return bool(re.match(PATTERNS[pattern_key], password))


def validate_hex_color(color: str) -> bool:
    """验证十六进制颜色代码"""
    return bool(re.match(PATTERNS['hex_color'], color))


def validate_uuid(uuid_str: str) -> bool:
    """验证 UUID 格式"""
    return bool(re.match(PATTERNS['uuid'], uuid_str))


def validate_username(username: str) -> bool:
    """验证用户名格式"""
    return bool(re.match(PATTERNS['username'], username))


def validate_ipv4(ip: str) -> bool:
    """验证 IPv4 地址"""
    return bool(re.match(PATTERNS['ip_v4'], ip))


def validate_ipv6(ip: str) -> bool:
    """验证 IPv6 地址"""
    return bool(re.match(PATTERNS['ip_v6'], ip))


def validate_domain(domain: str) -> bool:
    """验证域名格式"""
    return bool(re.match(PATTERNS['domain'], domain))


def validate_base64(data: str) -> bool:
    """验证 Base64 编码"""
    return bool(re.match(PATTERNS['base64'], data))


def validate_chinese(text: str) -> bool:
    """验证是否全为中文"""
    return bool(re.match(PATTERNS['chinese'], text))


def validate_alphanumeric(text: str, include_chinese: bool = False) -> bool:
    """
    验证是否为字母数字组合
    
    Args:
        text: 待验证文本
        include_chinese: 是否包含中文
    
    Returns:
        是否有效
    """
    pattern = PATTERNS['alphanumeric_cn'] if include_chinese else PATTERNS['alphanumeric']
    return bool(re.match(pattern, text))


# =============================================================================
# 提取函数
# =============================================================================

def extract_emails(text: str) -> List[str]:
    """从文本中提取所有邮箱地址"""
    pattern = PATTERNS['email'].replace('^', '').replace('$', '')
    return re.findall(pattern, text)


def extract_urls(text: str) -> List[str]:
    """从文本中提取所有 URL"""
    pattern = PATTERNS['url'].replace('^', '').replace('$', '')
    return re.findall(pattern, text)


def extract_phones(text: str, region: str = 'cn') -> List[str]:
    """从文本中提取所有电话号码"""
    pattern = PATTERNS[f'phone_{region}'].replace('^', '').replace('$', '')
    return re.findall(pattern, text)


def extract_dates(text: str, format_type: str = 'iso') -> List[str]:
    """从文本中提取所有日期"""
    pattern = PATTERNS[f'date_{format_type}'].replace('^', '').replace('$', '')
    return re.findall(pattern, text)


def extract_hashtags(text: str) -> List[str]:
    """从文本中提取所有话题标签"""
    return re.findall(PATTERNS['hashtag'], text)


def extract_mentions(text: str) -> List[str]:
    """从文本中提取所有@提及"""
    return re.findall(PATTERNS['mention'], text)


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    """
    从 Markdown 文本中提取链接
    
    Returns:
        列表，每项为 (链接文本，URL) 元组
    """
    return re.findall(PATTERNS['markdown_link'], text)


def extract_html_tags(text: str) -> List[Dict[str, str]]:
    """
    从 HTML 文本中提取标签信息
    
    Returns:
        列表，每项为包含 tag_name, attributes, content 的字典
    """
    results = []
    for match in re.finditer(PATTERNS['html_tag'], text, re.DOTALL):
        results.append({
            'tag_name': match.group(1),
            'attributes': match.group(2) or '',
            'content': match.group(3) or ''
        })
    return results


def extract_numbers(text: str, as_float: bool = False) -> List[Union[int, float]]:
    """
    从文本中提取数字
    
    Args:
        text: 输入文本
        as_float: 是否转换为浮点数
    
    Returns:
        数字列表
    """
    pattern = r'-?\d+(?:\.\d+)?' if as_float else r'-?\d+'
    matches = re.findall(pattern, text)
    return [float(m) if as_float else int(m) for m in matches]


def extract_between(text: str, start: str, end: str, include_markers: bool = False) -> List[str]:
    """
    提取两个标记之间的内容
    
    Args:
        text: 输入文本
        start: 起始标记
        end: 结束标记
        include_markers: 是否包含标记本身
    
    Returns:
        匹配内容列表
    """
    if include_markers:
        pattern = f'{re.escape(start)}.*?{re.escape(end)}'
    else:
        pattern = f'{re.escape(start)}(.*?){re.escape(end)}'
    
    matches = re.findall(pattern, text, re.DOTALL)
    if include_markers:
        return matches
    return [m if isinstance(m, str) else m[0] for m in matches]


# =============================================================================
# 替换函数
# =============================================================================

def remove_html_tags(html: str, keep_content: bool = True) -> str:
    """
    移除 HTML 标签
    
    Args:
        html: HTML 文本
        keep_content: 是否保留标签内容
    
    Returns:
        处理后的文本
    """
    if keep_content:
        return re.sub(r'<[^>]+>', '', html)
    return re.sub(r'<[^>]*>.*?</[^>]*>', '', html, flags=re.DOTALL)


def remove_mentions(text: str) -> str:
    """移除文本中的@提及"""
    return re.sub(PATTERNS['mention'], '', text)


def remove_hashtags(text: str) -> str:
    """移除文本中的话题标签"""
    return re.sub(PATTERNS['hashtag'], '', text)


def remove_extra_whitespace(text: str) -> str:
    """移除多余空白字符"""
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()


def normalize_whitespace(text: str) -> str:
    """标准化空白字符（将所有空白转为单个空格）"""
    return re.sub(r'\s+', ' ', text).strip()


def replace_urls(text: str, replacement: str = '[LINK]') -> str:
    """替换文本中的 URL"""
    pattern = PATTERNS['url'].replace('^', '').replace('$', '')
    return re.sub(pattern, replacement, text)


def replace_emails(text: str, replacement: str = '[EMAIL]') -> str:
    """替换文本中的邮箱地址"""
    pattern = PATTERNS['email'].replace('^', '').replace('$', '')
    return re.sub(pattern, replacement, text)


def replace_phones(text: str, replacement: str = '[PHONE]', region: str = 'cn') -> str:
    """替换文本中的电话号码"""
    pattern = PATTERNS[f'phone_{region}'].replace('^', '').replace('$', '')
    return re.sub(pattern, replacement, text)


def censor_text(text: str, pattern: str, replacement: str = '*') -> str:
    """
    根据模式屏蔽文本
    
    Args:
        text: 输入文本
        pattern: 匹配模式
        replacement: 替换字符
    
    Returns:
        屏蔽后的文本
    """
    def replace_match(match):
        matched = match.group(0)
        if len(matched) <= 2:
            return replacement * len(matched)
        return matched[0] + replacement * (len(matched) - 2) + matched[-1]
    
    return re.sub(pattern, replace_match, text)


def censor_phone(phone: str) -> str:
    """
    屏蔽电话号码中间数字
    
    Args:
        phone: 电话号码
    
    Returns:
        屏蔽后的号码（如：138****1234）
    """
    if len(phone) >= 7:
        return phone[:3] + '*' * 4 + phone[-4:]
    return phone


def censor_id_card(id_card: str) -> str:
    """
    屏蔽身份证号码
    
    Args:
        id_card: 身份证号码
    
    Returns:
        屏蔽后的号码（如：110101********1234）
    """
    if len(id_card) == 18:
        return id_card[:6] + '*' * 8 + id_card[-4:]
    return id_card


# =============================================================================
# 匹配和搜索函数
# =============================================================================

def find_all_matches(text: str, pattern: str, flags: int = 0) -> List[str]:
    """
    查找所有匹配项
    
    Args:
        text: 输入文本
        pattern: 正则表达式
        flags: 正则标志
    
    Returns:
        匹配结果列表
    """
    return re.findall(pattern, text, flags)


def find_first_match(text: str, pattern: str, flags: int = 0) -> Optional[str]:
    """
    查找第一个匹配项
    
    Args:
        text: 输入文本
        pattern: 正则表达式
        flags: 正则标志
    
    Returns:
        第一个匹配结果，无匹配返回 None
    """
    match = re.search(pattern, text, flags)
    return match.group(0) if match else None


def contains_pattern(text: str, pattern: str, flags: int = 0) -> bool:
    """
    检查文本是否包含匹配模式
    
    Args:
        text: 输入文本
        pattern: 正则表达式
        flags: 正则标志
    
    Returns:
        是否匹配
    """
    return bool(re.search(pattern, text, flags))


def match_groups(text: str, pattern: str, flags: int = 0) -> Optional[Tuple[str, ...]]:
    """
    获取匹配分组
    
    Args:
        text: 输入文本
        pattern: 正则表达式（应包含分组）
        flags: 正则标志
    
    Returns:
        分组元组，无匹配返回 None
    """
    match = re.search(pattern, text, flags)
    return match.groups() if match else None


def match_named_groups(text: str, pattern: str, flags: int = 0) -> Optional[Dict[str, str]]:
    """
    获取命名分组匹配
    
    Args:
        text: 输入文本
        pattern: 正则表达式（应包含命名分组）
        flags: 正则标志
    
    Returns:
        命名分组字典，无匹配返回 None
    """
    match = re.search(pattern, text, flags)
    return match.groupdict() if match else None


def split_by_pattern(text: str, pattern: str, maxsplit: int = 0) -> List[str]:
    """
    按模式分割文本
    
    Args:
        text: 输入文本
        pattern: 分割模式
        maxsplit: 最大分割次数（0 表示不限制）
    
    Returns:
        分割后的列表
    """
    return re.split(pattern, text, maxsplit)


# =============================================================================
# 实用工具函数
# =============================================================================

def escape_pattern(text: str) -> str:
    """转义正则表达式特殊字符"""
    return re.escape(text)


def compile_pattern(pattern: str, flags: int = 0) -> Pattern:
    """
    编译正则表达式
    
    Args:
        pattern: 正则表达式字符串
        flags: 正则标志
    
    Returns:
        编译后的 Pattern 对象
    """
    return re.compile(pattern, flags)


def get_pattern_names() -> List[str]:
    """获取所有预定义模式名称"""
    return list(PATTERNS.keys())


def get_pattern(pattern_name: str) -> str:
    """
    获取预定义的正则表达式模式
    
    Args:
        pattern_name: 模式名称
    
    Returns:
        正则表达式字符串
    """
    if pattern_name not in PATTERNS:
        raise ValueError(f"未知模式：{pattern_name}")
    return PATTERNS[pattern_name]


def test_pattern(pattern: str, test_strings: List[str], flags: int = 0) -> Dict[str, bool]:
    """
    测试正则表达式对多个字符串的匹配结果
    
    Args:
        pattern: 正则表达式
        test_strings: 测试字符串列表
    
    Returns:
        字典，键为测试字符串，值为是否匹配
    """
    compiled = re.compile(pattern, flags)
    return {s: bool(compiled.match(s)) for s in test_strings}


def pattern_info(pattern_name: str) -> Dict[str, Any]:
    """
    获取预定义模式的详细信息
    
    Args:
        pattern_name: 模式名称
    
    Returns:
        包含 pattern, description, examples 的字典
    """
    info = {
        'email': {'description': '邮箱地址', 'examples': ['test@example.com', 'user.name+tag@domain.co.uk']},
        'url': {'description': 'HTTP/HTTPS URL', 'examples': ['https://example.com', 'http://www.test.org/path']},
        'ip_v4': {'description': 'IPv4 地址', 'examples': ['192.168.1.1', '10.0.0.255']},
        'ip_v6': {'description': 'IPv6 地址', 'examples': ['2001:0db8:85a3:0000:0000:8a2e:0370:7334']},
        'domain': {'description': '域名', 'examples': ['example.com', 'sub.domain.co.uk']},
        'phone_cn': {'description': '中国大陆手机号', 'examples': ['13800138000', '19912345678']},
        'phone_us': {'description': '美国电话号码', 'examples': ['(555) 123-4567', '+1 555-123-4567']},
        'date_iso': {'description': 'ISO 日期格式', 'examples': ['2024-01-15', '2023-12-31']},
        'date_cn': {'description': '中文日期格式', 'examples': ['2024 年 1 月 15 日']},
        'datetime_iso': {'description': 'ISO 日期时间', 'examples': ['2024-01-15T10:30:00', '2024-01-15 10:30:00']},
        'id_card_cn': {'description': '中国身份证号码', 'examples': ['110101199001011234']},
        'hex_color': {'description': '十六进制颜色', 'examples': ['#FF5733', '#abc']},
        'uuid': {'description': 'UUID', 'examples': ['550e8400-e29b-41d4-a716-446655440000']},
        'username': {'description': '用户名', 'examples': ['john_doe', 'user-123']},
        'password_strong': {'description': '强密码（大小写 + 数字 + 特殊字符）', 'examples': ['Pass@123']},
        'chinese': {'description': '纯中文', 'examples': ['你好世界']},
        'alphanumeric': {'description': '字母数字', 'examples': ['abc123']},
    }
    
    if pattern_name not in PATTERNS:
        raise ValueError(f"未知模式：{pattern_name}")
    
    result = {
        'name': pattern_name,
        'pattern': PATTERNS[pattern_name],
    }
    
    if pattern_name in info:
        result.update(info[pattern_name])
    
    return result


# =============================================================================
# 高级功能
# =============================================================================

class RegexMatcher:
    """正则表达式匹配器类，提供更丰富的匹配功能"""
    
    def __init__(self, pattern: str, flags: int = 0):
        self.pattern = pattern
        self.flags = flags
        self.compiled = re.compile(pattern, flags)
    
    def match(self, text: str) -> Optional[Match]:
        """从字符串开头匹配"""
        return self.compiled.match(text)
    
    def search(self, text: str) -> Optional[Match]:
        """在字符串中搜索"""
        return self.compiled.search(text)
    
    def findall(self, text: str) -> List[str]:
        """查找所有匹配"""
        return self.compiled.findall(text)
    
    def finditer(self, text: str) -> List[Match]:
        """查找所有匹配（返回 Match 对象）"""
        return list(self.compiled.finditer(text))
    
    def split(self, text: str, maxsplit: int = 0) -> List[str]:
        """分割字符串"""
        return self.compiled.split(text, maxsplit)
    
    def sub(self, text: str, repl: str, count: int = 0) -> str:
        """替换匹配"""
        return self.compiled.sub(repl, text, count)
    
    def subn(self, text: str, repl: str, count: int = 0) -> Tuple[str, int]:
        """替换匹配并返回替换次数"""
        return self.compiled.subn(repl, text, count)
    
    def fullmatch(self, text: str) -> Optional[Match]:
        """完全匹配"""
        return self.compiled.fullmatch(text)


class TextCleaner:
    """文本清洗器，提供常用的文本清洗功能"""
    
    def __init__(self):
        self.text = ""
    
    def load(self, text: str) -> 'TextCleaner':
        """加载文本"""
        self.text = text
        return self
    
    def remove_html(self, keep_content: bool = True) -> 'TextCleaner':
        """移除 HTML 标签"""
        self.text = remove_html_tags(self.text, keep_content)
        return self
    
    def remove_mentions(self) -> 'TextCleaner':
        """移除@提及"""
        self.text = remove_mentions(self.text)
        return self
    
    def remove_hashtags(self) -> 'TextCleaner':
        """移除话题标签"""
        self.text = remove_hashtags(self.text)
        return self
    
    def normalize_whitespace(self) -> 'TextCleaner':
        """标准化空白"""
        self.text = normalize_whitespace(self.text)
        return self
    
    def remove_extra_whitespace(self) -> 'TextCleaner':
        """移除多余空白"""
        self.text = remove_extra_whitespace(self.text)
        return self
    
    def replace_urls(self, replacement: str = '[LINK]') -> 'TextCleaner':
        """替换 URL"""
        self.text = replace_urls(self.text, replacement)
        return self
    
    def replace_emails(self, replacement: str = '[EMAIL]') -> 'TextCleaner':
        """替换邮箱"""
        self.text = replace_emails(self.text, replacement)
        return self
    
    def censor_phones(self) -> 'TextCleaner':
        """屏蔽电话号码"""
        self.text = replace_phones(self.text, '[PHONE]')
        return self
    
    def get(self) -> str:
        """获取处理后的文本"""
        return self.text
    
    def reset(self) -> 'TextCleaner':
        """重置文本"""
        self.text = ""
        return self


# =============================================================================
# 批量处理函数
# =============================================================================

def batch_validate(items: List[str], validator_func) -> Dict[str, bool]:
    """
    批量验证
    
    Args:
        items: 待验证项目列表
        validator_func: 验证函数
    
    Returns:
        字典，键为项目，值为验证结果
    """
    return {item: validator_func(item) for item in items}


def batch_extract(texts: List[str], extractor_func) -> Dict[str, List]:
    """
    批量提取
    
    Args:
        texts: 文本列表
        extractor_func: 提取函数
    
    Returns:
        字典，键为原文本，值为提取结果列表
    """
    return {text: extractor_func(text) for text in texts}


def filter_by_pattern(items: List[str], pattern: str, keep_matching: bool = True) -> List[str]:
    """
    按模式过滤列表
    
    Args:
        items: 字符串列表
        pattern: 正则表达式
        keep_matching: True 保留匹配项，False 保留不匹配项
    
    Returns:
        过滤后的列表
    """
    compiled = re.compile(pattern)
    if keep_matching:
        return [item for item in items if compiled.search(item)]
    return [item for item in items if not compiled.search(item)]


def group_by_pattern(items: List[str], pattern: str) -> Dict[bool, List[str]]:
    """
    按模式分组
    
    Args:
        items: 字符串列表
        pattern: 正则表达式
    
    Returns:
        字典，True 为匹配组，False 为不匹配组
    """
    compiled = re.compile(pattern)
    groups = {True: [], False: []}
    for item in items:
        key = bool(compiled.search(item))
        groups[key].append(item)
    return groups


# =============================================================================
# 导出所有公共 API
# =============================================================================

__all__ = [
    # 常量
    'PATTERNS',
    
    # 验证函数
    'validate_email', 'validate_url', 'validate_phone', 'validate_date',
    'validate_id_card', 'validate_password', 'validate_hex_color',
    'validate_uuid', 'validate_username', 'validate_ipv4', 'validate_ipv6',
    'validate_domain', 'validate_base64', 'validate_chinese',
    'validate_alphanumeric',
    
    # 提取函数
    'extract_emails', 'extract_urls', 'extract_phones', 'extract_dates',
    'extract_hashtags', 'extract_mentions', 'extract_markdown_links',
    'extract_html_tags', 'extract_numbers', 'extract_between',
    
    # 替换函数
    'remove_html_tags', 'remove_mentions', 'remove_hashtags',
    'remove_extra_whitespace', 'normalize_whitespace', 'replace_urls',
    'replace_emails', 'replace_phones', 'censor_text', 'censor_phone',
    'censor_id_card',
    
    # 匹配和搜索
    'find_all_matches', 'find_first_match', 'contains_pattern',
    'match_groups', 'match_named_groups', 'split_by_pattern',
    
    # 工具函数
    'escape_pattern', 'compile_pattern', 'get_pattern_names',
    'get_pattern', 'test_pattern', 'pattern_info',
    
    # 类
    'RegexMatcher', 'TextCleaner',
    
    # 批量处理
    'batch_validate', 'batch_extract', 'filter_by_pattern', 'group_by_pattern',
]
