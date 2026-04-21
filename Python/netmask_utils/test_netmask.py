#!/usr/bin/env python3
"""
Netmask Utilities 测试模块

测试所有核心功能。
"""

import unittest
from .core import (
    IPv4Address, IPv6Address, Subnet,
    cidr_to_mask, mask_to_cidr,
    ip_to_int, int_to_ip,
    is_valid_ipv4, is_valid_ipv6, is_valid_ip,
    parse_cidr,
    get_network_address, get_broadcast_address,
    get_first_host, get_last_host,
    get_host_count, get_host_range,
    is_ip_in_subnet,
    split_subnet, merge_subnets,
    find_smallest_subnet,
    list_available_ips,
)


class TestIPv4Address(unittest.TestCase):
    """IPv4地址测试"""
    
    def test_valid_ipv4(self):
        """测试有效IPv4地址"""
        ip = IPv4Address("192.168.1.1")
        self.assertEqual(str(ip), "192.168.1.1")
        self.assertEqual(ip.version, 4)
        
    def test_ipv4_from_int(self):
        """测试从整数创建IPv4"""
        ip = IPv4Address(3232235777)
        self.assertEqual(str(ip), "192.168.1.1")
        
    def test_ipv4_to_int(self):
        """测试IPv4转整数"""
        ip = IPv4Address("192.168.1.1")
        self.assertEqual(int(ip), 3232235777)
        
    def test_ipv4_special_addresses(self):
        """测试特殊IPv4地址"""
        self.assertEqual(str(IPv4Address("0.0.0.0")), "0.0.0.0")
        self.assertEqual(str(IPv4Address("255.255.255.255")), "255.255.255.255")
        self.assertEqual(str(IPv4Address("127.0.0.1")), "127.0.0.1")
        
    def test_invalid_ipv4(self):
        """测试无效IPv4地址"""
        with self.assertRaises(ValueError):
            IPv4Address("256.1.1.1")
        with self.assertRaises(ValueError):
            IPv4Address("1.1.1")
        with self.assertRaises(ValueError):
            IPv4Address("abc.def.ghi.jkl")
            
    def test_ipv4_comparison(self):
        """测试IPv4比较"""
        ip1 = IPv4Address("192.168.1.1")
        ip2 = IPv4Address("192.168.1.2")
        ip3 = IPv4Address("192.168.1.1")
        
        self.assertTrue(ip1 < ip2)
        self.assertTrue(ip2 > ip1)
        self.assertTrue(ip1 == ip3)
        self.assertTrue(ip1 <= ip3)
        self.assertTrue(ip1 >= ip3)


class TestIPv6Address(unittest.TestCase):
    """IPv6地址测试"""
    
    def test_valid_ipv6(self):
        """测试有效IPv6地址"""
        ip = IPv6Address("2001:db8::1")
        self.assertEqual(str(ip), "2001:db8::1")
        self.assertEqual(ip.version, 6)
        
    def test_ipv6_compression(self):
        """测试IPv6地址压缩"""
        # 测试完整地址的压缩
        ip1 = IPv6Address("2001:0db8:0000:0000:0000:0000:0000:0001")
        self.assertEqual(str(ip1), "2001:db8::1")
        
    def test_ipv6_from_int(self):
        """测试从整数创建IPv6"""
        ip = IPv6Address(1)
        self.assertEqual(str(ip), "::1")
        
    def test_ipv6_loopback(self):
        """测试IPv6回环地址"""
        ip = IPv6Address("::1")
        self.assertEqual(str(ip), "::1")
        
    def test_invalid_ipv6(self):
        """测试无效IPv6地址"""
        with self.assertRaises(ValueError):
            IPv6Address("gggg::1")
        with self.assertRaises(ValueError):
            IPv6Address("1:2:3:4:5:6:7:8:9")  # 太多段


class TestCIDRConversion(unittest.TestCase):
    """CIDR转换测试"""
    
    def test_cidr_to_mask_ipv4(self):
        """测试IPv4 CIDR转掩码"""
        self.assertEqual(cidr_to_mask(24, 4), 0xFFFFFF00)
        self.assertEqual(cidr_to_mask(16, 4), 0xFFFF0000)
        self.assertEqual(cidr_to_mask(8, 4), 0xFF000000)
        self.assertEqual(cidr_to_mask(32, 4), 0xFFFFFFFF)
        self.assertEqual(cidr_to_mask(0, 4), 0)
        
    def test_mask_to_cidr_ipv4(self):
        """测试IPv4掩码转CIDR"""
        self.assertEqual(mask_to_cidr("255.255.255.0", 4), 24)
        self.assertEqual(mask_to_cidr("255.255.0.0", 4), 16)
        self.assertEqual(mask_to_cidr("255.0.0.0", 4), 8)
        self.assertEqual(mask_to_cidr("255.255.255.255", 4), 32)
        self.assertEqual(mask_to_cidr("0.0.0.0", 4), 0)
        
    def test_mask_to_cidr_from_int(self):
        """测试从整数掩码转CIDR"""
        self.assertEqual(mask_to_cidr(0xFFFFFF00, 4), 24)
        
    def test_invalid_mask(self):
        """测试无效掩码"""
        with self.assertRaises(ValueError):
            mask_to_cidr("255.0.255.0", 4)  # 非连续掩码


class TestSubnet(unittest.TestCase):
    """子网测试"""
    
    def test_parse_cidr(self):
        """测试CIDR解析"""
        net, prefix = parse_cidr("192.168.1.0/24")
        self.assertEqual(str(net), "192.168.1.0")
        self.assertEqual(prefix, 24)
        
    def test_subnet_creation(self):
        """测试子网创建"""
        subnet = Subnet("192.168.1.0/24")
        self.assertEqual(str(subnet.network), "192.168.1.0")
        self.assertEqual(subnet.prefix, 24)
        self.assertEqual(str(subnet), "192.168.1.0/24")
        
    def test_subnet_mask(self):
        """测试子网掩码"""
        subnet = Subnet("192.168.1.0/24")
        self.assertEqual(str(subnet.mask), "255.255.255.0")
        
    def test_broadcast_address(self):
        """测试广播地址"""
        subnet = Subnet("192.168.1.0/24")
        self.assertEqual(str(subnet.broadcast), "192.168.1.255")
        
    def test_host_range(self):
        """测试主机范围"""
        subnet = Subnet("192.168.1.0/24")
        self.assertEqual(str(subnet.first_host), "192.168.1.1")
        self.assertEqual(str(subnet.last_host), "192.168.1.254")
        
    def test_host_count(self):
        """测试主机数量"""
        self.assertEqual(get_host_count(24, 4), 254)
        self.assertEqual(get_host_count(25, 4), 126)
        self.assertEqual(get_host_count(30, 4), 2)
        self.assertEqual(get_host_count(32, 4), 1)
        self.assertEqual(get_host_count(31, 4), 2)
        
    def test_subnet_contains(self):
        """测试IP包含检查"""
        subnet = Subnet("192.168.1.0/24")
        self.assertTrue(subnet.contains("192.168.1.100"))
        self.assertTrue("192.168.1.100" in subnet)
        self.assertFalse(subnet.contains("192.168.2.1"))
        
    def test_ipv6_subnet(self):
        """测试IPv6子网"""
        subnet = Subnet("2001:db8::/32")
        self.assertEqual(subnet.prefix, 32)
        self.assertTrue(subnet.contains("2001:db8:1::1"))
        self.assertFalse(subnet.contains("2001:db9::1"))


class TestNetworkFunctions(unittest.TestCase):
    """网络计算函数测试"""
    
    def test_get_network_address(self):
        """测试网络地址计算"""
        self.assertEqual(str(get_network_address("192.168.1.100", 24)), "192.168.1.0")
        self.assertEqual(str(get_network_address("192.168.1.100", 25)), "192.168.1.0")
        self.assertEqual(str(get_network_address("192.168.1.150", 25)), "192.168.1.128")
        
    def test_get_broadcast_address(self):
        """测试广播地址计算"""
        self.assertEqual(str(get_broadcast_address("192.168.1.0", 24)), "192.168.1.255")
        self.assertEqual(str(get_broadcast_address("192.168.1.128", 25)), "192.168.1.255")
        
    def test_is_ip_in_subnet(self):
        """测试IP在子网内检查"""
        self.assertTrue(is_ip_in_subnet("192.168.1.100", "192.168.1.0", 24))
        self.assertFalse(is_ip_in_subnet("192.168.2.1", "192.168.1.0", 24))
        self.assertTrue(is_ip_in_subnet("10.0.0.5", "10.0.0.0", 8))


class TestSubnetSplit(unittest.TestCase):
    """子网划分测试"""
    
    def test_split_24_to_26(self):
        """测试/24划分为/26"""
        subnets = split_subnet("192.168.1.0/24", 26)
        self.assertEqual(len(subnets), 4)
        self.assertEqual(str(subnets[0]), "192.168.1.0/26")
        self.assertEqual(str(subnets[1]), "192.168.1.64/26")
        self.assertEqual(str(subnets[2]), "192.168.1.128/26")
        self.assertEqual(str(subnets[3]), "192.168.1.192/26")
        
    def test_split_24_to_25(self):
        """测试/24划分为/25"""
        subnets = split_subnet("192.168.1.0/24", 25)
        self.assertEqual(len(subnets), 2)
        self.assertEqual(str(subnets[0]), "192.168.1.0/25")
        self.assertEqual(str(subnets[1]), "192.168.1.128/25")
        
    def test_invalid_split(self):
        """测试无效划分"""
        with self.assertRaises(ValueError):
            split_subnet("192.168.1.0/24", 24)  # 相同前缀
        with self.assertRaises(ValueError):
            split_subnet("192.168.1.0/24", 20)  # 更小前缀


class TestSubnetMerge(unittest.TestCase):
    """子网合并测试"""
    
    def test_merge_two_25s(self):
        """测试合并两个/25"""
        result = merge_subnets(["192.168.1.0/25", "192.168.1.128/25"])
        self.assertIsNotNone(result)
        self.assertEqual(str(result), "192.168.1.0/24")
        
    def test_merge_four_26s(self):
        """测试合并四个/26"""
        result = merge_subnets([
            "192.168.1.0/26",
            "192.168.1.64/26",
            "192.168.1.128/26",
            "192.168.1.192/26"
        ])
        self.assertIsNotNone(result)
        self.assertEqual(str(result), "192.168.1.0/24")
        
    def test_cannot_merge(self):
        """测试无法合并的情况"""
        # 不连续的子网
        result = merge_subnets(["192.168.1.0/25", "192.168.2.0/25"])
        self.assertIsNone(result)
        
        # 不同前缀长度
        result = merge_subnets(["192.168.1.0/24", "192.168.2.0/25"])
        self.assertIsNone(result)


class TestFindSmallestSubnet(unittest.TestCase):
    """最小子网查找测试"""
    
    def test_find_subnet_two_ips(self):
        """测试两个IP的最小子网"""
        # 192.168.1.1 和 192.168.1.100 都在 /25 范围内
        result = find_smallest_subnet(["192.168.1.1", "192.168.1.100"])
        self.assertIsNotNone(result)
        self.assertEqual(str(result), "192.168.1.0/25")
        
    def test_find_subnet_different_networks(self):
        """测试不同网络的IP"""
        # 192.168.1.1 和 192.168.2.1 需要至少 /22 才能覆盖
        result = find_smallest_subnet(["192.168.1.1", "192.168.2.1"])
        self.assertIsNotNone(result)
        self.assertEqual(str(result), "192.168.0.0/22")
        
    def test_find_subnet_single_ip(self):
        """测试单个IP"""
        result = find_smallest_subnet(["192.168.1.100"])
        self.assertIsNotNone(result)
        self.assertEqual(str(result), "192.168.1.100/32")


class TestListAvailableIPs(unittest.TestCase):
    """IP列表测试"""
    
    def test_list_ips_30(self):
        """测试/30子网"""
        ips = list_available_ips("192.168.1.0/30")
        self.assertEqual(len(ips), 2)
        self.assertEqual(str(ips[0]), "192.168.1.1")
        self.assertEqual(str(ips[1]), "192.168.1.2")
        
    def test_list_ips_include_all(self):
        """测试包含网络和广播地址"""
        ips = list_available_ips("192.168.1.0/30", 
                                include_network=True, 
                                include_broadcast=True)
        self.assertEqual(len(ips), 4)
        
    def test_list_ips_too_large(self):
        """测试过大的子网"""
        with self.assertRaises(ValueError):
            list_available_ips("10.0.0.0/8")


class TestValidation(unittest.TestCase):
    """验证函数测试"""
    
    def test_is_valid_ipv4(self):
        """测试IPv4验证"""
        self.assertTrue(is_valid_ipv4("192.168.1.1"))
        self.assertTrue(is_valid_ipv4("0.0.0.0"))
        self.assertTrue(is_valid_ipv4("255.255.255.255"))
        self.assertFalse(is_valid_ipv4("256.1.1.1"))
        self.assertFalse(is_valid_ipv4("1.1.1"))
        self.assertFalse(is_valid_ipv4("::1"))
        
    def test_is_valid_ipv6(self):
        """测试IPv6验证"""
        self.assertTrue(is_valid_ipv6("2001:db8::1"))
        self.assertTrue(is_valid_ipv6("::1"))
        self.assertTrue(is_valid_ipv6("::"))
        self.assertFalse(is_valid_ipv6("gggg::1"))
        self.assertFalse(is_valid_ipv6("192.168.1.1"))
        
    def test_is_valid_ip(self):
        """测试IP验证"""
        self.assertEqual(is_valid_ip("192.168.1.1"), (True, 4))
        self.assertEqual(is_valid_ip("2001:db8::1"), (True, 6))
        self.assertEqual(is_valid_ip("invalid"), (False, None))


class TestIPConversion(unittest.TestCase):
    """IP转换测试"""
    
    def test_ip_to_int(self):
        """测试IP转整数"""
        self.assertEqual(ip_to_int("0.0.0.0"), 0)
        self.assertEqual(ip_to_int("0.0.0.1"), 1)
        self.assertEqual(ip_to_int("192.168.1.1"), 3232235777)
        
    def test_int_to_ip(self):
        """测试整数转IP"""
        self.assertEqual(str(int_to_ip(0, 4)), "0.0.0.0")
        self.assertEqual(str(int_to_ip(3232235777, 4)), "192.168.1.1")
        
    def test_roundtrip(self):
        """测试往返转换"""
        test_ips = ["192.168.1.1", "10.0.0.1", "172.16.0.1", "255.255.255.255"]
        for ip in test_ips:
            self.assertEqual(str(int_to_ip(ip_to_int(ip), 4)), ip)


if __name__ == "__main__":
    unittest.main()