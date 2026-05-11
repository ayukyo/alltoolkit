"""
CIDR Utils 测试文件
"""

import unittest
from mod import (
    CIDRError,
    IPAddress,
    CIDR,
    parse_cidr,
    ip_to_int,
    int_to_ip,
    prefix_to_netmask,
    netmask_to_prefix,
    is_valid_cidr,
    is_valid_ip,
    ip_in_cidr,
    get_ip_version,
    subnet_cidr,
    merge_cidrs,
    calculate_host_range,
    get_all_hosts,
    cidr_to_range,
    range_to_cidr,
    wildcard_to_cidr,
    get_network_class,
    is_private_ip,
    is_loopback_ip,
    is_multicast_ip,
    is_link_local_ip,
)


class TestIPAddress(unittest.TestCase):
    """IP 地址测试"""
    
    def test_ipv4_creation(self):
        """测试 IPv4 创建"""
        ip = IPAddress('192.168.1.1')
        self.assertEqual(ip.version, 4)
        self.assertEqual(str(ip), '192.168.1.1')
    
    def test_ipv6_creation(self):
        """测试 IPv6 创建"""
        ip = IPAddress('2001:db8::1')
        self.assertEqual(ip.version, 6)
        self.assertEqual(str(ip), '2001:db8::1')
    
    def test_ip_to_int(self):
        """测试 IP 转整数"""
        ip = IPAddress('192.168.1.1')
        expected = (192 << 24) | (168 << 16) | (1 << 8) | 1
        self.assertEqual(int(ip), expected)
    
    def test_int_to_ip(self):
        """测试整数转 IP"""
        value = (192 << 24) | (168 << 16) | (1 << 8) | 1
        ip = IPAddress(value, 4)
        self.assertEqual(str(ip), '192.168.1.1')
    
    def test_ip_comparison(self):
        """测试 IP 比较"""
        ip1 = IPAddress('192.168.1.1')
        ip2 = IPAddress('192.168.1.2')
        ip3 = IPAddress('192.168.1.1')
        
        self.assertTrue(ip1 < ip2)
        self.assertTrue(ip2 > ip1)
        self.assertTrue(ip1 == ip3)
        self.assertTrue(ip1 <= ip3)
        self.assertTrue(ip1 >= ip3)
    
    def test_ip_bitwise_ops(self):
        """测试位运算"""
        ip = IPAddress('192.168.1.1')
        mask = IPAddress('255.255.255.0')
        
        result = ip & mask
        self.assertEqual(str(result), '192.168.1.0')
        
        wildcard = ~mask
        self.assertEqual(str(wildcard), '0.0.0.255')
    
    def test_ip_addition(self):
        """测试 IP 加法"""
        ip = IPAddress('192.168.1.1')
        result = ip + 10
        self.assertEqual(str(result), '192.168.1.11')
    
    def test_ip_subtraction(self):
        """测试 IP 减法"""
        ip1 = IPAddress('192.168.1.11')
        ip2 = IPAddress('192.168.1.1')
        
        result = ip1 - 10
        self.assertEqual(str(result), '192.168.1.1')
        
        diff = ip1 - ip2
        self.assertEqual(diff, 10)
    
    def test_invalid_ip(self):
        """测试无效 IP"""
        with self.assertRaises(CIDRError):
            IPAddress('invalid.ip.address')
        
        with self.assertRaises(CIDRError):
            IPAddress('256.1.1.1')
    
    def test_ipv6_compression(self):
        """测试 IPv6 地址压缩"""
        ip1 = IPAddress('2001:0db8:0000:0000:0000:0000:0000:0001')
        ip2 = IPAddress('2001:db8::1')
        
        # 两者应该相等（压缩后相同）
        self.assertEqual(int(ip1), int(ip2))


class TestCIDR(unittest.TestCase):
    """CIDR 测试"""
    
    def test_cidr_creation(self):
        """测试 CIDR 创建"""
        cidr = CIDR('192.168.1.0/24')
        self.assertEqual(cidr.version, 4)
        self.assertEqual(cidr.prefix, 24)
        self.assertEqual(str(cidr.network_address), '192.168.1.0')
        self.assertEqual(str(cidr.broadcast_address), '192.168.1.255')
        self.assertEqual(str(cidr.netmask), '255.255.255.0')
    
    def test_cidr_properties(self):
        """测试 CIDR 属性"""
        cidr = CIDR('192.168.1.0/24')
        
        self.assertEqual(cidr.num_addresses, 256)
        self.assertEqual(cidr.num_hosts, 254)
        self.assertEqual(str(cidr.first_host), '192.168.1.1')
        self.assertEqual(str(cidr.last_host), '192.168.1.254')
        self.assertEqual(str(cidr.wildcard), '0.0.0.255')
    
    def test_cidr_16(self):
        """测试 /16 网络"""
        cidr = CIDR('172.16.0.0/16')
        
        self.assertEqual(cidr.num_addresses, 65536)
        self.assertEqual(cidr.num_hosts, 65534)
        self.assertEqual(str(cidr.netmask), '255.255.0.0')
    
    def test_cidr_32(self):
        """测试 /32 单主机"""
        cidr = CIDR('192.168.1.1/32')
        
        self.assertEqual(cidr.num_addresses, 1)
        self.assertEqual(cidr.num_hosts, 0)  # 无可用主机
        self.assertIsNone(cidr.first_host)
        self.assertIsNone(cidr.last_host)
    
    def test_cidr_31(self):
        """测试 /31 点对点链路"""
        cidr = CIDR('192.168.1.0/31')
        
        self.assertEqual(cidr.num_addresses, 2)
        self.assertEqual(cidr.num_hosts, 0)  # /31 无主机位
    
    def test_cidr_0(self):
        """测试 /0 全网"""
        cidr = CIDR('0.0.0.0/0')
        
        self.assertEqual(cidr.num_addresses, 4294967296)  # 2^32
        self.assertEqual(cidr.num_hosts, 4294967294)
    
    def test_ipv6_cidr(self):
        """测试 IPv6 CIDR"""
        cidr = CIDR('2001:db8::/32')
        
        self.assertEqual(cidr.version, 6)
        self.assertEqual(cidr.prefix, 32)
        self.assertEqual(str(cidr.network_address), '2001:db8::')
    
    def test_ip_in_cidr(self):
        """测试 IP 是否在 CIDR 内"""
        cidr = CIDR('192.168.1.0/24')
        
        self.assertTrue('192.168.1.1' in cidr)
        self.assertTrue('192.168.1.255' in cidr)
        self.assertFalse('192.168.2.1' in cidr)
        
        self.assertTrue(cidr.contains('192.168.1.100'))
    
    def test_cidr_overlaps(self):
        """测试 CIDR 重叠检查"""
        cidr1 = CIDR('192.168.1.0/24')
        cidr2 = CIDR('192.168.1.128/25')
        cidr3 = CIDR('192.168.2.0/24')
        
        self.assertTrue(cidr1.overlaps(cidr2))
        self.assertFalse(cidr1.overlaps(cidr3))
    
    def test_subnet_relation(self):
        """测试子网关系"""
        cidr1 = CIDR('192.168.0.0/16')
        cidr2 = CIDR('192.168.1.0/24')
        
        self.assertTrue(cidr2.is_subnet_of(cidr1))
        self.assertTrue(cidr1.is_supernet_of(cidr2))
    
    def test_subnet(self):
        """测试子网划分"""
        cidr = CIDR('192.168.1.0/24')
        subnets = cidr.subnet(26)
        
        self.assertEqual(len(subnets), 4)
        self.assertEqual(str(subnets[0]), '192.168.1.0/26')
        self.assertEqual(str(subnets[1]), '192.168.1.64/26')
        self.assertEqual(str(subnets[2]), '192.168.1.128/26')
        self.assertEqual(str(subnets[3]), '192.168.1.192/26')
    
    def test_hosts(self):
        """测试主机列表"""
        cidr = CIDR('192.168.1.0/30')  # 4 地址，2 主机
        hosts = cidr.hosts()
        
        self.assertEqual(len(hosts), 2)
        self.assertEqual(str(hosts[0]), '192.168.1.1')
        self.assertEqual(str(hosts[1]), '192.168.1.2')
    
    def test_invalid_cidr(self):
        """测试无效 CIDR"""
        with self.assertRaises(CIDRError):
            CIDR('invalid')
        
        with self.assertRaises(CIDRError):
            CIDR('192.168.1.0/33')  # 前缀超出范围


class TestUtilityFunctions(unittest.TestCase):
    """工具函数测试"""
    
    def test_parse_cidr(self):
        """测试 CIDR 解析"""
        cidr = parse_cidr('192.168.1.0/24')
        self.assertEqual(str(cidr), '192.168.1.0/24')
    
    def test_ip_to_int(self):
        """测试 IP 转整数"""
        value = ip_to_int('192.168.1.1')
        expected = (192 << 24) | (168 << 16) | (1 << 8) | 1
        self.assertEqual(value, expected)
    
    def test_int_to_ip(self):
        """测试整数转 IP"""
        value = (192 << 24) | (168 << 16) | (1 << 8) | 1
        ip = int_to_ip(value)
        self.assertEqual(ip, '192.168.1.1')
    
    def test_prefix_to_netmask(self):
        """测试前缀转掩码"""
        self.assertEqual(prefix_to_netmask(24), '255.255.255.0')
        self.assertEqual(prefix_to_netmask(16), '255.255.0.0')
        self.assertEqual(prefix_to_netmask(8), '255.0.0.0')
        self.assertEqual(prefix_to_netmask(0), '0.0.0.0')
        self.assertEqual(prefix_to_netmask(32), '255.255.255.255')
    
    def test_netmask_to_prefix(self):
        """测试掩码转前缀"""
        self.assertEqual(netmask_to_prefix('255.255.255.0'), 24)
        self.assertEqual(netmask_to_prefix('255.255.0.0'), 16)
        self.assertEqual(netmask_to_prefix('255.0.0.0'), 8)
        self.assertEqual(netmask_to_prefix('0.0.0.0'), 0)
        self.assertEqual(netmask_to_prefix('255.255.255.255'), 32)
    
    def test_is_valid_cidr(self):
        """测试 CIDR 验证"""
        self.assertTrue(is_valid_cidr('192.168.1.0/24'))
        self.assertTrue(is_valid_cidr('10.0.0.0/8'))
        self.assertFalse(is_valid_cidr('invalid'))
        self.assertFalse(is_valid_cidr('192.168.1.0/33'))
    
    def test_is_valid_ip(self):
        """测试 IP 验证"""
        self.assertTrue(is_valid_ip('192.168.1.1'))
        self.assertTrue(is_valid_ip('2001:db8::1'))
        self.assertFalse(is_valid_ip('256.1.1.1'))
        self.assertFalse(is_valid_ip('invalid'))
    
    def test_ip_in_cidr_function(self):
        """测试 IP 在 CIDR 内的函数"""
        self.assertTrue(ip_in_cidr('192.168.1.100', '192.168.1.0/24'))
        self.assertFalse(ip_in_cidr('192.168.2.1', '192.168.1.0/24'))
    
    def test_get_ip_version(self):
        """测试获取 IP 版本"""
        self.assertEqual(get_ip_version('192.168.1.1'), 4)
        self.assertEqual(get_ip_version('2001:db8::1'), 6)
    
    def test_subnet_cidr(self):
        """测试子网划分函数"""
        subnets = subnet_cidr('192.168.1.0/24', 26)
        self.assertEqual(len(subnets), 4)
    
    def test_calculate_host_range(self):
        """测试主机范围计算"""
        start, end = calculate_host_range('192.168.1.0/24')
        self.assertEqual(start, '192.168.1.1')
        self.assertEqual(end, '192.168.1.254')
    
    def test_get_all_hosts(self):
        """测试获取所有主机"""
        hosts = get_all_hosts('192.168.1.0/30')
        self.assertEqual(len(hosts), 2)
        self.assertIn('192.168.1.1', hosts)
        self.assertIn('192.168.1.2', hosts)
    
    def test_cidr_to_range(self):
        """测试 CIDR 转范围"""
        start, end = cidr_to_range('192.168.1.0/24')
        self.assertEqual(start, '192.168.1.0')
        self.assertEqual(end, '192.168.1.255')
    
    def test_range_to_cidr(self):
        """测试范围转 CIDR"""
        cidrs = range_to_cidr('192.168.1.0', '192.168.1.255')
        self.assertEqual(len(cidrs), 1)
        self.assertEqual(str(cidrs[0]), '192.168.1.0/24')
        
        # 测试连续但不是完美匹配的范围
        cidrs = range_to_cidr('192.168.0.0', '192.168.1.255')
        # 192.168.0.0/23 覆盖这个范围 (512 地址)
        self.assertEqual(len(cidrs), 1)
        self.assertEqual(str(cidrs[0]), '192.168.0.0/23')
    
    def test_wildcard_to_cidr(self):
        """测试通配符转 CIDR"""
        cidr = wildcard_to_cidr('192.168.1.0', '0.0.0.255')
        self.assertEqual(str(cidr), '192.168.1.0/24')


class TestIPClassification(unittest.TestCase):
    """IP 分类测试"""
    
    def test_network_class(self):
        """测试网络类别"""
        self.assertEqual(get_network_class('10.0.0.1'), 'A')
        self.assertEqual(get_network_class('172.16.0.1'), 'B')
        self.assertEqual(get_network_class('192.168.1.1'), 'C')
        self.assertEqual(get_network_class('224.0.0.1'), 'D')
        self.assertEqual(get_network_class('240.0.0.1'), 'E')
    
    def test_is_private_ip(self):
        """测试私有 IP"""
        self.assertTrue(is_private_ip('10.0.0.1'))
        self.assertTrue(is_private_ip('172.16.0.1'))
        self.assertTrue(is_private_ip('192.168.1.1'))
        self.assertFalse(is_private_ip('8.8.8.8'))
        
        # IPv6
        self.assertTrue(is_private_ip('fc00::1'))
        self.assertTrue(is_private_ip('fe80::1'))
    
    def test_is_loopback_ip(self):
        """测试环回地址"""
        self.assertTrue(is_loopback_ip('127.0.0.1'))
        self.assertTrue(is_loopback_ip('127.0.0.255'))
        self.assertFalse(is_loopback_ip('192.168.1.1'))
        
        # IPv6
        self.assertTrue(is_loopback_ip('::1'))
        self.assertFalse(is_loopback_ip('::2'))
    
    def test_is_multicast_ip(self):
        """测试组播地址"""
        self.assertTrue(is_multicast_ip('224.0.0.1'))
        self.assertTrue(is_multicast_ip('239.255.255.255'))
        self.assertFalse(is_multicast_ip('192.168.1.1'))
        
        # IPv6
        self.assertTrue(is_multicast_ip('ff00::1'))
    
    def test_is_link_local_ip(self):
        """测试链路本地地址"""
        self.assertTrue(is_link_local_ip('169.254.1.1'))
        self.assertFalse(is_link_local_ip('192.168.1.1'))
        
        # IPv6
        self.assertTrue(is_link_local_ip('fe80::1'))
        self.assertFalse(is_link_local_ip('fc00::1'))


class TestIPv6Support(unittest.TestCase):
    """IPv6 支持测试"""
    
    def test_ipv6_cidr_basic(self):
        """测试 IPv6 CIDR 基本功能"""
        cidr = CIDR('2001:db8::/32')
        
        self.assertEqual(cidr.version, 6)
        self.assertEqual(cidr.prefix, 32)
        self.assertEqual(str(cidr.network_address), '2001:db8::')
        self.assertEqual(cidr.num_addresses, 1 << 96)  # 2^96
    
    def test_ipv6_ip_operations(self):
        """测试 IPv6 IP 操作"""
        ip1 = IPAddress('2001:db8::1')
        ip2 = IPAddress('2001:db8::2')
        
        self.assertTrue(ip1 < ip2)
        self.assertEqual(str(ip1 + 1), '2001:db8::2')
    
    def test_ipv6_subnet(self):
        """测试 IPv6 子网划分"""
        cidr = CIDR('2001:db8::/32')
        subnets = cidr.subnet(48)
        
        self.assertEqual(len(subnets), 65536)  # 2^(48-32)
    
    def test_ipv6_in_cidr(self):
        """测试 IPv6 在 CIDR 内"""
        cidr = CIDR('2001:db8::/32')
        
        self.assertTrue('2001:db8::1' in cidr)
        self.assertTrue('2001:db8:ffff::1' in cidr)
        self.assertFalse('2001:db9::1' in cidr)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_single_host_network(self):
        """测试单主机网络"""
        cidr = CIDR('192.168.1.1/32')
        
        self.assertEqual(cidr.num_addresses, 1)
        self.assertEqual(cidr.num_hosts, 0)
    
    def test_entire_internet(self):
        """测试全网"""
        cidr = CIDR('0.0.0.0/0')
        
        self.assertEqual(cidr.num_addresses, 2**32)
        self.assertEqual(str(cidr.netmask), '0.0.0.0')
    
    def test_minimum_ipv4_network(self):
        """测试最小 IPv4 网络"""
        cidr = CIDR('255.255.255.255/32')
        
        self.assertEqual(cidr.num_addresses, 1)
    
    def test_large_subnet(self):
        """测试大型子网划分"""
        cidr = CIDR('10.0.0.0/8')
        subnets = cidr.subnet(16)
        
        self.assertEqual(len(subnets), 256)
    
    def test_consecutive_ips(self):
        """测试连续 IP"""
        ip = IPAddress('192.168.1.1')
        
        for i in range(10):
            self.assertEqual(str(ip + i), f'192.168.1.{1 + i}')
    
    def test_network_address_normalization(self):
        """测试网络地址标准化"""
        # 非标准网络地址应该被标准化
        cidr = CIDR('192.168.1.100/24')
        self.assertEqual(str(cidr.network_address), '192.168.1.0')
        self.assertEqual(str(cidr), '192.168.1.0/24')


class TestCIDRInfo(unittest.TestCase):
    """CIDR 信息测试"""
    
    def test_info_dict(self):
        """测试信息字典"""
        cidr = CIDR('192.168.1.0/24')
        info = cidr.info()
        
        self.assertEqual(info['cidr'], '192.168.1.0/24')
        self.assertEqual(info['version'], 4)
        self.assertEqual(info['network_address'], '192.168.1.0')
        self.assertEqual(info['broadcast_address'], '192.168.1.255')
        self.assertEqual(info['netmask'], '255.255.255.0')
        self.assertEqual(info['wildcard'], '0.0.0.255')
        self.assertEqual(info['first_host'], '192.168.1.1')
        self.assertEqual(info['last_host'], '192.168.1.254')
        self.assertEqual(info['num_addresses'], 256)
        self.assertEqual(info['num_hosts'], 254)
        self.assertEqual(info['prefix_length'], 24)


if __name__ == '__main__':
    unittest.main(verbosity=2)