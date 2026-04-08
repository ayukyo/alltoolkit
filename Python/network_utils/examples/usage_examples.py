#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit Network Utils - Usage Examples
==========================================
Demonstrates common use cases for the network utilities module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, 'network_utils'))

from mod import (
    # URL utilities
    is_valid_url, parse_url, build_url, extract_urls, normalize_url,
    # IPv4 utilities
    is_valid_ipv4, ip_to_int, int_to_ip, ip_in_range, get_network_address,
    get_broadcast_address, cidr_to_netmask, netmask_to_cidr,
    is_private_ip, is_loopback_ip,
    # IPv6 utilities
    is_valid_ipv6, compress_ipv6, expand_ipv6,
    # Port utilities
    is_valid_port, get_service_name, categorize_port,
    # MAC utilities
    is_valid_mac, normalize_mac, generate_mac, get_mac_oui,
    # Network diagnostics
    get_local_hostname, resolve_hostname, is_reachable,
    # HTTP utilities
    parse_content_type, is_json_content_type, parse_http_status,
    is_success_status, is_server_error_status,
    # Domain utilities
    is_valid_domain, extract_domain, get_base_domain, is_subdomain,
    # Utility functions
    bytes_to_human, human_to_bytes, format_bandwidth, calculate_transfer_time
)


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def example_url_utilities():
    """Example: URL Parsing and Manipulation"""
    print_section("URL Utilities")
    
    # Validate URLs
    urls = [
        "https://www.example.com/path?query=1#section",
        "http://api.test.org:8080/v1/users",
        "ftp://files.server.net/downloads",
        "not-a-valid-url",
        ""
    ]
    
    print("\nURL Validation:")
    for url in urls:
        valid = is_valid_url(url)
        status = "✓ Valid" if valid else "✗ Invalid"
        print(f"  {status}: {url[:50]}{'...' if len(url) > 50 else ''}")
    
    # Parse URL
    print("\nURL Parsing:")
    url = "https://user:pass@api.example.com:8443/v1/users?format=json&limit=10#results"
    parsed = parse_url(url)
    print(f"  Original: {url}")
    print(f"  Scheme:   {parsed.get('scheme')}")
    print(f"  Domain:   {parsed.get('domain')}")
    print(f"  Port:     {parsed.get('port')}")
    print(f"  Path:     {parsed.get('path')}")
    print(f"  Query:    {parsed.get('query_params')}")
    
    # Build URL
    print("\nURL Building:")
    built = build_url(
        scheme="https",
        domain="api.example.com",
        path="/v2/data",
        port=443,
        query_params={"format": "json", "pretty": "true"},
        fragment="results"
    )
    print(f"  Built URL: {built}")
    
    # Extract URLs from text
    print("\nURL Extraction:")
    text = """
    Check out these resources:
    - Documentation: https://docs.example.com
    - API Reference: http://api.example.com/v1
    - Support: https://support.example.com/help
    """
    found_urls = extract_urls(text)
    print(f"  Found {len(found_urls)} URLs:")
    for u in found_urls:
        print(f"    - {u}")
    
    # Normalize URL
    print("\nURL Normalization:")
    messy_urls = ["EXAMPLE.COM/path", "www.test.org", "https://API.Example.Com:443"]
    for url in messy_urls:
        normalized = normalize_url(url)
        print(f"  {url} → {normalized}")


def example_ipv4_utilities():
    """Example: IPv4 Address Manipulation"""
    print_section("IPv4 Utilities")
    
    # Validate IPs
    print("\nIP Validation:")
    ips = ["192.168.1.1", "10.0.0.1", "256.1.1.1", "8.8.8.8", "127.0.0.1"]
    for ip in ips:
        valid = is_valid_ipv4(ip)
        status = "✓" if valid else "✗"
        print(f"  {status} {ip}")
    
    # IP to integer conversion
    print("\nIP ↔ Integer Conversion:")
    ip = "192.168.1.100"
    ip_int = ip_to_int(ip)
    print(f"  {ip} → {ip_int}")
    print(f"  {ip_int} → {int_to_ip(ip_int)}")
    
    # Network calculations
    print("\nNetwork Calculations:")
    ip = "192.168.1.150"
    netmask = "255.255.255.0"
    print(f"  IP:       {ip}")
    print(f"  Netmask:  {netmask} (/{netmask_to_cidr(netmask)})")
    print(f"  Network:  {get_network_address(ip, netmask)}")
    print(f"  Broadcast: {get_broadcast_address(ip, netmask)}")
    
    # CIDR conversions
    print("\nCIDR Conversions:")
    cidrs = [8, 16, 24, 25, 26, 27, 28, 30, 32]
    for cidr in cidrs:
        mask = cidr_to_netmask(cidr)
        print(f"  /{cidr:2d} → {mask}")
    
    # IP range check
    print("\nIP Range Check:")
    test_ip = "192.168.1.50"
    start = "192.168.1.1"
    end = "192.168.1.255"
    in_range = ip_in_range(test_ip, start, end)
    print(f"  Is {test_ip} in range {start}-{end}? {'Yes' if in_range else 'No'}")
    
    # IP classification
    print("\nIP Classification:")
    test_ips = ["192.168.1.1", "10.0.0.1", "172.16.0.1", "8.8.8.8", "127.0.0.1"]
    for ip in test_ips:
        private = is_private_ip(ip)
        loopback = is_loopback_ip(ip)
        print(f"  {ip}: Private={private}, Loopback={loopback}")


def example_ipv6_utilities():
    """Example: IPv6 Address Manipulation"""
    print_section("IPv6 Utilities")
    
    # Validate IPv6
    print("\nIPv6 Validation:")
    ipv6s = [
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "2001:db8:85a3::8a2e:370:7334",
        "::1",
        "::",
        "fe80::1",
        "invalid:::ipv6"
    ]
    for ip in ipv6s:
        valid = is_valid_ipv6(ip)
        status = "✓" if valid else "✗"
        print(f"  {status} {ip}")
    
    # Compression
    print("\nIPv6 Compression:")
    full_addresses = [
        "2001:0db8:0000:0000:0000:0000:0000:0001",
        "0000:0000:0000:0000:0000:0000:0000:0000",
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    ]
    for addr in full_addresses:
        compressed = compress_ipv6(addr)
        print(f"  {addr}")
        print(f"    → {compressed}")
    
    # Expansion
    print("\nIPv6 Expansion:")
    compressed_addresses = ["::1", "::", "2001:db8::1", "fe80::1"]
    for addr in compressed_addresses:
        expanded = expand_ipv6(addr)
        print(f"  {addr} → {expanded}")


def example_port_utilities():
    """Example: Port Utilities"""
    print_section("Port Utilities")
    
    # Validate ports
    print("\nPort Validation:")
    ports = [22, 80, 443, 8080, 0, 65535, 65536, -1]
    for port in ports:
        valid = is_valid_port(port)
        status = "✓" if valid else "✗"
        print(f"  {status} Port {port}")
    
    # Service names
    print("\nCommon Service Names:")
    common_ports = [21, 22, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 8080]
    for port in common_ports:
        service = get_service_name(port)
        if service:
            print(f"  {port:5d} → {service}")
    
    # Port categories
    print("\nPort Categories:")
    sample_ports = [22, 80, 443, 8080, 3306, 50000, 60000]
    for port in sample_ports:
        category = categorize_port(port)
        print(f"  {port:5d} → {category}")


def example_mac_utilities():
    """Example: MAC Address Utilities"""
    print_section("MAC Address Utilities")
    
    # Validate MAC
    print("\nMAC Validation:")
    macs = [
        "00:1A:2B:3C:4D:5E",
        "00-1A-2B-3C-4D-5E",
        "aa:bb:cc:dd:ee:ff",
        "00:1A:2B:3C:4D",
        "invalid"
    ]
    for mac in macs:
        valid = is_valid_mac(mac)
        status = "✓" if valid else "✗"
        print(f"  {status} {mac}")
    
    # Normalize MAC
    print("\nMAC Normalization:")
    macs = ["00-1A-2B-3C-4D-5E", "aa:bb:cc:dd:ee:ff"]
    for mac in macs:
        normalized_colon = normalize_mac(mac, ":")
        normalized_dash = normalize_mac(mac, "-")
        print(f"  {mac} → Colon: {normalized_colon}, Dash: {normalized_dash}")
    
    # Generate MAC
    print("\nMAC Generation:")
    print(f"  Random Unicast:   {generate_mac(randomize=True, unicast=True)}")
    print(f"  Random Multicast: {generate_mac(randomize=True, unicast=False)}")
    print(f"  Zero MAC:         {generate_mac(randomize=False)}")
    
    # OUI extraction
    print("\nOUI Extraction:")
    mac = "00:1A:2B:3C:4D:5E"
    oui = get_mac_oui(mac)
    print(f"  MAC: {mac}")
    print(f"  OUI: {oui} (first 3 octets)")


def example_http_utilities():
    """Example: HTTP Utilities"""
    print_section("HTTP Utilities")
    
    # Parse Content-Type
    print("\nContent-Type Parsing:")
    content_types = [
        "text/html",
        "application/json",
        "application/json; charset=utf-8",
        "text/plain; charset=iso-8859-1",
        "multipart/form-data; boundary=----WebKitFormBoundary"
    ]
    for ct in content_types:
        parsed = parse_content_type(ct)
        print(f"  {ct}")
        print(f"    → Type: {parsed.get('type')}, Subtype: {parsed.get('subtype')}, Params: { {k:v for k,v in parsed.items() if k not in ['type', 'subtype']} }")
    
    # Content-Type detection
    print("\nContent-Type Detection:")
    tests = [
        ("application/json", "JSON"),
        ("application/json; charset=utf-8", "JSON"),
        ("text/html", "HTML"),
        ("text/html; charset=utf-8", "HTML"),
        ("text/plain", "Other")
    ]
    for ct, expected in tests:
        is_json = is_json_content_type(ct)
        print(f"  {ct}: is_json={is_json}")
    
    # Parse HTTP status
    print("\nHTTP Status Parsing:")
    status_lines = [
        "HTTP/1.1 200 OK",
        "HTTP/1.1 404 Not Found",
        "HTTP/2 500 Internal Server Error",
        "HTTP/1.0 301 Moved Permanently"
    ]
    for line in status_lines:
        parsed = parse_http_status(line)
        code = parsed['status_code']
        success = is_success_status(code)
        error = is_server_error_status(code)
        print(f"  {line}")
        print(f"    → Code: {code}, Success: {success}, Server Error: {error}")


def example_domain_utilities():
    """Example: Domain Utilities"""
    print_section("Domain Utilities")
    
    # Validate domains
    print("\nDomain Validation:")
    domains = [
        "example.com",
        "www.example.com",
        "sub.domain.example.co.uk",
        "localhost",
        "-invalid.com",
        "invalid-.com"
    ]
    for domain in domains:
        valid = is_valid_domain(domain)
        status = "✓" if valid else "✗"
        print(f"  {status} {domain}")
    
    # Extract domain from URL
    print("\nDomain Extraction:")
    urls = [
        "https://www.example.com/path/to/page",
        "http://api.sub.domain.co.uk:8080/v1",
        "ftp://files.server.net/downloads/file.zip"
    ]
    for url in urls:
        domain = extract_domain(url)
        print(f"  {url}")
        print(f"    → Domain: {domain}")
    
    # Base domain extraction
    print("\nBase Domain Extraction:")
    domains = [
        "www.example.com",
        "mail.server.example.com",
        "example.co.uk",
        "sub.domain.example.co.uk"
    ]
    for domain in domains:
        base = get_base_domain(domain)
        print(f"  {domain} → {base}")
    
    # Subdomain check
    print("\nSubdomain Check:")
    checks = [
        ("www.example.com", "example.com"),
        ("mail.server.example.com", "example.com"),
        ("example.com", "example.com"),
        ("other.com", "example.com")
    ]
    for child, parent in checks:
        is_sub = is_subdomain(child, parent)
        print(f"  Is '{child}' a subdomain of '{parent}'? {'Yes' if is_sub else 'No'}")


def example_utility_functions():
    """Example: Utility Functions"""
    print_section("Utility Functions")
    
    # Bytes to human-readable
    print("\nBytes to Human-Readable:")
    sizes = [512, 1536, 1048576, 1572864, 1073741824, 1610612736]
    for size in sizes:
        human = bytes_to_human(size)
        print(f"  {size:12d} bytes → {human}")
    
    # Human-readable to bytes
    print("\nHuman-Readable to Bytes:")
    human_sizes = ["512 B", "1.5 KB", "1 MB", "2.5 GB", "1 TB"]
    for h in human_sizes:
        bytes_val = human_to_bytes(h)
        print(f"  {h:10s} → {bytes_val:,} bytes")
    
    # Bandwidth formatting
    print("\nBandwidth Formatting:")
    bandwidths = [500, 1500, 1500000, 1500000000]
    for bw in bandwidths:
        formatted = format_bandwidth(bw)
        print(f"  {bw:12d} bps → {formatted}")
    
    # Transfer time calculation
    print("\nTransfer Time Calculation:")
    scenarios = [
        (1048576, 1000000, "1 MB file over 1 Mbps"),
        (1073741824, 100000000, "1 GB file over 100 Mbps"),
        (5368709120, 1000000000, "5 GB file over 1 Gbps"),
    ]
    for size, bandwidth, desc in scenarios:
        result = calculate_transfer_time(size, bandwidth)
        print(f"  {desc}")
        print(f"    → {result['formatted']}")


def example_network_diagnostics():
    """Example: Network Diagnostics"""
    print_section("Network Diagnostics")
    
    # Local hostname
    print("\nLocal Hostname:")
    hostname = get_local_hostname()
    print(f"  Hostname: {hostname}")
    
    # Resolve hostname
    print("\nHostname Resolution:")
    hosts = ["localhost", "google.com"]
    for host in hosts:
        ips = resolve_hostname(host)
        if ips:
            print(f"  {host} → {', '.join(ips[:3])}")
        else:
            print(f"  {host} → (resolution failed)")
    
    # Reachability check (optional, may fail without network)
    print("\nReachability Check (requires network):")
    tests = [
        ("127.0.0.1", 22, "Local SSH"),
        ("127.0.0.1", 80, "Local HTTP"),
    ]
    for host, port, desc in tests:
        reachable = is_reachable(host, port, timeout=0.5)
        status = "✓ Reachable" if reachable else "✗ Not reachable"
        print(f"  {desc} ({host}:{port}): {status}")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("  AllToolkit Network Utils - Usage Examples")
    print("="*60)
    
    example_url_utilities()
    example_ipv4_utilities()
    example_ipv6_utilities()
    example_port_utilities()
    example_mac_utilities()
    example_http_utilities()
    example_domain_utilities()
    example_utility_functions()
    example_network_diagnostics()
    
    print("\n" + "="*60)
    print("  Examples Complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
