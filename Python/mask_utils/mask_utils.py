"""
Mask Utilities - 敏感数据脱敏工具

提供各种敏感数据的脱敏/掩码功能，用于日志、调试、数据展示等场景。
零外部依赖，纯 Python 标准库实现。

Author: AllToolkit
Date: 2026-04-15
"""

import re
from typing import Optional, Tuple, List


def mask_email(email: str, visible_prefix: int = 2, visible_domain: int = 1, mask_char: str = "*") -> str:
    """
    掩码邮箱地址
    
    Args:
        email: 邮箱地址
        visible_prefix: 用户名可见前缀字符数
        visible_domain: 域名可见后缀部分数（如 .com = 1）
        mask_char: 掩码字符
    
    Returns:
        掩码后的邮箱
        
    Examples:
        >>> mask_email("user@example.com")
        'us**@*****.com'
        >>> mask_email("admin@company.co.uk")
        'ad***@******.co.uk'
    """
    if not email or '@' not in email:
        return email
    
    username, domain = email.rsplit('@', 1)
    
    # 掩码用户名
    if len(username) <= visible_prefix:
        masked_username = username[0] + mask_char * (len(username) - 1)
    else:
        masked_username = username[:visible_prefix] + mask_char * (len(username) - visible_prefix)
    
    # 掩码域名
    domain_parts = domain.split('.')
    if len(domain_parts) > visible_domain:
        visible_suffix = '.'.join(domain_parts[-visible_domain:])
        main_domain = '.'.join(domain_parts[:-visible_domain])
        masked_domain = mask_char * len(main_domain) + '.' + visible_suffix
    else:
        masked_domain = mask_char * (len(domain) - len(domain_parts[-1]) - 1) + '.' + domain_parts[-1]
    
    return f"{masked_username}@{masked_domain}"


def mask_phone(phone: str, visible_prefix: int = 3, visible_suffix: int = 4, mask_char: str = "*") -> str:
    """
    掩码手机号码
    
    Args:
        phone: 手机号码（可包含空格、横线等分隔符）
        visible_prefix: 可见前缀位数
        visible_suffix: 可见后缀位数
        mask_char: 掩码字符
    
    Returns:
        掩码后的手机号
        
    Examples:
        >>> mask_phone("13812345678")
        '138****5678'
        >>> mask_phone("+86 138-1234-5678")
        '+86 138****5678'
    """
    if not phone:
        return phone
    
    # 提取纯数字
    digits = re.sub(r'[^\d]', '', phone)
    
    if len(digits) < visible_prefix + visible_suffix:
        return phone  # 太短，不处理
    
    # 构建掩码
    masked_digits = (
        digits[:visible_prefix] + 
        mask_char * (len(digits) - visible_prefix - visible_suffix) + 
        digits[-visible_suffix:]
    )
    
    # 尝试保持原始格式
    # 简单处理：直接返回掩码后的数字
    if phone.startswith('+'):
        # 国际号码格式
        country_code_match = re.match(r'^\+(\d+)\s*', phone)
        if country_code_match:
            country_code = country_code_match.group(1)
            remaining_digits = digits[len(country_code):]
            masked_remaining = (
                remaining_digits[:visible_prefix-1] + 
                mask_char * (len(remaining_digits) - visible_prefix - visible_suffix + 1) + 
                remaining_digits[-visible_suffix:]
            )
            return f"+{country_code} {masked_remaining}"
    
    return masked_digits


def mask_id_card(id_number: str, visible_prefix: int = 2, visible_suffix: int = 2, mask_char: str = "*") -> str:
    """
    掩码身份证号码
    
    Args:
        id_number: 身份证号
        visible_prefix: 可见前缀位数
        visible_suffix: 可见后缀位数
        mask_char: 掩码字符
    
    Returns:
        掩码后的身份证号
        
    Examples:
        >>> mask_id_card("110101199001011234")
        '11**************34'
    """
    if not id_number:
        return id_number
    
    clean_id = id_number.replace(' ', '').replace('-', '')
    
    if len(clean_id) < visible_prefix + visible_suffix:
        return id_number
    
    masked = (
        clean_id[:visible_prefix] + 
        mask_char * (len(clean_id) - visible_prefix - visible_suffix) + 
        clean_id[-visible_suffix:]
    )
    
    return masked


def mask_bank_card(card_number: str, visible_prefix: int = 4, visible_suffix: int = 4, mask_char: str = "*") -> str:
    """
    掩码银行卡号
    
    Args:
        card_number: 银行卡号
        visible_prefix: 可见前缀位数
        visible_suffix: 可见后缀位数
        mask_char: 掩码字符
    
    Returns:
        掩码后的银行卡号
        
    Examples:
        >>> mask_bank_card("6222021234567890123")
        '6222***********0123'
    """
    if not card_number:
        return card_number
    
    digits = re.sub(r'[^\d]', '', card_number)
    
    if len(digits) < visible_prefix + visible_suffix:
        return card_number
    
    masked = (
        digits[:visible_prefix] + 
        mask_char * (len(digits) - visible_prefix - visible_suffix) + 
        digits[-visible_suffix:]
    )
    
    return masked


def mask_credit_card(card_number: str, show_last4: bool = True, mask_char: str = "*") -> str:
    """
    掩码信用卡号
    
    Args:
        card_number: 信用卡号
        show_last4: 是否显示后4位
        mask_char: 掩码字符
    
    Returns:
        掩码后的信用卡号（格式化为 ****-****-****-1234）
        
    Examples:
        >>> mask_credit_card("4532015112830366")
        '****-****-****-0366'
    """
    if not card_number:
        return card_number
    
    digits = re.sub(r'[^\d]', '', card_number)
    
    if len(digits) < 12:
        return card_number
    
    if show_last4:
        last4 = digits[-4:]
        masked = f"{mask_char * 4}-{mask_char * 4}-{mask_char * 4}-{last4}"
    else:
        masked = mask_char * len(digits)
    
    return masked


def mask_name(name: str, show_last_char: bool = True, mask_char: str = "*") -> str:
    """
    掩码姓名
    
    Args:
        name: 姓名
        show_last_char: 是否显示最后一个字符
        mask_char: 掩码字符
    
    Returns:
        掩码后的姓名
        
    Examples:
        >>> mask_name("张三")
        '张*'
        >>> mask_name("王小明")
        '王**'
        >>> mask_name("John Smith")
        'J*** S****'
    """
    if not name:
        return name
    
    # 判断是否为中文姓名
    is_chinese = all('\u4e00' <= char <= '\u9fff' or char in '·' for char in name if char.strip())
    
    if is_chinese:
        # 中文姓名处理
        if show_last_char:
            if len(name) <= 2:
                return name[0] + mask_char
            else:
                return name[0] + mask_char * (len(name) - 1)
        else:
            return name[0] + mask_char * (len(name) - 1)
    else:
        # 英文姓名处理
        parts = name.split()
        masked_parts = []
        for part in parts:
            if len(part) <= 1:
                masked_parts.append(mask_char)
            else:
                masked_parts.append(part[0] + mask_char * (len(part) - 1))
        return ' '.join(masked_parts)


def mask_address(address: str, show_start: int = 10, show_end: int = 5, mask_char: str = "*") -> str:
    """
    掩码地址
    
    Args:
        address: 地址
        show_start: 开头可见字符数
        show_end: 结尾可见字符数
        mask_char: 掩码字符
    
    Returns:
        掩码后的地址
        
    Examples:
        >>> mask_address("北京市朝阳区建国路88号SOHO现代城A座1001")
        '北京市朝阳区建国路**...**A座1001'
    """
    if not address:
        return address
    
    if len(address) <= show_start + show_end:
        return address
    
    # 中间用省略号表示
    masked = address[:show_start] + mask_char * 6 + address[-show_end:]
    return masked


def mask_ip(ip: str, mask_octets: int = 2, mask_char: str = "*") -> str:
    """
    掩码 IP 地址
    
    Args:
        ip: IP 地址（IPv4 或 IPv6）
        mask_octets: 要掩码的段数（对于 IPv4）
        mask_char: 掩码字符
    
    Returns:
        掩码后的 IP 地址
        
    Examples:
        >>> mask_ip("192.168.1.100")
        '192.168.*.*'
        >>> mask_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
        '2001:0db8:*:*:*:*:*:*'
    """
    if not ip:
        return ip
    
    if ':' in ip:
        # IPv6
        parts = ip.split(':')
        masked_parts = parts[:2] + [mask_char] * (len(parts) - 2)
        return ':'.join(masked_parts)
    else:
        # IPv4
        parts = ip.split('.')
        if len(parts) != 4:
            return ip
        
        for i in range(mask_octets):
            parts[-(i + 1)] = mask_char
        return '.'.join(parts)


def mask_password(password: str, show_length: bool = True, mask_char: str = "*") -> str:
    """
    掩码密码
    
    Args:
        password: 密码
        show_length: 是否显示密码长度信息
        mask_char: 掩码字符
    
    Returns:
        掩码后的密码表示
        
    Examples:
        >>> mask_password("MySecret123!")
        '************ (12 chars)'
        >>> mask_password("MySecret123!", show_length=False)
        '************'
    """
    if not password:
        return password
    
    masked = mask_char * len(password)
    if show_length:
        return f"{masked} ({len(password)} chars)"
    return masked


def mask_url(url: str, mask_query: bool = True, mask_path: bool = False, mask_char: str = "***") -> str:
    """
    掩码 URL
    
    Args:
        url: URL 地址
        mask_query: 是否掩码查询参数中的敏感值
        mask_path: 是否掩码路径部分
        mask_char: 掩码字符
    
    Returns:
        掩码后的 URL
        
    Examples:
        >>> mask_url("https://api.example.com/users/123?token=secret&key=abc")
        'https://api.example.com/users/123?token=***&key=***'
    """
    if not url:
        return url
    
    from urllib.parse import urlparse, urlunparse, parse_qs
    
    parsed = urlparse(url)
    
    # 敏感查询参数名
    sensitive_params = {'token', 'key', 'secret', 'password', 'pwd', 'auth', 'api_key', 
                        'apikey', 'access_token', 'refresh_token', 'session', 'session_id'}
    
    if mask_query and parsed.query:
        params = parse_qs(parsed.query, keep_blank_values=True)
        # 手动构建查询字符串，避免 urlencode 对 * 进行编码
        query_parts = []
        for key, values in params.items():
            for value in values:
                if key.lower() in sensitive_params:
                    query_parts.append(f"{key}={mask_char}")
                else:
                    from urllib.parse import quote
                    query_parts.append(f"{key}={quote(value, safe='')}")
        new_query = "&".join(query_parts)
        parsed = parsed._replace(query=new_query)
    
    result = urlunparse(parsed)
    return result


def mask_custom(text: str, pattern: str, mask_char: str = "*") -> str:
    """
    自定义正则模式掩码
    
    Args:
        text: 原始文本
        pattern: 正则表达式模式
        mask_char: 掩码字符
    
    Returns:
        掩码后的文本
        
    Examples:
        >>> mask_custom("订单号: ABC123456XYZ", r'[A-Z]{3}\d{6}[A-Z]{3}')
        '订单号: ***********'
    """
    if not text or not pattern:
        return text
    
    def replace_with_mask(match):
        return mask_char * len(match.group())
    
    return re.sub(pattern, replace_with_mask, text)


def detect_and_mask(text: str, mask_char: str = "*") -> Tuple[str, List[str]]:
    """
    自动检测并掩码文本中的敏感信息
    
    Args:
        text: 原始文本
        mask_char: 掩码字符
    
    Returns:
        (掩码后的文本, 检测到的类型列表)
        
    Examples:
        >>> detect_and_mask("联系邮箱: test@example.com，手机: 13812345678")
        ('联系邮箱: te**@*****.com，手机: 138****5678', ['email', 'phone'])
    """
    detected_types = set()
    result = text
    
    # 邮箱
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    if re.search(email_pattern, result):
        result = re.sub(email_pattern, lambda m: mask_email(m.group(), mask_char=mask_char), result)
        detected_types.add('email')
    
    # 手机号（中国）
    phone_pattern = r'(?<!\d)(?:\+86\s?)?1[3-9]\d{9}(?!\d)'
    if re.search(phone_pattern, result):
        result = re.sub(phone_pattern, lambda m: mask_phone(m.group(), mask_char=mask_char), result)
        detected_types.add('phone')
    
    # 身份证号
    id_card_pattern = r'(?<!\d)\d{17}[\dXx](?!\d)'
    if re.search(id_card_pattern, result):
        result = re.sub(id_card_pattern, lambda m: mask_id_card(m.group(), mask_char=mask_char), result)
        detected_types.add('id_card')
    
    # 银行卡号（16-19位连续数字）
    bank_card_pattern = r'(?<!\d)\d{16,19}(?!\d)'
    if re.search(bank_card_pattern, result):
        result = re.sub(bank_card_pattern, lambda m: mask_bank_card(m.group(), mask_char=mask_char), result)
        detected_types.add('bank_card')
    
    # IPv4
    ipv4_pattern = r'(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)'
    if re.search(ipv4_pattern, result):
        result = re.sub(ipv4_pattern, lambda m: mask_ip(m.group(), mask_char=mask_char[0]), result)
        detected_types.add('ip')
    
    return result, list(detected_types)


# 便捷函数：批量掩码
def batch_mask(data: dict, rules: dict, mask_char: str = "*") -> dict:
    """
    根据规则批量掩码字典数据
    
    Args:
        data: 原始数据字典
        rules: 掩码规则，key 为字段名，value 为掩码类型
               类型: 'email', 'phone', 'id_card', 'bank_card', 'name', 'address', 'ip', 'password'
        mask_char: 掩码字符
    
    Returns:
        掩码后的数据字典
        
    Examples:
        >>> data = {"email": "user@example.com", "phone": "13812345678"}
        >>> rules = {"email": "email", "phone": "phone"}
        >>> batch_mask(data, rules)
        {'email': 'us**@*****.com', 'phone': '138****5678'}
    """
    mask_functions = {
        'email': mask_email,
        'phone': mask_phone,
        'id_card': mask_id_card,
        'bank_card': mask_bank_card,
        'name': mask_name,
        'address': mask_address,
        'ip': mask_ip,
        'password': mask_password,
    }
    
    result = data.copy()
    for field, mask_type in rules.items():
        if field in result and mask_type in mask_functions:
            result[field] = mask_functions[mask_type](result[field], mask_char=mask_char)
    
    return result


if __name__ == "__main__":
    # 演示
    print("=" * 50)
    print("Mask Utils 演示")
    print("=" * 50)
    
    print(f"\n邮箱: {mask_email('user@example.com')}")
    print(f"手机: {mask_phone('13812345678')}")
    print(f"身份证: {mask_id_card('110101199001011234')}")
    print(f"银行卡: {mask_bank_card('6222021234567890123')}")
    print(f"信用卡: {mask_credit_card('4532015112830366')}")
    print(f"姓名(中): {mask_name('张三')}")
    print(f"姓名(英): {mask_name('John Smith')}")
    print(f"地址: {mask_address('北京市朝阳区建国路88号SOHO现代城A座1001')}")
    print(f"IP: {mask_ip('192.168.1.100')}")
    print(f"密码: {mask_password('MySecret123!')}")
    
    print("\n" + "=" * 50)
    print("自动检测演示:")
    text = "用户邮箱: admin@company.com，手机: 13912345678，身份证: 310101199001011234"
    masked, types = detect_and_mask(text)
    print(f"原文: {text}")
    print(f"掩码: {masked}")
    print(f"检测类型: {types}")
    
    print("\n" + "=" * 50)
    print("批量掩码演示:")
    data = {"email": "test@example.com", "phone": "13812345678", "name": "张三"}
    rules = {"email": "email", "phone": "phone", "name": "name"}
    print(f"原始: {data}")
    print(f"掩码: {batch_mask(data, rules)}")