#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Network Utilities Module
======================================
A comprehensive network utility module for Python with zero external dependencies.

Features:
    - URL parsing and validation
    - IP address manipulation (IPv4/IPv6)
    - Port utilities
    - Network diagnostics helpers
    - HTTP-related utilities
    - Domain/hostname utilities
    - MAC address utilities

Author: AllToolkit Contributors
License: MIT
"""

import re
import socket
import struct
import random
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse, parse_qs, urlencode


# ============================================================================
# URL Utilities
# ============================================================================

def is_valid_url(url: str) -> bool:
    """
    Validate if a string is a valid URL.
    
    Args:
        url: The URL string to validate
    
    Returns:
        True if valid URL, False otherwise
    
    Example:
        >>> is_valid_url("https://example.com/path?query=1")
        True
        >>> is_valid_url("not-a-url")
        False
    """
    if not url or not isinstance(url, str):
        return False
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def parse_url(url: str) -> Dict[str, Any]:
    """
    Parse a URL into its components.
    
    Args:
        url: The URL to parse
    
    Returns:
        Dictionary with url components: scheme, netloc, domain, port, path, 
        query, fragment, query_params
    
    Example:
        >>> parse_url("https://example.com:8080/path?query=1#section")
        {'scheme': 'https', 'netloc': 'example.com:8080', 'domain': 'example.com', 
         'port': 8080, 'path': '/path', 'query': 'query=1', 'fragment': 'section',
         'query_params': {'query': ['1']}}
    """
    if not url:
        return {}
    
    parsed = urlparse(url)
    
    # Extract domain and port
    domain = parsed.hostname or ""
    port = parsed.port
    
    # Parse query parameters
    query_params = parse_qs(parsed.query)
    
    return {
        'scheme': parsed.scheme,
        'netloc': parsed.netloc,
        'domain': domain,
        'port': port,
        'path': parsed.path,
        'query': parsed.query,
        'fragment': parsed.fragment,
        'query_params': query_params,
        'username': parsed.username,
        'password': parsed.password
    }


def build_url(scheme: str, domain: str, path: str = "", 
              port: Optional[int] = None, query_params: Optional[Dict] = None,
              fragment: str = "") -> str:
    """
    Build a URL from components.
    
    Args:
        scheme: URL scheme (http, https, etc.)
        domain: Domain name
        path: URL path
        port: Optional port number
        query_params: Optional query parameters dict
        fragment: URL fragment
    
    Returns:
        Constructed URL string
    
    Example:
        >>> build_url("https", "example.com", "/path", port=8080, query_params={"key": "value"})
        'https://example.com:8080/path?key=value'
    """
    netloc = domain
    if port:
        netloc = f"{domain}:{port}"
    
    url = f"{scheme}://{netloc}{path}"
    
    if query_params:
        query_string = urlencode(query_params, doseq=True)
        url = f"{url}?{query_string}"
    
    if fragment:
        url = f"{url}#{fragment}"
    
    return url


def extract_urls(text: str) -> List[str]:
    """
    Extract all URLs from text.
    
    Args:
        text: Text to search for URLs
    
    Returns:
        List of found URLs
    
    Example:
        >>> extract_urls("Visit https://example.com and http://test.org")
        ['https://example.com', 'http://test.org']
    """
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(url_pattern, text)


def normalize_url(url: str) -> str:
    """
    Normalize a URL (add scheme if missing, lowercase domain, etc.).
    
    Args:
        url: URL to normalize
    
    Returns:
        Normalized URL
    
    Example:
        >>> normalize_url("example.com/path")
        'http://example.com/path'
    """
    if not url:
        return ""
    
    # Add scheme if missing
    if not url.startswith(('http://', 'https://', 'ftp://')):
        url = 'http://' + url
    
    parsed = urlparse(url)
    
    # Rebuild with lowercase scheme and domain
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    
    normalized = f"{scheme}://{netloc}{parsed.path}"
    
    if parsed.query:
        normalized += f"?{parsed.query}"
    if parsed.fragment:
        normalized += f"#{parsed.fragment}"
    
    return normalized


# ============================================================================
# IP Address Utilities (IPv4)
# ============================================================================

def is_valid_ipv4(ip: str) -> bool:
    """
    Validate if a string is a valid IPv4 address.
    
    Args:
        ip: IP address string to validate
    
    Returns:
        True if valid IPv4, False otherwise
    
    Example:
        >>> is_valid_ipv4("192.168.1.1")
        True
        >>> is_valid_ipv4("256.1.1.1")
        False
    """
    if not ip or not isinstance(ip, str):
        return False
    
    pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    match = re.match(pattern, ip)
    
    if not match:
        return False
    
    # Check each octet is 0-255
    for group in match.groups():
        if int(group) > 255:
            return False
    
    return True


def ip_to_int(ip: str) -> int:
    """
    Convert IPv4 address to integer.
    
    Args:
        ip: IPv4 address string
    
    Returns:
        Integer representation
    
    Example:
        >>> ip_to_int("192.168.1.1")
        3232235777
    """
    if not is_valid_ipv4(ip):
        raise ValueError(f"Invalid IPv4 address: {ip}")
    
    octets = ip.split('.')
    return (int(octets[0]) << 24) + (int(octets[1]) << 16) + \
           (int(octets[2]) << 8) + int(octets[3])


def int_to_ip(num: int) -> str:
    """
    Convert integer to IPv4 address.
    
    Args:
        num: Integer representation
    
    Returns:
        IPv4 address string
    
    Example:
        >>> int_to_ip(3232235777)
        '192.168.1.1'
    """
    return f"{(num >> 24) & 255}.{(num >> 16) & 255}.{(num >> 8) & 255}.{num & 255}"


def ip_in_range(ip: str, start_ip: str, end_ip: str) -> bool:
    """
    Check if an IP address is within a range.
    
    Args:
        ip: IP to check
        start_ip: Range start IP
        end_ip: Range end IP
    
    Returns:
        True if IP is in range
    
    Example:
        >>> ip_in_range("192.168.1.50", "192.168.1.1", "192.168.1.255")
        True
    """
    try:
        ip_int = ip_to_int(ip)
        start_int = ip_to_int(start_ip)
        end_int = ip_to_int(end_ip)
        return start_int <= ip_int <= end_int
    except ValueError:
        return False


def get_network_address(ip: str, netmask: str) -> str:
    """
    Calculate network address from IP and netmask.
    
    Args:
        ip: IP address
        netmask: Network mask (e.g., "255.255.255.0")
    
    Returns:
        Network address
    
    Example:
        >>> get_network_address("192.168.1.100", "255.255.255.0")
        '192.168.1.0'
    """
    ip_int = ip_to_int(ip)
    mask_int = ip_to_int(netmask)
    network_int = ip_int & mask_int
    return int_to_ip(network_int)


def get_broadcast_address(ip: str, netmask: str) -> str:
    """
    Calculate broadcast address from IP and netmask.
    
    Args:
        ip: IP address
        netmask: Network mask
    
    Returns:
        Broadcast address
    
    Example:
        >>> get_broadcast_address("192.168.1.100", "255.255.255.0")
        '192.168.1.255'
    """
    ip_int = ip_to_int(ip)
    mask_int = ip_to_int(netmask)
    wildcard_int = mask_int ^ 0xFFFFFFFF
    broadcast_int = ip_int | wildcard_int
    return int_to_ip(broadcast_int)


def cidr_to_netmask(cidr: int) -> str:
    """
    Convert CIDR notation to netmask.
    
    Args:
        cidr: CIDR prefix length (0-32)
    
    Returns:
        Netmask string
    
    Example:
        >>> cidr_to_netmask(24)
        '255.255.255.0'
    """
    if not 0 <= cidr <= 32:
        raise ValueError("CIDR must be between 0 and 32")
    
    mask_int = (0xFFFFFFFF << (32 - cidr)) & 0xFFFFFFFF
    return int_to_ip(mask_int)


def netmask_to_cidr(netmask: str) -> int:
    """
    Convert netmask to CIDR notation.
    
    Args:
        netmask: Netmask string
    
    Returns:
        CIDR prefix length
    
    Example:
        >>> netmask_to_cidr("255.255.255.0")
        24
    """
    mask_int = ip_to_int(netmask)
    return bin(mask_int).count('1')


def get_hostmask(netmask: str) -> str:
    """
    Get hostmask (wildcard mask) from netmask.
    
    Args:
        netmask: Network mask
    
    Returns:
        Hostmask string
    
    Example:
        >>> get_hostmask("255.255.255.0")
        '0.0.0.255'
    """
    mask_int = ip_to_int(netmask)
    hostmask_int = mask_int ^ 0xFFFFFFFF
    return int_to_ip(hostmask_int)


def is_private_ip(ip: str) -> bool:
    """
    Check if IP is in private range.
    
    Args:
        ip: IP address to check
    
    Returns:
        True if private IP
    
    Example:
        >>> is_private_ip("192.168.1.1")
        True
        >>> is_private_ip("8.8.8.8")
        False
    """
    if not is_valid_ipv4(ip):
        return False
    
    octets = [int(x) for x in ip.split('.')]
    
    # 10.0.0.0/8
    if octets[0] == 10:
        return True
    
    # 172.16.0.0/12
    if octets[0] == 172 and 16 <= octets[1] <= 31:
        return True
    
    # 192.168.0.0/16
    if octets[0] == 192 and octets[1] == 168:
        return True
    
    # 127.0.0.0/8 (loopback)
    if octets[0] == 127:
        return True
    
    return False


def is_loopback_ip(ip: str) -> bool:
    """
    Check if IP is a loopback address.
    
    Args:
        ip: IP address to check
    
    Returns:
        True if loopback
    
    Example:
        >>> is_loopback_ip("127.0.0.1")
        True
    """
    if not is_valid_ipv4(ip):
        return False
    return ip.startswith('127.')


# ============================================================================
# IP Address Utilities (IPv6)
# ============================================================================

def is_valid_ipv6(ip: str) -> bool:
    """
    Validate if a string is a valid IPv6 address.
    
    Args:
        ip: IP address string to validate
    
    Returns:
        True if valid IPv6, False otherwise
    
    Example:
        >>> is_valid_ipv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
        True
        >>> is_valid_ipv6("::1")
        True
    """
    if not ip or not isinstance(ip, str):
        return False
    
    # Handle :: shorthand
    if ':::' in ip:
        return False
    
    # Count :: occurrences
    double_colon_count = ip.count('::')
    if double_colon_count > 1:
        return False
    
    # Expand :: if present
    if '::' in ip:
        parts = ip.split('::')
        left = parts[0].split(':') if parts[0] else []
        right = parts[1].split(':') if parts[1] else []
        
        # Filter empty strings
        left = [p for p in left if p]
        right = [p for p in right if p]
        
        missing = 8 - len(left) - len(right)
        if missing < 0:
            return False
        
        all_parts = left + ['0'] * missing + right
    else:
        all_parts = ip.split(':')
    
    if len(all_parts) != 8:
        return False
    
    # Validate each part
    for part in all_parts:
        if not part:
            return False
        if len(part) > 4:
            return False
        try:
            int(part, 16)
        except ValueError:
            return False
    
    return True


def compress_ipv6(ip: str) -> str:
    """
    Compress IPv6 address (remove leading zeros, use :: for longest zero run).
    
    Args:
        ip: IPv6 address
    
    Returns:
        Compressed IPv6 string
    
    Example:
        >>> compress_ipv6("2001:0db8:0000:0000:0000:0000:0000:0001")
        '2001:db8::1'
    """
    if not is_valid_ipv6(ip):
        raise ValueError(f"Invalid IPv6 address: {ip}")
    
    # Expand to full form first
    if '::' in ip:
        parts = ip.split('::')
        left = parts[0].split(':') if parts[0] else []
        right = parts[1].split(':') if parts[1] else []
        left = [p for p in left if p]
        right = [p for p in right if p]
        missing = 8 - len(left) - len(right)
        all_parts = left + ['0000'] * missing + right
    else:
        all_parts = ip.split(':')
    
    # Remove leading zeros from each part
    compressed = [part.lstrip('0') or '0' for part in all_parts]
    
    # Find longest run of zeros
    max_start = -1
    max_len = 0
    current_start = -1
    current_len = 0
    
    for i, part in enumerate(compressed):
        if part == '0':
            if current_start == -1:
                current_start = i
                current_len = 1
            else:
                current_len += 1
        else:
            if current_len > max_len:
                max_start = current_start
                max_len = current_len
            current_start = -1
            current_len = 0
    
    if current_len > max_len:
        max_start = current_start
        max_len = current_len
    
    # Only compress if run of 2 or more zeros
    if max_len >= 2:
        before = compressed[:max_start]
        after = compressed[max_start + max_len:]
        
        if not before and not after:
            return '::'
        elif not before:
            return '::' + ':'.join(after)
        elif not after:
            return ':'.join(before) + '::'
        else:
            return ':'.join(before) + '::' + ':'.join(after)
    
    return ':'.join(compressed)


def expand_ipv6(ip: str) -> str:
    """
    Expand IPv6 address to full form.
    
    Args:
        ip: IPv6 address (possibly compressed)
    
    Returns:
        Expanded IPv6 string
    
    Example:
        >>> expand_ipv6("::1")
        '0000:0000:0000:0000:0000:0000:0000:0001'
    """
    if not is_valid_ipv6(ip):
        raise ValueError(f"Invalid IPv6 address: {ip}")
    
    if '::' in ip:
        parts = ip.split('::')
        left = parts[0].split(':') if parts[0] else []
        right = parts[1].split(':') if parts[1] else []
        left = [p for p in left if p]
        right = [p for p in right if p]
        missing = 8 - len(left) - len(right)
        all_parts = left + ['0000'] * missing + right
    else:
        all_parts = ip.split(':')
    
    # Pad each part to 4 characters
    expanded = [part.zfill(4) for part in all_parts]
    return ':'.join(expanded)


# ============================================================================
# Port Utilities
# ============================================================================

def is_valid_port(port: Union[int, str]) -> bool:
    """
    Validate if a value is a valid port number.
    
    Args:
        port: Port number (int or string)
    
    Returns:
        True if valid port (1-65535)
    
    Example:
        >>> is_valid_port(80)
        True
        >>> is_valid_port(70000)
        False
    """
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except (ValueError, TypeError):
        return False


def get_service_name(port: int) -> Optional[str]:
    """
    Get common service name for a port.
    
    Args:
        port: Port number
    
    Returns:
        Service name or None if unknown
    
    Example:
        >>> get_service_name(80)
        'HTTP'
    """
    common_services = {
        20: 'FTP-DATA',
        21: 'FTP',
        22: 'SSH',
        23: 'TELNET',
        25: 'SMTP',
        53: 'DNS',
        67: 'DHCP-Server',
        68: 'DHCP-Client',
        69: 'TFTP',
        80: 'HTTP',
        110: 'POP3',
        119: 'NNTP',
        123: 'NTP',
        143: 'IMAP',
        161: 'SNMP',
        162: 'SNMP-TRAP',
        194: 'IRC',
        443: 'HTTPS',
        445: 'SMB',
        465: 'SMTPS',
        514: 'SYSLOG',
        587: 'SMTP-Submission',
        993: 'IMAPS',
        995: 'POP3S',
        1433: 'MSSQL',
        1521: 'Oracle',
        3306: 'MySQL',
        3389: 'RDP',
        5432: 'PostgreSQL',
        5900: 'VNC',
        6379: 'Redis',
        8080: 'HTTP-Alt',
        8443: 'HTTPS-Alt',
        9000: 'PHP-FPM',
        27017: 'MongoDB',
    }
    return common_services.get(port)


def categorize_port(port: int) -> str:
    """
    Categorize a port as well-known, registered, or dynamic.
    
    Args:
        port: Port number
    
    Returns:
        Category string
    
    Example:
        >>> categorize_port(80)
        'well-known'
    """
    if port < 1 or port > 65535:
        return 'invalid'
    elif port <= 1023:
        return 'well-known'
    elif port <= 49151:
        return 'registered'
    else:
        return 'dynamic'


# ============================================================================
# MAC Address Utilities
# ============================================================================

def is_valid_mac(mac: str) -> bool:
    """
    Validate MAC address format.
    
    Args:
        mac: MAC address string
    
    Returns:
        True if valid MAC
    
    Example:
        >>> is_valid_mac("00:1A:2B:3C:4D:5E")
        True
        >>> is_valid_mac("00-1A-2B-3C-4D-5E")
        True
    """
    if not mac or not isinstance(mac, str):
        return False
    
    # Normalize separators
    mac = mac.upper().replace('-', ':')
    
    # Check format
    pattern = r'^([0-9A-F]{2}:){5}[0-9A-F]{2}$'
    return bool(re.match(pattern, mac))


def normalize_mac(mac: str, separator: str = ':') -> str:
    """
    Normalize MAC address to specified format.
    
    Args:
        mac: MAC address string
        separator: Separator character (':' or '-')
    
    Returns:
        Normalized MAC address
    
    Example:
        >>> normalize_mac("00-1A-2B-3C-4D-5E", ":")
        '00:1A:2B:3C:4D:5E'
    """
    if not is_valid_mac(mac):
        raise ValueError(f"Invalid MAC address: {mac}")
    
    # Remove all separators and convert to uppercase
    mac_clean = mac.upper().replace('-', '').replace(':', '')
    
    # Split into pairs
    pairs = [mac_clean[i:i+2] for i in range(0, 12, 2)]
    
    return separator.join(pairs)


def generate_mac(randomize: bool = True, unicast: bool = True) -> str:
    """
    Generate a MAC address.
    
    Args:
        randomize: Generate random MAC (vs all zeros)
        unicast: Set unicast bit (vs multicast)
    
    Returns:
        Generated MAC address
    
    Example:
        >>> generate_mac()
        'XX:XX:XX:XX:XX:XX'  # Random MAC
    """
    if randomize:
        octets = [random.randint(0, 255) for _ in range(6)]
    else:
        octets = [0] * 6
    
    # Set unicast/multicast bit on first octet
    if unicast:
        octets[0] &= 0xFE  # Clear multicast bit
    else:
        octets[0] |= 0x01  # Set multicast bit
    
    return ':'.join(f'{o:02X}' for o in octets)


def get_mac_oui(mac: str) -> str:
    """
    Extract OUI (Organizationally Unique Identifier) from MAC.
    
    Args:
        mac: MAC address
    
    Returns:
        OUI portion (first 3 octets)
    
    Example:
        >>> get_mac_oui("00:1A:2B:3C:4D:5E")
        '00:1A:2B'
    """
    if not is_valid_mac(mac):
        raise ValueError(f"Invalid MAC address: {mac}")
    
    mac = normalize_mac(mac)
    parts = mac.split(':')
    return ':'.join(parts[:3])


# ============================================================================
# Network Diagnostics Helpers
# ============================================================================

def get_local_hostname() -> str:
    """
    Get the local hostname.
    
    Returns:
        Local hostname string
    
    Example:
        >>> get_local_hostname()
        'my-computer'
    """
    try:
        return socket.gethostname()
    except Exception:
        return "unknown"


def resolve_hostname(hostname: str) -> List[str]:
    """
    Resolve hostname to IP addresses.
    
    Args:
        hostname: Hostname to resolve
    
    Returns:
        List of IP addresses
    
    Example:
        >>> resolve_hostname("localhost")
        ['127.0.0.1']
    """
    try:
        result = socket.gethostbyname_ex(hostname)
        return list(result[2])
    except socket.gaierror:
        return []
    except Exception:
        return []


def resolve_ip_to_hostname(ip: str) -> Optional[str]:
    """
    Resolve IP address to hostname.
    
    Args:
        ip: IP address
    
    Returns:
        Hostname or None if resolution fails
    """
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return None


def get_all_interfaces() -> List[Dict[str, Any]]:
    """
    Get information about all network interfaces.
    
    Returns:
        List of interface info dictionaries
    
    Note: This is a basic implementation; for full interface info,
    platform-specific code may be needed.
    """
    interfaces = []
    
    try:
        hostname = socket.gethostname()
        addresses = socket.gethostbyname_ex(hostname)
        
        interfaces.append({
            'name': hostname,
            'addresses': list(addresses[2]),
            'alias': addresses[0]
        })
    except Exception:
        pass
    
    # Add localhost
    interfaces.append({
        'name': 'localhost',
        'addresses': ['127.0.0.1'],
        'alias': 'loopback'
    })
    
    return interfaces


def is_reachable(host: str, port: int, timeout: float = 1.0) -> bool:
    """
    Check if a host:port is reachable (TCP connection test).
    
    Args:
        host: Hostname or IP
        port: Port number
        timeout: Connection timeout in seconds
    
    Returns:
        True if reachable
    
    Example:
        >>> is_reachable("google.com", 443)
        True  # If connected
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False


# ============================================================================
# HTTP Utilities
# ============================================================================

def parse_content_type(content_type: str) -> Dict[str, str]:
    """
    Parse Content-Type header into media type and parameters.
    
    Args:
        content_type: Content-Type header value
    
    Returns:
        Dictionary with 'type', 'subtype', and parameters
    
    Example:
        >>> parse_content_type("text/html; charset=utf-8")
        {'type': 'text', 'subtype': 'html', 'charset': 'utf-8'}
    """
    if not content_type:
        return {}
    
    parts = content_type.split(';')
    media_type = parts[0].strip().lower()
    
    result = {}
    
    if '/' in media_type:
        type_parts = media_type.split('/')
        result['type'] = type_parts[0]
        result['subtype'] = type_parts[1] if len(type_parts) > 1 else ''
    else:
        result['type'] = media_type
        result['subtype'] = ''
    
    # Parse parameters
    for part in parts[1:]:
        if '=' in part:
            key, value = part.split('=', 1)
            result[key.strip().lower()] = value.strip().strip('"\'')
    
    return result


def is_json_content_type(content_type: str) -> bool:
    """
    Check if content type indicates JSON.
    
    Args:
        content_type: Content-Type header value
    
    Returns:
        True if JSON content type
    
    Example:
        >>> is_json_content_type("application/json; charset=utf-8")
        True
    """
    parsed = parse_content_type(content_type)
    return parsed.get('type') == 'application' and parsed.get('subtype') == 'json'


def is_html_content_type(content_type: str) -> bool:
    """
    Check if content type indicates HTML.
    
    Args:
        content_type: Content-Type header value
    
    Returns:
        True if HTML content type
    """
    parsed = parse_content_type(content_type)
    return parsed.get('type') == 'text' and parsed.get('subtype') == 'html'


def parse_http_status(status_line: str) -> Dict[str, Any]:
    """
    Parse HTTP status line.
    
    Args:
        status_line: HTTP status line (e.g., "HTTP/1.1 200 OK")
    
    Returns:
        Dictionary with version, status_code, reason
    
    Example:
        >>> parse_http_status("HTTP/1.1 200 OK")
        {'version': 'HTTP/1.1', 'status_code': 200, 'reason': 'OK'}
    """
    parts = status_line.strip().split(' ', 2)
    
    result = {
        'version': parts[0] if len(parts) > 0 else '',
        'status_code': int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0,
        'reason': parts[2] if len(parts) > 2 else ''
    }
    
    return result


def is_success_status(status_code: int) -> bool:
    """Check if HTTP status code indicates success (2xx)."""
    return 200 <= status_code < 300


def is_redirect_status(status_code: int) -> bool:
    """Check if HTTP status code indicates redirect (3xx)."""
    return 300 <= status_code < 400


def is_client_error_status(status_code: int) -> bool:
    """Check if HTTP status code indicates client error (4xx)."""
    return 400 <= status_code < 500


def is_server_error_status(status_code: int) -> bool:
    """Check if HTTP status code indicates server error (5xx)."""
    return 500 <= status_code < 600


# ============================================================================
# Domain/Hostname Utilities
# ============================================================================

def is_valid_domain(domain: str) -> bool:
    """
    Validate domain name format.
    
    Args:
        domain: Domain name to validate
    
    Returns:
        True if valid domain
    
    Example:
        >>> is_valid_domain("example.com")
        True
        >>> is_valid_domain("sub.example.co.uk")
        True
    """
    if not domain or not isinstance(domain, str):
        return False
    
    # Remove trailing dot if present
    domain = domain.rstrip('.')
    
    if not domain or len(domain) > 253:
        return False
    
    # Split into labels
    labels = domain.split('.')
    
    if len(labels) < 2:
        return False
    
    # Validate each label
    for label in labels:
        if not label or len(label) > 63:
            return False
        if label.startswith('-') or label.endswith('-'):
            return False
        if not re.match(r'^[a-zA-Z0-9-]+$', label):
            return False
    
    return True


def extract_domain(url: str) -> Optional[str]:
    """
    Extract domain from URL.
    
    Args:
        url: URL string
    
    Returns:
        Domain name or None
    
    Example:
        >>> extract_domain("https://www.example.com/path?query=1")
        'www.example.com'
    """
    if not url:
        return None
    
    parsed = urlparse(url)
    return parsed.hostname


def get_base_domain(domain: str) -> Optional[str]:
    """
    Get base domain (remove subdomains).
    
    Args:
        domain: Full domain name
    
    Returns:
        Base domain (last two labels)
    
    Example:
        >>> get_base_domain("www.sub.example.co.uk")
        'example.co.uk'  # Note: simplified, doesn't handle all TLDs
    """
    if not domain:
        return None
    
    domain = domain.rstrip('.')
    labels = domain.split('.')
    
    if len(labels) < 2:
        return domain
    
    # Simple approach: return last two labels
    # (Doesn't handle complex TLDs like .co.uk properly)
    return '.'.join(labels[-2:])


def is_subdomain(child: str, parent: str) -> bool:
    """
    Check if child domain is a subdomain of parent.
    
    Args:
        child: Child domain
        parent: Parent domain
    
    Returns:
        True if child is subdomain of parent
    
    Example:
        >>> is_subdomain("www.example.com", "example.com")
        True
    """
    if not child or not parent:
        return False
    
    child = child.rstrip('.').lower()
    parent = parent.rstrip('.').lower()
    
    return child == parent or child.endswith('.' + parent)


# ============================================================================
# Utility Functions
# ============================================================================

def bytes_to_human(size: int, precision: int = 2) -> str:
    """
    Convert bytes to human-readable format.
    
    Args:
        size: Size in bytes
        precision: Decimal precision
    
    Returns:
        Human-readable size string
    
    Example:
        >>> bytes_to_human(1536)
        '1.50 KB'
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if abs(size) < 1024.0:
            return f"{size:.{precision}f} {unit}"
        size /= 1024.0
    return f"{size:.{precision}f} EB"


def human_to_bytes(size_str: str) -> int:
    """
    Convert human-readable size to bytes.
    
    Args:
        size_str: Human-readable size (e.g., "1.5 KB")
    
    Returns:
        Size in bytes
    
    Example:
        >>> human_to_bytes("1.5 KB")
        1536
    """
    units = {
        'B': 1,
        'KB': 1024,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3,
        'TB': 1024 ** 4,
        'PB': 1024 ** 5,
        'EB': 1024 ** 6,
    }
    
    size_str = size_str.strip().upper()
    
    # Find unit
    unit = 'B'
    for u in sorted(units.keys(), key=len, reverse=True):
        if size_str.endswith(u):
            unit = u
            size_str = size_str[:-len(u)].strip()
            break
    
    try:
        value = float(size_str)
        return int(value * units[unit])
    except ValueError:
        raise ValueError(f"Invalid size format: {size_str}")


def format_bandwidth(bps: float, precision: int = 2) -> str:
    """
    Format bandwidth in bits per second to human-readable.
    
    Args:
        bps: Bits per second
        precision: Decimal precision
    
    Returns:
        Human-readable bandwidth string
    
    Example:
        >>> format_bandwidth(1500000)
        '1.50 Mbps'
    """
    for unit in ['bps', 'Kbps', 'Mbps', 'Gbps', 'Tbps']:
        if abs(bps) < 1000.0:
            return f"{bps:.{precision}f} {unit}"
        bps /= 1000.0
    return f"{bps:.{precision}f} Pbps"


def calculate_transfer_time(size_bytes: int, bandwidth_bps: float) -> Dict[str, Any]:
    """
    Calculate estimated transfer time.
    
    Args:
        size_bytes: File size in bytes
        bandwidth_bps: Bandwidth in bits per second
    
    Returns:
        Dictionary with time estimates
    
    Example:
        >>> calculate_transfer_time(1048576, 1000000)  # 1MB over 1Mbps
        {'seconds': 8.39, 'formatted': '8.39 seconds'}
    """
    if bandwidth_bps <= 0:
        return {'seconds': float('inf'), 'formatted': '∞'}
    
    # Convert bytes to bits
    size_bits = size_bytes * 8
    seconds = size_bits / bandwidth_bps
    
    if seconds < 60:
        formatted = f"{seconds:.2f} seconds"
    elif seconds < 3600:
        formatted = f"{seconds/60:.2f} minutes"
    else:
        formatted = f"{seconds/3600:.2f} hours"
    
    return {
        'seconds': seconds,
        'minutes': seconds / 60,
        'hours': seconds / 3600,
        'formatted': formatted
    }
