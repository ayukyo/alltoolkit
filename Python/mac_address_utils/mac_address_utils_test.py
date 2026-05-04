"""
MAC Address Utilities 测试文件

测试所有 MAC 地址处理功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mac_address_utils.mod import (
    validate,
    normalize,
    to_colon_format,
    to_hyphen_format,
    to_dot_format,
    to_no_separator_format,
    get_oui,
    lookup_vendor,
    is_multicast,
    is_unicast,
    is_broadcast,
    is_locally_administered,
    is_globally_unique,
    generate_random,
    generate_random_multicast,
    increment,
    decrement,
    compare,
    is_equal,
    get_type_info,
    parse,
    from_bytes,
    from_integer,
    to_integer,
    generate_range,
    get_ip_multicast_mac,
    get_ipv6_multicast_mac,
    mask_mac,
    list_vendors,
)


def test_validate():
    """测试 MAC 地址验证"""
    # 有效格式
    assert validate("00:11:22:33:44:55") == True
    assert validate("00-11-22-33-44-55") == True
    assert validate("001122334455") == True
    assert validate("0011.2233.4455") == True
    
    # 大小写不敏感
    assert validate("aa:bb:cc:dd:ee:ff") == True
    assert validate("AA:BB:CC:DD:EE:FF") == True
    
    # 无效格式
    assert validate("") == False
    assert validate("invalid") == False
    assert validate("00:11:22:33:44") == False  # 太短
    assert validate("00:11:22:33:44:55:66") == False  # 太长
    assert validate("GG:HH:II:JJ:KK:LL") == False  # 无效字符
    assert validate("00:11:22:33:44:5G") == False  # 无效字符
    
    print("✓ validate() 测试通过")


def test_normalize():
    """测试 MAC 地址标准化"""
    assert normalize("00:11:22:33:44:55") == "00:11:22:33:44:55"
    assert normalize("00-11-22-33-44-55") == "00:11:22:33:44:55"
    assert normalize("001122334455") == "00:11:22:33:44:55"
    assert normalize("0011.2233.4455") == "00:11:22:33:44:55"
    assert normalize("aa:bb:cc:dd:ee:ff") == "AA:BB:CC:DD:EE:FF"
    
    # 无效地址应抛出异常
    try:
        normalize("invalid")
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("✓ normalize() 测试通过")


def test_format_conversions():
    """测试格式转换"""
    mac = "00:11:22:33:44:55"
    
    assert to_colon_format(mac) == "00:11:22:33:44:55"
    assert to_hyphen_format(mac) == "00-11-22-33-44-55"
    assert to_dot_format(mac) == "0011.2233.4455"
    assert to_no_separator_format(mac) == "001122334455"
    
    # 测试不同输入格式
    assert to_colon_format("00-11-22-33-44-55") == "00:11:22:33:44:55"
    assert to_hyphen_format("001122334455") == "00-11-22-33-44-55"
    
    print("✓ 格式转换测试通过")


def test_oui_and_vendor():
    """测试 OUI 和厂商查询"""
    assert get_oui("00:11:22:33:44:55") == "00:11:22"
    
    # 厂商查询
    assert lookup_vendor("00:03:93:AB:CD:EF") == "Apple"
    assert lookup_vendor("00:0D:3A:12:34:56") == "Microsoft"
    assert lookup_vendor("00:0C:29:AB:CD:EF") == "VMware"
    assert lookup_vendor("52:54:00:12:34:56") == "QEMU/KVM"
    
    # 未知厂商
    assert lookup_vendor("DE:AD:BE:EF:CA:FE") is None
    
    print("✓ OUI 和厂商查询测试通过")


def test_multicast_unicast():
    """测试多播/单播判断"""
    # 多播地址
    assert is_multicast("01:00:5E:00:00:01") == True  # IPv4 多播
    assert is_multicast("33:33:FF:00:00:01") == True  # IPv6 多播
    assert is_multicast("FF:FF:FF:FF:FF:FF") == True  # 广播也是多播
    
    # 单播地址
    assert is_multicast("00:11:22:33:44:55") == False
    assert is_unicast("00:11:22:33:44:55") == True
    assert is_unicast("01:00:5E:00:00:01") == False
    
    print("✓ 多播/单播判断测试通过")


def test_broadcast():
    """测试广播地址判断"""
    assert is_broadcast("FF:FF:FF:FF:FF:FF") == True
    assert is_broadcast("ff:ff:ff:ff:ff:ff") == True  # 大小写不敏感
    assert is_broadcast("00:11:22:33:44:55") == False
    
    print("✓ 广播地址判断测试通过")


def test_locally_administered():
    """测试本地管理地址判断"""
    # 本地管理地址 (第二位是2, 6, A, E 等)
    assert is_locally_administered("02:11:22:33:44:55") == True
    assert is_locally_administered("06:11:22:33:44:55") == True
    assert is_locally_administered("0A:11:22:33:44:55") == True
    assert is_locally_administered("0E:11:22:33:44:55") == True
    
    # 全局唯一地址
    assert is_locally_administered("00:11:22:33:44:55") == False
    assert is_globally_unique("00:11:22:33:44:55") == True
    
    print("✓ 本地管理地址判断测试通过")


def test_generate_random():
    """测试随机 MAC 地址生成"""
    # 随机 MAC
    mac1 = generate_random()
    assert validate(mac1) == True
    
    mac2 = generate_random()
    assert mac1 != mac2  # 应该不同
    
    # 指定厂商
    apple_mac = generate_random(vendor="Apple")
    assert lookup_vendor(apple_mac) == "Apple"
    
    vmware_mac = generate_random(vendor="VMware")
    assert lookup_vendor(vmware_mac) == "VMware"
    
    # 本地管理地址
    local_mac = generate_random(locally_administered=True)
    assert is_locally_administered(local_mac) == True
    
    # 未知厂商
    try:
        generate_random(vendor="UnknownVendor")
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("✓ 随机 MAC 地址生成测试通过")


def test_generate_random_multicast():
    """测试随机多播 MAC 地址生成"""
    for _ in range(10):
        mac = generate_random_multicast()
        assert validate(mac) == True
        assert is_multicast(mac) == True
    
    print("✓ 随机多播 MAC 地址生成测试通过")


def test_increment_decrement():
    """测试递增和递减"""
    # 基本递增
    assert increment("00:11:22:33:44:55") == "00:11:22:33:44:56"
    assert increment("00:11:22:33:44:FF") == "00:11:22:33:45:00"
    assert increment("00:11:22:33:44:FF", 2) == "00:11:22:33:45:01"
    
    # 基本递减
    assert decrement("00:11:22:33:44:55") == "00:11:22:33:44:54"
    assert decrement("00:11:22:33:45:00") == "00:11:22:33:44:FF"
    
    # 溢出检查
    try:
        increment("FF:FF:FF:FF:FF:FF")
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    try:
        decrement("00:00:00:00:00:00")
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("✓ 递增和递减测试通过")


def test_compare():
    """测试比较"""
    assert compare("00:11:22:33:44:55", "00:11:22:33:44:56") == -1
    assert compare("00:11:22:33:44:55", "00:11:22:33:44:55") == 0
    assert compare("00:11:22:33:44:56", "00:11:22:33:44:55") == 1
    
    # 不同格式比较
    assert compare("00:11:22:33:44:55", "00-11-22-33-44-55") == 0
    assert compare("00:11:22:33:44:55", "001122334455") == 0
    
    print("✓ 比较测试通过")


def test_is_equal():
    """测试相等判断"""
    assert is_equal("00:11:22:33:44:55", "00:11:22:33:44:55") == True
    assert is_equal("00:11:22:33:44:55", "00-11-22-33-44-55") == True
    assert is_equal("00:11:22:33:44:55", "001122334455") == True
    assert is_equal("00:11:22:33:44:55", "0011.2233.4455") == True
    assert is_equal("00:11:22:33:44:55", "00:11:22:33:44:56") == False
    
    # 无效地址
    assert is_equal("invalid", "00:11:22:33:44:55") == False
    
    print("✓ 相等判断测试通过")


def test_get_type_info():
    """测试类型信息获取"""
    info = get_type_info("00:11:22:33:44:55")
    assert info['is_multicast'] == False
    assert info['is_unicast'] == True
    assert info['is_broadcast'] == False
    assert info['is_locally_administered'] == False
    assert info['is_globally_unique'] == True
    
    info = get_type_info("FF:FF:FF:FF:FF:FF")
    assert info['is_broadcast'] == True
    assert info['is_multicast'] == True
    
    info = get_type_info("01:00:5E:00:00:01")
    assert info['is_multicast'] == True
    
    print("✓ 类型信息获取测试通过")


def test_parse():
    """测试解析"""
    assert parse("00:11:22:33:44:55") == (0, 17, 34, 51, 68, 85)
    assert parse("FF:FF:FF:FF:FF:FF") == (255, 255, 255, 255, 255, 255)
    assert parse("00:00:00:00:00:00") == (0, 0, 0, 0, 0, 0)
    
    print("✓ 解析测试通过")


def test_from_bytes():
    """测试从字节构建"""
    assert from_bytes(0, 17, 34, 51, 68, 85) == "00:11:22:33:44:55"
    assert from_bytes(255, 255, 255, 255, 255, 255) == "FF:FF:FF:FF:FF:FF"
    
    # 超出范围
    try:
        from_bytes(0, 0, 0, 0, 0, 256)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("✓ 从字节构建测试通过")


def test_integer_conversion():
    """测试整数转换"""
    mac = "00:11:22:33:44:55"
    value = to_integer(mac)
    assert value == 0x1122334455
    
    # 往返转换
    assert from_integer(value) == mac
    
    # 边界值
    assert to_integer("00:00:00:00:00:00") == 0
    assert to_integer("FF:FF:FF:FF:FF:FF") == 0xFFFFFFFFFFFF
    
    # 超出范围
    try:
        from_integer(-1)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    try:
        from_integer(0x1000000000000)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("✓ 整数转换测试通过")


def test_generate_range():
    """测试生成 MAC 地址范围"""
    macs = generate_range("00:11:22:33:44:50", 5)
    assert len(macs) == 5
    assert macs[0] == "00:11:22:33:44:50"
    assert macs[4] == "00:11:22:33:44:54"
    
    # 测试进位
    macs = generate_range("00:11:22:33:44:FE", 5)
    assert macs[0] == "00:11:22:33:44:FE"
    assert macs[1] == "00:11:22:33:44:FF"
    assert macs[2] == "00:11:22:33:45:00"
    
    print("✓ 生成 MAC 地址范围测试通过")


def test_ip_multicast_mac():
    """测试 IPv4 多播 MAC 地址转换"""
    assert get_ip_multicast_mac("224.0.0.1") == "01:00:5E:00:00:01"
    assert get_ip_multicast_mac("239.255.255.250") == "01:00:5E:7F:FF:FA"
    assert get_ip_multicast_mac("239.0.0.1") == "01:00:5E:00:00:01"
    
    # 非 IPv4 多播地址
    try:
        get_ip_multicast_mac("192.168.1.1")
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    # 无效 IP
    try:
        get_ip_multicast_mac("invalid")
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("✓ IPv4 多播 MAC 地址转换测试通过")


def test_ipv6_multicast_mac():
    """测试 IPv6 多播 MAC 地址转换"""
    assert get_ipv6_multicast_mac("ff02::1") == "33:33:00:00:00:01"
    assert get_ipv6_multicast_mac("ff02::2") == "33:33:00:00:00:02"
    # ff02::1:ff00:0 展开为 ff02:0000:0000:0000:0000:0001:ff00:0000
    # 最后两个16位组是 ff00 和 0000，转换为 33:33:FF:00:00:00
    assert get_ipv6_multicast_mac("ff02::1:ff00:0") == "33:33:FF:00:00:00"
    
    # 非 IPv6 多播地址
    try:
        get_ipv6_multicast_mac("2001::1")
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("✓ IPv6 多播 MAC 地址转换测试通过")


def test_mask_mac():
    """测试 MAC 地址遮蔽"""
    assert mask_mac("00:11:22:33:44:55") == "00:11:22:**:**:**"
    assert mask_mac("00:11:22:33:44:55", "X") == "00:11:22:XX:XX:XX"
    assert mask_mac("AA:BB:CC:DD:EE:FF", "?") == "AA:BB:CC:??:??:??"
    
    print("✓ MAC 地址遮蔽测试通过")


def test_list_vendors():
    """测试厂商列表"""
    vendors = list_vendors()
    assert len(vendors) > 0
    assert "Apple" in vendors
    assert "Microsoft" in vendors
    assert "Google" in vendors
    assert "Samsung" in vendors
    
    # 确保排序
    assert vendors == sorted(vendors)
    
    print("✓ 厂商列表测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("MAC Address Utilities 测试")
    print("=" * 50)
    
    test_validate()
    test_normalize()
    test_format_conversions()
    test_oui_and_vendor()
    test_multicast_unicast()
    test_broadcast()
    test_locally_administered()
    test_generate_random()
    test_generate_random_multicast()
    test_increment_decrement()
    test_compare()
    test_is_equal()
    test_get_type_info()
    test_parse()
    test_from_bytes()
    test_integer_conversion()
    test_generate_range()
    test_ip_multicast_mac()
    test_ipv6_multicast_mac()
    test_mask_mac()
    test_list_vendors()
    
    print("=" * 50)
    print("所有测试通过! ✓")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()