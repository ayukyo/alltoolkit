"""
MAC Address Utilities - MAC地址处理工具

功能:
- 验证 MAC 地址格式
- MAC 地址格式转换（冒号、连字符、点号、无分隔符）
- 厂商 OUI 查询
- 随机 MAC 地址生成
- 多播/单播地址判断
- 本地/全局地址判断
- MAC 地址递增/递减
- MAC 地址比较

零依赖实现
"""

import re
from typing import Optional, Tuple, List, Dict

# OUI 前缀数据（常用厂商）
OUI_PREFIXES: Dict[str, str] = {
    # Apple
    "00:03:93": "Apple",
    "00:05:02": "Apple",
    "00:0A:27": "Apple",
    "00:0A:95": "Apple",
    "00:0D:93": "Apple",
    "00:11:24": "Apple",
    "00:14:51": "Apple",
    "00:16:CB": "Apple",
    "00:17:F2": "Apple",
    "00:19:E3": "Apple",
    "00:1B:63": "Apple",
    "00:1C:B3": "Apple",
    "00:1D:4F": "Apple",
    "00:1E:52": "Apple",
    "00:1E:C2": "Apple",
    "00:1F:5B": "Apple",
    "00:1F:F3": "Apple",
    "00:22:41": "Apple",
    "00:23:12": "Apple",
    "00:23:32": "Apple",
    "00:23:6C": "Apple",
    "00:23:DF": "Apple",
    "00:24:36": "Apple",
    "00:25:00": "Apple",
    "00:25:4B": "Apple",
    "00:25:BC": "Apple",
    "00:26:08": "Apple",
    "00:26:4A": "Apple",
    "00:26:B0": "Apple",
    "00:26:BB": "Apple",
    "00:30:65": "Apple",
    # Microsoft
    "00:01:C8": "Microsoft",
    "00:03:FF": "Microsoft",
    "00:0D:3A": "Microsoft",
    "00:0F:B0": "Microsoft",
    "00:12:5A": "Microsoft",
    "00:13:02": "Microsoft",
    "00:14:38": "Microsoft",
    "00:15:5D": "Microsoft",
    "00:16:4E": "Microsoft",
    "00:17:FA": "Microsoft",
    "00:18:71": "Microsoft",
    "00:1A:A0": "Microsoft",
    "00:1C:42": "Microsoft",
    "00:1D:D8": "Microsoft",
    "00:21:CC": "Microsoft",
    "00:22:48": "Microsoft",
    "00:24:7B": "Microsoft",
    "00:25:AE": "Microsoft",
    "00:50:F2": "Microsoft",
    # Google
    "00:02:5E": "Google",
    "00:08:74": "Google",
    "00:0A:EC": "Google",
    "00:12:A8": "Google",
    "00:14:A7": "Google",
    "00:15:99": "Google",
    "00:16:3E": "Google",
    "00:18:82": "Google",
    "00:1A:11": "Google",
    "00:1B:21": "Google",
    "00:1D:D9": "Google",
    "00:1E:68": "Google",
    "00:22:6B": "Google",
    "00:25:90": "Google",
    "00:26:90": "Google",
    "F0:9F:C2": "Google",
    "74:AC:B9": "Google",
    "94:EB:2F": "Google",
    "D8:1C:79": "Google",
    # Samsung
    "00:00:F0": "Samsung",
    "00:07:AB": "Samsung",
    "00:0D:E5": "Samsung",
    "00:12:FB": "Samsung",
    "00:13:77": "Samsung",
    "00:14:A5": "Samsung",
    "00:15:AF": "Samsung",
    "00:16:6B": "Samsung",
    "00:17:C2": "Samsung",
    "00:18:AF": "Samsung",
    "00:19:15": "Samsung",
    "00:1A:8A": "Samsung",
    "00:1B:59": "Samsung",
    "00:1C:62": "Samsung",
    "00:1D:1F": "Samsung",
    "00:1E:7D": "Samsung",
    "00:1F:35": "Samsung",
    "00:21:F1": "Samsung",
    "00:22:43": "Samsung",
    "00:23:39": "Samsung",
    "00:24:90": "Samsung",
    "00:25:38": "Samsung",
    "00:26:37": "Samsung",
    # Cisco
    "00:00:0C": "Cisco",
    "00:00:1A": "Cisco",
    "00:00:40": "Cisco",
    "00:00:46": "Cisco",
    "00:00:5A": "Cisco",
    "00:00:5E": "Cisco",
    "00:00:6A": "Cisco",
    "00:00:79": "Cisco",
    "00:00:8A": "Cisco",
    "00:00:93": "Cisco",
    "00:00:AB": "Cisco",
    "00:00:B4": "Cisco",
    "00:00:C5": "Cisco",
    "00:00:C7": "Cisco",
    "00:00:D0": "Cisco",
    "00:00:E2": "Cisco",
    "00:00:F2": "Cisco",
    "00:01:42": "Cisco",
    "00:01:63": "Cisco",
    "00:01:96": "Cisco",
    "00:01:C7": "Cisco",
    "00:01:C9": "Cisco",
    # Intel
    "00:02:B3": "Intel",
    "00:03:47": "Intel",
    "00:04:23": "Intel",
    "00:07:32": "Intel",
    "00:08:74": "Intel",
    "00:08:9B": "Intel",
    "00:09:6B": "Intel",
    "00:0B:DB": "Intel",
    "00:0C:F1": "Intel",
    "00:0D:56": "Intel",
    "00:0D:60": "Intel",
    "00:0E:0C": "Intel",
    "00:0E:35": "Intel",
    "00:0E:A6": "Intel",
    "00:0F:1F": "Intel",
    "00:10:FA": "Intel",
    "00:11:09": "Intel",
    "00:11:11": "Intel",
    "00:12:F0": "Intel",
    "00:13:20": "Intel",
    # Dell
    "00:01:C6": "Dell",
    "00:06:5B": "Dell",
    "00:08:74": "Dell",
    "00:0B:DB": "Dell",
    "00:0D:56": "Dell",
    "00:0E:0C": "Dell",
    "00:0F:1F": "Dell",
    "00:10:FA": "Dell",
    "00:11:09": "Dell",
    "00:12:3F": "Dell",
    "00:13:72": "Dell",
    "00:14:22": "Dell",
    "00:15:C5": "Dell",
    "00:16:76": "Dell",
    "00:17:A4": "Dell",
    "00:18:8B": "Dell",
    "00:19:B9": "Dell",
    "00:1A:A0": "Dell",
    "00:1B:38": "Dell",
    "00:1C:23": "Dell",
    # HP/Hewlett-Packard
    "00:00:09": "HP",
    "00:01:E6": "HP",
    "00:01:E7": "HP",
    "00:04:EA": "HP",
    "00:05:1B": "HP",
    "00:06:5B": "HP",
    "00:07:7D": "HP",
    "00:08:02": "HP",
    "00:09:6B": "HP",
    "00:0A:57": "HP",
    "00:0B:13": "HP",
    "00:0C:0E": "HP",
    "00:0D:9D": "HP",
    "00:0E:7E": "HP",
    "00:0F:20": "HP",
    "00:10:83": "HP",
    "00:11:0A": "HP",
    "00:12:41": "HP",
    "00:13:21": "HP",
    "00:14:38": "HP",
    # Huawei
    "00:00:5E": "Huawei",
    "00:0B:6B": "Huawei",
    "00:0E:0C": "Huawei",
    "00:0E:3A": "Huawei",
    "00:0F:7D": "Huawei",
    "00:10:F3": "Huawei",
    "00:11:25": "Huawei",
    "00:12:43": "Huawei",
    "00:13:1D": "Huawei",
    "00:14:5E": "Huawei",
    "00:15:65": "Huawei",
    "00:16:6A": "Huawei",
    "00:17:4D": "Huawei",
    "00:18:2D": "Huawei",
    "00:19:30": "Huawei",
    "00:1A:0D": "Huawei",
    "00:1B:10": "Huawei",
    "00:1C:14": "Huawei",
    "00:1D:0F": "Huawei",
    "00:1E:EC": "Huawei",
    # TP-Link
    "00:0A:EB": "TP-Link",
    "00:11:09": "TP-Link",
    "00:12:17": "TP-Link",
    "00:13:49": "TP-Link",
    "00:14:78": "TP-Link",
    "00:15:6D": "TP-Link",
    "00:16:01": "TP-Link",
    "00:17:31": "TP-Link",
    "00:18:4D": "TP-Link",
    "00:19:E0": "TP-Link",
    "00:1A:A0": "TP-Link",
    "00:1B:11": "TP-Link",
    "00:1C:BF": "TP-Link",
    "00:1D:0F": "TP-Link",
    "00:1E:58": "TP-Link",
    "00:1F:64": "TP-Link",
    "00:21:27": "TP-Link",
    "00:22:3F": "TP-Link",
    "00:23:54": "TP-Link",
    "00:24:01": "TP-Link",
    # Netgear
    "00:00:85": "Netgear",
    "00:00:B4": "Netgear",
    "00:01:02": "Netgear",
    "00:01:3F": "Netgear",
    "00:01:52": "Netgear",
    "00:03:52": "Netgear",
    "00:04:5A": "Netgear",
    "00:05:30": "Netgear",
    "00:06:25": "Netgear",
    "00:07:08": "Netgear",
    "00:08:2D": "Netgear",
    "00:09:5B": "Netgear",
    "00:0A:57": "Netgear",
    "00:0B:37": "Netgear",
    "00:0C:41": "Netgear",
    "00:0D:A0": "Netgear",
    "00:0E:0C": "Netgear",
    "00:0F:B5": "Netgear",
    "00:10:DD": "Netgear",
    "00:11:24": "Netgear",
    # Xiaomi
    "00:03:7F": "Xiaomi",
    "00:04:75": "Xiaomi",
    "00:05:4E": "Xiaomi",
    "00:06:1E": "Xiaomi",
    "00:07:3E": "Xiaomi",
    "00:08:22": "Xiaomi",
    "00:09:0F": "Xiaomi",
    "00:0A:12": "Xiaomi",
    "00:0B:80": "Xiaomi",
    "00:0C:6E": "Xiaomi",
    "00:0D:15": "Xiaomi",
    "00:0E:8F": "Xiaomi",
    "00:0F:6B": "Xiaomi",
    "00:10:7A": "Xiaomi",
    "00:11:8E": "Xiaomi",
    "10:E5:49": "Xiaomi",
    "28:ED:6A": "Xiaomi",
    "34:CE:00": "Xiaomi",
    "64:09:80": "Xiaomi",
    "6C:5D:43": "Xiaomi",
    "74:A3:E4": "Xiaomi",
    "7C:1D:D9": "Xiaomi",
    "88:4A:EA": "Xiaomi",
    "8C:BE:BE": "Xiaomi",
    "98:0C:82": "Xiaomi",
    "9C:2E:A1": "Xiaomi",
    "AC:1F:0D": "Xiaomi",
    # 虚拟化厂商
    "00:05:69": "VMware",
    "00:0C:29": "VMware",
    "00:0C:50": "VMware",
    "00:0E:0C": "VMware",
    "00:0F:4B": "VMware",
    "00:10:DB": "VMware",
    "00:11:25": "VMware",
    "00:12:1E": "VMware",
    "00:13:07": "VMware",
    "00:14:4F": "VMware",
    "00:15:5D": "VMware",
    "00:16:3E": "VMware",
    "00:17:A4": "VMware",
    "00:18:5E": "VMware",
    "00:19:49": "VMware",
    "00:1A:4A": "VMware",
    "00:1B:21": "VMware",
    "00:1C:42": "Parallels",
    "00:1C:50": "VirtualBox",
    "00:1D:D8": "Microsoft Hyper-V",
    "00:21:F6": "VirtualBox",
    "52:54:00": "QEMU/KVM",
    "54:52:00": "QEMU",
}


def validate(mac: str) -> bool:
    """
    验证 MAC 地址格式是否有效
    
    Args:
        mac: MAC 地址字符串
        
    Returns:
        bool: 是否有效
        
    Examples:
        >>> validate("00:11:22:33:44:55")
        True
        >>> validate("00-11-22-33-44-55")
        True
        >>> validate("001122334455")
        True
        >>> validate("0011.2233.4455")
        True
        >>> validate("invalid")
        False
    """
    if not mac:
        return False
    
    mac = mac.strip().upper()
    
    # 无分隔符格式
    if re.match(r'^[0-9A-F]{12}$', mac):
        return True
    
    # 冒号格式
    if re.match(r'^([0-9A-F]{2}:){5}[0-9A-F]{2}$', mac):
        return True
    
    # 连字符格式
    if re.match(r'^([0-9A-F]{2}-){5}[0-9A-F]{2}$', mac):
        return True
    
    # 点号格式 (Cisco)
    if re.match(r'^([0-9A-F]{4}\.){2}[0-9A-F]{4}$', mac):
        return True
    
    return False


def normalize(mac: str) -> str:
    """
    标准化 MAC 地址为冒号分隔的大写格式
    
    Args:
        mac: MAC 地址字符串
        
    Returns:
        str: 标准化后的 MAC 地址
        
    Raises:
        ValueError: MAC 地址格式无效
        
    Examples:
        >>> normalize("00-11-22-33-44-55")
        '00:11:22:33:44:55'
        >>> normalize("001122334455")
        '00:11:22:33:44:55'
        >>> normalize("0011.2233.4455")
        '00:11:22:33:44:55'
    """
    if not validate(mac):
        raise ValueError(f"Invalid MAC address: {mac}")
    
    mac = mac.strip().upper().replace(":", "").replace("-", "").replace(".", "")
    return ":".join(mac[i:i+2] for i in range(0, 12, 2))


def to_colon_format(mac: str) -> str:
    """
    转换为冒号格式 (00:11:22:33:44:55)
    
    Examples:
        >>> to_colon_format("00-11-22-33-44-55")
        '00:11:22:33:44:55'
    """
    return normalize(mac)


def to_hyphen_format(mac: str) -> str:
    """
    转换为连字符格式 (00-11-22-33-44-55)
    
    Examples:
        >>> to_hyphen_format("00:11:22:33:44:55")
        '00-11-22-33-44-55'
    """
    return normalize(mac).replace(":", "-")


def to_dot_format(mac: str) -> str:
    """
    转换为点号格式 (Cisco风格: 0011.2233.4455)
    
    Examples:
        >>> to_dot_format("00:11:22:33:44:55")
        '0011.2233.4455'
    """
    mac = normalize(mac).replace(":", "")
    return f"{mac[0:4]}.{mac[4:8]}.{mac[8:12]}"


def to_no_separator_format(mac: str) -> str:
    """
    转换为无分隔符格式 (001122334455)
    
    Examples:
        >>> to_no_separator_format("00:11:22:33:44:55")
        '001122334455'
    """
    return normalize(mac).replace(":", "")


def get_oui(mac: str) -> str:
    """
    获取 MAC 地址的 OUI (前24位/前三个八位组)
    
    Args:
        mac: MAC 地址字符串
        
    Returns:
        str: OUI 部分 (冒号格式)
        
    Examples:
        >>> get_oui("00:11:22:33:44:55")
        '00:11:22'
    """
    mac = normalize(mac)
    return ":".join(mac.split(":")[:3])


def lookup_vendor(mac: str) -> Optional[str]:
    """
    查询 MAC 地址对应的厂商名称
    
    Args:
        mac: MAC 地址字符串
        
    Returns:
        Optional[str]: 厂商名称，未找到返回 None
        
    Examples:
        >>> lookup_vendor("00:03:93:AB:CD:EF")
        'Apple'
        >>> lookup_vendor("00:0D:3A:12:34:56")
        'Microsoft'
    """
    oui = get_oui(mac)
    return OUI_PREFIXES.get(oui)


def is_multicast(mac: str) -> bool:
    """
    判断是否为多播 MAC 地址
    
    多播地址的第一个字节的最低位为1
    
    Args:
        mac: MAC 地址字符串
        
    Returns:
        bool: 是否为多播地址
        
    Examples:
        >>> is_multicast("01:00:5E:00:00:01")  # IPv4 多播
        True
        >>> is_multicast("33:33:FF:00:00:01")  # IPv6 多播
        True
        >>> is_multicast("00:11:22:33:44:55")
        False
    """
    mac = normalize(mac)
    first_byte = int(mac.split(":")[0], 16)
    return bool(first_byte & 0x01)


def is_unicast(mac: str) -> bool:
    """
    判断是否为单播 MAC 地址
    
    Args:
        mac: MAC 地址字符串
        
    Returns:
        bool: 是否为单播地址
        
    Examples:
        >>> is_unicast("00:11:22:33:44:55")
        True
        >>> is_unicast("FF:FF:FF:FF:FF:FF")
        False
    """
    return not is_multicast(mac)


def is_broadcast(mac: str) -> bool:
    """
    判断是否为广播 MAC 地址 (FF:FF:FF:FF:FF:FF)
    
    Args:
        mac: MAC 地址字符串
        
    Returns:
        bool: 是否为广播地址
        
    Examples:
        >>> is_broadcast("FF:FF:FF:FF:FF:FF")
        True
        >>> is_broadcast("00:11:22:33:44:55")
        False
    """
    return normalize(mac) == "FF:FF:FF:FF:FF:FF"


def is_locally_administered(mac: str) -> bool:
    """
    判断是否为本地管理的 MAC 地址
    
    本地管理地址的第一个字节的次低位为1
    
    Args:
        mac: MAC 地址字符串
        
    Returns:
        bool: 是否为本地管理地址
        
    Examples:
        >>> is_locally_administered("02:11:22:33:44:55")
        True
        >>> is_locally_administered("00:11:22:33:44:55")
        False
    """
    mac = normalize(mac)
    first_byte = int(mac.split(":")[0], 16)
    return bool(first_byte & 0x02)


def is_globally_unique(mac: str) -> bool:
    """
    判断是否为全局唯一的 MAC 地址
    
    全局唯一地址的第一个字节的次低位为0
    
    Args:
        mac: MAC 地址字符串
        
    Returns:
        bool: 是否为全局唯一地址
    """
    return not is_locally_administered(mac)


def generate_random(vendor: Optional[str] = None, 
                    locally_administered: bool = False) -> str:
    """
    生成随机 MAC 地址
    
    Args:
        vendor: 可选的厂商名称，使用该厂商的 OUI
        locally_administered: 是否生成本地管理地址
        
    Returns:
        str: 随机 MAC 地址
        
    Examples:
        >>> mac = generate_random()  # 随机 MAC
        >>> validate(mac)
        True
        >>> mac = generate_random(vendor="Apple")  # 使用 Apple OUI
        >>> lookup_vendor(mac)
        'Apple'
        >>> mac = generate_random(locally_administered=True)
        >>> is_locally_administered(mac)
        True
    """
    import random
    
    if vendor:
        # 查找厂商 OUI
        vendor_ouis = [oui for oui, v in OUI_PREFIXES.items() if v == vendor]
        if not vendor_ouis:
            raise ValueError(f"Unknown vendor: {vendor}")
        oui = random.choice(vendor_ouis)
        oui_parts = [int(x, 16) for x in oui.split(":")]
    else:
        oui_parts = [random.randint(0x00, 0xFF) for _ in range(3)]
    
    # 生成本地管理地址时设置次低位
    if locally_administered:
        oui_parts[0] |= 0x02
    
    # 生成本地部分 (后3个八位组)
    local_parts = [random.randint(0x00, 0xFF) for _ in range(3)]
    
    # 组合所有部分
    all_parts = oui_parts + local_parts
    return ":".join(f"{b:02X}" for b in all_parts)


def generate_random_multicast() -> str:
    """
    生成随机多播 MAC 地址
    
    Returns:
        str: 随机多播 MAC 地址
        
    Examples:
        >>> mac = generate_random_multicast()
        >>> is_multicast(mac)
        True
    """
    import random
    
    # 多播地址的第一个字节最低位为1
    # IPv4 多播使用 01:00:5E 前缀
    # 这里生成一个通用的多播地址
    first_byte = random.randint(0x01, 0xFF) | 0x01  # 确保最低位为1
    
    parts = [first_byte] + [random.randint(0x00, 0xFF) for _ in range(5)]
    return ":".join(f"{b:02X}" for b in parts)


def increment(mac: str, count: int = 1) -> str:
    """
    递增 MAC 地址
    
    Args:
        mac: MAC 地址字符串
        count: 递增数量，默认为1
        
    Returns:
        str: 递增后的 MAC 地址
        
    Raises:
        ValueError: 递增后超出范围
        
    Examples:
        >>> increment("00:11:22:33:44:55")
        '00:11:22:33:44:56'
        >>> increment("00:11:22:33:44:FF")
        '00:11:22:33:45:00'
        >>> increment("00:11:22:33:44:55", 10)
        '00:11:22:33:44:5F'
    """
    mac = normalize(mac)
    parts = [int(x, 16) for x in mac.split(":")]
    
    # 将 MAC 地址转换为整数
    value = (parts[0] << 40) | (parts[1] << 32) | (parts[2] << 24) | \
            (parts[3] << 16) | (parts[4] << 8) | parts[5]
    
    value += count
    
    if value > 0xFFFFFFFFFFFF:
        raise ValueError("MAC address increment overflow")
    
    # 转换回 MAC 地址格式
    new_parts = [
        (value >> 40) & 0xFF,
        (value >> 32) & 0xFF,
        (value >> 24) & 0xFF,
        (value >> 16) & 0xFF,
        (value >> 8) & 0xFF,
        value & 0xFF
    ]
    
    return ":".join(f"{b:02X}" for b in new_parts)


def decrement(mac: str, count: int = 1) -> str:
    """
    递减 MAC 地址
    
    Args:
        mac: MAC 地址字符串
        count: 递减数量，默认为1
        
    Returns:
        str: 递减后的 MAC 地址
        
    Raises:
        ValueError: 递减后超出范围
        
    Examples:
        >>> decrement("00:11:22:33:44:55")
        '00:11:22:33:44:54'
        >>> decrement("00:11:22:33:45:00")
        '00:11:22:33:44:FF'
    """
    mac = normalize(mac)
    parts = [int(x, 16) for x in mac.split(":")]
    
    # 将 MAC 地址转换为整数
    value = (parts[0] << 40) | (parts[1] << 32) | (parts[2] << 24) | \
            (parts[3] << 16) | (parts[4] << 8) | parts[5]
    
    value -= count
    
    if value < 0:
        raise ValueError("MAC address decrement underflow")
    
    # 转换回 MAC 地址格式
    new_parts = [
        (value >> 40) & 0xFF,
        (value >> 32) & 0xFF,
        (value >> 24) & 0xFF,
        (value >> 16) & 0xFF,
        (value >> 8) & 0xFF,
        value & 0xFF
    ]
    
    return ":".join(f"{b:02X}" for b in new_parts)


def compare(mac1: str, mac2: str) -> int:
    """
    比较两个 MAC 地址
    
    Args:
        mac1: 第一个 MAC 地址
        mac2: 第二个 MAC 地址
        
    Returns:
        int: 负数表示 mac1 < mac2，0 表示相等，正数表示 mac1 > mac2
        
    Examples:
        >>> compare("00:11:22:33:44:55", "00:11:22:33:44:56")
        -1
        >>> compare("00:11:22:33:44:55", "00:11:22:33:44:55")
        0
        >>> compare("00:11:22:33:44:56", "00:11:22:33:44:55")
        1
    """
    mac1 = normalize(mac1)
    mac2 = normalize(mac2)
    
    if mac1 < mac2:
        return -1
    elif mac1 > mac2:
        return 1
    else:
        return 0


def is_equal(mac1: str, mac2: str) -> bool:
    """
    判断两个 MAC 地址是否相等（忽略格式差异）
    
    Args:
        mac1: 第一个 MAC 地址
        mac2: 第二个 MAC 地址
        
    Returns:
        bool: 是否相等
        
    Examples:
        >>> is_equal("00:11:22:33:44:55", "00-11-22-33-44-55")
        True
        >>> is_equal("00:11:22:33:44:55", "001122334455")
        True
    """
    try:
        return normalize(mac1) == normalize(mac2)
    except ValueError:
        return False


def get_type_info(mac: str) -> Dict[str, bool]:
    """
    获取 MAC 地址的类型信息
    
    Args:
        mac: MAC 地址字符串
        
    Returns:
        Dict: 类型信息字典
        
    Examples:
        >>> info = get_type_info("01:00:5E:00:00:01")
        >>> info['is_multicast']
        True
        >>> info['is_unicast']
        False
    """
    return {
        'is_multicast': is_multicast(mac),
        'is_unicast': is_unicast(mac),
        'is_broadcast': is_broadcast(mac),
        'is_locally_administered': is_locally_administered(mac),
        'is_globally_unique': is_globally_unique(mac)
    }


def parse(mac: str) -> Tuple[int, int, int, int, int, int]:
    """
    解析 MAC 地址为六个整数字节
    
    Args:
        mac: MAC 地址字符串
        
    Returns:
        Tuple[int, int, int, int, int, int]: 六个字节值
        
    Examples:
        >>> parse("00:11:22:33:44:55")
        (0, 17, 34, 51, 68, 85)
    """
    mac = normalize(mac)
    return tuple(int(x, 16) for x in mac.split(":"))


def from_bytes(b1: int, b2: int, b3: int, b4: int, b5: int, b6: int) -> str:
    """
    从六个字节构建 MAC 地址
    
    Args:
        b1-b6: 六个字节值 (0-255)
        
    Returns:
        str: MAC 地址
        
    Raises:
        ValueError: 字节值超出范围
        
    Examples:
        >>> from_bytes(0, 17, 34, 51, 68, 85)
        '00:11:22:33:44:55'
    """
    for i, b in enumerate([b1, b2, b3, b4, b5, b6], 1):
        if not 0 <= b <= 255:
            raise ValueError(f"Byte {i} value {b} out of range (0-255)")
    
    return ":".join(f"{b:02X}" for b in [b1, b2, b3, b4, b5, b6])


def from_integer(value: int) -> str:
    """
    从整数构建 MAC 地址
    
    Args:
        value: 整数值 (0 到 0xFFFFFFFFFFFF)
        
    Returns:
        str: MAC 地址
        
    Raises:
        ValueError: 值超出范围
        
    Examples:
        >>> from_integer(0x1122334455)
        '00:00:00:11:22:33:44:55'[:17]
        '00:11:22:33:44:55'
    """
    if not 0 <= value <= 0xFFFFFFFFFFFF:
        raise ValueError(f"Value {value} out of range (0 to 281474976710655)")
    
    parts = [
        (value >> 40) & 0xFF,
        (value >> 32) & 0xFF,
        (value >> 24) & 0xFF,
        (value >> 16) & 0xFF,
        (value >> 8) & 0xFF,
        value & 0xFF
    ]
    
    return ":".join(f"{b:02X}" for b in parts)


def to_integer(mac: str) -> int:
    """
    将 MAC 地址转换为整数
    
    Args:
        mac: MAC 地址字符串
        
    Returns:
        int: 整数值
        
    Examples:
        >>> to_integer("00:11:22:33:44:55")
        73588229405
        >>> hex(to_integer("00:11:22:33:44:55"))
        '0x1122334455'
    """
    parts = parse(mac)
    return (parts[0] << 40) | (parts[1] << 32) | (parts[2] << 24) | \
           (parts[3] << 16) | (parts[4] << 8) | parts[5]


def generate_range(start_mac: str, count: int) -> List[str]:
    """
    生成连续的 MAC 地址范围
    
    Args:
        start_mac: 起始 MAC 地址
        count: 数量
        
    Returns:
        List[str]: MAC 地址列表
        
    Examples:
        >>> generate_range("00:11:22:33:44:50", 5)
        ['00:11:22:33:44:50', '00:11:22:33:44:51', '00:11:22:33:44:52', '00:11:22:33:44:53', '00:11:22:33:44:54']
    """
    if count < 0:
        raise ValueError("Count must be non-negative")
    
    result = [start_mac]
    current = start_mac
    for _ in range(count - 1):
        current = increment(current)
        result.append(current)
    
    return result


def get_ip_multicast_mac(ip_multicast: str) -> str:
    """
    将 IPv4 多播地址转换为对应的 MAC 多播地址
    
    Args:
        ip_multicast: IPv4 多播地址 (如 "239.0.0.1")
        
    Returns:
        str: 对应的 MAC 多播地址
        
    Raises:
        ValueError: 不是有效的 IPv4 多播地址
        
    Examples:
        >>> get_ip_multicast_mac("224.0.0.1")
        '01:00:5E:00:00:01'
        >>> get_ip_multicast_mac("239.255.255.250")
        '01:00:5E:7F:FF:FA'
    """
    # 解析 IP 地址
    try:
        parts = ip_multicast.split(".")
        if len(parts) != 4:
            raise ValueError("Invalid IPv4 address format")
        
        octets = [int(x) for x in parts]
        if not all(0 <= x <= 255 for x in octets):
            raise ValueError("Invalid IPv4 address")
        
        # 检查是否为多播地址 (224.0.0.0 - 239.255.255.255)
        if not (224 <= octets[0] <= 239):
            raise ValueError(f"Not a multicast IP address: {ip_multicast}")
        
        # MAC 多播地址格式: 01:00:5E:0x:xx:xx
        # 低 23 位来自 IP 地址
        mac_parts = [
            0x01,
            0x00,
            0x5E,
            octets[1] & 0x7F,  # 第4个八位组的最高位为0
            octets[2],
            octets[3]
        ]
        
        return ":".join(f"{b:02X}" for b in mac_parts)
        
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Invalid IPv4 multicast address: {ip_multicast}") from e


def get_ipv6_multicast_mac(ipv6_multicast: str) -> str:
    """
    将 IPv6 多播地址转换为对应的 MAC 多播地址
    
    Args:
        ipv6_multicast: IPv6 多播地址 (如 "ff02::1")
        
    Returns:
        str: 对应的 MAC 多播地址
        
    Raises:
        ValueError: 不是有效的 IPv6 多播地址
        
    Examples:
        >>> get_ipv6_multicast_mac("ff02::1")
        '33:33:00:00:00:01'
        >>> get_ipv6_multicast_mac("ff02::1:ff00:0")
        '33:33:00:01:FF:00'
    """
    ipv6_lower = ipv6_multicast.lower()
    
    # 检查是否为多播地址 (ff00::/8)
    if not ipv6_lower.startswith("ff"):
        raise ValueError(f"Not an IPv6 multicast address: {ipv6_multicast}")
    
    # 处理 :: 缩写，展开为完整的128位地址
    if "::" in ipv6_lower:
        parts = ipv6_lower.split("::")
        left_parts = parts[0].split(":") if parts[0] else []
        right_parts = parts[1].split(":") if len(parts) > 1 and parts[1] else []
        missing_count = 8 - len(left_parts) - len(right_parts)
        full_parts = left_parts + ["0000"] * missing_count + right_parts
    else:
        full_parts = ipv6_lower.split(":")
    
    # 确保每个部分是4位十六进制
    full_parts = [p.zfill(4) for p in full_parts]
    
    if len(full_parts) != 8:
        raise ValueError(f"Invalid IPv6 address format: {ipv6_multicast}")
    
    # 取最后32位 (最后两个16位组)
    last_group1 = full_parts[6]  # 第7个16位组
    last_group2 = full_parts[7]  # 第8个16位组
    
    # 每个16位组转换为2字节
    mac_parts = [
        0x33,
        0x33,
        int(last_group1[0:2], 16),
        int(last_group1[2:4], 16),
        int(last_group2[0:2], 16),
        int(last_group2[2:4], 16)
    ]
    
    return ":".join(f"{b:02X}" for b in mac_parts)


def mask_mac(mac: str, mask_char: str = "*") -> str:
    """
    遮蔽 MAC 地址的部分内容（用于隐私显示）
    
    Args:
        mac: MAC 地址字符串
        mask_char: 遮蔽字符，默认为 "*"
        
    Returns:
        str: 遮蔽后的 MAC 地址
        
    Examples:
        >>> mask_mac("00:11:22:33:44:55")
        '00:11:22:**:**:**'
        >>> mask_mac("00:11:22:33:44:55", "X")
        '00:11:22:XX:XX:XX'
    """
    mac = normalize(mac)
    parts = mac.split(":")
    # 显示前三组，遮蔽后三组
    masked_parts = parts[:3] + [mask_char * 2] * 3
    return ":".join(masked_parts)


def list_vendors() -> List[str]:
    """
    列出所有支持的厂商名称
    
    Returns:
        List[str]: 厂商名称列表（去重排序）
        
    Examples:
        >>> vendors = list_vendors()
        >>> 'Apple' in vendors
        True
        >>> 'Microsoft' in vendors
        True
    """
    return sorted(set(OUI_PREFIXES.values()))


# 模块信息
__version__ = "1.0.0"
__author__ = "AllToolkit"
__all__ = [
    'validate',
    'normalize',
    'to_colon_format',
    'to_hyphen_format',
    'to_dot_format',
    'to_no_separator_format',
    'get_oui',
    'lookup_vendor',
    'is_multicast',
    'is_unicast',
    'is_broadcast',
    'is_locally_administered',
    'is_globally_unique',
    'generate_random',
    'generate_random_multicast',
    'increment',
    'decrement',
    'compare',
    'is_equal',
    'get_type_info',
    'parse',
    'from_bytes',
    'from_integer',
    'to_integer',
    'generate_range',
    'get_ip_multicast_mac',
    'get_ipv6_multicast_mac',
    'mask_mac',
    'list_vendors',
    'OUI_PREFIXES',
]