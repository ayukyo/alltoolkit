#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Network Utilities Test Suite"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # URL utilities
    is_valid_url, parse_url, build_url, extract_urls, normalize_url,
    # IPv4 utilities
    is_valid_ipv4, ip_to_int, int_to_ip, ip_in_range, get_network_address,
    get_broadcast_address, cidr_to_netmask, netmask_to_cidr, get_hostmask,
    is_private_ip, is_loopback_ip,
    # IPv6 utilities
    is_valid_ipv6, compress_ipv6, expand_ipv6,
    # Port utilities
    is_valid_port, get_service_name, categorize_port,
    # MAC utilities
    is_valid_mac, normalize_mac, generate_mac, get_mac_oui,
    # Network diagnostics
    get_local_hostname, resolve_hostname, resolve_ip_to_hostname, is_reachable,
    # HTTP utilities
    parse_content_type, is_json_content_type, is_html_content_type,
    parse_http_status, is_success_status, is_redirect_status,
    is_client_error_status, is_server_error_status,
    # Domain utilities
    is_valid_domain, extract_domain, get_base_domain, is_subdomain,
    # Utility functions
    bytes_to_human, human_to_bytes, format_bandwidth, calculate_transfer_time
)


class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def test(self, name, condition):
        if condition:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            print(f"  ✗ {name}")
    
    def report(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Tests: {total} | Passed: {self.passed} | Failed: {self.failed}")
        if self.failed == 0:
            print("All tests passed!")
        else:
            print(f"{self.failed} test(s) failed.")
        print('='*60)
        return self.failed == 0


def run_tests():
    runner = TestRunner()
    
    # ========================================================================
    # URL Utilities Tests
    # ========================================================================
    print("\nURL Utilities Tests")
    print("="*60)
    
    runner.test("is_valid_url accepts https URL", is_valid_url("https://example.com") == True)
    runner.test("is_valid_url accepts http URL", is_valid_url("http://test.org/path") == True)
    runner.test("is_valid_url rejects invalid URL", is_valid_url("not-a-url") == False)
    runner.test("is_valid_url rejects empty string", is_valid_url("") == False)
    runner.test("is_valid_url rejects None", is_valid_url(None) == False)
    
    runner.test("parse_url extracts components", parse_url("https://example.com:8080/path?q=1")['port'] == 8080)
    runner.test("parse_url extracts domain", parse_url("https://example.com/path")['domain'] == "example.com")
    runner.test("parse_url handles empty URL", parse_url("") == {})
    
    runner.test("build_url constructs URL", build_url("https", "example.com", "/path", port=8080) == "https://example.com:8080/path")
    runner.test("build_url adds query params", "key=value" in build_url("https", "example.com", query_params={"key": "value"}))
    
    runner.test("extract_urls finds URLs", len(extract_urls("Visit https://example.com and http://test.org")) == 2)
    runner.test("extract_urls returns empty list", extract_urls("no urls here") == [])
    
    runner.test("normalize_url adds scheme", normalize_url("example.com").startswith("http://"))
    runner.test("normalize_url handles full URL", normalize_url("https://EXAMPLE.com") == "https://example.com")
    
    # ========================================================================
    # IPv4 Utilities Tests
    # ========================================================================
    print("\nIPv4 Utilities Tests")
    print("="*60)
    
    runner.test("is_valid_ipv4 accepts valid IP", is_valid_ipv4("192.168.1.1") == True)
    runner.test("is_valid_ipv4 accepts 0.0.0.0", is_valid_ipv4("0.0.0.0") == True)
    runner.test("is_valid_ipv4 accepts 255.255.255.255", is_valid_ipv4("255.255.255.255") == True)
    runner.test("is_valid_ipv4 rejects invalid octet", is_valid_ipv4("256.1.1.1") == False)
    runner.test("is_valid_ipv4 rejects too few octets", is_valid_ipv4("192.168.1") == False)
    runner.test("is_valid_ipv4 rejects empty string", is_valid_ipv4("") == False)
    runner.test("is_valid_ipv4 rejects None", is_valid_ipv4(None) == False)
    
    runner.test("ip_to_int converts correctly", ip_to_int("192.168.1.1") == 3232235777)
    runner.test("ip_to_int roundtrip", ip_to_int(int_to_ip(3232235777)) == 3232235777)
    
    runner.test("int_to_ip converts correctly", int_to_ip(3232235777) == "192.168.1.1")
    runner.test("int_to_ip roundtrip", int_to_ip(ip_to_int("10.0.0.1")) == "10.0.0.1")
    
    runner.test("ip_in_range detects in range", ip_in_range("192.168.1.50", "192.168.1.1", "192.168.1.255") == True)
    runner.test("ip_in_range detects out of range", ip_in_range("192.168.2.1", "192.168.1.1", "192.168.1.255") == False)
    
    runner.test("get_network_address calculates correctly", get_network_address("192.168.1.100", "255.255.255.0") == "192.168.1.0")
    runner.test("get_broadcast_address calculates correctly", get_broadcast_address("192.168.1.100", "255.255.255.0") == "192.168.1.255")
    
    runner.test("cidr_to_netmask /24", cidr_to_netmask(24) == "255.255.255.0")
    runner.test("cidr_to_netmask /16", cidr_to_netmask(16) == "255.255.0.0")
    runner.test("cidr_to_netmask /8", cidr_to_netmask(8) == "255.0.0.0")
    runner.test("cidr_to_netmask /32", cidr_to_netmask(32) == "255.255.255.255")
    
    runner.test("netmask_to_cidr /24", netmask_to_cidr("255.255.255.0") == 24)
    runner.test("netmask_to_cidr /16", netmask_to_cidr("255.255.0.0") == 16)
    
    runner.test("get_hostmask calculates correctly", get_hostmask("255.255.255.0") == "0.0.0.255")
    
    runner.test("is_private_ip detects 10.x.x.x", is_private_ip("10.0.0.1") == True)
    runner.test("is_private_ip detects 172.16.x.x", is_private_ip("172.16.0.1") == True)
    runner.test("is_private_ip detects 192.168.x.x", is_private_ip("192.168.1.1") == True)
    runner.test("is_private_ip detects loopback", is_private_ip("127.0.0.1") == True)
    runner.test("is_private_ip rejects public IP", is_private_ip("8.8.8.8") == False)
    
    runner.test("is_loopback_ip detects 127.0.0.1", is_loopback_ip("127.0.0.1") == True)
    runner.test("is_loopback_ip rejects non-loopback", is_loopback_ip("192.168.1.1") == False)
    
    # ========================================================================
    # IPv6 Utilities Tests
    # ========================================================================
    print("\nIPv6 Utilities Tests")
    print("="*60)
    
    runner.test("is_valid_ipv6 accepts full address", is_valid_ipv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334") == True)
    runner.test("is_valid_ipv6 accepts compressed", is_valid_ipv6("::1") == True)
    runner.test("is_valid_ipv6 accepts ::", is_valid_ipv6("::") == True)
    runner.test("is_valid_ipv6 accepts mixed compression", is_valid_ipv6("2001:db8::1") == True)
    runner.test("is_valid_ipv6 rejects invalid", is_valid_ipv6("2001:db8:::1") == False)
    runner.test("is_valid_ipv6 rejects too many parts", is_valid_ipv6("1:2:3:4:5:6:7:8:9") == False)
    
    runner.test("compress_ipv6 compresses zeros", compress_ipv6("2001:0db8:0000:0000:0000:0000:0000:0001") == "2001:db8::1")
    runner.test("compress_ipv6 handles all zeros", compress_ipv6("0000:0000:0000:0000:0000:0000:0000:0000") == "::")
    runner.test("compress_ipv6 handles loopback", compress_ipv6("0000:0000:0000:0000:0000:0000:0000:0001") == "::1")
    
    runner.test("expand_ipv6 expands ::1", expand_ipv6("::1") == "0000:0000:0000:0000:0000:0000:0000:0001")
    runner.test("expand_ipv6 expands ::", expand_ipv6("::") == "0000:0000:0000:0000:0000:0000:0000:0000")
    runner.test("expand_ipv6 roundtrip", expand_ipv6(compress_ipv6("2001:db8::1")) == expand_ipv6("2001:db8::1"))
    
    # ========================================================================
    # Port Utilities Tests
    # ========================================================================
    print("\nPort Utilities Tests")
    print("="*60)
    
    runner.test("is_valid_port accepts 80", is_valid_port(80) == True)
    runner.test("is_valid_port accepts string", is_valid_port("443") == True)
    runner.test("is_valid_port accepts 65535", is_valid_port(65535) == True)
    runner.test("is_valid_port rejects 0", is_valid_port(0) == False)
    runner.test("is_valid_port rejects 65536", is_valid_port(65536) == False)
    runner.test("is_valid_port rejects negative", is_valid_port(-1) == False)
    runner.test("is_valid_port rejects invalid string", is_valid_port("abc") == False)
    
    runner.test("get_service_name returns HTTP", get_service_name(80) == "HTTP")
    runner.test("get_service_name returns HTTPS", get_service_name(443) == "HTTPS")
    runner.test("get_service_name returns SSH", get_service_name(22) == "SSH")
    runner.test("get_service_name returns None for unknown", get_service_name(12345) == None)
    
    runner.test("categorize_port well-known", categorize_port(80) == "well-known")
    runner.test("categorize_port registered", categorize_port(8080) == "registered")
    runner.test("categorize_port dynamic", categorize_port(50000) == "dynamic")
    runner.test("categorize_port invalid", categorize_port(70000) == "invalid")
    
    # ========================================================================
    # MAC Address Utilities Tests
    # ========================================================================
    print("\nMAC Address Utilities Tests")
    print("="*60)
    
    runner.test("is_valid_mac accepts colon format", is_valid_mac("00:1A:2B:3C:4D:5E") == True)
    runner.test("is_valid_mac accepts dash format", is_valid_mac("00-1A-2B-3C-4D-5E") == True)
    runner.test("is_valid_mac accepts lowercase", is_valid_mac("aa:bb:cc:dd:ee:ff") == True)
    runner.test("is_valid_mac rejects invalid", is_valid_mac("00:1A:2B:3C:4D") == False)
    runner.test("is_valid_mac rejects empty", is_valid_mac("") == False)
    
    runner.test("normalize_mac converts to colons", normalize_mac("00-1A-2B-3C-4D-5E", ":") == "00:1A:2B:3C:4D:5E")
    runner.test("normalize_mac converts to dashes", normalize_mac("00:1A:2B:3C:4D:5E", "-") == "00-1A-2B-3C-4D-5E")
    
    runner.test("generate_mac returns valid format", is_valid_mac(generate_mac()) == True)
    runner.test("generate_mac unicast bit", int(generate_mac(unicast=True).split(':')[0], 16) & 0x01 == 0)
    
    runner.test("get_mac_oui extracts OUI", get_mac_oui("00:1A:2B:3C:4D:5E") == "00:1A:2B")
    
    # ========================================================================
    # Network Diagnostics Tests
    # ========================================================================
    print("\nNetwork Diagnostics Tests")
    print("="*60)
    
    runner.test("get_local_hostname returns string", isinstance(get_local_hostname(), str) == True)
    runner.test("get_local_hostname not empty", len(get_local_hostname()) > 0)
    
    runner.test("resolve_hostname localhost", "127.0.0.1" in resolve_hostname("localhost"))
    runner.test("resolve_hostname empty for invalid", resolve_hostname("invalid.host.that.does.not.exist") == [])
    
    runner.test("resolve_ip_to_hostname localhost", resolve_ip_to_hostname("127.0.0.1") in ["localhost", None])
    
    # ========================================================================
    # HTTP Utilities Tests
    # ========================================================================
    print("\nHTTP Utilities Tests")
    print("="*60)
    
    runner.test("parse_content_type simple", parse_content_type("text/html") == {'type': 'text', 'subtype': 'html'})
    runner.test("parse_content_type with charset", parse_content_type("text/html; charset=utf-8")['charset'] == "utf-8")
    runner.test("parse_content_type application/json", parse_content_type("application/json")['subtype'] == "json")
    
    runner.test("is_json_content_type detects JSON", is_json_content_type("application/json") == True)
    runner.test("is_json_content_type detects JSON with charset", is_json_content_type("application/json; charset=utf-8") == True)
    runner.test("is_json_content_type rejects HTML", is_json_content_type("text/html") == False)
    
    runner.test("is_html_content_type detects HTML", is_html_content_type("text/html") == True)
    runner.test("is_html_content_type rejects JSON", is_html_content_type("application/json") == False)
    
    runner.test("parse_http_status 200 OK", parse_http_status("HTTP/1.1 200 OK")['status_code'] == 200)
    runner.test("parse_http_status extracts version", parse_http_status("HTTP/1.1 200 OK")['version'] == "HTTP/1.1")
    runner.test("parse_http_status extracts reason", parse_http_status("HTTP/1.1 200 OK")['reason'] == "OK")
    
    runner.test("is_success_status 200", is_success_status(200) == True)
    runner.test("is_success_status 204", is_success_status(204) == True)
    runner.test("is_success_status 404", is_success_status(404) == False)
    
    runner.test("is_redirect_status 301", is_redirect_status(301) == True)
    runner.test("is_redirect_status 302", is_redirect_status(302) == True)
    runner.test("is_redirect_status 200", is_redirect_status(200) == False)
    
    runner.test("is_client_error_status 400", is_client_error_status(400) == True)
    runner.test("is_client_error_status 404", is_client_error_status(404) == True)
    runner.test("is_client_error_status 500", is_client_error_status(500) == False)
    
    runner.test("is_server_error_status 500", is_server_error_status(500) == True)
    runner.test("is_server_error_status 503", is_server_error_status(503) == True)
    runner.test("is_server_error_status 404", is_server_error_status(404) == False)
    
    # ========================================================================
    # Domain Utilities Tests
    # ========================================================================
    print("\nDomain Utilities Tests")
    print("="*60)
    
    runner.test("is_valid_domain accepts example.com", is_valid_domain("example.com") == True)
    runner.test("is_valid_domain accepts subdomain", is_valid_domain("www.example.com") == True)
    runner.test("is_valid_domain accepts multi-level TLD", is_valid_domain("example.co.uk") == True)
    runner.test("is_valid_domain rejects single label", is_valid_domain("localhost") == False)
    runner.test("is_valid_domain rejects empty", is_valid_domain("") == False)
    runner.test("is_valid_domain rejects leading dash", is_valid_domain("-example.com") == False)
    runner.test("is_valid_domain rejects trailing dash", is_valid_domain("example-.com") == False)
    
    runner.test("extract_domain from URL", extract_domain("https://www.example.com/path") == "www.example.com")
    runner.test("extract_domain from simple URL", extract_domain("http://test.org") == "test.org")
    
    runner.test("get_base_domain removes subdomain", get_base_domain("www.example.com") == "example.com")
    runner.test("get_base_domain keeps two labels", get_base_domain("example.co.uk") == "co.uk")
    
    runner.test("is_subdomain detects subdomain", is_subdomain("www.example.com", "example.com") == True)
    runner.test("is_subdomain same domain", is_subdomain("example.com", "example.com") == True)
    runner.test("is_subdomain different domain", is_subdomain("other.com", "example.com") == False)
    
    # ========================================================================
    # Utility Functions Tests
    # ========================================================================
    print("\nUtility Functions Tests")
    print("="*60)
    
    runner.test("bytes_to_human bytes", bytes_to_human(512) == "512.00 B")
    runner.test("bytes_to_human KB", bytes_to_human(1536) == "1.50 KB")
    runner.test("bytes_to_human MB", bytes_to_human(1572864) == "1.50 MB")
    runner.test("bytes_to_human GB", bytes_to_human(1610612736) == "1.50 GB")
    
    runner.test("human_to_bytes bytes", human_to_bytes("512 B") == 512)
    runner.test("human_to_bytes KB", human_to_bytes("1.5 KB") == 1536)
    runner.test("human_to_bytes MB", human_to_bytes("1 MB") == 1048576)
    
    runner.test("format_bandwidth bps", format_bandwidth(500) == "500.00 bps")
    runner.test("format_bandwidth Kbps", format_bandwidth(1500) == "1.50 Kbps")
    runner.test("format_bandwidth Mbps", format_bandwidth(1500000) == "1.50 Mbps")
    
    runner.test("calculate_transfer_time basic", calculate_transfer_time(1048576, 1000000)['seconds'] > 0)
    runner.test("calculate_transfer_time has formatted", 'formatted' in calculate_transfer_time(1000, 1000))
    
    # ========================================================================
    # Report
    # ========================================================================
    return runner.report()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
