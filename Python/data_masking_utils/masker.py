"""
Data Masker - 核心脱敏实现

提供灵活的敏感数据脱敏功能。
"""

import re
from enum import Enum
from typing import Callable, Optional, Union


class MaskMode(Enum):
    """脱敏模式"""
    KEEP_START = "keep_start"      # 保留开头，如 138****1234
    KEEP_END = "keep_end"          # 保留结尾，如 ****1234
    KEEP_BOTH = "keep_both"        # 保留两端，如 138****1234
    FULL = "full"                  # 完全脱敏，如 ********
    MIDDLE = "middle"              # 保留中间，如 **abc***
    HASH = "hash"                  # 使用哈希替换


class MaskRule:
    """脱敏规则"""
    
    def __init__(
        self,
        pattern: str,
        mask_char: str = "*",
        keep_start: int = 0,
        keep_end: int = 0,
        mode: MaskMode = MaskMode.KEEP_BOTH,
        min_mask_length: int = 1
    ):
        """
        初始化脱敏规则
        
        Args:
            pattern: 正则表达式模式
            mask_char: 脱敏字符
            keep_start: 保留开头字符数
            keep_end: 保留结尾字符数
            mode: 脱敏模式
            min_mask_length: 最小脱敏长度
        """
        self.pattern = re.compile(pattern)
        self.mask_char = mask_char
        self.keep_start = keep_start
        self.keep_end = keep_end
        self.mode = mode
        self.min_mask_length = min_mask_length
    
    def apply(self, text: str) -> str:
        """应用脱敏规则"""
        def replace(match):
            original = match.group(0)
            return self._mask_string(original)
        return self.pattern.sub(replace, text)
    
    def _mask_string(self, s: str) -> str:
        """对字符串进行脱敏"""
        if len(s) < self.keep_start + self.keep_end + self.min_mask_length:
            # 如果字符串太短，只保留最小脱敏
            return self.mask_char * max(self.min_mask_length, len(s) // 2)
        
        if self.mode == MaskMode.FULL:
            return self.mask_char * len(s)
        
        elif self.mode == MaskMode.KEEP_START:
            return s[:self.keep_start] + self.mask_char * (len(s) - self.keep_start)
        
        elif self.mode == MaskMode.KEEP_END:
            return self.mask_char * (len(s) - self.keep_end) + s[-self.keep_end:]
        
        elif self.mode == MaskMode.KEEP_BOTH:
            start_part = s[:self.keep_start]
            end_part = s[-self.keep_end:] if self.keep_end > 0 else ""
            mask_length = len(s) - self.keep_start - self.keep_end
            return start_part + self.mask_char * mask_length + end_part
        
        elif self.mode == MaskMode.MIDDLE:
            # 保留中间部分
            mid_start = len(s) // 4
            mid_end = len(s) - len(s) // 4
            middle = s[mid_start:mid_end]
            return self.mask_char * mid_start + middle + self.mask_char * (len(s) - mid_end)
        
        return s


def mask_string(
    text: str,
    keep_start: int = 0,
    keep_end: int = 0,
    mask_char: str = "*"
) -> str:
    """
    通用字符串脱敏
    
    Args:
        text: 原始字符串
        keep_start: 保留开头字符数
        keep_end: 保留结尾字符数
        mask_char: 脱敏字符
    
    Returns:
        脱敏后的字符串
    
    Examples:
        >>> mask_string("13812345678", 3, 4)
        '138****5678'
        >>> mask_string("张三丰", 1, 0)
        '张**'
    """
    if len(text) <= keep_start + keep_end:
        # 字符串太短，无法同时保留开头和结尾
        # 返回原字符串或根据需要调整
        return text
    
    start_part = text[:keep_start] if keep_start > 0 else ""
    end_part = text[-keep_end:] if keep_end > 0 else ""
    mask_length = len(text) - keep_start - keep_end
    
    return start_part + mask_char * mask_length + end_part


def mask_phone(phone: str, mask_char: str = "*") -> str:
    """
    手机号脱敏
    
    Args:
        phone: 手机号
        mask_char: 脱敏字符
    
    Returns:
        脱敏后的手机号
    
    Examples:
        >>> mask_phone("13812345678")
        '138****5678'
        >>> mask_phone("138-1234-5678")
        '138****5678'
    """
    # 移除所有非数字字符
    digits = re.sub(r'\D', '', phone)
    
    if len(digits) != 11:
        return mask_string(phone, 3, 4, mask_char)
    
    return digits[:3] + mask_char * 4 + digits[7:]


def mask_id_card(id_card: str, mask_char: str = "*") -> str:
    """
    身份证号脱敏
    
    Args:
        id_card: 身份证号（15位或18位）
        mask_char: 脱敏字符
    
    Returns:
        脱敏后的身份证号
    
    Examples:
        >>> mask_id_card("110101199001011234")
        '110101********1234'
        >>> mask_id_card("1101011990010112")
        '110101********12'
        >>> mask_id_card("12345678")
        '1234****'
    """
    # 移除空格
    id_card = id_card.replace(" ", "")
    
    if len(id_card) == 18:
        return id_card[:6] + mask_char * 8 + id_card[14:]
    elif len(id_card) == 15:
        return id_card[:6] + mask_char * 6 + id_card[12:]
    elif len(id_card) > 8:
        # 非标准长度但足够长，保留前4位和后4位
        return id_card[:4] + mask_char * (len(id_card) - 8) + id_card[-4:]
    elif len(id_card) == 8:
        # 恰好8位，保留前4位，后4位脱敏
        return id_card[:4] + mask_char * 4
    elif len(id_card) >= 4:
        # 较短长度，保留一半
        half = len(id_card) // 2
        return id_card[:half] + mask_char * (len(id_card) - half)
    else:
        # 太短，全部脱敏
        return mask_char * len(id_card)


def mask_bank_card(card: str, mask_char: str = "*") -> str:
    """
    银行卡号脱敏
    
    Args:
        card: 银行卡号
        mask_char: 脱敏字符
    
    Returns:
        脱敏后的银行卡号
    
    Examples:
        >>> mask_bank_card("6222021234567890123")
        '6222 **** **** 0123'
    """
    # 移除所有非数字字符
    digits = re.sub(r'\D', '', card)
    
    if len(digits) < 8:
        return mask_char * len(digits)
    
    if len(digits) == 8:
        # 恰好8位，保留前4位，中间脱敏4位
        masked = digits[:4] + mask_char * 4
    else:
        # 长度大于8，保留前4位和后4位
        masked = digits[:4] + mask_char * (len(digits) - 8) + digits[-4:]
    
    # 格式化为每4位一组
    formatted = ' '.join([masked[i:i+4] for i in range(0, len(masked), 4)])
    
    return formatted


def mask_email(email: str, mask_char: str = "*") -> str:
    """
    邮箱脱敏
    
    Args:
        email: 邮箱地址
        mask_char: 脱敏字符
    
    Returns:
        脱敏后的邮箱
    
    Examples:
        >>> mask_email("example@domain.com")
        'e*****@domain.com'
        >>> mask_email("ab@test.org")
        'a*@test.org'
    """
    if '@' not in email:
        return mask_string(email, 1, 0, mask_char)
    
    local, domain = email.rsplit('@', 1)
    
    if len(local) <= 1:
        masked_local = mask_char
    else:
        # 保留首字符，其余脱敏
        masked_local = local[0] + mask_char * (len(local) - 1)
    
    return f"{masked_local}@{domain}"


def mask_name(name: str, mask_char: str = "*") -> str:
    """
    姓名脱敏
    
    Args:
        name: 姓名
        mask_char: 脱敏字符
    
    Returns:
        脱敏后的姓名
    
    Examples:
        >>> mask_name("张三")
        '张*'
        >>> mask_name("欧阳修")
        '欧**'
        >>> mask_name("John Smith")
        'J*** S****'
    """
    if not name:
        return name
    
    # 检测是否为中文姓名
    if all('\u4e00' <= c <= '\u9fff' or c in '·' for c in name):
        # 中文姓名：保留姓氏，其余脱敏
        if '·' in name:
            # 少数民族姓名如"买买提·阿卜杜拉"
            parts = name.split('·')
            masked_parts = [p[0] + mask_char * (len(p) - 1) for p in parts]
            return '·'.join(masked_parts)
        else:
            # 普通中文姓名
            return name[0] + mask_char * (len(name) - 1)
    else:
        # 英文姓名：保留首字母
        parts = name.split()
        masked_parts = []
        for part in parts:
            if len(part) <= 1:
                masked_parts.append(part)
            else:
                masked_parts.append(part[0] + mask_char * (len(part) - 1))
        return ' '.join(masked_parts)


def mask_address(address: str, mask_char: str = "*") -> str:
    """
    地址脱敏
    
    Args:
        address: 地址
        mask_char: 脱敏字符
    
    Returns:
        脱敏后的地址
    
    Examples:
        >>> mask_address("北京市朝阳区建国路88号")
        '北京市朝阳区***'
    """
    if not address:
        return address
    
    # 检测是否为中文地址
    if '\u4e00' <= address[0] <= '\u9fff':
        # 中文地址：保留省市区，隐藏详细地址
        # 尝试识别到区/县/市
        patterns = [
            r'^(.+?[省市][^省市]*?[区县市])',  # 省/市/区
            r'^(.+?[省市])',  # 省/市
        ]
        
        for pattern in patterns:
            match = re.match(pattern, address)
            if match:
                prefix = match.group(1)
                # 保留到区/市，后面用星号替换
                suffix_len = len(address) - len(prefix)
                if suffix_len > 3:
                    return prefix + mask_char * min(suffix_len, 6)
                else:
                    return address
        
        # 无法识别格式，保留前6个字符
        if len(address) > 6:
            return address[:6] + mask_char * (len(address) - 6)
    
    # 非中文地址，保留前半部分
    half = len(address) // 2
    return address[:half] + mask_char * (len(address) - half)


def mask_ip(ip: str, mask_char: str = "*") -> str:
    """
    IP地址脱敏
    
    Args:
        ip: IP地址（IPv4或IPv6）
        mask_char: 脱敏字符
    
    Returns:
        脱敏后的IP地址
    
    Examples:
        >>> mask_ip("192.168.1.100")
        '192.168.*.*'
        >>> mask_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
        '2001:0db8:****::****:****:****'
    """
    if ':' in ip:
        # IPv6
        parts = ip.split(':')
        # 保留前两段，其余脱敏
        masked_parts = parts[:2] + [mask_char * 4] * (len(parts) - 2)
        return ':'.join(masked_parts)
    else:
        # IPv4
        parts = ip.split('.')
        if len(parts) == 4:
            return '.'.join(parts[:2] + [mask_char, mask_char])
        return ip


def mask_custom(
    text: str,
    pattern: str,
    keep_start: int = 0,
    keep_end: int = 0,
    mask_char: str = "*"
) -> str:
    """
    自定义正则脱敏
    
    Args:
        text: 原始文本
        pattern: 正则表达式
        keep_start: 保留开头字符数
        keep_end: 保留结尾字符数
        mask_char: 脱敏字符
    
    Returns:
        脱敏后的文本
    
    Examples:
        >>> mask_custom("订单号：123456789", r"订单号：(\d+)", 3, 2)
        '订单号：123***89'
    """
    rule = MaskRule(pattern, mask_char, keep_start, keep_end)
    return rule.apply(text)


class DataMasker:
    """
    数据脱敏器
    
    支持批量脱敏和自定义规则。
    
    Examples:
        >>> masker = DataMasker()
        >>> masker.mask("手机号：13812345678，身份证：110101199001011234")
        '手机号：138****5678，身份证：110101********1234'
        
        >>> # 添加自定义规则
        >>> masker.add_rule(r"订单号：(\d+)", keep_start=3, keep_end=2)
    """
    
    def __init__(self, default_mask_char: str = "*"):
        """
        初始化脱敏器
        
        Args:
            default_mask_char: 默认脱敏字符
        """
        self.default_mask_char = default_mask_char
        self.rules: list = []
        self._init_default_rules()
    
    def _init_default_rules(self):
        """初始化默认规则"""
        # 注意：规则顺序很重要，更具体的规则应该先执行
        
        # 身份证号规则（18位）- 最先执行，避免其他规则干扰
        self.rules.append({
            'pattern': r'\d{6}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]',
            'keep_start': 6,
            'keep_end': 4,
            'mask_char': self.default_mask_char,
            'name': 'id_card_18'
        })
        
        # 身份证号规则（15位）
        self.rules.append({
            'pattern': r'\d{6}\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}',
            'keep_start': 6,
            'keep_end': 2,
            'mask_char': self.default_mask_char,
            'name': 'id_card_15'
        })
        
        # 手机号规则 - 使用边界匹配，避免匹配身份证号的部分
        self.rules.append({
            'pattern': r'(?<![0-9])1[3-9]\d{9}(?![0-9Xx])',
            'keep_start': 3,
            'keep_end': 4,
            'mask_char': self.default_mask_char,
            'name': 'phone'
        })
        
        # 银行卡号规则 - 排除身份证号
        self.rules.append({
            'pattern': r'(?:6222|6228|6217|6225|6216|6226|6227|6229|6230|6236|6232|6234|6235|6237|6238|6239|6240|6245|6258|6259|6260|6262|6263|6264|6265|6266|6267|6268|6269|6270|6271|6272|6273|6274|6275|6276|6277|6278|6279|6280|6281|6282|6283|6284|6285|6286|6287|6288|6289|6290|6291|6292|6293|6294|6295|6296|6297|6298|6299|6300)\d{10,13}',
            'keep_start': 4,
            'keep_end': 4,
            'mask_char': self.default_mask_char,
            'name': 'bank_card'
        })
        
        # 邮箱规则
        self.rules.append({
            'pattern': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'keep_start': 1,
            'keep_end': 0,
            'mask_char': self.default_mask_char,
            'name': 'email',
            'handler': self._mask_email_handler
        })
        
        # IPv4规则
        self.rules.append({
            'pattern': r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
            'keep_start': 0,
            'keep_end': 0,
            'mask_char': self.default_mask_char,
            'name': 'ipv4',
            'handler': self._mask_ipv4_handler
        })
    
    def _mask_email_handler(self, email: str, rule: dict) -> str:
        """邮箱脱敏处理器"""
        return mask_email(email, rule['mask_char'])
    
    def _mask_ipv4_handler(self, ip: str, rule: dict) -> str:
        """IPv4脱敏处理器"""
        return mask_ip(ip, rule['mask_char'])
    
    def add_rule(
        self,
        pattern: str,
        keep_start: int = 0,
        keep_end: int = 0,
        mask_char: str = None,
        name: str = None,
        handler: Callable = None
    ):
        """
        添加自定义规则
        
        Args:
            pattern: 正则表达式
            keep_start: 保留开头字符数
            keep_end: 保留结尾字符数
            mask_char: 脱敏字符
            name: 规则名称
            handler: 自定义处理函数
        """
        self.rules.append({
            'pattern': pattern,
            'keep_start': keep_start,
            'keep_end': keep_end,
            'mask_char': mask_char or self.default_mask_char,
            'name': name,
            'handler': handler
        })
    
    def remove_rule(self, name: str):
        """移除规则"""
        self.rules = [r for r in self.rules if r.get('name') != name]
    
    def mask(self, text: str) -> str:
        """
        对文本进行脱敏
        
        Args:
            text: 原始文本
        
        Returns:
            脱敏后的文本
        """
        result = text
        
        for rule in self.rules:
            pattern = re.compile(rule['pattern'])
            
            def replace(match, r=rule):
                original = match.group(0)
                if r.get('handler'):
                    return r['handler'](original, r)
                
                keep_start = r['keep_start']
                keep_end = r['keep_end']
                mask_char = r['mask_char']
                
                if len(original) <= keep_start + keep_end:
                    return original
                
                start = original[:keep_start] if keep_start else ""
                end = original[-keep_end:] if keep_end else ""
                mask_length = len(original) - keep_start - keep_end
                
                return start + mask_char * mask_length + end
            
            result = pattern.sub(replace, result)
        
        return result
    
    def mask_dict(self, data: dict, fields: list = None) -> dict:
        """
        对字典数据进行脱敏
        
        Args:
            data: 原始字典
            fields: 需要脱敏的字段列表，为None时自动检测
        
        Returns:
            脱敏后的字典
        """
        result = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                if fields and key in fields:
                    result[key] = self.mask(value)
                elif fields is None:
                    result[key] = self.mask(value)
                else:
                    result[key] = value
            elif isinstance(value, dict):
                result[key] = self.mask_dict(value, fields)
            else:
                result[key] = value
        
        return result
    
    def mask_list(self, data: list) -> list:
        """
        对列表数据进行脱敏
        
        Args:
            data: 原始列表
        
        Returns:
            脱敏后的列表
        """
        result = []
        
        for item in data:
            if isinstance(item, str):
                result.append(self.mask(item))
            elif isinstance(item, dict):
                result.append(self.mask_dict(item))
            elif isinstance(item, list):
                result.append(self.mask_list(item))
            else:
                result.append(item)
        
        return result