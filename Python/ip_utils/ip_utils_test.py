#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - IP Address Utilities Test Suite
==============================================
Comprehensive tests for ip_utils module.

Run with: python -m pytest ip_utils_test.py -v
Or directly: python ip_utils_test.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # IPv4 functions
    validate_ipv4, ipv4_to_int, int_to_ipv4, get_ipv4_class,
    is_private_ipv4, is_loopback_ipv4, is_link_local_ipv4,
    is_multicast_ipv4, is_reserved_ipv4, get_ipv4_info,
    
    # Subnet functions
    cidr_to_mask, mask_to_cidr, get_subnet_info, ip_in_subnet,
    get_all_hosts_in_subnet, split_subnet,
    
    # IPv6 functions
    validate_ipv6, expand_ipv6, compress_ipv6, ipv6_to_int, int_to_ipv6,
    is_private_ipv6, is_loopback_ipv6, is_link_local_ipv6,
    is_multicast_ipv6, get_ipv6_info,
    
    # General functions
    validate_ip, get_ip_version, compare_ips, sort_ips, parse_cidr,
    get_local_ip_ranges, is_public_ip,
    
    # Data classes
    IPv4Info, SubnetInfo, IPv6Info
)

import unittest


class TestIPv4Validation(unittest.TestCase):
    """Test IPv4 address validation."""
    
    def test_valid_ipv4(self):
        """Test valid IPv4 addresses."""
        valid_ips = [
            '0.0.0.0',
            '192.168.1.1',
            '255.255.255.255',
            '10.0.0.1',
            '172.16.0.1',
            '127.0.0.1',
            '8.8.8.8',
            '1.2.3.4',
        ]
        for ip in valid_ips:
            with self.subTest(ip=ip):
                self.assertTrue(validate_ipv4(ip))
    
    def test_invalid_ipv4(self):
        """Test invalid IPv4 addresses."""
        invalid_ips = [
            '256.1.1.1',          # Octet > 255
            '1.256.1.1',          # Octet > 255
            '1.1.256.1',          # Octet > 255
            '1.1.1.256',          # Octet > 255
            '1.1.1',              # Missing octet
            '1.1.1.1.1',          # Too many octets
            '1.1.1.',             # Trailing dot
            '.1.1.1',             # Leading dot
            '1..1.1',             # Double dot
            'a.b.c.d',            # Non-numeric
            '1.1.1.-1',           # Negative
            '01.1.1.1',           # Leading zero (invalid)
            '1.01.1.1',           # Leading zero (invalid)
            '',                   # Empty string
            '192.168.1',          # Missing octet
        ]
        for ip in invalid_ips:
            with self.subTest(ip=ip):
                self.assertFalse(validate_ipv4(ip))


class TestIPv4Conversion(unittest.TestCase):
    """Test IPv4 address conversion functions."""
    
    def test_ipv4_to_int(self):
        """Test IPv4 to integer conversion."""
        test_cases = [
            ('0.0.0.0', 0),
            ('0.0.0.1', 1),
            ('0.0.1.0', 256),
            ('0.1.0.0', 65536),
            ('1.0.0.0', 16777216),
            ('192.168.1.1', 3232235777),
            ('255.255.255.255', 4294967295),
            ('127.0.0.1', 2130706433),
        ]
        for ip, expected in test_cases:
            with self.subTest(ip=ip):
                self.assertEqual(ipv4_to_int(ip), expected)
    
    def test_int_to_ipv4(self):
        """Test integer to IPv4 conversion."""
        test_cases = [
            (0, '0.0.0.0'),
            (1, '0.0.0.1'),
            (256, '0.0.1.0'),
            (65536, '0.1.0.0'),
            (16777216, '1.0.0.0'),
            (3232235777, '192.168.1.1'),
            (4294967295, '255.255.255.255'),
            (2130706433, '127.0.0.1'),
        ]
        for num, expected in test_cases:
            with self.subTest(num=num):
                self.assertEqual(int_to_ipv4(num), expected)
    
    def test_ipv4_int_roundtrip(self):
        """Test IPv4 <-> integer conversion roundtrip."""
        test_ips = [
            '192.168.1.1',
            '10.0.0.1',
            '172.16.0.1',
            '127.0.0.1',
            '8.8.8.8',
            '255.255.255.255',
            '0.0.0.0',
        ]
        for ip in test_ips:
            with self.subTest(ip=ip):
                self.assertEqual(int_to_ipv4(ipv4_to_int(ip)), ip)
    
    def test_int_to_ipv4_invalid(self):
        """Test int_to_ipv4 with invalid input."""
        with self.assertRaises(ValueError):
            int_to_ipv4(-1)
        with self.assertRaises(ValueError):
            int_to_ipv4(2**32)


class TestIPv4Classification(unittest.TestCase):
    """Test IPv4 address classification functions."""
    
    def test_get_ipv4_class(self):
        """Test IPv4 address class determination."""
        test_cases = [
            ('10.0.0.1', 'A'),
            ('127.0.0.1', 'A'),
            ('172.16.0.1', 'B'),
            ('128.0.0.1', 'B'),
            ('192.168.1.1', 'C'),
            ('224.0.0.1', 'D'),
            ('239.0.0.1', 'D'),
            ('240.0.0.1', 'E'),
            ('255.255.255.255', 'E'),
        ]
        for ip, expected in test_cases:
            with self.subTest(ip=ip):
                self.assertEqual(get_ipv4_class(ip), expected)
    
    def test_is_private_ipv4(self):
        """Test private IPv4 detection."""
        private_ips = [
            '10.0.0.1',
            '10.255.255.255',
            '172.16.0.1',
            '172.31.255.255',
            '192.168.0.1',
            '192.168.255.255',
        ]
        for ip in private_ips:
            with self.subTest(ip=ip):
                self.assertTrue(is_private_ipv4(ip))
        
        public_ips = [
            '8.8.8.8',
            '1.1.1.1',
            '172.15.0.1',   # Not in private range
            '192.169.0.1',  # Not in private range
        ]
        for ip in public_ips:
            with self.subTest(ip=ip):
                self.assertFalse(is_private_ipv4(ip))
    
    def test_is_loopback_ipv4(self):
        """Test loopback IPv4 detection."""
        self.assertTrue(is_loopback_ipv4('127.0.0.1'))
        self.assertTrue(is_loopback_ipv4('127.255.255.255'))
        self.assertTrue(is_loopback_ipv4('127.0.0.0'))
        self.assertFalse(is_loopback_ipv4('128.0.0.1'))
        self.assertFalse(is_loopback_ipv4('192.168.1.1'))
    
    def test_is_link_local_ipv4(self):
        """Test link-local IPv4 detection."""
        self.assertTrue(is_link_local_ipv4('169.254.0.1'))
        self.assertTrue(is_link_local_ipv4('169.254.255.255'))
        self.assertFalse(is_link_local_ipv4('169.255.0.1'))
        self.assertFalse(is_link_local_ipv4('192.168.1.1'))
    
    def test_is_multicast_ipv4(self):
        """Test multicast IPv4 detection."""
        self.assertTrue(is_multicast_ipv4('224.0.0.1'))
        self.assertTrue(is_multicast_ipv4('239.255.255.255'))
        self.assertFalse(is_multicast_ipv4('223.255.255.255'))
        self.assertFalse(is_multicast_ipv4('240.0.0.1'))
    
    def test_is_reserved_ipv4(self):
        """Test reserved IPv4 detection."""
        self.assertTrue(is_reserved_ipv4('0.0.0.0'))
        self.assertTrue(is_reserved_ipv4('192.0.2.1'))   # TEST-NET-1
        self.assertTrue(is_reserved_ipv4('198.51.100.1')) # TEST-NET-2
        self.assertTrue(is_reserved_ipv4('203.0.113.1'))  # TEST-NET-3
        self.assertFalse(is_reserved_ipv4('8.8.8.8'))
        self.assertFalse(is_reserved_ipv4('192.168.1.1'))


class TestIPv4Info(unittest.TestCase):
    """Test IPv4Info dataclass."""
    
    def test_get_ipv4_info(self):
        """Test get_ipv4_info function."""
        info = get_ipv4_info('192.168.1.1')
        
        self.assertEqual(info.address, '192.168.1.1')
        self.assertEqual(info.integer, 3232235777)
        self.assertEqual(info.binary, '11000000.10101000.00000001.00000001')
        self.assertTrue(info.is_private)
        self.assertFalse(info.is_loopback)
        self.assertFalse(info.is_link_local)
        self.assertFalse(info.is_multicast)
        self.assertFalse(info.is_reserved)
        self.assertEqual(info.address_class, 'C')
    
    def test_get_ipv4_info_loopback(self):
        """Test IPv4Info for loopback address."""
        info = get_ipv4_info('127.0.0.1')
        
        self.assertTrue(info.is_loopback)
        self.assertFalse(info.is_private)
    
    def test_get_ipv4_info_invalid(self):
        """Test get_ipv4_info with invalid input."""
        with self.assertRaises(ValueError):
            get_ipv4_info('invalid')


class TestSubnetUtilities(unittest.TestCase):
    """Test subnet utility functions."""
    
    def test_cidr_to_mask(self):
        """Test CIDR prefix to subnet mask conversion."""
        test_cases = [
            (0, '0.0.0.0'),
            (8, '255.0.0.0'),
            (16, '255.255.0.0'),
            (24, '255.255.255.0'),
            (25, '255.255.255.128'),
            (32, '255.255.255.255'),
        ]
        for prefix, expected in test_cases:
            with self.subTest(prefix=prefix):
                self.assertEqual(cidr_to_mask(prefix), expected)
    
    def test_cidr_to_mask_invalid(self):
        """Test cidr_to_mask with invalid input."""
        with self.assertRaises(ValueError):
            cidr_to_mask(-1)
        with self.assertRaises(ValueError):
            cidr_to_mask(33)
    
    def test_mask_to_cidr(self):
        """Test subnet mask to CIDR prefix conversion."""
        test_cases = [
            ('0.0.0.0', 0),
            ('255.0.0.0', 8),
            ('255.255.0.0', 16),
            ('255.255.255.0', 24),
            ('255.255.255.128', 25),
            ('255.255.255.255', 32),
        ]
        for mask, expected in test_cases:
            with self.subTest(mask=mask):
                self.assertEqual(mask_to_cidr(mask), expected)
    
    def test_mask_to_cidr_invalid(self):
        """Test mask_to_cidr with non-contiguous mask."""
        with self.assertRaises(ValueError):
            mask_to_cidr('255.0.255.0')  # Non-contiguous
    
    def test_get_subnet_info(self):
        """Test get_subnet_info function."""
        info = get_subnet_info('192.168.1.0/24')
        
        self.assertEqual(info.network_address, '192.168.1.0')
        self.assertEqual(info.broadcast_address, '192.168.1.255')
        self.assertEqual(info.first_usable, '192.168.1.1')
        self.assertEqual(info.last_usable, '192.168.1.254')
        self.assertEqual(info.subnet_mask, '255.255.255.0')
        self.assertEqual(info.cidr_prefix, 24)
        self.assertEqual(info.total_hosts, 256)
        self.assertEqual(info.usable_hosts, 254)
        self.assertEqual(info.wildcard_mask, '0.0.0.255')
    
    def test_get_subnet_info_31(self):
        """Test /31 subnet (point-to-point link)."""
        info = get_subnet_info('192.168.1.0/31')
        
        self.assertEqual(info.network_address, '192.168.1.0')
        self.assertEqual(info.broadcast_address, '192.168.1.1')
        self.assertEqual(info.total_hosts, 2)
        self.assertEqual(info.usable_hosts, 2)
    
    def test_get_subnet_info_32(self):
        """Test /32 subnet (single host)."""
        info = get_subnet_info('192.168.1.1/32')
        
        self.assertEqual(info.network_address, '192.168.1.1')
        self.assertEqual(info.broadcast_address, '192.168.1.1')
        self.assertEqual(info.total_hosts, 1)
        self.assertEqual(info.usable_hosts, 1)
    
    def test_ip_in_subnet(self):
        """Test IP in subnet check."""
        self.assertTrue(ip_in_subnet('192.168.1.100', '192.168.1.0/24'))
        self.assertTrue(ip_in_subnet('192.168.1.0', '192.168.1.0/24'))
        self.assertTrue(ip_in_subnet('192.168.1.255', '192.168.1.0/24'))
        self.assertFalse(ip_in_subnet('192.168.2.1', '192.168.1.0/24'))
        
        # Test with separate prefix argument
        self.assertTrue(ip_in_subnet('10.0.0.5', '10.0.0.0', 24))
    
    def test_get_all_hosts_in_subnet(self):
        """Test get all hosts in subnet."""
        hosts = get_all_hosts_in_subnet('192.168.1.0/30')
        self.assertEqual(hosts, ['192.168.1.1', '192.168.1.2'])
        
        hosts = get_all_hosts_in_subnet('10.0.0.0/29')
        self.assertEqual(len(hosts), 6)  # 8 - 2 = 6 usable hosts
        self.assertEqual(hosts[0], '10.0.0.1')
        self.assertEqual(hosts[-1], '10.0.0.6')
    
    def test_get_all_hosts_large_subnet(self):
        """Test that large subnet raises error."""
        with self.assertRaises(ValueError):
            get_all_hosts_in_subnet('10.0.0.0/8')
    
    def test_split_subnet(self):
        """Test subnet splitting."""
        subnets = split_subnet('192.168.1.0/24', None, 26)
        self.assertEqual(len(subnets), 4)
        self.assertEqual(subnets[0], '192.168.1.0/26')
        self.assertEqual(subnets[1], '192.168.1.64/26')
        self.assertEqual(subnets[2], '192.168.1.128/26')
        self.assertEqual(subnets[3], '192.168.1.192/26')
    
    def test_split_subnet_invalid(self):
        """Test split_subnet with invalid input."""
        with self.assertRaises(ValueError):
            split_subnet('192.168.1.0/24', None, 20)  # New prefix smaller


class TestIPv6Validation(unittest.TestCase):
    """Test IPv6 address validation."""
    
    def test_valid_ipv6(self):
        """Test valid IPv6 addresses."""
        valid_ips = [
            '::1',
            '::',
            '2001:db8::1',
            '2001:0db8:0000:0000:0000:0000:0000:0001',
            'fe80::1',
            'ff02::1',
            'fd00::1',
            '2001:db8:85a3::8a2e:370:7334',
            '2001:0db8:0000:0000:0000:0000:0000:0000',
        ]
        for ip in valid_ips:
            with self.subTest(ip=ip):
                self.assertTrue(validate_ipv6(ip))
    
    def test_invalid_ipv6(self):
        """Test invalid IPv6 addresses."""
        invalid_ips = [
            '2001:db8::1::2',      # Double ::
            '2001:db8:::1',        # Triple colon
            '2001:db8',            # Too short
            'gggg::1',             # Invalid hex
            '2001:db8::1::',       # Double :: twice
            '',                    # Empty
            '1:2:3:4:5:6:7:8:9',   # Too many groups
        ]
        for ip in invalid_ips:
            with self.subTest(ip=ip):
                self.assertFalse(validate_ipv6(ip))


class TestIPv6Conversion(unittest.TestCase):
    """Test IPv6 address conversion functions."""
    
    def test_expand_ipv6(self):
        """Test IPv6 expansion."""
        test_cases = [
            ('::1', '0000:0000:0000:0000:0000:0000:0000:0001'),
            ('::', '0000:0000:0000:0000:0000:0000:0000:0000'),
            ('2001:db8::1', '2001:0db8:0000:0000:0000:0000:0000:0001'),
            ('2001:db8:85a3::8a2e:370:7334', '2001:0db8:85a3:0000:0000:8a2e:0370:7334'),
        ]
        for ip, expected in test_cases:
            with self.subTest(ip=ip):
                self.assertEqual(expand_ipv6(ip), expected)
    
    def test_compress_ipv6(self):
        """Test IPv6 compression."""
        test_cases = [
            ('0000:0000:0000:0000:0000:0000:0000:0001', '::1'),
            ('0000:0000:0000:0000:0000:0000:0000:0000', '::'),
            ('2001:0db8:0000:0000:0000:0000:0000:0001', '2001:db8::1'),
        ]
        for ip, expected in test_cases:
            with self.subTest(ip=ip):
                self.assertEqual(compress_ipv6(ip), expected)
    
    def test_ipv6_roundtrip(self):
        """Test IPv6 expansion and compression roundtrip."""
        test_ips = [
            '::1',
            '2001:db8::1',
            'fe80::1',
            'ff02::1',
        ]
        for ip in test_ips:
            with self.subTest(ip=ip):
                expanded = expand_ipv6(ip)
                compressed = compress_ipv6(expanded)
                self.assertEqual(compressed, ip)
    
    def test_ipv6_to_int(self):
        """Test IPv6 to integer conversion."""
        self.assertEqual(ipv6_to_int('::1'), 1)
        self.assertEqual(ipv6_to_int('::'), 0)
    
    def test_int_to_ipv6(self):
        """Test integer to IPv6 conversion."""
        self.assertEqual(int_to_ipv6(1), '::1')
        self.assertEqual(int_to_ipv6(0), '::')


class TestIPv6Classification(unittest.TestCase):
    """Test IPv6 address classification functions."""
    
    def test_is_private_ipv6(self):
        """Test private IPv6 (ULA) detection."""
        self.assertTrue(is_private_ipv6('fd00::1'))
        self.assertTrue(is_private_ipv6('fc00::1'))
        self.assertFalse(is_private_ipv6('2001:db8::1'))
        self.assertFalse(is_private_ipv6('fe80::1'))
    
    def test_is_loopback_ipv6(self):
        """Test IPv6 loopback detection."""
        self.assertTrue(is_loopback_ipv6('::1'))
        self.assertFalse(is_loopback_ipv6('::2'))
        self.assertFalse(is_loopback_ipv6('2001:db8::1'))
    
    def test_is_link_local_ipv6(self):
        """Test IPv6 link-local detection."""
        self.assertTrue(is_link_local_ipv6('fe80::1'))
        self.assertTrue(is_link_local_ipv6('febf::1'))
        self.assertFalse(is_link_local_ipv6('fec0::1'))
        self.assertFalse(is_link_local_ipv6('2001:db8::1'))
    
    def test_is_multicast_ipv6(self):
        """Test IPv6 multicast detection."""
        self.assertTrue(is_multicast_ipv6('ff00::1'))
        self.assertTrue(is_multicast_ipv6('ff02::1'))
        self.assertFalse(is_multicast_ipv6('fe80::1'))


class TestIPv6Info(unittest.TestCase):
    """Test IPv6Info dataclass."""
    
    def test_get_ipv6_info(self):
        """Test get_ipv6_info function."""
        info = get_ipv6_info('2001:db8::1')
        
        self.assertEqual(info.compressed, '2001:db8::1')
        self.assertIn('2001', info.expanded.lower())
        self.assertFalse(info.is_private)
        self.assertFalse(info.is_loopback)
        self.assertFalse(info.is_link_local)
        self.assertFalse(info.is_multicast)


class TestGeneralIPUtilities(unittest.TestCase):
    """Test general IP utility functions."""
    
    def test_validate_ip(self):
        """Test IP validation (both v4 and v6)."""
        self.assertTrue(validate_ip('192.168.1.1'))
        self.assertTrue(validate_ip('2001:db8::1'))
        self.assertFalse(validate_ip('invalid'))
    
    def test_get_ip_version(self):
        """Test IP version detection."""
        self.assertEqual(get_ip_version('192.168.1.1'), 4)
        self.assertEqual(get_ip_version('2001:db8::1'), 6)
        self.assertEqual(get_ip_version('invalid'), 0)
    
    def test_compare_ips(self):
        """Test IP comparison."""
        self.assertEqual(compare_ips('192.168.1.1', '192.168.1.2'), -1)
        self.assertEqual(compare_ips('192.168.1.2', '192.168.1.1'), 1)
        self.assertEqual(compare_ips('192.168.1.1', '192.168.1.1'), 0)
        
        self.assertEqual(compare_ips('::1', '::2'), -1)
        self.assertEqual(compare_ips('::2', '::1'), 1)
        self.assertEqual(compare_ips('::1', '::1'), 0)
    
    def test_compare_ips_different_versions(self):
        """Test comparing IPv4 and IPv6 raises error."""
        with self.assertRaises(ValueError):
            compare_ips('192.168.1.1', '::1')
    
    def test_sort_ips(self):
        """Test IP sorting."""
        ips = ['192.168.1.3', '192.168.1.1', '192.168.1.2']
        sorted_ips = sort_ips(ips)
        self.assertEqual(sorted_ips, ['192.168.1.1', '192.168.1.2', '192.168.1.3'])
        
        # IPv6 sorting
        ips6 = ['::3', '::1', '::2']
        sorted_ips6 = sort_ips(ips6)
        self.assertEqual(sorted_ips6, ['::1', '::2', '::3'])
    
    def test_parse_cidr(self):
        """Test CIDR parsing."""
        addr, prefix = parse_cidr('192.168.1.0/24')
        self.assertEqual(addr, '192.168.1.0')
        self.assertEqual(prefix, 24)
        
        addr, prefix = parse_cidr('2001:db8::/32')
        self.assertEqual(addr, '2001:db8::')
        self.assertEqual(prefix, 32)
    
    def test_parse_cidr_invalid(self):
        """Test CIDR parsing with invalid input."""
        with self.assertRaises(ValueError):
            parse_cidr('192.168.1.0')  # Missing prefix
    
    def test_is_public_ip(self):
        """Test public IP detection."""
        self.assertTrue(is_public_ip('8.8.8.8'))
        self.assertTrue(is_public_ip('1.1.1.1'))
        self.assertFalse(is_public_ip('192.168.1.1'))
        self.assertFalse(is_public_ip('10.0.0.1'))
        self.assertFalse(is_public_ip('127.0.0.1'))
        self.assertFalse(is_public_ip('169.254.1.1'))
    
    def test_get_local_ip_ranges(self):
        """Test getting local IP ranges."""
        ranges = get_local_ip_ranges()
        self.assertEqual(len(ranges), 3)
        self.assertIn(('10.0.0.0', '10.255.255.255'), ranges)
        self.assertIn(('172.16.0.0', '172.31.255.255'), ranges)
        self.assertIn(('192.168.0.0', '192.168.255.255'), ranges)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_ipv4_boundaries(self):
        """Test IPv4 address boundaries."""
        self.assertTrue(validate_ipv4('0.0.0.0'))
        self.assertTrue(validate_ipv4('255.255.255.255'))
        self.assertEqual(ipv4_to_int('0.0.0.0'), 0)
        self.assertEqual(ipv4_to_int('255.255.255.255'), 0xFFFFFFFF)
    
    def test_ipv6_boundaries(self):
        """Test IPv6 address boundaries."""
        self.assertTrue(validate_ipv6('::'))
        self.assertEqual(ipv6_to_int('::'), 0)
    
    def test_subnet_boundaries(self):
        """Test subnet boundary calculations."""
        # /0 network
        info = get_subnet_info('0.0.0.0/0')
        self.assertEqual(info.total_hosts, 4294967296)
        
        # /32 network
        info = get_subnet_info('192.168.1.1/32')
        self.assertEqual(info.total_hosts, 1)
        self.assertEqual(info.usable_hosts, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)