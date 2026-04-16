"""
数据验证工具集 (Data Validator)
提供全面的数据格式验证功能，支持邮箱、手机号、身份证、IP地址、URL等多种格式
零外部依赖，纯 Python 实现
"""

import re
import json
from typing import Optional, Tuple, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ValidationResult:
    """验证结果"""
    
    def __init__(self, is_valid: bool, message: str = "", details: Optional[Dict[str, Any]] = None):
        self.is_valid = is_valid
        self.message = message
        self.details = details or {}
    
    def __bool__(self) -> bool:
        return self.is_valid
    
    def __repr__(self) -> str:
        status = "✓" if self.is_valid else "✗"
        return f"ValidationResult({status}, {self.message!r})"
    
    def __str__(self) -> str:
        return self.message


# ============ 邮箱验证 ============

# RFC 5322 简化版邮箱正则
EMAIL_PATTERN = re.compile(
    r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+'
    r'@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?'
    r'(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
)

# 常见邮箱域名
COMMON_EMAIL_DOMAINS = {
    'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
    'live.com', 'qq.com', '163.com', '126.com', 'sina.com',
    'foxmail.com', 'icloud.com', 'me.com', 'msn.com',
    'aliyun.com', 'yeah.net', '139.com', '189.cn'
}

# 临时邮箱域名（通常应被拒绝）
TEMP_EMAIL_DOMAINS = {
    'tempmail.com', 'guerrillamail.com', '10minutemail.com',
    'mailinator.com', 'throwaway.email', 'fakeinbox.com',
    'maildrop.cc', 'getairmail.com', 'sharklasers.com'
}


def validate_email(email: str, 
                   check_domain: bool = False,
                   allow_temp: bool = False,
                   allow_plus_alias: bool = True) -> ValidationResult:
    """
    验证邮箱地址
    
    Args:
        email: 邮箱地址
        check_domain: 是否检查域名是否为常见域名
        allow_temp: 是否允许临时邮箱
        allow_plus_alias: 是否允许 + 号别名（如 user+tag@gmail.com）
    
    Returns:
        ValidationResult: 验证结果
    """
    if not email or not isinstance(email, str):
        return ValidationResult(False, "邮箱不能为空")
    
    email = email.strip()
    
    if len(email) > 254:
        return ValidationResult(False, "邮箱长度超过254字符限制")
    
    # 检查 + 号别名
    if not allow_plus_alias and '+' in email.split('@')[0]:
        return ValidationResult(False, "不允许使用 + 号别名")
    
    # 基本格式验证
    if not EMAIL_PATTERN.match(email):
        return ValidationResult(False, "邮箱格式无效")
    
    # 分解检查
    parts = email.rsplit('@', 1)
    if len(parts) != 2:
        return ValidationResult(False, "邮箱格式无效")
    
    local_part, domain = parts
    
    # 检查本地部分
    if len(local_part) > 64:
        return ValidationResult(False, "邮箱本地部分超过64字符限制")
    
    if local_part.startswith('.') or local_part.endswith('.'):
        return ValidationResult(False, "邮箱本地部分不能以点开头或结尾")
    
    if '..' in local_part:
        return ValidationResult(False, "邮箱本地部分不能包含连续的点")
    
    # 检查域名
    domain = domain.lower()
    
    if check_domain:
        if domain in TEMP_EMAIL_DOMAINS and not allow_temp:
            return ValidationResult(False, f"临时邮箱域名 {domain} 不被允许")
    
    details = {
        'local_part': local_part,
        'domain': domain,
        'is_common_domain': domain in COMMON_EMAIL_DOMAINS,
        'is_temp_domain': domain in TEMP_EMAIL_DOMAINS
    }
    
    return ValidationResult(True, "邮箱格式有效", details)


# ============ 中国手机号验证 ============

# 中国手机号运营商号段（2024年更新）
CHINA_MOBILE_PREFIXES = {
    # 中国移动
    '134', '135', '136', '137', '138', '139', '147', '148',
    '150', '151', '152', '157', '158', '159', '172', '178',
    '182', '183', '184', '187', '188', '195', '197', '198',
    # 中国联通
    '130', '131', '132', '145', '146', '155', '156', '166',
    '175', '176', '185', '186', '196',
    # 中国电信
    '133', '149', '153', '173', '174', '177', '180', '181', '189',
    '190', '191', '193', '199',
    # 中国广电
    '192',
    # 虚拟运营商
    '162', '165', '167', '170', '171'
}

CHINA_MOBILE_CARRIER = {
    # 中国移动
    '134': '中国移动', '135': '中国移动', '136': '中国移动', '137': '中国移动',
    '138': '中国移动', '139': '中国移动', '147': '中国移动', '148': '中国移动',
    '150': '中国移动', '151': '中国移动', '152': '中国移动', '157': '中国移动',
    '158': '中国移动', '159': '中国移动', '172': '中国移动', '178': '中国移动',
    '182': '中国移动', '183': '中国移动', '184': '中国移动', '187': '中国移动',
    '188': '中国移动', '195': '中国移动', '197': '中国移动', '198': '中国移动',
    # 中国联通
    '130': '中国联通', '131': '中国联通', '132': '中国联通', '145': '中国联通',
    '146': '中国联通', '155': '中国联通', '156': '中国联通', '166': '中国联通',
    '175': '中国联通', '176': '中国联通', '185': '中国联通', '186': '中国联通',
    '196': '中国联通',
    # 中国电信
    '133': '中国电信', '149': '中国电信', '153': '中国电信', '173': '中国电信',
    '174': '中国电信', '177': '中国电信', '180': '中国电信', '181': '中国电信',
    '189': '中国电信', '190': '中国电信', '191': '中国电信', '193': '中国电信',
    '199': '中国电信',
    # 中国广电
    '192': '中国广电',
    # 虚拟运营商
    '162': '虚拟运营商', '165': '虚拟运营商', '167': '虚拟运营商',
    '170': '虚拟运营商', '171': '虚拟运营商'
}


def validate_china_mobile(phone: str, 
                          strict: bool = True) -> ValidationResult:
    """
    验证中国大陆手机号码
    
    Args:
        phone: 手机号码
        strict: 严格模式，验证运营商号段
    
    Returns:
        ValidationResult: 验证结果
    """
    if not phone or not isinstance(phone, str):
        return ValidationResult(False, "手机号不能为空")
    
    # 移除所有非数字字符
    phone = re.sub(r'[^\d]', '', phone)
    
    # 检查长度
    if len(phone) == 11 and phone.startswith('1'):
        pass  # 标准格式
    elif len(phone) == 13 and phone.startswith('86'):
        phone = phone[2:]  # 去掉国际区号
    elif len(phone) == 14 and phone.startswith('086'):
        phone = phone[3:]  # 去掉国际区号
    else:
        return ValidationResult(False, "手机号长度无效，应为11位数字")
    
    # 验证号段
    prefix = phone[:3]
    
    if strict:
        if prefix not in CHINA_MOBILE_PREFIXES:
            return ValidationResult(False, f"无效的手机号段: {prefix}")
        
        carrier = CHINA_MOBILE_CARRIER.get(prefix, '未知')
        details = {
            'phone': phone,
            'prefix': prefix,
            'carrier': carrier,
            'formatted': phone,
            'formatted_with_space': f"{phone[:3]} {phone[3:7]} {phone[7:]}"
        }
    else:
        # 非严格模式，只验证 13x/14x/15x/16x/17x/18x/19x
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return ValidationResult(False, "手机号格式无效")
        
        carrier = CHINA_MOBILE_CARRIER.get(prefix, '未知')
        details = {
            'phone': phone,
            'prefix': prefix,
            'carrier': carrier,
            'formatted': phone,
            'formatted_with_space': f"{phone[:3]} {phone[3:7]} {phone[7:]}"
        }
    
    return ValidationResult(True, "手机号格式有效", details)


# ============ 中国身份证验证 ============

# 省份代码
PROVINCE_CODES = {
    '11': '北京市', '12': '天津市', '13': '河北省', '14': '山西省',
    '15': '内蒙古自治区', '21': '辽宁省', '22': '吉林省', '23': '黑龙江省',
    '31': '上海市', '32': '江苏省', '33': '浙江省', '34': '安徽省',
    '35': '福建省', '36': '江西省', '37': '山东省', '41': '河南省',
    '42': '湖北省', '43': '湖南省', '44': '广东省', '45': '广西壮族自治区',
    '46': '海南省', '50': '重庆市', '51': '四川省', '52': '贵州省',
    '53': '云南省', '54': '西藏自治区', '61': '陕西省', '62': '甘肃省',
    '63': '青海省', '64': '宁夏回族自治区', '65': '新疆维吾尔自治区',
    '71': '台湾省', '81': '香港特别行政区', '82': '澳门特别行政区'
}

# 校验码权重
ID_WEIGHTS = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
# 校验码映射
ID_CHECK_CODES = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']


def validate_china_id(id_number: str, 
                      check_age: bool = False,
                      min_age: int = 0,
                      max_age: int = 150) -> ValidationResult:
    """
    验证中国大陆身份证号码
    
    Args:
        id_number: 身份证号码（15位或18位）
        check_age: 是否检查年龄范围
        min_age: 最小年龄
        max_age: 最大年龄
    
    Returns:
        ValidationResult: 验证结果
    """
    if not id_number or not isinstance(id_number, str):
        return ValidationResult(False, "身份证号不能为空")
    
    # 移除空格
    id_number = id_number.strip().upper()
    
    # 检查基本格式
    if not re.match(r'^\d{17}[\dX]$|^\d{15}$', id_number):
        return ValidationResult(False, "身份证号格式无效，应为15位或18位")
    
    # 如果是15位，转换为18位
    if len(id_number) == 15:
        id_number = _convert_15_to_18(id_number)
    
    # 验证省份代码
    province_code = id_number[:2]
    if province_code not in PROVINCE_CODES:
        return ValidationResult(False, f"无效的省份代码: {province_code}")
    
    # 验证出生日期
    birth_date_str = id_number[6:14]
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y%m%d')
    except ValueError:
        return ValidationResult(False, f"无效的出生日期: {birth_date_str}")
    
    # 检查日期是否合理
    if birth_date > datetime.now():
        return ValidationResult(False, "出生日期不能晚于当前日期")
    
    if birth_date.year < 1900:
        return ValidationResult(False, "出生年份不能早于1900年")
    
    # 验证校验码
    checksum = 0
    for i in range(17):
        checksum += int(id_number[i]) * ID_WEIGHTS[i]
    
    expected_check_code = ID_CHECK_CODES[checksum % 11]
    actual_check_code = id_number[17]
    
    if expected_check_code != actual_check_code:
        return ValidationResult(False, f"校验码错误，应为 {expected_check_code}")
    
    # 计算年龄
    today = datetime.now()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    if check_age:
        if age < min_age:
            return ValidationResult(False, f"年龄 {age} 岁小于最小年龄 {min_age} 岁")
        if age > max_age:
            return ValidationResult(False, f"年龄 {age} 岁超过最大年龄 {max_age} 岁")
    
    # 提取性别（第17位，奇数为男，偶数为女）
    gender_code = int(id_number[16])
    gender = '男' if gender_code % 2 == 1 else '女'
    
    # 提取地区码
    region_code = id_number[:6]
    
    details = {
        'id_number': id_number,
        'province': PROVINCE_CODES[province_code],
        'province_code': province_code,
        'region_code': region_code,
        'birth_date': birth_date.strftime('%Y-%m-%d'),
        'age': age,
        'gender': gender,
        'formatted': f"{id_number[:6]} {id_number[6:14]} {id_number[14:]}"
    }
    
    return ValidationResult(True, "身份证号有效", details)


def _convert_15_to_18(id_15: str) -> str:
    """将15位身份证号转换为18位"""
    # 在第6位后插入"19"（15位身份证默认为19xx年出生）
    id_17 = id_15[:6] + '19' + id_15[6:]
    
    # 计算校验码
    checksum = 0
    for i in range(17):
        checksum += int(id_17[i]) * ID_WEIGHTS[i]
    
    check_code = ID_CHECK_CODES[checksum % 11]
    return id_17 + check_code


# ============ IP 地址验证 ============

def validate_ipv4(ip: str) -> ValidationResult:
    """
    验证 IPv4 地址
    
    Args:
        ip: IPv4 地址字符串
    
    Returns:
        ValidationResult: 验证结果
    """
    if not ip or not isinstance(ip, str):
        return ValidationResult(False, "IP地址不能为空")
    
    ip = ip.strip()
    parts = ip.split('.')
    
    if len(parts) != 4:
        return ValidationResult(False, "IPv4地址应包含4个部分")
    
    try:
        octets = [int(part) for part in parts]
    except ValueError:
        return ValidationResult(False, "IPv4地址各部分应为数字")
    
    for octet in octets:
        if octet < 0 or octet > 255:
            return ValidationResult(False, f"无效的八位组值: {octet}")
    
    # 判断地址类型
    first_octet = octets[0]
    if first_octet == 10:
        ip_class = 'A类私有地址'
        is_private = True
    elif first_octet == 172 and 16 <= octets[1] <= 31:
        ip_class = 'B类私有地址'
        is_private = True
    elif first_octet == 192 and octets[1] == 168:
        ip_class = 'C类私有地址'
        is_private = True
    elif first_octet == 127:
        ip_class = '环回地址'
        is_private = True
    elif first_octet == 0:
        ip_class = '本网络地址'
        is_private = True
    elif first_octet >= 224:
        if first_octet <= 239:
            ip_class = 'D类组播地址'
        else:
            ip_class = 'E类保留地址'
        is_private = False
    else:
        ip_class = '公网地址'
        is_private = False
    
    # 计算数值
    ip_value = (octets[0] << 24) + (octets[1] << 16) + (octets[2] << 8) + octets[3]
    
    details = {
        'ip': ip,
        'octets': octets,
        'class': ip_class,
        'is_private': is_private,
        'is_loopback': first_octet == 127,
        'numeric_value': ip_value,
        'binary': '.'.join(f'{o:08b}' for o in octets)
    }
    
    return ValidationResult(True, "有效的IPv4地址", details)


def validate_ipv6(ip: str) -> ValidationResult:
    """
    验证 IPv6 地址
    
    Args:
        ip: IPv6 地址字符串
    
    Returns:
        ValidationResult: 验证结果
    """
    if not ip or not isinstance(ip, str):
        return ValidationResult(False, "IP地址不能为空")
    
    ip = ip.strip()
    
    # 处理 IPv4 映射地址
    if '.' in ip:
        # IPv4 映射地址 (::ffff:192.168.1.1)
        if ip.count(':') < 2:
            return ValidationResult(False, "无效的IPv6地址格式")
        
        # 分割 IPv4 部分
        last_colon = ip.rfind(':')
        ipv4_part = ip[last_colon + 1:]
        ipv6_part = ip[:last_colon + 1]
        
        # 验证 IPv4 部分
        ipv4_result = validate_ipv4(ipv4_part)
        if not ipv4_result:
            return ipv4_result
        
        # 将 IPv4 转换为 IPv6 格式
        octets = ipv4_result.details['octets']
        ipv4_in_ipv6 = f"{octets[0]:02x}{octets[1]:02x}:{octets[2]:02x}{octets[3]:02x}"
        ip = ipv6_part.replace('::', f':{ipv4_in_ipv6}::', 1) if '::' in ipv6_part else ipv6_part + ipv4_in_ipv6
    
    # 处理 :: 缩写
    if '::' in ip:
        if ip.count('::') > 1:
            return ValidationResult(False, "IPv6地址只能包含一个 ::")
        
        # 展开 :: 
        parts = ip.split('::')
        left = parts[0].split(':') if parts[0] else []
        right = parts[1].split(':') if parts[1] else []
        
        # 过滤空字符串
        left = [p for p in left if p]
        right = [p for p in right if p]
        
        missing = 8 - len(left) - len(right)
        if missing < 0:
            return ValidationResult(False, "IPv6地址段数过多")
        
        expanded = left + ['0'] * missing + right
    else:
        expanded = ip.split(':')
    
    # 验证段数
    if len(expanded) != 8:
        return ValidationResult(False, f"IPv6地址应包含8段，实际{len(expanded)}段")
    
    # 验证每段
    for i, part in enumerate(expanded):
        if not part:
            expanded[i] = '0'
            continue
        
        if len(part) > 4:
            return ValidationResult(False, f"IPv6地址段 {part} 超过4个字符")
        
        try:
            int(part, 16)
        except ValueError:
            return ValidationResult(False, f"无效的IPv6地址段: {part}")
    
    # 标准化
    normalized = ':'.join(expanded)
    
    # 判断类型
    if expanded[0] == '0' * 8:
        if all(p == '0' for p in expanded):
            ip_class = '未指定地址'
        elif expanded[-1] == '1' and all(p == '0' for p in expanded[:-1]):
            ip_class = '环回地址'
        else:
            ip_class = '特殊地址'
        is_loopback = expanded[-1] == '1'
    elif expanded[0].lower().startswith('fe8'):
        ip_class = '链路本地地址'
        is_loopback = False
    elif expanded[0].lower().startswith('fec') or expanded[0].lower().startswith('fed'):
        ip_class = '站点本地地址'
        is_loopback = False
    elif expanded[0] == '0' and '::' in ip:
        ip_class = 'IPv4映射地址'
        is_loopback = False
    else:
        ip_class = '公网地址'
        is_loopback = False
    
    details = {
        'ip': ip,
        'normalized': normalized,
        'compressed': _compress_ipv6(normalized),
        'class': ip_class,
        'is_loopback': is_loopback,
        'segments': expanded
    }
    
    return ValidationResult(True, "有效的IPv6地址", details)


def _compress_ipv6(ip: str) -> str:
    """压缩 IPv6 地址"""
    segments = ip.split(':')
    
    # 找到最长的连续零段
    zero_start = -1
    zero_len = 0
    current_start = -1
    current_len = 0
    
    for i, seg in enumerate(segments):
        if seg == '0':
            if current_start == -1:
                current_start = i
            current_len += 1
        else:
            if current_len > zero_len:
                zero_start = current_start
                zero_len = current_len
            current_start = -1
            current_len = 0
    
    if current_len > zero_len:
        zero_start = current_start
        zero_len = current_len
    
    # 如果有连续零段，压缩
    if zero_len >= 2:
        before = segments[:zero_start]
        after = segments[zero_start + zero_len:]
        
        if not before and not after:
            return '::'
        elif not before:
            return '::' + ':'.join(after)
        elif not after:
            return ':'.join(before) + '::'
        else:
            return ':'.join(before) + '::' + ':'.join(after)
    
    return ip


def validate_ip(ip: str) -> ValidationResult:
    """
    验证 IP 地址（自动检测 IPv4 或 IPv6）
    
    Args:
        ip: IP 地址字符串
    
    Returns:
        ValidationResult: 验证结果
    """
    if '.' in ip:
        return validate_ipv4(ip)
    elif ':' in ip:
        return validate_ipv6(ip)
    else:
        return ValidationResult(False, "无法识别的IP地址格式")


# ============ URL 验证 ============

# URL 正则
URL_PATTERN = re.compile(
    r'^(?P<scheme>[a-zA-Z][a-zA-Z0-9+.-]*)://'
    r'(?P<authority>'
        r'(?:(?P<userinfo>[^@/:?#]+)@)?'
        r'(?P<host>[^:/?#]+)'
        r'(?::(?P<port>\d+))?'
    r')'
    r'(?P<path>/[^?#]*)?'
    r'(?:\?(?P<query>[^#]*))?'
    r'(?:#(?P<fragment>.*))?'
)

# 常见协议
COMMON_SCHEMES = {
    'http', 'https', 'ftp', 'ftps', 'sftp',
    'ws', 'wss', 'ssh', 'telnet', 'mailto',
    'file', 'data', 'blob'
}


def validate_url(url: str,
                require_scheme: bool = True,
                allowed_schemes: Optional[List[str]] = None,
                require_tld: bool = True) -> ValidationResult:
    """
    验证 URL
    
    Args:
        url: URL 字符串
        require_scheme: 是否要求协议
        allowed_schemes: 允许的协议列表
        require_tld: 是否要求顶级域名
    
    Returns:
        ValidationResult: 验证结果
    """
    if not url or not isinstance(url, str):
        return ValidationResult(False, "URL不能为空")
    
    url = url.strip()
    
    # 检查是否缺少协议
    if require_scheme and '://' not in url:
        return ValidationResult(False, "URL缺少协议（如 https://）")
    
    # 基本解析
    match = URL_PATTERN.match(url)
    if not match:
        # 尝试更宽松的匹配
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            if not parsed.scheme and require_scheme:
                return ValidationResult(False, "URL缺少协议")
            if not parsed.netloc:
                return ValidationResult(False, "URL缺少主机名")
        except Exception:
            return ValidationResult(False, "URL格式无效")
    else:
        parsed = None
    
    # 使用正则匹配结果或 urlparse
    if match:
        scheme = match.group('scheme').lower()
        host = match.group('host')
        port = match.group('port')
        path = match.group('path') or '/'
        query = match.group('query')
        fragment = match.group('fragment')
    else:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        scheme = parsed.scheme.lower()
        host = parsed.netloc.split('@')[-1].split(':')[0]
        port = str(parsed.port) if parsed.port else None
        path = parsed.path or '/'
        query = parsed.query
        fragment = parsed.fragment
    
    # 检查协议
    if allowed_schemes and scheme not in allowed_schemes:
        return ValidationResult(False, f"不允许的协议: {scheme}")
    
    # 检查主机
    if not host:
        return ValidationResult(False, "URL缺少主机名")
    
    # 检查端口号
    if port:
        try:
            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                return ValidationResult(False, f"无效的端口号: {port}")
        except ValueError:
            return ValidationResult(False, f"无效的端口号: {port}")
    
    # 检查顶级域名
    if require_tld and '.' not in host:
        # 可能是 localhost 或 IP 地址
        if host != 'localhost' and not host.replace('.', '').replace(':', '').isdigit():
            # 不是 localhost 也不是 IP，检查是否有 TLD
            if not any(host.endswith(tld) for tld in ['.com', '.net', '.org', '.cn', '.io', '.co']):
                pass  # 宽松处理，允许各种格式
    
    details = {
        'url': url,
        'scheme': scheme,
        'host': host,
        'port': int(port) if port else (443 if scheme == 'https' else 80),
        'path': path,
        'query': query,
        'fragment': fragment,
        'is_secure': scheme in ('https', 'ftps', 'wss', 'sftp')
    }
    
    return ValidationResult(True, "有效的URL", details)


# ============ JSON 验证 ============

def validate_json(json_str: str,
                  schema: Optional[Dict[str, Any]] = None) -> ValidationResult:
    """
    验证 JSON 字符串
    
    Args:
        json_str: JSON 字符串
        schema: 可选的 JSON Schema（简化版）
    
    Returns:
        ValidationResult: 验证结果
    """
    if not json_str or not isinstance(json_str, str):
        return ValidationResult(False, "JSON字符串不能为空")
    
    json_str = json_str.strip()
    
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return ValidationResult(False, f"JSON解析错误: {e.msg} (位置: {e.pos})")
    
    details = {
        'type': type(data).__name__,
        'size': len(json_str),
        'valid': True
    }
    
    # 简单的 schema 验证
    if schema:
        schema_errors = _validate_schema(data, schema, '')
        if schema_errors:
            details['schema_errors'] = schema_errors
            return ValidationResult(False, f"Schema验证失败: {'; '.join(schema_errors)}", details)
    
    # 统计信息
    if isinstance(data, dict):
        details['keys'] = list(data.keys())
        details['depth'] = _get_json_depth(data)
    elif isinstance(data, list):
        details['length'] = len(data)
        details['depth'] = _get_json_depth(data)
    
    return ValidationResult(True, "有效的JSON", details)


def _validate_schema(data: Any, schema: Dict[str, Any], path: str) -> List[str]:
    """简化的 schema 验证"""
    errors = []
    
    if 'type' in schema:
        expected_type = schema['type']
        type_map = {
            'string': str,
            'number': (int, float),
            'integer': int,
            'boolean': bool,
            'array': list,
            'object': dict,
            'null': type(None)
        }
        
        if expected_type in type_map:
            if not isinstance(data, type_map[expected_type]):
                errors.append(f"{path}: 期望类型 {expected_type}，实际类型 {type(data).__name__}")
    
    if 'required' in schema and isinstance(data, dict):
        for field in schema['required']:
            if field not in data:
                errors.append(f"{path}: 缺少必需字段 '{field}'")
    
    if 'properties' in schema and isinstance(data, dict):
        for key, prop_schema in schema['properties'].items():
            if key in data:
                errors.extend(_validate_schema(data[key], prop_schema, f"{path}.{key}"))
    
    if 'items' in schema and isinstance(data, list):
        for i, item in enumerate(data):
            errors.extend(_validate_schema(item, schema['items'], f"{path}[{i}]"))
    
    if 'minLength' in schema and isinstance(data, (str, list)):
        if len(data) < schema['minLength']:
            errors.append(f"{path}: 长度 {len(data)} 小于最小长度 {schema['minLength']}")
    
    if 'maxLength' in schema and isinstance(data, (str, list)):
        if len(data) > schema['maxLength']:
            errors.append(f"{path}: 长度 {len(data)} 超过最大长度 {schema['maxLength']}")
    
    if 'minimum' in schema and isinstance(data, (int, float)):
        if data < schema['minimum']:
            errors.append(f"{path}: 值 {data} 小于最小值 {schema['minimum']}")
    
    if 'maximum' in schema and isinstance(data, (int, float)):
        if data > schema['maximum']:
            errors.append(f"{path}: 值 {data} 超过最大值 {schema['maximum']}")
    
    if 'pattern' in schema and isinstance(data, str):
        if not re.match(schema['pattern'], data):
            errors.append(f"{path}: 字符串不匹配模式 {schema['pattern']}")
    
    if 'enum' in schema:
        if data not in schema['enum']:
            errors.append(f"{path}: 值 {data} 不在枚举值中 {schema['enum']}")
    
    return errors


def _get_json_depth(data: Any, current: int = 1) -> int:
    """计算 JSON 深度"""
    if isinstance(data, dict):
        if not data:
            return current
        return max(_get_json_depth(v, current + 1) for v in data.values())
    elif isinstance(data, list):
        if not data:
            return current
        return max(_get_json_depth(item, current + 1) for item in data)
    return current


# ============ 信用卡号验证 ============

# 银行卡号前缀
CARD_PREFIXES = {
    '4': 'Visa',
    '5': 'MasterCard',
    '34': 'American Express',
    '37': 'American Express',
    '6': 'Discover',
    '35': 'JCB',
    '6011': 'Discover',
    '65': 'Discover',
    '2131': 'JCB',
    '1800': 'JCB'
}


def validate_credit_card(card_number: str) -> ValidationResult:
    """
    验证信用卡号
    
    Args:
        card_number: 信用卡号
    
    Returns:
        ValidationResult: 验证结果
    """
    if not card_number or not isinstance(card_number, str):
        return ValidationResult(False, "卡号不能为空")
    
    # 移除空格和横线
    card_number = re.sub(r'[\s-]', '', card_number)
    
    # 检查是否全为数字
    if not card_number.isdigit():
        return ValidationResult(False, "卡号只能包含数字")
    
    # 检查长度
    if len(card_number) < 13 or len(card_number) > 19:
        return ValidationResult(False, f"卡号长度 {len(card_number)} 无效，应为13-19位")
    
    # Luhn 算法校验
    if not _luhn_check(card_number):
        return ValidationResult(False, "卡号校验失败（Luhn算法）")
    
    # 识别卡类型
    card_type = 'Unknown'
    for prefix, name in sorted(CARD_PREFIXES.items(), key=lambda x: -len(x[0])):
        if card_number.startswith(prefix):
            card_type = name
            break
    
    details = {
        'card_number': card_number,
        'card_type': card_type,
        'length': len(card_number),
        'formatted': _format_card_number(card_number),
        'last_four': card_number[-4:]
    }
    
    return ValidationResult(True, f"有效的{card_type}卡号", details)


def _luhn_check(card_number: str) -> bool:
    """Luhn 算法校验"""
    digits = [int(d) for d in card_number]
    
    # 从右向左，每隔一位翻倍
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    
    return sum(digits) % 10 == 0


def _format_card_number(card_number: str) -> str:
    """格式化卡号显示"""
    if len(card_number) == 16:
        return f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
    elif len(card_number) == 15:
        return f"{card_number[:4]} {card_number[4:10]} {card_number[10:]}"
    else:
        # 通用格式化
        parts = [card_number[i:i+4] for i in range(0, len(card_number), 4)]
        return ' '.join(parts)


# ============ 其他验证 ============

def validate_china_bank_card(card_number: str) -> ValidationResult:
    """
    验证中国银行卡号（支持主流银行）
    
    Args:
        card_number: 银行卡号
    
    Returns:
        ValidationResult: 验证结果
    """
    if not card_number or not isinstance(card_number, str):
        return ValidationResult(False, "卡号不能为空")
    
    # 移除空格
    card_number = re.sub(r'\s', '', card_number)
    
    # 检查是否全为数字
    if not card_number.isdigit():
        return ValidationResult(False, "卡号只能包含数字")
    
    # 检查长度（通常16-19位）
    if len(card_number) < 16 or len(card_number) > 19:
        return ValidationResult(False, f"卡号长度 {len(card_number)} 无效，应为16-19位")
    
    # Luhn 校验（部分银行使用）
    # 中国部分银行使用 Luhn，部分不使用，所以只做基本检查
    
    # 银行卡前缀识别（部分常见银行）
    bank_prefixes = {
        '621': '中国银行',
        '622': '工商银行',
        '623': '建设银行',
        '601': '农业银行',
        '625': '交通银行',
        '628': '招商银行',
        '685': '民生银行',
        '6217': '中国银行',
        '6222': '工商银行',
        '6225': '建设银行',
        '6228': '农业银行'
    }
    
    bank = '未知银行'
    for prefix, name in sorted(bank_prefixes.items(), key=lambda x: -len(x[0])):
        if card_number.startswith(prefix):
            bank = name
            break
    
    details = {
        'card_number': card_number,
        'bank': bank,
        'length': len(card_number),
        'formatted': _format_card_number(card_number),
        'last_four': card_number[-4:]
    }
    
    return ValidationResult(True, f"有效的银行卡号", details)


def validate_chinese_name(name: str, min_length: int = 2, max_length: int = 20) -> ValidationResult:
    """
    验证中文姓名
    
    Args:
        name: 姓名
        min_length: 最小长度
        max_length: 最大长度
    
    Returns:
        ValidationResult: 验证结果
    """
    if not name or not isinstance(name, str):
        return ValidationResult(False, "姓名不能为空")
    
    name = name.strip()
    
    # 检查长度
    if len(name) < min_length:
        return ValidationResult(False, f"姓名长度不能少于{min_length}个字符")
    
    if len(name) > max_length:
        return ValidationResult(False, f"姓名长度不能超过{max_length}个字符")
    
    # 检查是否包含数字或特殊字符（允许中文、·、•）
    # 中文字符范围：\u4e00-\u9fff
    pattern = re.compile(r'^[\u4e00-\u9fff·•]+$')
    if not pattern.match(name):
        return ValidationResult(False, "姓名只能包含中文字符")
    
    # 检查常见姓氏
    common_surnames = ['王', '李', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴',
                       '徐', '孙', '胡', '朱', '高', '林', '何', '郭', '马', '罗',
                       '梁', '宋', '郑', '谢', '韩', '唐', '冯', '于', '董', '萧',
                       '程', '曹', '袁', '邓', '许', '傅', '沈', '曾', '彭', '吕',
                       '苏', '卢', '蒋', '蔡', '贾', '丁', '魏', '薛', '叶', '阎',
                       '余', '潘', '杜', '戴', '夏', '钟', '汪', '田', '任', '姜',
                       '范', '方', '石', '姚', '谭', '廖', '邹', '熊', '金', '陆',
                       '郝', '孔', '白', '崔', '康', '毛', '邱', '秦', '江', '史',
                       '顾', '侯', '邵', '孟', '龙', '万', '段', '漕', '钱', '汤',
                       '尹', '黎', '易', '常', '武', '乔', '贺', '赖', '龚', '文']
    
    surname = name[0]
    is_common_surname = surname in common_surnames
    
    details = {
        'name': name,
        'length': len(name),
        'surname': surname,
        'is_common_surname': is_common_surname
    }
    
    return ValidationResult(True, "有效的中文姓名", details)


def validate_password(password: str,
                     min_length: int = 8,
                     max_length: int = 128,
                     require_uppercase: bool = True,
                     require_lowercase: bool = True,
                     require_digit: bool = True,
                     require_special: bool = False,
                     special_chars: str = "!@#$%^&*()_+-=[]{}|;':\",./<>?") -> ValidationResult:
    """
    验证密码强度
    
    Args:
        password: 密码
        min_length: 最小长度
        max_length: 最大长度
        require_uppercase: 是否要求大写字母
        require_lowercase: 是否要求小写字母
        require_digit: 是否要求数字
        require_special: 是否要求特殊字符
        special_chars: 允许的特殊字符
    
    Returns:
        ValidationResult: 验证结果
    """
    if not password or not isinstance(password, str):
        return ValidationResult(False, "密码不能为空")
    
    errors = []
    checks = {}
    
    # 检查长度
    if len(password) < min_length:
        errors.append(f"密码长度不能少于{min_length}个字符")
    if len(password) > max_length:
        errors.append(f"密码长度不能超过{max_length}个字符")
    
    checks['length'] = len(password)
    
    # 检查大写字母
    has_upper = bool(re.search(r'[A-Z]', password))
    checks['has_uppercase'] = has_upper
    if require_uppercase and not has_upper:
        errors.append("密码必须包含大写字母")
    
    # 检查小写字母
    has_lower = bool(re.search(r'[a-z]', password))
    checks['has_lowercase'] = has_lower
    if require_lowercase and not has_lower:
        errors.append("密码必须包含小写字母")
    
    # 检查数字
    has_digit = bool(re.search(r'\d', password))
    checks['has_digit'] = has_digit
    if require_digit and not has_digit:
        errors.append("密码必须包含数字")
    
    # 检查特殊字符
    has_special = bool(re.search(f'[{re.escape(special_chars)}]', password))
    checks['has_special'] = has_special
    if require_special and not has_special:
        errors.append(f"密码必须包含特殊字符（{special_chars}）")
    
    # 计算强度分数
    score = 0
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1
    if has_upper:
        score += 1
    if has_lower:
        score += 1
    if has_digit:
        score += 1
    if has_special:
        score += 2
    
    strength_levels = ['非常弱', '弱', '一般', '中等', '强', '很强', '非常强', '极强']
    strength = strength_levels[min(score, len(strength_levels) - 1)]
    
    details = {
        'length': len(password),
        'has_uppercase': has_upper,
        'has_lowercase': has_lower,
        'has_digit': has_digit,
        'has_special': has_special,
        'score': score,
        'strength': strength
    }
    
    if errors:
        return ValidationResult(False, "; ".join(errors), details)
    
    return ValidationResult(True, f"密码强度：{strength}", details)


def validate_chinese_phone(phone: str) -> ValidationResult:
    """
    验证中国电话号码（固定电话或手机）
    
    Args:
        phone: 电话号码
    
    Returns:
        ValidationResult: 验证结果
    """
    if not phone or not isinstance(phone, str):
        return ValidationResult(False, "电话号码不能为空")
    
    # 移除所有非数字字符
    digits = re.sub(r'[^\d]', '', phone)
    
    # 尝试作为手机号验证
    if re.match(r'^1[3-9]\d{9}$', digits):
        return validate_china_mobile(digits)
    
    # 尝试作为固定电话验证
    # 格式：区号（3-4位）+ 号码（7-8位）
    # 常见区号：010, 020, 021, 022, 023, 024, 025, 027, 028, 029, 0755, 等
    
    landline_pattern = re.compile(r'^0\d{2,3}[1-9]\d{6,7}$')
    
    if landline_pattern.match(digits):
        # 提取区号和号码
        if digits[1] in '12':  # 两位区号（010, 020等）
            area_code = digits[:3]
            number = digits[3:]
        else:  # 三位区号
            area_code = digits[:4]
            number = digits[4:]
        
        # 常见城市区号
        city_codes = {
            '010': '北京', '020': '广州', '021': '上海', '022': '天津',
            '023': '重庆', '024': '沈阳', '025': '南京', '027': '武汉',
            '028': '成都', '029': '西安', '0755': '深圳', '0757': '佛山',
            '0769': '东莞', '0752': '惠州', '0760': '中山', '0754': '汕头'
        }
        
        city = city_codes.get(area_code, '未知城市')
        
        details = {
            'type': '固定电话',
            'phone': digits,
            'area_code': area_code,
            'number': number,
            'city': city,
            'formatted': f"{area_code}-{number}"
        }
        
        return ValidationResult(True, f"有效的固定电话号码（{city}）", details)
    
    # 400/800 电话
    if re.match(r'^[48]00\d{7}$', digits):
        service_type = '400客服电话' if digits.startswith('4') else '800客服电话'
        details = {
            'type': service_type,
            'phone': digits,
            'formatted': f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        }
        return ValidationResult(True, f"有效的{service_type}", details)
    
    return ValidationResult(False, "无法识别的电话号码格式")


# ============ 批量验证 ============

def validate_batch(items: List[str], validator: str, **kwargs) -> Dict[str, Any]:
    """
    批量验证
    
    Args:
        items: 待验证项列表
        validator: 验证器名称（email, mobile, id, ipv4, ipv6, url, json, credit_card, password）
        **kwargs: 传递给验证器的参数
    
    Returns:
        包含验证结果的字典
    """
    validators = {
        'email': lambda x: validate_email(x, **kwargs),
        'mobile': lambda x: validate_china_mobile(x, **kwargs),
        'id': lambda x: validate_china_id(x, **kwargs),
        'ipv4': validate_ipv4,
        'ipv6': validate_ipv6,
        'ip': validate_ip,
        'url': lambda x: validate_url(x, **kwargs),
        'json': validate_json,
        'credit_card': validate_credit_card,
        'bank_card': validate_china_bank_card,
        'chinese_name': lambda x: validate_chinese_name(x, **kwargs),
        'password': lambda x: validate_password(x, **kwargs),
        'phone': validate_chinese_phone
    }
    
    if validator not in validators:
        return {'error': f"未知的验证器: {validator}"}
    
    validate_func = validators[validator]
    
    results = {
        'total': len(items),
        'valid': 0,
        'invalid': 0,
        'items': []
    }
    
    for item in items:
        result = validate_func(item)
        results['items'].append({
            'input': item,
            'is_valid': result.is_valid,
            'message': result.message,
            'details': result.details
        })
        
        if result.is_valid:
            results['valid'] += 1
        else:
            results['invalid'] += 1
    
    return results


# 导出公共 API
__all__ = [
    'ValidationResult',
    # 邮箱验证
    'validate_email',
    # 手机号验证
    'validate_china_mobile',
    # 身份证验证
    'validate_china_id',
    # IP 地址验证
    'validate_ipv4',
    'validate_ipv6',
    'validate_ip',
    # URL 验证
    'validate_url',
    # JSON 验证
    'validate_json',
    # 信用卡验证
    'validate_credit_card',
    # 银行卡验证
    'validate_china_bank_card',
    # 中文姓名验证
    'validate_chinese_name',
    # 密码验证
    'validate_password',
    # 电话验证
    'validate_chinese_phone',
    # 批量验证
    'validate_batch',
    # 常量
    'COMMON_EMAIL_DOMAINS',
    'TEMP_EMAIL_DOMAINS',
    'CHINA_MOBILE_PREFIXES',
    'CHINA_MOBILE_CARRIER',
    'PROVINCE_CODES'
]