"""
Postal Code Utilities - 邮政编码工具

支持多国邮政编码验证、格式化、提取和生成。
零外部依赖，仅使用 Python 标准库。

支持的国家/地区：
- 中国 (CN): 6位数字
- 美国 (US): ZIP (5位) 或 ZIP+4 (5-4位)
- 日本 (JP): 〒NNN-NNNN 格式
- 英国 (UK): 复杂格式 (如 SW1A 1AA)
- 加拿大 (CA): ANA NAN 格式
- 澳大利亚 (AU): 4位数字
- 德国 (DE): 5位数字
- 法国 (FR): 5位数字
- 韩国 (KR): 5位数字
- 印度 (IN): 6位数字
- 巴西 (BR): NNNNN-NNN 格式
- 俄罗斯 (RU): 6位数字
- 墨西哥 (MX): 5位数字
- 意大利 (IT): 5位数字
- 西班牙 (ES): 5位数字
- 荷兰 (NL): NNNN XX 格式
- 瑞典 (SE): NNN NN 格式
- 波兰 (PL): NN-NNN 格式
- 台湾 (TW): 3+2位数字
- 香港 (HK): 无标准邮编
- 新加坡 (SG): 6位数字

作者: AllToolkit
日期: 2026-05-09
"""

import re
from typing import Optional, Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class CountryCode(Enum):
    """国家/地区代码枚举"""
    CN = "CN"  # 中国
    US = "US"  # 美国
    JP = "JP"  # 日本
    UK = "UK"  # 英国
    CA = "CA"  # 加拿大
    AU = "AU"  # 澳大利亚
    DE = "DE"  # 德国
    FR = "FR"  # 法国
    KR = "KR"  # 韩国
    IN = "IN"  # 印度
    BR = "BR"  # 巴西
    RU = "RU"  # 俄罗斯
    MX = "MX"  # 墨西哥
    IT = "IT"  # 意大利
    ES = "ES"  # 西班牙
    NL = "NL"  # 荷兰
    SE = "SE"  # 瑞典
    PL = "PL"  # 波兰
    TW = "TW"  # 台湾
    HK = "HK"  # 香港
    SG = "SG"  # 新加坡


@dataclass
class PostalCodeInfo:
    """邮政编码信息"""
    code: str  # 格式化后的邮编
    country: str  # 国家代码
    is_valid: bool  # 是否有效
    normalized: str  # 标准化格式（无空格、连字符）
    region: Optional[str] = None  # 地区/省份（如果可识别）
    format_type: Optional[str] = None  # 格式类型（如 ZIP, ZIP+4 等）
    raw_input: Optional[str] = None  # 原始输入


def _format_uk_postal_code(code: str) -> str:
    """
    格式化英国邮编，保留标准空格格式
    
    英国邮编格式示例：
    - SW1A 1AA (伦敦)
    - M1 1AA (曼彻斯特)
    - B33 8TH (伯明翰)
    
    格式规则：
    - 外码部分：1-4个字符（字母+数字混合）
    - 内码部分：3个字符（数字+2字母）
    - 空格分隔外码和内码
    """
    if not code:
        return code
    
    # 转大写并去除多余空格
    code = code.upper().strip()
    
    # 已经有空格，保持原样
    if " " in code:
        return code
    
    # 无空格，需要根据长度插入空格
    # 规则：外码长度为2-4，内码长度为3
    # 总长度为5-7
    length = len(code)
    
    if length == 5:  # 如 A9A9A -> A9 A9A
        return f"{code[:2]} {code[2:]}"
    elif length == 6:  # 如 A99A9A -> A99 A9A
        return f"{code[:3]} {code[3:]}"
    elif length == 7:  # 如 AA99A9A -> AA99 A9A
        return f"{code[:4]} {code[4:]}"
    
    return code


# 国家邮政编码规则定义
# 格式: (正则模式, 格式化函数, 说明)
POSTAL_CODE_RULES: Dict[str, Dict[str, Any]] = {
    "CN": {
        "name": "中国",
        "patterns": [
            (r"^\d{6}$", "standard", "标准6位数字"),
        ],
        "format": lambda c: c,
        "normalize": lambda c: c,
        "region_prefix": {
            "10": "北京", "11": "北京", "12": "北京", "13": "北京", "20": "上海",
            "21": "上海", "30": "天津", "31": "天津", "40": "重庆", "41": "重庆",
            "01": "北京", "02": "上海", "03": "天津", "04": "重庆",
            "05": "河北", "06": "河北", "07": "河北",
            "08": "内蒙古", "09": "内蒙古",
            "10-19": "北京", "20-29": "上海", "30-39": "天津", "40-49": "重庆",
            "50-59": "辽宁", "60-69": "吉林", "70-79": "黑龙江",
            "80-89": "江苏", "90-99": "江苏",
        }
    },
    "US": {
        "name": "美国",
        "patterns": [
            (r"^\d{5}-\d{4}$", "zip_plus_4", "ZIP+4格式"),
            (r"^\d{9}$", "zip_plus_4_compact", "ZIP+4紧凑格式"),
            (r"^\d{5}$", "zip", "标准ZIP格式"),
        ],
        "format": lambda c: f"{c[:5]}-{c[5:]}" if len(c) == 9 else c,
        "normalize": lambda c: c.replace("-", ""),
        "region_prefix": {
            "0": "东北部", "1": "东北部", "2": "中大西洋",
            "3": "东南部", "4": "东南部", "5": "中西部",
            "6": "西南部", "7": "西南部", "8": "西部", "9": "西部",
        }
    },
    "JP": {
        "name": "日本",
        "patterns": [
            (r"^〒?\d{3}-?\d{4}$", "standard", "〒NNN-NNNN格式"),
        ],
        "format": lambda c: f"〒{c[:3]}-{c[3:]}" if len(c) == 7 and c.isdigit() else c,
        "normalize": lambda c: c.replace("〒", "").replace("-", ""),
    },
    "UK": {
        "name": "英国",
        "patterns": [
            # 英国邮编格式复杂，有多种模式
            (r"^[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}$", "standard", "英国标准格式"),
        ],
        "format": lambda c: _format_uk_postal_code(c),
        "normalize": lambda c: c.replace(" ", "").upper(),
        # 英国邮编第一位字母代表地区
        "region_prefix": {
            "A": "英格兰中部", "B": "伯明翰", "C": "剑桥/康沃尔", "D": "德文",
            "E": "伦敦东部/埃塞克斯", "F": "法夫", "G": "格拉斯哥/格洛斯特",
            "H": "赫特福德/汉普郡", "I": "不使用", "J": "不使用", "K": "肯特",
            "L": "利物浦", "M": "曼彻斯特", "N": "伦敦北部", "O": "牛津",
            "P": "珀斯/朴茨茅斯", "Q": "不使用", "R": "雷丁/兰开夏",
            "S": "谢菲尔德/南安普顿", "T": "特伦特", "U": "不使用",
            "V": "不使用", "W": "伦敦西部", "X": "不使用", "Y": "约克",
            "Z": "不使用",
        }
    },
    "CA": {
        "name": "加拿大",
        "patterns": [
            # 加拿大邮编第一位字母不包含 D, F, I, O, Q, U, W, X, Z（避免混淆）
            (r"^[ABCEGHJKLMNPRSTVY]\d[ABCEGHJKLMNPRSTVY]\s*\d[ABCEGHJKLMNPRSTVY]\d$", "standard", "ANA NAN格式"),
        ],
        "format": lambda c: f"{c[:3]} {c[3:]}" if len(c) == 6 else c,
        "normalize": lambda c: c.replace(" ", "").upper(),
        # 加拿大邮编第一位字母代表省份/地区
        "region_prefix": {
            "A": "纽芬兰与拉布拉多", "B": "新斯科舍", "C": "爱德华王子岛",
            "E": "新不伦瑞克", "G": "魁北克东部", "H": "蒙特利尔", "J": "魁北克西部",
            "K": "安大略东部", "L": "安大略中部", "M": "多伦多", "N": "安大略西南部",
            "P": "安大略北部", "R": "马尼托巴", "S": "萨斯喀彻温", "T": "阿尔伯塔",
            "V": "不列颠哥伦比亚", "X": "西北地区/努纳武特", "Y": "育空",
        }
    },
    "AU": {
        "name": "澳大利亚",
        "patterns": [
            (r"^\d{4}$", "standard", "4位数字格式"),
        ],
        "format": lambda c: c,
        "normalize": lambda c: c,
        "region_prefix": {
            "0": "北领地", "2": "新南威尔士/澳大利亚首都领地",
            "3": "维多利亚", "4": "昆士兰", "5": "南澳大利亚",
            "6": "西澳大利亚", "7": "塔斯马尼亚",
        }
    },
    "DE": {
        "name": "德国",
        "patterns": [
            (r"^\d{5}$", "standard", "5位数字格式"),
        ],
        "format": lambda c: c,
        "normalize": lambda c: c,
        "region_prefix": {
            "0": "萨克森/萨克森-安哈特/图林根",
            "1": "柏林/勃兰登堡",
            "2": "汉堡/石勒苏益格-荷尔斯泰因/梅克伦堡-前波美拉尼亚",
            "3": "下萨克森/不来梅",
            "4": "北莱茵-威斯特法伦",
            "5": "北莱茵-威斯特法伦",
            "6": "黑森/莱茵兰-普法尔茨/萨尔",
            "7": "巴登-符腾堡",
            "8": "巴伐利亚",
            "9": "巴伐利亚",
        }
    },
    "FR": {
        "name": "法国",
        "patterns": [
            (r"^\d{5}$", "standard", "5位数字格式"),
        ],
        "format": lambda c: c,
        "normalize": lambda c: c,
        "region_prefix": {
            "75": "巴黎", "13": "马赛", "69": "里昂", "31": "图卢兹",
            "33": "波尔多", "59": "里尔", "44": "南特", "34": "蒙彼利埃",
            "67": "斯特拉斯堡", "06": "尼斯",
        }
    },
    "KR": {
        "name": "韩国",
        "patterns": [
            (r"^\d{5}$", "standard", "5位数字格式"),
            (r"^\d{3}-\d{3}$", "old_format", "旧6位格式"),
        ],
        "format": lambda c: c if len(c) == 5 else c,
        "normalize": lambda c: c.replace("-", ""),
    },
    "IN": {
        "name": "印度",
        "patterns": [
            (r"^\d{6}$", "standard", "6位数字格式(PIN)"),
        ],
        "format": lambda c: c,
        "normalize": lambda c: c,
    },
    "BR": {
        "name": "巴西",
        "patterns": [
            (r"^\d{5}-?\d{3}$", "standard", "CEP格式"),
        ],
        "format": lambda c: f"{c[:5]}-{c[5:]}" if len(c) == 8 else c,
        "normalize": lambda c: c.replace("-", ""),
    },
    "RU": {
        "name": "俄罗斯",
        "patterns": [
            (r"^\d{6}$", "standard", "6位数字格式"),
        ],
        "format": lambda c: c,
        "normalize": lambda c: c,
    },
    "MX": {
        "name": "墨西哥",
        "patterns": [
            (r"^\d{5}$", "standard", "5位数字格式"),
        ],
        "format": lambda c: c,
        "normalize": lambda c: c,
    },
    "IT": {
        "name": "意大利",
        "patterns": [
            (r"^\d{5}$", "standard", "CAP格式"),
        ],
        "format": lambda c: c,
        "normalize": lambda c: c,
    },
    "ES": {
        "name": "西班牙",
        "patterns": [
            (r"^\d{5}$", "standard", "5位数字格式"),
        ],
        "format": lambda c: c,
        "normalize": lambda c: c,
    },
    "NL": {
        "name": "荷兰",
        "patterns": [
            (r"^\d{4}\s*[A-Z]{2}$", "standard", "NNNN XX格式"),
        ],
        "format": lambda c: f"{c[:4]} {c[4:].strip()}" if len(c) >= 6 else c,
        "normalize": lambda c: c.replace(" ", "").upper(),
    },
    "SE": {
        "name": "瑞典",
        "patterns": [
            (r"^\d{3}\s*\d{2}$", "standard", "NNN NN格式"),
        ],
        "format": lambda c: f"{c[:3]} {c[3:]}" if len(c) == 5 else c,
        "normalize": lambda c: c.replace(" ", ""),
    },
    "PL": {
        "name": "波兰",
        "patterns": [
            (r"^\d{2}-\d{3}$", "standard", "NN-NNN格式"),
        ],
        "format": lambda c: c if "-" in c else f"{c[:2]}-{c[2:]}",
        "normalize": lambda c: c.replace("-", ""),
    },
    "TW": {
        "name": "台湾",
        "patterns": [
            (r"^\d{3}(?:\d{2})?$", "standard", "3位或5位数字格式"),
        ],
        "format": lambda c: c,
        "normalize": lambda c: c,
        "region_prefix": {
            "1": "台北市", "2": "高雄市", "3": "台中市", "4": "台南市",
            "5": "桃园市", "6": "新北市", "7": "基隆市", "8": "新竹市",
        }
    },
    "HK": {
        "name": "香港",
        "patterns": [],  # 香港无标准邮政编码系统
        "format": lambda c: c,
        "normalize": lambda c: c,
    },
    "SG": {
        "name": "新加坡",
        "patterns": [
            (r"^\d{6}$", "standard", "6位数字格式"),
        ],
        "format": lambda c: f"Singapore {c}",
        "normalize": lambda c: c,
    },
}


def validate_postal_code(postal_code: str, country: str) -> bool:
    """
    验证邮政编码是否有效
    
    Args:
        postal_code: 邮政编码
        country: 国家代码 (如 "CN", "US", "JP" 等)
    
    Returns:
        bool: 是否有效
    
    Examples:
        >>> validate_postal_code("100001", "CN")
        True
        >>> validate_postal_code("12345", "US")
        True
        >>> validate_postal_code("12345-6789", "US")
        True
        >>> validate_postal_code("SW1A 1AA", "UK")
        True
        >>> validate_postal_code("K1A 0B1", "CA")
        True
    """
    if not postal_code or not country:
        return False
    
    country = country.upper()
    if country not in POSTAL_CODE_RULES:
        return False
    
    rules = POSTAL_CODE_RULES[country]
    
    # 特殊处理：香港无标准邮编
    if country == "HK":
        return False  # 或返回 True，取决于业务需求
    
    # 标准化邮编
    normalized = rules["normalize"](postal_code.strip())
    
    # 检查模式
    for pattern, _, _ in rules["patterns"]:
        if re.match(pattern, postal_code.strip().upper(), re.IGNORECASE):
            return True
    
    # 尝试标准化后匹配
    for pattern, _, _ in rules["patterns"]:
        if re.match(pattern, normalized, re.IGNORECASE):
            return True
    
    return False


def format_postal_code(postal_code: str, country: str) -> str:
    """
    格式化邮政编码
    
    Args:
        postal_code: 邮政编码
        country: 国家代码
    
    Returns:
        str: 格式化后的邮政编码
    
    Examples:
        >>> format_postal_code("100001", "CN")
        '100001'
        >>> format_postal_code("123456789", "US")
        '12345-6789'
        >>> format_postal_code("1000001", "JP")
        '〒100-0001'
        >>> format_postal_code("K1A0B1", "CA")
        'K1A 0B1'
    """
    if not postal_code or not country:
        return postal_code or ""
    
    country = country.upper()
    if country not in POSTAL_CODE_RULES:
        return postal_code.strip()
    
    rules = POSTAL_CODE_RULES[country]
    normalized = rules["normalize"](postal_code.strip())
    
    return rules["format"](normalized)


def normalize_postal_code(postal_code: str, country: str) -> str:
    """
    标准化邮政编码（去除空格、连字符等）
    
    Args:
        postal_code: 邮政编码
        country: 国家代码
    
    Returns:
        str: 标准化后的邮政编码
    
    Examples:
        >>> normalize_postal_code("12345-6789", "US")
        '123456789'
        >>> normalize_postal_code("K1A 0B1", "CA")
        'K1A0B1'
        >>> normalize_postal_code("〒100-0001", "JP")
        '1000001'
    """
    if not postal_code or not country:
        return postal_code or ""
    
    country = country.upper()
    if country not in POSTAL_CODE_RULES:
        # 默认去除空格和连字符
        return re.sub(r'[\s\-]', '', postal_code)
    
    rules = POSTAL_CODE_RULES[country]
    return rules["normalize"](postal_code.strip())


def get_postal_code_info(postal_code: str, country: str) -> PostalCodeInfo:
    """
    获取邮政编码详细信息
    
    Args:
        postal_code: 邮政编码
        country: 国家代码
    
    Returns:
        PostalCodeInfo: 邮编详细信息
    
    Examples:
        >>> info = get_postal_code_info("100001", "CN")
        >>> info.is_valid
        True
        >>> info.region
        '北京'
        >>> info.format_type
        'standard'
    """
    # 保存原始输入
    raw_input = postal_code if postal_code else ""
    
    postal_code = postal_code.strip() if postal_code else ""
    country = country.upper() if country else ""
    
    if not postal_code or not country or country not in POSTAL_CODE_RULES:
        return PostalCodeInfo(
            code=postal_code,
            country=country,
            is_valid=False,
            normalized=postal_code,
            raw_input=raw_input
        )
    
    rules = POSTAL_CODE_RULES[country]
    normalized = rules["normalize"](postal_code)
    is_valid = validate_postal_code(postal_code, country)
    formatted = format_postal_code(postal_code, country)
    
    # 确定格式类型
    format_type = None
    for pattern, fmt_type, _ in rules["patterns"]:
        if re.match(pattern, postal_code.strip().upper(), re.IGNORECASE):
            format_type = fmt_type
            break
    
    # 尝试识别地区
    region = None
    if "region_prefix" in rules:
        region_prefix = rules["region_prefix"]
        for prefix, region_name in region_prefix.items():
            if normalized.startswith(prefix):
                region = region_name
                break
    
    return PostalCodeInfo(
        code=formatted,
        country=country,
        is_valid=is_valid,
        normalized=normalized,
        region=region,
        format_type=format_type,
        raw_input=raw_input
    )


def extract_postal_codes(text: str, country: Optional[str] = None) -> List[Tuple[str, str]]:
    """
    从文本中提取邮政编码
    
    Args:
        text: 输入文本
        country: 指定国家代码，如果为None则尝试所有国家
    
    Returns:
        List[Tuple[str, str]]: [(邮编, 国家代码), ...]
    
    Examples:
        >>> extract_postal_codes("Send to 100001, Beijing", "CN")
        [('100001', 'CN')]
        >>> extract_postal_codes("ZIP: 12345 or 90210-1234", "US")
        [('12345', 'US'), ('90210-1234', 'US')]
        >>> extract_postal_codes("Address: SW1A 1AA, London", "UK")
        [('SW1A 1AA', 'UK')]
    """
    results = []
    
    if country:
        # 指定国家
        country = country.upper()
        if country in POSTAL_CODE_RULES:
            rules = POSTAL_CODE_RULES[country]
            for pattern, _, _ in rules["patterns"]:
                # 去除锚点，使能在文本中匹配
                extract_pattern = pattern.replace("^", "").replace("$", "")
                matches = re.findall(extract_pattern, text, re.IGNORECASE)
                for match in matches:
                    results.append((match, country))
    else:
        # 尝试所有国家
        for country_code, rules in POSTAL_CODE_RULES.items():
            for pattern, _, _ in rules["patterns"]:
                # 去除锚点，使能在文本中匹配
                extract_pattern = pattern.replace("^", "").replace("$", "")
                matches = re.findall(extract_pattern, text, re.IGNORECASE)
                for match in matches:
                    # 验证匹配
                    if validate_postal_code(match, country_code):
                        results.append((match, country_code))
    
    return results


def detect_country(postal_code: str) -> List[str]:
    """
    根据邮政编码检测可能的国家
    
    Args:
        postal_code: 邮政编码
    
    Returns:
        List[str]: 可能的国家代码列表
    
    Examples:
        >>> detect_country("100001")
        ['CN', 'RU', 'IN']
        >>> detect_country("12345")
        ['US', 'DE', 'FR', 'KR', 'MX', 'IT', 'ES']
        >>> detect_country("K1A 0B1")
        ['CA']
        >>> detect_country("SW1A 1AA")
        ['UK']
    """
    postal_code = postal_code.strip() if postal_code else ""
    if not postal_code:
        return []
    
    possible_countries = []
    
    for country_code, rules in POSTAL_CODE_RULES.items():
        for pattern, _, _ in rules["patterns"]:
            if re.match(pattern, postal_code, re.IGNORECASE):
                possible_countries.append(country_code)
                break
    
    return possible_countries


def is_valid_postal_code_format(text: str) -> Tuple[bool, List[str]]:
    """
    检查文本是否为有效的邮政编码格式
    
    Args:
        text: 输入文本
    
    Returns:
        Tuple[bool, List[str]]: (是否为有效格式, 可能的国家列表)
    
    Examples:
        >>> is_valid_postal_code_format("100001")
        (True, ['CN', 'RU', 'IN'])
        >>> is_valid_postal_code_format("K1A 0B1")
        (True, ['CA'])
        >>> is_valid_postal_code_format("hello")
        (False, [])
    """
    countries = detect_country(text)
    return len(countries) > 0, countries


def get_country_postal_code_info(country: str) -> Dict[str, Any]:
    """
    获取国家邮政编码规则信息
    
    Args:
        country: 国家代码
    
    Returns:
        Dict: 国家邮编规则信息
    
    Examples:
        >>> info = get_country_postal_code_info("US")
        >>> info['name']
        '美国'
        >>> len(info['patterns']) > 0
        True
    """
    country = country.upper() if country else ""
    if country not in POSTAL_CODE_RULES:
        return {}
    
    rules = POSTAL_CODE_RULES[country]
    return {
        "name": rules["name"],
        "country_code": country,
        "patterns": [(p, t, d) for p, t, d in rules["patterns"]],
        "example_codes": _generate_example_codes(country, rules)
    }


def _generate_example_codes(country: str, rules: Dict) -> List[str]:
    """生成示例邮政编码"""
    examples = {
        "CN": ["100001", "200001", "510000"],
        "US": ["12345", "90210", "12345-6789"],
        "JP": ["100-0001", "150-0001", "〒100-0001"],
        "UK": ["SW1A 1AA", "M1 1AA", "B33 8TH"],
        "CA": ["K1A 0B1", "V6B 1A1", "T2P 1J9"],
        "AU": ["2000", "3000", "4000"],
        "DE": ["10115", "80331", "50667"],
        "FR": ["75001", "13001", "69001"],
        "KR": ["04524", "06000"],
        "IN": ["110001", "400001", "700001"],
        "BR": ["01311-000", "22041-080"],
        "RU": ["101000", "190000", "620000"],
        "MX": ["06600", "11560", "03900"],
        "IT": ["00100", "20100", "50100"],
        "ES": ["28001", "08001", "46001"],
        "NL": ["1011 AB", "1071 CD"],
        "SE": ["111 22", "123 45"],
        "PL": ["00-001", "30-001", "50-001"],
        "TW": ["100", "106", "404"],
        "HK": [],
        "SG": ["018956", "238858", "179103"],
    }
    return examples.get(country, [])


def compare_postal_codes(code1: str, code2: str, country: str) -> int:
    """
    比较两个邮政编码的大小（按标准化后字典序）
    
    Args:
        code1: 第一个邮编
        code2: 第二个邮编
        country: 国家代码
    
    Returns:
        int: -1, 0, 1 分别表示小于、等于、大于
    
    Examples:
        >>> compare_postal_codes("100001", "100002", "CN")
        -1
        >>> compare_postal_codes("12345", "12345", "US")
        0
    """
    if country not in POSTAL_CODE_RULES:
        # 默认字符串比较
        return -1 if code1 < code2 else (1 if code1 > code2 else 0)
    
    rules = POSTAL_CODE_RULES[country]
    norm1 = rules["normalize"](code1)
    norm2 = rules["normalize"](code2)
    
    return -1 if norm1 < norm2 else (1 if norm1 > norm2 else 0)


def get_nearby_postal_codes(postal_code: str, country: str, range_delta: int = 10) -> List[str]:
    """
    获取附近邮政编码（仅适用于数字型邮编）
    
    Args:
        postal_code: 邮政编码
        country: 国家代码
        range_delta: 范围偏移量
    
    Returns:
        List[str]: 附近邮编列表
    
    Examples:
        >>> get_nearby_postal_codes("100001", "CN", 2)
        ['099999', '100000', '100001', '100002', '100003']
    """
    if country not in POSTAL_CODE_RULES:
        return []
    
    rules = POSTAL_CODE_RULES[country]
    normalized = rules["normalize"](postal_code)
    
    # 仅适用于纯数字邮编
    if not normalized.isdigit():
        return [postal_code]
    
    try:
        code_num = int(normalized)
        nearby = []
        for delta in range(-range_delta, range_delta + 1):
            new_code = str(code_num + delta).zfill(len(normalized))
            nearby.append(format_postal_code(new_code, country))
        return nearby
    except ValueError:
        return [postal_code]


def batch_validate(postal_codes: List[Tuple[str, str]]) -> Dict[str, List[PostalCodeInfo]]:
    """
    批量验证邮政编码
    
    Args:
        postal_codes: [(邮编, 国家代码), ...]
    
    Returns:
        Dict: {"valid": [...], "invalid": [...]}
    
    Examples:
        >>> result = batch_validate([("100001", "CN"), ("invalid", "CN"), ("12345", "US")])
        >>> len(result["valid"])
        2
        >>> len(result["invalid"])
        1
    """
    valid = []
    invalid = []
    
    for postal_code, country in postal_codes:
        info = get_postal_code_info(postal_code, country)
        if info.is_valid:
            valid.append(info)
        else:
            invalid.append(info)
    
    return {"valid": valid, "invalid": invalid}


def generate_random_postal_code(country: str) -> Optional[str]:
    """
    生成随机邮政编码（用于测试）
    
    Args:
        country: 国家代码
    
    Returns:
        Optional[str]: 随机邮编，如果不支持则返回None
    
    Examples:
        >>> code = generate_random_postal_code("CN")
        >>> len(code) == 6 and code.isdigit()
        True
        >>> code = generate_random_postal_code("US")
        >>> len(code) == 5 or len(code) == 10  # ZIP or ZIP+4
        True
    """
    import random
    
    country = country.upper() if country else ""
    if country not in POSTAL_CODE_RULES:
        return None
    
    rules = POSTAL_CODE_RULES[country]
    
    if country == "CN":
        return str(random.randint(100000, 999999))
    elif country == "US":
        if random.random() > 0.5:
            return f"{random.randint(10000, 99999)}"
        else:
            return f"{random.randint(10000, 99999)}-{random.randint(1000, 9999)}"
    elif country == "JP":
        return f"〒{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    elif country == "UK":
        # 简化的英国邮编生成
        districts = ["SW", "NW", "SE", "NE", "W", "WC", "EC", "E", "N", "S"]
        return f"{random.choice(districts)}{random.randint(1, 99)} {random.randint(1, 9)}{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}"
    elif country == "CA":
        # 加拿大邮编不使用 D, F, I, O, Q, U, W, X, Z
        letters = "ABCEGHJKLMNPRSTVY"
        return f"{random.choice(letters)}{random.randint(0, 9)}{random.choice(letters)} {random.randint(0, 9)}{random.choice(letters)}{random.randint(0, 9)}"
    elif country == "AU":
        return f"{random.randint(1000, 9999)}"
    elif country in ["DE", "FR", "KR", "MX", "IT", "ES"]:
        return f"{random.randint(10000, 99999)}"
    elif country == "IN":
        return f"{random.randint(100000, 999999)}"
    elif country == "BR":
        return f"{random.randint(10000, 99999)}-{random.randint(100, 999)}"
    elif country == "RU":
        return f"{random.randint(100000, 999999)}"
    elif country == "NL":
        letters = "ABCDEFGHJKLMNPRSTUVWXYZ"
        return f"{random.randint(1000, 9999)} {random.choice(letters)}{random.choice(letters)}"
    elif country == "SE":
        return f"{random.randint(100, 999)} {random.randint(10, 99)}"
    elif country == "PL":
        return f"{random.randint(10, 99)}-{random.randint(100, 999)}"
    elif country == "TW":
        return f"{random.randint(100, 999)}"
    elif country == "SG":
        return f"{random.randint(100000, 999999)}"
    
    return None


def get_supported_countries() -> List[Dict[str, str]]:
    """
    获取支持的国家列表
    
    Returns:
        List[Dict]: [{"code": "CN", "name": "中国"}, ...]
    
    Examples:
        >>> countries = get_supported_countries()
        >>> len(countries) > 0
        True
        >>> {"code": "CN", "name": "中国"} in countries
        True
    """
    return [
        {"code": code, "name": rules["name"]}
        for code, rules in POSTAL_CODE_RULES.items()
    ]


# 便捷函数别名
validate = validate_postal_code
format = format_postal_code
normalize = normalize_postal_code
info = get_postal_code_info
extract = extract_postal_codes
detect = detect_country


if __name__ == "__main__":
    # 示例用法
    print("=== 邮政编码工具示例 ===\n")
    
    # 验证示例
    test_cases = [
        ("100001", "CN"),
        ("12345", "US"),
        ("12345-6789", "US"),
        ("100-0001", "JP"),
        ("SW1A 1AA", "UK"),
        ("K1A 0B1", "CA"),
        ("2000", "AU"),
        ("10115", "DE"),
        ("75001", "FR"),
    ]
    
    print("1. 验证邮政编码:")
    for code, country in test_cases:
        is_valid = validate_postal_code(code, country)
        formatted = format_postal_code(code, country)
        print(f"   {country}: {code} -> 有效: {is_valid}, 格式化: {formatted}")
    
    print("\n2. 获取详细信息:")
    info = get_postal_code_info("100001", "CN")
    print(f"   CN 100001: {info}")
    
    print("\n3. 从文本提取:")
    text = "请寄往北京市 100001 或上海 200001"
    codes = extract_postal_codes(text, "CN")
    print(f"   文本: {text}")
    print(f"   提取: {codes}")
    
    print("\n4. 自动检测国家:")
    for test_code in ["100001", "K1A 0B1", "SW1A 1AA", "12345"]:
        countries = detect_country(test_code)
        print(f"   {test_code} -> 可能的国家: {countries}")
    
    print("\n5. 批量验证:")
    batch = [("100001", "CN"), ("invalid", "CN"), ("12345", "US")]
    result = batch_validate(batch)
    print(f"   有效: {len(result['valid'])}, 无效: {len(result['invalid'])}")
    
    print("\n6. 随机生成:")
    for country in ["CN", "US", "JP", "UK", "CA"]:
        random_code = generate_random_postal_code(country)
        print(f"   {country}: {random_code}")